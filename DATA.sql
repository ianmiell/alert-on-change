--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: alert_on_change; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY alert_on_change (alert_on_change_id, name, output, last_updated) FROM stdin;
\.


--
-- Name: alert_on_change_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('alert_on_change_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

