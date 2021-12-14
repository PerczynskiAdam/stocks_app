CREATE OR REPLACE VIEW raports.v_wskazniki_roczne
 AS
 WITH roczne AS (
         SELECT date_part('year'::text, wg."kwartał") AS rok,
            wg.ticker,
            sum(wg.przychody_ze_sprzedazy_na_akcje) AS roczne_przychody_ze_sprzedazy_na_akcje,
            sum(wg.zysk_na_akcje) AS roczny_zysk_na_akcje,
            sum(wg.cena_zysk) AS roczna_cena_zysk,
            sum(wg.zysk_operacyjny_na_akcje) AS roczny_zysk_operacyjny_na_akcje,
            sum(wg.roe) AS roczne_roe,
            sum(wg.marza_zysku_netto) AS roczna_marza_zysku_netto
           FROM import.wskazniki_gpw wg
          GROUP BY (date_part('year'::text, wg."kwartał")), wg.ticker
          ORDER BY (date_part('year'::text, wg."kwartał")), wg.ticker
        ), liczba AS (
         SELECT count(*) AS liczba_danych_w_roku,
            date_part('year'::text, wskazniki_gpw."kwartał") AS rok,
            wskazniki_gpw.ticker
           FROM import.wskazniki_gpw
          GROUP BY (date_part('year'::text, wskazniki_gpw."kwartał")), wskazniki_gpw.ticker
        ), avg AS (
         SELECT roczne.rok,
            roczne.ticker,
            round((roczne.roczne_przychody_ze_sprzedazy_na_akcje / (liczba.liczba_danych_w_roku)::numeric), 2) AS avg_roczne_przychody_ze_sprzedazy_na_akcje,
            round((roczne.roczny_zysk_na_akcje / (liczba.liczba_danych_w_roku)::numeric), 2) AS avg_roczny_zysk_na_akcje,
            round((roczne.roczna_cena_zysk / (liczba.liczba_danych_w_roku)::numeric), 2) AS avg_roczna_cena_zysk,
            round((roczne.roczny_zysk_operacyjny_na_akcje / (liczba.liczba_danych_w_roku)::numeric), 2) AS avg_roczny_zysk_operacyjny_na_akcje,
            round((roczne.roczne_roe / (liczba.liczba_danych_w_roku)::numeric), 2) AS avg_roczne_roe,
            round((roczne.roczna_marza_zysku_netto / (liczba.liczba_danych_w_roku)::numeric), 2) AS avg_roczna_marza_zysku_netto
           FROM (liczba
             JOIN roczne ON ((((liczba.ticker)::text = (roczne.ticker)::text) AND (roczne.rok = liczba.rok))))
        ), py AS (
         SELECT avg.rok,
            avg.ticker,
            avg.avg_roczne_przychody_ze_sprzedazy_na_akcje,
            avg.avg_roczny_zysk_na_akcje,
            avg.avg_roczna_cena_zysk,
            avg.avg_roczny_zysk_operacyjny_na_akcje,
            avg.avg_roczne_roe,
            avg.avg_roczna_marza_zysku_netto,
            lag(avg.avg_roczne_przychody_ze_sprzedazy_na_akcje, 1) OVER (ORDER BY avg.ticker, avg.rok) AS avg_roczne_przychody_ze_sprzedazy_na_akcje_py,
            lag(avg.avg_roczny_zysk_na_akcje, 1) OVER (ORDER BY avg.ticker, avg.rok) AS avg_roczny_zysk_na_akcje_py,
            lag(avg.avg_roczna_cena_zysk, 1) OVER (ORDER BY avg.ticker, avg.rok) AS avg_roczna_cena_zysk_py,
            lag(avg.avg_roczny_zysk_operacyjny_na_akcje, 1) OVER (ORDER BY avg.ticker, avg.rok) AS avg_roczny_zysk_operacyjny_na_akcje_py,
            lag(avg.avg_roczne_roe, 1) OVER (ORDER BY avg.ticker, avg.rok) AS avg_roczne_roe_py,
            lag(avg.avg_roczna_marza_zysku_netto, 1) OVER (ORDER BY avg.ticker, avg.rok) AS avg_roczna_marza_zysku_netto_py
           FROM avg
        )
 SELECT py.rok,
    py.ticker,
    round(((py.avg_roczne_przychody_ze_sprzedazy_na_akcje - py.avg_roczne_przychody_ze_sprzedazy_na_akcje_py) / NULLIF(py.avg_roczne_przychody_ze_sprzedazy_na_akcje_py, (0)::numeric)), 2) AS przychody_ze_sprzedazy_na_akcje_yoy,
    round(((py.avg_roczny_zysk_na_akcje - py.avg_roczny_zysk_na_akcje_py) / NULLIF(py.avg_roczny_zysk_na_akcje_py, (0)::numeric)), 2) AS zysk_na_akcje_yoy,
    round(((py.avg_roczna_cena_zysk - py.avg_roczna_cena_zysk_py) / NULLIF(py.avg_roczna_cena_zysk_py, (0)::numeric)), 2) AS cena_zysk_yoy,
    round(((py.avg_roczny_zysk_operacyjny_na_akcje - py.avg_roczny_zysk_operacyjny_na_akcje_py) / NULLIF(py.avg_roczny_zysk_operacyjny_na_akcje_py, (0)::numeric)), 2) AS zysk_operacyjny_na_akcje_yoy,
    round(((py.avg_roczne_roe - py.avg_roczne_roe_py) / NULLIF(py.avg_roczne_roe_py, (0)::numeric)), 2) AS roe_yoy,
    round(((py.avg_roczna_marza_zysku_netto - py.avg_roczna_marza_zysku_netto_py) / NULLIF(py.avg_roczna_marza_zysku_netto_py, (0)::numeric)), 2) AS marza_zysku_netto_yoy
   FROM py;

