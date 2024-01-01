# pip install TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
# pip install pandas

# exit(1)  # to prevent run

import os
import pandas as pd

import talib
from talib import abstract


def export_to_csv_from_df(ticker, timeframe, data, export_dir, by_timeframes=False):
    if not os.path.exists(export_dir): os.makedirs(export_dir)
    if by_timeframes:
        export_dir = os.path.join(export_dir, timeframe)
        if not os.path.exists(export_dir): os.makedirs(export_dir)
    data.to_csv(os.path.join(export_dir, ticker+"_"+timeframe+".csv"), index=False, encoding='utf-8')


def func_extra(name, _df, _func, _periods, _periods2=None, _return=None, _return_names=None):
    _df_func = pd.DataFrame()
    _mult = 2
    _mult2 = 3
    if not _periods: _periods = ["0", ]
    for _period in _periods:

        if not _periods2:
            _f = _func(_df, timeperiod=_period)
            _field = f"{name}_{_period}"
        elif name in ["apo", "ppo", "adosc", ]:  # _periods2 == 2:
            _f = _func(_df, fastperiod=_period, slowperiod=_period*_mult)
            _field = f"{name}_{_period}_{_period*_mult}"
        elif name in ["macd", ]:  # _periods2 == 3:
            _f = _func(_df, fastperiod=_period, slowperiod=_period*_mult, signalperiod=int(_period/2))
            _field = f"{name}_{_period}_{_period*_mult}_{int(_period/2)}"
        elif name in ["bbands", ]:  # _periods2 == 3:
            _f = _func(_df, timeperiod=_period, nbdevup=2, nbdevdn=2, matype=0)
            _field = f"{name}_{_period}_{_period*_mult}_{int(_period/2)}"
        elif name in ["stoch", ]:
            _f = _func(_df, fastk_period=_period, slowk_period=_period*_mult, slowk_matype=0, slowd_period=int(_period/2), slowd_matype=0, )
            _field = f"{name}_{_period}_{_period*_mult}_{int(_period/2)}"
        elif name in ["stochf", ]:
            _f = _func(_df, fastk_period=_period*_mult, fastd_period=_period, fastd_matype=0)
            _field = f"{name}_{_period}_{_period*_mult}"
        elif name in ["stochrsi", ]:
            _f = _func(_df, fastk_period=_period, fastd_period=int(_period/2), fastd_matype=0, timeperiod=_period*_mult, )
            _field = f"{name}_{_period}_{_period*_mult}_{_period*_mult}"
        elif name in ["ultosc", ]:
            _f = _func(_df, timeperiod1=_period, timeperiod2=_period*_mult, timeperiod3=_period*_mult2)
            _field = f"{name}_{_period}_{_period*_mult}_{_period*_mult2}"
        elif name in ["mama", ]:
            _f = _func(_df, fastlimit=0, slowlimit=0)
            _field = f"{name}_{_period}_{_period*_mult}"

        if not _return:
            _df_func[_field] = _f
            _df_func[_field] = _df_func[_field].astype(float).round(2)
        elif _return > 1:
            _temp_df = _f
            for i in range(_return):
                _field = f"{name}_{_period}_{_period*_mult}_{_return_names[i]}"
                if _return == 3: _field = f"{name}_{_period}_{_period*_mult}_{int(_period/2)}_{_return_names[i]}"
                if _return == 3 and not _periods2: _field = f"{name}_{_period}_{_return_names[i]}"
                _df_func[_field] = _temp_df[_return_names[i]]
                _df_func[_field] = _df_func[_field].astype(float).round(2)

    return _df_func


