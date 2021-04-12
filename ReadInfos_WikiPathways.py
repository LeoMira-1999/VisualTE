#!/usr/bin/python3
import sys
import os
import pandas as pd
import shutil

####################################################################################################################################
###	Copy Wiki Pathways from files
####################################################################################################################################

def CopyPathWaysFile(pathVisualDATA) :
	
	pathVisualWiki = pathVisualDATA + '/WikiPathWays'
	os.mkdir(pathVisualWiki)
	
	pathOriginWiki = os.getcwd() + '/Scripts/DATA/WikiPathWays/AllSVG/'
	
	for nomFichier in os.listdir(pathOriginWiki) :
		if(os.path.isdir(nomFichier) != True) :
			decoupe = nomFichier.split('_')
			nomFichier2 = pathOriginWiki + '/' + nomFichier
			nomFichier3 = pathVisualWiki + '/' + decoupe[len(decoupe)-2] + '.svg'
			shutil.copyfile(nomFichier2, nomFichier3)
	
			#print(nomFichier2, ' -> ', nomFichier3)
