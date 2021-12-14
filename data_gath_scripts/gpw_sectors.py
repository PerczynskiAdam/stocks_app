import urllib.request
import pandas as pd
from datetime import date
import psycopg2
import time


def get_sectors():
   """
   Method read ticker from csv and already imported tickers from db
   and getting overall information about stock

   Returns:
   Fulfilled SQL Table
   """

   # load tickers
   tickers_series = pd.read_csv(r"C:\Users\AdamPer\Desktop\Python\gpw_market\data\gpw_tickers.csv", index_col=0)

   # save tickers as list
   tickers = tickers_series["Ticker"].to_list()

   # połączenie do bazy danych
   conn = psycopg2.connect(dbname="gpw_stocks", user="postgres", password="jeden8l")

   # otwarcie cursora
   cur = conn.cursor()

   # wczytanie tickerow z tabeli, która zawiera tickery już odpytywane
   select_stmt_sektory = "SELECT DISTINCT(ticker) \
                          FROM stage.podsumowanie_ladowania_sektory"

   tickery_sektory = pd.read_sql(select_stmt_sektory, conn)

   tickery_sektory = tickery_sektory['ticker'].to_list()

   # usuniecie już pobranych tickerow z listy
   tickers = [ticker for ticker in tickers if ticker not in tickery_sektory]

   tickers = tickers[:89]

   # utworzenie wyrażenia insert
   insert_stmt = "INSERT INTO tech.sektory (data_pozyskania, ticker, liczba_akcji, kapitalizacja, sektor, branża) \
                  VALUES (%s, %s, %s, %s, %s, %s)"

   # wyrażenie insertujące komunikat do tabeli podsumowania
   insert_notify_stmt = "INSERT INTO stage.podsumowanie_ladowania_sektory (data_ladowania, ticker, status_ladowania) \
                        VALUES (%s, %s, %s)"

   for index, ticker in enumerate(tickers):
      try:
         if (index + 1) % 30 == 0:
            # co trzydiesty ticker poczekaj 30 minut
            time.sleep(900)
         else:
            # co każdy inny poczekaj 2 minuty
            time.sleep(120)

         # zapisz response do zmiennej
         html_file = urllib.request.urlopen('https://www.biznesradar.pl/notowania/' + ticker)
         # pozyskaj tabele z response
         tables = pd.read_html(html_file)
         # dla każdej tabeli
         for table in tables:
            for index, row in table.iterrows():
               # jeśli pierwsza kolumna wiersza tabeli równa się słowu sektor to
               if row[0] == "Sektor:":
                  # transponuj tabele
                  df = table.T

                  # oznacz kolumny jako pierwszy wiersz df
                  df.columns = df.iloc[0, :]

                  # wyrzuc pierwszy wiersz df
                  df.drop([0], inplace=True)

                  # wyrzuc niepotrzebne kolumny
                  df = df.loc[:, ["Liczba akcji:", "Kapitalizacja:", "Sektor:", "Branża:"]]

                  # wstaw na pierwszą pozycję datę pobrania informacji
                  df.insert(column="Data pozyskania", loc=0, value=date.today())

                  # wstaw na drugą pozycję kolumnę z nazwą tickera
                  df.insert(column="Ticker", loc=1, value=ticker)

                  # usniecie spacji z kolumn numerycznych
                  df.loc[:, "Liczba akcji:"].replace(" ", "", inplace=True, regex=True)
                  df.loc[:, "Kapitalizacja:"].replace(" ", "", inplace=True, regex=True)

                  # wstawienie danych do tabeli
                  cur.execute(insert_stmt, df.iloc[0].to_list())

                  # zapisanie do tabeli "sukces" jeśli informacje dla ticker'a zostały poprawnie zaimportowane
                  cur.execute(insert_notify_stmt, [date.today(), ticker, "Sukces"])

                  # zapisanie zmian
                  conn.commit()
               
         print("Done: ", ticker)

      except Exception as e:
         # zapisanie do tabeli treści błędu jeśli informacje dla ticker'a zostały poprawnie zaimportowane
         cur.execute(insert_notify_stmt, [date.today(), ticker, "Błąd: {}".format(str(e))])
         print(ticker, ": Uruchomione exception")

         # zapisanie zmian
         conn.commit()

         conn.rollback()

         continue

   cur.close()
   conn.close()


get_sectors()
