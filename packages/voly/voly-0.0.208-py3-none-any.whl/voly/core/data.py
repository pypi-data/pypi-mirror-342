"""
Data fetching and processing module for the Voly package.

This module handles fetching options data from exchanges and processing 
it into a standardized format for further analysis.
"""

import os
import asyncio
import websockets
import json
import pandas as pd
import requests
import time
import datetime as dt
import re
import numpy as np
from typing import List, Dict, Any, Optional, Union
from voly.utils.logger import logger, catch_exception
from voly.exceptions import VolyError


async def subscribe_channels(ws, channels):
    """Helper function to subscribe to a list of channels"""
    await ws.send(json.dumps({
        "jsonrpc": "2.0",
        "method": "public/subscribe",
        "id": 42,
        "params": {"channels": channels}
    }))
    await ws.recv()  # Skip confirmation


async def unsubscribe_channels(ws, channels):
    """Helper function to unsubscribe from a list of channels"""
    await ws.send(json.dumps({
        "jsonrpc": "2.0",
        "method": "public/unsubscribe",
        "id": 43,
        "params": {"channels": channels}
    }))
    await ws.recv()  # Skip confirmation


@catch_exception
async def process_batch(ws, batch: List[str], batch_num: int, total_batches: int) -> List[Dict[str, Any]]:
    """Process a batch of instruments and return their data"""
    # Create channel subscriptions
    ticker_channels = [f"ticker.{instr}.100ms" for instr in batch]
    book_channels = [f"book.{instr}.100ms" for instr in batch]
    channels = ticker_channels + book_channels

    # Subscribe to channels
    await subscribe_channels(ws, channels)

    # Process batch responses
    data_count = 0
    needed_responses = len(batch) * 2  # Ticker and book for each instrument
    instrument_data = {}

    while data_count < needed_responses:
        try:
            response = await ws.recv()
            data = json.loads(response)

            if 'params' in data and 'data' in data['params'] and 'channel' in data['params']:
                channel = data['params']['channel']
                parts = channel.split('.')

                if len(parts) >= 2:
                    channel_type = parts[0]  # 'ticker' or 'book'
                    instr_name = parts[1]

                    if instr_name in batch:
                        if instr_name not in instrument_data:
                            instrument_data[instr_name] = {}

                        if channel_type not in instrument_data[instr_name]:
                            instrument_data[instr_name][channel_type] = data['params']['data']
                            data_count += 1

        except Exception as e:
            logger.error(f"Error in batch {batch_num}: {e}")
            break

    # Unsubscribe from channels
    await unsubscribe_channels(ws, channels)

    # Process data for this batch
    batch_results = []
    for instr_name, channels_data in instrument_data.items():
        row = {"instrument_name": instr_name}

        # Merge ticker data
        if 'ticker' in channels_data:
            ticker = channels_data['ticker']
            # Add basic fields
            for k, v in ticker.items():
                if k not in ['stats', 'greeks']:
                    row[k] = v

            # Flatten stats and greeks
            for nested_key in ['stats', 'greeks']:
                if nested_key in ticker and isinstance(ticker[nested_key], dict):
                    for k, v in ticker[nested_key].items():
                        row[k] = v

        # Merge book data
        if 'book' in channels_data:
            book = channels_data['book']
            # Add book fields that don't conflict with ticker
            for k, v in book.items():
                if k not in row and k not in ['bids', 'asks']:
                    row[k] = v

            # Store raw bids and asks
            if 'bids' in book:
                row['bids'] = book['bids']
            if 'asks' in book:
                row['asks'] = book['asks']

        batch_results.append(row)

    return batch_results


@catch_exception
async def get_deribit_data(currency: str = "BTC") -> pd.DataFrame:
    """
    Get options data with ticker and order book information from Deribit.

    Parameters:
    currency (str): Currency to fetch options for (default: "BTC")

    Returns:
    pandas.DataFrame: DataFrame with ticker and book data
    """
    total_start = time.time()

    # Get active options instruments
    logger.info(f"Fetching {currency} options...")
    try:
        response = requests.get(
            "https://www.deribit.com/api/v2/public/get_instruments",
            params={"currency": currency, "kind": "option", "expired": "false"}
        )
        response.raise_for_status()  # Raise exception for non-200 status codes
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to connect to Deribit API: {str(e)}")

    try:
        instruments = [i['instrument_name'] for i in response.json()['result']]
    except (KeyError, json.JSONDecodeError) as e:
        raise VolyError(f"Failed to parse Deribit API response: {str(e)}")

    total_instruments = len(instruments)
    logger.info(f"Found {total_instruments} active {currency} options")

    # Calculate batches
    total_batches = (total_instruments + 100 - 1) // 100

    # Collect data
    all_data = []

    try:
        async with websockets.connect('wss://www.deribit.com/ws/api/v2') as ws:
            for i in range(0, total_instruments, 100):
                batch_num = i // 100 + 1
                batch = instruments[i:i + 100]

                batch_results = await process_batch(ws, batch, batch_num, total_batches)
                all_data.extend(batch_results)
    except (websockets.exceptions.WebSocketException, ConnectionError) as e:
        raise ConnectionError(f"WebSocket connection error: {str(e)}")

    total_time = time.time() - total_start
    logger.info(f"Total fetching time: {total_time:.2f}s")

    if not all_data:
        raise VolyError("No data collected from Deribit")

    return pd.DataFrame(all_data)


