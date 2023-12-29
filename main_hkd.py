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
    current_dir = os.path.dirname(os.path.abspath(__file__))  # текущая директория
    how_many_bars = 99999  # сколько баров закачать - предел...

    utc_till = datetime.datetime.now() + datetime.timedelta(days=1)  # получим данные по завтрашний день
    print(utc_till)

    timeframes = {mt5.TIMEFRAME_M5, mt5.TIMEFRAME_M10, mt5.TIMEFRAME_M15, mt5.TIMEFRAME_M30, mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H4, mt5.TIMEFRAME_D1, mt5.TIMEFRAME_W1, mt5.TIMEFRAME_MN1}
    # timeframes = {mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H4, mt5.TIMEFRAME_D1, mt5.TIMEFRAME_W1, mt5.TIMEFRAME_MN1}
    # timeframes = {mt5.TIMEFRAME_M5, mt5.TIMEFRAME_M10, mt5.TIMEFRAME_M15, mt5.TIMEFRAME_M30}  # 99999 - предел...
    # timeframes = {mt5.TIMEFRAME_D1, }
    tickers = {"MSFT.US", "BAC.US"}
    # tickers = {"ALLFUTRTSI"}  # только через Финам ..

    tickers = ['1', '101', '1024', '1038', '1044', '1055', '1061', '1066', '1072', '1088', '1093', '1099', '1109',
    '1113', '1138', '1171', '1177', '12', '1209', '1211', '1288', '1299', '1336', '1339', '1347', '1359', '1368',
    '1378', '1385', '1398', '1548', '16', '1658', '168', '175', '1766', '1797', '1801', '1810', '1816', '1818', '1876',
    '1877', '1880', '1898', '1919', '1928', '1929', '1988', '1997', '1COV@DE', '2007', '2015', '2020', '2196', '2202',
    '2208', '2238', '2252', '2269', '2313', '2318', '2319', '2328', '2331', '2333', '2359', '2382', '2388', '241',
    '2518', '2600', '2601', '2618', '2628', '267', '268', '2688', '27', '2800', '2822', '2823', '2828', '285', '288',
    '2883', '2899', '291', '3', '3010', '3033', '3067', '3188', '322', '3319', '3328', '3347', '338', '3606', '3690',
    '3692', '3759', '3800', '386', '388', '3888', '3898', '390', '3900', '3908', '3968', '3988', '3993', '489', '5',
    '6', '6030', '6049', '6060', '6078', '6098', '6185', '66', '6618', '669', '6690', '670', '6837', '6862', '6865',
    '6869', '688', '6881', '6886', '6969', '700', '753', '763', '788', '82800', '82822', '82823', '82828', '83010',
    '83188', '836', '857', '868', '881', '914', '916', '939', '956', '960', '9618', '9626', '9633', '968', '9696',
    '9866', '9868', '9888', '992', '9922', '9926', '9961', '9988', '9992', '9995', '9999', 'A', 'AA', 'AAL', 'AAN',
    'AAON', 'AAP', 'AAPL', 'AAXJ', 'ABBV', 'ABCB', 'ABCL', 'ABG', 'ABM', 'ABNB', 'ABR', 'ABT', 'ACAD', 'ACGL', 'ACI',
    'ACIW', 'ACLS', 'ACM', 'ACMR', 'ACN', 'ACWI', 'ACWX', 'ADAP', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADPT', 'ADS@DE', 'ADSK',
    'ADUS', 'AEE', 'AEIS', 'AEM', 'AEO', 'AEP', 'AER', 'AES', 'AFG', 'AFKS', 'AFL', 'AFMD', 'AFRM', 'AFX@DE', 'AG',
    'AGCO', 'AGG', 'AGIO', 'AGNC', 'AGO', 'AI', 'AIG', 'AIN', 'AIR', 'AIRC', 'AIT', 'AIV', 'AIZ', 'AJG', 'AKAM', 'ALB',
    'ALC', 'ALE', 'ALEC', 'ALFA0430', 'ALG', 'ALGM', 'ALGN', 'ALGT', 'ALIT', 'ALK', 'ALL', 'ALLE', 'ALLK', 'ALLO',
    'ALLY', 'ALNY', 'ALRM', 'ALRS', 'ALSN', 'ALT', 'ALTR', 'ALV', 'ALV@DE', 'ALXO', 'AM', 'AMAT', 'AMBA', 'AMCR',
    'AMCX', 'AMD', 'AME', 'AMED', 'AMEH', 'AMG', 'AMGN', 'AMH', 'AMKR', 'AMN', 'AMP', 'AMPH', 'AMR', 'AMSF', 'AMT',
    'AMTI', 'AMWD', 'AMZN', 'AN', 'ANAB', 'ANDE', 'ANET', 'ANF', 'ANGI', 'ANGL', 'ANIK', 'ANIP', 'ANSS', 'AON', 'AORT',
    'AOS', 'AOSL', 'AOUT', 'APA', 'APAM', 'APD', 'APEI', 'APH', 'APLE', 'APLS', 'APLT', 'APO', 'APP', 'APPF', 'APPN',
    'APPS', 'APTV', 'ARCC', 'ARCH', 'ARCT', 'ARE', 'ARI', 'ARKF', 'ARMK', 'ARQT', 'ARRY', 'ARVL', 'ARVN', 'ARW', 'ARWR',
    'ASAN', 'ASGN', 'ASH', 'ASHR', 'ASIX', 'ASO', 'ASTR', 'ASTS', 'ATEN', 'ATEX', 'ATGE', 'ATI', 'ATKR', 'ATNI', 'ATO',
    'ATR', 'ATRA', 'ATRC', 'ATRI', 'ATRO', 'ATRR01', 'ATUS', 'AUPH', 'AVA', 'AVAV', 'AVB', 'AVGO', 'AVIR', 'AVNS',
    'AVNT', 'AVT', 'AVTR', 'AVXL', 'AVY', 'AWH', 'AWI', 'AWK', 'AWR', 'AX', 'AXGN', 'AXNX', 'AXON', 'AXP', 'AXSM',
    'AXTA', 'AYI', 'AYX', 'AZEK', 'AZN', 'AZO', 'AZPN', 'AZTA', 'Atomenpr01', 'BA', 'BABA', 'BAC', 'BAH', 'BALL',
    'BAND', 'BAS@DE', 'BAX', 'BAYN@DE', 'BBIO', 'BBSI', 'BBWI', 'BBY', 'BC', 'BCC', 'BCE', 'BCO', 'BCPC', 'BCRX',
    'BDC', 'BDTX', 'BDX', 'BE', 'BEAM', 'BECN', 'BEL0226', 'BEL0230', 'BEL0231', 'BEL0627', 'BEN', 'BERY', 'BF B',
    'BFAM', 'BFH', 'BGNE', 'BGS', 'BH', 'BHF', 'BIDU', 'BIG', 'BIGC', 'BIIB', 'BIL', 'BILI', 'BILL', 'BIO', 'BJ',
    'BJRI', 'BK', 'BKNG', 'BKR', 'BKU', 'BL', 'BLD', 'BLDP', 'BLDR', 'BLK', 'BLKB', 'BLMN', 'BLNK', 'BLUE', 'BLZE',
    'BMBL', 'BMI', 'BMO', 'BMRN', 'BMW@DE', 'BMY', 'BNGO', 'BNTX', 'BOH', 'BOIL', 'BOKF', 'BOOT', 'BOSS@DE', 'BOTZ',
    'BOX', 'BPMC', 'BR', 'BRBR', 'BRC', 'BRK A', 'BRK B', 'BRKR', 'BRO', 'BROS', 'BRX', 'BSX', 'BSY', 'BTAI', 'BTI',
    'BUD', 'BURL', 'BVB@DE', 'BWA', 'BWXT', 'BX', 'BXMT', 'BXP', 'BYND', 'BYON', 'BYSI', 'BZUN', 'C', 'CABO', 'CACC',
    'CACI', 'CAG', 'CAH', 'CALM', 'CAR', 'CARA', 'CARG', 'CARR', 'CARS', 'CASY', 'CAT', 'CB', 'CBOM', 'CBOM0224EU',
    'CBRE', 'CBRL', 'CBSH', 'CBT', 'CBU', 'CC', 'CCI', 'CCJ', 'CCK', 'CCL', 'CCOI', 'CCS', 'CCSI', 'CDAY', 'CDLX',
    'CDNA', 'CDNS', 'CDW', 'CE', 'CEG', 'CELH', 'CENT', 'CENTA', 'CERE', 'CEVA', 'CF', 'CFG', 'CFLT', 'CFR', 'CG',
    'CGEN', 'CGNT', 'CGNX', 'CHAU', 'CHCO', 'CHD', 'CHDN', 'CHE', 'CHEF', 'CHGG', 'CHH', 'CHKP', 'CHMF', 'CHPT', 'CHRS',
    'CHRW', 'CHTR', 'CHWY', 'CHX', 'CI', 'CIAN@US', 'CIBR', 'CIEN', 'CINF', 'CL', 'CLB', 'CLBK', 'CLDT', 'CLF', 'CLH',
    'CLOV', 'CLSK', 'CLVT', 'CLX', 'CM', 'CMA', 'CMC', 'CMCO', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMP', 'CMS', 'CNC',
    'CNHI', 'CNI', 'CNK', 'CNMD', 'CNNE', 'CNO', 'CNP', 'CNQ', 'CNS', 'CNX', 'CNXC', 'CNXN', 'CNYA', 'COF', 'COFS',
    'COHR', 'COHU', 'COIN', 'COKE', 'COLB', 'COLD', 'COLM', 'CON@DE', 'COO', 'COOP', 'COP', 'COPX', 'COR', 'CORR',
    'CORT', 'COST', 'COTY', 'COUR', 'CP', 'CPB', 'CPNG', 'CPRI', 'CPRT', 'CPS', 'CPT', 'CQQQ', 'CR', 'CRI', 'CRL',
    'CRM', 'CRMT', 'CRNC', 'CROX', 'CRS', 'CRSP', 'CRSR', 'CRUS', 'CRVL', 'CRWD', 'CSCO', 'CSGP', 'CSGS', 'CSIQ', 'CSL',
    'CSWI', 'CSX', 'CTAS', 'CTLT', 'CTRA', 'CTSH', 'CTVA', 'CUBE', 'CUZ', 'CVCO', 'CVGW', 'CVLT', 'CVM', 'CVNA', 'CVS',
    'CVX', 'CW', 'CWB', 'CWEN', 'CWH', 'CWST', 'CWT', 'CXT', 'CXW', 'CYBR', 'CYRX', 'CYTK', 'CZR', 'D', 'DAL', 'DAN',
    'DAR', 'DASH', 'DAVA', 'DAWN', 'DB1@DE', 'DBK@DE', 'DBX', 'DCI', 'DCPH', 'DD', 'DDD', 'DDOG', 'DDS', 'DE', 'DECK',
    'DEI', 'DELL', 'DFS', 'DG', 'DGRO', 'DGX', 'DHER@DE', 'DHI', 'DHL@DE', 'DHR', 'DIA', 'DINO', 'DIOD', 'DIRP01',
    'DIRP02', 'DIRP03', 'DIS', 'DISH', 'DK', 'DKNG', 'DKS', 'DLB', 'DLO', 'DLR', 'DLTH', 'DLTR', 'DLX', 'DM', 'DMNN01',
    'DMTK', 'DNA', 'DNB', 'DNLI', 'DNMR', 'DNOW', 'DOCN', 'DOCS', 'DOCU', 'DORM', 'DOV', 'DOW', 'DPZ', 'DRI', 'DRIV',
    'DRQ', 'DSKY', 'DT', 'DTE@DE', 'DUK', 'DUOL', 'DUST', 'DV', 'DVA', 'DVN', 'DVY', 'DXC', 'DXCM', 'DXJ', 'DY', 'EA',
    'EAF', 'EAR', 'EAT', 'EBAY', 'EBS', 'ECH', 'ECL', 'ECPG', 'ED', 'EDIT', 'EEFT', 'EEM', 'EFA', 'EFG', 'EFV', 'EFX',
    'EG', 'EGHT', 'EGP', 'EGPT0329', 'EGPT0431', 'EGRX', 'EHTH', 'EIDO', 'EIS', 'EIX', 'EL', 'ELAN', 'ELFV', 'ELS',
    'ELV', 'EMB', 'EMBC', 'EME', 'EMN', 'EMR', 'ENB', 'ENOV', 'ENPH', 'ENR', 'ENS', 'ENSG', 'ENTA', 'ENTG', 'ENV',
    'ENVX', 'EOAN@DE', 'EOG', 'EPAM', 'EPC', 'EPI', 'EPP', 'EQH', 'EQIX', 'EQR', 'EQT', 'ERIE', 'ES', 'ESAB', 'ESE',
    'ESGD', 'ESGE', 'ESGR', 'ESGU', 'ESGV', 'ESPR', 'ESS', 'ESTC', 'ET', 'ETD', 'ETLN@GS', 'ETN', 'ETR', 'ETRN', 'ETSY',
    'EUFN', 'EVBG', 'EVER', 'EVH', 'EVK@DE', 'EVR', 'EVRG', 'EVT@DE', 'EW', 'EWA', 'EWBC', 'EWC', 'EWD', 'EWG', 'EWH',
    'EWI', 'EWJ', 'EWL', 'EWM', 'EWN', 'EWP', 'EWQ', 'EWS', 'EWT', 'EWU', 'EWW', 'EWY', 'EWZ', 'EXAS', 'EXC', 'EXEL',
    'EXLS', 'EXP', 'EXPD', 'EXPE', 'EXPI', 'EXPO', 'EXR', 'EYE', 'EZA', 'EZU', 'F', 'FAF', 'FANG', 'FARO', 'FAS',
    'FAST', 'FATE', 'FAZ', 'FBIN', 'FCEL', 'FCFS', 'FCN', 'FCNCA', 'FCX', 'FDS', 'FDX', 'FE', 'FEES', 'FELE', 'FEZ',
    'FFIN', 'FFIV', 'FG', 'FGEN', 'FHI', 'FI', 'FICO', 'FIGS', 'FIPO', 'FIS', 'FITB', 'FIVE', 'FIVE@GS', 'FIVN',
    'FIXP@GS', 'FIZZ', 'FL', 'FLGT', 'FLO', 'FLR', 'FLS', 'FLT', 'FLWS', 'FLYW', 'FMC', 'FME@DE', 'FND', 'FNF', 'FNKO',
    'FNV', 'FOLD', 'FORM', 'FORR', 'FOUR', 'FOX', 'FOXA', 'FOXF', 'FR', 'FRE@DE', 'FRHC', 'FRME', 'FROG', 'FRPH',
    'FRPT', 'FRT', 'FSLR', 'FSLY', 'FSR', 'FTCH', 'FTCI', 'FTDR', 'FTI', 'FTNT', 'FTRE', 'FTV', 'FUL', 'FULC', 'FVRR',
    'FWRD', 'FXI', 'G', 'GATX', 'GAZP', 'GAZP0327', 'GAZP0837', 'GAZP1124', 'GBCI', 'GBX', 'GCHE', 'GCO', 'GD', 'GDDY',
    'GDEV', 'GDOT', 'GDRX', 'GDX', 'GDXJ', 'GE', 'GEF', 'GEHC', 'GEN', 'GES', 'GEVO', 'GGG', 'GH', 'GHC', 'GILD', 'GIS',
    'GKOS', 'GL', 'GLBE', 'GLD', 'GLGR02', 'GLOB', 'GLPI', 'GLTR', 'GLTR@GS', 'GLW', 'GM', 'GMED', 'GMKN', 'GMS', 'GNL',
    'GNRC', 'GNTX', 'GO', 'GOGL', 'GOLD', 'GOOG', 'GOOGL', 'GOSS', 'GPC', 'GPI', 'GPK', 'GPN', 'GPRO', 'GPS', 'GRBK',
    'GRMN', 'GROWS', 'GRPH', 'GS', 'GSHD', 'GSLC', 'GT', 'GTHX', 'GTLB', 'GTLS', 'GTN', 'GTX', 'GVA', 'GWRE', 'GWW',
    'GXC', 'GXO', 'H', 'HA', 'HAE', 'HAIN', 'HAL', 'HALO', 'HAS', 'HASI', 'HBAN', 'HBI', 'HCA', 'HCAT', 'HCC', 'HCSG',
    'HD', 'HDV', 'HE', 'HEAR', 'HEI', 'HEI@DE', 'HEN3@DE', 'HES', 'HGV', 'HHH', 'HHR', 'HI', 'HIBB', 'HIG', 'HII',
    'HIMS', 'HIW', 'HLF', 'HLI', 'HLNE', 'HLT', 'HOG', 'HOLX', 'HON', 'HOOD', 'HOT@DE', 'HP', 'HPE', 'HPQ', 'HQY', 'HR',
    'HRB', 'HRL', 'HRMY', 'HRTX', 'HSIC', 'HST', 'HSY', 'HTHT', 'HUBB', 'HUBG', 'HUBS', 'HUM', 'HUN', 'HURN', 'HWM',
    'HXL', 'HYDR', 'HYG', 'HYLN', 'HZO', 'IAC', 'IART', 'IAU', 'IBB', 'IBKR', 'IBM', 'IBN', 'IBP', 'IBTX', 'ICE',
    'ICFI', 'ICLN', 'ICLR', 'ICUI', 'IDA', 'IDCC', 'IDXX', 'IEF', 'IEFA', 'IEMG', 'IEV', 'IEX', 'IFF', 'IFX@DE', 'IGMS',
    'IGOV', 'IGSB', 'IGV', 'IHI', 'IIPR', 'IJH', 'IJJ', 'IJK', 'IJR', 'ILF', 'ILMN', 'INCY', 'INDA', 'INDB', 'INGN',
    'INGR', 'INMD', 'INO', 'INSG', 'INSM', 'INSP', 'INTC', 'INTU', 'INVA', 'INVH', 'IONS', 'IOSP', 'IOVA', 'IP', 'IPAR',
    'IPG', 'IPGP', 'IQLT', 'IQV', 'IR', 'IRAO', 'IRBT', 'IRDM', 'IRM', 'IRTC', 'IRWD', 'ISBNK0424', 'ISRG', 'IT', 'ITA',
    'ITB', 'ITCI', 'ITGR', 'ITOT', 'ITRI', 'ITT', 'ITW', 'IUSG', 'IUSV', 'IVE', 'IVV', 'IVW', 'IVZ', 'IWB', 'IWD',
    'IWF', 'IWM', 'IWN', 'IWO', 'IWP', 'IWR', 'IWS', 'IWV', 'IXC', 'IXG', 'IXN', 'IXUS', 'IYE', 'IYF', 'IYR', 'IYT',
    'IYW', 'J', 'JACK', 'JAMF', 'JBHT', 'JBL', 'JBSS', 'JBT', 'JCI', 'JD', 'JEF', 'JELD', 'JHG', 'JJSF', 'JKHY', 'JLL',
    'JNJ', 'JNK', 'JNPR', 'JNUG', 'JOBY', 'JOUT', 'JPM', 'JWN', 'K', 'KAI', 'KALU', 'KAP@GS', 'KBE', 'KBH', 'KBWB',
    'KD', 'KDP', 'KEP', 'KEX', 'KEY', 'KEYS', 'KFY', 'KGC', 'KHC', 'KIDS', 'KIE', 'KIM', 'KKR', 'KLAC', 'KLG', 'KLIC',
    'KMB', 'KMI', 'KMPR', 'KMT', 'KMX', 'KNF', 'KNSL', 'KNX', 'KO', 'KOD', 'KOPN', 'KR', 'KRC', 'KRG', 'KRTX', 'KRYS',
    'KSPI@GS', 'KSS', 'KTB', 'KTOS', 'KWEB', 'KWR', 'KYMR', 'L', 'LAAC', 'LAC', 'LAD', 'LANC', 'LASR', 'LAZR', 'LBRDK',
    'LC', 'LCID', 'LCII', 'LDOS', 'LEA', 'LECO', 'LEG', 'LEGH', 'LEN', 'LEVI', 'LFST', 'LFUS', 'LGIH', 'LGND', 'LH',
    'LHA@DE', 'LHX', 'LI', 'LICY', 'LII', 'LIN', 'LIT', 'LITE', 'LKOH', 'LKQ', 'LLY', 'LMT', 'LNC', 'LNG', 'LNN', 'LNT',
    'LNTH', 'LOGI', 'LOPE', 'LOW', 'LPL', 'LPLA', 'LPRO', 'LPSN', 'LPX', 'LQD', 'LRCX', 'LRN', 'LSCC', 'LSPD', 'LSRG',
    'LSTR', 'LTHM', 'LUK1126', 'LULU', 'LUMN', 'LUV', 'LVS', 'LW', 'LYB', 'LYEL', 'LYFT', 'LYV', 'M', 'MA', 'MAA',
    'MAC', 'MAGN', 'MAN', 'MANH', 'MANU', 'MAR', 'MARA', 'MAS', 'MASI', 'MAT', 'MATV', 'MATX', 'MBC', 'MBG@DE', 'MBUU',
    'MC', 'MCD', 'MCHI', 'MCHP', 'MCK', 'MCO', 'MCRI', 'MD', 'MDB', 'MDC', 'MDGL', 'MDLZ', 'MDRX', 'MDT', 'MDU', 'MDY',
    'MED', 'MEDP', 'MEI', 'MELI', 'MET', 'META', 'METC', 'METCB', 'MGA', 'MGK', 'MGM', 'MGNT', 'MGPI', 'MGRC', 'MGY',
    'MHK', 'MHO', 'MIDD', 'MKC', 'MKL', 'MKSI', 'MKTX', 'MLAB', 'MLCO', 'MLKN', 'MLM', 'MLNK', 'MMC', 'MMI', 'MMM',
    'MMS', 'MMSI', 'MNDY', 'MNRO', 'MNST', 'MO', 'MOAT', 'MODG', 'MODV', 'MOH', 'MOMO', 'MORN', 'MOS', 'MOV', 'MP',
    'MPC', 'MPW', 'MPWR', 'MQ', 'MRC', 'MRK', 'MRK@DE', 'MRNA', 'MRO', 'MRTX', 'MRVI', 'MRVL', 'MS', 'MSA', 'MSCI',
    'MSEX', 'MSFT', 'MSGE', 'MSGS', 'MSI', 'MSM', 'MSNG', 'MSTR', 'MTB', 'MTCH', 'MTD', 'MTG', 'MTH', 'MTKB', 'MTN',
    'MTRN', 'MTS18soc', 'MTSS', 'MTTR', 'MTUM', 'MTX', 'MTX@DE', 'MU', 'MUR', 'MUSA', 'MUV2@DE', 'MVIS', 'MXL', 'MYGN',
    'MYRG', 'NABL', 'NAIL', 'NARI', 'NATL', 'NAVI', 'NBIX', 'NCNO', 'NDAQ', 'NDSN', 'NEE', 'NEM', 'NEO', 'NEOG', 'NET',
    'NEU', 'NFE', 'NFG', 'NFLX', 'NGVT', 'NHI', 'NI', 'NIC', 'NICE', 'NJR', 'NKE', 'NKLA', 'NKTR', 'NLMK', 'NLY',
    'NMIH', 'NMTP', 'NOC', 'NOK', 'NOV', 'NOVA', 'NOW', 'NPK', 'NRG', 'NRIX', 'NSC', 'NSIT', 'NSP', 'NSSC', 'NTAP',
    'NTCO', 'NTCT', 'NTES', 'NTGR', 'NTLA', 'NTNX', 'NTR', 'NTRA', 'NTRS', 'NU', 'NUE', 'NUGT', 'NUS', 'NVAX', 'NVCR',
    'NVDA', 'NVEE', 'NVR', 'NVRI', 'NVRO', 'NVS', 'NVST', 'NVTA', 'NVTK', 'NWE', 'NWL', 'NWLI', 'NWS', 'NWSA', 'NXPI',
    'NXST', 'NYCB', 'NYT', 'O', 'OABI', 'OC', 'ODFL', 'OEF', 'OFIX', 'OGE', 'OGN', 'OGS', 'OHI', 'OI', 'OIH', 'OII',
    'OIS', 'OKE', 'OKTA', 'OLED', 'OLLI', 'OLN', 'OMA0128', 'OMA0148', 'OMC', 'OMCL', 'OMF', 'ON', 'ONL', 'ONTO', 'ORA',
    'ORCL', 'ORG1P1', 'ORI', 'ORLY', 'ORMP', 'OSIS', 'OSK', 'OSUR', 'OTIS', 'OUST', 'OVV', 'OXY', 'OZON@US', 'PAAS',
    'PACB', 'PAG', 'PAGS', 'PALL', 'PANW', 'PAR', 'PARA', 'PATH', 'PATK', 'PAY', 'PAYC', 'PAYO', 'PAYX', 'PB', 'PBA',
    'PBF', 'PBH', 'PBI', 'PBW', 'PCAR', 'PCG', 'PCH', 'PCOR', 'PCRX', 'PCTY', 'PCVX', 'PD', 'PDBC', 'PDCO', 'PDS',
    'PEAK', 'PEG', 'PEGA', 'PEN', 'PENN', 'PEP', 'PETQ', 'PFE', 'PFG', 'PFGC', 'PFSI', 'PG', 'PGNY', 'PGR', 'PGTI',
    'PH', 'PHIN', 'PHM', 'PHO', 'PHOR', 'PI', 'PICK', 'PII', 'PIKK', 'PINC', 'PINS', 'PIPR', 'PJT', 'PKG', 'PKW',
    'PLAY', 'PLCE', 'PLD', 'PLL', 'PLNT', 'PLTK', 'PLTR', 'PLUG', 'PLUS', 'PLXS', 'PLZL', 'PM', 'PMT', 'PNC', 'PNFP',
    'PNTG', 'PNW', 'PODD', 'POOL', 'POR', 'POST', 'POWI', 'PPC', 'PPG', 'PPL', 'PPLT', 'PRAA', 'PRFT', 'PRG', 'PRGS',
    'PRI', 'PRLB', 'PRO', 'PRTA', 'PRTS', 'PRU', 'PSA', 'PSEC', 'PSMT', 'PSN', 'PSTG', 'PSX', 'PTC', 'PTCT', 'PTON',
    'PUBM', 'PUM@DE', 'PUMP', 'PVH', 'PWR', 'PXD', 'PYPL', 'PZZA', 'QCOM', 'QDEL', 'QGEN', 'QLD', 'QLYS', 'QNCX',
    'QNST', 'QQQ', 'QRTEA', 'QRVO', 'QS', 'QTWO', 'QUAL', 'QYLD', 'R', 'RACE', 'RAGR', 'RAMP', 'RARE', 'RBA', 'RBC',
    'RBLX', 'RCL', 'RCUS', 'RDFN', 'RDN', 'RDY', 'REG', 'REGN', 'RELY', 'REMX', 'REX', 'REYN', 'REZI', 'RF', 'RGA',
    'RGEN', 'RGLD', 'RGNX', 'RGR', 'RH', 'RHI', 'RHM@DE', 'RIG', 'RIO', 'RIOT', 'RITM', 'RIVN', 'RJF', 'RKLB', 'RKT',
    'RL', 'RLAY', 'RMD', 'RNG', 'RNR', 'ROCK', 'ROG', 'ROK', 'ROKU', 'ROL', 'ROP', 'ROST', 'RPD', 'RPM', 'RPV', 'RRBI',
    'RRC', 'RRGB', 'RRR', 'RRX', 'RS', 'RSG', 'RSKD', 'RSP', 'RTKM', 'RTO', 'RTX', 'RU000A0JXTY7', 'RU000A1008J4',
    'RU000A100FE5', 'RU000A100N12', 'RU000A100P85', 'RU000A103FP5', 'RUN', 'RUS0628', 'RVLV', 'RVMD', 'RVNC', 'RVTY',
    'RWE@DE', 'RXO', 'RXRX', 'RY', 'RYN', 'RYTM', 'RZD0527', 'S', 'SAGE', 'SAH', 'SAIA', 'SAIC', 'SAM', 'SAP', 'SAP@DE',
    'SATS', 'SAVA', 'SAVE', 'SBAC', 'SBCF', 'SBER', 'SBERP', 'SBGI', 'SBH', 'SBRA', 'SBUX', 'SCCO', 'SCHA', 'SCHB',
    'SCHD', 'SCHE', 'SCHF', 'SCHG', 'SCHW', 'SCHX', 'SCI', 'SCJ', 'SCL', 'SCSC', 'SCZ', 'SDGR', 'SDS', 'SDY', 'SEDG',
    'SEE', 'SEGE2P1R', 'SEGE2P3R', 'SEIC', 'SF', 'SFIX', 'SFM', 'SGENperp', 'SGMO', 'SH', 'SHAK', 'SHEL', 'SHEN',
    'SHL@DE', 'SHLS', 'SHOO', 'SHOP', 'SHW', 'SIBN', 'SIE@DE', 'SIG', 'SIGA', 'SIGI', 'SILK', 'SIRI', 'SITE', 'SITM',
    'SJM', 'SJW', 'SKIN', 'SKLZ', 'SKM', 'SKT', 'SKX', 'SKY', 'SLAB', 'SLB', 'SLDB', 'SLG', 'SLGN', 'SLM', 'SLP',
    'SLQT', 'SLV', 'SLVM', 'SMAR', 'SMG', 'SMH', 'SMPL', 'SMTC', 'SNA', 'SNAP', 'SNBR', 'SNGS', 'SNGSP', 'SNOW', 'SNPS',
    'SNX', 'SNY', 'SO', 'SOFI', 'SOFL', 'SOHU', 'SON', 'SONO', 'SONY', 'SOXL', 'SOXS', 'SOXX', 'SP', 'SPB@US', 'SPBE',
    'SPCE', 'SPDW', 'SPEM', 'SPG', 'SPGI', 'SPHQ', 'SPHR', 'SPLG', 'SPLK', 'SPLV', 'SPNS', 'SPOT', 'SPR', 'SPSB',
    'SPSC', 'SPT', 'SPXL', 'SPXS', 'SPXU', 'SPY', 'SPYD', 'SQ', 'SQQQ', 'SQSP', 'SR', 'SRC', 'SRCL', 'SRDX', 'SRE',
    'SRI', 'SRPT', 'SSB', 'SSD', 'SSNC', 'SSTK', 'STAA', 'STAG', 'STE', 'STEM', 'STLA', 'STLD', 'STM1P2', 'STNE',
    'STRA', 'STT', 'STWD', 'STX', 'STZ', 'SU', 'SUPN', 'SUSA', 'SVEC1P1', 'SWAV', 'SWBI', 'SWI', 'SWK', 'SWKS', 'SWN',
    'SWTX', 'SWX', 'SXI', 'SXT', 'SYF', 'SYK', 'SYNA', 'SYY', 'T', 'TAK', 'TAL', 'TAN', 'TAP', 'TASK', 'TATN', 'TATNP',
    'TBF', 'TCBI', 'TCMD', 'TCS', 'TCX', 'TDC', 'TDEU01', 'TDEU03', 'TDG', 'TDOC', 'TDS', 'TDY', 'TEAM', 'TECH', 'TECL',
    'TEL', 'TENB', 'TER', 'TEX', 'TFC', 'TFII', 'TFM01', 'TFX', 'TGNA', 'TGT', 'TGTX', 'THD', 'THG', 'THO', 'THRM',
    'THS', 'TIP', 'TJX', 'TKKclA1', 'TKKclA2', 'TKKclA3', 'TKKclB', 'TKO', 'TKR', 'TLS', 'TLT', 'TM', 'TMHC', 'TMO',
    'TMUS', 'TNA', 'TNC', 'TNDM', 'TNET', 'TNL', 'TOL', 'TOST', 'TPG', 'TPH', 'TPIC', 'TPR', 'TPX', 'TQQQ', 'TREE',
    'TREX', 'TRGP', 'TRI', 'TRIP', 'TRMB', 'TRNFP', 'TRNO', 'TROW', 'TRU', 'TRUP', 'TRV', 'TRY0130', 'TRY0141',
    'TRY0225', 'TRY0228', 'TRY0234', 'TRY0327', 'TRY0330', 'TRY0336', 'TRY1028', 'TSCO', 'TSLA', 'TSM', 'TSN', 'TSVT',
    'TT', 'TTC', 'TTD', 'TTE', 'TTEK', 'TTEL0225', 'TTMI', 'TTT', 'TTWO', 'TUR', 'TVTX', 'TW', 'TWLO', 'TWOU', 'TWST',
    'TXG', 'TXN', 'TXRH', 'TXT', 'TYL', 'U', 'UA', 'UAA', 'UAL', 'UBER', 'UBS', 'UBSI', 'UBT', 'UCTT', 'UDMY', 'UDOW',
    'UDR', 'UEC', 'UFPI', 'UGI', 'UHS', 'UI', 'ULTA', 'UMBF', 'UNF', 'UNFI', 'UNH', 'UNM', 'UNP', 'UPBD', 'UPS', 'UPST',
    'UPWK', 'URA', 'URBN', 'URI', 'URTY', 'USB', 'USFD', 'USM', 'USMV', 'USNA', 'USPH', 'UTHR', 'UTL', 'UUUU', 'V',
    'VAC', 'VAKI0324', 'VAL', 'VALE', 'VBR', 'VC', 'VCEL', 'VCIT', 'VCLT', 'VCSH', 'VCYT', 'VDE', 'VEA', 'VEB2P33',
    'VEEV', 'VEON', 'VERU', 'VERV', 'VET', 'VEU', 'VFC', 'VFH', 'VGK', 'VGT', 'VHT', 'VICR', 'VIG', 'VIPS', 'VIR',
    'VIRT', 'VIS', 'VKCO', 'VLO', 'VLTO', 'VLUE', 'VMC', 'VMEO', 'VMI', 'VNA@DE', 'VNDA', 'VNO', 'VNT', 'VO', 'VOO',
    'VOT', 'VOW3@DE', 'VOYA', 'VPG', 'VPL', 'VREX', 'VRNS', 'VRNT', 'VRSK', 'VRSN', 'VRT', 'VRTS', 'VRTX', 'VSAT',
    'VSCO', 'VSS', 'VST', 'VSTO', 'VSTS', 'VT', 'VTBR', 'VTBperp', 'VTI', 'VTNR', 'VTR', 'VTRS', 'VTS', 'VTSC@DE',
    'VTV', 'VUG', 'VUZI', 'VV', 'VVV', 'VVX', 'VWO', 'VXF', 'VXRT', 'VXUS', 'VYM', 'VYMI', 'VYX', 'VZ', 'VZIO', 'W',
    'WAB', 'WABC', 'WAFD', 'WAL', 'WAT', 'WB', 'WBA', 'WBD', 'WBS', 'WCC', 'WCLD', 'WCN', 'WDAY', 'WDC', 'WDFC', 'WEC',
    'WELL', 'WERN', 'WEX', 'WFC', 'WGO', 'WH', 'WHD', 'WHR', 'WING', 'WIRE', 'WISH', 'WIX', 'WK', 'WKC', 'WKHS', 'WLK',
    'WM', 'WMB', 'WMG', 'WMS', 'WMT', 'WOLF', 'WOR', 'WPC', 'WPM', 'WRB', 'WRBY', 'WRK', 'WRLD', 'WSC', 'WSFS', 'WSM',
    'WSO', 'WST', 'WTFC', 'WTRG', 'WTS', 'WTTR', 'WTW', 'WU', 'WW', 'WWD', 'WWW', 'WY', 'WYNN', 'X', 'XBI', 'XEL',
    'XENE', 'XHB', 'XLB', 'XLC', 'XLE', 'XLF', 'XLG', 'XLI', 'XLK', 'XLP', 'XLRE', 'XLU', 'XLV', 'XLY', 'XME', 'XNCR',
    'XOM', 'XOP', 'XP', 'XPEL', 'XPO', 'XRAY', 'XRT', 'XRX', 'XS0191754729', 'XS0559915961', 'XS0885736925',
    'XS1577953174', 'XSD', 'XYL', 'YELP', 'YETI', 'YEXT', 'YINN', 'YNDX@US', 'YUM', 'YUMC', 'YY', 'Z', 'ZBH', 'ZBRA',
    'ZD', 'ZG', 'ZI', 'ZIM', 'ZIMV', 'ZION', 'ZIP', 'ZLAB', 'ZM', 'ZNTL', 'ZS', 'ZTS', 'ZUMZ', 'ZUO', 'ZWS', 'ZYXI']


    # cant_load_tickers:

    cant_load_tickers = []

    for timeframe in timeframes:
        for ticket in tickers:
            try:
                load_data = SharesDataLoader(ticket)
                load_data.connect_to_metatrader5(path=f"C:\Program Files\FINAM MetaTrader 5\terminal64.exe")
                data = load_data.get_share_data(ticket=ticket, timeframe=timeframe, utc_till=utc_till, how_many_bars=how_many_bars, remove_today_bars=True)
                load_data.export_to_csv_from_df(ticket=ticket, timeframe=timeframe, data=data, export_dir=os.path.join(current_dir, "csv_export_hkd"), by_timeframes=True)
                load_data.disconnect_from_metatrader5()
            except:
                cant_load_tickers.append(ticket)

    print("cant_load_tickers:", cant_load_tickers)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()