ALTER TABLE raports.v_wskazniki_roczne
    OWNER TO postgres;


-- chcę porównać ten sam kwartał w poprzednich latach
drop view raports.V_wskazniki_kwartalne
create or replace view raports.V_wskazniki_kwartalne as with 
pq as (select -- przeliczam różnice procentową pomiędzy tymi samymi kwartałami z poprzedniego roku
kwartał,
ticker,
przychody_ze_sprzedazy_na_akcje,
zysk_na_akcje,
cena_zysk,
zysk_operacyjny_na_akcje,
roe,
marza_zysku_netto,
LAG(przychody_ze_sprzedazy_na_akcje, 4) OVER (
order by ticker, kwartał) przychody_ze_sprzedazy_na_akcje_pq,
LAG(zysk_na_akcje, 4) OVER (
order by ticker, kwartał) zysk_na_akcje_pq,
LAG(cena_zysk, 4) OVER (
order by ticker, kwartał) cena_zysk_pq,
LAG(zysk_operacyjny_na_akcje, 4) OVER (
order by ticker, kwartał) zysk_operacyjny_na_akcje_pq,
LAG(roe, 4) OVER (
order by ticker, kwartał) roe_pq,
LAG(marza_zysku_netto, 4) OVER (
order by ticker, kwartał) marza_zysku_netto_pq
from import.wskazniki_gpw wg)
select -- liczę wartości procentowe 
kwartał,
ticker,
ROUND((przychody_ze_sprzedazy_na_akcje - przychody_ze_sprzedazy_na_akcje_pq)/NULLIF(przychody_ze_sprzedazy_na_akcje_pq, 0), 2) przychody_ze_sprzedazy_na_akcje_qoq,
ROUND((zysk_na_akcje - zysk_na_akcje_pq)/NULLIF(zysk_na_akcje_pq, 0), 2) zysk_na_akcje_qoq,
ROUND((cena_zysk - cena_zysk_pq)/NULLIF(cena_zysk_pq, 0), 2) cena_zysk_qoq,
ROUND((zysk_operacyjny_na_akcje - zysk_operacyjny_na_akcje_pq)/NULLIF(zysk_operacyjny_na_akcje_pq, 0), 2) zysk_operacyjny_na_akcje_qoq,
ROUND((roe - roe_pq)/NULLIF(roe_pq, 0), 2) roe_qoq,
ROUND((marza_zysku_netto - marza_zysku_netto_pq)/NULLIF(marza_zysku_netto_pq, 0), 2) marza_zysku_netto_qoq
from pq
