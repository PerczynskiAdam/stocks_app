import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from tvDatafeed import TvDatafeed, Interval


authtoken = "bdi2xVGe81ZAenZfvwhL"
start_date = "2019-01-01"

dbname = "gpw_market"
user = "postgres"
db_password = ""

username = 'perczynskiadam'
password = ''

tv = TvDatafeed(username, password)

fslr = tv.get_hist('FSLR', 'NASDAQ', n_bars=10, interval=Interval.in_1_minute)

# z pierwszym razem muszę wczytać tickery i pobrać dane za np. 200 słupkow
# zapisywać błedne tickery do listy i wstawiać do tabelki technicznej, ktore pobraly sie ze zla data
# data | status | tickery, ktore sie nie sciagnely

# za kolejnym razem muszę wczytać tickery z ostatnią datą i filtrować dane z tv po dacie

# connect to db
conn = psycopg2.connect(dbname=dbname, user=user, password=db_password)

# cursor open
cur = conn.cursor()

# read tickers from database
select_stmt = "SELECT ticker FROM import.tickers"

# save data as dataframe
tickers_df = pd.read_sql(select_stmt, conn)

# save tickers as list
tickers = tickers_df['ticker'].to_list()

tickers = tickers[21:22]

for ticker in tickers:
    # read data from quandl
    # data = quandl.get("WSE/AMC", authtoken="bdi2xVGe81ZAenZfvwhL", start_date="2019-01-01")

    # date as a column
    data.reset_index(inplace=True)

    # delete unnesecery columns
    data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

    # insert ticker as a column
    data.insert(column='Ticker', loc=0, value=ticker)

    # save data as list of tuples
    data_tuples = [tuple(row) for row in data.to_numpy()]

    # insert stmt
    insert_tickers_stmt = "INSERT INTO import.stocks_price (Ticker,Date, Open, High, Low, Close, Volume)\
        VALUES %s"

    # insert tuples to database
    execute_values(cur, insert_tickers_stmt, data_tuples)

    # commit changes
    conn.commit()

# closing the cursor
cur.close()

# closing the connection
conn.close()