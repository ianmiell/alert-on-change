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

COPY alert_on_change (alert_on_change_id, command, output, last_updated, common_threshold, email_address) FROM stdin;
1	curl https://github.com/docker/docker/tags | html2text | sed -n "/Releases Tags/,/PreviousNext/p"	Releases Tags\n             **** v1.9.0-rc4 ****\n             v1.9.0-rc4\nOct_31,_2015     * _e6f5a3c       *** Read_release_notes ***\n                 * _zip\n                 * _tar.gz\n                 * _Notes\n             **** v1.9.0-rc3 ****\n             v1.9.0-rc3\nOct_28,_2015     * _2100b94       *** Read_release_notes ***\n                 * _zip\n                 * _tar.gz\n                 * _Notes\n             **** v1.9.0-rc2 ****\n             v1.9.0-rc2\nOct_23,_2015     * _60d36f7       *** Read_release_notes ***\n                 * _zip\n                 * _tar.gz\n                 * _Notes\n             **** v1.9.0-rc1 ****\n             v1.9.0-rc1\nOct_14,_2015     * _9291a0e       *** Read_release_notes ***\n                 * _zip\n                 * _tar.gz\n                 * _Notes\n             **** v1.8.3 ****\n             v1.8.3\nOct_12,_2015     * _f4bf5c7       *** Read_release_notes ***\n                 * _zip\n                 * _tar.gz\n                 * _Notes\n             **** v1.8.2 ****\n             v1.8.2\nSep_10,_2015     * _0a8c2e3       *** Read_release_notes ***\n                 * _zip\n                 * _tar.gz\n                 * _Notes\n             **** v1.8.2-rc1 ****\n             v1.8.2-rc1\nSep_3,_2015      * _28220ac       *** Read_release_notes ***\n                 * _zip\n                 * _tar.gz\n                 * _Notes\n             **** v1.8.1 ****\n             v1.8.1\nAug_13,_2015     * _d12ea79       *** Read_release_notes ***\n                 * _zip\n                 * _tar.gz\n                 * _Notes\n             **** v1.8.0 ****\n             v1.8.0\nAug_11,_2015     * _0d03096       *** Read_release_notes ***\n                 * _zip\n                 * _tar.gz\n                 * _Notes\n             **** v1.8.0-rc3 ****\n             v1.8.0-rc3\nAug_7,_2015      * _696147b       *** Read_release_notes ***\n                 * _zip\n                 * _tar.gz\n                 * _Notes\nPreviousNext	2015-10-31 19:18:21.798666	100	ian.miell@gmail.com
2	/bin/true		2015-10-31 19:18:21.894835	101	ian.miell@gmail.com
\.


--
-- Name: alert_on_change_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('alert_on_change_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

