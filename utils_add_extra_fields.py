# pip install TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
# pip install pandas

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
    if not _periods: _periods = ["0", ]
    for _period in _periods:

        if not _periods2:
            _f = _func(_df, timeperiod=_period)
            _field = f"{name}_{_period}"
        else:
            _f = _func(_df, fastperiod=_period, slowperiod=_period*_mult)
            _field = f"{name}_{_period}_{_period*_mult}"

        if not _return:
            _df_func[_field] = _f
            _df_func[_field] = _df_func[_field].astype(float).round(2)
        elif _return > 1:
            _temp_df = _f
            for i in range(_return):
                _field = f"{name}_{_period}_{_return_names[i]}"
                _df_func[_field] = _temp_df[_return_names[i]]
                _df_func[_field] = _df_func[_field].astype(float).round(2)

    return _df_func


if __name__ == '__main__':
    timeframes = ["MN1", "W1", "D1", "H4", "H1", "M30", "M15", "M10", "M5"]

    csv_folders = ["csv_export_usa", "csv_export_rus"]
    csv_folders_appendix = "_extra"

    current_dir = os.path.dirname(os.path.abspath(__file__))  # текущая директория

    for csv_folder in csv_folders:
        for timeframe in timeframes:
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
                    print(_periods, "len:", len(_periods))  # [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100] len: 24

                    # # SMA
                    # _extra = func_extra(name="sma", _df=df0, _func=abstract.SMA, _periods=_periods)
                    # df = pd.concat([df, _extra], axis=1)
                    #
                    # # EMA
                    # _extra = func_extra(name="ema", _df=df0, _func=abstract.EMA, _periods=_periods)
                    # df = pd.concat([df, _extra], axis=1)
                    #
                    # # ATR
                    # _extra = func_extra(name="atr", _df=df0, _func=abstract.ATR, _periods=_periods)
                    # df = pd.concat([df, _extra], axis=1)
                    #
                    # # ATR
                    # _extra = func_extra(name="atr", _df=df0, _func=abstract.ATR, _periods=_periods)
                    # df = pd.concat([df, _extra], axis=1)

                    # --------------- Momentum Indicator Functions ---------------

                    # # ADX - Average Directional Movement Index
                    # _extra = func_extra(name="adx", _df=df0, _func=abstract.ADX, _periods=_periods)
                    # df = pd.concat([df, _extra], axis=1)

                    # # ADXR - Average Directional Movement Index Rating # input == 1, output == 1
                    # _extra = func_extra(name="adxr", _df=df0, _func=abstract.ADXR, _periods=_periods)
                    # df = pd.concat([df, _extra], axis=1)

                    # # APO - Absolute Price Oscillator # input == 2, output == 1
                    # _extra = func_extra(name="apo", _df=df0, _func=abstract.APO, _periods=_periods, _periods2=2)
                    # df = pd.concat([df, _extra], axis=1)

                    # # AROON - Aroon # input == 1, output == N
                    # _extra = func_extra(name="aroon", _df=df0, _func=abstract.AROON, _periods=_periods, _return=2, _return_names=["aroondown", "aroonup"])
                    # df = pd.concat([df, _extra], axis=1)

                    # # AROONOSC - Aroon Oscillator # input == 1, output == 1
                    # _extra = func_extra(name="aroonosc", _df=df0, _func=abstract.AROONOSC, _periods=_periods)
                    # df = pd.concat([df, _extra], axis=1)

                    # BOP - Balance Of Power # input == df, output == 1
                    _extra = func_extra(name="bop", _df=df0, _func=abstract.BOP, _periods=[])
                    df = pd.concat([df, _extra], axis=1)

                    # --------------- Momentum Indicator Functions ---------------

                    data = df

                    # выгружаем в новую папку
                    export_to_csv_from_df(ticker=ticker, timeframe=timeframe, data=data,
                                          export_dir=os.path.join(current_dir, f"{csv_folder}{csv_folders_appendix}"), by_timeframes=True)

                exit(1)
