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
    load_data.export_to_db( host="192.168.0.200",
                            user="sharesuser",
                            passwd="SomePassword123",
                            db="shares")


    # получим данные по завтрашний день
    # how_many_bars = 100
    # utc_till = datetime.datetime.now() + datetime.timedelta(days=1)
    # print(utc_till)
    # SBER_D1 = load_data.get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_D1, utc_till=utc_till, how_many_bars=how_many_bars)
    # print(SBER_D1)

    how_many_bars = 10
    data = load_data.get_share_data_from_db(ticket="SBER", timeframe="D1", how_many_bars=how_many_bars)
    print(data)

    #load_data.always_get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_M1, table_name="SBER_M1")
    #load_data.always_get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_M5, table_name="SBER_M5")
    #load_data.always_get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_M15, table_name="SBER_M15")
    #load_data.always_get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_M30, table_name="SBER_M30")      # ERROR !!!!
    #load_data.always_get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_H1, table_name="SBER_H1")
    #load_data.always_get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_H4, table_name="SBER_H4")
    #load_data.always_get_share_data(ticket="SBER", timeframe=mt5.TIMEFRAME_D1, table_name="SBER_D1")

    # для работы потоков - нужно поменять код ))) сделаем попозже - можно просто копии файлов в расписании повесить - будет проще
    # thread_sber_m1 = Thread(target=load_data.always_get_share_data, args=("SBER", mt5.TIMEFRAME_M1, "SBER_M1",))
    # thread_sber_m1.start()
    # thread_sber_m5 = Thread(target=load_data.always_get_share_data, args=("SBER", mt5.TIMEFRAME_M5, "SBER_M5",))
    # thread_sber_m5.start()
    # thread_sber_m15 = Thread(target=load_data.always_get_share_data, args=("SBER", mt5.TIMEFRAME_M15, "SBER_M15",))
    # thread_sber_m15.start()
    # #thread_sber_m30 = Thread(target=load_data.always_get_share_data, args=("SBER", mt5.TIMEFRAME_M30, "SBER_M30",))    # ERROR !!!!
    # #thread_sber_m30.start()
    # thread_sber_h1 = Thread(target=load_data.always_get_share_data, args=("SBER", mt5.TIMEFRAME_H1, "SBER_H1",))
    # thread_sber_h1.start()
    # thread_sber_h4 = Thread(target=load_data.always_get_share_data, args=("SBER", mt5.TIMEFRAME_H4, "SBER_H4",))
    # thread_sber_h4.start()
    # thread_sber_d1 = Thread(target=load_data.always_get_share_data, args=("SBER", mt5.TIMEFRAME_D1, "SBER_D1",))
    # thread_sber_d1.start()
    # while True:
    #     #print("*", end=" ")
    #     k = cv2.waitKey(33)
    #     if k == 27:  # Esc key to stop
    #         break
    #     elif k == -1:  # normally -1 returned,so don't print it
    #         continue
    #     else:
    #         print(k)  # else print its value

    load_data.disconnect_from_metatrader5()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()