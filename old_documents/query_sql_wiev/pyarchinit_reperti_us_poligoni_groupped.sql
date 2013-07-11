-- View: pyarchinit_reperti_us_poligoni_groupped

-- DROP VIEW pyarchinit_reperti_us_poligoni_groupped;

CREATE OR REPLACE VIEW pyarchinit_reperti_us_poligoni_groupped AS 
 SELECT pyarchinit_reperti_e_us_e_poligoni_view.id_invmat AS new_id_invmat, st_union(pyarchinit_reperti_e_us_e_poligoni_view.the_geom) AS new_geom
   FROM pyarchinit_reperti_e_us_e_poligoni_view
  GROUP BY pyarchinit_reperti_e_us_e_poligoni_view.id_invmat;

ALTER TABLE pyarchinit_reperti_us_poligoni_groupped OWNER TO postgres;

