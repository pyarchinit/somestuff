--database basato su un template postgis 1.5

-- TOC entry 208 (class 1259 OID 186351)
-- Dependencies: 7 1553
-- Name: pyarchinit_ripartizioni_spaziali; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

-- Schema: public

--DROP SCHEMA public;

--CREATE SCHEMA public
  --AUTHORIZATION postgres;

CREATE TABLE public.pyarchinit_ripartizioni_spaziali (
    gid  serial NOT NULL,
    id_rs character varying(80),
    sito_rs character varying(80),
    tip_rip character varying,
    descr_rs character varying
);

ALTER TABLE public.pyarchinit_ripartizioni_spaziali
  ADD CONSTRAINT ripartizioni_spaziali_pk PRIMARY KEY(gid);


SELECT public.AddGeometryColumn('public', 'pyarchinit_ripartizioni_spaziali','the_geom',3004, 'POLYGON',2);

CREATE INDEX pyarchinit_ripartizioni_spaziali_geom_gist
  ON public.pyarchinit_ripartizioni_spaziali
  USING gist
  (the_geom);

--##############################
-- TABELLA SITI
--##############################

CREATE TABLE public.pyarchinit_siti (
    gid  serial NOT NULL,
    id_sito character varying(80),
    sito_nome character varying(80),
    descr_sito character varying
);

ALTER TABLE public.pyarchinit_siti
  ADD CONSTRAINT siti_pk PRIMARY KEY(gid);

SELECT public.AddGeometryColumn('public', 'pyarchinit_siti','the_geom',3004, 'POINT',2);

CREATE INDEX pyarchinit_siti_geom_gist
  ON public.pyarchinit_siti
  USING gist
  (the_geom);

--##############################
-- TABELLA CAMPIONATURE
--##############################

CREATE TABLE public.pyarchinit_campionature
(
  gid serial NOT NULL,
  id_campion integer,
  sito character varying(200),
  tipo_camp character varying(200),
  dataz character varying(200),
  cronologia integer,
  link_immag character varying(500),
  sigla_camp character varying
);

ALTER TABLE public.pyarchinit_campionature
  ADD CONSTRAINT campionature_pk PRIMARY KEY(gid);

SELECT public.AddGeometryColumn('public', 'pyarchinit_campionature','the_geom',3004, 'POINT',2);

CREATE INDEX pyarchinit_campionature_geom_gist
  ON public.pyarchinit_campionature
  USING gist
  (the_geom);

--##############################
-- TABELLA INDIVIDUI
--##############################

CREATE TABLE  public.pyarchinit_individui
(
  gid serial NOT NULL,
  sito character varying(255),
  sigla_struttura character varying(255),
  note character varying(255),
  id_individuo integer
);

ALTER TABLE public.pyarchinit_individui
  ADD CONSTRAINT individui_pk PRIMARY KEY(gid);

SELECT public.AddGeometryColumn('public', 'pyarchinit_individui','the_geom',3004, 'POINT',2);

CREATE INDEX pyarchinit_individui_geom_gist
  ON public.pyarchinit_individui
  USING gist
  (the_geom);

--##############################
-- TABELLA UNITA' STRATIGRAFICHE
--##############################

CREATE TABLE public.pyunitastratigrafiche
(
  gid serial NOT NULL,
  area_s integer,
  scavo_s character varying(80),
  us_s integer,
  stratigraph_index_us integer DEFAULT 2,
  tipo_us_s character varying,
  rilievo_orginale character varying,
  disegnatore character varying,
  data date);

ALTER TABLE public.pyunitastratigrafiche
  ADD CONSTRAINT pyunitastratigrafiche_pk PRIMARY KEY(gid);

SELECT public.AddGeometryColumn('public', 'pyunitastratigrafiche','the_geom',3004, 'MULTIPOLYGON',2);

CREATE INDEX pyunitastratigrafiche_geom_gist
  ON public.pyunitastratigrafiche
  USING gist
  (the_geom);

--##############################
-- TABELLA QUOTE US
--##############################


CREATE TABLE public.pyarchinit_quote
(
  gid serial NOT NULL,
  sito_q character varying(80),
  area_q integer,
  us_q integer,
  unita_misu_q character varying(80),
  quota_q double precision,
  data character varying,
  disegnatore character varying,
  rilievo_originale character varying);

ALTER TABLE public.pyarchinit_quote
  ADD CONSTRAINT pyarchinit_quote_pk PRIMARY KEY(gid);

SELECT public.AddGeometryColumn('public', 'pyarchinit_quote','the_geom',3004, 'POINT',2);

