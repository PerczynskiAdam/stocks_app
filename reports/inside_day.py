from tvDatafeed import TvDatafeed, Interval
import logging
import pandas as pd
import numpy as np


def insideDayReport(txt_file, interval, exp_file_path):
    with open(txt_file, 'r') as f:
        text = f.read()

    # creating a list from string
    list_of_stocks = text.split(',')

    logging.basicConfig(level=logging.DEBUG)
    # login to TradingView acc
    tv = TvDatafeed(auto_login=False)

    df_dict = {}

    for stock in list_of_stocks:
        # import last two daily bars for each stock 
        data = tv.get_hist(stock.split(":")[1], stock.split(":")[0], interval=interval, n_bars=2)

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

# txt_file = r'C:\Users\aperczyn\Downloads\Purple list.txt'
txt_file = r'C:\Users\aperczyn\Downloads\GPW.txt'

# exp_file_path = r'C:\Users\aperczyn\Desktop\Python\stocks_app\files\Raporty\insideDayUS.xlsx'
# exp_file_path = r'C:\Users\aperczyn\Desktop\Python\stocks_app\files\Raporty\insideWeekUS.xlsx'
exp_file_path = r'C:\Users\aperczyn\Desktop\Python\stocks_app\files\Raporty\insideDayGPW.xlsx'
# exp_file_path = r'C:\Users\aperczyn\Desktop\Python\stocks_app\files\Raporty\insideWeekGPW.xlsx'

interval = Interval.in_daily
# interval = Interval.in_weekly

insideDayReport(txt_file, interval, exp_file_path)