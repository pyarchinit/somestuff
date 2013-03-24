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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.QtGui

from qgis.core import *
from qgis.gui import *

from settings import *

class Pyarchinit_pyqgis(QDialog, Settings):
	if os.name == 'posix':
		HOME = os.environ['HOME']
	elif os.name == 'nt':
		HOME = os.environ['HOMEPATH']
	FILEPATH = os.path.dirname(__file__)
	LAYER_STYLE_PATH = ('%s%s%s%s') % (FILEPATH, os.sep, 'styles', os.sep)
	SRS = 3004
	
	USLayerId = ""

	def __init__(self, iface):
		self.iface = iface
		QDialog.__init__(self)


	def remove_USlayer_from_registry(self):
		QgsMapLayerRegistry.instance().removeMapLayer(self.USLayerId)
		return 0
		
	
	def charge_individui_us(self, data):
		#Clean Qgis Map Later Registry
		#QgsMapLayerRegistry.instance().removeAllMapLayers()
		# Get the user input, starting with the table name
		
		#self.find_us_cutted(data)

		cfg_rel_path = os.path.join(os.sep,'pyarchinit_DB_folder', 'config.cfg')
		file_path = ('%s%s') % (self.HOME, cfg_rel_path)
		conf = open(file_path, "r")
		con_sett = conf.read()
		conf.close()

		settings = Settings(con_sett)
		settings.set_configuration()
		
		if settings.SERVER == 'sqlite':
			sqliteDB_path = os.path.join(os.sep,'pyarchinit_DB_folder', 'pyarchinit_db.sqlite')
			db_file_path = ('%s%s') % (self.HOME, sqliteDB_path)

			gidstr =  id_us = "id_us = '" + str(data[0]) +"'"
			if len(data) > 1:
				for i in range(len(data)):
					gidstr += " OR id_us = '" + str(data[i]) +"'"

			uri = QgsDataSourceURI()
			uri.setDatabase(db_file_path)

			uri.setDataSource('','pyarchinit_us_view', 'Geometry', gidstr, "gid")
			layerUS=QgsVectorLayer(uri.uri(), 'pyarchinit_us_view', 'spatialite')

			if  layerUS.isValid() == True:
				self.USLayerId = layerUS.getLayerID()
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'us_caratterizzazioni.qml')
				layerUS.loadNamedStyle(style_path)
				QgsMapLayerRegistry.instance().addMapLayer(layerUS, True)

			"""
			Sistema abolito
			uri.setDataSource('','pyarchinit_caratterizzazioni_view', 'Geometry', gidstr, "gid")
			layerCA=QgsVectorLayer(uri.uri(), 'pyarchinit_caratterizzazioni_view', 'spatialite')

			if  layerCA.isValid() == True:
				CALayerId = layerCA.getLayerID()
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'previewCAstyle.qml')
				layerCA.loadNamedStyle(style_path)
				QgsMapLayerRegistry.instance().addMapLayer(layerCA, True)
			"""
			uri.setDataSource('','pyarchinit_quote_view', 'Geometry', gidstr, "gid")
			layerQUOTE=QgsVectorLayer(uri.uri(), 'pyarchinit_quote_view', 'spatialite')
			if  layerQUOTE.isValid() == True:
				QgsMapLayerRegistry.instance().addMapLayer(layerQUOTE, True)
			
			uri.setDataSource('','pyarchinit_pyuscarlinee_view', 'Geometry', gidstr, "gid")
			layerQUOTE=QgsVectorLayer(uri.uri(), 'pyarchinit_pyuscarlinee_view', 'spatialite')
			if  layerQUOTE.isValid() == True:
				QgsMapLayerRegistry.instance().addMapLayer(layerQUOTE, True)

		elif settings.SERVER == 'postgres':

			uri = QgsDataSourceURI()
			# set host name, port, database name, username and password
		
			uri.setConnection(settings.HOST, settings.PORT, settings.DATABASE, settings.USER, settings.PASSWORD)

			gidstr =  id_us = "id_us = " + str(data[0])
			if len(data) > 1:
				for i in range(len(data)):
					gidstr += " OR id_us = " + str(data[i])

			srs = QgsCoordinateReferenceSystem(self.SRS, QgsCoordinateReferenceSystem.PostgisCrsId)

			uri.setDataSource("public", "pyarchinit_us_view", "the_geom", gidstr, "gid")
			layerUS = QgsVectorLayer(uri.uri(), "Unita' Stratigrafiche", "postgres")
		
			if  layerUS.isValid() == True:
				layerUS.setCrs(srs)
				self.USLayerId = layerUS.getLayerID()
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'us_caratterizzazioni.qml')
				layerUS.loadNamedStyle(style_path)
				QgsMapLayerRegistry.instance().addMapLayer(layerUS, True)

			"""
			sistema abolito 
			uri.setDataSource("public", "pyarchinit_uscaratterizzazioni_view", "the_geom", gidstr, "gid")
			layerCA = QgsVectorLayer(uri.uri(), "Caratterizzazioni US", "postgres")
			
			if layerCA.isValid() == True:
				layerCA.setCrs(srs)
				CALayerId = layerCA.getLayerID()
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'previewCAstyle.qml')
				layerCA.loadNamedStyle(style_path)
				QgsMapLayerRegistry.instance().addMapLayer(layerCA, True)
			"""
			uri.setDataSource("public", "pyarchinit_quote_view", "the_geom", gidstr, "gid")
			layerQUOTE = QgsVectorLayer(uri.uri(), "Quote Unita' Stratigrafiche", "postgres")

			if layerQUOTE.isValid() == True:
				layerQUOTE.setCrs(srs)
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'stile_quote.qml')
				layerQUOTE.loadNamedStyle(style_path)
				try:
					QgsMapLayerRegistry.instance().addMapLayer(layerQUOTE, True)
				except Exception, e:
					pass
					#f = open('/test_ok.txt','w')
					#f.write(str(e))
					#f.close()

			uri.setDataSource("public", "pyarchinit_pyuscarlinee_view", "the_geom", gidstr, "gid")
			layerCA = QgsVectorLayer(uri.uri(), "Caratterizzazioni US linee", "postgres")

			if layerCA.isValid() == True:
				layerCA.setCrs(srs)
				CALayerId = layerCA.getLayerID()
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'caratterizzazioni_linee.qml')
				layerCA.loadNamedStyle(style_path)
				QgsMapLayerRegistry.instance().addMapLayer(layerCA, True)
		

	def charge_vector_layers(self, data):
		#Clean Qgis Map Later Registry
		#QgsMapLayerRegistry.instance().removeAllMapLayers()
		# Get the user input, starting with the table name
		
		#self.find_us_cutted(data)

		cfg_rel_path = os.path.join(os.sep,'pyarchinit_DB_folder', 'config.cfg')
		file_path = ('%s%s') % (self.HOME, cfg_rel_path)
		conf = open(file_path, "r")
		con_sett = conf.read()
		conf.close()

		settings = Settings(con_sett)
		settings.set_configuration()
		
		if settings.SERVER == 'sqlite':
			sqliteDB_path = os.path.join(os.sep,'pyarchinit_DB_folder', 'pyarchinit_db.sqlite')
			db_file_path = ('%s%s') % (self.HOME, sqliteDB_path)

			gidstr =  id_us = "id_us = '" + str(data[0].id_us) +"'"
			if len(data) > 1:
				for i in range(len(data)):
					gidstr += " OR id_us = '" + str(data[i].id_us) +"'"

			uri = QgsDataSourceURI()
			uri.setDatabase(db_file_path)

			uri.setDataSource('','pyarchinit_us_view', 'Geometry', gidstr, "gid")
			layerUS=QgsVectorLayer(uri.uri(), 'pyarchinit_us_view', 'spatialite')

			if  layerUS.isValid() == True:
				self.USLayerId = layerUS.getLayerID()
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'us_caratterizzazioni.qml')
				layerUS.loadNamedStyle(style_path)
				QgsMapLayerRegistry.instance().addMapLayer(layerUS, True)

			"""
			uri.setDataSource('','pyarchinit_caratterizzazioni_view', 'Geometry', gidstr, "gid")
			layerCA=QgsVectorLayer(uri.uri(), 'pyarchinit_caratterizzazioni_view', 'spatialite')


			if  layerCA.isValid() == True:
				CALayerId = layerCA.getLayerID()
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'previewCAstyle.qml')
				layerCA.loadNamedStyle(style_path)
				QgsMapLayerRegistry.instance().addMapLayer(layerCA, True)
			"""

			uri.setDataSource('','pyarchinit_quote_view', 'Geometry', gidstr, "gid")
			layerQUOTE=QgsVectorLayer(uri.uri(), 'pyarchinit_quote_view', 'spatialite')
			if  layerQUOTE.isValid() == True:
				QgsMapLayerRegistry.instance().addMapLayer(layerQUOTE, True)
				

			uri.setDataSource('','pyarchinit_pyuscarlinee_view', 'Geometry', gidstr, "gid")
			layerQUOTE=QgsVectorLayer(uri.uri(), 'pyarchinit_pyuscarlinee_view', 'spatialite')
			if  layerQUOTE.isValid() == True:
				QgsMapLayerRegistry.instance().addMapLayer(layerQUOTE, True)

		elif settings.SERVER == 'postgres':

			uri = QgsDataSourceURI()
			# set host name, port, database name, username and password
		
			uri.setConnection(settings.HOST, settings.PORT, settings.DATABASE, settings.USER, settings.PASSWORD)

			gidstr =  id_us = "id_us = " + str(data[0].id_us)
			if len(data) > 1:
				for i in range(len(data)):
					gidstr += " OR id_us = " + str(data[i].id_us)


			srs = QgsCoordinateReferenceSystem(self.SRS, QgsCoordinateReferenceSystem.PostgisCrsId)

			uri.setDataSource("public", "pyarchinit_us_view", "the_geom", gidstr, "gid")
			layerUS = QgsVectorLayer(uri.uri(), "Unita' Stratigrafiche", "postgres")
		
			if  layerUS.isValid() == True:
				layerUS.setCrs(srs)
				self.USLayerId = layerUS.getLayerID()
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'us_caratterizzazioni.qml')
				layerUS.loadNamedStyle(style_path)
				QgsMapLayerRegistry.instance().addMapLayer(layerUS, True)
			
			"""
			uri.setDataSource("public", "pyarchinit_uscaratterizzazioni_view", "the_geom", gidstr, "gid")
			layerCA = QgsVectorLayer(uri.uri(), "Caratterizzazioni US", "postgres")
			
			if layerCA.isValid() == True:
				layerCA.setCrs(srs)
				CALayerId = layerCA.getLayerID()
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'previewCAstyle.qml')
				layerCA.loadNamedStyle(style_path)
				QgsMapLayerRegistry.instance().addMapLayer(layerCA, True)
			"""

			uri.setDataSource("public", "pyarchinit_quote_view", "the_geom", gidstr, "gid")
			layerQUOTE = QgsVectorLayer(uri.uri(), "Quote Unita' Stratigrafiche", "postgres")

			if layerQUOTE.isValid() == True:
				layerQUOTE.setCrs(srs)
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'stile_quote.qml')
				layerQUOTE.loadNamedStyle(style_path)
				try:
					QgsMapLayerRegistry.instance().addMapLayer(layerQUOTE, True)
				except Exception, e:
					pass
					#f = open('/test_ok.txt','w')
					#f.write(str(e))
					#f.close()

			uri.setDataSource("public", "pyarchinit_pyuscarlinee_view", "the_geom", gidstr, "gid")
			layerCA = QgsVectorLayer(uri.uri(), "Caratterizzazioni US linee", "postgres")
			"""
			if layerCA.isValid() == True:
				layerCA.setCrs(srs)
				CALayerId = layerCA.getLayerID()
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'caratterizzazioni_linee.qml')
				layerCA.loadNamedStyle(style_path)
				QgsMapLayerRegistry.instance().addMapLayer(layerCA, True)
			"""
	def charge_vector_layers_periodo(self, cont_per):
		self.cont_per = str(cont_per)
		#Clean Qgis Map Later Registry
		#QgsMapLayerRegistry.instance().removeAllMapLayers()
		# Get the user input, starting with the table name

		#self.find_us_cutted(data)

		cfg_rel_path = os.path.join(os.sep,'pyarchinit_DB_folder', 'config.cfg')
		file_path = ('%s%s') % (self.HOME, cfg_rel_path)
		conf = open(file_path, "r")
		con_sett = conf.read()
		conf.close()

		settings = Settings(con_sett)
		settings.set_configuration()

		if settings.SERVER == 'sqlite':
			pass
			#non attivato
			"""
			sqliteDB_path = os.path.join(os.sep,'pyarchinit_DB_folder', 'pyarchinit_db.sqlite')
			db_file_path = ('%s%s') % (self.HOME, sqliteDB_path)

			gidstr =  id_us = "id_us = '" + str(data[0].id_us) +"'"
			if len(data) > 1:
				for i in range(len(data)):
					gidstr += " OR id_us = '" + str(data[i].id_us) +"'"

			uri = QgsDataSourceURI()
			uri.setDatabase(db_file_path)

			uri.setDataSource('','pyarchinit_us_view', 'Geometry', gidstr)
			layerUS=QgsVectorLayer(uri.uri(), 'pyarchinit_us_view', 'spatialite')

			if  layerUS.isValid() == True:
				self.USLayerId = layerUS.getLayerID()
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'us_caratterizzazioni.qml')
				layerUS.loadNamedStyle(style_path)
				QgsMapLayerRegistry.instance().addMapLayer(layerUS, True)

			uri.setDataSource('','pyarchinit_caratterizzazioni_view', 'Geometry', gidstr)
			layerCA=QgsVectorLayer(uri.uri(), 'pyarchinit_caratterizzazioni_view', 'spatialite')

			if  layerCA.isValid() == True:
				CALayerId = layerCA.getLayerID()
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'previewCAstyle.qml')
				layerCA.loadNamedStyle(style_path)
				QgsMapLayerRegistry.instance().addMapLayer(layerCA, True)

			uri.setDataSource('','pyarchinit_quote_view', 'Geometry', gidstr)
			layerQUOTE=QgsVectorLayer(uri.uri(), 'pyarchinit_quote_view', 'spatialite')
			if  layerQUOTE.isValid() == True:
				QgsMapLayerRegistry.instance().addMapLayer(layerQUOTE, True)


			uri.setDataSource('','pyarchinit_pyuscarlinee_view', 'Geometry', gidstr)
			layerQUOTE=QgsVectorLayer(uri.uri(), 'pyarchinit_pyuscarlinee_view', 'spatialite')
			if  layerQUOTE.isValid() == True:
				QgsMapLayerRegistry.instance().addMapLayer(layerQUOTE, True)
			"""
		elif settings.SERVER == 'postgres':

			uri = QgsDataSourceURI()
			# set host name, port, database name, username and password

			uri.setConnection(settings.HOST, settings.PORT, settings.DATABASE, settings.USER, settings.PASSWORD)

			cont_per_string =  "cont_per = '" + self.cont_per + "' OR cont_per LIKE '" + self.cont_per + "/%' OR cont_per LIKE '%/" + self.cont_per + "' OR cont_per LIKE '%/" + self.cont_per + "/%'"


			srs = QgsCoordinateReferenceSystem(self.SRS, QgsCoordinateReferenceSystem.PostgisCrsId)

			uri.setDataSource("public", "pyarchinit_us_view", "the_geom", cont_per_string, "gid")
			layerUS = QgsVectorLayer(uri.uri(), "Unita' Stratigrafiche", "postgres")

			if  layerUS.isValid() == True:
				layerUS.setCrs(srs)
				self.USLayerId = layerUS.getLayerID()
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'us_caratterizzazioni.qml')
				layerUS.loadNamedStyle(style_path)
				QgsMapLayerRegistry.instance().addMapLayer(layerUS, True)

			uri.setDataSource("public", "pyarchinit_quote_view", "the_geom", cont_per_string, "gid")
			layerQUOTE = QgsVectorLayer(uri.uri(), "Quote Unita' Stratigrafiche", "postgres")

			if layerQUOTE.isValid() == True:
				layerQUOTE.setCrs(srs)
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'stile_quote.qml')
				layerQUOTE.loadNamedStyle(style_path)
				try:
					QgsMapLayerRegistry.instance().addMapLayer(layerQUOTE, True)
				except Exception, e:
					pass
					#f = open('/test_ok.txt','w')
					#f.write(str(e))
					#f.close()

			uri.setDataSource("public", "pyarchinit_pyuscarlinee_view", "the_geom", cont_per_string, "gid")
			layerCAL = QgsVectorLayer(uri.uri(), "Caratterizzazioni US linee", "postgres")

			if layerCAL.isValid() == True:
				layerCAL.setCrs(srs)
				CALayerId = layerCAL.getLayerID()
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'caratterizzazioni_linee.qml')
				layerCAL.loadNamedStyle(style_path)
				QgsMapLayerRegistry.instance().addMapLayer(layerCAL, True)


	"""
	def find_us_cutted(self, gl):
		gid_list = gl
		lista_rapporti = []
		for i in range(len(gid_list)):
			lista_rapporti.append([gid_list[i].sito,
			 						gid_list[i].area,
									gid_list[i].us,
									gid_list[i].rapporti])
		
		for i in lista_rapporti:
			pass
		"""
		

	def loadMapPreview(self, gidstr):
		""" if has geometry column load to map canvas """
		layerToSet = []
		
		srs = QgsCoordinateReferenceSystem(self.SRS, QgsCoordinateReferenceSystem.PostgisCrsId)
		
		
		sqlite_DB_path = ('%s%s%s') % (self.HOME, os.sep, "pyarchinit_DB_folder")
		path_cfg = ('%s%s%s') % (sqlite_DB_path, os.sep, 'config.cfg')

		conf = open(path_cfg, "r")
		con_sett = conf.read()
		conf.close()

		settings = Settings(con_sett)
		settings.set_configuration()

		uri = QgsDataSourceURI()
		# set host name, port, database name, username and password
		
		uri.setConnection(settings.HOST, settings.PORT, settings.DATABASE, settings.USER, settings.PASSWORD)
		
		#layerUS
		uri.setDataSource("public", "pyarchinit_us_view", "the_geom", gidstr, "id_us")
		layerUS = QgsVectorLayer(uri.uri(), "Unita' Stratigrafiche", "postgres")

		if layerUS.isValid() == True:
			self.USLayerId = layerUS.getLayerID()
			style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'us_caratterizzazioni.qml')
			layerUS.loadNamedStyle(style_path)
			QgsMapLayerRegistry.instance().addMapLayer(layerUS, False)
			layerToSet.append(QgsMapCanvasLayer(layerUS, True, False))

		#layerCA
		"""
		uri.setDataSource("public", "pyarchinit_uscaratterizzazioni_view", "the_geom", gidstr, "id_us")
		layerCA = QgsVectorLayer(uri.uri(), "Caratterizzazioni US", "postgres")

		if layerCA.isValid() == True:
			style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'previewCAstyle.qml')
			layerCA.loadNamedStyle(style_path)
			QgsMapLayerRegistry.instance().addMapLayer(layerCA, False)
			layerToSet.append(QgsMapCanvasLayer(layerCA, True, False))
		"""

		#layerQuote
		uri.setDataSource("public", "pyarchinit_quote_view", "the_geom", gidstr, "id_us")
		layerQUOTE = QgsVectorLayer(uri.uri(), "Quote", "postgres")

		if layerQUOTE.isValid() == True:
			style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'stile_quote.qml')
			layerQUOTE.loadNamedStyle(style_path)
			QgsMapLayerRegistry.instance().addMapLayer(layerQUOTE, False)
			layerToSet.append(QgsMapCanvasLayer(layerQUOTE, True, False))

			uri.setDataSource("public", "pyarchinit_pyuscarlinee_view", "the_geom", cont_per_string, "gid")
			layerCAL = QgsVectorLayer(uri.uri(), "Caratterizzazioni US linee", "postgres")

			if layerCAL.isValid() == True:
				layerCAL.setCrs(srs)
				CALayerId = layerCAL.getLayerID()
				style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'caratterizzazioni_linee.qml')
				layerCAL.loadNamedStyle(style_path)
				QgsMapLayerRegistry.instance().addMapLayer(layerCAL, True)

		return layerToSet

	"""
	def addRasterLayer(self):
		fileName = "/rimini_1_25000/Rimini_25000_g.tif"
		fileInfo = QFileInfo(fileName)
		baseName = fileInfo.baseName()
		rlayer = QgsRasterLayer(fileName, baseName)

		if not rlayer.isValid():
			QMessageBox.warning(self, "TESTER", "PROBLEMA DI CARICAMENTO RASTER" + str(baseName),	 QMessageBox.Ok)
		
		srs = QgsCoordinateReferenceSystem(3004, QgsCoordinateReferenceSystem.PostgisCrsId)
		rlayer.setCrs(srs)
		# add layer to the registry
		QgsMapLayerRegistry.instance().addMapLayer(rlayer);
	
		self.canvas = QgsMapCanvas()
		self.canvas.setExtent(rlayer.extent())

		# set the map canvas layer set
		cl = QgsMapCanvasLayer(rlayer)
		layers = [cl]
		self.canvas.setLayerSet(layers)
	"""

	#iface custom methods
	def dataProviderFields(self):
		fields = self.iface.mapCanvas().currentLayer().dataProvider().fields()
		return fields
		
	def selectedFeatures(self):
		selected_features = self.iface.mapCanvas().currentLayer().selectedFeatures()
		return selected_features

	def findFieldFrDict(self, fn):
		self.field_name = fn
		fields_dict = self.dataProviderFields()
		for k in fields_dict:
			if fields_dict[k].name() == self.field_name:
				res = k
		return res

	def findItemInAttributeMap(self, fp, fl):
		self.field_position = fp
		self.features_list = fl
		value_list = []
		for item in self.iface.mapCanvas().currentLayer().selectedFeatures():
			value_list.append(item.attributeMap().__getitem__(self.field_position).toString())
		return value_list

