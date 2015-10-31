CREATE TABLE alert_on_change (
    alert_on_change_id integer NOT NULL,
    name text NOT NULL,
    output text NOT NULL default '',
    last_updated timestamp NOT NULL DEFAULT now()        
);


ALTER TABLE public.alert_on_change OWNER TO postgres;

CREATE SEQUENCE alert_on_change_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.alert_on_change_id_seq OWNER TO postgres;
                                                                                                            
ALTER TABLE ONLY alert_on_change ADD CONSTRAINT alert_on_change_pkey PRIMARY KEY (alert_on_change_id);  
