-- Database: binance_price

-- DROP DATABASE IF EXISTS binance_price;

CREATE DATABASE binance_price
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- Table: public.prices

-- DROP TABLE IF EXISTS public.prices;

CREATE TABLE IF NOT EXISTS public.prices
(
    symbol text COLLATE pg_catalog."default" NOT NULL DEFAULT '',
    value  double precision                  NOT NULL DEFAULT 0.0,
    CONSTRAINT price_pkey PRIMARY KEY (symbol)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.prices
    OWNER to postgres;

COMMENT ON COLUMN public.prices.symbol
    IS 'Название инструмента';

COMMENT ON COLUMN public.prices.value
    IS 'Цена инструмента';

-- Column: public.prices.symbol

-- ALTER TABLE IF EXISTS public.prices DROP COLUMN IF EXISTS symbol;

-- ALTER TABLE IF EXISTS public.prices
--     ADD COLUMN symbol text COLLATE pg_catalog."default" NOT NULL DEFAULT '';
--
-- COMMENT ON COLUMN public.prices.symbol
--     IS 'Название инструмента';

-- Column: public.prices.value

-- ALTER TABLE IF EXISTS public.prices DROP COLUMN IF EXISTS value;

-- ALTER TABLE IF EXISTS public.prices
--     ADD COLUMN value double precision NOT NULL DEFAULT 0.0;
--
-- COMMENT ON COLUMN public.prices.value
--     IS 'Цена инструмента';
