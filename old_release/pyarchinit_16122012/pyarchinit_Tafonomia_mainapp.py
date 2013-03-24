#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
/***************************************************************************
        pyArchInit Plugin  - A QGIS plugin to manage archaeological dataset
        					 stored in Postgres
                             -------------------
    begin                : 2007-12-01
    copyright            : (C) 2008 by Luca Mandolesi
    email                : mandoluca at gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import sys, os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.QtGui

from qgis.core import *
from qgis.gui import *


from datetime import date
from psycopg2 import *

#--import pyArchInit modules--#
from  pyarchinit_Tafonomia_ui import Ui_Dialog_tafonomia
from  pyarchinit_Tafonomia_ui import *
from  pyarchinit_utility import *
from  pyarchinit_error_check import *
try:
	from  pyarchinit_matrix_exp import *
except:
	pass
from  pyarchinit_pyqgis import Pyarchinit_pyqgis, Order_layers
from  sortpanelmain import SortPanelMain
from  pyarchinit_db_manager import *
from  pyarchinit_exp_USsheet_pdf import *
from delegateComboBox import *
from imageViewer import ImageViewer

class pyarchinit_Tafonomia(QDialog, Ui_Dialog_tafonomia):
	MSG_BOX_TITLE = "PyArchInit - Scheda Tafonomica"
	DATA_LIST = []
	DATA_LIST_REC_CORR = []
	DATA_LIST_REC_TEMP = []
	REC_CORR = 0
	REC_TOT = 0
	STATUS_ITEMS = {"b": "Usa", "f": "Trova", "n": "Nuovo Record"}
	BROWSE_STATUS = "b"
	SORT_MODE = 'asc'
	SORTED_ITEMS = {"n": "Non ordinati", "o": "Ordinati"}
	SORT_STATUS = "n"
	SORT_ITEMS_CONVERTED = ''
	UTILITY = Utility()
	DB_MANAGER = ""
	TABLE_NAME = 'Tafonomia_table'
	MAPPER_TABLE_CLASS = "TAFONOMIA"
	NOME_SCHEDA = "Scheda Tafonomica"
	ID_TABLE = "id_tafonomia"
	CONVERSION_DICT = {
	ID_TABLE:ID_TABLE,
	"Sito":"sito",
	"Numero scheda":"nr_scheda_taf",
	"Tipo struttura scheda":"sigla_struttura",
	"Nr struttura":"nr_struttura",
	"Nr Individuo": "nr_individuo",
	"Rito":"rito",
	"Decrizione":"descrizione_taf",
	"Interpretazione":"interpretazione_taf",
	"Segnacoli":"segnacoli",
	"Canale libatorio":"canale_libatorio_si_no",
	"Oggetti esterni rinvenuti":"oggetti_rinvenuti_esterno",
	"Stato di conservazione":"stato_di_conservazione",
	"Tipo di copertura":"copertura_tipo",
	"Tipo contenitore resti":"tipo_contenitore_resti",
	"Orientamento asse":"orientamento_asse",
	"Orientament Azimut":"orientamento_azimut",
	"Presenza del corredo":"corredo_presenza",
	"Tipo di corredo":"corredo_tipo",
	"Descrizione corredo":"corredo_descrizione",
	"Lunghezza scheletro":"lunghezza_scheletro",
	"Posizione scheletro":"posizione_scheletro",
	"Posizione cranio":"posizione_cranio",
	"Posizione arti superiori":"posizione_arti_superiori",
	"Posizione arti inferiori":"posizione_arti_inferiori",
	"Completo":"completo_si_no",
	"Disturbato":"disturbato_si_no",
	"In connessione":"in_connessione_si_no",
	"Caratteristiche":"caratteristiche"
	}

	SORT_ITEMS = [
				ID_TABLE, 
				"Sito",
				"Numero scheda",
				"Tipo struttura",
				"Nr struttura",
				"Nr Individuo",
				"Rito",
				"Decrizione",
				"Interpretazione",
				"Segnacoli",
				"Canale libatorio",
				"Oggetti esterni rinvenuti",
				"Stato di conservazione",
				"Tipo di copertura",
				"Tipo contenitore resti",
				"Orientamento asse",
				"Orientament Azimut",
				"Presenza del corredo",
				"Tipo di corredo",
				"Descrizione corredo",
				"Lunghezza scheletro",
				"Posizione scheletro",
				"Posizione cranio",
				"Posizione arti superiori",
				"Posizione arti inferiori",
				"Completo",
				"Disturbato",
				"In connessione",
				"Caratteristiche"
				]

	TABLE_FIELDS = [
				"sito",
				"nr_scheda_taf",
				"sigla_struttura",
				"nr_struttura",
				"nr_individuo",
				"rito",
				"descrizione_taf",
				"interpretazione_taf",
				"segnacoli",
				"canale_libatorio_si_no",
				"oggetti_rinvenuti_esterno",
				"stato_di_conservazione",
				"copertura_tipo",
				"tipo_contenitore_resti",
				"orientamento_asse",
				"orientamento_azimut",
				"corredo_presenza",
				"corredo_tipo",
				"corredo_descrizione",
				"lunghezza_scheletro",
				"posizione_scheletro",
				"posizione_cranio",
				"posizione_arti_superiori",
				"posizione_arti_inferiori",
				"completo_si_no",
				"disturbato_si_no",
				"in_connessione_si_no",
				"caratteristiche"
				]

	def __init__(self, iface):
		self.iface = iface
		self.pyQGIS = Pyarchinit_pyqgis(self.iface)

		QDialog.__init__(self)
		self.setupUi(self)
		
		self.customize_GUI() #call for GUI customizations
		self.currentLayerId = None
		try:
			self.on_pushButton_connect_pressed()
		except:
			pass
		
		#SIGNALS & SLOTS Functions
		self.connect(self.comboBox_sito, SIGNAL("currentIndexChanged(int)"), self.charge_struttura_list)  
		self.connect(self.comboBox_sito, SIGNAL("currentIndexChanged(int)"), self.charge_individuo_list)
		#self.connect(self.comboBox_struttura, SIGNAL("editTextChanged (const QString&)"), self.charge_struttura_list)


	def enable_button(self, n):
		self.pushButton_connect.setEnabled(n)

		self.pushButton_new_rec.setEnabled(n)

		self.pushButton_view_all.setEnabled(n)

		self.pushButton_first_rec.setEnabled(n)

		self.pushButton_last_rec.setEnabled(n)

		self.pushButton_prev_rec.setEnabled(n)

		self.pushButton_next_rec.setEnabled(n)

		self.pushButton_delete.setEnabled(n)

		self.pushButton_new_search.setEnabled(n)

		self.pushButton_search_go.setEnabled(n)

		self.pushButton_sort.setEnabled(n)

	def enable_button_search(self, n):
		self.pushButton_connect.setEnabled(n)

		self.pushButton_new_rec.setEnabled(n)

		self.pushButton_view_all.setEnabled(n)

		self.pushButton_first_rec.setEnabled(n)

		self.pushButton_last_rec.setEnabled(n)

		self.pushButton_prev_rec.setEnabled(n)

		self.pushButton_next_rec.setEnabled(n)

		self.pushButton_delete.setEnabled(n)

		self.pushButton_save.setEnabled(n)

		self.pushButton_sort.setEnabled(n)


	def on_pushButton_connect_pressed(self):
		from pyarchinit_conn_strings import *

		conn = Connection()
		conn_str = conn.conn_str()
		try:
			self.DB_MANAGER = Pyarchinit_db_management(conn_str)
			self.DB_MANAGER.connection()
			self.charge_records() #charge records from DB
			#check if DB is empty
			if bool(self.DATA_LIST) == True:
				self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
				self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
				self.BROWSE_STATUS = 'b'
				self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
				self.label_sort.setText(self.SORTED_ITEMS["n"])
				self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
				self.charge_list()
				self.fill_fields()
			else:
				QMessageBox.warning(self, "BENVENUTO", "Benvenuto in pyArchInit" + self.NOME_SCHEDA + ". Il database e' vuoto. Premi 'Ok' e buon lavoro!",  QMessageBox.Ok)
				self.charge_list()
				self.on_pushButton_new_rec_pressed()
		except Exception, e:
			e = str(e)
			if e.find("no such table"):
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br><br> %s. E' NECESSARIO RIAVVIARE QGIS" % (str(e)),  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br> Errore: <br>" + str(e) ,  QMessageBox.Ok)

	def customize_GUI(self):
		self.tableWidget_caratteristiche.setColumnWidth(1,300)
		self.tableWidget_caratteristiche.setColumnWidth(1,200)
		
		#comboBox customizations
		self.setComboBoxEditable(["self.comboBox_sito"],1)
		self.setComboBoxEditable(["self.comboBox_sigla_struttura"],1)
		self.setComboBoxEditable(["self.comboBox_nr_struttura"],1)
		self.setComboBoxEditable(["self.comboBox_nr_individuo"],1)
		self.setComboBoxEnable(["self.lineEdit_nr_scheda"],"False")
		

		#map prevew system
		#self.mapPreview = QgsMapCanvas(self)
		#self.mapPreview.setCanvasColor(QColor(225,225,225))
		#self.tabWidget.addTab(self.mapPreview, "Piante")
		"""
		#media prevew system
		self.iconListWidget = QtGui.QListWidget(self)
		self.iconListWidget.setFrameShape(QtGui.QFrame.StyledPanel)
		self.iconListWidget.setFrameShadow(QtGui.QFrame.Sunken)
		self.iconListWidget.setLineWidth(2)
		self.iconListWidget.setMidLineWidth(2)
		self.iconListWidget.setProperty("showDropIndicator", False)
		self.iconListWidget.setIconSize(QtCore.QSize(150, 150))
		self.iconListWidget.setMovement(QtGui.QListView.Snap)
		self.iconListWidget.setResizeMode(QtGui.QListView.Adjust)
		self.iconListWidget.setLayoutMode(QtGui.QListView.Batched)
		self.iconListWidget.setGridSize(QtCore.QSize(160, 160))
		self.iconListWidget.setViewMode(QtGui.QListView.IconMode)
		self.iconListWidget.setUniformItemSizes(True)
		self.iconListWidget.setBatchSize(1000)
		self.iconListWidget.setObjectName("iconListWidget")
		self.iconListWidget.SelectionMode()
		self.iconListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		self.connect(self.iconListWidget, SIGNAL("itemDoubleClicked(QListWidgetItem *)"),self.openWide_image)
		self.tabWidget.addTab(self.iconListWidget, "Media")



		valuesRS = ["Uguale a", "Si lega a", "Copre", "Coperto da", "Riempie", "Riempito da", "Taglia", "Tagliato da", "Si appoggia a", "Gli si appoggia", ""]
		self.delegateRS = ComboBoxDelegate()
		self.delegateRS.def_values(valuesRS)
		self.delegateRS.def_editable('False')
		self.tableWidget_rapporti.setItemDelegateForColumn(0,self.delegateRS)

		valuesINCL_CAMP = ["Terra", "Pietre", "Laterizio", "Ciottoli", "Calcare", "Calce", "Carboni", "Concotto", "Ghiaia", "Cariossidi", "Malacofauna", "Sabbia", "Malta"]
		self.delegateINCL_CAMP = ComboBoxDelegate()
		valuesINCL_CAMP.sort()
		self.delegateINCL_CAMP.def_values(valuesINCL_CAMP)
		self.delegateINCL_CAMP.def_editable('False')
		self.tableWidget_inclusi.setItemDelegateForColumn(0,self.delegateINCL_CAMP)
		self.tableWidget_campioni.setItemDelegateForColumn(0,self.delegateINCL_CAMP)
		"""

	def loadMapPreview(self, mode = 0):
		if mode == 0:
			""" if has geometry column load to map canvas """
			
			gidstr =  self.ID_TABLE + " = " + str(eval("self.DATA_LIST[int(self.REC_CORR)]." + self.ID_TABLE))	
			layerToSet = self.pyQGIS.loadMapPreview(gidstr)
			self.mapPreview.setLayerSet(layerToSet)
			self.mapPreview.zoomToFullExtent()

		elif mode == 1:
			self.mapPreview.setLayerSet( [ ] )
			self.mapPreview.zoomToFullExtent()

	def loadMediaPreview(self, mode = 0):
		pass
		"""
		self.iconListWidget.clear()
		if mode == 0:
			#if has geometry column load to map canvas

			rec_list =  self.ID_TABLE + " = " + str(eval("self.DATA_LIST[int(self.REC_CORR)]." + self.ID_TABLE))
			search_dict = {'id_us'  : "'"+str(eval("self.DATA_LIST[int(self.REC_CORR)]." + self.ID_TABLE))+"'"}
			record_us_list = self.DB_MANAGER.query_bool(search_dict, 'MEDIATOUS')
			for i in record_us_list:
				search_dict = {'id_media' : "'"+str(i.id_media)+"'"}

				u = Utility()
				search_dict = u.remove_empty_items_fr_dict(search_dict)
				mediathumb_data = self.DB_MANAGER.query_bool(search_dict, "MEDIA_THUMB")
				thumb_path = str(mediathumb_data[0].filepath)

				item = QListWidgetItem(str(i.id_media))

				item.setData(QtCore.Qt.UserRole,str(i.id_media))
				icon = QIcon(thumb_path)
				item.setIcon(icon)
				self.iconListWidget.addItem(item)

		elif mode == 1:
			self.iconListWidget.clear()
		"""


	def openWide_image(self):
		pass
		"""
		items = self.iconListWidget.selectedItems()
		for item in items:
			dlg = ImageViewer(self)
			id_orig_item = item.text() #return the name of original file

			search_dict = {'id_media' : "'"+str(id_orig_item)+"'"}

			u = Utility()
			search_dict = u.remove_empty_items_fr_dict(search_dict)

			try:
				res = self.DB_MANAGER.query_bool(search_dict, "MEDIA")
				file_path = str(res[0].filepath)
			except Exception, e:
				QMessageBox.warning(self, "Errore", "Attenzione 1 file: "+ str(e),  QMessageBox.Ok)

			dlg.show_image(unicode(file_path)) #item.data(QtCore.Qt.UserRole).toString()))
			dlg.exec_()
		"""

	def charge_list(self):
		#lista sito
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))
		try:
			sito_vl.remove('')
		except:
			pass

		self.comboBox_sito.clear()
		self.comboBox_sito_rappcheck.clear()

		sito_vl.sort()
		self.comboBox_sito.addItems(sito_vl)
		self.comboBox_sito_rappcheck.addItems(sito_vl)

		"""
		#lista definizione_stratigrafica
		search_dict = {
		'nome_tabella'  : "'"+'us_table'+"'",
		'tipologia_sigla' : "'"+'definizione stratigrafica'+"'"
		}
		d_stratigrafica = self.DB_MANAGER.query_bool(search_dict, 'PYARCHINIT_THESAURUS_SIGLE')
		d_stratigrafica_vl = [ ]
		for i in range(len(d_stratigrafica)):
			d_stratigrafica_vl.append(d_stratigrafica[i].sigla_estesa)

		d_stratigrafica_vl.sort()
		self.comboBox_def_strat.addItems(d_stratigrafica_vl)
		"""

	def charge_struttura_list(self):
		search_dict = {
		'sito'  : "'"+str(self.comboBox_sito.currentText())+"'",
		}

		struttura_vl = self.DB_MANAGER.query_bool(search_dict, 'STRUTTURA')
		
		#carica il tipo di struttura
		sigla_struttura_list = []

		for i in range(len(struttura_vl)):
			sigla_struttura_list.append(str(struttura_vl[i].sigla_struttura))
		try:
			sigla_struttura_list.remove('')
		except:
			pass

		sigla_struttura_list.sort()

		self.comboBox_sigla_struttura.clear()
		self.comboBox_sigla_struttura.addItems(sigla_struttura_list)
		try:
			self.comboBox_sigla_struttura.setEditText(str(self.DATA_LIST[self.rec_num].sigla_struttura))
		except:
			pass

		
		nr_struttura_list = []

		for i in range(len(struttura_vl)):
			nr_struttura_list.append(str(struttura_vl[i].numero_struttura))
		try:
			nr_struttura_list.remove('')
		except:
			pass

		nr_struttura_list.sort()

		self.comboBox_nr_struttura.clear()
		self.comboBox_nr_struttura.addItems(nr_struttura_list)
		try:
			self.comboBox_nr_struttura.setEditText(self.DATA_LIST[self.rec_num].numero_struttura)
		except:
			pass
			
		
	def charge_individuo_list(self):
		search_dict = {
		'sito'  : "'"+str(self.comboBox_sito.currentText())+"'",
		}

		individuo_vl = self.DB_MANAGER.query_bool(search_dict, 'SCHEDAIND')

		#carica il tipo di individuo
		nr_individuo_list = []

		for i in range(len(individuo_vl)):
			nr_individuo_list.append(str(individuo_vl[i].nr_individuo))
		try:
			nr_individuo_list.remove('')
		except:
			pass

		nr_individuo_list.sort()

		self.comboBox_nr_individuo.clear()
		self.comboBox_nr_individuo.addItems(nr_individuo_list)
		try:
			self.comboBox_nr_individuo.setEditText(self.DATA_LIST[self.rec_num].nr_individuo)
		except:
			pass


	#buttons functions


	def generate_list_pdf(self):
		pass
		"""
		data_list = []

		for i in range(len(self.DATA_LIST)):
			#assegnazione valori di quota mn e max
			sito =  str(self.DATA_LIST[i].sito)
			area = str(self.DATA_LIST[i].area)
			us = int(self.DATA_LIST[i].us)

			res = self.DB_MANAGER.select_quote_from_db_sql(sito, area, us)
			quote = []
			for sing_us in res:
				sing_quota_value = str(sing_us[5])
				if sing_quota_value[0] == '-':
					sing_quota_value = sing_quota_value[:7]
				else:
					sing_quota_value = sing_quota_value[:6]

				sing_quota = [sing_quota_value, sing_us[4]]
				quote.append(sing_quota)
			quote.sort()
			if bool(quote) == True:
				quota_min = '%s %s' % (quote[0][0], quote[0][1])
				quota_max = '%s %s' % (quote[-1][0], quote[-1][1])
			else:
				quota_min = "Non rilevata"
				quota_max = "Non rilevata"
			#assegnazione numero di pianta
			resus = self.DB_MANAGER.select_us_from_db_sql(sito, area, us, "2")
			elenco_record = []
			for us in resus:
				elenco_record.append(us)
			if bool(elenco_record) == True:
				sing_rec = elenco_record[0]
				f = open("test_elenco.txt", "w")
				f.write(str(sing_rec))
				f.close()
				elenco_piante = sing_rec[7]
				if elenco_piante != None:
					piante = elenco_piante
				else:
					piante = "US disegnata su base GIS"
			else:
				piante = "US non disegnata"

			data_list.append([
			str(self.DATA_LIST[i].sito), 									#1 - Sito
			str(self.DATA_LIST[i].area),									#2 - Area
			int(self.DATA_LIST[i].us),										#3 - US
			str(self.DATA_LIST[i].d_stratigrafica),							#4 - Definizione stratigrafica
			str(self.DATA_LIST[i].d_interpretativa),						#5 - Definizione intepretata
			self.DATA_LIST[i].descrizione,									#6 - descrizione
			self.DATA_LIST[i].interpretazione,								#7 - interpretazione
			str(self.DATA_LIST[i].periodo_iniziale),						#8 - periodo iniziale
			str(self.DATA_LIST[i].fase_iniziale),							#9 - fase iniziale
			str(self.DATA_LIST[i].periodo_finale),							#10 - periodo finale iniziale
			str(self.DATA_LIST[i].fase_finale), 							#11 - fase finale
			str(self.DATA_LIST[i].scavato),									#12 - scavato
			str(self.DATA_LIST[i].attivita),								#13 - attivita
			str(self.DATA_LIST[i].anno_scavo),								#14 - anno scavo
			str(self.DATA_LIST[i].metodo_di_scavo),							#15 - metodo
			str(self.DATA_LIST[i].inclusi),									#16 - inclusi
			str(self.DATA_LIST[i].campioni),								#17 - campioni
			str(self.DATA_LIST[i].rapporti),								#18 - rapporti
			str(self.DATA_LIST[i].data_schedatura),							#19 - data schedatura
			str(self.DATA_LIST[i].schedatore),								#20 - schedatore
			str(self.DATA_LIST[i].formazione),								#21 - formazione
			str(self.DATA_LIST[i].stato_di_conservazione),					#22 - conservazione
			str(self.DATA_LIST[i].colore),									#23 - colore
			str(self.DATA_LIST[i].consistenza),								#24 - consistenza
			str(self.DATA_LIST[i].struttura),								#25 - struttura
			str(quota_min),													#26 - quota_min
			str(quota_max),													#27 - quota_max
			str(piante)														#27 - piante
		])
		return data_list
		"""

	def on_pushButton_pdf_exp_pressed(self):
		US_pdf_sheet = generate_pdf()
		data_list = self.generate_list_pdf()
		US_pdf_sheet.build_US_sheets(data_list)


	def on_pushButton_exp_index_us_pressed(self):
		US_index_pdf = generate_pdf()
		data_list = self.generate_list_pdf()
		US_index_pdf.build_index_US(data_list, data_list[0][0])


	def on_toolButtonPan_toggled(self):
		self.toolPan = QgsMapToolPan(self.mapPreview)
		self.mapPreview.setMapTool(self.toolPan)

	def on_pushButton_showSelectedFeatures_pressed(self):
		field_position = self.pyQGIS.findFieldFrDict(self.ID_TABLE)

		field_list = self.pyQGIS.selectedFeatures()

		id_list_sf = self.pyQGIS.findItemInAttributeMap(field_position, field_list)
		id_list = []
		for idl in id_list_sf:
			sid = idl.toInt()
			id_list.append(sid[0])

		items,order_type = [self.ID_TABLE], "asc"
		self.empty_fields()

		self.DATA_LIST = []

		temp_data_list = self.DB_MANAGER.query_sort(id_list, items, order_type, self.MAPPER_TABLE_CLASS, self.ID_TABLE)

		for us in temp_data_list:
			self.DATA_LIST.append(us)

		self.fill_fields()
		self.BROWSE_STATUS = 'b'
		self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
		if type(self.REC_CORR) == "<type 'str'>":
			corr = 0
		else:
			corr = self.REC_CORR

		self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
		self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]

	def on_pushButton_sort_pressed(self):
		dlg = SortPanelMain(self)
		dlg.insertItems(self.SORT_ITEMS)
		dlg.exec_()

		items,order_type = dlg.ITEMS, dlg.TYPE_ORDER

		self.SORT_ITEMS_CONVERTED = []
		for i in items:
			self.SORT_ITEMS_CONVERTED.append(self.CONVERSION_DICT[i])

		self.SORT_MODE = order_type
		self.empty_fields()

		id_list = []
		for i in self.DATA_LIST:
			id_list.append(eval("i." + self.ID_TABLE))
		self.DATA_LIST = []

		temp_data_list = self.DB_MANAGER.query_sort(id_list, self.SORT_ITEMS_CONVERTED, self.SORT_MODE, self.MAPPER_TABLE_CLASS, self.ID_TABLE)

		for i in temp_data_list:
			self.DATA_LIST.append(i)
		self.BROWSE_STATUS = 'b'
		self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
		if type(self.REC_CORR) == "<type 'str'>":
			corr = 0
		else:
			corr = self.REC_CORR

		self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
		self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
		self.SORT_STATUS = "o"
		self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])
		self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.fill_fields()

	def on_toolButtonGis_toggled(self):
		if self.toolButtonGis.isChecked() == True:
			QMessageBox.warning(self, "Messaggio", "Modalita' GIS attiva. Da ora le tue ricerche verranno visualizzate sul GIS", QMessageBox.Ok)
		else:
			QMessageBox.warning(self, "Messaggio", "Modalita' GIS disattivata. Da ora le tue ricerche non verranno piu' visualizzate sul GIS", QMessageBox.Ok)

	def on_toolButtonPreview_toggled(self):
		if self.toolButtonPreview.isChecked() == True:
			QMessageBox.warning(self, "Messaggio", "Modalita' Preview US attivata. Le piante delle US saranno visualizzate nella sezione Piante", QMessageBox.Ok)
			self.loadMapPreview()
		else:
			self.loadMapPreview(1)

	def on_toolButtonPreviewMedia_toggled(self):
		if self.toolButtonPreviewMedia.isChecked() == True:
			QMessageBox.warning(self, "Messaggio", "Modalita' Preview Media US attivata. Le immagini delle US saranno visualizzate nella sezione Media", QMessageBox.Ok)
			self.loadMediaPreview()
		else:
			self.loadMediaPreview(1)

	def on_pushButton_addRaster_pressed(self):
		if self.toolButtonGis.isChecked() == True:
			self.pyQGIS.addRasterLayer()

	def on_pushButton_new_rec_pressed(self):
		#set the GUI for a new record

		if self.BROWSE_STATUS != "n":
			self.BROWSE_STATUS = "n"
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			self.empty_fields()

			self.setComboBoxEditable(["self.comboBox_sito"],0)
			self.setComboBoxEditable(["self.comboBox_sigla_struttura"],0)
			self.setComboBoxEditable(["self.comboBox_nr_struttura"],0)
			self.setComboBoxEditable(["self.comboBox_nr_individuo"],0)
			
			self.setComboBoxEnable(["self.lineEdit_nr_scheda"],"True")
			self.setComboBoxEnable(["self.comboBox_sito"],"True")
			self.setComboBoxEnable(["self.comboBox_sigla_struttura"],"True")
			self.setComboBoxEnable(["self.comboBox_nr_struttura"],"True")
			self.setComboBoxEnable(["self.comboBox_nr_individuo"],"True")

			self.SORT_STATUS = "n"
			self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])

			self.enable_button(0)

	def on_pushButton_save_pressed(self):
		#save record
		if self.BROWSE_STATUS == "b":
			if self.records_equal_check() == 1:
				self.update_if(QMessageBox.warning(self,'ATTENZIONE',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
				self.SORT_STATUS = "n"
				self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])
				self.enable_button(1)
			else:
				QMessageBox.warning(self, "ATTENZIONE", "Non è stata realizzata alcuna modifica.",  QMessageBox.Ok)
		else:
			if self.data_error_check() == 0:
				test_insert = self.insert_new_rec()
				if test_insert == 1:
					self.empty_fields()
					self.SORT_STATUS = "n"
					self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])
					self.charge_records()
					self.charge_list()
					self.BROWSE_STATUS = "b"
					self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
					self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST)-1
					self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
					self.setComboBoxEditable(["self.comboBox_sito"],1)
					self.setComboBoxEditable(["self.comboBox_sigla_struttura"],1)
					self.setComboBoxEditable(["self.comboBox_nr_struttura"],1)
					self.setComboBoxEditable(["self.comboBox_nr_individuo"],1)
					self.setComboBoxEnable(["self.lineEdit_nr_scheda"],"False")
					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.comboBox_sigla_struttura"],"False")
					self.setComboBoxEnable(["self.comboBox_nr_struttura"],"False")
					self.setComboBoxEnable(["self.comboBox_nr_individuo"],"False")

					self.fill_fields(self.REC_CORR)
					self.enable_button(1)

	def on_pushButton_rapp_check_pressed(self):
		sito_check = self.comboBox_sito_rappcheck.currentText()
		self.rapporti_stratigrafici_check(sito_check)
		QMessageBox.warning(self, "Messaggio", "Controllo Rapporti Stratografici. \n Controllo eseguito con successo",  QMessageBox.Ok)

	def data_error_check(self):
		test = 0
		EC = Error_check()

		if EC.data_is_empty(str(self.comboBox_sito.currentText())) == 0:
			QMessageBox.warning(self, "ATTENZIONE", "Campo Sito. \n Il campo non deve essere vuoto",  QMessageBox.Ok)
			test = 1

		if EC.data_is_empty(str(self.comboBox_sigla_struttura.currentText())) == 0:
			QMessageBox.warning(self, "ATTENZIONE", "Campo Tipo Struttura. \n Il campo non deve essere vuoto",  QMessageBox.Ok)
			test = 1

		if EC.data_is_empty(str(self.comboBox_nr_struttura.currentText())) == 0:
			QMessageBox.warning(self, "ATTENZIONE", "Campo Nr Struttura. \n Il campo non deve essere vuoto",  QMessageBox.Ok)
			test = 1

		if EC.data_is_empty(str(self.lineEdit_nr_scheda.text())) == 0:
			QMessageBox.warning(self, "ATTENZIONE", "Campo nr_scheda. \n Il campo non deve essere vuoto",  QMessageBox.Ok)
			test = 1

		nr_scheda_tafonomia = self.lineEdit_nr_scheda.text()
		nr_struttura = self.comboBox_nr_struttura.currentText()

		if nr_scheda_tafonomia != "":
			if EC.data_is_int(nr_scheda_tafonomia) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo nr_scheda. \n Il valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		if nr_struttura != "":
			if EC.data_is_int(nr_struttura) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Nr Struttura. \n Il valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1
		return test

	def insert_new_rec(self):
		##Caratteristiche
		caratteristiche = self.table2dict("self.tableWidget_caratteristiche")
		##
		corredo_tipo = self.table2dict("self.tableWidget_corredo_tipo")

		##orientamento azimut
		if self.lineEdit_orientamento_azimut.text() == "":
			orientamento_azimut = None
		else:
			orientamento_azimut = float(self.lineEdit_orientamento_azimut.text())

		##lunghezza scheletro
		if self.lineEdit_lunghezza_scheletro.text() == "":
			lunghezza_scheletro = None
		else:
			lunghezza_scheletro = float(self.lineEdit_lunghezza_scheletro.text())

		try:
			#data
			data = self.DB_MANAGER.insert_values_tafonomia(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE)+1,
			str(self.comboBox_sito.currentText()), 						#1 - Sito
			int(self.lineEdit_nr_scheda.text()),						#2 - nr scheda tafonomica
			str(self.comboBox_sigla_struttura.currentText()),			#3 - tipo struttura
			int(self.comboBox_nr_struttura.currentText()),				#4 - nr struttura
			int(self.comboBox_nr_struttura.currentText()),				#5 - nr struttura
			str(self.comboBox_rito.currentText()),						#6 - rito
			unicode(self.textEdit_descrizione_taf.toPlainText()),		#7 - descrizione
			unicode(self.textEdit_interpretazione_taf.toPlainText()),	#8 - interpretazione
			str(self.comboBox_segnacoli.currentText()),					#9 - segnacoli
			str(self.comboBox_canale_libatorio.currentText()),			#10 - canale libatorio
			str(self.comboBox_oggetti_esterno.currentText()),			#11 - oggetti esterno
			str(self.comboBox_conservazione_taf.currentText()),			#12 - conservazione
			str(self.comboBox_copertura_tipo.currentText()),			#13 - copertura
			str(self.comboBox_tipo_contenitore_resti.currentText()),	#14 - tipo contenitore resti
			str(self.lineEdit_orientamento_asse.text()),				#15 - orientamento asse
			orientamento_azimut,										#16 - orientamento azimut
			str(self.comboBox_corredo_presenza.currentText()),			#17 - corredo presenza
			str(corredo_tipo),											#18 - corredo tipo
			unicode(self.textEdit_descrizione_corredo.toPlainText()),	#19 - descrizione corredo
			lunghezza_scheletro,										#20 - lunghezza scheletro
			str(self.comboBox_posizione_scheletro.currentText()),		#21 - posizione scheletro
			str(self.comboBox_posizione_cranio.currentText()),			#22 - posizione cranio
			str(self.comboBox_arti_superiori.currentText()),			#23 - arti inferiori
			str(self.comboBox_arti_inferiori.currentText()),			#24 - arti superiori
			str(self.comboBox_completo.currentText()),					#25 - completo
			str(self.comboBox_disturbato.currentText()),				#26 - disturbato
			str(self.comboBox_in_connessione.currentText()), 			#27 - in connessione
			str(caratteristiche))										#28 - caratteristiche

			try:
				self.DB_MANAGER.insert_data_session(data)
				return 1
			except Exception, e:
				e_str = str(e)
				if e_str.__contains__("Integrity"):
					msg = self.ID_TABLE + " gia' presente nel database"
				else:
					msg = e
				QMessageBox.warning(self, "Errore", "Errore di immisione 1 \n"+ str(msg),  QMessageBox.Ok)
				return 0

		except Exception, e:
			QMessageBox.warning(self, "Errore", "Errore di immisione 2 \n"+str(e),  QMessageBox.Ok)
			return 0


	#insert new row into tableWidget
	def on_pushButton_insert_row_corredo_pressed(self):
		self.insert_new_row('self.tableWidget_corredo_tipo')
	def on_pushButton_remove_row_corredo_pressed(self):
		self.remove_row('self.tableWidget_corredo_tipo')

	def on_pushButton_insert_row_caratteristiche_pressed(self):
		self.insert_new_row('self.tableWidget_caratteristiche')
	def on_pushButton_remove_row_caratteristiche_pressed(self):
		self.remove_row('self.tableWidget_caratteristiche')


	#records surf functions
	def on_pushButton_view_all_pressed(self):
		self.empty_fields()
		self.charge_records()
		self.fill_fields()
		self.BROWSE_STATUS = "b"
		self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
		if type(self.REC_CORR) == "<type 'str'>":
			corr = 0
		else:
			corr = self.REC_CORR
		self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
		self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
		self.SORT_STATUS = "n"
		self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])


	def on_pushButton_first_rec_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
		try:
			self.empty_fields()
			self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
			self.fill_fields(0)
			self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
		except Exception, e:
			QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)


	def on_pushButton_last_rec_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
		try:
			self.empty_fields()
			self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST)-1
			self.fill_fields(self.REC_CORR)
			self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
		except Exception, e:
			QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)


	def on_pushButton_prev_rec_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))

		self.REC_CORR = self.REC_CORR-1
		if self.REC_CORR == -1:
			self.REC_CORR = 0
			QMessageBox.warning(self, "Errore", "Sei al primo record!",  QMessageBox.Ok)
		else:
			try:
				self.empty_fields()
				self.fill_fields(self.REC_CORR)
				self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
			except Exception, e:
				QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)


	def on_pushButton_next_rec_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))

		self.REC_CORR = self.REC_CORR+1
		if self.REC_CORR >= self.REC_TOT:
			self.REC_CORR = self.REC_CORR-1
			QMessageBox.warning(self, "Errore", "Sei all'ultimo record!",  QMessageBox.Ok)
		else:
			try:
				self.empty_fields()
				self.fill_fields(self.REC_CORR)
				self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
			except Exception, e:
				QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)


	def on_pushButton_delete_pressed(self):
		msg = QMessageBox.warning(self,"Attenzione!!!","Vuoi veramente eliminare il record? \n L'azione e' irreversibile", QMessageBox.Cancel,1)
		if msg != 1:
			QMessageBox.warning(self,"Messagio!!!","Azione Annullata!")
		else:
			try:
				id_to_delete = eval("self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE)
				self.DB_MANAGER.delete_one_record(self.TABLE_NAME, self.ID_TABLE, id_to_delete)
				self.charge_records() #charge records from DB
				QMessageBox.warning(self,"Messaggio!!!","Record eliminato!")
				self.charge_list()
			except:
					QMessageBox.warning(self, "Attenzione", "Il database e' vuoto!",  QMessageBox.Ok)
			if bool(self.DATA_LIST) == False:
				self.DATA_LIST = []
				self.DATA_LIST_REC_CORR = []
				self.DATA_LIST_REC_TEMP = []
				self.REC_CORR = 0
				self.REC_TOT = 0
				self.empty_fields()
				self.set_rec_counter(0, 0)
			#check if DB is empty
			if bool(self.DATA_LIST) == True:
				self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
				self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
				self.fill_fields()
				self.BROWSE_STATUS = "b"
				self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
				self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.SORT_STATUS = "n"
		self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])


	def on_pushButton_new_search_pressed(self):
		#set the GUI for a new search
		self.enable_button_search(0)
		if self.BROWSE_STATUS != "f":
			self.BROWSE_STATUS = "f"
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			self.empty_fields()
			self.set_rec_counter('','')
			self.SORT_STATUS = "n"
			self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])
			self.setComboBoxEditable(["self.comboBox_sito"],1)
			self.setComboBoxEditable(["self.comboBox_sigla_struttura"],1)
			self.setComboBoxEditable(["self.comboBox_nr_struttura"],1)
			self.setComboBoxEditable(["self.comboBox_nr_individuo"],1)
			self.setComboBoxEnable(["self.lineEdit_nr_scheda"],"True")
			self.setComboBoxEnable(["self.comboBox_sito"],"True")
			self.setComboBoxEnable(["self.comboBox_sigla_struttura"],"True")
			self.setComboBoxEnable(["self.comboBox_nr_struttura"],"True")
			self.setComboBoxEnable(["self.comboBox_nr_individuo"],"True")

	def on_pushButton_showLayer_pressed(self):
		sing_layer = [self.DATA_LIST[self.REC_CORR]]
		self.pyQGIS.charge_vector_layers(sing_layer)

	def on_pushButton_crea_codice_periodo_pressed(self):
		sito = str(self.comboBox_sito.currentText())
		self.DB_MANAGER.update_cont_per(sito)
		self.empty_fields()
		self.charge_records()
		self.fill_fields(self.REC_CORR) #ricaricare tutti i record in uso e passare il valore REC_CORR a fill_fields

		QMessageBox.warning(self, "Attenzione", "Codice periodo aggiornato per lo scavo %s" % (sito),  QMessageBox.Ok)

	def on_pushButton_search_go_pressed(self):
		if self.BROWSE_STATUS != "f":
			QMessageBox.warning(self, "ATTENZIONE", "Per eseguire una nuova ricerca clicca sul pulsante 'new search' ",  QMessageBox.Ok)
		else:
			## nr scheda
			if self.lineEdit_nr_scheda.text() != "":
				nr_scheda = int(self.lineEdit_nr_scheda.text())
			else:
				nr_scheda = ""

			## nr struttura
			if self.comboBox_nr_struttura.currentText() != "":
				nr_struttura = int(self.comboBox_nr_struttura.currentText())
			else:
				nr_struttura = ""

			## nr individuo
			if self.comboBox_nr_individuo.currentText() != "":
				nr_individuo = int(self.comboBox_nr_individuo.currentText())
			else:
				nr_individuo = ""

			##orientamento azimut
			if self.lineEdit_orientamento_azimut.text() != "":
				orientamento_azimut = float(self.lineEdit_orientamento_azimut.text())
			else:
				orientamento_azimut = None

			##lunghezza scheletro
			if self.lineEdit_lunghezza_scheletro.text() != "":
				lunghezza_scheletro = float(self.lineEdit_lunghezza_scheletro.text())
			else:
				lunghezza_scheletro = None

			search_dict = {
			self.TABLE_FIELDS[0]  : "'"+str(self.comboBox_sito.currentText())+"'", 									#1 - Sito
			self.TABLE_FIELDS[1]  : nr_scheda,																		#2 - Nr schede
			self.TABLE_FIELDS[2]  : "'"+str(self.comboBox_sigla_struttura.currentText())+"'",						#3 - Tipo struttura
			self.TABLE_FIELDS[3]  : nr_struttura,																	#4 - Nr struttura
			self.TABLE_FIELDS[4]  : nr_individuo,																	#5 - Nr struttura
			self.TABLE_FIELDS[5]  : "'"+str(self.comboBox_rito.currentText())+"'",									#6 - Rito
			self.TABLE_FIELDS[6]  : "'"+unicode(self.textEdit_descrizione_taf.toPlainText())+"'",					#7 - Descrizione tafonimia
			self.TABLE_FIELDS[7]  : "'"+unicode(self.textEdit_interpretazione_taf.toPlainText())+"'",				#8 - Interpretazione tafonimia
			self.TABLE_FIELDS[8]  : "'"+str(self.comboBox_segnacoli.currentText())+"'",								#9 - Segnacoli
			self.TABLE_FIELDS[9]  : "'"+str(self.comboBox_canale_libatorio.currentText())+"'",						#10 - Canale libatorio
			self.TABLE_FIELDS[10]  : "'"+str(self.comboBox_oggetti_esterno.currentText())+"'",	 					#11 - Oggetti esterno
			self.TABLE_FIELDS[11] : "'"+str(self.comboBox_conservazione_taf.currentText())+"'", 					#12 - Conservazione tafonomia
			self.TABLE_FIELDS[12] : "'"+str(self.comboBox_copertura_tipo.currentText())+"'",						#13 - Copertura tipo
			self.TABLE_FIELDS[13] : "'"+str(self.comboBox_tipo_contenitore_resti.currentText())+"'",				#14 - Tipo contenitore resti  
			self.TABLE_FIELDS[14] : "'"+str(self.lineEdit_orientamento_asse.text())+"'",							#15 - orientamento asse
			self.TABLE_FIELDS[15] : orientamento_azimut,															#16 - orientamento azimut
			self.TABLE_FIELDS[17] : "'"+str(self.comboBox_corredo_presenza.currentText())+"'",						#17 - corredo
			self.TABLE_FIELDS[20] : lunghezza_scheletro,															#18 - lunghezza scheletro
			self.TABLE_FIELDS[21] : "'"+str(self.comboBox_posizione_scheletro.currentText())+"'",					#19 - posizione scheletro
			self.TABLE_FIELDS[22] : "'"+str(self.comboBox_posizione_cranio.currentText())+"'",						#20 - posizione cranio
			self.TABLE_FIELDS[23] : "'"+str(self.comboBox_arti_superiori.currentText())+"'",						#21 - arti superiori
			self.TABLE_FIELDS[24] : "'"+str(self.comboBox_arti_inferiori.currentText())+"'",						#24 - arti inferiori
			self.TABLE_FIELDS[25] : "'"+str(self.comboBox_completo.currentText())+"'",								#25 - completo
			self.TABLE_FIELDS[26] : "'"+str(self.comboBox_disturbato.currentText())+"'",							#26 - disturbato
			self.TABLE_FIELDS[27] : "'"+str(self.comboBox_in_connessione.currentText())+"'"							#27 - in connessione
			}

			u = Utility()
			search_dict = u.remove_empty_items_fr_dict(search_dict)

			if bool(search_dict) == False:
				QMessageBox.warning(self, "ATTENZIONE", "Non e' stata impostata alcuna ricerca!!!",  QMessageBox.Ok)
			else:
				res = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS)
				if bool(res) == False:
					QMessageBox.warning(self, "ATTENZIONE", "Non e' stato trovato alcun record!",  QMessageBox.Ok)

					self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
					self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
					self.fill_fields(self.REC_CORR)
					self.BROWSE_STATUS = "b"
					self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])

					self.setComboBoxEditable(["self.comboBox_sito"],1)
					self.setComboBoxEditable(["self.comboBox_sigla_struttura"],1)
					self.setComboBoxEditable(["self.comboBox_nr_struttura"],1)
					self.setComboBoxEditable(["self.comboBox_nr_individuo"],1)
					self.setComboBoxEnable(["self.lineEdit_nr_scheda"],"False")
					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.comboBox_sigla_struttura"],"False")
					self.setComboBoxEnable(["self.comboBox_nr_struttura"],"False")
					self.setComboBoxEnable(["self.comboBox_nr_individuo"],"False")
				else:
					self.DATA_LIST = []
					for i in res:
						self.DATA_LIST.append(i)
					self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
					self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
					self.fill_fields()
					self.BROWSE_STATUS = "b"
					self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
					self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)

					if self.REC_TOT == 1:
						strings = ("E' stato trovato", self.REC_TOT, "record")
						if self.toolButtonGis.isChecked() == True:
							self.pyQGIS.charge_vector_layers(self.DATA_LIST)
					else:
						strings = ("Sono stati trovati", self.REC_TOT, "records")
						if self.toolButtonGis.isChecked() == True:
							self.pyQGIS.charge_vector_layers(self.DATA_LIST)

					self.setComboBoxEditable(["self.comboBox_sito"],1)
					self.setComboBoxEditable(["self.comboBox_sigla_struttura"],1)
					self.setComboBoxEditable(["self.comboBox_nr_struttura"],1)
					self.setComboBoxEditable(["self.comboBox_nr_individuo"],1)
					self.setComboBoxEnable(["self.lineEdit_nr_scheda"],"False")
					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.comboBox_sigla_struttura"],"False")
					self.setComboBoxEnable(["self.comboBox_nr_struttura"],"False")
					self.setComboBoxEnable(["self.comboBox_nr_individuo"],"False")

					QMessageBox.warning(self, "Messaggio", "%s %d %s" % strings,  QMessageBox.Ok)
		self.enable_button_search(1)

	def update_if(self, msg):
		rec_corr = self.REC_CORR
		self.msg = msg
		if self.msg == 1:
			self.update_record()
			id_list = []
			for i in self.DATA_LIST:
				id_list.append(eval("i."+ self.ID_TABLE))
			self.DATA_LIST = []
			if self.SORT_STATUS == "n":
				temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], 'asc', self.MAPPER_TABLE_CLASS, self.ID_TABLE)
			else:
				temp_data_list = self.DB_MANAGER.query_sort(id_list, self.SORT_ITEMS_CONVERTED, self.SORT_MODE, self.MAPPER_TABLE_CLASS, self.ID_TABLE)

			for i in temp_data_list:
				self.DATA_LIST.append(i)
			self.BROWSE_STATUS = "b"
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			if type(self.REC_CORR) == "<type 'str'>":
				corr = 0
			else:
				corr = self.REC_CORR

	def update_record(self):
		self.DB_MANAGER.update(self.MAPPER_TABLE_CLASS, 
						self.ID_TABLE,
						[eval("int(self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE+")")],
						self.TABLE_FIELDS,
						self.rec_toupdate())


	def rec_toupdate(self):
		rec_to_update = self.UTILITY.pos_none_in_list(self.DATA_LIST_REC_TEMP)
		#self.testing('/testtaafo.txt', str(rec_to_update))
		return rec_to_update


	#custom functions
	def charge_records(self):
		self.DATA_LIST = []
		id_list = []
		for i in self.DB_MANAGER.query(eval(self.MAPPER_TABLE_CLASS)):
			id_list.append(eval("i."+ self.ID_TABLE))
		temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], 'asc', self.MAPPER_TABLE_CLASS, self.ID_TABLE)
		for i in temp_data_list:
			self.DATA_LIST.append(i)


	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today


	def table2dict(self, n):
		self.tablename = n
		row = eval(self.tablename+".rowCount()")
		col = eval(self.tablename+".columnCount()")
		lista=[]
		for r in range(row):
			sub_list = []
			for c in range(col):
				value = eval(self.tablename+".item(r,c)")
				if value != None:
					sub_list.append(str(value.text()))
					
			if bool(sub_list) == True:
				lista.append(sub_list)
		return lista


	def tableInsertData(self, t, d):
		"""Set the value into alls Grid"""
		self.table_name = t
		self.data_list = eval(d)
		self.data_list.sort()

		#column table count
		table_col_count_cmd = ("%s.columnCount()") % (self.table_name)
		table_col_count = eval(table_col_count_cmd)

		#clear table
		table_clear_cmd = ("%s.clearContents()") % (self.table_name)
		eval(table_clear_cmd)

		for i in range(table_col_count):
			table_rem_row_cmd = ("%s.removeRow(%d)") % (self.table_name, i)
			eval(table_rem_row_cmd)

		#for i in range(len(self.data_list)):
			#self.insert_new_row(self.table_name)
		
		for row in range(len(self.data_list)):
			cmd = ('%s.insertRow(%s)') % (self.table_name, row)
			eval(cmd)
			for col in range(len(self.data_list[row])):
				#item = self.comboBox_sito.setEditText(self.data_list[0][col]
				item = QTableWidgetItem(self.data_list[row][col])
				exec_str = ('%s.setItem(%d,%d,item)') % (self.table_name,row,col)
				eval(exec_str)

	def insert_new_row(self, table_name):
		"""insert new row into a table based on table_name"""
		cmd = table_name+".insertRow(0)"
		eval(cmd)

	def remove_row(self, table_name):
		"""insert new row into a table based on table_name"""
		table_row_count_cmd = ("%s.rowCount()") % (table_name)
		table_row_count = eval(table_row_count_cmd)
		rowSelected_cmd = ("%s.selectedIndexes()") % (table_name)
		rowSelected = eval(rowSelected_cmd)
		rowIndex = (rowSelected[0].row())
		cmd = ("%s.removeRow(%d)") % (table_name, rowIndex)
		eval(cmd)


	def empty_fields(self):
		caratteristiche_row_count = self.tableWidget_caratteristiche.rowCount()
		corredo_tipo_row_count = self.tableWidget_corredo_tipo.rowCount()

		for i in range(caratteristiche_row_count):
			self.tableWidget_caratteristiche.removeRow(0)
		self.insert_new_row("self.tableWidget_caratteristiche")				#17 - caratteristiche

		for i in range(corredo_tipo_row_count):
			self.tableWidget_corredo_tipo.removeRow(0)
		self.insert_new_row("self.tableWidget_corredo_tipo")				#18 - corredo tipo

		self.comboBox_sito.setEditText("") 						#1 - Sito
		self.lineEdit_nr_scheda.clear()							#2 - nr scheda tafonomica
		self.comboBox_sigla_struttura.setEditText("")			#3 - tipo struttura
		self.comboBox_nr_struttura.setEditText("")				#4 - nr struttura
		self.comboBox_nr_individuo.setEditText("")				#4 - nr struttura
		self.comboBox_rito.setEditText("")						#5 - rito
		self.textEdit_descrizione_taf.clear()					#6 - descrizione
		self.textEdit_interpretazione_taf.clear()				#7 - interpretazione
		self.comboBox_segnacoli.setEditText("")					#8 - segnacoli
		self.comboBox_canale_libatorio.setEditText("")			#9 - canale libatorio
		self.comboBox_oggetti_esterno.setEditText("")			#10 - oggetti esterno
		self.comboBox_conservazione_taf.setEditText("")			#11 - conservazione
		self.comboBox_copertura_tipo.setEditText("")			#12 - copertura
		self.comboBox_tipo_contenitore_resti.setEditText("")	#13 - tipo contenitore resti
		self.lineEdit_orientamento_asse.clear()					#14 - orientamento asse
		self.lineEdit_orientamento_azimut.clear()				#14 - orientamento azimut
		self.comboBox_corredo_presenza.setEditText("")			#19 - corredo presenza
		self.textEdit_descrizione_corredo.clear()				#20 - descrizione corredo
		self.lineEdit_lunghezza_scheletro.clear()				#21 - lunghezza scheletro
		self.comboBox_posizione_scheletro.setEditText("")		#22 - posizione scheletro
		self.comboBox_posizione_cranio.setEditText("")			#23 - posizione cranio
		self.comboBox_arti_superiori.setEditText("")			#24 - arti inferiori
		self.comboBox_arti_inferiori.setEditText("")			#25 - arti superiori
		self.comboBox_completo.setEditText("")					#26 - completo
		self.comboBox_disturbato.setEditText("")				#27 - disturbato
		self.comboBox_in_connessione.setEditText("") 			#28 - in connessione

	def fill_fields(self, n=0):
		self.rec_num = n
		try:
			if self.DATA_LIST[self.rec_num].orientamento_azimut == None:
				self.lineEdit_orientamento_azimut.setText("")
			else:
				self.lineEdit_orientamento_azimut.setText(str(self.DATA_LIST[self.rec_num].orientamento_azimut))		#14 - orientamento azimut

			if self.DATA_LIST[self.rec_num].lunghezza_scheletro == None:
				self.lineEdit_lunghezza_scheletro.setText("")
			else:
				self.lineEdit_lunghezza_scheletro.setText(str(self.DATA_LIST[self.rec_num].lunghezza_scheletro))		#14 - orientamento azimut
			self.comboBox_sito.setEditText(str(self.DATA_LIST[self.rec_num].sito))															#1 - Sito
			self.lineEdit_nr_scheda.setText(str(self.DATA_LIST[self.rec_num].nr_scheda_taf))												#2 - nr_scheda_taf
			self.comboBox_sigla_struttura.setEditText(self.DATA_LIST[self.rec_num].sigla_struttura) 										#3 - sigla_struttura
			self.comboBox_nr_struttura.setEditText(str(self.DATA_LIST[self.rec_num].nr_struttura)) 											#4 - nr_struttura
			self.comboBox_nr_individuo.setEditText(str(self.DATA_LIST[self.rec_num].nr_individuo)) 											#5 - nr_individuo
			self.comboBox_rito.setEditText(str(self.DATA_LIST[self.rec_num].rito))															#6 - rito
			unicode(self.textEdit_descrizione_taf.setText(self.DATA_LIST[self.rec_num].descrizione_taf))									#7 - descrizione_taf
			unicode(self.textEdit_interpretazione_taf.setText(self.DATA_LIST[self.rec_num].interpretazione_taf))							#8 - interpretazione_taf
			self.comboBox_segnacoli.setEditText(self.DATA_LIST[self.rec_num].segnacoli)														#9 - segnacoli
			self.comboBox_canale_libatorio.setEditText(self.DATA_LIST[self.rec_num].canale_libatorio_si_no)									#10 - canale_libatorio_si_no
			self.comboBox_oggetti_esterno.setEditText(self.DATA_LIST[self.rec_num].oggetti_rinvenuti_esterno)								#11 -  oggetti_rinvenuti_esterno
			self.comboBox_conservazione_taf.setEditText(self.DATA_LIST[self.rec_num].stato_di_conservazione)								#12 - stato_di_conservazione
			self.comboBox_copertura_tipo.setEditText(self.DATA_LIST[self.rec_num].copertura_tipo)											#13 - copertura_tipo
			self.comboBox_tipo_contenitore_resti.setEditText(self.DATA_LIST[self.rec_num].tipo_contenitore_resti)							#14 - tipo contenitore resti tipo_contenitore_resti
			self.lineEdit_orientamento_asse.setText(self.DATA_LIST[self.rec_num].orientamento_asse)											#15 - orientamento asse
			self.comboBox_corredo_presenza.setEditText(str(self.DATA_LIST[self.rec_num].corredo_presenza))									#16 - corredo presenza
			unicode(self.textEdit_descrizione_corredo.setText(self.DATA_LIST[self.rec_num].corredo_descrizione))							#17 - descrizione corredo
			self.comboBox_posizione_scheletro.setEditText(self.DATA_LIST[self.rec_num].posizione_scheletro)									#18 - posizione scheletro
			self.comboBox_posizione_cranio.setEditText(self.DATA_LIST[self.rec_num].posizione_cranio)										#19 - posizione cranio
			self.comboBox_arti_superiori.setEditText(self.DATA_LIST[self.rec_num].posizione_arti_superiori)									#20 - arti superiori
			self.comboBox_arti_inferiori.setEditText(self.DATA_LIST[self.rec_num].posizione_arti_inferiori)									#21 - arti inferiori 
			self.comboBox_completo.setEditText(self.DATA_LIST[self.rec_num].completo_si_no)													#22 - completo
			self.comboBox_disturbato.setEditText(self.DATA_LIST[self.rec_num].disturbato_si_no)												#23 - disturbato
			self.comboBox_in_connessione.setEditText(self.DATA_LIST[self.rec_num].in_connessione_si_no) 									#24 - in connessione
			self.tableInsertData("self.tableWidget_caratteristiche", self.DATA_LIST[self.rec_num].caratteristiche)							#26 - caratteristiche
			self.tableInsertData("self.tableWidget_corredo_tipo", self.DATA_LIST[self.rec_num].corredo_tipo)								#27 - corredo tipo

			#gestione tool
			if self.toolButtonPreview.isChecked() == True:
				self.loadMapPreview()
			if self.toolButtonPreviewMedia.isChecked() == True:
				self.loadMediaPreview()
		except Exception, e:
			QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)

	def set_rec_counter(self, t, c):
		self.rec_tot = t
		self.rec_corr = c
		self.label_rec_tot.setText(str(self.rec_tot))
		self.label_rec_corrente.setText(str(self.rec_corr))

	def set_LIST_REC_TEMP(self):
		## nr scheda
		if self.lineEdit_nr_scheda.text() == "":
			nr_scheda = None
		else:
			nr_scheda = self.lineEdit_nr_scheda.text()

		## nr struttura
		if self.comboBox_nr_struttura.currentText() == "":
			nr_struttura = None
		else:
			nr_struttura = self.comboBox_nr_struttura.currentText()

		## nr individuo
		if self.comboBox_nr_individuo.currentText() == "":
			nr_individuo = None
		else:
			nr_individuo = self.comboBox_nr_individuo.currentText()

		##orientamento azimut
		if self.lineEdit_orientamento_azimut.text() == "":
			orientamento_azimut = None
		else:
			orientamento_azimut =  self.lineEdit_orientamento_azimut.text()

		##lunghezza scheletro
		if self.lineEdit_lunghezza_scheletro.text() == "":
			lunghezza_scheletro = None
		else:
			lunghezza_scheletro = self.lineEdit_lunghezza_scheletro.text()

		#TableWidget

		##Caratteristiche
		caratteristiche = self.table2dict("self.tableWidget_caratteristiche")
		##Corredo tipo
		corredo_tipo = self.table2dict("self.tableWidget_corredo_tipo")

		self.DATA_LIST_REC_TEMP = [
		str(self.comboBox_sito.currentText()), 									#1 - Sito
		str(nr_scheda),															#2 - Nr schede
		str(self.comboBox_sigla_struttura.currentText()),						#3 - Tipo struttura
		str(nr_struttura),														#4 - Nr struttura
		str(nr_individuo),														#5 - Nr individuo
		str(self.comboBox_rito.currentText()),									#6 - Rito
		str(self.textEdit_descrizione_taf.toPlainText().toLatin1()),			#7 - Descrizione tafonimia
		str(self.textEdit_interpretazione_taf.toPlainText().toLatin1()),		#8 - Interpretazione tafonimia
		str(self.comboBox_segnacoli.currentText()),								#9 - Segnacoli
		str(self.comboBox_canale_libatorio.currentText()),						#10 - Canale libatorio
		str(self.comboBox_oggetti_esterno.currentText()),	 					#11 - Oggetti esterno
		str(self.comboBox_conservazione_taf.currentText()), 					#12 - Conservazione tafonomia
		str(self.comboBox_copertura_tipo.currentText()),						#13 - Copertura tipo
		str(self.comboBox_tipo_contenitore_resti.currentText()),				#14 - Tipo contenitore resti  
		str(self.lineEdit_orientamento_asse.text()),							#15 - orientamento asse
		str(orientamento_azimut),												#16 - orientamento azimut
		str(self.comboBox_corredo_presenza.currentText()),						#17 - corredo
		str(corredo_tipo),														#18 - corredo tipo
		str(self.textEdit_descrizione_corredo.toPlainText().toLatin1()),		#19 - descrizione corredo
		str(lunghezza_scheletro),												#20 - lunghezza scheletro
		str(self.comboBox_posizione_scheletro.currentText()),					#21 - posizione scheletro
		str(self.comboBox_posizione_cranio.currentText()),						#22 - posizione cranio
		str(self.comboBox_arti_superiori.currentText()),						#23 - arti superiori
		str(self.comboBox_arti_inferiori.currentText()),						#24 - arti inferiori
		str(self.comboBox_completo.currentText()),								#25 - completo
		str(self.comboBox_disturbato.currentText()),							#26 - disturbato
		str(self.comboBox_in_connessione.currentText()), 						#27 - in connessione
		str(caratteristiche)													#28 - caratteristiche
		]

	def set_LIST_REC_CORR(self):
		self.DATA_LIST_REC_CORR = []
		for i in self.TABLE_FIELDS:
			self.DATA_LIST_REC_CORR.append(eval("str(self.DATA_LIST[self.REC_CORR]." + i + ")"))

	def records_equal_check(self):
		self.set_LIST_REC_TEMP()
		self.set_LIST_REC_CORR()
		#f = open('/test_rec_corr_TAFONOMIA.txt', 'w')
		#test = str(self.DATA_LIST_REC_CORR) + " " + str(self.DATA_LIST_REC_TEMP)
		#f.write(test)
		#f.close()

		if self.DATA_LIST_REC_CORR == self.DATA_LIST_REC_TEMP:
			return 0
		else:
			return 1

	def setComboBoxEditable(self, f, n):
		field_names = f
		value = n

		for fn in field_names:
			cmd = ('%s%s%d%s') % (fn, '.setEditable(', n, ')')
			eval(cmd)

	def setComboBoxEnable(self, f, v):
		field_names = f
		value = v

		for fn in field_names:
			cmd = ('%s%s%s%s') % (fn, '.setEnabled(', v, ')')
			eval(cmd)

	def testing(self, name_file, message):
		f = open(str(name_file), 'w')
		f.write(str(message))
		f.close()

## Class end