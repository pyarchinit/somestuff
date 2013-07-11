-- View: pyarchinit_reperti_e_us_view

-- DROP VIEW pyarchinit_reperti_e_us_view;

CREATE OR REPLACE VIEW pyarchinit_reperti_e_us_view AS 
 SELECT inventario_materiali_table.id_invmat, inventario_materiali_table.sito AS sito_rep, inventario_materiali_table.area AS area_rep, inventario_materiali_table.us AS us_rep, inventario_materiali_table.tipo_reperto, inventario_materiali_table.criterio_schedatura, inventario_materiali_table.definizione, inventario_materiali_table.descrizione AS descrizione_rep, inventario_materiali_table.lavato, inventario_materiali_table.nr_cassa, inventario_materiali_table.luogo_conservazione, inventario_materiali_table.stato_conservazione AS stato_conservazione_rep, inventario_materiali_table.datazione_reperto, inventario_materiali_table.elementi_reperto, inventario_materiali_table.misurazioni, inventario_materiali_table.rif_biblio, inventario_materiali_table.tecnologie, us_table.sito AS sito_us, us_table.area AS area_us, us_table.us AS us_us, us_table.d_stratigrafica, us_table.d_interpretativa, us_table.descrizione AS descrizione_us, us_table.interpretazione AS interpretazione_us, us_table.periodo_iniziale, us_table.fase_iniziale, us_table.periodo_finale, us_table.fase_finale, us_table.scavato, us_table.attivita, us_table.anno_scavo, us_table.metodo_di_scavo, us_table.inclusi, us_table.campioni, us_table.rapporti, us_table.data_schedatura, us_table.schedatore, us_table.formazione, us_table.stato_di_conservazione, us_table.colore, us_table.consistenza, us_table.struttura, us_table.cont_per
   FROM inventario_materiali_table
   JOIN us_table ON inventario_materiali_table.sito = us_table.sito AND inventario_materiali_table.area::text = us_table.area::text AND inventario_materiali_table.us::text = us_table.us::text;

ALTER TABLE pyarchinit_reperti_e_us_view OWNER TO postgres;

