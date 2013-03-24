#!/usr/bin/env python
# encoding: utf-8
"""
pyarchinit_media_utility.py
Created by Pyarchinit on 2010_11_25.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""


import os, sys 
from Image import *
import Image
from pyarchinit_conn_strings  import *

class Media_utility:
	
	def resample_images(self, mid, ip, i, o, ts):
		self.max_num_id = mid
		self.input_path = ip
		self.infile = i
		self.outpath = o
		self.thumb_suffix = ts
	

		size = 300, 300
		infile = str(self.input_path)
		outfile = ('%s%s_%s%s') % (self.outpath,str(self.max_num_id), os.path.splitext(self.infile)[0], self.thumb_suffix)
		im = Image.open(infile)
		im.thumbnail(size) 
		im.save(outfile, dpi=(100,100))

if __name__== '__main__':
	m = Media_utility()
	conn = Connection()
	thumb_path = conn.thumb_path()
	thumb_path_str = thumb_path['thumb_path']
	print thumb_path_str
	m.resample_images('/Users/pyarchinit/desktop/Archivio/', 'Immagine2.png', thumb_path_str, '_pay.png')
	

"""
listfiles = os.listdir(self.pathfiles)
for infile in listfiles:
	comp_file = ('%s/%s') % (self.pathfiles,infile)
	outfile = os.path.splitext(infile)[0] + "_pay.png"
	if infile != outfile: 
		try:
			im = Image.open(self.pathfiles + infile)
			print 'im', im
			im.thumbnail(size) 
			im.save(self.outputpath + outfile, dpi=(100,100)) 

		except IOError: 
			print "cannot create thumbnail for", infile
"""