import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import datetime as dt


def import_xtb_transactions(dbname, user, password):
    # load the data with header as first row and ; separator
    transactions = pd.read_csv(
        r'C:\Users\aperczyn\Desktop\Python\stocks_app\files\xStation5_cashOperations_1988376_31-12-2006--11-11-2021.csv',
        header=0,
        sep=';'
    )

    conn = psycopg2.connect(dbname=dbname, user=user, password=password)

    cur = conn.cursor()

    # insert statement with skipping not unique pk
    insert_stmt = "INSERT INTO import.transactions_xtb VALUES %s ON CONFLICT (id) DO NOTHING"

    # insert statement with skipping not unique pk
    insert_stmt_sum = "INSERT INTO tech.import_summary (date_of_import, import_type, import_msg)\
                       VALUES (%s, %s, %s) ON CONFLICT (date_of_import, import_type, import_msg) DO NOTHING"

    # values need to be as list of tuples
    values = [tuple(row) for row in transactions.to_numpy()]

    # getting a date to insert
    today = dt.date.today()

    # setting import_type to differ from other imports
    import_type = 'Xtb transactions'

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



dbname = "stock_market"
user = "postgres"
password = ""


import_xtb_transactions(dbname, user, password)



