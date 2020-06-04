CREATE TABLE public.items
(
  id integer NOT NULL,
  site character varying(16) NOT NULL,
  price double precision,
  start_time timestamp without time zone,
  name character varying(128),
  description character varying(64),
  nickname character varying(50),
  CONSTRAINT items_pkey PRIMARY KEY (site, id)
);
