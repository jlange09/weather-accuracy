--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.6
-- Dumped by pg_dump version 9.6.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: collection_times; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE collection_times (
    collection_id integer NOT NULL,
    date_taken timestamp without time zone
);


--
-- Name: current_observations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE current_observations (
    observation_id integer NOT NULL,
    collection_id integer,
    display_location jsonb,
    observation_location jsonb,
    observation_data jsonb
);


--
-- Name: current_observations_observation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE current_observations_observation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: current_observations_observation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE current_observations_observation_id_seq OWNED BY current_observations.observation_id;


--
-- Name: forecast_times_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE forecast_times_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: forecast_times_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE forecast_times_id_seq OWNED BY collection_times.collection_id;


--
-- Name: hourly_forecasts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE hourly_forecasts (
    forecast_id integer NOT NULL,
    collection_id integer,
    fcttime jsonb,
    forecast_data jsonb
);


--
-- Name: hourly_forecast_forecast_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE hourly_forecast_forecast_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hourly_forecast_forecast_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE hourly_forecast_forecast_id_seq OWNED BY hourly_forecasts.forecast_id;


--
-- Name: collection_times collection_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY collection_times ALTER COLUMN collection_id SET DEFAULT nextval('forecast_times_id_seq'::regclass);


--
-- Name: current_observations observation_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY current_observations ALTER COLUMN observation_id SET DEFAULT nextval('current_observations_observation_id_seq'::regclass);


--
-- Name: hourly_forecasts forecast_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY hourly_forecasts ALTER COLUMN forecast_id SET DEFAULT nextval('hourly_forecast_forecast_id_seq'::regclass);


--
-- Name: collection_times collection_times_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY collection_times
    ADD CONSTRAINT collection_times_pkey PRIMARY KEY (collection_id);


--
-- Name: current_observations current_observations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY current_observations
    ADD CONSTRAINT current_observations_pkey PRIMARY KEY (observation_id);


--
-- Name: hourly_forecasts hourly_forecast_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hourly_forecasts
    ADD CONSTRAINT hourly_forecast_pkey PRIMARY KEY (forecast_id);


--
-- Name: current_observations_collection_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX current_observations_collection_id_idx ON current_observations USING btree (collection_id);


--
-- Name: current_observations_gin_observation_data; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX current_observations_gin_observation_data ON current_observations USING gin (observation_data);


--
-- Name: current_observations_gin_observation_data_epoch; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX current_observations_gin_observation_data_epoch ON current_observations USING gin (((observation_data -> 'observation_epoch'::text)));


--
-- Name: hourly_forecasts_collection_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX hourly_forecasts_collection_id_idx ON hourly_forecasts USING btree (collection_id);


--
-- Name: hourly_forecasts_gin_epoch; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX hourly_forecasts_gin_epoch ON hourly_forecasts USING gin (((fcttime -> 'epoch'::text)));


--
-- Name: hourly_forecasts_gin_forecast_data; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX hourly_forecasts_gin_forecast_data ON hourly_forecasts USING gin (forecast_data);


--
-- Name: current_observations current_observations_collection_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY current_observations
    ADD CONSTRAINT current_observations_collection_id_fkey FOREIGN KEY (collection_id) REFERENCES collection_times(collection_id);


--
-- Name: hourly_forecasts hourly_forecast_collection_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hourly_forecasts
    ADD CONSTRAINT hourly_forecast_collection_id_fkey FOREIGN KEY (collection_id) REFERENCES collection_times(collection_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: -
--

GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

