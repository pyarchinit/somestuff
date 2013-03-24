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
from  pyarchinit_Ipogei_ui import Ui_DialogIpogei
from  pyarchinit_Ipogei_ui import *
from  pyarchinit_utility import *
from  pyarchinit_error_check import *
from  pyarchinit_pyqgis import Pyarchinit_pyqgis

try:
	from  pyarchinit_db_manager import *
except:
	pass

from  sortpanelmain import SortPanelMain
from delegateComboBox import *

class pyarchinit_Ipogei(QDialog, Ui_DialogIpogei):
	MSG_BOX_TITLE = "PyArchInit - Scheda Ipogeo"
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
	TABLE_NAME = 'ipogeo_table'
	MAPPER_TABLE_CLASS = 'IPOGEO'
	NOME_SCHEDA = "Scheda Ipogeo"
	ID_TABLE = "id_ipogeo"
	CONVERSION_DICT = {
	ID_TABLE:ID_TABLE,
	"Sito ipogeo":"sito_ipogeo",
	"Sigla ipogeo":"sigla_ipogeo",
	"Numero ipogeo":"numero_ipogeo",
	"Categoria ipogeo":"categoria_ipogeo",
	"Tipologia ipogeo":"tipologia_ipogeo",
	"Definizione ipogeo":"definizione_ipogeo",
	"Descrizione ipogeo":"descrizione_ipogeo",
	"Interpretazione ipogeo":"interpretazione_ipogeo",
	"Periodo iniziale ipogeo":"periodo_iniziale_ipogeo",
	"Fase iniziale ipogeo":"fase_iniziale_ipogeo",
	"Periodo finale ipogeo":"periodo_finale_ipogeo",
	"Fase_finale ipogeo":"fase_finale_ipogeo",
	"Datazione estesa ipogeo":"datazione_estesa_ipogeo",
        "Percentuale umidita ipogeo":"percentuale_umidita_ipogeo",
        "Grado conservazione ipogeo":"grado_conservazione_ipogeo",
        "Grado staticita ipogeo":"grado_staticita_ipogeo"
	}
	SORT_ITEMS = [
				ID_TABLE,
				"Sito ipogeo",
				"Sigla ipogeo",
				"Numero ipogeo",
				"Categoria ipogeo",
				"Tipologia ipogeo",
				"Definizione ipogeo",
				"Descrizione ipogeo",
				"Interpretazione ipogeo",
				"Periodo iniziale ipogeo",
				"Fase iniziale ipogeo",
				"Periodo finale ipogeo",
				"Fase_finale ipogeo",
				"Datazione estesa ipogeo",
                                "Percentuale umidita ipogeo",
                                "Grado conservazione ipogeo",
                                "Grado staticita ipogeo"
				]

	TABLE_FIELDS = [
					"sito_ipogeo",
					"sigla_ipogeo",
					"numero_ipogeo",
					"categoria_ipogeo",
					"tipologia_ipogeo",
					"definizione_ipogeo",
					"descrizione_ipogeo",
					"interpretazione_ipogeo",
					"periodo_iniziale_ipogeo",
					"fase_iniziale_ipogeo",
					"periodo_finale_ipogeo",
					"fase_finale_ipogeo",
					"datazione_estesa_ipogeo",
					"materiali_impiegati_ipogeo",
					"elementi_strutturali_ipogeo",
					"rapporti_ipogeo",
					"misure_ipogeo",
                                        "percentuale_umidita_ipogeo",
                                        "grado_conservazione_ipogeo",
                                        "grado_staticita_ipogeo"
					]

	def __init__(self, iface):
		self.iface = iface
		self.pyQGIS = Pyarchinit_pyqgis(self.iface)

		QDialog.__init__(self)
		self.setupUi(self)
		self.customize_GUI()
		self.currentLayerId = None


		try:
			self.on_pushButton_connect_pressed()
		except:
			pass

		#SIGNALS & SLOTS Functions
		
		self.connect(self.comboBox_sigla_ipogeo, SIGNAL("editTextChanged (const QString&)"), self.add_value_to_categoria)
		self.connect(self.comboBox_sito_ipogeo, SIGNAL("editTextChanged (const QString&)"), self.charge_periodo_list)
		self.connect(self.comboBox_per_iniz_ipogeo, SIGNAL("currentIndexChanged(int)"), self.charge_fase_iniz_list)
		self.connect(self.comboBox_per_fin_ipogeo, SIGNAL("currentIndexChanged(int)"), self.charge_fase_fin_list)
		
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
				QMessageBox.warning(self, "Alert", "La connessione e' fallita" + str(e) + "<br>Tabella non presente. E' NECESSARIO RIAVVIARE QGIS" ,  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br> Errore: <br>" + str(e) ,  QMessageBox.Ok)

	def customize_GUI(self):
		self.tableWidget_rapporti_ipogeo.setColumnWidth(0,120)
		self.tableWidget_rapporti_ipogeo.setColumnWidth(1,280)
		self.tableWidget_rapporti_ipogeo.setColumnWidth(2,75)
		self.tableWidget_rapporti_ipogeo.setColumnWidth(3,75)

		self.tableWidget_materiali_impiegati_ipogeo.setColumnWidth(0,535)

		self.tableWidget_elementi_strutturali_ipogeo.setColumnWidth(0,480)
		self.tableWidget_elementi_strutturali_ipogeo.setColumnWidth(1,60)

		self.tableWidget_misurazioni_ipogeo.setColumnWidth(0,360)
		self.tableWidget_misurazioni_ipogeo.setColumnWidth(1,100)
		self.tableWidget_misurazioni_ipogeo.setColumnWidth(2,60)

		self.setComboBoxEditable(["self.comboBox_per_iniz_ipogeo"],1)
		self.setComboBoxEditable(["self.comboBox_fas_iniz_ipogeo"],1)
		self.setComboBoxEditable(["self.comboBox_per_fin_ipogeo"],1)
		self.setComboBoxEditable(["self.comboBox_fas_fin_ipogeo"],1)
		self.setComboBoxEditable(["self.comboBox_percentuale_umidita_ipogeo"],1)
		self.setComboBoxEditable(["self.comboBox_grado_conservazione_ipogeo"],1)
		self.setComboBoxEditable(["self.comboBox_grado_staticita_ipogeo"],1)

		valuesRapporti = ['Si appoggia a', 'Gli si appoggia' 'Connesso con', 'Si sovrappone a', 'Gli si sovrappone', 'Ampliato da', 'Amplia']
		self.delegateRapporti = ComboBoxDelegate()
		self.delegateRapporti.def_values(valuesRapporti)
		self.delegateRapporti.def_editable('True')
		self.tableWidget_rapporti_ipogeo.setItemDelegateForColumn(0,self.delegateRapporti)
		

		valuesMateriali = ["Terra", "Pietre", "Laterizio", "Ciottoli", "Calcare", "Calce", "Legno", "Concotto", "Ghiaia", "Sabbia", "Malta", "Metallo", "Gesso"]
		self.delegateMateriali = ComboBoxDelegate()
		self.delegateMateriali.def_values(valuesMateriali)
		self.delegateMateriali.def_editable('False')
		self.tableWidget_materiali_impiegati_ipogeo.setItemDelegateForColumn(0,self.delegateMateriali)




	def charge_list(self):
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))

		try:
			sito_vl.remove('')
		except:
			pass
		self.comboBox_sito_ipogeo.clear()
		sito_vl.sort()
		self.comboBox_sito_ipogeo.addItems(sito_vl)

	def charge_periodo_list(self):
		try:
			search_dict = {
			'sito'  : "'"+str(self.comboBox_sito_ipogeo.currentText())+"'",
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

			self.comboBox_per_iniz_ipogeo.clear()
			self.comboBox_per_iniz_ipogeo.addItems(periodo_list)
			self.comboBox_per_iniz_ipogeo.setEditText(self.DATA_LIST[self.rec_num].periodo_iniziale_ipogeo)
			self.comboBox_per_fin_ipogeo.clear()
			self.comboBox_per_fin_ipogeo.addItems(periodo_list)
			self.comboBox_per_fin_ipogeo.setEditText(self.DATA_LIST[self.rec_num].periodo_finale_ipogeo)
		except:
			pass

	def charge_fase_iniz_list(self):
		try:
			search_dict = {
			'sito'  : "'"+str(self.comboBox_sito_ipogeo.currentText())+"'",
			'periodo'  : "'"+str(self.comboBox_per_iniz_ipogeo.currentText())+"'",
			}

			fase_list_vl = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')

			fase_list = []

			for i in range(len(fase_list_vl)):
				fase_list.append(str(fase_list_vl[i].fase))

			try:
				fase_list.remove('')
			except:
				pass

			self.comboBox_fas_iniz_ipogeo.clear()

			fase_list.sort()
			self.comboBox_fas_iniz_ipogeo.addItems(fase_list)
			self.comboBox_fas_iniz_ipogeo.setEditText(self.DATA_LIST[self.rec_num].fase_iniziale_ipogeo)

		except:
			pass


	def charge_fase_fin_list(self):
		try:
			search_dict = {
			'sito'  : "'"+str(self.comboBox_sito_ipogeo.currentText())+"'",
			'periodo'  : "'"+str(self.comboBox_per_fin_ipogeo.currentText())+"'",
			}

			fase_list_vl = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')

			fase_list = []

			for i in range(len(fase_list_vl)):
				fase_list.append(str(fase_list_vl[i].fase))

			try:
				fase_list.remove('')
			except:
				pass

			self.comboBox_fas_fin_ipogeo.clear()

			fase_list.sort()
			self.comboBox_fas_fin_ipogeo.addItems(fase_list)
			self.comboBox_fas_fin_ipogeo.setEditText(self.DATA_LIST[self.rec_num].fase_finale_ipogeo)

		except:
			pass



	#buttons functions
	def on_pushButton_sort_pressed(self):
		dlg = SortPanelMain(self)
		dlg.insertItems(self.SORT_ITEMS)
		dlg.exec_()

		items,order_type = dlg.ITEMS, dlg.TYPE_ORDER

		items_converted = []
		for i in items:
			items_converted.append(self.CONVERSION_DICT[i])

		self.SORT_MODE = order_type
		self.empty_fields()

		id_list = []
		for i in self.DATA_LIST:
			id_list.append(eval("i." + self.ID_TABLE))
		self.DATA_LIST = []

		temp_data_list = self.DB_MANAGER.query_sort(id_list, items_converted, order_type, self.MAPPER_TABLE_CLASS, self.ID_TABLE)

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
		self.label_sort.setText(self.SORTED_ITEMS["o"])
		self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.fill_fields()

	def add_value_to_categoria(self):
		if str(self.comboBox_sigla_ipogeo.currentText()) == 'Aggiungi un valore...':
			self.setComboBoxEditable(["self.comboBox_sigla_ipogeo"],1)


	def on_pushButton_new_rec_pressed(self):
		
		#set the GUI for a new record
		if self.BROWSE_STATUS != "n":
			self.BROWSE_STATUS = "n"
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			self.empty_fields()
			self.label_sort.setText(self.SORTED_ITEMS["n"])

			self.setComboBoxEditable(["self.comboBox_sito_ipogeo"],1)
			self.setComboBoxEditable(["self.comboBox_sigla_ipogeo"],1)
			self.setComboBoxEditable(["self.comboBox_percentuale_umidita_ipogeo"],1)
			self.setComboBoxEditable(["self.comboBox_grado_conservazione_ipogeo"],1)
			self.setComboBoxEditable(["self.comboBox_grado_staticita_ipogeo"],1)
			self.setComboBoxEnable(["self.comboBox_sito_ipogeo"],True)
			self.setComboBoxEnable(["self.comboBox_sigla_ipogeo"],True)
			self.setComboBoxEnable(["self.numero_ipogeo"],True)
			self.setComboBoxEnable(["self.comboBox_percentuale_umidita_ipogeo"],True)
			self.setComboBoxEnable(["self.comboBox_grado_conservazione_ipogeo"],True)
			self.setComboBoxEnable(["self.comboBox_grado_staticita_ipogeo"],True)

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
			#if self.data_error_check() == 0:

			self.insert_new_rec()

			self.empty_fields()
			self.label_sort.setText(self.SORTED_ITEMS["n"])
			self.charge_list()
			self.charge_records()
			self.BROWSE_STATUS = "b"
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST)-1
			self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
			self.fill_fields(self.REC_CORR)

			self.setComboBoxEditable(["self.comboBox_sito_ipogeo"],1)
			self.setComboBoxEditable(["self.comboBox_sigla_ipogeo"],1)
			self.setComboBoxEditable(["self.comboBox_percentuale_umidita_ipogeo"],1)
			self.setComboBoxEditable(["self.comboBox_grado_conservazione_ipogeo"],1)
			self.setComboBoxEditable(["self.comboBox_grado_staticita_ipogeo"],1)
			self.setComboBoxEnable(["self.comboBox_sito_ipogeo"],"False")
			self.setComboBoxEnable(["self.comboBox_sigla_ipogeo"],"False")
			self.setComboBoxEnable(["self.comboBox_percentuale_umidita_ipogeo"],"False")
			self.setComboBoxEnable(["self.comboBox_grado_conservazione_ipogeo"],"False")
			self.setComboBoxEnable(["self.comboBox_grado_staticita_ipogeo"],"False")
			self.setComboBoxEnable(["self.numero_ipogeo"],"False")
			self.enable_button(1)
		
				
	"""
	def data_error_check(self):
		test = 0
		EC = Error_check()

		cron_iniz = self.lineEdit_cron_iniz.text()
		cron_fin = self.lineEdit_cron_fin.text()
		if cron_iniz != "":
			if EC.data_is_int(cron_iniz) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Cronologia Iniziale. \n Il valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		if cron_fin != "":
			if EC.data_is_int(cron_fin) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Cronologia Finale. \n Il valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1


		return test
	"""

	def insert_new_rec(self):

		#TableWidget
		##Materiali_impiegati
		materiali_impiegati_ipogeo = self.table2dict("self.tableWidget_materiali_impiegati_ipogeo")
		##Elementi_strutturali
		elementi_strutturali_ipogeo = self.table2dict("self.tableWidget_elementi_strutturali_ipogeo")
		##Rapporti_struttura
		rapporti_ipogeo = self.table2dict("self.tableWidget_rapporti_ipogeo")
		##Misurazioni
		misurazioni_ipogeo = self.table2dict("self.tableWidget_misurazioni_ipogeo")

		try:
			if self.comboBox_per_iniz_ipogeo.currentText() == "":
				per_iniz = None
			else:
				per_iniz = int(self.comboBox_per_iniz_ipogeo.currentText())

			if self.comboBox_fas_iniz_ipogeo.currentText() == "":
				fas_iniz = None
			else:
				fas_iniz = int(self.comboBox_fas_iniz_ipogeo.currentText())

			if self.comboBox_per_fin_ipogeo.currentText() == "":
				per_fin = None
			else:
				per_fin = int(self.comboBox_per_fin_ipogeo.currentText())

			if self.comboBox_fas_fin_ipogeo.currentText() == "":
				fas_fin = None
			else:
				fas_fin = int(self.comboBox_fas_fin_ipogeo.currentText())
				
			if self.comboBox_percentuale_umidita_ipogeo.currentText() == "":
			        percentuale_umidita_ipogeo = None
		        else:
			        percentuale_umidita_ipogeo = float(self.comboBox_percentuale_umidita_ipogeo.currentText())

			if self.comboBox_grado_conservazione_ipogeo.currentText() == "":
				grado_conservazione_ipogeo = None
			else:
				grado_conservazione_ipogeo = int(self.comboBox_grado_conservazione_ipogeo.currentText())

			if self.comboBox_grado_staticita_ipogeo.currentText() == "":
				grado_staticita_ipogeo = None
			else:
				grado_staticita_ipogeo = int(self.comboBox_grado_staticita_ipogeo.currentText())


			data = self.DB_MANAGER.insert_ipogeo_values(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE)+1, #0
			str(self.comboBox_sito_ipogeo.currentText()), 								#1 - Sito
			str(self.comboBox_sigla_ipogeo.currentText()), 					#2 - sigla_struttura
			int(self.numero_ipogeo.text()), 									#3 - numero_struttura
			str(self.comboBox_categoria_ipogeo.currentText()), 				#4 - categoria_struttura
			str(self.comboBox_tipologia_ipogeo.currentText()), 				#5 - tipologia_struttura
			str(self.comboBox_definizione_ipogeo.currentText()), 			#6 - definizione_struttura
			unicode(self.descrizione_ipogeo.toPlainText()),			#7 - descrizione
			unicode(self.textEdit_interpretazione_ipogeo.toPlainText()),		#8 - interpretazione
			per_iniz,															#9 - periodo iniziale
			fas_iniz,															#10 - fase iniziale
			per_fin, 															#11 - periodo finale iniziale
			fas_fin, 															#12 - fase finale
			str(self.lineEdit_datazione_estesa_ipogeo.text()),							#13 - datazione estesa
			str(materiali_impiegati_ipogeo),											#14 - materiali impiegati
			str(elementi_strutturali_ipogeo),											#15 - elementi_strutturali
			str(rapporti_ipogeo),											#16 - rapporti struttura
			str(misurazioni_ipogeo),													#17 - misurazioni
			percentuale_umidita_ipogeo,
			grado_conservazione_ipogeo,
			grado_staticita_ipogeo)

			try:
				self.DB_MANAGER.insert_data_session(data)

			except Exception, e:
				e_str = str(e)
				if e_str.__contains__("Integrity"):
					msg = self.ID_TABLE + " gia' presente nel database"
				else:
					msg = e
				QMessageBox.warning(self, "Errore", "immisione 1 \n"+ str(msg),  QMessageBox.Ok)
		except Exception, e:
			QMessageBox.warning(self, "Errore", "Errore di immissione 2 \n"+str(e),  QMessageBox.Ok)

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
		self.label_sort.setText(self.SORTED_ITEMS["n"])

	def on_pushButton_new_search_pressed(self):
		self.enable_button_search(0)
		
		self.setComboBoxEditable(["self.comboBox_sito_ipogeo"],1)

		#set the GUI for a new search
		if self.BROWSE_STATUS != "f":
			self.BROWSE_STATUS = "f"
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			self.empty_fields()
			self.set_rec_counter('','')
			self.label_sort.setText(self.SORTED_ITEMS["n"])

			self.setComboBoxEditable(["self.comboBox_sito_ipogeo"],1)
			self.setComboBoxEditable(["self.comboBox_sigla_ipogeo"],1)
			self.setComboBoxEditable(["self.comboBox_percentuale_umidita_ipogeo"],1)
			self.setComboBoxEditable(["self.comboBox_grado_conservazione_ipogeo"],1)
			self.setComboBoxEditable(["self.comboBox_grado_staticita_ipogeo"],1)
			self.setComboBoxEnable(["self.comboBox_sito_ipogeo"],True)
			self.setComboBoxEnable(["self.comboBox_sigla_ipogeo"],True)
			self.setComboBoxEnable(["self.comboBox_percentuale_umidita_ipogeo"],True)
			self.setComboBoxEnable(["self.comboBox_grado_conservazione_ipogeo"],True)
			self.setComboBoxEnable(["self.comboBox_grado_staticita_ipogeo"],True)
			self.setComboBoxEnable(["self.numero_ipogeo"],True)

	def on_pushButton_search_go_pressed(self):
		if self.BROWSE_STATUS != "f":
			QMessageBox.warning(self, "ATTENZIONE", "Per eseguire una nuova ricerca clicca sul pulsante 'new search' ",  QMessageBox.Ok)
		else:
			if self.numero_ipogeo.text() != "":
				numero_ipogeo = int(self.numero_ipogeo.text())
			else:
				numero_ipogeo = ""

			if self.comboBox_per_iniz_ipogeo.currentText() != "":
				periodo_iniziale_ipogeo = int(self.comboBox_per_iniz_ipogeo.currentText())
			else:
				periodo_iniziale_ipogeo = ""

			if self.comboBox_fas_iniz_ipogeo.currentText() != "":
				fase_iniziale_ipogeo = int(self.comboBox_fas_iniz_ipogeo.currentText())
			else:
				fase_iniziale_ipogeo = ""

			if self.comboBox_per_fin_ipogeo.currentText() != "":
				periodo_finale_ipogeo = int(self.comboBox_per_fin_ipogeo.currentText())
			else:
				periodo_finale_ipogeo = ""

			if self.comboBox_fas_fin_ipogeo.currentText() != "":
				fase_finale_ipogeo = int(self.comboBox_fas_fin_ipogeo.currentText())
			else:
				fase_finale_ipogeo = ""

			if self.comboBox_percentuale_umidita_ipogeo.currentText() != "":
				percentuale_umidita_ipogeo = float(self.comboBox_percentuale_umidita_ipogeo.currentText())
			else:
				percentuale_umidita_ipogeo = ""

			if self.comboBox_grado_conservazione_ipogeo.currentText() != "":
				grado_conservazione_ipogeo = int(self.comboBox_grado_conservazione_ipogeo.currentText())
			else:
				grado_conservazione_ipogeo = ""

			if self.comboBox_grado_staticita_ipogeo.currentText() != "":
				grado_staticita_ipogeo = int(self.comboBox_grado_staticita_ipogeo.currentText())
			else:
				grado_staticita_ipogeo = ""

			search_dict = {
			self.TABLE_FIELDS[0] : "'"+str(self.comboBox_sito_ipogeo.currentText())+"'",				#1 - Sito
			self.TABLE_FIELDS[1] : "'"+str(self.comboBox_sigla_ipogeo.currentText())+"'", #1 - Sigla struttura
			self.TABLE_FIELDS[2] : numero_ipogeo, #3 numero struttura
			self.TABLE_FIELDS[3] : "'"+str(self.comboBox_categoria_ipogeo.currentText())+"'",
			self.TABLE_FIELDS[4] : "'"+str(self.comboBox_tipologia_ipogeo.currentText())+"'",
			self.TABLE_FIELDS[5] : "'"+str(self.comboBox_definizione_ipogeo.currentText())+"'",
			self.TABLE_FIELDS[6] : str(self.descrizione_ipogeo.toPlainText()),
			self.TABLE_FIELDS[7] : str(self.textEdit_interpretazione_ipogeo.toPlainText()),
			self.TABLE_FIELDS[8] : periodo_iniziale_ipogeo,
			self.TABLE_FIELDS[9] : fase_iniziale_ipogeo,
			self.TABLE_FIELDS[10] : periodo_finale_ipogeo,
			self.TABLE_FIELDS[11] : fase_finale_ipogeo,
			self.TABLE_FIELDS[12] : str(self.lineEdit_datazione_estesa_ipogeo.text()),
                        self.TABLE_FIELDS[17] : percentuale_umidita_ipogeo,
                        self.TABLE_FIELDS[18] : grado_conservazione_ipogeo,
                        self.TABLE_FIELDS[19] : grado_staticita_ipogeo
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

					self.setComboBoxEditable(["self.comboBox_sito_ipogeo"],0)
					self.setComboBoxEditable(["self.comboBox_sigla_ipogeo"],0)
					self.setComboBoxEditable(["self.comboBox_percentuale_umidita_ipogeo"],0)
					self.setComboBoxEditable(["self.comboBox_grado_conservazione_ipogeo"],0)
					self.setComboBoxEditable(["self.comboBox_grado_staticita_ipogeo"],0)
					self.setComboBoxEnable(["self.comboBox_sito_ipogeo"],"True")
					self.setComboBoxEnable(["self.comboBox_sigla_ipogeo"],"True")
					self.setComboBoxEnable(["self.comboBox_percentuale_umidita_ipogeo"],"True")
					self.setComboBoxEnable(["self.comboBox_grado_conservazione_ipogeo"],"True")
					self.setComboBoxEnable(["self.comboBox_grado_staticita_ipogeo"],"True")
					self.setComboBoxEnable(["self.numero_ipogeo"],"True")

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
					else:
						strings = ("Sono stati trovati", self.REC_TOT, "records")

					self.setComboBoxEditable(["self.comboBox_sito_ipogeo"],1)
					self.setComboBoxEditable(["self.comboBox_sigla_ipogeo"],1)
					self.setComboBoxEditable(["self.comboBox_percentuale_umidita_ipogeo"],1)
					self.setComboBoxEditable(["self.comboBox_grado_conservazione_ipogeo"],1)
					self.setComboBoxEditable(["self.comboBox_grado_staticita_ipogeo"],1)
					self.setComboBoxEnable(["self.comboBox_sito_ipogeo"],"False")
					self.setComboBoxEnable(["self.comboBox_sigla_ipogeo"],"False")
					self.setComboBoxEnable(["self.comboBox_percentuale_umidita_ipogeo"],"False")
					self.setComboBoxEnable(["self.comboBox_grado_conservazione_ipogeo"],"False")
					self.setComboBoxEnable(["self.comboBox_grado_staticita_ipogeo"],"False")
					self.setComboBoxEnable(["self.numero_ipogeo"],"False")

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
				#self.testing('test_sort.txt', 'qua')
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
		id_list = []
		self.DATA_LIST = []

		for i in self.DB_MANAGER.query(eval(self.MAPPER_TABLE_CLASS)):
			id_list.append(eval("i." + self.ID_TABLE))

		temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], 'asc', self.MAPPER_TABLE_CLASS, self.ID_TABLE)
		for i in temp_data_list:
			self.DATA_LIST.append(i)


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
				if bool(value) == True:
					sub_list.append(str(value.text()))
			lista.append(sub_list)
		return lista

	def empty_fields(self):

		materiali_impiegati_row_count = self.tableWidget_materiali_impiegati_ipogeo.rowCount()
		elementi_strutturali_row_count = self.tableWidget_elementi_strutturali_ipogeo.rowCount()
		rapporti_ipogeo_row_count = self.tableWidget_rapporti_ipogeo.rowCount()
		misurazioni_row_count = self.tableWidget_misurazioni_ipogeo.rowCount()

		self.comboBox_sito_ipogeo.setEditText("") 								#1 - Sito
		self.comboBox_sigla_ipogeo.setEditText("")					#2 - sigla_struttura
		self.numero_ipogeo.clear()									#3 - numero_struttura
		self.comboBox_categoria_ipogeo.setEditText("") 				#4 - categoria_struttura
		self.comboBox_tipologia_ipogeo.setEditText("") 				#5 - tipologia_struttura
		self.comboBox_definizione_ipogeo.setEditText("") 			#6 - definizione_struttura
		self.descrizione_ipogeo.clear()						#7 - descrizione
		self.textEdit_interpretazione_ipogeo.clear()					#8 - interpretazione
		self.comboBox_per_iniz_ipogeo.setEditText("")							#9 - periodo iniziale
		self.comboBox_fas_iniz_ipogeo.setEditText("")							#10 - fase iniziale
		self.comboBox_per_fin_ipogeo.setEditText("")							#11 - periodo finale iniziale
		self.comboBox_fas_fin_ipogeo.setEditText("")							#12 - fase finale
                self.comboBox_percentuale_umidita_ipogeo.setEditText("")
                self.comboBox_grado_conservazione_ipogeo.setEditText("")
                self.comboBox_grado_staticita_ipogeo.setEditText("")
		self.lineEdit_datazione_estesa_ipogeo.clear()							#13 - datazione estesa

		for i in range(materiali_impiegati_row_count):
			self.tableWidget_materiali_impiegati_ipogeo.removeRow(0)
		self.insert_new_row("self.tableWidget_materiali_impiegati_ipogeo")		#16 - materiali impiegati

		for i in range(elementi_strutturali_row_count):
			self.tableWidget_elementi_strutturali_ipogeo.removeRow(0)
		self.insert_new_row("self.tableWidget_elementi_strutturali_ipogeo")	#15 - elementi_strutturali

		for i in range(rapporti_ipogeo_row_count):
			self.tableWidget_rapporti_ipogeo.removeRow(0)
		self.insert_new_row("self.tableWidget_rapporti_ipogeo")				#16 - rapporti struttura

		for i in range(misurazioni_row_count):
			self.tableWidget_misurazioni_ipogeo.removeRow(0)
		self.insert_new_row("self.tableWidget_misurazioni_ipogeo")				#17 - rapporti struttura

	def fill_fields(self, n=0):
		self.rec_num = n
		f=open("test_ipogei.txt","w")
		f.write(str(self.rec_num))
		f.close()

		if str(self.DATA_LIST[self.rec_num].periodo_iniziale_ipogeo) == 'None':
			periodo_iniziale_ipogeo = ''
		else:
			periodo_iniziale_ipogeo = str(self.DATA_LIST[self.rec_num].periodo_iniziale_ipogeo)

		if str(self.DATA_LIST[self.rec_num].fase_iniziale_ipogeo) == 'None':
			fase_iniziale_ipogeo = ''
		else:
			fase_iniziale_ipogeo = str(self.DATA_LIST[self.rec_num].fase_iniziale_ipogeo)

		if str(self.DATA_LIST[self.rec_num].periodo_finale_ipogeo) == 'None':
			periodo_finale_ipogeo = ''
		else:
			periodo_finale_ipogeo = str(self.DATA_LIST[self.rec_num].periodo_finale_ipogeo)

		if str(self.DATA_LIST[self.rec_num].fase_finale_ipogeo) == 'None':
			fase_finale_ipogeo = ''
		else:
			fase_finale_ipogeo = str(self.DATA_LIST[self.rec_num].fase_finale_ipogeo)

		if str(self.DATA_LIST[self.rec_num].percentuale_umidita_ipogeo) == 'None':
			percentuale_umidita_ipogeo = ''
		else:
			percentuale_umidita_ipogeo = str(self.DATA_LIST[self.rec_num].percentuale_umidita_ipogeo)

		if str(self.DATA_LIST[self.rec_num].grado_conservazione_ipogeo) == 'None':
			grado_conservazione_ipogeo = ''
		else:
			grado_conservazione_ipogeo = str(self.DATA_LIST[self.rec_num].grado_conservazione_ipogeo)			

		if str(self.DATA_LIST[self.rec_num].grado_staticita_ipogeo) == 'None':
			grado_staticita_ipogeo = ''
		else:
			grado_staticita_ipogeo = str(self.DATA_LIST[self.rec_num].grado_staticita_ipogeo)
		try:
			self.comboBox_sito_ipogeo.setEditText(self.DATA_LIST[self.rec_num].sito_ipogeo)											#1 - Sito
			self.comboBox_sigla_ipogeo.setEditText(str(self.DATA_LIST[self.rec_num].sigla_ipogeo)) 				#2 - Periodo
			self.numero_ipogeo.setText(str(self.DATA_LIST[self.rec_num].numero_ipogeo)) 							#3 - Fase
			self.comboBox_categoria_ipogeo.setEditText(str(self.DATA_LIST[self.rec_num].categoria_ipogeo))			#4 - Fase
			self.comboBox_tipologia_ipogeo.setEditText(str(self.DATA_LIST[self.rec_num].tipologia_ipogeo))		#5 - tipologia_struttura
			self.comboBox_definizione_ipogeo.setEditText(str(self.DATA_LIST[self.rec_num].definizione_ipogeo)) 	#6 - definizione_struttura
			unicode(self.descrizione_ipogeo.setText(self.DATA_LIST[self.rec_num].descrizione_ipogeo))						#6 - descrizione
			unicode(self.textEdit_interpretazione_ipogeo.setText(self.DATA_LIST[self.rec_num].interpretazione_ipogeo))				#7 - interpretazione
			self.comboBox_per_iniz_ipogeo.setEditText(periodo_iniziale_ipogeo)												#8 - periodo iniziale
			self.comboBox_fas_iniz_ipogeo.setEditText(fase_iniziale_ipogeo)										#9 - fase iniziale
			self.comboBox_per_fin_ipogeo.setEditText(periodo_finale_ipogeo)								#10 - periodo finale iniziale
			self.comboBox_fas_fin_ipogeo.setEditText(fase_finale_ipogeo)								#11 - fase finale
			self.lineEdit_datazione_estesa_ipogeo.setText(str(self.DATA_LIST[self.rec_num].datazione_estesa_ipogeo))					#12 - datazione estesa
			self.tableInsertData("self.tableWidget_materiali_impiegati_ipogeo", self.DATA_LIST[self.rec_num].materiali_impiegati_ipogeo)			#13 - inclusi
			self.tableInsertData("self.tableWidget_elementi_strutturali_ipogeo", self.DATA_LIST[self.rec_num].elementi_strutturali_ipogeo)		#14 - inclusi
			self.tableInsertData("self.tableWidget_rapporti_ipogeo", self.DATA_LIST[self.rec_num].rapporti_ipogeo)		#15 - inclusi
			self.tableInsertData("self.tableWidget_misurazioni_ipogeo", self.DATA_LIST[self.rec_num].misure_ipogeo)			#16 - inclusi
 			self.comboBox_percentuale_umidita_ipogeo.setEditText(percentuale_umidita_ipogeo)												#8 - periodo iniziale
			self.comboBox_grado_conservazione_ipogeo.setEditText(grado_conservazione_ipogeo)										#9 - fase iniziale
			self.comboBox_grado_staticita_ipogeo.setEditText(grado_staticita_ipogeo)	                       
		except Exception, e:
			QMessageBox.warning(self, "Errore Fill Fields", "Problema di riempimento campi" + str(e),  QMessageBox.Ok)

	def set_rec_counter(self, t, c):
		self.rec_tot = t
		self.rec_corr = c
		self.label_rec_tot.setText(str(self.rec_tot))
		self.label_rec_corrente.setText(str(self.rec_corr))

	def set_LIST_REC_TEMP(self):
		#data

		if self.numero_ipogeo.text() != "":
			numero_ipogeo = self.numero_ipogeo.text()
		else:
			numero_ipogeo = 'None'

		if self.comboBox_per_iniz_ipogeo.currentText() != "":
			periodo_iniziale_ipogeo = self.comboBox_per_iniz_ipogeo.currentText()
		else:
			periodo_iniziale_ipogeo = 'None'

		if self.comboBox_fas_iniz_ipogeo.currentText() != "":
			fase_iniziale_ipogeo = self.comboBox_fas_iniz_ipogeo.currentText()
		else:
			fase_iniziale_ipogeo = 'None'

		if self.comboBox_per_fin_ipogeo.currentText() != "":
			periodo_finale_ipogeo = self.comboBox_per_fin_ipogeo.currentText()
		else:
			periodo_finale_ipogeo = 'None'

		if self.comboBox_fas_fin_ipogeo.currentText() != "":
			fase_finale_ipogeo = self.comboBox_fas_fin_ipogeo.currentText()
		else:
			fase_finale_ipogeo = 'None'

		if self.comboBox_percentuale_umidita_ipogeo.currentText() != "":
			percentuale_umidita_ipogeo = self.comboBox_percentuale_umidita_ipogeo.currentText()
		else:
			percentuale_umidita_ipogeo = 'None'			

		if self.comboBox_grado_conservazione_ipogeo.currentText() != "":
			grado_conservazione_ipogeo = self.comboBox_grado_conservazione_ipogeo.currentText()
		else:
			grado_conservazione_ipogeo = 'None'

		if self.comboBox_grado_staticita_ipogeo.currentText() != "":
			grado_staticita_ipogeo = self.comboBox_grado_staticita_ipogeo.currentText()
		else:
			grado_staticita_ipogeo = 'None'
			
		##Campioni
		materiali_impiegati_ipogeo = self.table2dict("self.tableWidget_materiali_impiegati_ipogeo")
		##Elementi_strutturali
		elementi_strutturali_ipogeo = self.table2dict("self.tableWidget_elementi_strutturali_ipogeo")
		##Rapporti_ipogeo
		rapporti_ipogeo = self.table2dict("self.tableWidget_rapporti_ipogeo")
		##Misurazioni
		misurazioni_ipogeo = self.table2dict("self.tableWidget_misurazioni_ipogeo")

		self.DATA_LIST_REC_TEMP = [
		str(self.comboBox_sito_ipogeo.currentText()), 												#1 - Sito
		str(self.comboBox_sigla_ipogeo.currentText()), 									#2 - sigla
		str(numero_ipogeo), 																#3 - numero_struttura
		str(self.comboBox_categoria_ipogeo.currentText()),												#3 - numero_struttura
		str(self.comboBox_tipologia_ipogeo.currentText()), 											#3 - numero_struttura
		str(self.comboBox_definizione_ipogeo.currentText()),											#4 - cron iniziale
		str(self.descrizione_ipogeo.toPlainText().toLatin1()),					#6 - descrizioene
		str(self.textEdit_interpretazione_ipogeo.toPlainText().toLatin1()),				#6 - descrizioene
		str(periodo_iniziale_ipogeo),																#6 - descrizioene
		str(fase_iniziale_ipogeo),																	#6 - descrizioene
		str(periodo_finale_ipogeo),																#6 - descrizioene
		str(fase_finale_ipogeo),																	#6 - descrizioene
		str(self.lineEdit_datazione_estesa_ipogeo.text()),												#7- cron estesa
		str(materiali_impiegati_ipogeo),
		str(elementi_strutturali_ipogeo),
		str(rapporti_ipogeo),
		str(misurazioni_ipogeo),
                str(percentuale_umidita_ipogeo),
                str(grado_conservazione_ipogeo),
                str(grado_staticita_ipogeo)
		]

	def rec_toupdate(self):
		rec_to_update = self.UTILITY.pos_none_in_list(self.DATA_LIST_REC_TEMP)
		return rec_to_update

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

	#insert new row into tableWidget
	def on_pushButton_insert_row_rapporti_pressed(self):
		self.insert_new_row('self.tableWidget_rapporti_ipogeo')

	def on_pushButton_insert_row_materiali_pressed(self):
		self.insert_new_row('self.tableWidget_materiali_impiegati_ipogeo')

	def on_pushButton_insert_row_elementi_pressed(self):
		self.insert_new_row('self.tableWidget_elementi_strutturali_ipogeo')

	def on_pushButton_insert_row_misurazioni_pressed(self):
		self.insert_new_row('self.tableWidget_misurazioni_ipogeo')

	def insert_new_row(self, table_name):
		"""insert new row into a table based on table_name"""
		cmd = table_name+".insertRow(0)"
		eval(cmd)

	def on_pushButton_view_geometry_pressed(self):
		id_ipogeo = eval("int(self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE+")")
		self.pyQGIS.charge_vector_layers_ipogeo(id_ipogeo)

	def testing(self, name_file, message):
		f = open(str(name_file), 'w')
		f.write(str(message))
		f.close()

## Class end

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui = pyarchinit_US()
	ui.show()
	sys.exit(app.exec_())
