--
-- PostgreSQL database dump
--

-- Started on 2012-07-12 18:40:28 CEST

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
-- TOC entry 2547 (class 1259 OID 142258)
-- Dependencies: 6
-- Name: pyarchinit_thesaurus_sigle; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE pyarchinit_thesaurus_sigle (
    id_thesaurus_sigle integer NOT NULL,
    nome_tabella character varying,
    sigla character(3),
    sigla_estesa character varying,
    descrizione character varying,
    tipologia_sigla character varying
);


ALTER TABLE public.pyarchinit_thesaurus_sigle OWNER TO postgres;

--
-- TOC entry 2546 (class 1259 OID 142256)
-- Dependencies: 6 2547
-- Name: pyarchinit_thesaurus_sigle_id_thesaurus_sigle_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE pyarchinit_thesaurus_sigle_id_thesaurus_sigle_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.pyarchinit_thesaurus_sigle_id_thesaurus_sigle_seq OWNER TO postgres;

--
-- TOC entry 2895 (class 0 OID 0)
-- Dependencies: 2546
-- Name: pyarchinit_thesaurus_sigle_id_thesaurus_sigle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE pyarchinit_thesaurus_sigle_id_thesaurus_sigle_seq OWNED BY pyarchinit_thesaurus_sigle.id_thesaurus_sigle;


--
-- TOC entry 2896 (class 0 OID 0)
-- Dependencies: 2546
-- Name: pyarchinit_thesaurus_sigle_id_thesaurus_sigle_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('pyarchinit_thesaurus_sigle_id_thesaurus_sigle_seq', 134, true);


--
-- TOC entry 2889 (class 2604 OID 142261)
-- Dependencies: 2546 2547 2547
-- Name: id_thesaurus_sigle; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE pyarchinit_thesaurus_sigle ALTER COLUMN id_thesaurus_sigle SET DEFAULT nextval('pyarchinit_thesaurus_sigle_id_thesaurus_sigle_seq'::regclass);