@catch_exception
def process_option_chain(df: pd.DataFrame, currency: str) -> pd.DataFrame:
    """
    Process raw option chain data into a standardized format.

    Parameters:
    df (pd.DataFrame): Raw option chain data
    currency (str): Currency code (e.g., 'BTC', 'ETH')

    Returns:
    pd.DataFrame: Processed option chain data
    """
    logger.info(f"Processing data for {currency}...")

    # Apply extraction to create new columns
    splits = df['instrument_name'].str.split('-')
    df['maturity_name'] = splits.str[1]
    if currency == 'XRP':
        df['strikes'] = splits.str[2].str.replace('d', '.', regex=False).astype(float)
    else:
        df['strikes'] = splits.str[2].astype(float)
    df['option_type'] = splits.str[3]

    # Create maturity date at 8:00 AM UTC
    df['maturity_date'] = pd.to_datetime(df['maturity_name'].apply(
        lambda x: int(dt.datetime.strptime(x, "%d%b%y")
                      .replace(hour=8, minute=0, second=0, tzinfo=dt.timezone.utc)
                      .timestamp() * 1000)), unit='ms')

    # Get reference time from timestamp
    reference_time = dt.datetime.fromtimestamp(df['timestamp'].iloc[0] / 1000)

    # Calculate time to expiry in years
    df['t'] = ((df['maturity_date'] - reference_time).dt.total_seconds() / (24 * 60 * 60)) / 365.25

    # Calculate implied volatility (convert from percentage)
    df['mark_iv'] = df['mark_iv'] / 100
    df['bid_iv'] = df['bid_iv'].replace({0: np.nan}) / 100
    df['ask_iv'] = df['ask_iv'].replace({0: np.nan}) / 100

    # Calculate log-moneyness
    df['log_moneyness'] = np.log(df['strikes'] / df['index_price'].iloc[0])
    # Calculate moneyness
    df['moneyness'] = np.exp(df['log_moneyness'])
    # Calculate returns
    df['returns'] = df['moneyness'] - 1

    logger.info(f"Processing complete!")

    return df


