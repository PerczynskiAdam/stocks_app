-- tickery, które się nie załadowały do tech.sektory
select *
from stage.podsumowanie_ladowania_sektory
where status_ladowania <> 'Sukces';

-- delete from stage.podsumowanie_ladowania_sektory
-- where status_ladowania <> 'Sukces';

-- liczba tickerow stage.podsumowanie_ladowania_sektory
select count(*)
from stage.podsumowanie_ladowania_sektory
where status_ladowania = 'Sukces'; -- 431

-- liczba tickerow w tech.sektory
select count(*)
from tech.sektory; -- 431

-- sprawdzenie czy niezaladowane tickery do podsumowania_ladowania_sektory są w tech.sektory
select *
from tech.sektory
where ticker in ('CNG', 'DADA', 'MCF0222', 'PLY');

-- -- -- -- -- -- -- 
-- tickery, które się nie załadowały do import.wskazniki_gpw
select *
from stage.podsumowanie_ladowania_inicjalnego
where status_ladowania <> 'Sukces'; -- 1

-- delete from stage.podsumowanie_ladowania_inicjalnego
-- where status_ladowania <> 'Sukces';

-- sprawdzenie czy niezaladowane tickery do podsumowanie_ladowania_inicjalnego są w import.wskazniki_gpw
select *
from import.wskazniki_gpw
where ticker in ('JJO', 'ELB');

-- liczba tickerow stage.podsumowanie_ladowania_inicjalnego
select count(*)
from stage.podsumowanie_ladowania_inicjalnego
where status_ladowania = 'Sukces'; -- 429


-- liczba tickerow w import.wskazniki_gpw
select count(distinct(ticker))
from import.wskazniki_gpw; -- 429

-- sprawdz jakich tickerow w wskazniki_gpw brakuje z podsumowania ladowania inicjalnego - usunac i sprobwac jeszcze raz zaladowac
select *
-- delete
from stage.podsumowanie_ladowania_inicjalnego
where ticker in (
select pli.ticker
from stage.podsumowanie_ladowania_inicjalnego pli
left join (select distinct(ticker)
	 from import.wskazniki_gpw) as wg on wg.ticker = pli.ticker
where wg.ticker is null);

select *
from import.wskazniki_gpw
where ticker = 'ADV';


-- CAN SLIM
-- zysk na akcję 3 ostatnie kwartały
select kwartał, ticker, zysk_na_akcje_qoq*100 zysk_na_akcje_qoq_pct
from raports.V_wskazniki_kwartalne
where kwartał >= '2020-03-31'
order by ticker asc, kwartał desc;

select count(distinct(ticker))
from raports.V_wskazniki_kwartalne
WHERE kwartał >= '2020-03-31';

-- zysk na akcje ostatnie 4 lata
select rok, ticker, zysk_na_akcje_yoy*100 zysk_na_akcje_yoy_pct
from raports.V_wskazniki_roczne
where rok >= 2017 AND ticker = 'GRN'
order by ticker asc, rok asc;