class Order_layers:

	LISTA_US = [] #lista che contiene tutte le US singole prese dai singoli rapporti stratigrafici
	DIZ_ORDER_LAYERS = {} #contiene una serie di chiavi valori dove la chiave e' il livello di ordinamento e il valore l'US relativa
	MAX_VALUE_KEYS = -1 #contiene l'indice progressivo dei livelli del dizionario
	TUPLE_TO_REMOVING = [] #contiene le tuple da rimuovere dai rapporti stratigrafici man mano che si passa ad un livello successivo

	"""variabili di controllo di paradossi nei rapporti stratigrafici"""
	status = 0 #contiene lo stato della lunghezza della lista dei rapporti stratigrafici
	check_status = 0 #il valore aumenta se la lunghezza della lista dei rapporti stratigrafici non cambia. Va in errore dopo 4000 ripetizioni del loop stratigraficocambia 
	stop_while = '' #assume il valore 'stop' dopo 4000 ripetizioni ed esce dal loop

	def __init__(self, lr):
		self.lista_rapporti = lr #istanzia la classe con una lista di tuple rappresentanti i rapporti stratigrafici
		#f = open('C:\\test_matrix_1.txt', 'w') #to delete
		#f.write(str(self.lista_rapporti))
		#f.close()
		self.lista_rapporti.sort() #ordina la lista dei rapporti stratigrafici
		self.status = len(self.lista_rapporti) #assegna la lunghezza della lista dei rapporti per verificare se cambia nel corso del loop

	def main(self):
		#esegue la funzione per creare la lista valori delle US dai singoli rapporti stratigrafici
		self.add_values_to_lista_us()
		#finche la lista US contiene valori la funzione bool ritorna True e il ciclo while prosegue
		while bool(self.LISTA_US) == True:
				#viene eseguito il ciclo per ogni US contenuto nella lista delle US
				self.loop_on_lista_us()
		return self.DIZ_ORDER_LAYERS
		#self.print_values():

	def loop_on_lista_us(self):
		#se il valore di stop_while rimane vuoto (ovvero non vi sono paradossi stratigrafici) parte la ricerca del livello da assegnare all'US
		if self.stop_while == '':
			for i in self.LISTA_US:
				if self.check_position(i) == 1:#se la funzione check_position ritorna 1 significa che e' stata trovata l'US che va nel prossimo livello e in seguito viene rimossa
					self.LISTA_US.remove(i)
				else:
					#se il valore ritornato e' 0 significa che e' necessario passare all'US successiva in lista US e la lista delle tuple da rimuovere e' svuotata
					self.tuple_to_removing = []
				#se il valore di status non cambia significa che non e' stata trovata l'US da rimuovere. Se cio' accade per + di 4000 volte e' possibile che vi sia un paradosso e lo script va in errore
				if self.status == len(self.lista_rapporti):
					self.check_status += 1
					print self.check_status
					if self.check_status > 20:
						self.stop_while = 'stop'
				else:
					#se entro le 4000 ricerche il valore cambia il check status torna a 0 e lo script va avanti
					self.check_status = 0
		else:
			#ferma il loop ma va in errore (baco da correggere)
			error = MyError('error')
			raise error

	def add_values_to_lista_us(self):
		#crea la lista valori delle US dai singoli rapporti stratigrafici
		for i in self.lista_rapporti:
			if i[0] == i[1]:
				pass
			else:
				if self.LISTA_US.__contains__(i[0]) == False:
					self.LISTA_US.append(i[0])
				if self.LISTA_US.__contains__(i[1]) == False:
					self.LISTA_US.append(i[1])

	def check_position(self, n):
		#riceve un numero di US dalla lista_US
		num_us = n
		#assegna 0 alla variabile check
		check = 0
		#inizia l'iterazione sUlla lista rapporti
		for i in self.lista_rapporti:
			#se la tupla assegnata a i contiene in prima posizione il numero di US, ovvero e' un'US che viene dopo le altre nella sequenza, check diventa 1 e non si ha un nuovo livello stratigrafico
			if i[1] == num_us:
				check = 1
			#se invece il valore e' sempre e solo in posizione 1, ovvero e' in cima ai rapporti stratigrafici viene assegnata la tupla di quei rapporti stratigrafici per essere rimossa in seguito
			elif i[0] == num_us:
				self.TUPLE_TO_REMOVING.append(i)
				#f = open('C:\\test_matrix_3.txt', 'w') #to delete
				#testo = str(i)
				#f.write(str(testo))
				#f.close()
		#se alla fine dell'iterazione check e' rimasto 0, significa che quell'US e' in cima ai rapporti stratigrafici e si passa all'assegnazione di un nuovo livello stratigrafico nel dizionario
		if check == 0:
			#viene eseguita la funzione di aggiunta valori al dizionario passandogli il numero di US
			self.add_key_value_to_diz(num_us)
			#vengono rimosse tutte le tuple in cui e' presente l'us assegnata al dizionario e la lista di tuple viene svuotata
			for i in self.TUPLE_TO_REMOVING:
				#f = open('C:\\test_matrix_2.txt', 'w') #to delete
				#testo = str(self.lista_rapporti) + ", ", str(i)
				#f.write(str(testo))
				#f.close()
				self.lista_rapporti.remove(i)
			self.TUPLE_TO_REMOVING = []
			#la funzione ritorna il valore 1
			return 1

	def add_key_value_to_diz(self, n):
		self.num_us_value = n #numero di US da inserire nel dizionario
		self.MAX_VALUE_KEYS += 1 #il valore globale del numero di chiave aumenta di 1
		self.DIZ_ORDER_LAYERS[self.MAX_VALUE_KEYS] = self.num_us_value #viene assegnata una nuova coppia di chiavi-valori
	"""
	def print_values(self):
		print "dizionario_valori per successione stratigrafica: ",self.DIZ_ORDER_LAYERS
		print "ordine di successione delle US: "
		for k in self.DIZ_ORDER_LAYERS.keys():
			print k
	"""
class MyError(Exception):
		def __init__(self, value):
			self.value = value
		def __str__(self):
			return repr(self.value)

##lista_rapporti = [(1,1),(3,5),(4,6), (6,8)]
##OL = Order_layers(lista_rapporti)
##print OL.main()a
