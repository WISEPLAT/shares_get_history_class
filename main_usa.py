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
    # tickers = {"MSFT.US", "BAC.US"}
    # tickers = {"ALLFUTRTSI"}  # только через Финам ..

    tickers = ['CE.US', 'WELL.US', 'GRMN.US', 'IEX.US', 'CAG.US', 'BEN.US', 'ATO.US', 'WY.US', 'TSCO.US', 'COR.US',
                   'MOS.US', 'SWKS.US', 'ORCL.US', 'URI.US', 'INCY.US', 'MPC.US', 'HD.US', 'PPG.US', 'NUE.US',
                   'DDOG.US', 'HSIC.US', 'CAT.US', 'HSY.US', 'MKTX.US', 'CCEP.US', 'GWW.US', 'LEN.US', 'IFF.US',
                   'GL.US', 'MDB.US', 'SNPS.US', 'KR.US', 'DVN.US', 'SYY.US', 'USB.US', 'DRI.US', 'PARA.US', 'FMC.US',
                   'UBER.US', 'WRK.US', 'DLR.US', 'SO.US', 'AMGN.US', 'MA.US', 'STT.US', 'BWA.US', 'KVUE.US', 'GFS.US',
                   'BBY.US', 'BK.US', 'MRVL.US', 'VFC.US', 'EIX.US', 'ADSK.US', 'ZBH.US', 'MU.US', 'HUBB.US', 'PEAK.US',
                   'CVX.US', 'CPB.US', 'GILD.US', 'BXP.US', 'DD.US', 'MCD.US', 'KDP.US', 'GE.US', 'PKG.US', 'HST.US',
                   'WTW.US', 'XOM.US', 'ED.US', 'SPG.US', 'PFG.US', 'LVS.US', 'FAST.US', 'ROST.US', 'TTD.US', 'CNC.US',
                   'PGR.US', 'CMI.US', 'TEAM.US', 'MELI.US', 'BKR.US', 'EBAY.US', 'CPRT.US', 'MSFT.US', 'HOLX.US',
                   'ABBV.US', 'AMZN.US', 'FE.US', 'WYNN.US', 'KMI.US', 'APA.US', 'CRWD.US', 'DPZ.US', 'EQT.US',
                   'NOC.US', 'TAP.US', 'ETR.US', 'T.US', 'OMC.US', 'MTCH.US', 'TRMB.US', 'EXPE.US', 'DTE.US', 'PNR.US',
                   'LH.US', 'ALL.US', 'CTRA.US', 'VMC.US', 'XRAY.US', 'NWS.US', 'GOOGL.US', 'WEC.US', 'BIIB.US',
                   'LLY.US', 'BMY.US', 'STE.US', 'NI.US', 'MKC.US', 'AMT.US', 'CFG.US', 'LW.US', 'HIG.US', 'ETSY.US',
                   'AON.US', 'ULTA.US', 'DVA.US', 'LKQ.US', 'MPWR.US', 'TEL.US', 'FICO.US', 'CVS.US', 'CMA.US',
                   'NVDA.US', 'TDG.US', 'AWK.US', 'PSA.US', 'FOXA.US', 'ON.US', 'ODFL.US', 'NVR.US', 'ROP.US', 'TFX.US',
                   'HLT.US', 'EXPD.US', 'FOX.US', 'D.US', 'AMAT.US', 'AZO.US', 'DLTR.US', 'TT.US', 'SBUX.US', 'JNJ.US',
                   'HAS.US', 'DASH.US', 'NRG.US', 'JNPR.US', 'BIO.US', 'AMD.US', 'NFLX.US', 'VLTO.US', 'BRO.US',
                   'REGN.US', 'WRB.US', 'LRCX.US', 'SYK.US', 'MCO.US', 'CSGP.US', 'TROW.US', 'ETN.US', 'RTX.US',
                   'CRM.US', 'SIRI.US', 'UPS.US', 'HES.US', 'RSG.US', 'PEP.US', 'MET.US', 'HON.US', 'IQV.US', 'JPM.US',
                   'DG.US', 'CBRE.US', 'NDSN.US', 'DOW.US', 'SBAC.US', 'TSN.US', 'IT.US', 'WM.US', 'TPR.US', 'IBM.US',
                   'CHTR.US', 'HAL.US', 'ROL.US', 'FDS.US', 'SHW.US', 'EW.US', 'RJF.US', 'APH.US', 'AIZ.US', 'ZBRA.US',
                   'SRE.US', 'CTAS.US', 'PXD.US', 'MTD.US', 'NOW.US', 'MAS.US', 'FFIV.US', 'ELV.US', 'SYF.US',
                   'CSCO.US', 'APTV.US', 'FI.US', 'LHX.US', 'DAL.US', 'DFS.US', 'COST.US', 'LOW.US', 'SJM.US',
                   'ABNB.US', 'KHC.US', 'CCL.US', 'PM.US', 'WBD.US', 'PANW.US', 'CCI.US', 'ANET.US', 'ASML.US',
                   'CMS.US', 'PDD.US', 'MRNA.US', 'ACGL.US', 'LIN.US', 'CMG.US', 'PRU.US', 'ISRG.US', 'DGX.US',
                   'TSLA.US', 'AAPL.US', 'FDX.US', 'RVTY.US', 'BKNG.US', 'MLM.US', 'UNP.US', 'HBAN.US', 'CB.US',
                   'NTRS.US', 'FLT.US', 'TJX.US', 'AEE.US', 'HII.US', 'ES.US', 'BAC.US', 'CDNS.US', 'ABT.US', 'QRVO.US',
                   'AXON.US', 'ANSS.US', 'TFC.US', 'BA.US', 'JKHY.US', 'STZ.US', 'CTSH.US', 'TDY.US', 'CZR.US',
                   'MDLZ.US', 'A.US', 'CDW.US', 'ARE.US', 'XEL.US', 'STX.US', 'DIS.US', 'VTRS.US', 'IPG.US', 'WAT.US',
                   'AVB.US', 'FITB.US', 'BSX.US', 'OKE.US', 'BLDR.US', 'TRGP.US', 'OTIS.US', 'AME.US', 'CINF.US',
                   'HCA.US', 'PWR.US', 'ALB.US', 'DHR.US', 'VLO.US', 'FSLR.US', 'CDAY.US', 'CHRW.US', 'AVGO.US',
                   'NWSA.US', 'MS.US', 'AJG.US', 'HPQ.US', 'WBA.US', 'PPL.US', 'J.US', 'KEY.US', 'TECH.US', 'VICI.US',
                   'AMCR.US', 'ILMN.US', 'EA.US', 'FCX.US', 'MO.US', 'RL.US', 'TYL.US', 'ENPH.US', 'ADBE.US', 'BDX.US',
                   'EPAM.US', 'BF.B.US', 'AVY.US', 'CTLT.US', 'TER.US', 'APD.US', 'GS.US', 'ZS.US', 'KMX.US', 'INTC.US',
                   'MNST.US', 'PHM.US', 'PH.US', 'PFE.US', 'DXCM.US', 'MGM.US', 'EMN.US', 'STLD.US', 'BR.US', 'RF.US',
                   'TXT.US', 'WDAY.US', 'WST.US', 'CMCSA.US', 'GNRC.US', 'MCHP.US', 'EQR.US', 'ROK.US', 'MCK.US',
                   'MDT.US', 'PSX.US', 'BAX.US', 'FTNT.US', 'PNC.US', 'FIS.US', 'HRL.US', 'ICE.US', 'EL.US', 'KEYS.US',
                   'FTV.US', 'ADI.US', 'NCLH.US', 'IR.US', 'META.US', 'CME.US', 'DHI.US', 'V.US', 'MMM.US', 'MSI.US',
                   'DUK.US', 'MRO.US', 'TMO.US', 'JBL.US', 'CSX.US', 'AES.US', 'UHS.US', 'GEHC.US', 'UDR.US', 'CAH.US',
                   'LUV.US', 'DOV.US', 'PAYC.US', 'EVRG.US', 'CL.US', 'IP.US', 'F.US', 'HWM.US', 'K.US', 'C.US',
                   'REG.US', 'AIG.US', 'CTVA.US', 'ITW.US', 'AMP.US', 'TTWO.US', 'PG.US', 'KLAC.US', 'SCHW.US',
                   'AAL.US', 'PNW.US', 'WAB.US', 'MSCI.US', 'O.US', 'CLX.US', 'LDOS.US', 'YUM.US', 'L.US', 'ZION.US',
                   'AXP.US', 'COO.US', 'ALGN.US', 'ALLE.US', 'RCL.US', 'LYV.US', 'MMC.US', 'COF.US', 'CHD.US',
                   'PODD.US', 'NKE.US', 'SWK.US', 'GD.US', 'GPC.US', 'ADP.US', 'IVZ.US', 'BG.US', 'GEN.US', 'ESS.US',
                   'AFL.US', 'PCAR.US', 'CEG.US', 'NXPI.US', 'CRL.US', 'LNT.US', 'EOG.US', 'AKAM.US', 'JBHT.US',
                   'EXR.US', 'MOH.US', 'XYL.US', 'MTB.US', 'TGT.US', 'NTAP.US', 'ACN.US', 'CPT.US', 'FANG.US', 'ADM.US',
                   'PLD.US', 'CF.US', 'WMT.US', 'GM.US', 'POOL.US', 'TXN.US', 'CARR.US', 'EXC.US', 'FRT.US', 'INVH.US',
                   'HUM.US', 'NEE.US', 'UNH.US', 'LYB.US', 'EMR.US', 'AZN.US', 'NEM.US', 'WFC.US', 'MAR.US', 'PTC.US',
                   'CNP.US', 'WHR.US', 'ECL.US', 'KMB.US', 'EG.US', 'ZTS.US', 'BLK.US', 'PEG.US', 'TRV.US', 'IDXX.US',
                   'GIS.US', 'CI.US', 'IRM.US', 'BBWI.US', 'BALL.US', 'PAYX.US', 'QCOM.US', 'GLW.US', 'CBOE.US',
                   'VRSK.US', 'RMD.US', 'SPGI.US', 'KO.US', 'MRK.US', 'DE.US', 'WMB.US', 'MAA.US', 'BRK.B.US',
                   'EQIX.US', 'EFX.US', 'SPLK.US', 'TMUS.US', 'LMT.US', 'VZ.US', 'PYPL.US', 'HPE.US', 'MHK.US',
                   'NDAQ.US', 'KIM.US', 'AEP.US', 'JCI.US', 'OXY.US', 'WDC.US', 'VTR.US', 'GPN.US', 'BX.US', 'UAL.US',
                   'AOS.US', 'GOOG.US', 'VRSN.US', 'INTU.US', 'ORLY.US', 'NSC.US', 'VRTX.US', 'LULU.US', 'SNA.US',
                   'RHI.US', 'COP.US', 'PCG.US', 'SLB.US']

    # cant_load_tickers: ['KVUE.US', 'GFS.US', 'VLTO.US', 'ELV.US', 'RVTY.US', 'EG.US']

    cant_load_tickers = []

    for timeframe in timeframes:
        for ticket in tickers:
            try:
                load_data = SharesDataLoader(ticket)
                load_data.connect_to_metatrader5(path=f"C:\Program Files\FINAM MetaTrader 5\terminal64.exe")
                data = load_data.get_share_data(ticket=ticket, timeframe=timeframe, utc_till=utc_till, how_many_bars=how_many_bars, remove_today_bars=True)
                if len(data): print(f'- данные по тикеру {ticket} загружены: {data["time"].iloc[0]} - {data["time"].iloc[-1]} \t size: {len(data)}')
                load_data.export_to_csv_from_df(ticket=ticket, timeframe=timeframe, data=data, export_dir=os.path.join(current_dir, "csv_export_usa"), by_timeframes=True)
                load_data.disconnect_from_metatrader5()
            except Exception as e:
                print(f"Error: {e}")
                cant_load_tickers.append(ticket)

    print("cant_load_tickers:", cant_load_tickers)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()