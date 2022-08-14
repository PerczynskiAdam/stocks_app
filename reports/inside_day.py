from tvDatafeed import Interval
from tvDatafeed import TvDatafeed
import pandas as pd
import numpy as np
from os import environ
import logging

# utwórz decorator factory, umożliwiający różne typy logowania do tv
logging.basicConfig(level=logging.DEBUG)
tv = TvDatafeed(
    auto_login=False
)

tv = TvDatafeed(
    username=environ.get('tv_user'),
    password=environ.get('tv_password'),
    chromedriver_path=None
)

def dec_tv_login(fn):
    from tvDatafeed import TvDatafeed
    from functools import wraps
    import logging
    @wraps(fn)
    def inner(*args, **kwargs):
        logging.basicConfig(level=logging.DEBUG)
        # login to TradingView acc
        tv = TvDatafeed(
            username=environ.get('tv_user'),
            password=environ.get('tv_password'),
            chromedriver_path=environ.get('chromedriver')
        )
        return fn(*args, tv=tv, **kwargs)
    
    return inner

@dec_tv_login
def insideDayReport(tv, path, interval, exp_file_path):
    data = pd.read_csv(path)

    data['ticker_exchange'] = data['Ticker'] + ":" + data['Exchange']

    # creating a list from string
    list_of_stocks = data['ticker_exchange'].unique()

    df_dict = {}

    for stock in list_of_stocks:
        # import last two daily bars for each stock 
        data = tv.get_hist(stock.split(":")[1], stock.split(":")[0], interval=interval, n_bars=2)
        print(data)

        # high previous day higher then current and low previous day lower then current
        inside_day = data.iloc[0]['high'] > data.iloc[1]['high'] and data.iloc[0]['low'] < data.iloc[1]['low']

        # high previous day higher then current high
        # close previous lower then current low and green day
        # or
        # open previous lower than current low and red day
        wick = data.iloc[0]['high'] > data.iloc[1]['high'] and (
            (data.iloc[0]['close'] < data.iloc[1]['low'] and data.iloc[0]['close'] > data.iloc[0]['open']) or
            (data.iloc[0]['open'] < data.iloc[1]['low'] and data.iloc[0]['close'] < data.iloc[0]['open'])
        )
        df_dict[stock] = [inside_day, wick]

    df = pd.DataFrame.from_dict(df_dict, orient='index', columns=['Inside day', 'Wick play'])

    # Replacing False as np.nan to easily drop rows that meet any conditions
    df.replace({True: 'Tak', False: np.nan}, inplace=True)
    df.dropna(subset=['Inside day', 'Wick play'], how='all', inplace=True)
    df = df.sort_values(by=['Inside day', 'Wick play'], ascending=[False, False])

    # export to excel
    # in app i want to create a db table
    df.to_excel(exp_file_path)

vars_dict = {
    # 'gpw_weekly': {
    #     'txt_file': r'C:\Users\aperczyn\Downloads\GPW.txt',
    #     'interval': Interval.in_weekly,
    #     'exp_file_path': r'C:\Users\aperczyn\Desktop\Python\stocks_app\files\Raporty\insideWeekGPW.xlsx'
    # },
    # 'gpw_daily':{
    #     'txt_file': r'C:\Users\aperczyn\Downloads\GPW.txt',
    #     'interval': Interval.in_daily,
    #     'exp_file_path': r'C:\Users\aperczyn\Desktop\Python\stocks_app\files\Raporty\insideDayGPW.xlsx'
    # },
    'usa_weekly': {
        'path': r'C:\Users\aperczyn\Desktop\Python\trading_view\source_data\industries_playable.csv',
        'interval': Interval.in_weekly,
        'exp_file_path': r'C:\Users\aperczyn\Desktop\Python\stocks_app\files\Raporty\insideWeekUS.xlsx'
    },
    'usa_daily':{
        'path': r'C:\Users\aperczyn\Desktop\Python\trading_view\source_data\industries_playable.csv',
        'interval': Interval.in_daily,
        'exp_file_path': r'C:\Users\aperczyn\Desktop\Python\stocks_app\files\Raporty\insideDayUS.xlsx'
    }
}

insideDayReport(**vars_dict['usa_weekly'])


