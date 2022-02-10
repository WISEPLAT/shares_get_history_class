#pip install opencv-python mysqlclient MetaTrader5 pandas pytz

from core.get_shares_data_processor import SharesDataLoader
import MetaTrader5 as mt5       # импортируем модуль для подключения к MetaTrader5
import datetime
from threading import Thread    # для поточной закачки разных датафреймов
import cv2
import pandas as pd
pd.set_option('display.max_columns', 500) # сколько столбцов показываем
pd.set_option('display.width', 1500)      # макс. ширина таблицы для показа


def main():
    load_data = SharesDataLoader('SBER')
    load_data.connect_to_metatrader5(path=f"C:\Program Files\FINAM MetaTrader 5\terminal64.exe")
    load_data.connect_to_db( host="192.168.0.200",
                            user="sharesuser",
                            passwd="SomePassword123",
                            db="shares")

    load_data.always_get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_M1)

    load_data.disconnect_from_metatrader5()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()