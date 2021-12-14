# goal is import data like QQQ, GOLD, YIELDS, SPY and leaders data to score a market before trading

from tvDatafeed import TvDatafeed, Interval
import datetime as dt
import psycopg2
from psycopg2.extras import execute_values


def import_overall_market_informations(symbol_dict, tv_username, tv_password,
                                       db_name, db_user, db_password):
    # login
    tv = TvDatafeed(tv_username, tv_password)

    for ticker, exchange in symbol_dict.items():

        data = tv.get_hist(ticker, exchange, interval=Interval.in_daily, n_bars=110)

        # datetime is stored as a index. We are moving this to columns
        data.reset_index(inplace=True)

        # we need just date column for our analysis
        data['date'] = data.loc[:, 'datetime'].dt.date
        data.drop(columns=['datetime'], inplace=True)

        # getting today date
        today = dt.date.today()

        # Filtering data with today date because some tickers can trade all day.
        # We want have data for full days only
        data = data.loc[data['date'] < today]

        # ordering columns the same as sql table
        data = data[['symbol', 'open', 'high', 'low', 'close', 'volume', 'date']]

        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password)

        cur = conn.cursor()

        # storing columns as a string using in insert_stmt
        columns = data.columns
        columns_str = ','.join(columns)

        # insert statement with skipping not unique pk
        insert_stmt = f"INSERT INTO import.market_info ({columns_str}) VALUES %s ON CONFLICT (date, symbol) DO NOTHING"

        # insert statement with skipping not unique pk
        insert_stmt_sum = "INSERT INTO tech.import_summary (date_of_import, import_type, import_msg)\
                           VALUES (%s, %s, %s) ON CONFLICT (date_of_import, import_type, import_msg) DO NOTHING"

        # values need to be as list of tuples
        values = [tuple(row) for row in data.to_numpy()]

        # setting import_type to differ from other imports
        import_type = f'{ticker} informations'

        try:
            execute_values(cur, insert_stmt, values)

            # commit changes
            conn.commit()

            # list of values to insert
            sum_values_to_insert = [today, import_type, 'Success']

            cur.execute(insert_stmt_sum, sum_values_to_insert)

            conn.commit()

        except psycopg2.Error as e:
            # assign error message to var  
            error_msg = str(e)

            # list of values to insert
            sum_values_to_insert = [today, import_type, error_msg]

            cur.execute(insert_stmt_sum, sum_values_to_insert)

            # commit changes
            conn.commit()

            conn.rollback()

        # closing the cursor
        cur.close()

        # closing the connection
        conn.close()


symbol_dict = {
    'QQQ': 'NASDAQ',
}

tv_username = 'perczynskiadam'
tv_password = ''

db_name = "stock_market"
db_user = "postgres"
db_password = ""


import_overall_market_informations(symbol_dict, tv_username, tv_password, db_name, db_user, db_password)