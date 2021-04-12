#!/usr/bin/python3
import os
import sys
from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox
import tkinter.ttk as ttk
import urllib.request
import ftplib
import gzip
import shutil


########################################################################################################################
# 	Initialize variables
########################################################################################################################
root = ''
acessTE = 0
acessGene = 0
acessGO = 0
acessChip = 0	#temporaire
# Variables qui contiennent les data
fichierTE = ''			# 1 seul fichier						(resultat TE)
fileGFFgenome = ''		# 1 fichier GFF							(annotation genome)
fileFNAgenome = ''		# 1 fichier FNA	meme repertoire que le GFF			(sequence genome)
ChipSeqDirectory = ''		# 1 dossier contenant les chipseq au format bed.gz		(1 chipseq = 1 fichier)
GeneOntologyOBO = ''		# 1 fichier provenant de GeneOntology				(liste des tous les GO)
GeneOntologyGI = ''		# 1 fichier provenant de NCBI					(equivalence GO GeneID)
ChipSEQdirectory = ''		# 1 repertoire qui contient les chipseq				(au format VisualTE3)
dictionary_organ = {}
dictionary_tissue = {}



########################################################################################################################
###	Unzip the chromosome file from NCBI
########################################################################################################################

def UnzipFile(file, pathVisualGenomes):	

	temp = pathVisualGenomes + '/' + file
	tempName = pathVisualGenomes + '/' + file[:len(file)-3]
	fichier = open(tempName, 'wb')
	f = gzip.GzipFile(temp, 'rb')
	file_content = f.read()
	fichier.write(file_content)
	fichier.close()

	os.remove(temp) 
	
	#UnzipFile(FNAaTelecharger, DossierTelecharger)
