DROP TABLE IF EXISTS tech.ticker_indexes;

CREATE TABLE tech.ticker_indexes (
	id serial4 NOT NULL,
	market_index varchar(10) NOT NULL,
	ticker varchar(10) NOT NULL,
	CONSTRAINT ticker_indexes_pkey PRIMARY KEY (market_index, ticker)
);


drop table if exists import.tickers;
create table import.tickers (
	id serial not null,
	ticker varchar(10)
);


drop table tech.sektory;
create table tech.sektory (
id serial PRIMARY KEY,
data_pozyskania date,
ticker varchar(10) UNIQUE,
liczba_akcji integer,
kapitalizacja integer,
sektor varchar(50),
branża varchar(50)
)

truncate table tech.sektory;

dROP TABLE import.wskazniki_gpw;
CREATE TABLE import.wskazniki_gpw
(
    id serial NOT NULL,
    kwartał date,
    ticker character varying(10),
	liczba_akcji bigint,
    przychody_ze_sprzedazy_na_akcje numeric(7,2),
    zysk_na_akcje numeric(7,2),
    cena_zysk numeric(7,2),
    zysk_operacyjny_na_akcje numeric(7,2),
    roe numeric(7,2),
    marza_zysku_netto numeric(7,2),
    PRIMARY KEY (id),
    UNIQUE (kwartał, ticker)
)



drop table stage.podsumowanie_ladowania_sektory;
create table stage.podsumowanie_ladowania_sektory (
data_ladowania date,
ticker varchar(10),
status_ladowania varchar(1000) default Null
)

drop table stage.podsumowanie_ladowania_inicjalnego;
create table stage.podsumowanie_ladowania_inicjalnego (
data_ladowania date,
ticker varchar(10),
status_ladowania varchar(1000) default Null
)
