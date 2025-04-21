"""
Volatility models for the Voly package.
"""

import numpy as np
from numpy.linalg import solve
from scipy.optimize import minimize
from typing import Tuple, Dict, List, Optional, Union


class SVIModel:
    """
    Stochastic Volatility Inspired (SVI) model.

    This class provides methods for calculating implied volatility using the
    SVI parameterization, as well as its derivatives and related functions.
    """

    # Parameter names for reference
    PARAM_NAMES = ['a', 'b', 'm', 'rho', 'sigma']
    JW_PARAM_NAMES = ['nu', 'psi', 'p', 'c', 'nu_tilde']

    # Parameter descriptions for documentation
    PARAM_DESCRIPTIONS = {
        'a': 'Base level of total implied variance',
        'b': 'Volatility skewness/smile modulation (controls wing slopes)',
        'sigma': 'Convexity control of the volatility smile (reduces ATM curvature)',
        'rho': 'Skewness/slope of the volatility smile (-1 to 1, rotates smile)',
        'm': 'Horizontal shift of the smile peak',
        'nu': 'ATM variance (level of ATM volatility)',
        'psi': 'ATM volatility skew (affects the gradient of the curve at ATM point)',
        'p': 'Slope of put wing (left side of curve)',
        'c': 'Slope of call wing (right side of curve)',
        'nu_tilde': 'Minimum implied total variance',
    }

    @staticmethod
    def svi_raw(k, a, b, m, rho, sigma):
        assert b >= 0, 'b must be non-negative'
        assert abs(rho) <= 1, '|rho| must be <= 1'
        assert sigma >= 0, 'sigma must be non-negative'
        assert a + b * sigma * sqrt(1 - rho ** 2) >= 0, 'a + b*sigma*sqrt(1-rho^2) must be non-negative'
        return a + b * (rho * (k - m) + sqrt((k - m) ** 2 + sigma ** 2))

    @staticmethod
    def svi(LM: float, a: float, b: float, sigma: float, rho: float, m: float) -> float:
        return a + b * (rho * (LM - m) + np.sqrt((LM - m) ** 2 + sigma ** 2))

    @staticmethod
    def raw_to_jw_params(a: float, b: float, m: float, rho: float, sigma: float, t: float) -> Tuple[
        float, float, float, float, float]:
        nu = (a + b * ((-rho) * m + np.sqrt(m ** 2 + sigma ** 2))) / t
        psi = (1 / np.sqrt(nu * t)) * (b / 2) * (rho - (m / np.sqrt(m ** 2 + sigma ** 2)))
        p = (1 / np.sqrt(nu * t)) * b * (1 - rho)
        c = (1 / np.sqrt(nu * t)) * b * (1 + rho)
        nu_tilde = (1 / t) * (a + b * sigma * np.sqrt(1 - rho ** 2))
        return nu, psi, p, c, nu_tilde

    @classmethod
    def calibration(cls, tiv, vega, k, m, sigma):
        """
        Calibrate SVI parameters using a more stable approach.

        Parameters:
        - tiv: Total implied variance values
        - vega: Option vega values (for weighting)
        - k: Log-moneyness values
        - m: Horizontal shift parameter
        - sigma: Convexity parameter

        Returns:
        - c, d, a: Calibrated parameters
        - loss: Calibration loss value
        """
        sigma = max(sigma, 0.001)
        vega = vega / vega.max() if vega.max() > 0 else np.ones_like(vega)
        y = (k - m) / sigma
        w = vega.mean()
        y1 = (vega * y).mean()
        y2 = (vega * y * y).mean()
        y3 = (vega * np.sqrt(y * y + 1)).mean()
        y4 = (vega * y * np.sqrt(y * y + 1)).mean()
        y5 = (vega * (y * y + 1)).mean()
        vy2 = (vega * tiv * np.sqrt(y * y + 1)).mean()
        vy = (vega * tiv * y).mean()
        v = (vega * tiv).mean()

        matrix = [[y5, y4, y3], [y4, y2, y1], [y3, y1, w]]
        vector = [vy2, vy, v]
        c, d, a = solve(np.array(matrix), np.array(vector))

        c = np.clip(c, 0, 4 * sigma)
        a = max(a, 1e-6)
        d = np.clip(d, -min(c, 4 * sigma - c), min(c, 4 * sigma - c))

        loss = cls.loss(tiv, vega, y, c, d, a)
        return c, d, a, loss

    @staticmethod
    def loss(tiv, vega, y, c, d, a):
        """Calculate weighted loss for SVI calibration."""
        diff = tiv - (a + d * y + c * np.sqrt(y * y + 1))
        return (vega * diff * diff).mean()

    @classmethod
    def fit(cls, tiv, vega, k, tau=1.0):
        """
        Fit SVI model to market data using a more stable two-step approach.

        Parameters:
        - tiv: Total implied variance values
        - vega: Option vega values (for weighting)
        - k: Log-moneyness values
        - tau: Time to expiry in years

        Returns:
        - params: [a, b, m, rho, sigma] parameters
        - loss: Fitting loss value
        """
        if len(k) <= 5:
            return [np.nan] * 5, np.inf

        vega = vega / vega.max() if vega.max() > 0 else np.ones_like(vega)
        m_init = np.mean(k)
        sigma_init = max(0.1, np.std(k) * 0.1)

        def score(params):
            sigma, m = params
            c, d, a_calib, loss = cls.calibration(tiv, vega, k, m, sigma)
            return loss

        result = minimize(score, [sigma_init, m_init], bounds=[(0.001, None), (None, None)],
                          tol=1e-16, method="Nelder-Mead", options={'maxfun': 5000})

        sigma, m = result.x
        c, d, a_calib, loss = cls.calibration(tiv, vega, k, m, sigma)
        a_calib = max(a_calib, 1e-6)

        if c != 0:
            a_svi = a_calib / tau
            rho_svi = d / c
            b_svi = c / (sigma * tau)
        else:
            a_svi = a_calib / tau
            rho_svi = b_svi = 0

        return [a_svi, b_svi, m, rho_svi, sigma], loss

    @classmethod
    def correct_calendar_arbitrage(cls, params, t, tiv, vega, k, prev_params, prev_t, domain_params):
        """
        Correct calendar arbitrage by ensuring the current SVI surface stays above the previous one.

        Parameters:
        - params: Current SVI parameters [a, b, sigma, rho, m]
        - t: Current time to expiry
        - tiv: Current total implied variance values
        - vega: Current vega values
        - k: Current log-moneyness values
        - prev_params: Previous SVI parameters
        - prev_t: Previous time to expiry
        - k_grid: Grid of log-moneyness values for arbitrage checking

        Returns:
        - New arbitrage-free parameters
        """

        if np.any(np.isnan(params)) or np.any(np.isnan(prev_params)):
            return params

        a_init, b_init, sigma_init, rho_init, m_init = params
        a_prev, b_prev, sigma_prev, rho_prev, m_prev = prev_params
        k_constraint = np.unique(np.concatenate([k, np.linspace(min(k), max(k), domain_params[2])]))

        def objective(x):
            a, b, sigma, rho, m = x
            w_model = cls.svi(k, a * t, b * t, sigma, rho, m)
            fit_loss = ((w_model - tiv) ** 2 * vega).mean()
            param_deviation = sum(((x[i] - params[i]) / max(abs(params[i]), 1e-6)) ** 2
                                  for i in range(len(params)))
            return fit_loss + 0.01 * param_deviation

        def calendar_constraint(x):
            a, b, sigma, rho, m = x
            w_current = cls.svi(k_constraint, a * t, b * t, sigma, rho, m)
            w_prev = cls.svi(k_constraint, a_prev * prev_t, b_prev * prev_t, sigma_prev, rho_prev, m_prev)
            return w_current - w_prev

        bounds = [
            (max(a_init * 0.8, 1e-6), a_init * 1.2),
            (max(b_init * 0.8, 0), b_init * 1.2),
            (max(sigma_init * 0.8, 1e-6), sigma_init * 1.2),
            (max(rho_init - 0.05, -1), min(rho_init + 0.05, 1)),
            (m_init - 0.05, m_init + 0.05)
        ]

        constraints = [
            {'type': 'ineq', 'fun': calendar_constraint},
            {'type': 'ineq', 'fun': lambda x: x[0] + x[1] * x[2] * np.sqrt(1 - x[3] ** 2)}
        ]

        result = minimize(
            objective, [a_init, b_init, sigma_init, rho_init, m_init],
            bounds=bounds, constraints=constraints, method='SLSQP',
            options={'disp': False, 'maxiter': 1000, 'ftol': 1e-8}
        )

        if result.success:
            return result.x

        return params


# Models dictionary for easy access
MODELS = {
    'svi': SVIModel,
}
