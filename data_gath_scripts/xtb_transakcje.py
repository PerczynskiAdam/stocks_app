import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


transactions = pd.read_csv(
        r'C:\Users\aperczyn\Desktop\Python\stocks_app\files\xStation5_closedPositions_1988376_31-12-2006--30-12-2021.csv',
        header=0,
        sep=';'
    )

transactions[transactions.duplicated(subset=['Position'])]

transactions.loc[transactions['Position'] == 476849930]

transactions.loc[transactions['Symbol'] == 'LCID.US']


def import_xtb_transactions(dbname, user, password):
    # load the data with header as first row and ; separator
    transactions = pd.read_csv(
        r'C:\Users\aperczyn\Desktop\Python\stocks_app\files\xStation5_closedPositions_1988376_31-12-2006--30-12-2021.csv',
        header=0,
        sep=';'
    )

    conn = psycopg2.connect(dbname=dbname, user=user, password=password)

    cur = conn.cursor()

    # insert statement with skipping not unique key
    insert_stmt = "INSERT INTO import.transactions_xtb\
        (symbol, position, type, quantity, open_time, open_price, close_time, close_price, profit, net_profit, rollover, comment)\
            VALUES %s ON CONFLICT (symbol, position, open_time, close_time) DO NOTHING"

    # values need to be as list of tuples
    values = [tuple(row) for row in transactions.to_numpy()]

    try:
        execute_values(cur, insert_stmt, values)

        # commit changes
        conn.commit()

    except psycopg2.Error as e:
        # assign error message to var
        error_msg = str(e)
        print(error_msg)

        # w razie błędu baza wraca do stanu przed transakcją
        conn.rollback()

    # closing the cursor
    cur.close()

    # closing the connection
    conn.close()



dbname = "stock_market"
user = "postgres"
password = ""


import_xtb_transactions(dbname, user, password)