@catch_exception
def process_order_book_depth(option_chain, max_depth=5):
    """
    Process the order book depth data to enhance option pricing and weighting.

    Args:
        option_chain: DataFrame containing option data with 'bids' and 'asks' columns
        max_depth: Maximum number of levels to consider from the order book

    Returns:
        Enhanced option_chain with additional columns for depth analysis
    """
    # Create new columns for depth analysis
    option_chain['vwap_bid'] = float('nan')
    option_chain['vwap_ask'] = float('nan')
    option_chain['vwap_mid'] = float('nan')
    option_chain['depth_bid_qty'] = float('nan')
    option_chain['depth_ask_qty'] = float('nan')
    option_chain['vwap_bid_iv'] = float('nan')
    option_chain['vwap_ask_iv'] = float('nan')
    option_chain['vwap_mid_iv'] = float('nan')
    option_chain['depth_liquidity'] = float('nan')

    for idx, row in option_chain.iterrows():
        s = row['underlying_price']
        k = row['strikes']
        t = row['t']
        r = row['interest_rate'] if 'interest_rate' in row else 0.0
        option_type = 'C' if row['option_type'] == 'call' else 'P'

        # Process bid side
        if 'bids' in row and isinstance(row['bids'], list) and len(row['bids']) > 0:
            # Clean up the bid data
            clean_bids = []
            for bid in row['bids'][:max_depth]:  # Limit to max_depth levels
                if len(bid) >= 3:
                    # Extract price and quantity, removing 'new' if present
                    price = float(bid[1]) if bid[0] == 'new' else float(bid[0])
                    qty = float(bid[2]) if bid[0] == 'new' else float(bid[1])
                    clean_bids.append((price, qty))

            if clean_bids:
                # Calculate volume-weighted average price
                total_qty = sum(qty for _, qty in clean_bids)
                vwap_bid = sum(price * qty for price, qty in clean_bids) / total_qty if total_qty > 0 else float('nan')

                # Calculate IV for VWAP
                try:
                    vwap_bid_iv = voly.iv(vwap_bid * s, s, k, r, t, option_type)
                except:
                    vwap_bid_iv = float('nan')

                option_chain.at[idx, 'vwap_bid'] = vwap_bid
                option_chain.at[idx, 'depth_bid_qty'] = total_qty
                option_chain.at[idx, 'vwap_bid_iv'] = vwap_bid_iv

        # Process ask side
        if 'asks' in row and isinstance(row['asks'], list) and len(row['asks']) > 0:
            # Clean up the ask data
            clean_asks = []
            for ask in row['asks'][:max_depth]:  # Limit to max_depth levels
                if len(ask) >= 3:
                    # Extract price and quantity, removing 'new' if present
                    price = float(ask[1]) if ask[0] == 'new' else float(ask[0])
                    qty = float(ask[2]) if ask[0] == 'new' else float(ask[1])
                    clean_asks.append((price, qty))

            if clean_asks:
                # Calculate volume-weighted average price
                total_qty = sum(qty for _, qty in clean_asks)
                vwap_ask = sum(price * qty for price, qty in clean_asks) / total_qty if total_qty > 0 else float('nan')

                # Calculate IV for VWAP
                try:
                    vwap_ask_iv = voly.iv(vwap_ask * s, s, k, r, t, option_type)
                except:
                    vwap_ask_iv = float('nan')

                option_chain.at[idx, 'vwap_ask'] = vwap_ask
                option_chain.at[idx, 'depth_ask_qty'] = total_qty
                option_chain.at[idx, 'vwap_ask_iv'] = vwap_ask_iv

        # Calculate mid VWAP if both bid and ask are available
        if not np.isnan(option_chain.at[idx, 'vwap_bid']) and not np.isnan(option_chain.at[idx, 'vwap_ask']):
            vwap_mid = (option_chain.at[idx, 'vwap_bid'] + option_chain.at[idx, 'vwap_ask']) / 2

            # Calculate IV for mid VWAP
            try:
                vwap_mid_iv = voly.iv(vwap_mid * s, s, k, r, t, option_type)
            except:
                vwap_mid_iv = float('nan')

            option_chain.at[idx, 'vwap_mid'] = vwap_mid
            option_chain.at[idx, 'vwap_mid_iv'] = vwap_mid_iv

        # Calculate depth liquidity (sum of bid and ask quantities)
        bid_qty = option_chain.at[idx, 'depth_bid_qty'] if not np.isnan(option_chain.at[idx, 'depth_bid_qty']) else 0
        ask_qty = option_chain.at[idx, 'depth_ask_qty'] if not np.isnan(option_chain.at[idx, 'depth_ask_qty']) else 0
        option_chain.at[idx, 'depth_liquidity'] = bid_qty + ask_qty

    option_chain = option_chain.replace(float('inf'), float('nan'))

    return option_chain


@catch_exception
async def fetch_option_chain(exchange: str = 'deribit',
                             currency: str = 'BTC',
                             depth: bool = False) -> pd.DataFrame:
    """
    Fetch option chain data from the specified exchange.

    Parameters:
    exchange (str): Exchange to fetch data from (currently only 'deribit' is supported)
    currency (str): Currency to fetch options for (e.g., 'BTC', 'ETH')
    depth (bool): Whether to include full order book depth. Else, just top of book.

    Returns:
    pd.DataFrame: Processed option chain data
    """
    if exchange.lower() != 'deribit':
        raise VolyError(f"Exchange '{exchange}' is not supported. Currently only 'deribit' is available.")

    # Get raw data
    if currency not in ['BTC', 'ETH']:
        new_currency = 'USDC'
        raw_data = await get_deribit_data(currency=new_currency)
        raw_data['currency'] = raw_data['instrument_name'].str.split('-').str[0].str.split('_').str[0]
        raw_data = raw_data[raw_data['currency'] == currency]
    else:
        raw_data = await get_deribit_data(currency=currency)
        raw_data['currency'] = currency

    # Process data
    processed_data = process_option_chain(raw_data, currency)

    # Remove order book depth if not needed
    if not depth and 'bids' in processed_data.columns and 'asks' in processed_data.columns:
        processed_data = processed_data.drop(columns=['bids', 'asks'])

    return processed_data
