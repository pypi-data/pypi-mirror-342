"""
Model fitting and calibration module for the Voly package.

This module handles fitting volatility models to market data and
calculating fitting statistics.
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional, Union, Any
from scipy.optimize import least_squares
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from voly.utils.logger import logger, catch_exception
from voly.formulas import get_domain
from voly.exceptions import VolyError
from voly.models import SVIModel
import warnings

warnings.filterwarnings("ignore")


@catch_exception
def fit_model(option_chain: pd.DataFrame,
              domain_params: Tuple[float, float, int] = (-1.5, 1.5, 1000)) -> pd.DataFrame:
    """
    Fit Voly's volatility model to market data.

    Parameters:
    - option_chain: DataFrame with market data
    - domain_params : Tuple[float, float, int]
        (min_log_moneyness, max_log_moneyness, num_points)

    Returns:
    - DataFrame with all fit results and performance metrics as columns, maturity_names as index
    """

    # Define column names and their data types
    column_dtypes = {
        's': float,
        't': float,
        'r': float,
        'maturity_date': 'datetime64[ns]',
        'a': float,
        'b': float,
        'm': float,
        'rho': float,
        'sigma': float,
        'nu': float,
        'psi': float,
        'p': float,
        'c': float,
        'nu_tilde': float,
        'log_min_strike': float,
        'usd_min_strike': float,
        'fit_success': bool,
        'butterfly_arbitrage_free': bool,
        'calendar_arbitrage_free': bool,
        'loss': float,
        'rmse': float,
        'mae': float,
        'r2': float,
        'max_error': float,
        'n_points': int
    }

    # Get unique maturities and sort them
    unique_ts = sorted(option_chain['t'].unique())
    maturity_names = [option_chain[option_chain['t'] == t]['maturity_name'].iloc[0] for t in unique_ts]

    # Store results in a dictionary first
    results_data = {col: [] for col in column_dtypes.keys()}

    # ANSI color codes for terminal output
    GREEN, RED, RESET = '\033[32m', '\033[31m', '\033[0m'

    s = option_chain['index_price'].iloc[-1]

    # Dictionary to track fit results by maturity for arbitrage checks
    fit_params_dict = {}

    # First pass: Fit each maturity
    for t in unique_ts:
        # Get data for this maturity
        maturity_data = option_chain[option_chain['t'] == t]
        maturity_name = maturity_data['maturity_name'].iloc[0]
        maturity_date = maturity_data['maturity_date'].iloc[0]

        logger.info(f"Optimizing for {maturity_name}...")

        # Extract data for fitting
        k = maturity_data['log_moneyness'].values
        iv = maturity_data['mark_iv'].values
        vega = maturity_data['vega'].values if 'vega' in maturity_data else np.ones_like(iv)

        # Apply mask to filter out invalid data
        mask = ~np.isnan(iv) & ~np.isnan(k) & (iv > 0)
        k_masked, iv_masked, vega_masked = k[mask], iv[mask], vega[mask]

        # Check if we have enough valid points
        if len(k_masked) <= 5:
            logger.warning(f"Not enough valid data points for {maturity_name}, skipping.")
            params = [np.nan] * 5
            loss = np.inf
        else:
            # Calculate total implied variance (w = iv² * t)
            w = (iv_masked ** 2) * t

            # Fit using the improved SVI method
            params, loss = SVIModel.fit(tiv=w, vega=vega_masked, k=k_masked, tau=t)

        # Store the parameters for this maturity
        fit_params_dict[maturity_date] = (t, params)

        # Extract parameters (will be nan if fit failed)
        a, b, m, rho, sigma = params

        # Calculate statistics
        fit_success = not np.isnan(a)
        butterfly_arbitrage_free = True
        calendar_arbitrage_free = True  # Will check later

        # Initialize default metrics
        rmse = mae = r2 = max_error = np.nan
        nu = psi = p = c = nu_tilde = np.nan
        log_min_strike = usd_min_strike = np.nan
        a_scaled = b_scaled = np.nan

        if fit_success:
            # Scale a and b by t
            a_scaled, b_scaled = a * t, b * t

            # Calculate Jump-Wing parameters
            nu, psi, p, c, nu_tilde = SVIModel.raw_to_jw_params(a_scaled, b_scaled, m, rho, sigma, t)

            # Calculate model predictions for statistics
            w_model = np.array([SVIModel.svi_raw(x, a_scaled, b_scaled, m, rho, sigma) for x in k_masked])
            iv_model = np.sqrt(w_model / t)
            iv_market = iv_masked

            # Calculate statistics
            rmse = np.sqrt(mean_squared_error(iv_market, iv_model))
            mae = mean_absolute_error(iv_market, iv_model)
            r2 = r2_score(iv_market, iv_model)
            max_error = np.max(np.abs(iv_market - iv_model))

            # Calculate minimum strike
            log_min_strike = SVIModel.svi_min_strike(sigma, rho, m)
            usd_min_strike = s * np.exp(-log_min_strike)  # Convert from log_moneyness to strike

            # Check butterfly arbitrage
            k_range = np.linspace(min(k_masked), max(k_masked), domain_params[2])
            for k_val in k_range:
                wk = SVIModel.svi_raw(k_val, a_scaled, b_scaled, m, rho, sigma)
                wp = SVIModel.svi_d(k_val, a_scaled, b_scaled, m, rho, sigma)
                wpp = SVIModel.svi_dd(k_val, a_scaled, b_scaled, m, rho, sigma)
                g = (1 - (k_val * wp) / (2 * wk)) ** 2 - (wp ** 2) / 4 * (1 / wk + 1 / 4) + wpp / 2
                if g < 0:
                    butterfly_arbitrage_free = False
                    break

        r = maturity_data['interest_rate'].iloc[0] if 'interest_rate' in maturity_data.columns else 0

        # Store values in the results dictionary with proper types
        results_data['s'].append(float(s))
        results_data['t'].append(float(t))
        results_data['r'].append(float(r))
        results_data['maturity_date'].append(maturity_date)
        results_data['a'].append(float(a_scaled) if fit_success else np.nan)
        results_data['b'].append(float(b_scaled) if fit_success else np.nan)
        results_data['sigma'].append(float(sigma) if fit_success else np.nan)
        results_data['m'].append(float(m) if fit_success else np.nan)
        results_data['rho'].append(float(rho) if fit_success else np.nan)
        results_data['nu'].append(float(nu))
        results_data['psi'].append(float(psi))
        results_data['p'].append(float(p))
        results_data['c'].append(float(c))
        results_data['nu_tilde'].append(float(nu_tilde))
        results_data['log_min_strike'].append(float(log_min_strike))
        results_data['usd_min_strike'].append(float(usd_min_strike))
        results_data['fit_success'].append(bool(fit_success))
        results_data['butterfly_arbitrage_free'].append(bool(butterfly_arbitrage_free))
        results_data['calendar_arbitrage_free'].append(bool(True))  # Will update in second pass
        results_data['loss'].append(float(loss))
        results_data['rmse'].append(float(rmse))
        results_data['mae'].append(float(mae))
        results_data['r2'].append(float(r2))
        results_data['max_error'].append(float(max_error))
        results_data['n_points'].append(int(len(k_masked)))

        # Log result
        status = f'{GREEN}SUCCESS{RESET}' if fit_success else f'{RED}FAILED{RESET}'
        logger.info(f'Optimization for {maturity_name}: {status}')
        logger.info('-------------------------------------')

    # Create DataFrame with proper types
    results_df = pd.DataFrame(results_data, index=maturity_names)

    # Convert columns to appropriate types
    for col, dtype in column_dtypes.items():
        if col in results_df.columns:
            try:
                results_df[col] = results_df[col].astype(dtype)
            except (ValueError, TypeError) as e:
                logger.warning(f"Could not convert column {col} to {dtype}: {e}")

    # Second pass: Check and correct for calendar arbitrage
    logger.info("Checking for calendar arbitrage...")
    sorted_maturities = sorted(fit_params_dict.keys())
    k_grid = np.linspace(domain_params[0], domain_params[1], domain_params[2])  # Grid for arbitrage checking

    # Check calendar arbitrage before correction
    calendar_arbitrage_free = True
    for i in range(len(sorted_maturities) - 1):
        mat1, mat2 = sorted_maturities[i], sorted_maturities[i + 1]
        t1, params1 = fit_params_dict[mat1]
        t2, params2 = fit_params_dict[mat2]
        a1, b1, sigma1, rho1, m1 = params1
        a2, b2, sigma2, rho2, m2 = params2

        if np.isnan(a1) or np.isnan(a2):
            continue

        # Check arbitrage on a grid of points
        for k_val in k_grid:
            w1 = SVIModel.svi_raw(k_val, a1 * t1, b1 * t1, m1, rho1, sigma1)
            w2 = SVIModel.svi_raw(k_val, a2 * t2, b2 * t2, m2, rho2, sigma2)
            if w2 < w1 - 1e-6:
                calendar_arbitrage_free = False
                logger.warning(
                    f"Calendar arbitrage detected between {sorted_maturities[i]} and {sorted_maturities[i + 1]}")
                break

    # Update results with calendar arbitrage status
    for i, maturity_name in enumerate(maturity_names):
        idx = results_df.index[i]
        results_df.at[idx, 'calendar_arbitrage_free'] = calendar_arbitrage_free

    # Correct calendar arbitrage if needed
    if not calendar_arbitrage_free:
        logger.info("Correcting calendar arbitrage...")
        for i in range(1, len(sorted_maturities)):
            mat1 = sorted_maturities[i - 1]
            mat2 = sorted_maturities[i]
            t1, params1 = fit_params_dict[mat1]
            t2, params2 = fit_params_dict[mat2]

            if np.isnan(params1[0]) or np.isnan(params2[0]):
                continue

            # Find the index in maturity_names that corresponds to mat2
            maturity_idx = None
            for j, maturity_name in enumerate(maturity_names):
                if results_df.iloc[j]['maturity_date'] == mat2:
                    maturity_idx = j
                    break

            if maturity_idx is None:
                continue

            # Get data for correction
            idx = results_df.index[maturity_idx]
            maturity_data = option_chain[option_chain['maturity_name'] == idx]
            k = maturity_data['log_moneyness'].values
            iv = maturity_data['mark_iv'].values
            vega = maturity_data['vega'].values if 'vega' in maturity_data else np.ones_like(iv)

            # Apply mask to filter out invalid data
            mask = ~np.isnan(iv) & ~np.isnan(k) & (iv > 0)
            k_masked, iv_masked, vega_masked = k[mask], iv[mask], vega[mask]

            if len(k_masked) <= 5:
                continue

            # Calculate total implied variance
            w = (iv_masked ** 2) * t2

            # Apply calendar arbitrage correction
            new_params = SVIModel.correct_calendar_arbitrage(
                params=params2, t=t2, tiv=w, vega=vega_masked, k=k_masked,
                prev_params=params1, prev_t=t1, k_grid=k_grid
            )

            # Update the parameters dictionary
            fit_params_dict[mat2] = (t2, new_params)

            # Extract corrected parameters
            a, b, m, rho, sigma = new_params

            # Calculate scaled parameters and Jump-Wing parameters
            a_scaled, b_scaled = a * t2, b * t2
            nu, psi, p, c, nu_tilde = SVIModel.raw_to_jw_params(a_scaled, b_scaled, m, rho, sigma, t2)

            # Calculate model predictions for statistics
            w_model = np.array([SVIModel.svi_raw(x, a_scaled, b_scaled, m, rho, sigma) for x in k_masked])
            iv_model = np.sqrt(w_model / t2)
            iv_market = iv_masked

            # Calculate statistics
            rmse = np.sqrt(mean_squared_error(iv_market, iv_model))
            mae = mean_absolute_error(iv_market, iv_model)
            r2 = r2_score(iv_market, iv_model)
            max_error = np.max(np.abs(iv_market - iv_model))

            # Calculate minimum strike
            log_min_strike = SVIModel.svi_min_strike(sigma, rho, m)
            usd_min_strike = s * np.exp(-log_min_strike)

            # Check butterfly arbitrage
            butterfly_arbitrage_free = True
            k_range = np.linspace(min(k_masked), max(k_masked), domain_params[2])
            for k_val in k_range:
                wk = SVIModel.svi_raw(k_val, a_scaled, b_scaled, m, rho, sigma)
                wp = SVIModel.svi_d(k_val, a_scaled, b_scaled, m, rho, sigma)
                wpp = SVIModel.svi_dd(k_val, a_scaled, b_scaled, m, rho, sigma)
                g = (1 - (k_val * wp) / (2 * wk)) ** 2 - (wp ** 2) / 4 * (1 / wk + 1 / 4) + wpp / 2
                if g < 0:
                    butterfly_arbitrage_free = False
                    break

            # Update results in the DataFrame
            results_df.at[idx, 'a'] = float(a_scaled)
            results_df.at[idx, 'b'] = float(b_scaled)
            results_df.at[idx, 'm'] = float(m)
            results_df.at[idx, 'rho'] = float(rho)
            results_df.at[idx, 'sigma'] = float(sigma)
            results_df.at[idx, 'nu'] = float(nu)
            results_df.at[idx, 'psi'] = float(psi)
            results_df.at[idx, 'p'] = float(p)
            results_df.at[idx, 'c'] = float(c)
            results_df.at[idx, 'nu_tilde'] = float(nu_tilde)
            results_df.at[idx, 'log_min_strike'] = float(log_min_strike)
            results_df.at[idx, 'usd_min_strike'] = float(usd_min_strike)
            results_df.at[idx, 'butterfly_arbitrage_free'] = bool(butterfly_arbitrage_free)
            results_df.at[idx, 'rmse'] = float(rmse)
            results_df.at[idx, 'mae'] = float(mae)
            results_df.at[idx, 'r2'] = float(r2)
            results_df.at[idx, 'max_error'] = float(max_error)

            logger.info(
                f"SVI parameters for {idx}: a={a_scaled:.4f}, b={b_scaled:.4f}, sigma={sigma:.4f}, rho={rho:.4f}, m={m:.4f}")

        # Check calendar arbitrage after correction
        calendar_arbitrage_free = True
        for i in range(len(sorted_maturities) - 1):
            mat1, mat2 = sorted_maturities[i], sorted_maturities[i + 1]
            t1, params1 = fit_params_dict[mat1]
            t2, params2 = fit_params_dict[mat2]
            a1, b1, sigma1, rho1, m1 = params1
            a2, b2, sigma2, rho2, m2 = params2

            if np.isnan(a1) or np.isnan(a2):
                continue

            # Check arbitrage on a grid of points
            for k_val in k_grid:
                w1 = SVIModel.svi_raw(k_val, a1 * t1, b1 * t1, m1, rho1, sigma1)
                w2 = SVIModel.svi_raw(k_val, a2 * t2, b2 * t2, m2, rho2, sigma2)
                if w2 < w1 - 1e-6:
                    calendar_arbitrage_free = False
                    logger.warning(f"Calendar arbitrage still detected between {mat1} and {mat2} after correction")
                    break

        # Update results with final calendar arbitrage status
        for i, maturity_name in enumerate(maturity_names):
            maturity_date = results_df.iloc[i]['maturity_date']
            idx = results_df.index[i]
            results_df.at[idx, 'calendar_arbitrage_free'] = calendar_arbitrage_free

    logger.info("Model fitting complete.")
    return results_df


@catch_exception
def get_iv_surface(model_results: pd.DataFrame,
                   domain_params: Tuple[float, float, int] = (-1.5, 1.5, 1000),
                   return_domain: str = 'log_moneyness') -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    """
    Generate implied volatility surface using optimized SVI parameters.

    Works with both regular fit_results and interpolated_results dataframes.

    Parameters:
    - model_results: DataFrame from fit_model() or interpolate_model(). Maturity names or DTM as Index
    - domain_params: Tuple of (min, max, num_points) for the log-moneyness array
    - return_domain: Domain for x-axis values ('log_moneyness', 'moneyness', 'returns', 'strikes', 'delta')

    Returns:
    - Tuple of (iv_surface, x_surface)
      iv_surface: Dictionary mapping maturity/dtm names to IV arrays
      x_surface: Dictionary mapping maturity/dtm names to requested x domain arrays
    """
    # Check if required columns are present
    required_columns = ['a', 'b', 'm', 'rho', 'sigma', 't']
    missing_columns = [col for col in required_columns if col not in model_results.columns]
    if missing_columns:
        raise VolyError(f"Required columns missing in model_results: {missing_columns}")

    # Generate implied volatility surface in log-moneyness domain
    LM = np.linspace(domain_params[0], domain_params[1], domain_params[2])

    iv_surface = {}
    x_surface = {}

    # Process each maturity/dtm
    for i in model_results.index:
        # Calculate SVI total implied variance and convert to IV
        params = [
            model_results.loc[i, 'a'],
            model_results.loc[i, 'b'],
            model_results.loc[i, 'm'],
            model_results.loc[i, 'rho'],
            model_results.loc[i, 'sigma']
        ]
        s = model_results.loc[i, 's']
        r = model_results.loc[i, 'r']
        t = model_results.loc[i, 't']

        # Calculate implied volatility
        w = np.array([SVIModel.svi_raw(x, *params) for x in LM])
        o = np.sqrt(w / t)
        iv_surface[i] = o

        # Calculate x domain for this maturity/dtm
        x = get_domain(domain_params, s, r, o, t, return_domain)
        x_surface[i] = x

    return iv_surface, x_surface
