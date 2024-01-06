# pip install opencv-python mysqlclient MetaTrader5 pandas pytz
import os

from core.get_shares_data_processor import SharesDataLoader
import MetaTrader5 as mt5       # импортируем модуль для подключения к MetaTrader5
import datetime, time
from threading import Thread    # для поточной закачки разных датафреймов
import cv2
import pandas as pd
pd.set_option('display.max_columns', 500) # сколько столбцов показываем
pd.set_option('display.width', 1500)      # макс. ширина таблицы для показа

import functions_thread  # to prevent hang Metatrader5
global time_of_getting_data


def prevent_hang(name):
    now = datetime.datetime.now()
    _delta = now - time_of_getting_data
    if _delta.seconds > 30:  # если зависло на 30 секунд, то удаляем процесс MetaTrader5
        print(f"MetaTrader5 is hang - killing process...")
        try: os.system("taskkill /F /IM terminal64.exe")  # run in pycharm
        except: print("Can't kill process of MetaTrader5...")


def get_hkd_shares(name):
    # print(".test.")
    # for i in range(10):
    #     time.sleep(5)
    #     print(".", end="")

    current_dir = os.path.dirname(os.path.abspath(__file__))  # текущая директория
    how_many_bars = 99999  # сколько баров закачать - предел...

    utc_till = datetime.datetime.now() + datetime.timedelta(days=1)  # получим данные по завтрашний день
    print(utc_till)

    # timeframes = {mt5.TIMEFRAME_M5, mt5.TIMEFRAME_M10, mt5.TIMEFRAME_M15, mt5.TIMEFRAME_M30, mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H4, mt5.TIMEFRAME_D1, mt5.TIMEFRAME_W1, mt5.TIMEFRAME_MN1}
    timeframes = {mt5.TIMEFRAME_M5, mt5.TIMEFRAME_M10, mt5.TIMEFRAME_M15, mt5.TIMEFRAME_M30, mt5.TIMEFRAME_H4,
                  mt5.TIMEFRAME_D1, mt5.TIMEFRAME_W1, mt5.TIMEFRAME_MN1}
    # timeframes = {mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H4, mt5.TIMEFRAME_D1, mt5.TIMEFRAME_W1, mt5.TIMEFRAME_MN1}
    # timeframes = {mt5.TIMEFRAME_M5, mt5.TIMEFRAME_M10, mt5.TIMEFRAME_M15, mt5.TIMEFRAME_M30}  # 99999 - предел...
    # timeframes = {mt5.TIMEFRAME_D1, }
    timeframes = {mt5.TIMEFRAME_W1, }
    # tickers = {"MSFT.US", "BAC.US"}
    # tickers = {"ALLFUTRTSI"}  # только через Финам ..

    tickers = ['1.SPB', '101.SPB', '1024.SPB', '1038.SPB', '1044.SPB', '1055.SPB', '1061.SPB', '1066.SPB', '1072.SPB',
     '1088.SPB', '1093.SPB', '1099.SPB', '1109.SPB', '1113.SPB', '1138.SPB', '1171.SPB', '1177.SPB', '12.SPB', '1209.SPB',
     '1211.SPB', '1288.SPB', '1299.SPB', '1336.SPB', '1339.SPB', '1347.SPB', '1359.SPB', '1368.SPB', '1378.SPB',
     '1385.SPB', '1398.SPB', '1548.SPB', '16.SPB', '1658.SPB', '168.SPB', '175.SPB', '1766.SPB', '1797.SPB', '1801.SPB',
     '1810.SPB', '1816.SPB', '1818.SPB', '1876.SPB', '1877.SPB', '1880.SPB', '1898.SPB', '1919.SPB', '1928.SPB',
     '1929.SPB', '1988.SPB', '1997.SPB', '1COV@DE.SPB', '2007.SPB', '2015.SPB', '2020.SPB', '2196.SPB', '2202.SPB',
     '2208.SPB', '2238.SPB', '2252.SPB', '2269.SPB', '2313.SPB', '2318.SPB', '2319.SPB', '2328.SPB', '2331.SPB',
     '2333.SPB', '2359.SPB', '2382.SPB', '2388.SPB', '241.SPB', '2518.SPB', '2600.SPB', '2601.SPB', '2618.SPB',
     '2628.SPB', '267.SPB', '268.SPB', '2688.SPB', '27.SPB', '2800.SPB', '2822.SPB', '2823.SPB', '2828.SPB', '285.SPB',
     '288.SPB', '2883.SPB', '2899.SPB', '291.SPB', '3.SPB', '3010.SPB', '3033.SPB', '3067.SPB', '3188.SPB', '322.SPB',
     '3319.SPB', '3328.SPB', '3347.SPB', '338.SPB', '3606.SPB', '3690.SPB', '3692.SPB', '3759.SPB', '3800.SPB',
     '386.SPB', '388.SPB', '3888.SPB', '3898.SPB', '390.SPB', '3900.SPB', '3908.SPB', '3968.SPB', '3988.SPB',
     '3993.SPB', '489.SPB', '5.SPB', '6.SPB', '6030.SPB', '6049.SPB', '6060.SPB', '6078.SPB', '6098.SPB', '6185.SPB',
     '66.SPB', '6618.SPB', '669.SPB', '6690.SPB', '670.SPB', '6837.SPB', '6862.SPB', '6865.SPB', '6869.SPB', '688.SPB',
     '6881.SPB', '6886.SPB', '6969.SPB', '700.SPB', '753.SPB', '763.SPB', '788.SPB', '82800.SPB', '82822.SPB',
     '82823.SPB', '82828.SPB', '83010.SPB', '83188.SPB', '836.SPB', '857.SPB', '868.SPB', '881.SPB', '914.SPB',
     '916.SPB', '939.SPB', '956.SPB', '960.SPB', '9618.SPB', '9626.SPB', '9633.SPB', '968.SPB', '9696.SPB', '9866.SPB',
     '9868.SPB', '9888.SPB', '992.SPB', '9922.SPB', '9926.SPB', '9961.SPB', '9988.SPB', '9992.SPB', '9995.SPB',
     '9999.SPB', 'A.SPB', 'AA.SPB', 'AAL.SPB', 'AAN.SPB', 'AAON.SPB', 'AAP.SPB', 'AAPL.SPB', 'AAXJ.SPB', 'ABBV.SPB',
     'ABCB.SPB', 'ABCL.SPB', 'ABG.SPB', 'ABM.SPB', 'ABNB.SPB', 'ABR.SPB', 'ABT.SPB', 'ACAD.SPB', 'ACGL.SPB', 'ACI.SPB',
     'ACIW.SPB', 'ACLS.SPB', 'ACM.SPB', 'ACMR.SPB', 'ACN.SPB', 'ACWI.SPB', 'ACWX.SPB', 'ADAP.SPB', 'ADBE.SPB',
     'ADI.SPB', 'ADM.SPB', 'ADP.SPB', 'ADPT.SPB', 'ADS@DE.SPB', 'ADSK.SPB', 'ADUS.SPB', 'AEE.SPB', 'AEIS.SPB',
     'AEM.SPB', 'AEO.SPB', 'AEP.SPB', 'AER.SPB', 'AES.SPB', 'AFG.SPB', 'AFKS.SPB', 'AFL.SPB', 'AFMD.SPB', 'AFRM.SPB',
     'AFX@DE.SPB', 'AG.SPB', 'AGCO.SPB', 'AGG.SPB', 'AGIO.SPB', 'AGNC.SPB', 'AGO.SPB', 'AI.SPB', 'AIG.SPB', 'AIN.SPB',
     'AIR.SPB', 'AIRC.SPB', 'AIT.SPB', 'AIV.SPB', 'AIZ.SPB', 'AJG.SPB', 'AKAM.SPB', 'ALB.SPB', 'ALC.SPB', 'ALE.SPB',
     'ALEC.SPB', 'ALFA0430.SPB', 'ALG.SPB', 'ALGM.SPB', 'ALGN.SPB', 'ALGT.SPB', 'ALIT.SPB', 'ALK.SPB', 'ALL.SPB',
     'ALLE.SPB', 'ALLK.SPB', 'ALLO.SPB', 'ALLY.SPB', 'ALNY.SPB', 'ALRM.SPB', 'ALRS.SPB', 'ALSN.SPB', 'ALT.SPB',
     'ALTR.SPB', 'ALV.SPB', 'ALV@DE.SPB', 'ALXO.SPB', 'AM.SPB', 'AMAT.SPB', 'AMBA.SPB', 'AMCR.SPB', 'AMCX.SPB',
     'AMD.SPB', 'AME.SPB', 'AMED.SPB', 'AMEH.SPB', 'AMG.SPB', 'AMGN.SPB', 'AMH.SPB', 'AMKR.SPB', 'AMN.SPB', 'AMP.SPB',
     'AMPH.SPB', 'AMR.SPB', 'AMSF.SPB', 'AMT.SPB', 'AMTI.SPB', 'AMWD.SPB', 'AMZN.SPB', 'AN.SPB', 'ANAB.SPB', 'ANDE.SPB',
     'ANET.SPB', 'ANF.SPB', 'ANGI.SPB', 'ANGL.SPB', 'ANIK.SPB', 'ANIP.SPB', 'ANSS.SPB', 'AON.SPB', 'AORT.SPB',
     'AOS.SPB', 'AOSL.SPB', 'AOUT.SPB', 'APA.SPB', 'APAM.SPB', 'APD.SPB', 'APEI.SPB', 'APH.SPB', 'APLE.SPB', 'APLS.SPB',
     'APLT.SPB', 'APO.SPB', 'APP.SPB', 'APPF.SPB', 'APPN.SPB', 'APPS.SPB', 'APTV.SPB', 'ARCC.SPB', 'ARCH.SPB',
     'ARCT.SPB', 'ARE.SPB', 'ARI.SPB', 'ARKF.SPB', 'ARMK.SPB', 'ARQT.SPB', 'ARRY.SPB', 'ARVL.SPB', 'ARVN.SPB',
     'ARW.SPB', 'ARWR.SPB', 'ASAN.SPB', 'ASGN.SPB', 'ASH.SPB', 'ASHR.SPB', 'ASIX.SPB', 'ASO.SPB', 'ASTR.SPB',
     'ASTS.SPB', 'ATEN.SPB', 'ATEX.SPB', 'ATGE.SPB', 'ATI.SPB', 'ATKR.SPB', 'ATNI.SPB', 'ATO.SPB', 'ATR.SPB',
     'ATRA.SPB', 'ATRC.SPB', 'ATRI.SPB', 'ATRO.SPB', 'ATRR01.SPB', 'ATUS.SPB', 'AUPH.SPB', 'AVA.SPB', 'AVAV.SPB',
     'AVB.SPB', 'AVGO.SPB', 'AVIR.SPB', 'AVNS.SPB', 'AVNT.SPB', 'AVT.SPB', 'AVTR.SPB', 'AVXL.SPB', 'AVY.SPB', 'AWH.SPB',
     'AWI.SPB', 'AWK.SPB', 'AWR.SPB', 'AX.SPB', 'AXGN.SPB', 'AXNX.SPB', 'AXON.SPB', 'AXP.SPB', 'AXSM.SPB', 'AXTA.SPB',
     'AYI.SPB', 'AYX.SPB', 'AZEK.SPB', 'AZN.SPB', 'AZO.SPB', 'AZPN.SPB', 'AZTA.SPB', 'Atomenpr01.SPB', 'BA.SPB',
     'BABA.SPB', 'BAC.SPB', 'BAH.SPB', 'BALL.SPB', 'BAND.SPB', 'BAS@DE.SPB', 'BAX.SPB', 'BAYN@DE.SPB', 'BBIO.SPB',
     'BBSI.SPB', 'BBWI.SPB', 'BBY.SPB', 'BC.SPB', 'BCC.SPB', 'BCE.SPB', 'BCO.SPB', 'BCPC.SPB', 'BCRX.SPB', 'BDC.SPB',
     'BDTX.SPB', 'BDX.SPB', 'BE.SPB', 'BEAM.SPB', 'BECN.SPB', 'BEL0226.SPB', 'BEL0230.SPB', 'BEL0231.SPB',
     'BEL0627.SPB', 'BEN.SPB', 'BERY.SPB', 'BF B.SPB', 'BFAM.SPB', 'BFH.SPB', 'BGNE.SPB', 'BGS.SPB', 'BH.SPB',
     'BHF.SPB', 'BIDU.SPB', 'BIG.SPB', 'BIGC.SPB', 'BIIB.SPB', 'BIL.SPB', 'BILI.SPB', 'BILL.SPB', 'BIO.SPB', 'BJ.SPB',
     'BJRI.SPB', 'BK.SPB', 'BKNG.SPB', 'BKR.SPB', 'BKU.SPB', 'BL.SPB', 'BLD.SPB', 'BLDP.SPB', 'BLDR.SPB', 'BLK.SPB',
     'BLKB.SPB', 'BLMN.SPB', 'BLNK.SPB', 'BLUE.SPB', 'BLZE.SPB', 'BMBL.SPB', 'BMI.SPB', 'BMO.SPB', 'BMRN.SPB',
     'BMW@DE.SPB', 'BMY.SPB', 'BNGO.SPB', 'BNTX.SPB', 'BOH.SPB', 'BOIL.SPB', 'BOKF.SPB', 'BOOT.SPB', 'BOSS@DE.SPB',
     'BOTZ.SPB', 'BOX.SPB', 'BPMC.SPB', 'BR.SPB', 'BRBR.SPB', 'BRC.SPB', 'BRK A.SPB', 'BRK B.SPB', 'BRKR.SPB',
     'BRO.SPB', 'BROS.SPB', 'BRX.SPB', 'BSX.SPB', 'BSY.SPB', 'BTAI.SPB', 'BTI.SPB', 'BUD.SPB', 'BURL.SPB', 'BVB@DE.SPB',
     'BWA.SPB', 'BWXT.SPB', 'BX.SPB', 'BXMT.SPB', 'BXP.SPB', 'BYND.SPB', 'BYON.SPB', 'BYSI.SPB', 'BZUN.SPB', 'C.SPB',
     'CABO.SPB', 'CACC.SPB', 'CACI.SPB', 'CAG.SPB', 'CAH.SPB', 'CALM.SPB', 'CAR.SPB', 'CARA.SPB', 'CARG.SPB',
     'CARR.SPB', 'CARS.SPB', 'CASY.SPB', 'CAT.SPB', 'CB.SPB', 'CBOM.SPB', 'CBOM0224EU.SPB', 'CBRE.SPB', 'CBRL.SPB',
     'CBSH.SPB', 'CBT.SPB', 'CBU.SPB', 'CC.SPB', 'CCI.SPB', 'CCJ.SPB', 'CCK.SPB', 'CCL.SPB', 'CCOI.SPB', 'CCS.SPB',
     'CCSI.SPB', 'CDAY.SPB', 'CDLX.SPB', 'CDNA.SPB', 'CDNS.SPB', 'CDW.SPB', 'CE.SPB', 'CEG.SPB', 'CELH.SPB', 'CENT.SPB',
     'CENTA.SPB', 'CERE.SPB', 'CEVA.SPB', 'CF.SPB', 'CFG.SPB', 'CFLT.SPB', 'CFR.SPB', 'CG.SPB', 'CGEN.SPB', 'CGNT.SPB',
     'CGNX.SPB', 'CHAU.SPB', 'CHCO.SPB', 'CHD.SPB', 'CHDN.SPB', 'CHE.SPB', 'CHEF.SPB', 'CHGG.SPB', 'CHH.SPB',
     'CHKP.SPB', 'CHMF.SPB', 'CHPT.SPB', 'CHRS.SPB', 'CHRW.SPB', 'CHTR.SPB', 'CHWY.SPB', 'CHX.SPB', 'CI.SPB',
     'CIAN@US.SPB', 'CIBR.SPB', 'CIEN.SPB', 'CINF.SPB', 'CL.SPB', 'CLB.SPB', 'CLBK.SPB', 'CLDT.SPB', 'CLF.SPB',
     'CLH.SPB', 'CLOV.SPB', 'CLSK.SPB', 'CLVT.SPB', 'CLX.SPB', 'CM.SPB', 'CMA.SPB', 'CMC.SPB', 'CMCO.SPB', 'CMCSA.SPB',
     'CME.SPB', 'CMG.SPB', 'CMI.SPB', 'CMP.SPB', 'CMS.SPB', 'CNC.SPB', 'CNHI.SPB', 'CNI.SPB', 'CNK.SPB', 'CNMD.SPB',
     'CNNE.SPB', 'CNO.SPB', 'CNP.SPB', 'CNQ.SPB', 'CNS.SPB', 'CNX.SPB', 'CNXC.SPB', 'CNXN.SPB', 'CNYA.SPB', 'COF.SPB',
     'COFS.SPB', 'COHR.SPB', 'COHU.SPB', 'COIN.SPB', 'COKE.SPB', 'COLB.SPB', 'COLD.SPB', 'COLM.SPB', 'CON@DE.SPB',
     'COO.SPB', 'COOP.SPB', 'COP.SPB', 'COPX.SPB', 'COR.SPB', 'CORR.SPB', 'CORT.SPB', 'COST.SPB', 'COTY.SPB',
     'COUR.SPB', 'CP.SPB', 'CPB.SPB', 'CPNG.SPB', 'CPRI.SPB', 'CPRT.SPB', 'CPS.SPB', 'CPT.SPB', 'CQQQ.SPB', 'CR.SPB',
     'CRI.SPB', 'CRL.SPB', 'CRM.SPB', 'CRMT.SPB', 'CRNC.SPB', 'CROX.SPB', 'CRS.SPB', 'CRSP.SPB', 'CRSR.SPB', 'CRUS.SPB',
     'CRVL.SPB', 'CRWD.SPB', 'CSCO.SPB', 'CSGP.SPB', 'CSGS.SPB', 'CSIQ.SPB', 'CSL.SPB', 'CSWI.SPB', 'CSX.SPB',
     'CTAS.SPB', 'CTLT.SPB', 'CTRA.SPB', 'CTSH.SPB', 'CTVA.SPB', 'CUBE.SPB', 'CUZ.SPB', 'CVCO.SPB', 'CVGW.SPB',
     'CVLT.SPB', 'CVM.SPB', 'CVNA.SPB', 'CVS.SPB', 'CVX.SPB', 'CW.SPB', 'CWB.SPB', 'CWEN.SPB', 'CWH.SPB', 'CWST.SPB',
     'CWT.SPB', 'CXT.SPB', 'CXW.SPB', 'CYBR.SPB', 'CYRX.SPB', 'CYTK.SPB', 'CZR.SPB', 'D.SPB', 'DAL.SPB', 'DAN.SPB',
     'DAR.SPB', 'DASH.SPB', 'DAVA.SPB', 'DAWN.SPB', 'DB1@DE.SPB', 'DBK@DE.SPB', 'DBX.SPB', 'DCI.SPB', 'DCPH.SPB',
     'DD.SPB', 'DDD.SPB', 'DDOG.SPB', 'DDS.SPB', 'DE.SPB', 'DECK.SPB', 'DEI.SPB', 'DELL.SPB', 'DFS.SPB', 'DG.SPB',
     'DGRO.SPB', 'DGX.SPB', 'DHER@DE.SPB', 'DHI.SPB', 'DHL@DE.SPB', 'DHR.SPB', 'DIA.SPB', 'DINO.SPB', 'DIOD.SPB',
     'DIRP01.SPB', 'DIRP02.SPB', 'DIRP03.SPB', 'DIS.SPB', 'DISH.SPB', 'DK.SPB', 'DKNG.SPB', 'DKS.SPB', 'DLB.SPB',
     'DLO.SPB', 'DLR.SPB', 'DLTH.SPB', 'DLTR.SPB', 'DLX.SPB', 'DM.SPB', 'DMNN01.SPB', 'DMTK.SPB', 'DNA.SPB', 'DNB.SPB',
     'DNLI.SPB', 'DNMR.SPB', 'DNOW.SPB', 'DOCN.SPB', 'DOCS.SPB', 'DOCU.SPB', 'DORM.SPB', 'DOV.SPB', 'DOW.SPB',
     'DPZ.SPB', 'DRI.SPB', 'DRIV.SPB', 'DRQ.SPB', 'DSKY.SPB', 'DT.SPB', 'DTE@DE.SPB', 'DUK.SPB', 'DUOL.SPB', 'DUST.SPB',
     'DV.SPB', 'DVA.SPB', 'DVN.SPB', 'DVY.SPB', 'DXC.SPB', 'DXCM.SPB', 'DXJ.SPB', 'DY.SPB', 'EA.SPB', 'EAF.SPB',
     'EAR.SPB', 'EAT.SPB', 'EBAY.SPB', 'EBS.SPB', 'ECH.SPB', 'ECL.SPB', 'ECPG.SPB', 'ED.SPB', 'EDIT.SPB', 'EEFT.SPB',
     'EEM.SPB', 'EFA.SPB', 'EFG.SPB', 'EFV.SPB', 'EFX.SPB', 'EG.SPB', 'EGHT.SPB', 'EGP.SPB', 'EGPT0329.SPB',
     'EGPT0431.SPB', 'EGRX.SPB', 'EHTH.SPB', 'EIDO.SPB', 'EIS.SPB', 'EIX.SPB', 'EL.SPB', 'ELAN.SPB', 'ELFV.SPB',
     'ELS.SPB', 'ELV.SPB', 'EMB.SPB', 'EMBC.SPB', 'EME.SPB', 'EMN.SPB', 'EMR.SPB', 'ENB.SPB', 'ENOV.SPB', 'ENPH.SPB',
     'ENR.SPB', 'ENS.SPB', 'ENSG.SPB', 'ENTA.SPB', 'ENTG.SPB', 'ENV.SPB', 'ENVX.SPB', 'EOAN@DE.SPB', 'EOG.SPB',
     'EPAM.SPB', 'EPC.SPB', 'EPI.SPB', 'EPP.SPB', 'EQH.SPB', 'EQIX.SPB', 'EQR.SPB', 'EQT.SPB', 'ERIE.SPB', 'ES.SPB',
     'ESAB.SPB', 'ESE.SPB', 'ESGD.SPB', 'ESGE.SPB', 'ESGR.SPB', 'ESGU.SPB', 'ESGV.SPB', 'ESPR.SPB', 'ESS.SPB',
     'ESTC.SPB', 'ET.SPB', 'ETD.SPB', 'ETLN@GS.SPB', 'ETN.SPB', 'ETR.SPB', 'ETRN.SPB', 'ETSY.SPB', 'EUFN.SPB',
     'EVBG.SPB', 'EVER.SPB', 'EVH.SPB', 'EVK@DE.SPB', 'EVR.SPB', 'EVRG.SPB', 'EVT@DE.SPB', 'EW.SPB', 'EWA.SPB',
     'EWBC.SPB', 'EWC.SPB', 'EWD.SPB', 'EWG.SPB', 'EWH.SPB', 'EWI.SPB', 'EWJ.SPB', 'EWL.SPB', 'EWM.SPB', 'EWN.SPB',
     'EWP.SPB', 'EWQ.SPB', 'EWS.SPB', 'EWT.SPB', 'EWU.SPB', 'EWW.SPB', 'EWY.SPB', 'EWZ.SPB', 'EXAS.SPB', 'EXC.SPB',
     'EXEL.SPB', 'EXLS.SPB', 'EXP.SPB', 'EXPD.SPB', 'EXPE.SPB', 'EXPI.SPB', 'EXPO.SPB', 'EXR.SPB', 'EYE.SPB', 'EZA.SPB',
     'EZU.SPB', 'F.SPB', 'FAF.SPB', 'FANG.SPB', 'FARO.SPB', 'FAS.SPB', 'FAST.SPB', 'FATE.SPB', 'FAZ.SPB', 'FBIN.SPB',
     'FCEL.SPB', 'FCFS.SPB', 'FCN.SPB', 'FCNCA.SPB', 'FCX.SPB', 'FDS.SPB', 'FDX.SPB', 'FE.SPB', 'FEES.SPB', 'FELE.SPB',
     'FEZ.SPB', 'FFIN.SPB', 'FFIV.SPB', 'FG.SPB', 'FGEN.SPB', 'FHI.SPB', 'FI.SPB', 'FICO.SPB', 'FIGS.SPB', 'FIPO.SPB',
     'FIS.SPB', 'FITB.SPB', 'FIVE.SPB', 'FIVE@GS.SPB', 'FIVN.SPB', 'FIXP@GS.SPB', 'FIZZ.SPB', 'FL.SPB', 'FLGT.SPB',
     'FLO.SPB', 'FLR.SPB', 'FLS.SPB', 'FLT.SPB', 'FLWS.SPB', 'FLYW.SPB', 'FMC.SPB', 'FME@DE.SPB', 'FND.SPB', 'FNF.SPB',
     'FNKO.SPB', 'FNV.SPB', 'FOLD.SPB', 'FORM.SPB', 'FORR.SPB', 'FOUR.SPB', 'FOX.SPB', 'FOXA.SPB', 'FOXF.SPB', 'FR.SPB',
     'FRE@DE.SPB', 'FRHC.SPB', 'FRME.SPB', 'FROG.SPB', 'FRPH.SPB', 'FRPT.SPB', 'FRT.SPB', 'FSLR.SPB', 'FSLY.SPB',
     'FSR.SPB', 'FTCH.SPB', 'FTCI.SPB', 'FTDR.SPB', 'FTI.SPB', 'FTNT.SPB', 'FTRE.SPB', 'FTV.SPB', 'FUL.SPB', 'FULC.SPB',
     'FVRR.SPB', 'FWRD.SPB', 'FXI.SPB', 'G.SPB', 'GATX.SPB', 'GAZP.SPB', 'GAZP0327.SPB', 'GAZP0837.SPB', 'GAZP1124.SPB',
     'GBCI.SPB', 'GBX.SPB', 'GCHE.SPB', 'GCO.SPB', 'GD.SPB', 'GDDY.SPB', 'GDEV.SPB', 'GDOT.SPB', 'GDRX.SPB', 'GDX.SPB',
     'GDXJ.SPB', 'GE.SPB', 'GEF.SPB', 'GEHC.SPB', 'GEN.SPB', 'GES.SPB', 'GEVO.SPB', 'GGG.SPB', 'GH.SPB', 'GHC.SPB',
     'GILD.SPB', 'GIS.SPB', 'GKOS.SPB', 'GL.SPB', 'GLBE.SPB', 'GLD.SPB', 'GLGR02.SPB', 'GLOB.SPB', 'GLPI.SPB',
     'GLTR.SPB', 'GLTR@GS.SPB', 'GLW.SPB', 'GM.SPB', 'GMED.SPB', 'GMKN.SPB', 'GMS.SPB', 'GNL.SPB', 'GNRC.SPB',
     'GNTX.SPB', 'GO.SPB', 'GOGL.SPB', 'GOLD.SPB', 'GOOG.SPB', 'GOOGL.SPB', 'GOSS.SPB', 'GPC.SPB', 'GPI.SPB', 'GPK.SPB',
     'GPN.SPB', 'GPRO.SPB', 'GPS.SPB', 'GRBK.SPB', 'GRMN.SPB', 'GROWS.SPB', 'GRPH.SPB', 'GS.SPB', 'GSHD.SPB',
     'GSLC.SPB', 'GT.SPB', 'GTHX.SPB', 'GTLB.SPB', 'GTLS.SPB', 'GTN.SPB', 'GTX.SPB', 'GVA.SPB', 'GWRE.SPB', 'GWW.SPB',
     'GXC.SPB', 'GXO.SPB', 'H.SPB', 'HA.SPB', 'HAE.SPB', 'HAIN.SPB', 'HAL.SPB', 'HALO.SPB', 'HAS.SPB', 'HASI.SPB',
     'HBAN.SPB', 'HBI.SPB', 'HCA.SPB', 'HCAT.SPB', 'HCC.SPB', 'HCSG.SPB', 'HD.SPB', 'HDV.SPB', 'HE.SPB', 'HEAR.SPB',
     'HEI.SPB', 'HEI@DE.SPB', 'HEN3@DE.SPB', 'HES.SPB', 'HGV.SPB', 'HHH.SPB', 'HHR.SPB', 'HI.SPB', 'HIBB.SPB',
     'HIG.SPB', 'HII.SPB', 'HIMS.SPB', 'HIW.SPB', 'HLF.SPB', 'HLI.SPB', 'HLNE.SPB', 'HLT.SPB', 'HOG.SPB', 'HOLX.SPB',
     'HON.SPB', 'HOOD.SPB', 'HOT@DE.SPB', 'HP.SPB', 'HPE.SPB', 'HPQ.SPB', 'HQY.SPB', 'HR.SPB', 'HRB.SPB', 'HRL.SPB',
     'HRMY.SPB', 'HRTX.SPB', 'HSIC.SPB', 'HST.SPB', 'HSY.SPB', 'HTHT.SPB', 'HUBB.SPB', 'HUBG.SPB', 'HUBS.SPB',
     'HUM.SPB', 'HUN.SPB', 'HURN.SPB', 'HWM.SPB', 'HXL.SPB', 'HYDR.SPB', 'HYG.SPB', 'HYLN.SPB', 'HZO.SPB', 'IAC.SPB',
     'IART.SPB', 'IAU.SPB', 'IBB.SPB', 'IBKR.SPB', 'IBM.SPB', 'IBN.SPB', 'IBP.SPB', 'IBTX.SPB', 'ICE.SPB', 'ICFI.SPB',
     'ICLN.SPB', 'ICLR.SPB', 'ICUI.SPB', 'IDA.SPB', 'IDCC.SPB', 'IDXX.SPB', 'IEF.SPB', 'IEFA.SPB', 'IEMG.SPB',
     'IEV.SPB', 'IEX.SPB', 'IFF.SPB', 'IFX@DE.SPB', 'IGMS.SPB', 'IGOV.SPB', 'IGSB.SPB', 'IGV.SPB', 'IHI.SPB',
     'IIPR.SPB', 'IJH.SPB', 'IJJ.SPB', 'IJK.SPB', 'IJR.SPB', 'ILF.SPB', 'ILMN.SPB', 'INCY.SPB', 'INDA.SPB', 'INDB.SPB',
     'INGN.SPB', 'INGR.SPB', 'INMD.SPB', 'INO.SPB', 'INSG.SPB', 'INSM.SPB', 'INSP.SPB', 'INTC.SPB', 'INTU.SPB',
     'INVA.SPB', 'INVH.SPB', 'IONS.SPB', 'IOSP.SPB', 'IOVA.SPB', 'IP.SPB', 'IPAR.SPB', 'IPG.SPB', 'IPGP.SPB',
     'IQLT.SPB', 'IQV.SPB', 'IR.SPB', 'IRAO.SPB', 'IRBT.SPB', 'IRDM.SPB', 'IRM.SPB', 'IRTC.SPB', 'IRWD.SPB',
     'ISBNK0424.SPB', 'ISRG.SPB', 'IT.SPB', 'ITA.SPB', 'ITB.SPB', 'ITCI.SPB', 'ITGR.SPB', 'ITOT.SPB', 'ITRI.SPB',
     'ITT.SPB', 'ITW.SPB', 'IUSG.SPB', 'IUSV.SPB', 'IVE.SPB', 'IVV.SPB', 'IVW.SPB', 'IVZ.SPB', 'IWB.SPB', 'IWD.SPB',
     'IWF.SPB', 'IWM.SPB', 'IWN.SPB', 'IWO.SPB', 'IWP.SPB', 'IWR.SPB', 'IWS.SPB', 'IWV.SPB', 'IXC.SPB', 'IXG.SPB',
     'IXN.SPB', 'IXUS.SPB', 'IYE.SPB', 'IYF.SPB', 'IYR.SPB', 'IYT.SPB', 'IYW.SPB', 'J.SPB', 'JACK.SPB', 'JAMF.SPB',
     'JBHT.SPB', 'JBL.SPB', 'JBSS.SPB', 'JBT.SPB', 'JCI.SPB', 'JD.SPB', 'JEF.SPB', 'JELD.SPB', 'JHG.SPB', 'JJSF.SPB',
     'JKHY.SPB', 'JLL.SPB', 'JNJ.SPB', 'JNK.SPB', 'JNPR.SPB', 'JNUG.SPB', 'JOBY.SPB', 'JOUT.SPB', 'JPM.SPB', 'JWN.SPB',
     'K.SPB', 'KAI.SPB', 'KALU.SPB', 'KAP@GS.SPB', 'KBE.SPB', 'KBH.SPB', 'KBWB.SPB', 'KD.SPB', 'KDP.SPB', 'KEP.SPB',
     'KEX.SPB', 'KEY.SPB', 'KEYS.SPB', 'KFY.SPB', 'KGC.SPB', 'KHC.SPB', 'KIDS.SPB', 'KIE.SPB', 'KIM.SPB', 'KKR.SPB',
     'KLAC.SPB', 'KLG.SPB', 'KLIC.SPB', 'KMB.SPB', 'KMI.SPB', 'KMPR.SPB', 'KMT.SPB', 'KMX.SPB', 'KNF.SPB', 'KNSL.SPB',
     'KNX.SPB', 'KO.SPB', 'KOD.SPB', 'KOPN.SPB', 'KR.SPB', 'KRC.SPB', 'KRG.SPB', 'KRTX.SPB', 'KRYS.SPB', 'KSPI@GS.SPB',
     'KSS.SPB', 'KTB.SPB', 'KTOS.SPB', 'KWEB.SPB', 'KWR.SPB', 'KYMR.SPB', 'L.SPB', 'LAAC.SPB', 'LAC.SPB', 'LAD.SPB',
     'LANC.SPB', 'LASR.SPB', 'LAZR.SPB', 'LBRDK.SPB', 'LC.SPB', 'LCID.SPB', 'LCII.SPB', 'LDOS.SPB', 'LEA.SPB',
     'LECO.SPB', 'LEG.SPB', 'LEGH.SPB', 'LEN.SPB', 'LEVI.SPB', 'LFST.SPB', 'LFUS.SPB', 'LGIH.SPB', 'LGND.SPB', 'LH.SPB',
     'LHA@DE.SPB', 'LHX.SPB', 'LI.SPB', 'LICY.SPB', 'LII.SPB', 'LIN.SPB', 'LIT.SPB', 'LITE.SPB', 'LKOH.SPB', 'LKQ.SPB',
     'LLY.SPB', 'LMT.SPB', 'LNC.SPB', 'LNG.SPB', 'LNN.SPB', 'LNT.SPB', 'LNTH.SPB', 'LOGI.SPB', 'LOPE.SPB', 'LOW.SPB',
     'LPL.SPB', 'LPLA.SPB', 'LPRO.SPB', 'LPSN.SPB', 'LPX.SPB', 'LQD.SPB', 'LRCX.SPB', 'LRN.SPB', 'LSCC.SPB', 'LSPD.SPB',
     'LSRG.SPB', 'LSTR.SPB', 'LTHM.SPB', 'LUK1126.SPB', 'LULU.SPB', 'LUMN.SPB', 'LUV.SPB', 'LVS.SPB', 'LW.SPB',
     'LYB.SPB', 'LYEL.SPB', 'LYFT.SPB', 'LYV.SPB', 'M.SPB', 'MA.SPB', 'MAA.SPB', 'MAC.SPB', 'MAGN.SPB', 'MAN.SPB',
     'MANH.SPB', 'MANU.SPB', 'MAR.SPB', 'MARA.SPB', 'MAS.SPB', 'MASI.SPB', 'MAT.SPB', 'MATV.SPB', 'MATX.SPB', 'MBC.SPB',
     'MBG@DE.SPB', 'MBUU.SPB', 'MC.SPB', 'MCD.SPB', 'MCHI.SPB', 'MCHP.SPB', 'MCK.SPB', 'MCO.SPB', 'MCRI.SPB', 'MD.SPB',
     'MDB.SPB', 'MDC.SPB', 'MDGL.SPB', 'MDLZ.SPB', 'MDRX.SPB', 'MDT.SPB', 'MDU.SPB', 'MDY.SPB', 'MED.SPB', 'MEDP.SPB',
     'MEI.SPB', 'MELI.SPB', 'MET.SPB', 'META.SPB', 'METC.SPB', 'METCB.SPB', 'MGA.SPB', 'MGK.SPB', 'MGM.SPB', 'MGNT.SPB',
     'MGPI.SPB', 'MGRC.SPB', 'MGY.SPB', 'MHK.SPB', 'MHO.SPB', 'MIDD.SPB', 'MKC.SPB', 'MKL.SPB', 'MKSI.SPB', 'MKTX.SPB',
     'MLAB.SPB', 'MLCO.SPB', 'MLKN.SPB', 'MLM.SPB', 'MLNK.SPB', 'MMC.SPB', 'MMI.SPB', 'MMM.SPB', 'MMS.SPB', 'MMSI.SPB',
     'MNDY.SPB', 'MNRO.SPB', 'MNST.SPB', 'MO.SPB', 'MOAT.SPB', 'MODG.SPB', 'MODV.SPB', 'MOH.SPB', 'MOMO.SPB',
     'MORN.SPB', 'MOS.SPB', 'MOV.SPB', 'MP.SPB', 'MPC.SPB', 'MPW.SPB', 'MPWR.SPB', 'MQ.SPB', 'MRC.SPB', 'MRK.SPB',
     'MRK@DE.SPB', 'MRNA.SPB', 'MRO.SPB', 'MRTX.SPB', 'MRVI.SPB', 'MRVL.SPB', 'MS.SPB', 'MSA.SPB', 'MSCI.SPB',
     'MSEX.SPB', 'MSFT.SPB', 'MSGE.SPB', 'MSGS.SPB', 'MSI.SPB', 'MSM.SPB', 'MSNG.SPB', 'MSTR.SPB', 'MTB.SPB',
     'MTCH.SPB', 'MTD.SPB', 'MTG.SPB', 'MTH.SPB', 'MTKB.SPB', 'MTN.SPB', 'MTRN.SPB', 'MTS18soc.SPB', 'MTSS.SPB',
     'MTTR.SPB', 'MTUM.SPB', 'MTX.SPB', 'MTX@DE.SPB', 'MU.SPB', 'MUR.SPB', 'MUSA.SPB', 'MUV2@DE.SPB', 'MVIS.SPB',
     'MXL.SPB', 'MYGN.SPB', 'MYRG.SPB', 'NABL.SPB', 'NAIL.SPB', 'NARI.SPB', 'NATL.SPB', 'NAVI.SPB', 'NBIX.SPB',
     'NCNO.SPB', 'NDAQ.SPB', 'NDSN.SPB', 'NEE.SPB', 'NEM.SPB', 'NEO.SPB', 'NEOG.SPB', 'NET.SPB', 'NEU.SPB', 'NFE.SPB',
     'NFG.SPB', 'NFLX.SPB', 'NGVT.SPB', 'NHI.SPB', 'NI.SPB', 'NIC.SPB', 'NICE.SPB', 'NJR.SPB', 'NKE.SPB', 'NKLA.SPB',
     'NKTR.SPB', 'NLMK.SPB', 'NLY.SPB', 'NMIH.SPB', 'NMTP.SPB', 'NOC.SPB', 'NOK.SPB', 'NOV.SPB', 'NOVA.SPB', 'NOW.SPB',
     'NPK.SPB', 'NRG.SPB', 'NRIX.SPB', 'NSC.SPB', 'NSIT.SPB', 'NSP.SPB', 'NSSC.SPB', 'NTAP.SPB', 'NTCO.SPB', 'NTCT.SPB',
     'NTES.SPB', 'NTGR.SPB', 'NTLA.SPB', 'NTNX.SPB', 'NTR.SPB', 'NTRA.SPB', 'NTRS.SPB', 'NU.SPB', 'NUE.SPB', 'NUGT.SPB',
     'NUS.SPB', 'NVAX.SPB', 'NVCR.SPB', 'NVDA.SPB', 'NVEE.SPB', 'NVR.SPB', 'NVRI.SPB', 'NVRO.SPB', 'NVS.SPB',
     'NVST.SPB', 'NVTA.SPB', 'NVTK.SPB', 'NWE.SPB', 'NWL.SPB', 'NWLI.SPB', 'NWS.SPB', 'NWSA.SPB', 'NXPI.SPB',
     'NXST.SPB', 'NYCB.SPB', 'NYT.SPB', 'O.SPB', 'OABI.SPB', 'OC.SPB', 'ODFL.SPB', 'OEF.SPB', 'OFIX.SPB', 'OGE.SPB',
     'OGN.SPB', 'OGS.SPB', 'OHI.SPB', 'OI.SPB', 'OIH.SPB', 'OII.SPB', 'OIS.SPB', 'OKE.SPB', 'OKTA.SPB', 'OLED.SPB',
     'OLLI.SPB', 'OLN.SPB', 'OMA0128.SPB', 'OMA0148.SPB', 'OMC.SPB', 'OMCL.SPB', 'OMF.SPB', 'ON.SPB', 'ONL.SPB',
     'ONTO.SPB', 'ORA.SPB', 'ORCL.SPB', 'ORG1P1.SPB', 'ORI.SPB', 'ORLY.SPB', 'ORMP.SPB', 'OSIS.SPB', 'OSK.SPB',
     'OSUR.SPB', 'OTIS.SPB', 'OUST.SPB', 'OVV.SPB', 'OXY.SPB', 'OZON@US.SPB', 'PAAS.SPB', 'PACB.SPB', 'PAG.SPB',
     'PAGS.SPB', 'PALL.SPB', 'PANW.SPB', 'PAR.SPB', 'PARA.SPB', 'PATH.SPB', 'PATK.SPB', 'PAY.SPB', 'PAYC.SPB',
     'PAYO.SPB', 'PAYX.SPB', 'PB.SPB', 'PBA.SPB', 'PBF.SPB', 'PBH.SPB', 'PBI.SPB', 'PBW.SPB', 'PCAR.SPB', 'PCG.SPB',
     'PCH.SPB', 'PCOR.SPB', 'PCRX.SPB', 'PCTY.SPB', 'PCVX.SPB', 'PD.SPB', 'PDBC.SPB', 'PDCO.SPB', 'PDS.SPB', 'PEAK.SPB',
     'PEG.SPB', 'PEGA.SPB', 'PEN.SPB', 'PENN.SPB', 'PEP.SPB', 'PETQ.SPB', 'PFE.SPB', 'PFG.SPB', 'PFGC.SPB', 'PFSI.SPB',
     'PG.SPB', 'PGNY.SPB', 'PGR.SPB', 'PGTI.SPB', 'PH.SPB', 'PHIN.SPB', 'PHM.SPB', 'PHO.SPB', 'PHOR.SPB', 'PI.SPB',
     'PICK.SPB', 'PII.SPB', 'PIKK.SPB', 'PINC.SPB', 'PINS.SPB', 'PIPR.SPB', 'PJT.SPB', 'PKG.SPB', 'PKW.SPB', 'PLAY.SPB',
     'PLCE.SPB', 'PLD.SPB', 'PLL.SPB', 'PLNT.SPB', 'PLTK.SPB', 'PLTR.SPB', 'PLUG.SPB', 'PLUS.SPB', 'PLXS.SPB',
     'PLZL.SPB', 'PM.SPB', 'PMT.SPB', 'PNC.SPB', 'PNFP.SPB', 'PNTG.SPB', 'PNW.SPB', 'PODD.SPB', 'POOL.SPB', 'POR.SPB',
     'POST.SPB', 'POWI.SPB', 'PPC.SPB', 'PPG.SPB', 'PPL.SPB', 'PPLT.SPB', 'PRAA.SPB', 'PRFT.SPB', 'PRG.SPB', 'PRGS.SPB',
     'PRI.SPB', 'PRLB.SPB', 'PRO.SPB', 'PRTA.SPB', 'PRTS.SPB', 'PRU.SPB', 'PSA.SPB', 'PSEC.SPB', 'PSMT.SPB', 'PSN.SPB',
     'PSTG.SPB', 'PSX.SPB', 'PTC.SPB', 'PTCT.SPB', 'PTON.SPB', 'PUBM.SPB', 'PUM@DE.SPB', 'PUMP.SPB', 'PVH.SPB',
     'PWR.SPB', 'PXD.SPB', 'PYPL.SPB', 'PZZA.SPB', 'QCOM.SPB', 'QDEL.SPB', 'QGEN.SPB', 'QLD.SPB', 'QLYS.SPB',
     'QNCX.SPB', 'QNST.SPB', 'QQQ.SPB', 'QRTEA.SPB', 'QRVO.SPB', 'QS.SPB', 'QTWO.SPB', 'QUAL.SPB', 'QYLD.SPB', 'R.SPB',
     'RACE.SPB', 'RAGR.SPB', 'RAMP.SPB', 'RARE.SPB', 'RBA.SPB', 'RBC.SPB', 'RBLX.SPB', 'RCL.SPB', 'RCUS.SPB',
     'RDFN.SPB', 'RDN.SPB', 'RDY.SPB', 'REG.SPB', 'REGN.SPB', 'RELY.SPB', 'REMX.SPB', 'REX.SPB', 'REYN.SPB', 'REZI.SPB',
     'RF.SPB', 'RGA.SPB', 'RGEN.SPB', 'RGLD.SPB', 'RGNX.SPB', 'RGR.SPB', 'RH.SPB', 'RHI.SPB', 'RHM@DE.SPB', 'RIG.SPB',
     'RIO.SPB', 'RIOT.SPB', 'RITM.SPB', 'RIVN.SPB', 'RJF.SPB', 'RKLB.SPB', 'RKT.SPB', 'RL.SPB', 'RLAY.SPB', 'RMD.SPB',
     'RNG.SPB', 'RNR.SPB', 'ROCK.SPB', 'ROG.SPB', 'ROK.SPB', 'ROKU.SPB', 'ROL.SPB', 'ROP.SPB', 'ROST.SPB', 'RPD.SPB',
     'RPM.SPB', 'RPV.SPB', 'RRBI.SPB', 'RRC.SPB', 'RRGB.SPB', 'RRR.SPB', 'RRX.SPB', 'RS.SPB', 'RSG.SPB', 'RSKD.SPB',
     'RSP.SPB', 'RTKM.SPB', 'RTO.SPB', 'RTX.SPB', 'RU000A0JXTY7.SPB', 'RU000A1008J4.SPB', 'RU000A100FE5.SPB',
     'RU000A100N12.SPB', 'RU000A100P85.SPB', 'RU000A103FP5.SPB', 'RUN.SPB', 'RUS0628.SPB', 'RVLV.SPB', 'RVMD.SPB',
     'RVNC.SPB', 'RVTY.SPB', 'RWE@DE.SPB', 'RXO.SPB', 'RXRX.SPB', 'RY.SPB', 'RYN.SPB', 'RYTM.SPB', 'RZD0527.SPB',
     'S.SPB', 'SAGE.SPB', 'SAH.SPB', 'SAIA.SPB', 'SAIC.SPB', 'SAM.SPB', 'SAP.SPB', 'SAP@DE.SPB', 'SATS.SPB', 'SAVA.SPB',
     'SAVE.SPB', 'SBAC.SPB', 'SBCF.SPB', 'SBER.SPB', 'SBERP.SPB', 'SBGI.SPB', 'SBH.SPB', 'SBRA.SPB', 'SBUX.SPB',
     'SCCO.SPB', 'SCHA.SPB', 'SCHB.SPB', 'SCHD.SPB', 'SCHE.SPB', 'SCHF.SPB', 'SCHG.SPB', 'SCHW.SPB', 'SCHX.SPB',
     'SCI.SPB', 'SCJ.SPB', 'SCL.SPB', 'SCSC.SPB', 'SCZ.SPB', 'SDGR.SPB', 'SDS.SPB', 'SDY.SPB', 'SEDG.SPB', 'SEE.SPB',
     'SEGE2P1R.SPB', 'SEGE2P3R.SPB', 'SEIC.SPB', 'SF.SPB', 'SFIX.SPB', 'SFM.SPB', 'SGENperp.SPB', 'SGMO.SPB', 'SH.SPB',
     'SHAK.SPB', 'SHEL.SPB', 'SHEN.SPB', 'SHL@DE.SPB', 'SHLS.SPB', 'SHOO.SPB', 'SHOP.SPB', 'SHW.SPB', 'SIBN.SPB',
     'SIE@DE.SPB', 'SIG.SPB', 'SIGA.SPB', 'SIGI.SPB', 'SILK.SPB', 'SIRI.SPB', 'SITE.SPB', 'SITM.SPB', 'SJM.SPB',
     'SJW.SPB', 'SKIN.SPB', 'SKLZ.SPB', 'SKM.SPB', 'SKT.SPB', 'SKX.SPB', 'SKY.SPB', 'SLAB.SPB', 'SLB.SPB', 'SLDB.SPB',
     'SLG.SPB', 'SLGN.SPB', 'SLM.SPB', 'SLP.SPB', 'SLQT.SPB', 'SLV.SPB', 'SLVM.SPB', 'SMAR.SPB', 'SMG.SPB', 'SMH.SPB',
     'SMPL.SPB', 'SMTC.SPB', 'SNA.SPB', 'SNAP.SPB', 'SNBR.SPB', 'SNGS.SPB', 'SNGSP.SPB', 'SNOW.SPB', 'SNPS.SPB',
     'SNX.SPB', 'SNY.SPB', 'SO.SPB', 'SOFI.SPB', 'SOFL.SPB', 'SOHU.SPB', 'SON.SPB', 'SONO.SPB', 'SONY.SPB', 'SOXL.SPB',
     'SOXS.SPB', 'SOXX.SPB', 'SP.SPB', 'SPB@US.SPB', 'SPBE.SPB', 'SPCE.SPB', 'SPDW.SPB', 'SPEM.SPB', 'SPG.SPB',
     'SPGI.SPB', 'SPHQ.SPB', 'SPHR.SPB', 'SPLG.SPB', 'SPLK.SPB', 'SPLV.SPB', 'SPNS.SPB', 'SPOT.SPB', 'SPR.SPB',
     'SPSB.SPB', 'SPSC.SPB', 'SPT.SPB', 'SPXL.SPB', 'SPXS.SPB', 'SPXU.SPB', 'SPY.SPB', 'SPYD.SPB', 'SQ.SPB', 'SQQQ.SPB',
     'SQSP.SPB', 'SR.SPB', 'SRC.SPB', 'SRCL.SPB', 'SRDX.SPB', 'SRE.SPB', 'SRI.SPB', 'SRPT.SPB', 'SSB.SPB', 'SSD.SPB',
     'SSNC.SPB', 'SSTK.SPB', 'STAA.SPB', 'STAG.SPB', 'STE.SPB', 'STEM.SPB', 'STLA.SPB', 'STLD.SPB', 'STM1P2.SPB',
     'STNE.SPB', 'STRA.SPB', 'STT.SPB', 'STWD.SPB', 'STX.SPB', 'STZ.SPB', 'SU.SPB', 'SUPN.SPB', 'SUSA.SPB',
     'SVEC1P1.SPB', 'SWAV.SPB', 'SWBI.SPB', 'SWI.SPB', 'SWK.SPB', 'SWKS.SPB', 'SWN.SPB', 'SWTX.SPB', 'SWX.SPB',
     'SXI.SPB', 'SXT.SPB', 'SYF.SPB', 'SYK.SPB', 'SYNA.SPB', 'SYY.SPB', 'T.SPB', 'TAK.SPB', 'TAL.SPB', 'TAN.SPB',
     'TAP.SPB', 'TASK.SPB', 'TATN.SPB', 'TATNP.SPB', 'TBF.SPB', 'TCBI.SPB', 'TCMD.SPB', 'TCS.SPB', 'TCX.SPB', 'TDC.SPB',
     'TDEU01.SPB', 'TDEU03.SPB', 'TDG.SPB', 'TDOC.SPB', 'TDS.SPB', 'TDY.SPB', 'TEAM.SPB', 'TECH.SPB', 'TECL.SPB',
     'TEL.SPB', 'TENB.SPB', 'TER.SPB', 'TEX.SPB', 'TFC.SPB', 'TFII.SPB', 'TFM01.SPB', 'TFX.SPB', 'TGNA.SPB', 'TGT.SPB',
     'TGTX.SPB', 'THD.SPB', 'THG.SPB', 'THO.SPB', 'THRM.SPB', 'THS.SPB', 'TIP.SPB', 'TJX.SPB', 'TKKclA1.SPB',
     'TKKclA2.SPB', 'TKKclA3.SPB', 'TKKclB.SPB', 'TKO.SPB', 'TKR.SPB', 'TLS.SPB', 'TLT.SPB', 'TM.SPB', 'TMHC.SPB',
     'TMO.SPB', 'TMUS.SPB', 'TNA.SPB', 'TNC.SPB', 'TNDM.SPB', 'TNET.SPB', 'TNL.SPB', 'TOL.SPB', 'TOST.SPB', 'TPG.SPB',
     'TPH.SPB', 'TPIC.SPB', 'TPR.SPB', 'TPX.SPB', 'TQQQ.SPB', 'TREE.SPB', 'TREX.SPB', 'TRGP.SPB', 'TRI.SPB', 'TRIP.SPB',
     'TRMB.SPB', 'TRNFP.SPB', 'TRNO.SPB', 'TROW.SPB', 'TRU.SPB', 'TRUP.SPB', 'TRV.SPB', 'TRY0130.SPB', 'TRY0141.SPB',
     'TRY0225.SPB', 'TRY0228.SPB', 'TRY0234.SPB', 'TRY0327.SPB', 'TRY0330.SPB', 'TRY0336.SPB', 'TRY1028.SPB',
     'TSCO.SPB', 'TSLA.SPB', 'TSM.SPB', 'TSN.SPB', 'TSVT.SPB', 'TT.SPB', 'TTC.SPB', 'TTD.SPB', 'TTE.SPB', 'TTEK.SPB',
     'TTEL0225.SPB', 'TTMI.SPB', 'TTT.SPB', 'TTWO.SPB', 'TUR.SPB', 'TVTX.SPB', 'TW.SPB', 'TWLO.SPB', 'TWOU.SPB',
     'TWST.SPB', 'TXG.SPB', 'TXN.SPB', 'TXRH.SPB', 'TXT.SPB', 'TYL.SPB', 'U.SPB', 'UA.SPB', 'UAA.SPB', 'UAL.SPB',
     'UBER.SPB', 'UBS.SPB', 'UBSI.SPB', 'UBT.SPB', 'UCTT.SPB', 'UDMY.SPB', 'UDOW.SPB', 'UDR.SPB', 'UEC.SPB', 'UFPI.SPB',
     'UGI.SPB', 'UHS.SPB', 'UI.SPB', 'ULTA.SPB', 'UMBF.SPB', 'UNF.SPB', 'UNFI.SPB', 'UNH.SPB', 'UNM.SPB', 'UNP.SPB',
     'UPBD.SPB', 'UPS.SPB', 'UPST.SPB', 'UPWK.SPB', 'URA.SPB', 'URBN.SPB', 'URI.SPB', 'URTY.SPB', 'USB.SPB', 'USFD.SPB',
     'USM.SPB', 'USMV.SPB', 'USNA.SPB', 'USPH.SPB', 'UTHR.SPB', 'UTL.SPB', 'UUUU.SPB', 'V.SPB', 'VAC.SPB',
     'VAKI0324.SPB', 'VAL.SPB', 'VALE.SPB', 'VBR.SPB', 'VC.SPB', 'VCEL.SPB', 'VCIT.SPB', 'VCLT.SPB', 'VCSH.SPB',
     'VCYT.SPB', 'VDE.SPB', 'VEA.SPB', 'VEB2P33.SPB', 'VEEV.SPB', 'VEON.SPB', 'VERU.SPB', 'VERV.SPB', 'VET.SPB',
     'VEU.SPB', 'VFC.SPB', 'VFH.SPB', 'VGK.SPB', 'VGT.SPB', 'VHT.SPB', 'VICR.SPB', 'VIG.SPB', 'VIPS.SPB', 'VIR.SPB',
     'VIRT.SPB', 'VIS.SPB', 'VKCO.SPB', 'VLO.SPB', 'VLTO.SPB', 'VLUE.SPB', 'VMC.SPB', 'VMEO.SPB', 'VMI.SPB',
     'VNA@DE.SPB', 'VNDA.SPB', 'VNO.SPB', 'VNT.SPB', 'VO.SPB', 'VOO.SPB', 'VOT.SPB', 'VOW3@DE.SPB', 'VOYA.SPB',
     'VPG.SPB', 'VPL.SPB', 'VREX.SPB', 'VRNS.SPB', 'VRNT.SPB', 'VRSK.SPB', 'VRSN.SPB', 'VRT.SPB', 'VRTS.SPB',
     'VRTX.SPB', 'VSAT.SPB', 'VSCO.SPB', 'VSS.SPB', 'VST.SPB', 'VSTO.SPB', 'VSTS.SPB', 'VT.SPB', 'VTBR.SPB',
     'VTBperp.SPB', 'VTI.SPB', 'VTNR.SPB', 'VTR.SPB', 'VTRS.SPB', 'VTS.SPB', 'VTSC@DE.SPB', 'VTV.SPB', 'VUG.SPB',
     'VUZI.SPB', 'VV.SPB', 'VVV.SPB', 'VVX.SPB', 'VWO.SPB', 'VXF.SPB', 'VXRT.SPB', 'VXUS.SPB', 'VYM.SPB', 'VYMI.SPB',
     'VYX.SPB', 'VZ.SPB', 'VZIO.SPB', 'W.SPB', 'WAB.SPB', 'WABC.SPB', 'WAFD.SPB', 'WAL.SPB', 'WAT.SPB', 'WB.SPB',
     'WBA.SPB', 'WBD.SPB', 'WBS.SPB', 'WCC.SPB', 'WCLD.SPB', 'WCN.SPB', 'WDAY.SPB', 'WDC.SPB', 'WDFC.SPB', 'WEC.SPB',
     'WELL.SPB', 'WERN.SPB', 'WEX.SPB', 'WFC.SPB', 'WGO.SPB', 'WH.SPB', 'WHD.SPB', 'WHR.SPB', 'WING.SPB', 'WIRE.SPB',
     'WISH.SPB', 'WIX.SPB', 'WK.SPB', 'WKC.SPB', 'WKHS.SPB', 'WLK.SPB', 'WM.SPB', 'WMB.SPB', 'WMG.SPB', 'WMS.SPB',
     'WMT.SPB', 'WOLF.SPB', 'WOR.SPB', 'WPC.SPB', 'WPM.SPB', 'WRB.SPB', 'WRBY.SPB', 'WRK.SPB', 'WRLD.SPB', 'WSC.SPB',
     'WSFS.SPB', 'WSM.SPB', 'WSO.SPB', 'WST.SPB', 'WTFC.SPB', 'WTRG.SPB', 'WTS.SPB', 'WTTR.SPB', 'WTW.SPB', 'WU.SPB',
     'WW.SPB', 'WWD.SPB', 'WWW.SPB', 'WY.SPB', 'WYNN.SPB', 'X.SPB', 'XBI.SPB', 'XEL.SPB', 'XENE.SPB', 'XHB.SPB',
     'XLB.SPB', 'XLC.SPB', 'XLE.SPB', 'XLF.SPB', 'XLG.SPB', 'XLI.SPB', 'XLK.SPB', 'XLP.SPB', 'XLRE.SPB', 'XLU.SPB',
     'XLV.SPB', 'XLY.SPB', 'XME.SPB', 'XNCR.SPB', 'XOM.SPB', 'XOP.SPB', 'XP.SPB', 'XPEL.SPB', 'XPO.SPB', 'XRAY.SPB',
     'XRT.SPB', 'XRX.SPB', 'XS0191754729.SPB', 'XS0559915961.SPB', 'XS0885736925.SPB', 'XS1577953174.SPB', 'XSD.SPB',
     'XYL.SPB', 'YELP.SPB', 'YETI.SPB', 'YEXT.SPB', 'YINN.SPB', 'YNDX@US.SPB', 'YUM.SPB', 'YUMC.SPB', 'YY.SPB', 'Z.SPB',
     'ZBH.SPB', 'ZBRA.SPB', 'ZD.SPB', 'ZG.SPB', 'ZI.SPB', 'ZIM.SPB', 'ZIMV.SPB', 'ZION.SPB', 'ZIP.SPB', 'ZLAB.SPB',
     'ZM.SPB', 'ZNTL.SPB', 'ZS.SPB', 'ZTS.SPB', 'ZUMZ.SPB', 'ZUO.SPB', 'ZWS.SPB', 'ZYXI.SPB']

    # cant_load_tickers:

    cant_load_tickers = []

    for timeframe in timeframes:
        for ticker in tickers:
            try:
                time_of_getting_data = datetime.datetime.now()
                load_data = SharesDataLoader(ticker)
                load_data.connect_to_metatrader5(path=f"C:\Program Files\FINAM MetaTrader 5\terminal64.exe")
                data = load_data.get_share_data(ticker=ticker, timeframe=timeframe, utc_till=utc_till,
                                                how_many_bars=how_many_bars, remove_today_bars=True)
                load_data.export_to_csv_from_df(ticker=ticker, timeframe=timeframe, data=data,
                                                export_dir=os.path.join(current_dir, "csv_export_hkd"),
                                                by_timeframes=True)
                load_data.disconnect_from_metatrader5()
            except:
                cant_load_tickers.append(ticker)

    print("cant_load_tickers:", cant_load_tickers)


if __name__ == '__main__':
    time_of_getting_data = datetime.datetime.now()
    # to prevent hang Metatrader5
    work_thread = functions_thread.Periodic(10, prevent_hang, "prevent_hang", autostart=True)  # поток для периодической обработки функции # it auto-starts, no need of rt.start()
    work_thread2 = functions_thread.RunOnce(get_hkd_shares, "get_hkd_shares", autostart=True)  # поток для однократного запуска функции # it auto-starts, no need of rt.start()

    while work_thread2.is_running(): pass
    work_thread.stop()
