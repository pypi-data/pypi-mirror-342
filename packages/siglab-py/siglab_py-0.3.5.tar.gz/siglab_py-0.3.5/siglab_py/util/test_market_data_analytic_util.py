from datetime import datetime
import time
from typing import Union
import pandas as pd

from ccxt.okx import okx

from market_data_util import fetch_candles
from analytic_util import compute_candles_stats

base_ccy : str = "BTC"
# ticker = "GRIFFAIN/USDT:USDT"
# ticker = "OL/USDT:USDT"
ticker = f"{base_ccy}/USDT:USDT"

reload_raw_candles : bool = True
raw_candles_file : str = f"{base_ccy}_raw_candles.csv"
candles_with_ta_file : str = f"{base_ccy}_candles_ta.csv"

param = {
        'rateLimit' : 100,    # In ms
        'options' : {
            'defaultType': 'swap', # Should test linear instead
        }
    }
exchange = okx(param) # type: ignore

start_date : datetime = datetime(2024,1,1)
end_date : datetime = datetime(2025,4,22)
candle_size : str = '1h'
ma_long_intervals : int = 24*30
ma_short_intervals : int = 24
boillenger_std_multiples : int = 2
pypy_compatible : bool = False

markets = exchange.load_markets()
assert(ticker in markets)

start = time.time()

if reload_raw_candles:
    pd_candles: Union[pd.DataFrame, None] = fetch_candles(
                start_ts=int(start_date.timestamp()),
                end_ts=int(end_date.timestamp()),
                exchange=exchange,
                normalized_symbols=[ ticker ],
                candle_size=candle_size
            )[ ticker ]

    pd_candles.to_csv(raw_candles_file) # type: ignore
else:
    pd_candles = pd.read_csv(raw_candles_file) # type: ignore

compute_candles_stats(
                                    pd_candles=pd_candles, # type: ignore
                                    boillenger_std_multiples=boillenger_std_multiples, 
                                    sliding_window_how_many_candles=ma_long_intervals, 
                                    slow_fast_interval_ratio=(ma_long_intervals/ma_short_intervals),
                                    pypy_compat=pypy_compatible
                                ) 
pd_candles.to_csv(candles_with_ta_file) # type: ignore

compute_candles_stats_elapsed_ms = int((time.time() - start) *1000)
print(f"elapsed (ms): {compute_candles_stats_elapsed_ms}")