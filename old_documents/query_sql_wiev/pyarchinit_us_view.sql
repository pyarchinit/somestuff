-- View: pyarchinit_us_view

-- DROP VIEW pyarchinit_us_view;

CREATE OR REPLACE VIEW pyarchinit_us_view AS 
 SELECT pyunitastratigrafiche.gid, pyunitastratigrafiche.the_geom, pyunitastratigrafiche.tipo_us_s, pyunitastratigrafiche.scavo_s, pyunitastratigrafiche.area_s, pyunitastratigrafiche.us_s, pyunitastratigrafiche.stratigraph_index_us, us_table.id_us, us_table.sito, us_table.area, us_table.us, us_table.struttura, us_table.d_stratigrafica AS definizione_stratigrafica, us_table.d_interpretativa AS definizione_interpretativa, us_table.descrizione, us_table.interpretazione, us_table.rapporti, us_table.periodo_iniziale, us_table.fase_iniziale, us_table.periodo_finale, us_table.fase_finale, us_table.anno_scavo, us_table.cont_per, us_table.order_layer
   FROM pyunitastratigrafiche
   JOIN us_table ON pyunitastratigrafiche.scavo_s::text = us_table.sito AND pyunitastratigrafiche.area_s::text = us_table.area::text AND pyunitastratigrafiche.us_s = us_table.us
  ORDER BY us_table.order_layer DESC, pyunitastratigrafiche.stratigraph_index_us DESC, pyunitastratigrafiche.gid;

ALTER TABLE pyarchinit_us_view OWNER TO postgres;

