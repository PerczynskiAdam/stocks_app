from tvDatafeed import TvDatafeed, Interval
from apscheduler.schedulers.background import BackgroundScheduler
import datetime as dt
import pandas as pd


def volume_check(p_username, p_password, p_symbol_dict, p_interval, p_no_of_days_to_calc_avg_vol,
                 p_start_market, p_end_market, p_volume_threshold):
    INTERVAL_DICT = {
        Interval.in_1_minute: 1,
        Interval.in_3_minute: 3,
        Interval.in_5_minute: 5
        # Interval.in_15_minute
        # Interval.in_30_minute
        # Interval.in_45_minute
        # Interval.in_1_hour
        # Interval.in_2_hour
        # Interval.in_3_hour
        # Interval.in_4_hour
        # Interval.in_daily
        # Interval.in_weekly
        # Interval.in_monthly
    }

    MARKET_DICT = {
        # EXCHANGE: market_due_time
        'GPW': 480,
        'NYSE': 450,
        'NASDAQ': 450,
        'BITSTAMP': 1440
    }

    table_dict = {}
    time_list = []
    ticker_list = []
    vol_list = []
    vol_avg_list = []
    rvol_list = []

    for ticker, exchange in p_symbol_dict.items():
        try:
            # print(ticker, exchange)
            market_time = MARKET_DICT[exchange] # minutes
            # count of bars for each day
            no_of_bar_each_day = int(market_time/INTERVAL_DICT[p_interval])

            # login
            tv = TvDatafeed(p_username, p_password)

            # calculate n_bars to load
            n_bars = int(no_of_bar_each_day * p_no_of_days_to_calc_avg_vol)

            # import data
            data = tv.get_hist(ticker, exchange, interval=p_interval, n_bars=n_bars)

            # datetime index as column
            data.reset_index(inplace=True)

            # trimming dataframe
            data = data[['datetime', 'symbol', 'volume']]

            # splitting datetime for date and time columns
            data['date'] = data.loc[:, 'datetime'].dt.date
            data['time'] = data.loc[:, 'datetime'].dt.time

            # trimming dataframe
            data = data[['date', 'time', 'volume']]

            # set type for time
            data['time'] = data['time'].astype('str')

            # filtering data depending on market start/end
            data = data.loc[(data['time'] >= p_start_market) & (data['time'] <= p_end_market)]

            # sorting dataframe
            data = data.sort_values(by=['date', 'time'], ascending=[False, False])

            # last feeded time for data
            last_time = data.iloc[0].loc['time']

            # filtering data on last feed time
            data = data.loc[data['time'] < last_time]

            # groupby by date sum for volume and mean for %_change
            data = data.groupby(by=['date']).agg({'volume': 'sum'})

            # reset_index
            data.reset_index(inplace=True)

            # calculate avg volume
            avg_volume = int(data.loc[:, 'volume'].mean())

            # sort by date desc
            data = data.sort_values(by=['date'], ascending=False)

            # last feeded volume for data
            last_volume = data.iloc[0].loc['volume']

            # calculate % change of current volume against avg volume
            volume_pct_change = round((last_volume - avg_volume) / avg_volume * 100, 2)

            if volume_pct_change > p_volume_threshold:
                time_list.append(last_time)
                ticker_list.append(ticker)
                vol_list.append(last_volume)
                vol_avg_list.append(avg_volume)
                rvol_list.append(volume_pct_change)
        except Exception as e:
            print('ticker: ', ticker, str(e))
    table_dict['Time'] = time_list
    table_dict['Ticker'] = ticker_list
    table_dict['SumVol_today'] = vol_list
    table_dict['AvgVol_50days'] = vol_avg_list
    table_dict['RVol_%'] = rvol_list
        
    result = pd.DataFrame.from_dict(table_dict)
    result = result.sort_values(by=['RVol_%'], ascending=False)

    print(dt.datetime.now().strftime("%H:%M:%S"))
    if not result.empty:
        print(result)
    else:
        print("Brak wysokiego volume na wybranych aktywach")


p_username = 'perczynskiadam'
p_password = ''

p_symbol_dict = {
    'FSLR': 'NASDAQ',
    'CRWD': 'NASDAQ',
    'COIN': 'NASDAQ',
    'MARA': 'NASDAQ',
    'AMBA': 'NASDAQ',
    'CRM': 'NYSE',
    'OPEN': 'NASDAQ',
    'MDB': 'NASDAQ',
    'AFRM': 'NASDAQ',
    'UPST': 'NASDAQ',
    'SKIN': 'NASDAQ',
    'U': 'NYSE',
    'NVDA': 'NASDAQ',
    'SPOT': 'NYSE',
    'INMD': 'NASDAQ',
    'ENPH': 'NASDAQ',
    'TEAM': 'NASDAQ',
    'CSX': 'NASDAQ',
    'MQ': 'NASDAQ',
    'APPS': 'NASDAQ',
    'DDOG': 'NASDAQ',
    'COP': 'NYSE',
    'DVN': 'NYSE',
    'NET': 'NYSE',
    'SEDG': 'NASDAQ',
    'ABNB': 'NASDAQ',
    'DOCN': 'NYSE',
    'ETSY': 'NASDAQ'
}
p_interval = Interval.in_5_minute
p_volume_threshold = 50
p_no_of_days_to_calc_avg_vol = 50

today = dt.date.today().strftime("%Y-%m-%d")

# GPW
# p_sch_start_date, p_sch_end_date, p_start_market, p_end_market = f'{today} 09:05:30', f'{today} 17:00:30', '09:00:00', '17:00:00'
# USA
p_sch_start_date, p_sch_end_date, p_start_market, p_end_market = f'{today} 14:35:30', f'{today} 21:00:30', '14:30:00', '21:00:00'

p_timeframe = 5 # minutes

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BackgroundScheduler(timezone='Europe/Warsaw', job_defaults=job_defaults)

scheduler.add_job(
    volume_check,
    'interval', 
    args=[
        p_username, p_password, p_symbol_dict, p_interval,
        p_no_of_days_to_calc_avg_vol,
        p_start_market,
        p_end_market,
        p_volume_threshold
    ],
    minutes=p_timeframe,
    start_date=p_sch_start_date,
    end_date=p_sch_end_date
)
scheduler.start()

scheduler.shutdown()

# porownuj volume do 50 dni bez dzisiejszego
# sprawdz czy dane faktycznie uciekają jeśli tak to zgłoś
# porównuj zmianę Rvol, generuj wykresy live, powiadamiaj o wzroście volume w ciągu dnia

