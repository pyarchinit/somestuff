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
#from  pyarchinit_inventario_reperti_ui import Ui_DialogInventarioMateriali
from  pyarchinit_inventario_reperti_ui import *
from  pyarchinit_utility import *
from  pyarchinit_error_check import *

try:
	from  pyarchinit_db_manager import *
except:
	pass
from  sortpanelmain import SortPanelMain

from  pyarchinit_exp_Findssheet_pdf import *

class pyarchinit_Inventario_reperti(QDialog, Ui_DialogInventarioMateriali):
	MSG_BOX_TITLE = "PyArchInit - Scheda Inventario Materiali"
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
	TABLE_NAME = 'inventario_materiali_table'
	MAPPER_TABLE_CLASS = "INVENTARIO_MATERIALI"
	NOME_SCHEDA = "Scheda 	Inventario Materiali"
	ID_TABLE = "id_invmat"
	CONVERSION_DICT = {
	ID_TABLE:ID_TABLE,
	"Sito" : "sito",
	"Numero inventario" : "numero_inventario",
	"Tipo reperto" : "tipo_reperto",
	"Criterio schedatura" : "criterio_schedatura",
	"Definizione" : "definizione",
	"Descrizione" : "descrizione",
	"Area" : "area",
	"US" : "us",
	"Lavato" : "lavato",
	"Numero cassa" : "nr_cassa",
	"Luogo di conservazione" : "luogo_conservazione",
	"Stato conservazione" : "stato_conservazione",
	"Datazione reperto" : "datazione_reperto"
	}

	SORT_ITEMS = [
				ID_TABLE,
				"Sito",
				"Numero inventario",
				"Tipo reperto",
				"Criterio schedatura",
				"Definizione",
				"Descrizione",
				"Area",
				"US",
				"Lavato",
				"Numero cassa",
				"Luogo di conservazione"
				"Stato conservazione",
				"Datazione reperto"
				]

	TABLE_FIELDS = [
					"sito",
					"numero_inventario",
					"tipo_reperto",
					"criterio_schedatura",
					"definizione",
					"descrizione",
					"area",
					"us",
					"lavato",
					"nr_cassa",
					"luogo_conservazione",
					"stato_conservazione",
					"datazione_reperto",
					"elementi_reperto",
					"misurazioni",
					"rif_biblio",
					"tecnologie"
					]

	def __init__(self, iface):
		self.iface = iface

		QDialog.__init__(self)
		self.setupUi(self)
		self.currentLayerId = None
		try:
			self.on_pushButton_connect_pressed()
		except:
			pass


	def on_pushButton_connect_pressed(self):
		from pyarchinit_conn_strings import *
		self.setComboBoxEditable(["self.comboBox_sito"],1)
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
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br><br> E' NECESSARIO RIAVVIARE QGIS" + e ,  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br> Errore: <br>" + str(e) ,  QMessageBox.Ok)
		self.charge_list()
	def charge_list(self):
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))

		try:
			sito_vl.remove('')
		except:
			pass
		self.comboBox_sito.clear()
		sito_vl.sort()
		self.comboBox_sito.addItems(sito_vl)
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


	def on_pushButton_new_rec_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
		#set the GUI for a new record

		if self.BROWSE_STATUS != "n":
			self.BROWSE_STATUS = "n"
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			self.empty_fields()

			self.setComboBoxEditable(['self.comboBox_sito'], 1)
			#self.setComboBoxEditable(['self.comboBox_sito'], 1)
			self.setComboBoxEnable(['self.comboBox_sito'], 'True')
			self.setComboBoxEnable(['self.lineEdit_num_inv'], 'True')


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
                                QMessageBox.warning(self, "ATTENZIONE", "Non e' stata realizzata alcuna modifica.",  QMessageBox.Ok)
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

                        self.setComboBoxEditable(['self.comboBox_sito'], 1)
                        self.setComboBoxEnable(['self.comboBox_sito'], 'False')
                        self.setComboBoxEnable(['self.lineEdit_num_inv'], 'False')

                        self.fill_fields(self.REC_CORR)
                        self.enable_button(1)

	def generate_list_pdf(self):
		data_list = []
		for i in range(len(self.DATA_LIST)):
			data_list.append([
            str(self.DATA_LIST[i].id_invmat), 							#1 - id_invmat
            str(self.DATA_LIST[i].sito),								#2 - sito
			int(self.DATA_LIST[i].numero_inventario),					#3 - numero_inventario
			str(self.DATA_LIST[i].tipo_reperto),						#4 - tipo_reperto
			str(self.DATA_LIST[i].criterio_schedatura),				#5 - criterio_schedatura
            self.DATA_LIST[i].definizione,								#6 - definizione
            unicode(self.DATA_LIST[i].descrizione),					#7 - descrizione
            str(self.DATA_LIST[i].area),								#8 - area
            str(self.DATA_LIST[i].us),                                 #9 - us
            str(self.DATA_LIST[i].lavato),                             #10 - lavato
            str(self.DATA_LIST[i].nr_cassa), 							#11 - nr_cassa
			str(self.DATA_LIST[i].luogo_conservazione),			    #12 - luogo_conservazione
			str(self.DATA_LIST[i].stato_conservazione),				#13 - stato_conservazione
			str(self.DATA_LIST[i].datazione_reperto),					#14 - datazione_reperto
			str(self.DATA_LIST[i].elementi_reperto),					#15 - elementi_reperto
            str(self.DATA_LIST[i].misurazioni),                        #16 - misurazioni
            str(self.DATA_LIST[i].rif_biblio),                         #17 - rif_biblio
            str(self.DATA_LIST[i].tecnologie)							#18 - misurazioni
		])
		return data_list

	def on_pushButton_exp_pdf_sheet_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
		Finds_pdf_sheet = generate_pdf()
		data_list = self.generate_list_pdf()
		Finds_pdf_sheet.build_Finds_sheets(data_list)

	def data_error_check(self):
		test = 0
		EC = Error_check()

		area = self.lineEdit_area.text()
		us = self.lineEdit_us.text()
		nr_cassa = self.lineEdit_nr_cassa.text()
		if area != "":
			if EC.data_is_int(area) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Area.\nIl valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		if us != "":
			if EC.data_is_int(us) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo US.\nIl valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		if nr_cassa != "":
			if EC.data_is_int(nr_cassa) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Numero Cassa.\nIl valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		return test



	def insert_new_rec(self):
		#elementi reperto
		elementi_reperto = self.table2dict("self.tableWidget_elementi_reperto")
		##misurazioni
		misurazioni = self.table2dict("self.tableWidget_misurazioni")
		##rif_biblio
		rif_biblio = self.table2dict("self.tableWidget_rif_biblio")
		##tecnologie
		tecnologie = self.table2dict("self.tableWidget_tecnologie")

		try:
			if self.lineEdit_area.text() == "":
				area = None
			else:
				area = int(self.lineEdit_area.text())

			if self.lineEdit_us.text() == "":
				us = None
			else:
				us = int(self.lineEdit_us.text())
				
			if self.lineEdit_nr_cassa.text() == "":
				nr_cassa = None
			else:
				nr_cassa = int(self.lineEdit_nr_cassa.text())

			data = self.DB_MANAGER.insert_values_reperti(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE)+1, 		#0 - IDsito
                        str(self.comboBox_sito.currentText()), 						#1 - Sito
                        int(self.lineEdit_num_inv.text()),						        #2 - num_inv
                        str(self.comboBox_tipo_reperto.currentText()), 				#3 - tipo_reperto
                        str(self.comboBox_criterio_schedatura.currentText()),			#4 - criterio
                        str(self.comboBox_definizione.currentText()), 					#5 - definizione
                        unicode(self.textEdit_descrizione_reperto.toPlainText()),		#6 - descrizione
                        area,										                    #7 - area
                        us,										                        #8 - us
                        str(self.comboBox_lavato.currentText()),					    #9 - lavato
                        nr_cassa,									                    #10 - nr cassa
                        str(self.lineEdit_luogo_conservazione.text()),					#11 - luogo conservazione
                        str(self.comboBox_conservazione.currentText()),				#12 - stato di conservazione
                        str(self.lineEdit_datazione_rep.text()),					    #13 - datazione reperto
                        str(elementi_reperto),								            #14 - elementi reperto
                        str(misurazioni),								                #15 - misurazioni
                        str(rif_biblio), 								                #16 - rif biblio
                        str(tecnologie)									                #17 - tecnologie
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
				QMessageBox.warning(self, "Errore", "immisione 1 \n"+ str(msg),  QMessageBox.Ok)
				return 0

		except Exception, e:
			QMessageBox.warning(self, "Errore", "Errore di immisione 2 \n"+str(e),  QMessageBox.Ok)
			return 0

	#insert new row into tableWidget
	#elementi reperto
	def on_pushButton_insert_row_elementi_pressed(self):
		self.insert_new_row('self.tableWidget_elementi_reperto')
	def on_pushButton_remove_row_elementi_pressed(self):
		self.remove_row('self.tableWidget_elementi_reperto')

	#misurazioni
	def on_pushButton_insert_row_misure_pressed(self):
		self.insert_new_row('self.tableWidget_misurazioni')
	def on_pushButton_remove_row_misure_pressed(self):
		self.remove_row('self.tableWidget_misurazioni')

	#tecnologie
	def on_pushButton_insert_row_tecnologie_pressed(self):
		self.insert_new_row('self.tableWidget_tecnologie')
	def on_pushButton_remove_row_tecnologie_pressed(self):
		self.remove_row('self.tableWidget_tecnologie')

	#rif biblio
	def on_pushButton_insert_row_rif_biblio_pressed(self):
		self.insert_new_row('self.tableWidget_rif_biblio')
	def on_pushButton_remove_row_rif_bibilio_pressed(self):
		self.remove_row('self.tableWidget_rif_biblio')

	def on_pushButton_view_all_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
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
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
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
		if self.records_equal_check() == 1:
			msg = self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
		else:
			self.enable_button_search(0)

			#set the GUI for a new search

			if self.BROWSE_STATUS != "f":
				self.BROWSE_STATUS = "f"
				self.setComboBoxEditable(['self.comboBox_sito'], 1)
				self.setComboBoxEnable(['self.comboBox_sito'], 'True')
				self.setComboBoxEditable(['self.comboBox_lavato'], 1)
				self.setComboBoxEnable(['self.comboBox_lavato'], 'True')
				self.setComboBoxEnable(['self.lineEdit_num_inv'], 'True')
				self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
				self.set_rec_counter('','')
				self.label_sort.setText(self.SORTED_ITEMS["n"])
				self.charge_list()
				self.empty_fields()

	def on_pushButton_search_go_pressed(self):
		if self.BROWSE_STATUS != "f":
			QMessageBox.warning(self, "ATTENZIONE", "Per eseguire una nuova ricerca clicca sul pulsante 'new search' ",  QMessageBox.Ok)
		else:
			##scavato
			if self.lineEdit_num_inv.text() != "":
				numero_inventario = int(self.lineEdit_num_inv.text())
			else:
				numero_inventario = ""

			if self.lineEdit_area.text() != "":
				area = int(self.lineEdit_area.text())
			else:
				area = ""

			if self.lineEdit_us.text() != "":
				us = int(self.lineEdit_us.text())
			else:
				us = ""

			if self.lineEdit_nr_cassa.text() != "":
				nr_cassa = int(self.lineEdit_nr_cassa.text())
			else:
				nr_cassa = ""

			search_dict = {
			self.TABLE_FIELDS[0] : "'"+str(self.comboBox_sito.currentText())+"'",
			self.TABLE_FIELDS[1] : numero_inventario,
			self.TABLE_FIELDS[2] : "'" + str(self.comboBox_tipo_reperto.currentText()) + "'",
			self.TABLE_FIELDS[3] : "'" + str(self.comboBox_criterio_schedatura.currentText()) + "'",
			self.TABLE_FIELDS[4] : "'" + str(self.comboBox_definizione.currentText()) + "'",
			self.TABLE_FIELDS[5] : "'" + str(self.textEdit_descrizione_reperto.toPlainText()) + "'",
			self.TABLE_FIELDS[6] : area,
			self.TABLE_FIELDS[7] : us,
			self.TABLE_FIELDS[8] : "'" + str(self.comboBox_lavato.currentText()) + "'",
			self.TABLE_FIELDS[9] : nr_cassa,
			self.TABLE_FIELDS[10] : "'" + str(self.lineEdit_luogo_conservazione.text()) + "'",
			self.TABLE_FIELDS[11] : "'" +  str(self.comboBox_conservazione.currentText()) + "'",
			self.TABLE_FIELDS[12] : "'" + str(self.lineEdit_datazione_rep.text()) + "'",
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
					self.setComboBoxEditable(["self.comboBox_lavato"],1)
					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.lineEdit_num_inv"],"False")

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

					self.setComboBoxEditable(["self.comboBox_sito"],0)
					self.setComboBoxEditable(["self.comboBox_lavato"],0)
					self.setComboBoxEnable(['self.lineEdit_num_inv'], "False")
					self.setComboBoxEnable(['self.comboBox_sito'], "False")
					


					QMessageBox.warning(self, "Messaggio", "%s %d %s" % strings,  QMessageBox.Ok)

		self.enable_button_search(1)

	def update_if(self, msg):
		rec_corr = self.REC_CORR
		self.msg = msg
		if self.msg == 1:
			test = self.update_record()
			if test == 1:
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
				return 1
			elif test == 0:
				return 0
			

	#custom functions
	def charge_records(self):
		self.DATA_LIST = []
		id_list = []
		for i in self.DB_MANAGER.query(eval(self.MAPPER_TABLE_CLASS)):
			id_list.append(eval("i."+ self.ID_TABLE))

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
		try:
			rowIndex = (rowSelected[1].row())
			cmd = ("%s.removeRow(%d)") % (table_name, rowIndex)
			eval(cmd)
		except:
			QMessageBox.warning(self, "Messaggio", "Devi selezionare una riga",  QMessageBox.Ok)


	def empty_fields(self):
		elementi_reperto_row_count = self.tableWidget_elementi_reperto.rowCount()
		misurazioni_row_count = self.tableWidget_misurazioni.rowCount()
		rif_biblio_row_count = self.tableWidget_rif_biblio.rowCount()
		tecnologie_row_count = self.tableWidget_tecnologie.rowCount()

		self.comboBox_sito.setEditText("") 								#1 - Sito
		self.lineEdit_num_inv.clear()									#2 - num_inv
		self.comboBox_tipo_reperto.setEditText("")  					#3 - tipo_reperto
		self.comboBox_criterio_schedatura.setEditText("") 				#4 - criterio
		self.comboBox_definizione.setEditText("") 						#5 - definizione
		self.textEdit_descrizione_reperto.clear()						#6 - descrizione
		self.lineEdit_area.clear()										#7 - area
		self.lineEdit_us.clear()										#8 - US
		self.comboBox_lavato.setEditText("")							#9 - lavato
		self.lineEdit_nr_cassa.clear()									#10 - nr_cassa
		self.lineEdit_luogo_conservazione.clear()						#11 - luogo_conservazione
		self.comboBox_conservazione.setEditText("") 					#12 - stato conservazione
		self.lineEdit_datazione_rep.clear()								#13 - datazione reperto
		for i in range(elementi_reperto_row_count):
			self.tableWidget_elementi_reperto.removeRow(0) 					
		self.insert_new_row("self.tableWidget_elementi_reperto")		#14 - elementi reperto

		for i in range(misurazioni_row_count):
			self.tableWidget_misurazioni.removeRow(0)
		self.insert_new_row("self.tableWidget_misurazioni")				#15 - misurazioni

		for i in range(rif_biblio_row_count):
			self.tableWidget_rif_biblio.removeRow(0)
		self.insert_new_row("self.tableWidget_rif_biblio")				#16 - rif_biblio

		for i in range(tecnologie_row_count):
			self.tableWidget_tecnologie.removeRow(0)
		self.insert_new_row("self.tableWidget_tecnologie")				#17 - misurazioni


	def fill_fields(self, n=0):
		self.rec_num = n
		try:
			self.comboBox_sito.setEditText(self.DATA_LIST[self.rec_num].sito)  											#1 - Sito
			self.lineEdit_num_inv.setText(str(self.DATA_LIST[self.rec_num].numero_inventario))							#2 - num_inv
			self.comboBox_tipo_reperto.setEditText(str(self.DATA_LIST[self.rec_num].tipo_reperto))						#3 - Tipo reperto
			self.comboBox_criterio_schedatura.setEditText(str(self.DATA_LIST[self.rec_num].criterio_schedatura))		#4 - Criterio schedatura
			self.comboBox_definizione.setEditText(str(self.DATA_LIST[self.rec_num].definizione))						#5 - definizione
			unicode(self.textEdit_descrizione_reperto.setText(self.DATA_LIST[self.rec_num].descrizione))				#6 - descrizione
			if self.DATA_LIST[self.rec_num].area == None:																#7 - Area
				self.lineEdit_area.setText("")
			else:
				self.lineEdit_area.setText(str(self.DATA_LIST[self.rec_num].area))

			if self.DATA_LIST[self.rec_num].us == None:																	#8 - US
				self.lineEdit_us.setText("")
			else:
				self.lineEdit_us.setText(str(self.DATA_LIST[self.rec_num].us))

			self.comboBox_lavato.setEditText(str(self.DATA_LIST[self.rec_num].lavato))

			if self.DATA_LIST[self.rec_num].nr_cassa == None:															#10 - nr_cassa
				self.lineEdit_nr_cassa.setText("")
			else:
				self.lineEdit_nr_cassa.setText(str(self.DATA_LIST[self.rec_num].nr_cassa))

			self.lineEdit_luogo_conservazione.setText(str(self.DATA_LIST[self.rec_num].luogo_conservazione))			#11 - luogo_conservazione

			self.comboBox_conservazione.setEditText(str(self.DATA_LIST[self.rec_num].stato_conservazione))				#12 - stato conservazione

			self.lineEdit_datazione_rep.setText(str(self.DATA_LIST[self.rec_num].datazione_reperto))					#13 - datazione reperto

			self.tableInsertData("self.tableWidget_elementi_reperto", self.DATA_LIST[self.rec_num].elementi_reperto)	#14 - elementi_reperto

			self.tableInsertData("self.tableWidget_misurazioni", self.DATA_LIST[self.rec_num].misurazioni)				#15 - campioni

			self.tableInsertData("self.tableWidget_rif_biblio", self.DATA_LIST[self.rec_num].rif_biblio)				#16 - rif biblio

			self.tableInsertData("self.tableWidget_tecnologie",self.DATA_LIST[self.rec_num].tecnologie)					#17 - rapporti
			
			

		except Exception, e:
			QMessageBox.warning(self, "Errore Fill Fields", str(e),  QMessageBox.Ok)

	def set_rec_counter(self, t, c):
		self.rec_tot = t
		self.rec_corr = c
		self.label_rec_tot.setText(str(self.rec_tot))
		self.label_rec_corrente.setText(str(self.rec_corr))

	def set_LIST_REC_TEMP(self):
		#TableWidget

		#elementi reperto
		elementi_reperto = self.table2dict("self.tableWidget_elementi_reperto")
		##misurazioni
		misurazioni = self.table2dict("self.tableWidget_misurazioni")
		##rif_biblio
		rif_biblio = self.table2dict("self.tableWidget_rif_biblio")
		##tecnologie
		tecnologie = self.table2dict("self.tableWidget_tecnologie")
		
		
		##scavato
		if self.lineEdit_area.text() == "":
			area = None
		else:
			area = self.lineEdit_area.text()
		if self.lineEdit_us.text() == "":
			us = None
		else:
			us = self.lineEdit_us.text()
		if self.lineEdit_nr_cassa.text() == "":
			nr_cassa = None
		else:
			nr_cassa = self.lineEdit_nr_cassa.text()

		#data
		self.DATA_LIST_REC_TEMP = [
		str(self.comboBox_sito.currentText()), 								#1 - Sito
		str(self.lineEdit_num_inv.text()), 									#2 - num_inv
		str(self.comboBox_tipo_reperto.currentText()), 						#3 - tipo_reperto
		str(self.comboBox_criterio_schedatura.currentText()),				#4 - criterio schedatura
		str(self.comboBox_definizione.currentText()), 						#5 - definizione
		str(self.textEdit_descrizione_reperto.toPlainText().toLatin1()),	#6 - descrizione
		str(area),															#7 - area
		str(us),															#8 - us
		str(self.comboBox_lavato.currentText()),							#9 - lavato
		str(nr_cassa),														#10 - nr cassa
		str(self.lineEdit_luogo_conservazione.text()),						#11 - luogo conservazione
		str(self.comboBox_conservazione.currentText()), 					#12 - stato conservazione
		str(self.lineEdit_datazione_rep.text()), 							#13 - datazione reperto
		str(elementi_reperto), 												#14 - elementi reperto
		str(misurazioni),													#15 - misurazioni
		str(rif_biblio),													#16 - rif_biblio
		str(tecnologie)														#17 - tecnologie
		]


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


	def set_LIST_REC_CORR(self):
		self.DATA_LIST_REC_CORR = []
		for i in self.TABLE_FIELDS:
			self.DATA_LIST_REC_CORR.append(eval("str(self.DATA_LIST[self.REC_CORR]." + i + ")"))

	def records_equal_check(self):
		self.set_LIST_REC_TEMP()
		self.set_LIST_REC_CORR()

		check_str = str(self.DATA_LIST_REC_CORR) + " " + str(self.DATA_LIST_REC_TEMP)
                
		#ff = open('test_check.txt', 'w')
		#ff.write(str(check_str))
		#ff.close()

		if self.DATA_LIST_REC_CORR == self.DATA_LIST_REC_TEMP:
			return 0
		else:
			return 1



	def update_record(self):
		try:
			self.DB_MANAGER.update(self.MAPPER_TABLE_CLASS, 
						self.ID_TABLE,
						[eval("int(self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE+")")],
						self.TABLE_FIELDS,
						self.rec_toupdate())
			return 1
		except Exception, e:
			QMessageBox.warning(self, "Messaggio", "Problema di encoding: sono stati inseriti accenti o caratteri non accettati dal database. Se chiudete ora la scheda senza correggere gli errori perderete i dati. Fare una copia di tutto su un foglio word a parte. Errore :" + str(e), QMessageBox.Ok)
			return 0

	def rec_toupdate(self):
		rec_to_update = self.UTILITY.pos_none_in_list(self.DATA_LIST_REC_TEMP)
		return rec_to_update


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
