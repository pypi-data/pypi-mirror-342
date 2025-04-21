"""
Volatility models for the Voly package.
"""

import numpy as np
from numpy.linalg import solve
from typing import Tuple, Dict, List, Optional, Union


class SVIModel:
    """
    Stochastic Volatility Inspired (SVI) model.
    """

    # Parameter names for reference
    PARAM_NAMES = ['a', 'b', 'm', 'rho', 'sigma']
    JW_PARAM_NAMES = ['nu', 'psi', 'p', 'c', 'nu_tilde']

    # Parameter descriptions for documentation
    PARAM_DESCRIPTIONS = {
        'a': 'Base level of total implied variance',
        'b': 'Volatility skewness/smile modulation (controls wing slopes)',
        'm': 'Horizontal shift of the smile peak',
        'rho': 'Skewness/slope of the volatility smile (-1 to 1, rotates smile)',
        'sigma': 'Convexity control of the volatility smile (reduces ATM curvature)',
        'nu': 'ATM variance (level of ATM volatility)',
        'psi': 'ATM volatility skew (affects the gradient of the curve at ATM point)',
        'p': 'Slope of put wing (left side of curve)',
        'c': 'Slope of call wing (right side of curve)',
        'nu_tilde': 'Minimum implied total variance',
    }

    @staticmethod
    def svi_raw(k, a, b, m, rho, sigma):
        assert b >= 0 and abs(rho) <= 1 and sigma >= 0 and a + b * sigma * np.sqrt(1 - rho ** 2) >= 0
        return a + b * (rho * (k - m) + np.sqrt((k - m) ** 2 + sigma ** 2))

    @staticmethod
    def svi_min_strike(sigma: float, rho: float, m: float) -> float:
        """Calculate the minimum valid log-strike for this SVI parameterization."""
        return m - ((sigma * rho) / np.sqrt(1 - rho ** 2))

    @staticmethod
    def raw_to_jw_params(a: float, b: float, m: float, rho: float, sigma: float, t: float) -> Tuple[
        float, float, float, float, float]:
        """Convert raw SVI parameters to Jump-Wing parameters."""
        nu = (a + b * ((-rho) * m + np.sqrt(m ** 2 + sigma ** 2))) / t
        psi = (1 / np.sqrt(nu * t)) * (b / 2) * (rho - (m / np.sqrt(m ** 2 + sigma ** 2)))
        p = (1 / np.sqrt(nu * t)) * b * (1 - rho)
        c = (1 / np.sqrt(nu * t)) * b * (1 + rho)
        nu_tilde = (1 / t) * (a + b * sigma * np.sqrt(1 - rho ** 2))
        return nu, psi, p, c, nu_tilde

    @classmethod
    def calibration(cls, tiv, vega, k, m, sigma):
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
        diff = tiv - (a + d * y + c * np.sqrt(y * y + 1))
        return (vega * diff * diff).mean()

    @classmethod
    def fit(cls, tiv, vega, k, tau=1.0):
        if len(k) <= 5:
            return [np.nan] * 5, np.inf

        from scipy.optimize import minimize

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
    def correct_calendar_arbitrage(cls, params, t, tiv, vega, k, prev_params, prev_t, k_grid):
        if np.any(np.isnan(params)) or np.any(np.isnan(prev_params)):
            return params

        from scipy.optimize import minimize

        a_init, b_init, m_init, rho_init, sigma_init = params
        a_prev, b_prev, m_prev, rho_prev, sigma_prev = prev_params
        k_constraint = np.unique(np.concatenate([k, np.linspace(min(k), max(k), len(k_grid))]))

        def objective(x):
            a, b, m, rho, sigma = x
            w_model = cls.svi_raw(k, a * t, b * t, m, rho, sigma)
            from sklearn.metrics import mean_squared_error
            fit_loss = mean_squared_error(tiv, w_model, sample_weight=vega)
            param_deviation = sum(((x[i] - x_init) / max(abs(x_init), 1e-6)) ** 2
                                  for i, x_init in enumerate([a_init, b_init, m_init, rho_init, sigma_init]))
            return fit_loss + 0.01 * param_deviation

        def calendar_constraint(x):
            a, b, m, rho, sigma = x
            w_current = cls.svi_raw(k_constraint, a * t, b * t, m, rho, sigma)
            w_prev = cls.svi_raw(k_constraint, a_prev * prev_t, b_prev * prev_t, m_prev, rho_prev, sigma_prev)
            return w_current - w_prev

        bounds = [
            (max(a_init * 0.8, 1e-6), a_init * 1.2),
            (max(b_init * 0.8, 0), b_init * 1.2),
            (m_init - 0.05, m_init + 0.05),
            (max(rho_init - 0.05, -1), min(rho_init + 0.05, 1)),
            (max(sigma_init * 0.8, 1e-6), sigma_init * 1.2)
        ]

        constraints = [
            {'type': 'ineq', 'fun': calendar_constraint},
            {'type': 'ineq', 'fun': lambda x: x[0] + x[1] * x[4] * np.sqrt(1 - x[3] ** 2)}
        ]

        result = minimize(
            objective, [a_init, b_init, m_init, rho_init, sigma_init],
            bounds=bounds, constraints=constraints, method='SLSQP',
            options={'disp': False, 'maxiter': 1000, 'ftol': 1e-8}
        )

        if result.success:
            new_params = result.x
            w_current = cls.svi_raw(k_constraint, new_params[0] * t, new_params[1] * t, *new_params[2:])
            w_prev = cls.svi_raw(k_constraint, a_prev * prev_t, b_prev * prev_t, m_prev, rho_prev, sigma_prev)
            violation = np.min(w_current - w_prev)
            print(f"Calendar arbitrage correction {'successful' if violation >= -1e-6 else 'failed'} for t={t:.4f}, "
                  f"min margin={violation:.6f}")
            return new_params
        print(f"Calendar arbitrage correction failed for t={t:.4f}")
        return params


# Models dictionary for easy access
MODELS = {
    'svi': SVIModel,
}
