import urllib.request
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


def scrap_gpw_tickers_and_insert_to_db(url, dbname, user, password):
    """
    Method to web scrap gpw tickers from url and insert to DB
    Parameters:
    url (str): url as a string with ticker tables
    
    """

    # get reponse from url
    html_file = urllib.request.urlopen(url)

    # save response as list of dataframes
    tables = pd.read_html(html_file)

    # get first dataframe from a list
    tickers_table = tables[0]

    # filter df on Profil column
    tickers_table_filtered = tickers_table[tickers_table.apply(lambda x: ("gdfp" not in x["Profil"] and "Profil" not in x["Profil"]), axis=1)].copy()

    # create ticker column based on Profil column
    tickers_table_filtered.loc[:, "Ticker"] = tickers_table_filtered.loc[:, "Profil"].apply(lambda x: x.split(" (")[0])

    # get all rows for Ticker column
    tickers = tickers_table_filtered.loc[:, "Ticker"]

    # connect to db
    conn = psycopg2.connect(dbname=dbname, user=user, password=password)

    # cursor open
    cur = conn.cursor()

    # insert stmt
    insert_tickers_stmt = "INSERT INTO import.tickers (ticker) VALUES %s"

    # convert series to list of ticker tuples
    ticker_tuples = [tuple([row]) for row in tickers]

    # insert tuples to database
    execute_values(cur, insert_tickers_stmt, tuple(ticker_tuples))

    # commit changes
    conn.commit()

    # closing the cursor
    cur.close()

    # closing the connection
    conn.close()


url = 'https://www.biznesradar.pl/gielda/akcje_gpw'

dbname = "gpw_market"
user = "postgres"
password = ""

scrap_gpw_tickers_and_insert_to_db(url, dbname, user, password)
