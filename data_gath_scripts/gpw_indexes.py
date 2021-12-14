import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import datetime as dt


def get_gpw_indexes_with_tickers(dbname, user, password, urls):
    """
    Method to get gpw stocks indexes with tickers and load them to sql table

    Parameters:
    dbname (str): database name
    user (str): database user name
    password (str): data base user password
    urls (list): list of urls to scrap indexes and tickers from
    """
    today = dt.date.today()

    for url in urls:
        try:
            # wczytaj tabele z url
            data = pd.read_html(url)

            # choose dataframe from list
            data = data[0]

            # get a ticker from Profil column
            data.loc[:, 'Ticker'] = data.loc[:, 'Profil'].apply(lambda row: row.split(" ")[0])

            # assign market index to var
            market_index = url.split(":")[2]

            # get a ticker from Profil column
            data['Market_index'] = market_index

            data = data.loc[data['Ticker'].apply(lambda row: len(row) < 5)]

            # choose data
            data = data[['Market_index', 'Ticker']]

            # connect to db
            conn = psycopg2.connect(dbname=dbname, user=user, password=password)

            # cursor open
            cur = conn.cursor()

            # sql statement
            insert_stmt = "INSERT INTO tech.ticker_indexes (market_index, ticker) VALUES %s"

            # tuples of data to insert
            tickers = [tuple(row) for row in data.to_numpy()]

            # execute statement
            execute_values(cur, insert_stmt, tickers)

            # commit changes
            conn.commit()

            # create list of values to insert to summary import table
            values_to_insert = [today, market_index, 'Sukces']

            # insert statement
            insert_stmt_sum = "INSERT INTO tech.ticker_indexes_load_sum (date_of_import, market_index, error_msg) VALUES (%s, %s, %s)"

            # execute statement
            cur.execute(insert_stmt_sum, values_to_insert)

            # commit changes
            conn.commit()

        except Exception as e:
            # assign error message to var  
            error_msg = str(e)

            # create list of values to insert
            values_to_insert = [today, market_index, error_msg]

            # insert statement
            insert_stmt = "INSERT INTO tech.ticker_indexes_load_sum (date_of_import, market_index, error_msg) VALUES (%s, %s, %s)"

            # execute statement
            execute_values(cur, insert_stmt, values_to_insert)

            # commit changes
            conn.commit()

            conn.rollback()

        # closing the cursor
        cur.close()

        # closing the connection
        conn.close()


urls = [
    'https://www.biznesradar.pl/gielda/indeks:WIG20',
    'https://www.biznesradar.pl/gielda/indeks:mWIG40',
    'https://www.biznesradar.pl/gielda/indeks:sWIG80'
]

dbname = "stock_market"
user = "postgres"
password = ""


get_gpw_indexes_with_tickers(dbname, user, password, urls)