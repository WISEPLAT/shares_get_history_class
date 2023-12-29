# git clone https://github.com/cia76/FinamPy
# pip install pytz, requests, grpcio, protobuf, types-protobuf, googleapis-common-protos

import os, ast
from FinamPy.grpc.tradeapi.v1.securities_pb2 import GetSecuritiesResult  # Тип списка инструментов
from google.protobuf.json_format import MessageToJson, Parse  # Будем хранить справочник в файле в формате JSON


if __name__ == '__main__':
    filename = os.path.join("cached", f"finam_securities.txt")
    securities = GetSecuritiesResult()  # Тип списка инструментов

    with open(filename, 'r', encoding='UTF-8') as f:  # Открываем файл на чтение
        securities = MessageToJson(Parse(f.read(), securities))  # Получаем список инструментов из файла, приводим к типу

    securities = ast.literal_eval(securities)  # превращаем в словарь

    # приводим к словарю по инструментам
    all_securities = {}
    all_securities_usa = {}
    all_securities_rus = {}
    all_securities_hkd = {}
    for sec_info in securities["securities"]:
        all_securities[sec_info["code"]] = sec_info
        if sec_info['board'] == "MCT": all_securities_usa[sec_info["code"]] = sec_info
        if sec_info['board'] == "TQBR": all_securities_rus[sec_info["code"]] = sec_info
        if sec_info['board'] == "SPFEQ": all_securities_hkd[sec_info["code"]] = sec_info

    # print(all_securities)
    # print(all_securities_usa)
    # print(all_securities_rus)
    # print(all_securities_hkd)

    print(list(all_securities_hkd))