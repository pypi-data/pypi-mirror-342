"""
Model fitting and calibration module for the Voly package.

This module handles fitting volatility models to market data and
calculating fitting statistics.
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional, Union, Any
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from voly.utils.logger import logger, catch_exception
from voly.formulas import get_domain
from voly.exceptions import VolyError
from voly.models import SVIModel
import warnings

warnings.filterwarnings("ignore")


@catch_exception
def fit_model(option_chain: pd.DataFrame,
              domain_params: Tuple[float, float, int] = (-2, 2, 1000)) -> pd.DataFrame:
    """
    Fit a volatility model to market data.

    Parameters:
    - option_chain: DataFrame with market data
    - domain_params: Tuple of (min, max, num_points) for the log-moneyness grid

    Returns:
    - DataFrame with all fit results and performance metrics as columns, maturity_names as index
    """
    # Define column names and their data types
    column_dtypes = {
        's': float,
        'u': float,
        't': float,
        'r': float,
        'oi': float,
        'volume': float,
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
    groups = option_chain.groupby('maturity_date')
    unique_ts = sorted(option_chain['t'].unique())
    maturity_names = [option_chain[option_chain['t'] == t]['maturity_name'].iloc[0] for t in unique_ts]

    # Store results in a dictionary first
    results_data = {col: [] for col in column_dtypes.keys()}

    # ANSI color codes for terminal output
    GREEN, RED, RESET = '\033[32m', '\033[31m', '\033[0m'

    s = option_chain['index_price'].iloc[-1]

    # Dictionary to track fit results by maturity for arbitrage checks
    params_dict = {}

    # Calibrate and check arbitrage
    for t in unique_ts:
        # Get data for this maturity
        maturity_data = option_chain[option_chain['t'] == t]
        maturity_name = maturity_data['maturity_name'].iloc[0]
        maturity_date = maturity_data['maturity_date'].iloc[0]

        logger.info(f"Processing maturity {maturity_date}, t={t:.4f}")

        K = maturity_data['strikes'].values
        iv = maturity_data['mark_iv'].values
        vega = maturity_data['vega'].values if 'vega' in maturity_data.columns else np.ones_like(iv)
        k = np.log(K / s)
        w = (iv ** 2) * t
        mask = ~np.isnan(w) & ~np.isnan(vega) & ~np.isnan(k) & (iv >= 0)
        k, w, vega, iv = k[mask], w[mask], vega[mask], iv[mask]

        logger.info(f"Points after filtering: {len(k)}")

        params = [np.nan] * 5
        loss = np.inf
        nu = psi = p = c = nu_tilde = np.nan
        rmse = mae = r2 = max_error = np.nan
        butterfly_arbitrage_free = True
        u = s  # Assume underlying_price is index_price
        r = maturity_data['interest_rate'].iloc[0] if 'interest_rate' in maturity_data.columns else 0
        oi = maturity_data['open_interest'].sum() if 'open_interest' in maturity_data.columns else 0
        volume = maturity_data['volume'].sum() if 'volume' in maturity_data.columns else 0
        log_min_strike = usd_min_strike = np.nan

        if len(k) > 5:
            params, loss = SVIModel.fit(tiv=w, vega=vega, k=k, tau=t)
            if not np.isnan(params[0]):
                params_dict[maturity_date] = (t, params)
                a, b, m, rho, sigma = params
                a_scaled, b_scaled = a * t, b * t

                nu, psi, p, c, nu_tilde = SVIModel.raw_to_jw_params(a_scaled, b_scaled, m, rho, sigma, t)

                # Compute fit statistics
                w_model = np.array([SVIModel.svi_raw(x, a_scaled, b_scaled, m, rho, sigma) for x in k])
                iv_model = np.sqrt(w_model / t)
                iv_market = iv
                rmse = np.sqrt(mean_squared_error(iv_market, iv_model))
                mae = mean_absolute_error(iv_market, iv_model)
                r2 = r2_score(iv_market, iv_model)
                max_error = np.max(np.abs(iv_market - iv_model))

                # Compute min strike
                log_min_strike = SVIModel.svi_min_strike(sigma, rho, m)
                usd_min_strike = np.exp(log_min_strike) * s

                # Butterfly arbitrage check
                k_range = np.linspace(min(k), max(k), domain_params[2])
                w_k = lambda k: SVIModel.svi_raw(k, a_scaled, b_scaled, m, rho, sigma)
                w_prime = lambda k: b_scaled * (rho + (k - m) / np.sqrt((k - m) ** 2 + sigma ** 2))
                w_double_prime = lambda k: b_scaled * sigma ** 2 / ((k - m) ** 2 + sigma ** 2) ** (3 / 2)

                for k_val in k_range:
                    wk = w_k(k_val)
                    wp = w_prime(k_val)
                    wpp = w_double_prime(k_val)
                    g = (1 - (k_val * wp) / (2 * wk)) ** 2 - (wp ** 2) / 4 * (1 / wk + 1 / 4) + wpp / 2
                    if g < 0:
                        butterfly_arbitrage_free = False
                        break

        # Log result
        status = f'{GREEN}SUCCESS{RESET}' if not np.isnan(params[0]) else f'{RED}FAILED{RESET}'
        logger.info(f'Optimization for {maturity_name}: {status}')
        if not np.isnan(params[0]):
            logger.info(
                f"Maturity {maturity_name}: a={a_scaled:.4f}, b={b_scaled:.4f}, m={m:.4f}, rho={rho:.4f}, sigma={sigma:.4f}")
        logger.info("=================================================================")

        results_data['s'].append(float(s))
        results_data['u'].append(float(u))
        results_data['t'].append(float(t))
        results_data['r'].append(float(r))
        results_data['oi'].append(float(oi))
        results_data['volume'].append(float(volume))
        results_data['maturity_date'].append(maturity_date)
        results_data['a'].append(float(a_scaled) if not np.isnan(params[0]) else np.nan)
        results_data['b'].append(float(b_scaled) if not np.isnan(params[0]) else np.nan)
        results_data['m'].append(float(m))
        results_data['rho'].append(float(rho))
        results_data['sigma'].append(float(sigma))
        results_data['nu'].append(float(nu))
        results_data['psi'].append(float(psi))
        results_data['p'].append(float(p))
        results_data['c'].append(float(c))
        results_data['nu_tilde'].append(float(nu_tilde))
        results_data['log_min_strike'].append(float(log_min_strike))
        results_data['usd_min_strike'].append(float(usd_min_strike))
        results_data['fit_success'].append(bool(not np.isnan(params[0])))
        results_data['butterfly_arbitrage_free'].append(butterfly_arbitrage_free)
        results_data['calendar_arbitrage_free'].append(True)  # Updated after check
        results_data['rmse'].append(float(rmse))
        results_data['mae'].append(float(mae))
        results_data['r2'].append(float(r2))
        results_data['max_error'].append(float(max_error))
        results_data['loss'].append(float(loss))
        results_data['n_points'].append(int(len(k)))

    # Create results DataFrame
    results_df = pd.DataFrame(results_data, index=maturity_names)

    # Convert columns to appropriate types
    for col, dtype in column_dtypes.items():
        if col in results_df.columns:
            try:
                results_df[col] = results_df[col].astype(dtype)
            except (ValueError, TypeError) as e:
                logger.warning(f"Could not convert column {col} to {dtype}: {e}")

    # Calendar arbitrage check (pre-correction)
    logger.info("\nChecking calendar arbitrage (pre-correction)...")
    k_grid = np.linspace(domain_params[0], domain_params[1], domain_params[2])
    sorted_maturities = sorted(params_dict.keys(), key=lambda x: params_dict[x][0])
    calendar_arbitrage_free = True

    for i in range(len(sorted_maturities) - 1):
        mat1, mat2 = sorted_maturities[i], sorted_maturities[i + 1]
        t1, params1 = params_dict[mat1]
        t2, params2 = params_dict[mat2]
        a1, b1, m1, rho1, sigma1 = params1
        a2, b2, m2, rho2, sigma2 = params2

        if np.isnan(a1) or np.isnan(a2):
            continue

        group = groups.get_group(mat2)
        K = group['strikes'].values
        s = group['index_price'].iloc[0]
        k_market = np.log(K / s)
        mask = ~np.isnan(k_market)
        k_check = np.unique(
            np.concatenate([k_market[mask], np.linspace(min(k_market[mask]), max(k_market[mask]), domain_params[2])]))

        for k_val in k_check:
            w1 = SVIModel.svi_raw(k_val, a1 * t1, b1 * t1, m1, rho1, sigma1)
            w2 = SVIModel.svi_raw(k_val, a2 * t2, b2 * t2, m2, rho2, sigma2)
            if w2 < w1 - 1e-6:
                logger.warning(
                    f"Calendar arbitrage violation at t1={t1:.4f}, t2={t2:.4f}, k={k_val:.4f}: w1={w1:.6f}, w2={w2:.6f}")
                calendar_arbitrage_free = False
                break
        if not calendar_arbitrage_free:
            break

    for mat in sorted_maturities:
        idx = None
        for i, maturity_name in enumerate(maturity_names):
            if results_df.iloc[i]['maturity_date'] == mat:
                idx = results_df.index[i]
                break
        if idx is not None:
            results_df.at[idx, 'calendar_arbitrage_free'] = calendar_arbitrage_free

    # Calendar arbitrage correction
    if not calendar_arbitrage_free:
        logger.info("\nPerforming calendar arbitrage correction...")
        for i in range(1, len(sorted_maturities)):
            mat2 = sorted_maturities[i]
            mat1 = sorted_maturities[i - 1]
            t2, params2 = params_dict[mat2]
            t1, params1 = params_dict[mat1]

            if np.any(np.isnan(params2)) or np.any(np.isnan(params1)):
                continue

            group = groups.get_group(mat2)
            s = group['index_price'].iloc[0]
            K = group['strikes'].values
            iv = group['mark_iv'].values
            vega = group['vega'].values if 'vega' in group.columns else np.ones_like(iv)
            k = np.log(K / s)
            w = (iv ** 2) * t2
            mask = ~np.isnan(w) & ~np.isnan(vega) & ~np.isnan(k) & (iv >= 0)
            k, w, vega, iv = k[mask], w[mask], vega[mask], iv[mask]

            new_params = SVIModel.correct_calendar_arbitrage(
                params=params2, t=t2, tiv=w, vega=vega, k=k,
                prev_params=params1, prev_t=t1, k_grid=k_grid
            )

            params_dict[mat2] = (t2, new_params)

            a, b, m, rho, sigma = new_params
            a_scaled, b_scaled = a * t2, b * t2
            nu, psi, p, c, nu_tilde = SVIModel.raw_to_jw_params(a_scaled, b_scaled, m, rho, sigma, t2)

            # Recompute fit statistics
            w_model = np.array([SVIModel.svi_raw(x, a_scaled, b_scaled, m, rho, sigma) for x in k])
            iv_model = np.sqrt(w_model / t2)
            iv_market = iv
            rmse = np.sqrt(mean_squared_error(iv_market, iv_model))
            mae = mean_absolute_error(iv_market, iv_model)
            r2 = r2_score(iv_market, iv_model)
            max_error = np.max(np.abs(iv_market - iv_model))

            # Recompute min strike
            log_min_strike = SVIModel.svi_min_strike(sigma, rho, m)
            usd_min_strike = np.exp(log_min_strike) * s

            # Update butterfly arbitrage check
            butterfly_arbitrage_free = True
            k_range = np.linspace(min(k), max(k), domain_params[2])
            w_k = lambda k: SVIModel.svi_raw(k, a_scaled, b_scaled, m, rho, sigma)
            w_prime = lambda k: b_scaled * (rho + (k - m) / np.sqrt((k - m) ** 2 + sigma ** 2))
            w_double_prime = lambda k: b_scaled * sigma ** 2 / ((k - m) ** 2 + sigma ** 2) ** (3 / 2)

            for k_val in k_range:
                wk = w_k(k_val)
                wp = w_prime(k_val)
                wpp = w_double_prime(k_val)
                g = (1 - (k_val * wp) / (2 * wk)) ** 2 - (wp ** 2) / 4 * (1 / wk + 1 / 4) + wpp / 2
                if g < 0:
                    butterfly_arbitrage_free = False
                    break

            # Find the correct index to update
            idx = None
            for j, maturity_name in enumerate(maturity_names):
                if results_df.iloc[j]['maturity_date'] == mat2:
                    idx = results_df.index[j]
                    break

            if idx is not None:
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
                results_df.at[idx, 'rmse'] = float(rmse)
                results_df.at[idx, 'mae'] = float(mae)
                results_df.at[idx, 'r2'] = float(r2)
                results_df.at[idx, 'max_error'] = float(max_error)
                results_df.at[idx, 'log_min_strike'] = float(log_min_strike)
                results_df.at[idx, 'usd_min_strike'] = float(usd_min_strike)
                results_df.at[idx, 'butterfly_arbitrage_free'] = butterfly_arbitrage_free
                results_df.at[idx, 'fit_success'] = bool(not np.isnan(a))

        # Calendar arbitrage check (post-correction)
        logger.info("\nChecking calendar arbitrage (post-correction)...")
        calendar_arbitrage_free = True
        for i in range(len(sorted_maturities) - 1):
            mat1, mat2 = sorted_maturities[i], sorted_maturities[i + 1]
            t1, params1 = params_dict[mat1]
            t2, params2 = params_dict[mat2]
            a1, b1, m1, rho1, sigma1 = params1
            a2, b2, m2, rho2, sigma2 = params2

            if np.isnan(a1) or np.isnan(a2):
                continue

            group = groups.get_group(mat2)
            K = group['strikes'].values
            s = group['index_price'].iloc[0]
            k_market = np.log(K / s)
            mask = ~np.isnan(k_market)
            k_check = np.unique(np.concatenate(
                [k_market[mask], np.linspace(min(k_market[mask]), max(k_market[mask]), domain_params[2])]))

            for k_val in k_check:
                w1 = SVIModel.svi_raw(k_val, a1 * t1, b1 * t1, m1, rho1, sigma1)
                w2 = SVIModel.svi_raw(k_val, a2 * t2, b2 * t2, m2, rho2, sigma2)
                if w2 < w1 - 1e-6:
                    logger.warning(
                        f"Calendar arbitrage violation at t1={t1:.4f}, t2={t2:.4f}, k={k_val:.4f}: w1={w1:.6f}, w2={w2:.6f}")
                    calendar_arbitrage_free = False
                    break
            if not calendar_arbitrage_free:
                break

        for mat in sorted_maturities:
            idx = None
            for j, maturity_name in enumerate(maturity_names):
                if results_df.iloc[j]['maturity_date'] == mat:
                    idx = results_df.index[j]
                    break
            if idx is not None:
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
