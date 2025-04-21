from datetime import datetime
from typing import Dict, Union

import pandas as pd
import matplotlib.pyplot as plt

from ccxt.okx import okx

from market_data_util import fetch_candles
from analytic_util import compute_candles_stats

base_ccy : str = "BTC"
# ticker = "GRIFFAIN/USDT:USDT"
# ticker = "OL/USDT:USDT"
ticker = f"{base_ccy}/USDT:USDT"

param = {
        'rateLimit' : 100,    # In ms
        'options' : {
            'defaultType': 'swap', # Should test linear instead
        }
    }
exchange = okx(param) # type: ignore

start_date : datetime = datetime(2024,1,1)
end_date : datetime = datetime(2025,4,20)
candle_size : str = '1h'
ma_long_intervals : int = 24*30
ma_short_intervals : int = 24
boillenger_std_multiples : int = 2
pypy_compatible : bool = False

markets = exchange.load_markets()
assert(ticker in markets)

pd_candles: Union[pd.DataFrame, None] = fetch_candles(
            start_ts=int(start_date.timestamp()),
            end_ts=int(end_date.timestamp()),
            exchange=exchange,
            normalized_symbols=[ ticker ],
            candle_size=candle_size
        )[ ticker ]

pd_candles.to_csv(f"{base_ccy}_raw_candles.csv") # type: ignore

compute_candles_stats(
                                    pd_candles=pd_candles, # type: ignore
                                    boillenger_std_multiples=boillenger_std_multiples, 
                                    sliding_window_how_many_candles=ma_long_intervals, 
                                    slow_fast_interval_ratio=(ma_long_intervals/ma_short_intervals),
                                    pypy_compat=pypy_compatible
                                ) 