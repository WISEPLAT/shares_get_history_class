#pip install opencv-python mysqlclient MetaTrader5 pandas pytz
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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    how_many_bars = 70000

    utc_till = datetime.datetime.now() + datetime.timedelta(days=1)  # получим данные по завтрашний день
    # utc_till = datetime.datetime.now() - datetime.timedelta(days=1)  # получим данные по вчерашний день
    print(utc_till)

    timeframes = {mt5.TIMEFRAME_M5, mt5.TIMEFRAME_M10, mt5.TIMEFRAME_M15, mt5.TIMEFRAME_M30, mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H4, mt5.TIMEFRAME_D1}
    tickers = {"VTBR", "GMKN", "SBER", "LKOH", "GAZP", "CHMF", "AFLT", "PLZL"}

    for timeframe in timeframes:
        for ticket in tickers:
            load_data = SharesDataLoader(ticket)
            # load_data.connect_to_metatrader5(path=f"C:\Program Files\FINAM MetaTrader 5\terminal64.exe")
            load_data.connect_to_metatrader5(path=f"C:\Program Files\Открытие Брокер\terminal64.exe")
            # load_data.connect_to_db(host="192.168.20.200",
            #                         user="sharesuser",
            #                         passwd="SomePassword123",
            #                         db="shares")

            data = load_data.get_share_data(ticket=ticket, timeframe=timeframe, utc_till=utc_till, how_many_bars=how_many_bars)
            # print(data)

            # how_many_bars = 10
            # data = load_data.get_share_data_from_db(ticket="SBER", timeframe=mt5.TIMEFRAME_D1, how_many_bars=how_many_bars)
            # print(data)

            # load_data.always_get_share_data(ticket=ticket, timeframe=timeframe)
            # load_data.export_to_csv(ticket=ticket, timeframe=timeframe, how_many_bars=how_many_bars, export_dir="csv_export")

            load_data.export_to_csv_from_df(ticket=ticket, timeframe=timeframe, data=data, export_dir=os.path.join(current_dir, "csv_export"))

            #load_data.always_get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_M1)
            #load_data.always_get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_M5)
            #load_data.always_get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_M15)
            #load_data.always_get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_M30)
            #load_data.always_get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_H1)
            #load_data.always_get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_H4)
            #load_data.always_get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_D1)

            load_data.disconnect_from_metatrader5()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()