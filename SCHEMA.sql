--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alert_on_change; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE alert_on_change (
    alert_on_change_id integer NOT NULL,
    command text NOT NULL,
    output text DEFAULT ''::text NOT NULL,
    last_updated timestamp without time zone DEFAULT now() NOT NULL,
    common_threshold int default 100 NOT NULL,
	email_address text NOT NULL
);


ALTER TABLE public.alert_on_change OWNER TO postgres;

--
-- Name: alert_on_change_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE alert_on_change_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.alert_on_change_id_seq OWNER TO postgres;

ALTER TABLE ONLY alert_on_change ALTER COLUMN alert_on_change_id SET DEFAULT nextval('alert_on_change_id_seq'::regclass);

--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

