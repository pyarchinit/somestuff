#!/usr/bin/env python
# encoding: utf-8
"""
pyarchinit_image_d_d.py

Created by Pyarchinit on 2010-05-02.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

#!/usr/bin/env python
# Copyright (c) 2007-8 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.


import os
import sys

filepath = os.path.dirname(__file__)

gui_path = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'gui'))
gis_path = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'gis'))
db_path  = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'db'))
utility  = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'utility'))

sys.path.insert(0,gui_path)
sys.path.insert(1,gis_path)
sys.path.insert(2,db_path)
sys.path.insert(3,utility)
sys.path.insert(4,filepath)

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from imageViewer import ImageViewer
from pyarchinit_image_viewer_dialog import *
from pyarchinit_image_viewer_dialog import Ui_DialogImageViewer

from pyarchinit_utility import *
try:
	from  pyarchinit_db_manager import *
except:
	pass
from delegateComboBox import *
from pyarchinit_media_utility import *
from pyarchinit_conn_strings  import *


class Main(QDialog, Ui_DialogImageViewer):
	delegateSites = ''
	DB_MANAGER = ""
	TABLE_NAME = 'media_table'
	MAPPER_TABLE_CLASS = "MEDIA"
	ID_TABLE = "id_media"
	MAPPER_TABLE_CLASS_mediatous = 'MEDIATOUS'
	ID_TABLE_mediatous = 'id_mediaToUs'
	NOME_SCHEDA = "Scheda Media Manager"
	
	TABLE_THUMB_NAME = 'media_thumb_table'
	MAPPER_TABLE_CLASS_thumb = 'MEDIA_THUMB'
	ID_TABLE_THUMB = "id_media_thumb"
	
	UTILITY = Utility()

	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		
		# This is always the same
		QDialog.__init__(self)
		self.connection()
		self.setupUi(self)
		self.customize_gui()
		self.iconListWidget.SelectionMode()
		self.iconListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		self.connect(self.iconListWidget, SIGNAL("itemDoubleClicked(QListWidgetItem *)"),self.openWide_image)
		self.setWindowTitle("pyArchInit - Media Manager")
		self.open_images()

	def customize_gui(self):
		self.tableWidgetTags.setColumnWidth(0,300)
		self.tableWidgetTags.setColumnWidth(1,50)
		self.tableWidgetTags.setColumnWidth(2,50)

		valuesSites = self.charge_sito_list()
		self.delegateSites = ComboBoxDelegate()
		self.delegateSites.def_values(valuesSites)
		self.delegateSites.def_editable('False')
		self.tableWidgetTags.setItemDelegateForColumn(0,self.delegateSites)

		self.charge_sito_list()

	def connection(self):
		from pyarchinit_conn_strings import *
		conn = Connection()
		conn_str = conn.conn_str()
		try:
			self.DB_MANAGER = Pyarchinit_db_management(conn_str)
			self.DB_MANAGER.connection()
		except Exception, e:
			e = str(e)
			if e.find("no such table"):
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br><br> Tabella non presente. E' NECESSARIO RIAVVIARE QGIS" ,  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br> Errore: <br>" + str(e) ,  QMessageBox.Ok)


	def getDirectory(self):
		directory = QtGui.QFileDialog.getExistingDirectory(self, "Scegli una directory", "Seleziona una directory:", QtGui.QFileDialog.ShowDirsOnly)
		for image in sorted(os.listdir(directory.toUtf8())):
			if image.endswith(".png") or image.endswith(".PNG") or image.endswith(".JPG") or image.endswith(".jpg") or image.endswith(".jpeg") or image.endswith(".JPEG") or image.endswith(".tiff") or image.endswith(".TIFF") or image.endswith(".tiff") or image.endswith(".TIFF"):

				filename, filetype = image.split(".")[0], image.split(".")[1]		#db definisce nome immagine originale
				filepath = directory.toUtf8()+'/'+filename+"."+filetype 			#db definisce il path immagine originale
				idunique_image_check = self.db_search_check(self.MAPPER_TABLE_CLASS, 'filepath', filepath) #controlla che l'immagine non sia già presente nel db sulla base del suo path

				if bool(idunique_image_check) == False:
					mediatype = 'image'													#db definisce il tipo di immagine originale
					self.insert_record_media(mediatype, filename, filetype, filepath) 	#db inserisce i dati nella tabella media originali
					MU = Media_utility()
					conn = Connection()
					media_max_num_id = self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE) #db recupera il valore più alto ovvero l'ultimo immesso per l'immagine originale

					thumb_path = conn.thumb_path()
					thumb_path_str = thumb_path['thumb_path']

					media_thumb_suffix = '_pay.png'

					filenameorig = filename
					filename_thumb = str(media_max_num_id)+"_"+filename+media_thumb_suffix
					filepath_thumb = thumb_path_str+filename_thumb
					#crea la thumbnail
					try:
						MU.resample_images(media_max_num_id,filepath, filenameorig, thumb_path_str, media_thumb_suffix)
					except Exception, e:
						QMessageBox.warning(self, "Cucu", str(e),  QMessageBox.Ok)
			
					#inserisce i dati nel DB
					self.insert_record_mediathumb(media_max_num_id, mediatype,filename,filename_thumb,filetype,filepath_thumb)

					#visualizza le immagini nella gui
					item = QListWidgetItem(str(media_max_num_id))
					item.setData(QtCore.Qt.UserRole,filepath_thumb)
					icon = QIcon(filepath_thumb) #os.path.join('%s/%s' % (directory.toUtf8(), image)))
					item.setIcon(icon)
					self.iconListWidget.addItem(item)

				elif bool(idunique_image_check) == True:

					#recupero il valore id_media basato sul path dell'immagine

					data = idunique_image_check
					id_media = data[0].id_media

					#visualizza le immagini nella gui
					item = QListWidgetItem(str(id_media))
					
					data_for_thumb = self.db_search_check(self.MAPPER_TABLE_CLASS_thumb, 'id_media', id_media) # recupera i valori della thumb in base al valore id_media del file originale
					
					thumb_path = data_for_thumb[0].filepath
					item.setData(QtCore.Qt.UserRole,thumb_path)
					icon = QIcon(thumb_path) #os.path.join('%s/%s' % (directory.toUtf8(), image)))
					item.setIcon(icon)
					self.iconListWidget.addItem(item)


	def insert_record_media(self, mediatype, filename, filetype, filepath):
		self.mediatype = mediatype
		self.filename = filename
		self.filetype = filetype
		self.filepath = filepath

		try:
			data = self.DB_MANAGER.insert_media_values(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE)+1,
			str(self.mediatype), 									#1 - mediatyype
			str(self.filename), 									#2 - filename
			str(self.filetype),						 				#3 - filetype
			str(self.filepath), 									#4 - filepath
			str('Inserisci una descrizione'),						#5 - descrizione
			str("['immagine']")) 									#6 - tags
			try:
				self.DB_MANAGER.insert_data_session(data)
				return 1
			except Exception, e:
				e_str = str(e)
				if e_str.__contains__("Integrity"):
					msg = self.filename + ": immagine gia' presente nel database"
				else:
					msg = e
				QMessageBox.warning(self, "Errore", "Attenzione 1 ! \n"+ str(msg),  QMessageBox.Ok)
				return 0

		except Exception, e:
			QMessageBox.warning(self, "Errore", "Attenzione 2 ! \n"+str(e),  QMessageBox.Ok)
			return 0

	def insert_record_mediathumb(self, media_max_num_id, mediatype,filename,filename_thumb,filetype,filepath_thumb):
		self.media_max_num_id = media_max_num_id
		self.mediatype = mediatype
		self.filename = filename
		self.filename_thumb = filename_thumb
		self.filetype = filetype
		self.filepath_thumb = filepath_thumb

		try:
			data = self.DB_MANAGER.insert_mediathumb_values(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS_thumb, self.ID_TABLE_THUMB)+1,
			str(self.media_max_num_id), 							#1 - media_max_num_id
			str(self.mediatype),									#2 - mediatype
			str(self.filename), 									#3 - filename
			str(self.filename_thumb),						 		#4 - filename_thumb
			str(self.filetype), 									#5 - filetype
			str(self.filepath_thumb))								#6 - filepath_thumb

			try:
				self.DB_MANAGER.insert_data_session(data)
				return 1
			except Exception, e:
				e_str = str(e)
				if e_str.__contains__("Integrity"):
					msg = self.filename + ": thumb gia' presente nel database"
				else:
					msg = e
				QMessageBox.warning(self, "Errore", "Attenzione 1 ! \n"+ str(msg),  QMessageBox.Ok)
				return 0

		except Exception, e:
			QMessageBox.warning(self, "Errore", "Attenzione 2 ! \n"+str(e),  QMessageBox.Ok)
			return 0


	def insert_mediaTous_rec(self, id_us, sito, area, us, id_media, filepath):
		self.id_us = id_us
		self.sito = sito
		self.area = area
		self.us = us
		self.id_media = id_media
		self.filepath = filepath

		try:
			data = self.DB_MANAGER.insert_media2us_values(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS_mediatous, self.ID_TABLE_mediatous)+1,
			int(self.id_us), 											#1 - id_us
			str(self.sito), 											#2 - sito
			str(self.area), 											#3 - area
			int(self.us), 												#4 - us
			int(self.id_media),											#5 - id_media
			str(self.filepath))											#6 - filepath
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

	def db_search_check(self, table_class, field, value):
		self.table_class = table_class
		self.field = field
		self.value = value

		search_dict = {self.field : "'"+str(self.value)+"'"}

		u = Utility()
		search_dict = u.remove_empty_items_fr_dict(search_dict)

		res = self.DB_MANAGER.query_bool(search_dict, self.table_class)

		return res

	def insert_new_row(self, table_name):
		"""insert new row into a table based on table_name"""
		cmd = table_name+".insertRow(0)"
		eval(cmd)

	def remove_row(self, table_name):
		"""insert new row into a table based on table_name"""
		table_row_count_cmd = ("%s.rowCount()") % (table_name)
		table_row_count = eval(table_row_count_cmd)
		row_index = table_row_count - 1
		cmd = ("%s.removeRow(%d)") % (table_name, row_index)
		eval(cmd)

	def openWide_image(self):
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

	def charge_sito_list(self):
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))
		try:
			sito_vl.remove('')
		except:
			pass

		sito_vl.sort()
		return sito_vl


	def generate_US(self):
		tags_list = self.table2dict('self.tableWidgetTags')
		record_us_list = []
		for sing_tags in tags_list:
				search_dict = {'sito'  : "'"+str(sing_tags[0])+"'",
								'area': "'"+str(sing_tags[1])+"'" ,
								'us': "'"+str(sing_tags[2])+"'"
								}
				record_us_list.append(self.DB_MANAGER.query_bool(search_dict, 'US'))

		us_list = []
		for r in record_us_list:
			us_list.append([r[0].id_us, r[0].sito, r[0].area, r[0].us])
		return us_list


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

	def open_images(self):
		data = self.DB_MANAGER.query(eval(self.MAPPER_TABLE_CLASS_thumb))
		
		for i in range(len(data)):
			item = QListWidgetItem(str(data[i].id_media))

			#data_for_thumb = self.db_search_check(self.MAPPER_TABLE_CLASS_thumb, 'id_media', id_media) # recupera i valori della thumb in base al valore id_media del file originale
		
			thumb_path = data[i].filepath
			item.setData(QtCore.Qt.UserRole,thumb_path)
			icon = QIcon(thumb_path) #os.path.join('%s/%s' % (directory.toUtf8(), image)))
			item.setIcon(icon)
			self.iconListWidget.addItem(item)

	#Button utility
	def on_pushButton_chose_dir_pressed(self):
		self.getDirectory()

	def on_pushButton_addRow_pressed(self):
		self.insert_new_row('self.tableWidgetTags')

	def on_pushButton_removeRow_pressed(self):
		self.remove_row('self.tableWidgetTags')

	def on_pushButton_assignTags_pressed(self):
		items_selected = self.iconListWidget.selectedItems()
		us_list = self.generate_US()

		for item in items_selected:
			for us_data in us_list:
				id_orig_item = item.text() #return the name of original file
				search_dict = {'id_media' : "'"+str(id_orig_item)+"'"}
				media_data = self.DB_MANAGER.query_bool(search_dict, 'MEDIA')
				self.insert_mediaTous_rec(us_data[0], us_data[1], us_data[2], us_data[3], media_data[0].id_media, media_data[0].filepath)

	def on_pushButton_openMedia_pressed(self):
		self.open_images()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui = Main()
	ui.show()
	sys.exit(app.exec_())