CREATE INDEX pyarchinit_quote_geom_gist
  ON public.pyarchinit_quote
  USING gist
  (the_geom);

--##############################
-- TABELLA LINEE DI RIFERIMENTO
--##############################

CREATE TABLE public.pyarchinit_linee_rif
(
  gid serial NOT NULL,
  sito character varying(300),
  definizion character varying(80),
  descrizion character varying(80));

ALTER TABLE public.pyarchinit_linee_rif
  ADD CONSTRAINT pyarchinit_linee_rif_pk PRIMARY KEY(gid);

SELECT public.AddGeometryColumn('public', 'pyarchinit_linee_rif','the_geom',3004,'LINESTRING',2);

CREATE INDEX pyarchinit_linee_rif_geom_gist
  ON public.pyarchinit_linee_rif
USING gist
  (the_geom);

--##############################
-- TABELLA PUNTI DI RIFERIMENTO
--##############################

CREATE TABLE public.pyarchinit_punti_rif
(
  gid serial NOT NULL,
  sito character varying(80),
  def_punto character varying(80),
  id_punto character varying(80),
  quota double precision,
  unita_misura_quota character varying,
  area integer);

ALTER TABLE public.pyarchinit_punti_rif
  ADD CONSTRAINT pyarchinit_punti_rif_pk PRIMARY KEY(gid);

SELECT public.AddGeometryColumn('public', 'pyarchinit_punti_rif', 'the_geom',3004,'POINT',2);

CREATE INDEX pyarchinit_punti_rif_geom_gist
  ON public.pyarchinit_punti_rif
USING gist
  (the_geom);

--##############################
-- TABELLA SEZIONI
--##############################

CREATE TABLE public.pyarchinit_sezioni
(
  gid serial NOT NULL,
  id_sezione character varying(80),
  sito character varying(80),
  area integer,
  descr character varying(80));

ALTER TABLE public.pyarchinit_sezioni
  ADD CONSTRAINT pyarchinit_sezioni_pk PRIMARY KEY(gid);

SELECT public.AddGeometryColumn('public', 'pyarchinit_sezioni', 'the_geom',3004,'LINESTRING',2);

CREATE INDEX pyarchinit_sezioni_geom_gist
  ON public.pyarchinit_sezioni
USING gist
  (the_geom);

--##############################
-- TABELLA IPOTESI STRUTTURE
--##############################


CREATE TABLE public.pyarchinit_strutture_ipotesi
(
  gid serial NOT NULL,
  scavo character varying(80),
  id_strutt character varying(80),
  per_iniz integer,
  per_fin integer,
  dataz_ext character varying(80),
  fase_iniz integer,
  fase_fin integer,
  descrizione character varying);

ALTER TABLE public.pyarchinit_strutture_ipotesi
  ADD CONSTRAINT pyarchinit_strutture_ipotesi_pk PRIMARY KEY(gid);

SELECT public.AddGeometryColumn('public', 'pyarchinit_strutture_ipotesi', 'the_geom',3004,'POLYGON',2);

CREATE INDEX pyarchinit_strutture_ipotesi_geom_gist
  ON public.pyarchinit_strutture_ipotesi
USING gist
  (the_geom);

--##############################
-- TABELLA THESAURUS SIGLE & DATA
--##############################

CREATE TABLE public.pyarchinit_thesaurus_sigle
(id_thesaurus_sigle serial NOT NULL,
 nome_tabella character varying,
 sigla character(3),
 sigla_estesa character varying,
 descrizione character varying,
 tipologia_sigla character varying);

ALTER TABLE public.pyarchinit_thesaurus_sigle
  ADD CONSTRAINT pyarchinit_thesaurus_sigle_pk PRIMARY KEY(id_thesaurus_sigle);

--########## DATA ##########

INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (11, 'struttura_table', 'VA ', 'Vasca', 'La sigla VA comprende ogni tipologia di vasca', 'Tipologia di struttura');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (12, 'struttura_table', 'ST ', 'Strada', 'La sigla ST comprende ogni tipologia di strada', 'Tipologia di struttura');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (13, 'struttura_table', 'TB ', 'Tomba', 'La sigla TB comprende ogni tipologia di tomba', 'Tipologia di struttura');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (15, 'struttura_table', 'SAR', 'Struttura Artigianale', 'La sigla SAR comprende qualsiasi tipo di struttura artigianale', 'Tipologia di struttura');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (14, 'struttura_table', 'SA ', 'Struttura Agricola', 'La sigla SA indica una struttura agricola', 'Tipologia di struttura');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (102, 'pyunitastratigrafiche', NULL, 'barba', 'utilizzata per caratterizzare la pendenza di una us', 'tipo di caratterizzazione');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (20, 'struttura_table', 'TOR', 'Torrione', 'La sigla TOR comprende i torrioni', 'Tipologia di struttura');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (103, 'pyunitastratigrafiche', NULL, 'cocciopesto', 'cocciopesto rinvenuto in scavo', 'tipo di caratterizzazione');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (22, 'struttura_table', 'RPA', 'Recinto per animali', 'La sigla RPA indica i recinti per animali', 'Tipologia di struttura');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (19, 'struttura_table', 'FIG', 'Figlinae', 'La sigla FIG indica figline', 'Tipologia di struttura');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (24, 'struttura_table', 'FOM', 'Fornace per mattoni', 'La sigla FOM indica la fornace per mattoni', 'Tipologia di struttura');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (25, 'struttura_table', 'FOF', 'Fornace per metalli', 'La sigla FOF indica la fornace per il metallo', 'Tipologia di struttura');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (23, 'struttura_table', 'CAL', 'Calcara', 'La sigla CAL indica la calcara', 'Tipologia di struttura');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (26, 'struttura_table', 'FOV', 'Fornace per il vetro', 'La sigla FOV indica la fornace per il vetro', 'Tipologia di struttura');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (28, 'struttura_table', 'MAG', 'Magazzino', 'La sigla MAG comprende ogni tipologia di magazzino', 'Tipologia di struttura');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (105, 'pyunitastratigrafiche', NULL, 'calce', 'utilizzata per calce sbriciolata all''interno di uno strato', 'tipo di caratterizzazione');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (106, 'pyunitastratigrafiche', NULL, 'tegola', 'utilizzata per le tegole rinvenute in scavo', 'tipo di caratterizzazione');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (108, 'pyunitastratigrafiche', NULL, 'pietra', 'pietre rinvenute in scavo', 'tipo di caratterizzazione');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (109, 'pyunitastratigrafiche', NULL, 'ghiaia', 'utilizzata per gli inclusi di ghiaia presenti in strato', 'tipo di caratterizzazione');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (110, 'pyunitastratigrafiche', NULL, 'ferro', 'ferro rinvenuto in scavo', 'tipo di caratterizzazione');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (111, 'pyunitastratigrafiche', NULL, 'curva di livello', 'utilizzata per indicare i cambiamenti di quota', 'tipo di caratterizzazione');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (112, 'pyunitastratigrafiche', NULL, 'mosaico', 'tessere di mosaico rinvenute in scavo', 'tipo di caratterizzazione');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (113, 'pyunitastratigrafiche', NULL, 'coppo', 'coppi rinvenuti in scavo', 'tipo di caratterizzazione');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (116, 'inventario_materiali_table', NULL, 'Medioadriatica', NULL, 'tipo reperto');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (74, 'us_table', NULL, 'Strato di pietre e ciottoli', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (75, 'us_table', NULL, 'Strato di pietre e laterizi', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (76, 'us_table', NULL, 'Strato di pietrisco', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (117, 'us_table', NULL, 'Riempimento di carboni e cenere', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (114, 'us_table', NULL, 'Strato di carbone e cenere', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (115, 'inventario_materiali_table', NULL, 'Sigillata africana', NULL, 'tipo reperto');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (118, 'us_table', NULL, 'Riempimento di argilla concotta', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (77, 'us_table', NULL, 'Strato di porfido', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (119, 'us_table', NULL, 'Riempimento di argilla', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (120, 'us-table', NULL, 'Riempimento di ceramica sbriciolata', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (121, 'pyunitastratigrafiche', NULL, 'ceramica sbriciolata', 'piccoli frammenti ceramici rinvenuti di sulla superficie di strato', 'tipo di caratterizzazione');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (31, 'us_table', NULL, 'Reperto ceramico', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (32, 'us_table', NULL, 'Assito di legno', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (123, 'pyunitastratigrafiche', NULL, 'anfora', 'definisce la presenza di frammenti di anfora', 'tipo di caratterizzazione');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (33, 'us_table', NULL, 'Elemento in pietra', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (34, 'us_table', NULL, 'Cavi', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (35, 'us_table', NULL, 'Reperto generico', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (36, 'us_table', NULL, 'Materiali eterogenei', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (135, 'pyunitastratigrafiche', NULL, 'terra', 'utilizzata per legante incoerente', 'tipo di caratterizzazione');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (136, 'us_table', NULL, 'Strato di ghiaia e sabbia ', NULL, 'definizione stratigrafica');
INSERT INTO public.pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (137, 'us_table', NULL, 'Strato di pietre e frammenti ceramici', NULL, 'definizione stratigrafica');