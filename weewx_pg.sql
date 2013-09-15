--
-- PostgreSQL database initialization script
--
-- Execute it like this:  psql -d <your_database> -f weewx_pg.sql
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: archive; Type: TABLE; Schema: public; Owner: weewx; Tablespace: 
--

CREATE TABLE archive (
    datetime timestamp without time zone NOT NULL,
    usunits integer NOT NULL,
    "interval" integer NOT NULL,
    barometer real,
    pressure real,
    altimeter real,
    intemp real,
    outtemp real,
    inhumidity real,
    outhumidity real,
    windspeed real,
    winddir real,
    windgust real,
    windgustdir real,
    rainrate real,
    rain real,
    dewpoint real,
    windchill real,
    heatindex real,
    et real,
    radiation real,
    uv real,
    extratemp1 real,
    extratemp2 real,
    extratemp3 real,
    soiltemp1 real,
    soiltemp2 real,
    soiltemp3 real,
    soiltemp4 real,
    leaftemp1 real,
    leaftemp2 real,
    extrahumid1 real,
    extrahumid2 real,
    soilmoist1 real,
    soilmoist2 real,
    soilmoist3 real,
    soilmoist4 real,
    leafwet1 real,
    leafwet2 real,
    rxcheckpercent real,
    txbatterystatus real,
    consbatteryvoltage real,
    hail real,
    hailrate real,
    heatingtemp real,
    heatingvoltage real,
    supplyvoltage real,
    referencevoltage real,
    windbatterystatus real,
    rainbatterystatus real,
    outtempbatterystatus real,
    intempbatterystatus real
);


ALTER TABLE public.archive OWNER TO weewx;

--
-- Name: archive_pkey; Type: CONSTRAINT; Schema: public; Owner: weewx; Tablespace: 
--

ALTER TABLE ONLY archive
    ADD CONSTRAINT archive_pkey PRIMARY KEY (datetime);

