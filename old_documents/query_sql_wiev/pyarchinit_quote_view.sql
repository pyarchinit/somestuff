-- View: pyarchinit_quote_view

-- DROP VIEW pyarchinit_quote_view;

CREATE OR REPLACE VIEW pyarchinit_quote_view AS 
 SELECT pyarchinit_quote.gid, pyarchinit_quote.sito_q, pyarchinit_quote.area_q, pyarchinit_quote.us_q, pyarchinit_quote.unita_misura_q, pyarchinit_quote.quota_q, pyarchinit_quote.the_geom, us_table.id_us, us_table.sito, us_table.area, us_table.us, us_table.struttura, us_table.d_stratigrafica, us_table.d_interpretativa, us_table.descrizione, us_table.interpretazione, us_table.rapporti, us_table.periodo_iniziale, us_table.fase_iniziale, us_table.periodo_finale, us_table.fase_finale, us_table.anno_scavo, us_table.cont_per
   FROM pyarchinit_quote
   JOIN us_table ON pyarchinit_quote.sito_q::text = us_table.sito AND pyarchinit_quote.area_q::text = us_table.area::text AND pyarchinit_quote.us_q::text = us_table.us::text;

ALTER TABLE pyarchinit_quote_view OWNER TO postgres;

