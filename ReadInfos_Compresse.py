#!/usr/bin/python3
import sys
import os
import gzip

########################################################################################################################
###	Unzip the file present in Download directory
########################################################################################################################

def UnzipFile(file, path):	

	decoupe = file.split('/')
	nomSimple = decoupe[len(decoupe)-1]
	compressFile = path + '/' + nomSimple
	decompressFile = path + '/' + nomSimple[:len(nomSimple)-3]
	
	fichier = open(decompressFile, 'wb')
	f = gzip.GzipFile(compressFile, 'rb')
	file_content = f.read()
	fichier.write(file_content)
	fichier.close()

	os.remove(compressFile) 
