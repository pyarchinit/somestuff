-- View: pyarchinit_pyuscarlinee_view

-- DROP VIEW pyarchinit_pyuscarlinee_view;

CREATE OR REPLACE VIEW pyarchinit_pyuscarlinee_view AS 
 SELECT pyuscarlinee.gid, pyuscarlinee.the_geom, pyuscarlinee.tipo_us_l, pyuscarlinee.sito_l, pyuscarlinee.area_l, pyuscarlinee.us_l, us_table.sito, us_table.id_us, us_table.area, us_table.us, us_table.struttura, us_table.d_stratigrafica AS definizione_stratigrafica, us_table.d_interpretativa AS definizione_interpretativa, us_table.descrizione, us_table.interpretazione, us_table.rapporti, us_table.periodo_iniziale, us_table.fase_iniziale, us_table.periodo_finale, us_table.fase_finale, us_table.anno_scavo, us_table.cont_per
   FROM pyuscarlinee
   JOIN us_table ON pyuscarlinee.sito_l::text = us_table.sito AND pyuscarlinee.area_l::text = us_table.area::text AND pyuscarlinee.us_l = us_table.us;

ALTER TABLE pyarchinit_pyuscarlinee_view OWNER TO postgres;

