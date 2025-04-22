import pandas as pd

def option_speculation(symbol_underlying: str = "اهرم",  
                       long_target: int = None, 
                       short_target: int = None,
                       status: str = "all",
                       high_value: bool = False,
                       min_days_remaining: int = None,
                       max_days_remaining: int = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Compares the return on investment (RoR) between the underlying asset and its options (both long and short).
    The function returns a dataframe for long positions (call options) if long_target is provided,
    and for short positions (put options) if short_target is provided.
    
    Additionally, filters contracts based on the `status`, `high_value`, and `remained day` parameters:
    - status = 'all' for no filter, 'itm' for in-the-money and at-the-money contracts,
      'otm' for out-of-the-money contracts.
    - high_value = True for filtering high value contracts (with a higher transaction value).
    - min_days_remaining and max_days_remaining to filter contracts by the number of remaining days.
    
    Args:
        symbol_underlying (str): The underlying symbol to consider.
        long_target (int, optional): Target price for long positions (call options) for the underlying symbol.
        short_target (int, optional): Target price for short positions (put options) for the underlying symbol.
        status (str): The contract status to filter by ('all', 'itm', 'otm').
        high_value (bool): Whether to filter for high value contracts (True for high value, False for all).
        min_days_remaining (int, optional): The minimum number of remaining days for contracts to be considered.
        max_days_remaining (int, optional): The maximum number of remaining days for contracts to be considered.

    Returns:
        Returns two separate dataframes: one for long (call) and one for short (put) positions.
    """

    from arb_tehran_finance.tse.tse_report import option_contract

    long_positions = None
    short_positions = None
    
    option_data = option_contract(symbol_underlying=symbol_underlying, option="all")

    option_data['close price (underlying) %'] = (option_data["close price (underlying)"] - option_data["yesterday price (underlying)"]) / option_data["yesterday price (underlying)"]
    option_data["close price (call) %"] = (option_data["close price (call)"] - option_data["yesterday price (call)"]) / option_data["yesterday price (call)"]
    option_data["close price (put) %"] = (option_data["close price (put)"] - option_data["yesterday price (put)"]) / option_data["yesterday price (put)"]

    option_data['close price (underlying) %'] = option_data['close price (underlying) %'].round(2)
    option_data["close price (call) %"] = option_data["close price (call) %"].round(2)
    option_data["close price (put) %"] = option_data["close price (put) %"].round(2)

    if long_target is not None:
        option_data['RoR (underlying)'] = (long_target - option_data["close price (underlying)"]) / option_data["close price (underlying)"]
        option_data['RoR (underlying)'] = option_data['RoR (underlying)'].round(2)

    option_data['status'] = option_data.apply(
        lambda row: 'itm' if row['close price (underlying)'] >= row['strike price'] else 'otm', axis=1
    )

    if status == "itm":
        option_data = option_data[option_data['status'].isin(['itm'])]
    elif status == "otm":
        option_data = option_data[option_data['status'] == 'otm']
    elif status != "all":
        raise ValueError("Invalid status value. It must be 'all', 'itm', or 'otm'.")

    if high_value:
        avg_value_call = option_data['notional value (call)'].mean()
        avg_value_put = option_data['notional value (put)'].mean()
        option_data = option_data[(option_data['notional value (call)'] > avg_value_call) | 
                                  (option_data['notional value (put)'] > avg_value_put)]

    if min_days_remaining is not None:
        option_data = option_data[option_data['remained day'] >= min_days_remaining]
    if max_days_remaining is not None:
        option_data = option_data[option_data['remained day'] <= max_days_remaining]

    if long_target is not None:
        long_data = option_data[['symbol underlying', 'remained day', 'strike price', 'close price (underlying)', 'close price (underlying) %', 'RoR (underlying)', 
                                 'contract symbol (call)', 'contract name (call)', 'value (call)', 'notional value (call)', 'open interest (call)', 
                                 'close price (call)', 'close price (call) %']].copy()

        long_data['breakeven price (call)'] = long_data['strike price'] + long_data['close price (call)']
        long_data['RoR (call)'] = (long_target - long_data['breakeven price (call)']) / long_data['close price (call)']
        long_data['breakeven price (call)'] = long_data['breakeven price (call)'].round(2)
        long_data['RoR (call)'] = long_data['RoR (call)'].round(2)

        long_data['status'] = option_data['status']
        long_data = long_data[['symbol underlying', 'remained day', 'strike price', 'close price (underlying)', 'close price (underlying) %', 'RoR (underlying)', 
                               'contract symbol (call)', 'contract name (call)', 'value (call)', 'notional value (call)', 'open interest (call)', 
                               'close price (call)', 'close price (call) %', 'breakeven price (call)', 'RoR (call)', 'status']]
        long_data = long_data.sort_values(by='RoR (call)', ascending=False)
        
        # Set index to 'contract symbol (call)'
        long_data = long_data.set_index('contract symbol (call)')

        long_positions = long_data

    if short_target is not None:
        short_data = option_data[['symbol underlying', 'remained day', 'strike price', 'close price (underlying)', 'close price (underlying) %', 'RoR (underlying)', 
                                  'contract symbol (put)', 'contract name (put)', 'value (put)', 'notional value (put)', 'open interest (put)', 
                                  'close price (put)', 'close price (put) %']].copy()

        short_data['breakeven price (put)'] = short_data['strike price'] - short_data['close price (put)']
        short_data['RoR (put)'] = (short_target - short_data['breakeven price (put)']) / short_data['close price (put)']
        short_data['breakeven price (put)'] = short_data['breakeven price (put)'].round(2)
        short_data['RoR (put)'] = short_data['RoR (put)'].round(2)

        short_data['status'] = option_data['status']
        short_data = short_data[['symbol underlying', 'remained day', 'strike price', 'close price (underlying)', 'close price (underlying) %', 'RoR (underlying)', 
                                 'contract symbol (put)', 'contract name (put)', 'value (put)', 'notional value (put)', 'open interest (put)', 
                                 'close price (put)', 'close price (put) %', 'breakeven price (put)', 'RoR (put)', 'status']]
        short_data = short_data.sort_values(by='RoR (put)', ascending=False)
        
        # Set index to 'contract symbol (put)'
        short_data = short_data.set_index('contract symbol (put)')

        short_positions = short_data

    return long_positions, short_positions