--
-- TOC entry 2892 (class 0 OID 142258)
-- Dependencies: 2547
-- Data for Name: pyarchinit_thesaurus_sigle; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (11, 'struttura_table', 'VA ', 'Vasca', 'La sigla VA comprende ogni tipologia di vasca', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (12, 'struttura_table', 'ST ', 'Strada', 'La sigla ST comprende ogni tipologia di strada', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (13, 'struttura_table', 'TB ', 'Tomba', 'La sigla TB comprende ogni tipologia di tomba', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (15, 'struttura_table', 'SAR', 'Struttura Artigianale', 'La sigla SAR comprende qualsiasi tipo di struttura artigianale', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (14, 'struttura_table', 'SA ', 'Struttura Agricola', 'La sigla SA indica una struttura agricola', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (102, 'pyunitastratigrafiche', NULL, 'barba', 'utilizzata per caratterizzare la pendenza di una us', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (20, 'struttura_table', 'TOR', 'Torrione', 'La sigla TOR comprende i torrioni', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (103, 'pyunitastratigrafiche', NULL, 'cocciopesto', 'cocciopesto rinvenuto in scavo', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (22, 'struttura_table', 'RPA', 'Recinto per animali', 'La sigla RPA indica i recinti per animali', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (19, 'struttura_table', 'FIG', 'Figlinae', 'La sigla FIG indica figline', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (24, 'struttura_table', 'FOM', 'Fornace per mattoni', 'La sigla FOM indica la fornace per mattoni', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (25, 'struttura_table', 'FOF', 'Fornace per metalli', 'La sigla FOF indica la fornace per il metallo', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (23, 'struttura_table', 'CAL', 'Calcara', 'La sigla CAL indica la calcara', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (26, 'struttura_table', 'FOV', 'Fornace per il vetro', 'La sigla FOV indica la fornace per il vetro', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (28, 'struttura_table', 'MAG', 'Magazzino', 'La sigla MAG comprende ogni tipologia di magazzino', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (105, 'pyunitastratigrafiche', NULL, 'calce', 'utilizzata per calce sbriciolata all''interno di uno strato', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (106, 'pyunitastratigrafiche', NULL, 'tegola', 'utilizzata per le tegole rinvenute in scavo', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (108, 'pyunitastratigrafiche', NULL, 'pietra', 'pietre rinvenute in scavo', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (109, 'pyunitastratigrafiche', NULL, 'ghiaia', 'utilizzata per gli inclusi di ghiaia presenti in strato', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (110, 'pyunitastratigrafiche', NULL, 'ferro', 'ferro rinvenuto in scavo', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (111, 'pyunitastratigrafiche', NULL, 'curva di livello', 'utilizzata per indicare i cambiamenti di quota', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (112, 'pyunitastratigrafiche', NULL, 'mosaico', 'tessere di mosaico rinvenute in scavo', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (113, 'pyunitastratigrafiche', NULL, 'coppo', 'coppi rinvenuti in scavo', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (116, 'inventario_materiali_table', NULL, 'Medioadriatica', NULL, 'tipo reperto');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (74, 'us_table', NULL, 'Strato di pietre e ciottoli', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (75, 'us_table', NULL, 'Strato di pietre e laterizi', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (76, 'us_table', NULL, 'Strato di pietrisco', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (117, 'us_table', NULL, 'Riempimento di carboni e cenere', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (114, 'us_table', NULL, 'Strato di carbone e cenere', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (115, 'inventario_materiali_table', NULL, 'Sigillata africana', NULL, 'tipo reperto');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (118, 'us_table', NULL, 'Riempimento di argilla concotta', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (77, 'us_table', NULL, 'Strato di porfido', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (119, 'us_table', NULL, 'Riempimento di argilla', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (120, 'us-table', NULL, 'Riempimento di ceramica sbriciolata', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (121, 'pyunitastratigrafiche', NULL, 'ceramica sbriciolata', 'piccoli frammenti ceramici rinvenuti di sulla superficie di strato', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (31, 'us_table', NULL, 'Reperto ceramico', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (32, 'us_table', NULL, 'Assito di legno', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (123, 'pyunitastratigrafiche', NULL, 'anfora', 'definisce la presenza di frammenti di anfora', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (33, 'us_table', NULL, 'Elemento in pietra', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (34, 'us_table', NULL, 'Cavi', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (35, 'us_table', NULL, 'Reperto generico', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (36, 'us_table', NULL, 'Materiali eterogenei', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (39, 'us_table', NULL, 'Strato di ciottoli', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (30, 'us_table', NULL, 'Abolita', 'Unità stratigrafica abolita', 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (7, 'struttura_table', 'FG ', 'Fogna', 'La sigla FO comprende ogni tipologia di fogna', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (6, 'struttura_table', 'CA ', 'Capanna', 'La sigla CA comprende ogni tipologia di capanna', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (5, 'struttura_table', 'CL ', 'Canaletta', 'La sigla CL comprende le canalette di scolo dell''acqua', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (16, 'struttura_table', 'OS ', 'Ossario', 'La sigla OS indica l'' ossario', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (17, 'struttura_table', 'CM ', 'Cinta Muraria', 'La sigla CM comprende ogni tipologia di cinta muraria', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (18, 'struttura_table', 'RE ', 'Recinto Funerario', 'La sigla RE comprende ogni tipologia di recinto funerario', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (21, 'struttura_table', 'PZ ', 'Pozzo', 'La sigla PZ comprende ogni tipologia di pozzo', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (27, 'struttura_table', 'AN ', 'Anfoteatro', 'La sigla AN indica l''anfiteatro', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (29, 'struttura_table', 'FS ', 'Fossa di scarico', 'La sigla FS indica le fosse di scarico', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (4, 'struttura_table', 'MU ', 'Muro', 'La sigla MU conprende ogni tipologia muraria', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (3, 'struttura_table', 'CN ', 'Canale', 'La sigla CN indica i canali', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (2, 'struttura_table', 'ED ', 'Edificio', 'La sigla ED comprende ogni tipologia di edificio', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (1, 'struttura_table', 'FO ', 'Fornace', 'La sigla FO comprende tutte le tipologie di fornace', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (8, 'struttura_table', 'TO ', 'Torre', 'La sigla TO indica le torri', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (9, 'struttura_table', 'CI ', 'Cisterna', 'La sigla CI comprende ogni tipologia di cisterna', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (10, 'struttura_table', 'PA ', 'Pavimento', 'La sigla PA comprende ogni tipologia di pavimento', 'Tipologia di struttura');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (52, 'us_table', NULL, 'Blocco di malta', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (91, 'pyunitastratigrafiche', NULL, 'reperto ceramico', 'definisce tutte le caratterizzazioni inerenti a reperti ceramici rinvenuti in scavo', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (38, 'us_table', NULL, 'Conglomerato cementizio', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (40, 'us_table', NULL, 'Struttura in muratura', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (41, 'us_table', NULL, 'Strato di intonaco', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (42, 'us_table', NULL, 'Strato di laterizi', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (46, 'us_table', NULL, 'Strato di ciottoli e laterizi', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (47, 'us_table', NULL, 'Strato di ciottoli, laterizi e pietrisco', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (48, 'us_table', NULL, 'Strato di ciottoli, laterizi e ceramica', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (104, 'pyunitastratigrafiche', NULL, 'reperto osteologico animale', 'utilizzata per le componenti dello scheletro animale', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (44, 'us_table', NULL, 'Strato di cenere', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (37, 'us_table', NULL, 'Strato di terreno concottato', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (51, 'us_table', NULL, 'Reperto in osso', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (127, 'pyunitastratigrafiche', NULL, 'dolio', 'definisce la presenza di frammenti di dolio', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (53, 'us_table', NULL, 'Reperto in bronzo', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (54, 'us_table', NULL, 'Reperto osteologico', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (55, 'us_table', NULL, 'Reperto osteologico umano', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (56, 'us_table', NULL, 'Riempimento', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (57, 'us_table', NULL, 'Strato di macerie', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (58, 'us_table', NULL, 'Strato di argilla', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (59, 'us_table', NULL, 'Strato di argilla concotta', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (60, 'us_table', NULL, 'Strato di asfalto', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (45, 'us_table', NULL, 'Strato di cenere e ossa umane combuste', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (78, 'us_table', NULL, 'Strato di sabbia', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (62, 'us_table', NULL, 'Strato di carbone e ossa umane combuste', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (61, 'us_table', NULL, 'Strato di cenere, carbone e ossa umane combuste', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (63, 'us_table', NULL, 'Strato di carbone e reperti vegetali', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (43, 'us_table', NULL, 'Strato di carbone', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (64, 'us_table', NULL, 'Strato di ghiaia', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (65, 'us_table', NULL, 'Strato di ghiaia e catrame', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (66, 'us_table', NULL, 'Strato di laterizi e legno', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (67, 'us_table', NULL, 'Strato di laterizi e malta', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (68, 'us_table', NULL, 'Strato di laterizi e pietre', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (69, 'us_table', NULL, 'Strato di legno carbonizzato', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (70, 'us_table', NULL, 'Strato di malta', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (71, 'us_table', NULL, 'Strato di malta e ciottoli', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (72, 'us_table', NULL, 'Strato di pietra', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (73, 'us_table', NULL, 'Reperto litico', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (79, 'us_table', NULL, 'Strato di sabbia e argilla', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (80, 'us_table', NULL, 'Strato di sabbia e carbone', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (81, 'us_table', NULL, 'Strato di sabbia e calce', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (124, 'pyunitastratigrafiche', NULL, 'anfora testa', 'definisce la presenza di frammenti di anfora', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (83, 'us_table', NULL, 'Strato di terra', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (84, 'us_table', NULL, 'Strato di terra e laterizi', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (85, 'us_table', NULL, 'Strato di terra e carbone', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (86, 'us_table', NULL, 'Strato di terra e malta', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (87, 'us_table', NULL, 'Strato di terra e pietre', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (88, 'us_table', NULL, 'Strato di sabbia e terra', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (50, 'us_table', NULL, 'Elemento in cemento', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (89, 'us_table', NULL, 'Taglio', NULL, 'definizione stratigrafica');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (125, 'pyunitastratigrafiche', NULL, 'anfora fondo', 'definisce la presenza di frammenti di anfora', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (122, 'pyunitastratigrafiche', NULL, 'reperto metallico', 'definisce tutte le caratterizzazioni inerenti a reperti metallici rinvenuti in scavo', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (90, 'pyunitastratigrafiche', NULL, 'ciottolo', 'serve per definire tutti i ciottoli che vengono disegnati in scavo', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (128, 'pyunitastratigrafiche', NULL, 'esagonetta', 'definisce la presenza di esagonette', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (107, 'pyunitastratigrafiche', NULL, 'reperto vitreo', 'utilizzata per i reperti vitrei rinvenuti in scavo', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (93, 'pyunitastratigrafiche', NULL, 'laterizio', 'laterizi rinvenuti in scavo', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (94, 'pyunitastratigrafiche', NULL, 'malta', 'legante dei muri', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (92, 'pyunitastratigrafiche', NULL, 'positiva', 'definisce i tipi di us positive', 'tipo di us');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (95, 'pyunitastratigrafiche', NULL, 'grumi di malta', 'utilizzata in caso di malta che caratterizza uno strato', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (96, 'pyunitastratigrafiche', NULL, 'negativa', 'limiti di us negative', 'tipo di us');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (97, 'pyunitastratigrafiche', NULL, 'struttura', 'limiti di strutture', 'tipo di us');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (98, 'pyunitastratigrafiche', NULL, 'cemento', 'legante di strutture', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (99, 'pyunitastratigrafiche', NULL, 'carbone', 'utilizzata per inclusi di carbone rinvenuti all''interno dello strato', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (100, 'pyunitastratigrafiche', NULL, 'concotto', 'utilizzata per grumi di concotto che caratterizzano uno strato', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (101, 'pyunitastratigrafiche', NULL, 'argilla', 'utilizzata per grumi di argilla che caratterizzano uno strato', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (129, 'pyunitastratigrafiche', NULL, 'pelta', 'definisce la presenza di pelte da pavimento', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (130, 'pyunitastratigrafiche', NULL, 'intonaco', 'definisce la presenza di pelte di intonaco nello strato', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (131, 'pyunitastratigrafiche', NULL, 'reperto osteologico umano', 'utilizzata per le componenti dello scheletro umano', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (132, 'pyunitastratigrafiche', NULL, 'reperto osteologico animale', 'utilizzata per le componenti dello scheletro animale', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (133, 'pyunitastratigrafiche', NULL, 'reperto osteologico non identificabile', 'utilizzata per le componenti dello scheletro non identificabile', 'tipo di caratterizzazione');
INSERT INTO pyarchinit_thesaurus_sigle (id_thesaurus_sigle, nome_tabella, sigla, sigla_estesa, descrizione, tipologia_sigla) VALUES (134, 'pyunitastratigrafiche', NULL, 'reperto lapideo', 'utilizzata per i reperti vitrei rinvenuti in scavo', 'tipo di caratterizzazione');


--
-- TOC entry 2891 (class 2606 OID 142266)
-- Dependencies: 2547 2547
-- Name: id_thesaurus_sigle_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY pyarchinit_thesaurus_sigle
    ADD CONSTRAINT id_thesaurus_sigle_pk PRIMARY KEY (id_thesaurus_sigle);


-- Completed on 2012-07-12 18:40:29 CEST

--
-- PostgreSQL database dump complete
--

