#pip install opencv-python mysqlclient MetaTrader5 pandas pytz kaggle
import os

from core.get_shares_data_processor import SharesDataLoader
import MetaTrader5 as mt5       # импортируем модуль для подключения к MetaTrader5
import datetime
from threading import Thread    # для поточной закачки разных датафреймов
import cv2
import pandas as pd
pd.set_option('display.max_columns', 500) # сколько столбцов показываем
pd.set_option('display.width', 1500)      # макс. ширина таблицы для показа


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))  # текущая директория
    how_many_bars = 99999  # сколько баров закачать - предел... - для загрузки с нуля!!!
    how_many_bars = 2500  # сколько баров закачать - предел... - для обновлений...

    utc_till = datetime.datetime.now() + datetime.timedelta(days=1)  # получим данные по завтрашний день
    print(utc_till)

    timeframes = {mt5.TIMEFRAME_M5, mt5.TIMEFRAME_M10, mt5.TIMEFRAME_M15, mt5.TIMEFRAME_M30, mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H4, mt5.TIMEFRAME_D1, mt5.TIMEFRAME_W1, mt5.TIMEFRAME_MN1}
    # timeframes = {mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H4, mt5.TIMEFRAME_D1, mt5.TIMEFRAME_W1, mt5.TIMEFRAME_MN1}
    # timeframes = {mt5.TIMEFRAME_M5, mt5.TIMEFRAME_M10, mt5.TIMEFRAME_M15, mt5.TIMEFRAME_M30}  # 99999 - предел...
    # timeframes = {mt5.TIMEFRAME_D1, }
    # tickers = ["VTBR", "GMKN", "SBER", "LKOH", "GAZP", "CHMF", "AFLT", "PLZL"]
    # tickers = {"ALLFUTRTSI"}  # только через Финам ..

    tickers = ['ABIO', 'ABRD', 'ACKO', 'AFKS', 'AFLT', 'AGRO', 'AKRN', 'ALRS', 'AMEZ', 'APTK', 'AQUA', 'ARSA', 'ASSB',
               'ASTR', 'AVAN', 'BANE', 'BANEP', 'BELU', 'BISVP', 'BLNG', 'BRZL', 'BSPB', 'BSPBP', 'CARM', 'CBOM',
               'CHGZ', 'CHKZ', 'CHMF', 'CHMK', 'CIAN', 'CNTL', 'CNTLP', 'DIOD', 'DSKY', 'DVEC', 'DZRD', 'DZRDP', 'EELT',
               'ELFV', 'ENPG', 'ETLN', 'EUTR', 'FEES', 'FESH', 'FIVE', 'FIXP', 'FLOT', 'GAZA', 'GAZAP', 'GAZC', 'GAZP',
               'GAZS', 'GAZT', 'GCHE', 'GECO', 'GEMA', 'GEMC', 'GLTR', 'GMKN', 'GTRK', 'HHRU', 'HIMCP', 'HMSG', 'HNFG',
               'HYDR', 'IGST', 'IGSTP', 'INGR', 'IRAO', 'IRKT', 'JNOS', 'JNOSP', 'KAZT', 'KAZTP', 'KBSB', 'KCHE',
               'KCHEP', 'KGKC', 'KGKCP', 'KLSB', 'KMAZ', 'KMEZ', 'KOGK', 'KRKN', 'KRKNP', 'KRKOP', 'KROT', 'KROTP',
               'KRSB', 'KRSBP', 'KTSB', 'KTSBP', 'KUBE', 'KUZB', 'KZOS', 'KZOSP', 'LENT', 'LIFE', 'LKOH', 'LNZL',
               'LNZLP', 'LSNG', 'LSNGP', 'LSRG', 'LVHK', 'MAGE', 'MAGEP', 'MAGN', 'MDMG', 'MFGS', 'MFGSP', 'MGNT',
               'MGNZ', 'MGTS', 'MGTSP', 'MISB', 'MISBP', 'MOEX', 'MRKC', 'MRKK', 'MRKP', 'MRKS', 'MRKU', 'MRKV', 'MRKY',
               'MRKZ', 'MRSB', 'MSNG', 'MSRS', 'MSTT', 'MTLR', 'MTLRP', 'MTSS', 'MVID', 'NAUK', 'NFAZ', 'NKHP', 'NKNC',
               'NKNCP', 'NKSH', 'NLMK', 'NMTP', 'NNSB', 'NNSBP', 'NSVZ', 'NVTK', 'OGKB', 'OKEY', 'OMZZP', 'OZON',
               'PAZA', 'PHOR', 'PIKK', 'PLZL', 'PMSB', 'PMSBP', 'POLY', 'POSI', 'PRFN', 'PRMB', 'QIWI', 'RASP', 'RBCM',
               'RDRB', 'RENI', 'RGSS', 'RKKE', 'RNFT', 'ROLO', 'ROSB', 'ROSN', 'ROST', 'RTGZ', 'RTKM', 'RTKMP', 'RTSB',
               'RTSBP', 'RUAL', 'RUSI', 'RZSB', 'SAGO', 'SAGOP', 'SARE', 'SAREP', 'SBER', 'SBERP', 'SELG', 'SFIN',
               'SGZH', 'SIBN', 'SLEN', 'SMLT', 'SNGS', 'SNGSP', 'SOFL', 'SPBE', 'STSB', 'STSBP', 'SVAV', 'SVCB', 'SVET',
               'TASB', 'TASBP', 'TATN', 'TATNP', 'TCSG', 'TGKA', 'TGKB', 'TGKBP', 'TGKN', 'TNSE', 'TORS', 'TORSP',
               'TRMK', 'TRNFP', 'TTLK', 'TUZA', 'UGLD', 'UKUZ', 'UNAC', 'UNKL', 'UPRO', 'URKZ', 'USBN', 'UTAR',
               'VEON-RX', 'VGSB', 'VGSBP', 'VJGZ', 'VJGZP', 'VKCO', 'VLHZ', 'VRSB', 'VRSBP', 'VSMO', 'VSYD', 'VSYDP',
               'VTBR', 'WTCM', 'WTCMP', 'WUSH', 'YAKG', 'YKEN', 'YKENP', 'YNDX', 'YRSB', 'YRSBP', 'ZILL', 'ZVEZ']

    # cant_load_tickers:

    cant_load_tickers = []

    for timeframe in timeframes:
        for ticket in tickers:
            try:
                load_data = SharesDataLoader(ticket)
                load_data.connect_to_metatrader5(path=f"C:\Program Files\FINAM MetaTrader 5\terminal64.exe")
                data = load_data.get_share_data(ticket=ticket, timeframe=timeframe, utc_till=utc_till, how_many_bars=how_many_bars, remove_today_bars=True)
                if len(data): print(f'- данные по тикеру {ticket} {timeframe} загружены: {data["time"].iloc[0]} - {data["time"].iloc[-1]} \t size: {len(data)}')
                load_data.export_to_csv_from_df(ticket=ticket, timeframe=timeframe, data=data, export_dir=os.path.join(current_dir, "csv_export_rus"), by_timeframes=True)
                load_data.disconnect_from_metatrader5()
            except Exception as e:
                print(f"Error: {e}")
                cant_load_tickers.append(ticket)

    print("cant_load_tickers:", cant_load_tickers)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()