if __name__ == '__main__':

    # !!! ~6 Mb => 1 Gb !!! +1298 columns with indicators

    # timeframes = ["MN1", "W1", "D1", "H4", "H1", "M30", "M15", "M10", "M5"]
    timeframes = ["MN1", "W1", "D1", ]
    # timeframes = ["H4", "H1", ]

    csv_folders = ["csv_export_usa", "csv_export_rus"]
    csv_folders_appendix = "_extra"

    current_dir = os.path.dirname(os.path.abspath(__file__))  # текущая директория

    for csv_folder in csv_folders:
        for timeframe in timeframes:
            print(csv_folder, timeframe)
            _folder = os.path.join(csv_folder, timeframe)
            for f in os.listdir(_folder):
                _filename = os.path.join(_folder, f)
                if os.path.isfile(_filename):
                    # считываем файл
                    df = pd.read_csv(_filename, )
                    df0 = df.copy()

                    ticker = f.split(sep="_")[0]

                    # +extra fields
                    _periods = list(range(3, 11)) + list(range(12, 20, 2)) + list(range(20, 55, 5)) + list(range(60, 110, 10))
                    # print(_periods, "len:", len(_periods))  # [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100] len: 24


                    # --------------- Overlap Studies Functions ---------------

                    # BBANDS - Bollinger Bands # input == 3, output == N
                    _extra = func_extra(name="bbands", _df=df0, _func=abstract.BBANDS, _periods=_periods, _return=3, _return_names=["upperband", "middleband", "lowerband"])
                    df = pd.concat([df, _extra], axis=1)

                    # DEMA - Double Exponential Moving Average # input == 1, output == 1
                    _extra = func_extra(name="dema", _df=df0, _func=abstract.DEMA, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # EMA - Exponential Moving Average # input == 1, output == 1
                    _extra = func_extra(name="ema", _df=df0, _func=abstract.EMA, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # HT_TRENDLINE - Hilbert Transform - Instantaneous Trendline # input == df, output == 1
                    _extra = func_extra(name="ht_trendline", _df=df0, _func=abstract.HT_TRENDLINE, _periods=[])
                    df = pd.concat([df, _extra], axis=1)

                    # KAMA - Kaufman Adaptive Moving Average # input == 1, output == 1
                    _extra = func_extra(name="kama", _df=df0, _func=abstract.KAMA, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # MA - Moving average # input == 1, output == 1
                    _extra = func_extra(name="ma", _df=df0, _func=abstract.MA, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # MAMA - MESA Adaptive Moving Average # input == df, output == N
                    _extra = func_extra(name="mama", _df=df0, _func=abstract.MAMA, _periods=[], _return=2, _return_names=["mama", "fama"])
                    df = pd.concat([df, _extra], axis=1)

                    # MIDPOINT - MidPoint over period # input == 1, output == 1
                    _extra = func_extra(name="midpoint", _df=df0, _func=abstract.MIDPOINT, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # MIDPRICE - Midpoint Price over period # input == 1, output == 1
                    _extra = func_extra(name="midprice", _df=df0, _func=abstract.MIDPRICE, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # SAR - Parabolic SAR # input == df, output == 1
                    _extra = func_extra(name="sar", _df=df0, _func=abstract.SAR, _periods=[])
                    df = pd.concat([df, _extra], axis=1)

                    # SAREXT - Parabolic SAR - Extended # input == df, output == 1
                    _extra = func_extra(name="sarext", _df=df0, _func=abstract.SAREXT, _periods=[])
                    df = pd.concat([df, _extra], axis=1)

                    # SMA - Simple Moving Average # input == 1, output == 1
                    _extra = func_extra(name="sma", _df=df0, _func=abstract.SMA, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # T3 - Triple Exponential Moving Average (T3) # input == 1, output == 1
                    _extra = func_extra(name="t3", _df=df0, _func=abstract.T3, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # TEMA - Triple Exponential Moving Average # input == 1, output == 1
                    _extra = func_extra(name="tema", _df=df0, _func=abstract.TEMA, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # TRIMA - Triangular Moving Average # input == 1, output == 1
                    _extra = func_extra(name="trima", _df=df0, _func=abstract.TRIMA, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # WMA - Weighted Moving Average # input == 1, output == 1
                    _extra = func_extra(name="wma", _df=df0, _func=abstract.WMA, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # --------------- Overlap Studies Functions ---------------


                    # --------------- Volume Indicator Functions ---------------

                    # AD - Chaikin A/D Line # input == df, output == 1
                    _extra = func_extra(name="ad", _df=df0, _func=abstract.AD, _periods=[])
                    df = pd.concat([df, _extra], axis=1)

                    # ADOSC - Chaikin A/D Oscillator # input == 2, output == 1
                    _extra = func_extra(name="adosc", _df=df0, _func=abstract.ADOSC, _periods=_periods, _periods2=2)
                    df = pd.concat([df, _extra], axis=1)

                    # OBV - On Balance Volume # input == df, output == 1
                    _extra = func_extra(name="obv", _df=df0, _func=abstract.OBV, _periods=[])
                    df = pd.concat([df, _extra], axis=1)

                    # --------------- Volume Indicator Functions ---------------


                    # --------------- Volatility Indicator Functions ---------------

                    # ATR - Average True Range # input == 1, output == 1
                    _extra = func_extra(name="atr", _df=df0, _func=abstract.ATR, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # NATR - Normalized Average True Range # input == 1, output == 1
                    _extra = func_extra(name="natr", _df=df0, _func=abstract.NATR, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # TRANGE - True Range # input == df, output == 1
                    _extra = func_extra(name="trange", _df=df0, _func=abstract.TRANGE, _periods=[])
                    df = pd.concat([df, _extra], axis=1)

                    # --------------- Volatility Indicator Functions ---------------


                    # --------------- Price Transform Functions ---------------

                    # AVGPRICE - Average Price # input == df, output == 1
                    _extra = func_extra(name="avgprice", _df=df0, _func=abstract.AVGPRICE, _periods=[])
                    df = pd.concat([df, _extra], axis=1)

                    # MEDPRICE - Median Price # input == df, output == 1
                    _extra = func_extra(name="medprice", _df=df0, _func=abstract.MEDPRICE, _periods=[])
                    df = pd.concat([df, _extra], axis=1)

                    # TYPPRICE - Typical Price # input == df, output == 1
                    _extra = func_extra(name="typprice", _df=df0, _func=abstract.TYPPRICE, _periods=[])
                    df = pd.concat([df, _extra], axis=1)

                    # WCLPRICE - Weighted Close Price # input == df, output == 1
                    _extra = func_extra(name="wclprice", _df=df0, _func=abstract.WCLPRICE, _periods=[])
                    df = pd.concat([df, _extra], axis=1)

                    # --------------- Price Transform Functions ---------------


                    # --------------- Cycle Indicator Functions ---------------

                    # HT_DCPERIOD - Hilbert Transform - Dominant Cycle Period # input == df, output == 1
                    _extra = func_extra(name="ht_dcperiod", _df=df0, _func=abstract.HT_DCPERIOD, _periods=[])
                    df = pd.concat([df, _extra], axis=1)

                    # HT_DCPHASE - Hilbert Transform - Dominant Cycle Phase # input == df, output == 1
                    _extra = func_extra(name="ht_dcphase", _df=df0, _func=abstract.HT_DCPHASE, _periods=[])
                    df = pd.concat([df, _extra], axis=1)

                    # HT_PHASOR - Hilbert Transform - Phasor Components # input == df, output == 1
                    _extra = func_extra(name="ht_dcphasor", _df=df0, _func=abstract.HT_PHASOR, _periods=[], _return=2, _return_names=["inphase", "quadrature"])
                    df = pd.concat([df, _extra], axis=1)

                    # HT_SINE - Hilbert Transform - SineWave # input == df, output == 1
                    _extra = func_extra(name="ht_sine", _df=df0, _func=abstract.HT_SINE, _periods=[], _return=2, _return_names=["sine", "leadsine"])
                    df = pd.concat([df, _extra], axis=1)

                    # HT_TRENDMODE - Hilbert Transform - Trend vs Cycle Mode # input == df, output == 1
                    _extra = func_extra(name="ht_trendmode", _df=df0, _func=abstract.HT_TRENDMODE, _periods=[])
                    df = pd.concat([df, _extra], axis=1)

                    # --------------- Cycle Indicator Functions ---------------


                    # --------------- Momentum Indicator Functions ---------------

                    # ADX - Average Directional Movement Index
                    _extra = func_extra(name="adx", _df=df0, _func=abstract.ADX, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # ADXR - Average Directional Movement Index Rating # input == 1, output == 1
                    _extra = func_extra(name="adxr", _df=df0, _func=abstract.ADXR, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # APO - Absolute Price Oscillator # input == 2, output == 1
                    _extra = func_extra(name="apo", _df=df0, _func=abstract.APO, _periods=_periods, _periods2=2)
                    df = pd.concat([df, _extra], axis=1)

                    # AROON - Aroon # input == 1, output == N
                    _extra = func_extra(name="aroon", _df=df0, _func=abstract.AROON, _periods=_periods, _return=2, _return_names=["aroondown", "aroonup"])
                    df = pd.concat([df, _extra], axis=1)

                    # AROONOSC - Aroon Oscillator # input == 1, output == 1
                    _extra = func_extra(name="aroonosc", _df=df0, _func=abstract.AROONOSC, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # BOP - Balance Of Power # input == df, output == 1
                    _extra = func_extra(name="bop", _df=df0, _func=abstract.BOP, _periods=[])
                    df = pd.concat([df, _extra], axis=1)

                    # CCI - Commodity Channel Index # input == 1, output == 1
                    _extra = func_extra(name="cci", _df=df0, _func=abstract.CCI, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # CMO - Chande Momentum Oscillator # input == 1, output == 1
                    _extra = func_extra(name="cmo", _df=df0, _func=abstract.CMO, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # DX - Directional Movement Index # input == 1, output == 1
                    _extra = func_extra(name="dx", _df=df0, _func=abstract.DX, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # MACD - Moving Average Convergence/Divergence # input == 3, output == N
                    _extra = func_extra(name="macd", _df=df0, _func=abstract.MACD, _periods=_periods, _periods2=3, _return=3, _return_names=["macd", "macdsignal", "macdhist"])
                    df = pd.concat([df, _extra], axis=1)

                    # MACDFIX - Moving Average Convergence/Divergence Fix 12/26 # input == 1, output == N
                    _extra = func_extra(name="macdfix", _df=df0, _func=abstract.MACDFIX, _periods=_periods, _return=3, _return_names=["macd", "macdsignal", "macdhist"])
                    df = pd.concat([df, _extra], axis=1)

                    # MFI - Money Flow Index # input == 1, output == 1
                    _extra = func_extra(name="mfi", _df=df0, _func=abstract.MFI, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # MINUS_DI - Minus Directional Indicator # input == 1, output == 1
                    _extra = func_extra(name="minus_di", _df=df0, _func=abstract.MINUS_DI, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # MINUS_DM - Minus Directional Movement # input == 1, output == 1
                    _extra = func_extra(name="minus_dm", _df=df0, _func=abstract.MINUS_DM, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # MOM - Momentum # input == 1, output == 1
                    _extra = func_extra(name="mom", _df=df0, _func=abstract.MOM, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # PLUS_DI - Plus Directional Indicator # input == 1, output == 1
                    _extra = func_extra(name="plus_di", _df=df0, _func=abstract.PLUS_DI, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # PLUS_DM - Plus Directional Movement # input == 1, output == 1
                    _extra = func_extra(name="plus_dm", _df=df0, _func=abstract.PLUS_DM, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # PPO - Percentage Price Oscillator # input == 2, output == 1
                    _extra = func_extra(name="ppo", _df=df0, _func=abstract.PPO, _periods=_periods, _periods2=2)
                    df = pd.concat([df, _extra], axis=1)

                    # ROC - Rate of change : ((price/prevPrice)-1)*100 # input == 1, output == 1
                    _extra = func_extra(name="roc", _df=df0, _func=abstract.ROC, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # ROCP - Rate of change Percentage: (price-prevPrice)/prevPrice # input == 1, output == 1
                    _extra = func_extra(name="rocp", _df=df0, _func=abstract.ROCP, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # ROCR - Rate of change ratio: (price/prevPrice) # input == 1, output == 1
                    _extra = func_extra(name="rocr", _df=df0, _func=abstract.ROCR, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # ROCR100 - Rate of change ratio 100 scale: (price/prevPrice)*100 # input == 1, output == 1
                    _extra = func_extra(name="rocr100", _df=df0, _func=abstract.ROCR100, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # RSI - Relative Strength Index # input == 1, output == 1
                    _extra = func_extra(name="rsi", _df=df0, _func=abstract.RSI, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # STOCH - Stochastic # input == 3, output == N
                    _extra = func_extra(name="stoch", _df=df0, _func=abstract.STOCH, _periods=_periods, _periods2=3, _return=2, _return_names=["slowk", "slowd"])
                    df = pd.concat([df, _extra], axis=1)

                    # STOCHF - Stochastic Fast # input == 2, output == N
                    _extra = func_extra(name="stochf", _df=df0, _func=abstract.STOCHF, _periods=_periods, _periods2=2, _return=2, _return_names=["fastk", "fastd"])
                    df = pd.concat([df, _extra], axis=1)

                    # STOCHRSI - Stochastic Relative Strength Index # input == 2, output == N
                    _extra = func_extra(name="stochrsi", _df=df0, _func=abstract.STOCHRSI, _periods=_periods, _periods2=3, _return=2, _return_names=["fastk", "fastd"])
                    df = pd.concat([df, _extra], axis=1)

                    # TRIX - 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA # input == 1, output == 1
                    _extra = func_extra(name="trix", _df=df0, _func=abstract.TRIX, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # ULTOSC - Ultimate Oscillator # input == 3, output == 1
                    _extra = func_extra(name="ultosc", _df=df0, _func=abstract.ULTOSC, _periods=_periods, _periods2=3, )
                    df = pd.concat([df, _extra], axis=1)

                    # WILLR - Williams' %R # input == 1, output == 1
                    _extra = func_extra(name="willr", _df=df0, _func=abstract.WILLR, _periods=_periods)
                    df = pd.concat([df, _extra], axis=1)

                    # --------------- Momentum Indicator Functions ---------------


                    data = df

                    # выгружаем в новую папку
                    export_to_csv_from_df(ticker=ticker, timeframe=timeframe, data=data,
                                          export_dir=os.path.join(current_dir, f"{csv_folder}{csv_folders_appendix}"), by_timeframes=True)

                    # print(data.info())  # Columns: 1298 entries, datetime to willr_100

                # exit(1)
