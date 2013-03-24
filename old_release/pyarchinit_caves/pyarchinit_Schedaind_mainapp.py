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
try:
	from qgis.core import *
	from qgis.gui import *
except:
	pass

from datetime import date
from psycopg2 import *

#--import pyArchInit modules--#
from  pyarchinit_schedaind_ui import Ui_DialogInd
from  pyarchinit_schedaind_ui import *
from  pyarchinit_utility import *

from  pyarchinit_pyqgis import Pyarchinit_pyqgis
from  sortpanelmain import SortPanelMain
try:
	from  pyarchinit_db_manager import *
except:
	pass

from  pyarchinit_exp_Individui_pdf import *

from delegateComboBox import *



class pyarchinit_Schedaind(QDialog, Ui_DialogInd):
	MSG_BOX_TITLE = "PyArchInit - pyarchinit_US_version 0.4 - Scheda Individuo"
	DATA_LIST = []
	DATA_LIST_REC_CORR = []
	DATA_LIST_REC_TEMP = []
	REC_CORR = 0
	REC_TOT = 0
	BROWSE_STATUS = "b"
	STATUS_ITEMS = {"b": "Usa", "f": "Trova", "n": "Nuovo Record"}
	SORT_MODE = 'asc'
	SORTED_ITEMS = {"n": "Non ordinati", "o": "Ordinati"}
	SORT_STATUS = "n"
	UTILITY = Utility()
	DB_MANAGER = ""
	TABLE_NAME = 'individui_table'
	MAPPER_TABLE_CLASS = "SCHEDAIND"
	NOME_SCHEDA = "Scheda Individuo"
	ID_TABLE = "id_scheda_ind"
	CONVERSION_DICT = {
	ID_TABLE:ID_TABLE,
	"Sito":"sito",
	"US":"us",
	"Area": "area",
	"Nr. Individuo":"nr_individuo",
	"Data Schedatura":"data_schedatura",
	"Schedatore":"schedatore",
	"Stima del sesso":"sesso",
	"Stima dell'eta' di morte min":"eta_min",
	"Stima dell'eta' di morte max":"eta_max",
	"Classi di eta'":"classi_eta",
	"Osservazioni":"osservazioni"
	}
	SORT_ITEMS = [
				ID_TABLE, 
				"Sito",
				"Area",
				"US",
				"Nr. Individuo",
				"Data schedatura",
				"Schedatore",
				"Stima del sesso",
				"Stima dell'eta' di morte min",
				"Stima dell'eta' di morte max",
				"Classi di eta'",
				"Osservazioni" 
				]
				
	TABLE_FIELDS = [
					'sito',
					'area',
					'us',
					'nr_individuo',
					'data_schedatura',
					'schedatore',
					'sesso',
					'eta_min',
					'eta_max',
					'classi_eta',
					'osservazioni'
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
				self.BROWSE_STATUS = "b"
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
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br><br> Tabella non presente. E' NECESSARIO RIAVVIARE QGIS" ,  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br> Errore: <br>" + str(e) ,  QMessageBox.Ok)

	def customize_GUI(self):
		pass
		"""
		self.tableWidget_rapporti.setColumnWidth(0,380)
		self.tableWidget_rapporti.setColumnWidth(1,110)

		self.mapPreview = QgsMapCanvas(self)
		self.mapPreview.setCanvasColor(QColor(225,225,225))
		self.tabWidget.addTab(self.mapPreview, "Piante")
		
		self.setComboBoxEditable(["self.comboBox_per_iniz"],1)
		self.setComboBoxEditable(["self.comboBox_fas_iniz"],1)
		self.setComboBoxEditable(["self.comboBox_per_fin"],1)
		self.setComboBoxEditable(["self.comboBox_fas_fin"],1)
		
		valuesRS = ["Uguale_a", "Si_lega_a", "Copre", "Coperto da", "Riempie", "Riempito da", "Taglia", "Tagliato da", "Si appoggia a", "Gli si appoggia"]
		self.delegateRS = ComboBoxDelegate()
		self.delegateRS.def_values(valuesRS)
		self.tableWidget_rapporti.setItemDelegateForColumn(0,self.delegateRS)

		valuesINCL_CAMP = ["Terra", "Pietre", "Laterzio", "Ciottoli", "Calcare", "Calce", "Carboni", "Concotto", "Ghiaia", "Cariossidi", "Malacofauna", "Sabbia", "Malta"]
		self.delegateINCL_CAMP = ComboBoxDelegate()
		valuesINCL_CAMP.sort()
		self.delegateINCL_CAMP.def_values(valuesINCL_CAMP)
		self.tableWidget_inclusi.setItemDelegateForColumn(0,self.delegateINCL_CAMP)
		self.tableWidget_campioni.setItemDelegateForColumn(0,self.delegateINCL_CAMP)
		"""

	def loadMapPreview(self, mode = 0):
		pass
			


	def charge_list(self):
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))
		try:
			sito_vl.remove('')
		except:
			pass

		self.comboBox_sito.clear()

		sito_vl.sort()
		self.comboBox_sito.addItems(sito_vl)

	def charge_periodo_list(self):
		pass
		"""
		try:
			search_dict = {
			'sito'  : "'"+str(self.comboBox_sito.currentText())+"'",
			}
		
			periodo_vl = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')
		
			periodo_list = []

			for i in range(len(periodo_vl)):
				periodo_list.append(str(periodo_vl[i].periodo))
			try:
				periodo_vl.remove('')
			except:
				pass

			periodo_list.sort()

			self.comboBox_per_iniz.clear()
			self.comboBox_per_iniz.addItems(periodo_list)
			self.comboBox_per_iniz.setEditText(self.DATA_LIST[self.rec_num].periodo_iniziale)
			self.comboBox_per_fin.clear()
			self.comboBox_per_fin.addItems(periodo_list)
			self.comboBox_per_fin.setEditText(self.DATA_LIST[self.rec_num].periodo_finale)
		except:
			pass
		"""

	def charge_fase_iniz_list(self):
		pass
		"""
		try:
			search_dict = {
			'sito'  : "'"+str(self.comboBox_sito.currentText())+"'",
			'periodo'  : "'"+str(self.comboBox_per_iniz.currentText())+"'",
			}
		
			fase_list_vl = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')
		
			fase_list = []

			for i in range(len(fase_list_vl)):
				fase_list.append(str(fase_list_vl[i].fase))
		
			try:
				fase_list.remove('')
			except:
				pass

			self.comboBox_fas_iniz.clear()

			fase_list.sort()
			self.comboBox_fas_iniz.addItems(fase_list)
			self.comboBox_fas_iniz.setEditText(self.DATA_LIST[self.rec_num].fase_iniziale)

		except:
			pass
		"""


	def charge_fase_fin_list(self):
		pass
		"""
		try:
			search_dict = {
			'sito'  : "'"+str(self.comboBox_sito.currentText())+"'",
			'periodo'  : "'"+str(self.comboBox_per_fin.currentText())+"'",
			}

			fase_list_vl = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')

			fase_list = []

			for i in range(len(fase_list_vl)):
				fase_list.append(str(fase_list_vl[i].fase))

			try:
				fase_list.remove('')
			except:
				pass

			self.comboBox_fas_fin.clear()

			fase_list.sort()
			self.comboBox_fas_fin.addItems(fase_list)
			self.comboBox_fas_fin.setEditText(self.DATA_LIST[self.rec_num].fase_finale)

		except:
			pass
		"""


	#buttons functions


	def generate_list_pdf(self):
		data_list = []
		for i in range(len(self.DATA_LIST)):
			data_list.append([
			str(self.DATA_LIST[i].sito),					#1 - Sito
			int(self.DATA_LIST[i].area),					#2 - US
			int(self.DATA_LIST[i].us),		        		#3 - data
			int(self.DATA_LIST[i].nr_individuo),			#4- osservazioni
			str(self.DATA_LIST[i].data_schedatura),			#5 - eta_stima
			str(self.DATA_LIST[i].schedatore),
			str(self.DATA_LIST[i].sesso), 	                #6 - sex_stima
			str(self.DATA_LIST[i].eta_min), 	        			#7 - sex_stima
			str(self.DATA_LIST[i].eta_max),					#8- sex_stima
			str(self.DATA_LIST[i].classi_eta),					#9 - sex_stima
			str(self.DATA_LIST[i].osservazioni)				#10 - sex_stima
		])
		return data_list

	def on_pushButton_pdf_exp_pressed(self):
		Individui_pdf_sheet = generate_pdf()
		data_list = self.generate_list_pdf()
		Individui_pdf_sheet.build_Individui_sheets(data_list)

	"""
	def on_toolButtonPan_toggled(self):
		self.toolPan = QgsMapToolPan(self.mapPreview)
		self.mapPreview.setMapTool(self.toolPan)


	def on_pushButton_showSelectedFeatures_pressed(self):
		pass
		
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
		self.label_status.setText(self.STATUS["usa"])
		if type(self.REC_CORR) == "<type 'str'>":
			corr = 0
		else:
			corr = self.REC_CORR

		self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
		self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
	"""

	#buttons functions
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
		self.BROWSE_STATUS = "b"
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
	"""
	def on_pushButton_addRaster_pressed(self):
		if self.toolButtonGis.isChecked() == True:
			self.pyQGIS.addRasterLayer()
	"""
	def on_pushButton_new_rec_pressed(self):
		#set the GUI for a new record
		if  self.BROWSE_STATUS != "n":
			self.BROWSE_STATUS = "n"
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			self.empty_fields()
			self.label_sort.setText(self.SORTED_ITEMS["n"])

			self.setComboBoxEditable(["self.comboBox_sito"],0)
			self.setComboBoxEnable(["self.comboBox_sito"],"True")
			self.setComboBoxEnable(["self.lineEdit_area"],"True")
			self.setComboBoxEnable(["self.lineEdit_us"],"True")
			self.setComboBoxEnable(["self.lineEdit_individuo"],"True")

			self.set_rec_counter('', '')
			self.enable_button(0)


	def on_pushButton_save_pressed(self):
		#save record
		if self.BROWSE_STATUS == "b":
			if self.records_equal_check() == 1:
				self.update_if(QMessageBox.warning(self,'ATTENZIONE',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
				self.label_sort.setText(self.SORTED_ITEMS["n"])
				self.enable_button(1)
			else:
				QMessageBox.warning(self, "ATTENZIONE", "Non è stata realizzata alcuna modifica.",  QMessageBox.Ok)
		else:
			if self.data_error_check() == 0:
				test_insert = self.insert_new_rec()
				if test_insert == 1:
					self.empty_fields()
					self.label_sort.setText(self.SORTED_ITEMS["n"])
					self.charge_list()
					self.charge_records()
					self.BROWSE_STATUS = "b"
					self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
					self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST)-1
					self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
					self.fill_fields(self.REC_CORR)

					self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
					self.setComboBoxEditable(["self.comboBox_sito"],1)
					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.lineEdit_area"],"False")
					self.setComboBoxEnable(["self.lineEdit_us"],"False")
					self.setComboBoxEnable(["self.lineEdit_individuo"],"False")

					self.enable_button(1)

			else:
				pass

	def data_error_check(self):
		test = 0
		#EC = Error_check()
		#somes check here
		
		return test


	def insert_new_rec(self):

		if self.comboBox_eta_min.currentText() == "":
			eta_min = None
		else:
			eta_min = int(self.comboBox_eta_min.currentText())

		if self.comboBox_eta_max.currentText() == "":
			eta_max = None
		else:
			eta_max = int(self.comboBox_eta_max.currentText())
		
		if self.comboBox_classi_eta.currentText() == "":
			classi_eta = ''
		else:
			classi_eta = str(self.comboBox_classi_eta.currentText())

		try:
			data = self.DB_MANAGER.insert_values_ind(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE)+1,
			str(self.comboBox_sito.currentText()), 				        #1 - Sito
			str(self.lineEdit_area.text()),
			int(self.lineEdit_us.text()),
			int(self.lineEdit_individuo.text()),					        #3 - US
			str(self.lineEdit_data_schedatura.text()),			                #4 - data
			str(self.lineEdit_schedatore.text()),		                        #7 - osservazioni
			str(self.comboBox_sesso.currentText()),								#9 - sex_stima
			eta_min,													#10 - sex_stima
			eta_max,								#11 - sex_stima
			classi_eta,								#11 - sex_stima
			str(self.textEdit_osservazioni.toPlainText())								#12 - sex_stima
			)
			try:
				self.DB_MANAGER.insert_data_session(data)
				return 1
			except Exception, e:
				e_str = str(e)
				if e_str.__contains__("Integrity"):
					msg = self.ID_TABLE + " gia' presente nel database"
				else:
					msg = e
				QMessageBox.warning(self, "Errore", "Attenzione 1 ! \n"+ str(msg),  QMessageBox.Ok)
				return 0
		except Exception, e:
			QMessageBox.warning(self, "Errore", "Attenzione 2 ! \n"+str(e),  QMessageBox.Ok)
			return 0

	#insert new row into tableWidget
	def on_pushButton_insert_row_rapporti_pressed(self):
		self.insert_new_row('self.tableWidget_rapporti')

	def on_pushButton_insert_row_inclusi_pressed(self):
		self.insert_new_row('self.tableWidget_inclusi')

	def on_pushButton_insert_row_campioni_pressed(self):
		self.insert_new_row('self.tableWidget_campioni')

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
		self.label_sort.setText(self.SORTED_ITEMS["n"])


	#records surf functions
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
			except Exception, e:
				QMessageBox.warning(self, "Attenzione", "Il database e' vuoto!" + str(e),  QMessageBox.Ok)

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
		self.label_sort.setText(self.SORTED_ITEMS["n"])


	def on_pushButton_new_search_pressed(self):
		self.enable_button_search(0)
		self.setComboBoxEditable(["self.comboBox_sito"],1)

		#set the GUI for a new search

		if self.BROWSE_STATUS != "f":
			self.BROWSE_STATUS = "f"
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			self.empty_fields()
			self.set_rec_counter('','')
			self.label_sort.setText(self.SORTED_ITEMS["n"])

			self.setComboBoxEditable(["self.comboBox_sito"],1)
			self.setComboBoxEnable(["self.comboBox_sito"],"True")
			self.setComboBoxEnable(["self.lineEdit_area"],"True")
			self.setComboBoxEnable(["self.lineEdit_us"],"True")
			self.setComboBoxEnable(["self.lineEdit_individuo"],"True")


	def on_pushButton_search_go_pressed(self):
		if self.BROWSE_STATUS != "f":
			QMessageBox.warning(self, "ATTENZIONE", "Per eseguire una nuova ricerca clicca sul pulsante 'new search' ",  QMessageBox.Ok)
		else:

			#TableWidget
			
			if self.lineEdit_us.text() != "":
				us = int(self.lineEdit_us.text())
			else:
				us = ""
				
			if self.lineEdit_individuo.text() != "":
				individuo = int(self.lineEdit_individuo.text())
			else:
				individuo = ""
					
			if self.comboBox_eta_min.currentText() != "":
				eta_min = int(self.comboBox_eta_min.currentText())
			else:
				eta_min = ""

			if self.comboBox_eta_max.currentText() != "":
				eta_max = int(self.comboBox_eta_max.currentText())
			else:
				eta_max = ""

			search_dict = {
			self.TABLE_FIELDS[0]  : "'" + str(self.comboBox_sito.currentText())+"'",		#0 - Sito
			self.TABLE_FIELDS[1]  : "'" + str(self.lineEdit_area.text()) + "'",
			self.TABLE_FIELDS[2]  : us,																#2 - US
			self.TABLE_FIELDS[3]  : individuo,                #3 - data
			self.TABLE_FIELDS[4]  : "'" + str(self.lineEdit_data_schedatura.text()) + "'",		        #6 - osservazioni
			self.TABLE_FIELDS[5]  : "'" + str(self.lineEdit_schedatore.text())+"'",		        #7 - eta_stima
			self.TABLE_FIELDS[6]  : "'" + str(self.comboBox_sesso.currentText())+"'",		        #8 - sex_stima
			self.TABLE_FIELDS[7]  : eta_min,						#9 - sex_stima
			self.TABLE_FIELDS[8]  : eta_max,						#10 - sex_stima
			self.TABLE_FIELDS[9]  :  "'" + str(self.comboBox_classi_eta.currentText())+"'",						#10 - sex_stima
			self.TABLE_FIELDS[10]  : str(self.textEdit_osservazioni.toPlainText())		#11 - sex_stima
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

					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.lineEdit_area"],"False")
					self.setComboBoxEnable(["self.lineEdit_us"],"False")
					self.setComboBoxEnable(["self.lineEdit_individuo"],"False")

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
							id_us_list = self.charge_id_us_for_individuo()
							self.pyQGIS.charge_individui_us(id_us_list)
					else:
						strings = ("Sono stati trovati", self.REC_TOT, "records")
						if self.toolButtonGis.isChecked() == True:
							id_us_list = self.charge_id_us_for_individuo()
							self.pyQGIS.charge_individui_us(id_us_list)

					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.lineEdit_area"],"False")
					self.setComboBoxEnable(["self.lineEdit_us"],"False")
					self.setComboBoxEnable(["self.lineEdit_individuo"],"False")

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
		pass
		"""
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
		"""

	def insert_new_row(self, table_name):
		"""insert new row into a table based on table_name"""
		cmd = table_name+".insertRow(0)"
		eval(cmd)


	def empty_fields(self):
		#rapporti_row_count = self.tableWidget_rapporti.rowCount()
		#campioni_row_count = self.tableWidget_campioni.rowCount()
		#inclusi_row_count = self.tableWidget_inclusi.rowCount()

		self.comboBox_sito.setEditText("")  						#1 - Sito
		self.lineEdit_area.clear()							#3 - US
		self.lineEdit_us.clear()							#3 - US
		self.lineEdit_data_schedatura.clear()						        #4 - data
		self.lineEdit_schedatore.clear()						#7 - osservazioni
		self.lineEdit_individuo.clear()						        #8 - eta_stima
		self.comboBox_sesso.setEditText("")						        #9 - sex_stima
		self.comboBox_eta_min.setEditText("")						        #10 - sex_stima
		self.comboBox_eta_max.setEditText("")						        #11 - sex_stima
		self.comboBox_classi_eta.setEditText("")						        #11 - sex_stima
		self.textEdit_osservazioni.clear()					#12 - sex_stima


	def fill_fields(self, n=0):
		self.rec_num = n
		try:
			
			self.comboBox_sito.setEditText(str(self.DATA_LIST[self.rec_num].sito))  				#1 - Sito
			self.lineEdit_area.setText(str(self.DATA_LIST[self.rec_num].area))			#8 - eta_stim
			self.lineEdit_us.setText(str(self.DATA_LIST[self.rec_num].us))
			self.lineEdit_individuo.setText(str(self.DATA_LIST[self.rec_num].nr_individuo))			#8 - eta_stim
			self.lineEdit_data_schedatura.setText(str(self.DATA_LIST[self.rec_num].data_schedatura))				#4 - data
			self.lineEdit_schedatore.setText(str(self.DATA_LIST[self.rec_num].schedatore))			#7 - osservazioni
			self.comboBox_sesso.setEditText(str(self.DATA_LIST[self.rec_num].sesso))			        #9 - sex_stima

			if self.DATA_LIST[self.rec_num].eta_min == None:												#4 - cronologia iniziale
				self.comboBox_eta_min.setEditText("")
			else:
				self.comboBox_eta_min.setEditText(str(self.DATA_LIST[self.rec_num].eta_min))

			if self.DATA_LIST[self.rec_num].eta_max == None:												#4 - cronologia iniziale
				self.comboBox_eta_max.setEditText("")
			else:
				self.comboBox_eta_max.setEditText(str(self.DATA_LIST[self.rec_num].eta_max))

			self.comboBox_classi_eta.setEditText(str(self.DATA_LIST[self.rec_num].classi_eta))

			unicode(self.textEdit_osservazioni.setText(self.DATA_LIST[self.rec_num].osservazioni))		#12 - sex_stima
			if self.toolButtonPreview.isChecked() == True:
				self.loadMapPreview()
		except Exception, e:
			QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)

	def set_rec_counter(self, t, c):
		self.rec_tot = t
		self.rec_corr = c
		self.label_rec_tot.setText(str(self.rec_tot))
		self.label_rec_corrente.setText(str(self.rec_corr))

	def set_LIST_REC_TEMP(self):
		if self.comboBox_eta_min.currentText() == "":
			eta_min = None
		else:
			eta_min = self.comboBox_eta_min.currentText()

		if self.comboBox_eta_max.currentText() == "":
			eta_max = None
		else:
			eta_max = self.comboBox_eta_max.currentText()

		#data
		self.DATA_LIST_REC_TEMP = [
		str(self.comboBox_sito.currentText()),							#1 - Sito
		str(self.lineEdit_area.text()),									#1 - Sito
		str(self.lineEdit_us.text()),									#1 - Sito
		str(self.lineEdit_individuo.text()),							#8 - eta_stima
		str(self.lineEdit_data_schedatura.text()),						#4 - data
		str(self.lineEdit_schedatore.text()),			    		    #7 - osservazioni
		str(self.comboBox_sesso.currentText()),			    		    #9 - sex_stima
		str(eta_min),													#10- sex_stima
		str(eta_max),													#11 - sex_stima
		str(self.comboBox_classi_eta.currentText()),					#11 - sex_stima
		str(self.textEdit_osservazioni.toPlainText().toLatin1())]		#12 - sex_stima

	def set_LIST_REC_CORR(self):
		self.DATA_LIST_REC_CORR = []
		for i in self.TABLE_FIELDS:
			self.DATA_LIST_REC_CORR.append(eval("str(self.DATA_LIST[self.REC_CORR]." + i + ")"))

	def records_equal_check(self):
		self.set_LIST_REC_TEMP()
		self.set_LIST_REC_CORR()

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

	def update_record(self):
		self.DB_MANAGER.update(self.MAPPER_TABLE_CLASS, 
						self.ID_TABLE,
						[eval("int(self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE+")")],
						self.TABLE_FIELDS,
						self.rec_toupdate())

	def rec_toupdate(self):
		rec_to_update = self.UTILITY.pos_none_in_list(self.DATA_LIST_REC_TEMP)

		#f = open('/test_rec_to_update_ind.txt', 'w')
		#f.write(str(rec_to_update))
		#f.close()

		return rec_to_update
	
	def charge_id_us_for_individuo(self):
		data_list_us = []
		for rec in range(len(self.DATA_LIST)):
			sito = "'"+str(self.DATA_LIST[rec].sito)+"'"
			area = "'"+str(self.DATA_LIST[rec].area)+"'"
			us = int(self.DATA_LIST[rec].us)
			
			serch_dict_us = {'sito': sito, 'area': area, 'us': us}
			us_ind = self.DB_MANAGER.query_bool(serch_dict_us, "US")
			data_list_us.append(us_ind)
		
		data_list_id_us = []
		for us in range(len(data_list_us)):
			data_list_id_us.append(data_list_us[us][0].id_us)
		
		return data_list_id_us

	def testing(self, name_file, message):
		f = open(str(name_file), 'w')
		f.write(str(message))
		f.close()
		
		
		
		

## Class end
