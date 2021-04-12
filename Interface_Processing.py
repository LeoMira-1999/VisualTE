#!/usr/bin/python3
import os
import sys
from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox
import tkinter.ttk as ttk
import urllib.request
import ftplib
import time 
from . import Interface_SettingVariables
from . import ReadInfos_Compresse, ReadInfos_NCBIAnnotations, ReadInfos_GeneOntology, ReadInfos_TE, ReadInfos_RepeatMasker, ReadInfos_CHIPSeq, ReadInfos_WikiPathways

nbSeq_Assemble = 0
nameOrganism   = ''
maxSize        = 0
taxon          = 0
progressTask = ''



########################################################################################################################
# 	Run the process data
########################################################################################################################
def RunProcesses(pathVisualDATA, fileGFFgenome, fileFNAgenome, GeneOntologyOBO, GeneOntologyGI, fichierTE, textProcess) :
	
	global nbSeq_Assemble
	global nameOrganism
	global maxSize
	global taxon
	global progressTask
	nbLigneText = 1
	insertionText = str(nbLigneText) + '.0'
	
	########################################################################################################################
	###	Unzip the necessary files
	########################################################################################################################
	if fileGFFgenome[-3:] == '.gz' or fileFNAgenome[-3:] == '.gz' or GeneOntologyGI[-3:] == '.gz' :
		print("\tUnzip the necessary files ...")
		textProcess.insert(insertionText, 'Unzip the necessary files ...\n')
		nbLigneText += 1
		insertionText = str(nbLigneText) + '.0'
	
	if fileGFFgenome[-3:] == '.gz' :
		ReadInfos_Compresse.UnzipFile(fileGFFgenome, pathVisualDATA)
	if fileFNAgenome[-3:] == '.gz' :
		ReadInfos_Compresse.UnzipFile(fileFNAgenome, pathVisualDATA)
	if GeneOntologyGI[-3:] == '.gz' :
		ReadInfos_Compresse.UnzipFile(GeneOntologyGI, pathVisualDATA)
		
		
		
	########################################################################################################################
	###	Read data files
	########################################################################################################################
	
	# Choice of the script that reads the TE results
	# Extract the Repbase data
	textAEcrire = 'Extracting TE data from Repbase sequences \n'
	textProcess.insert(insertionText, textAEcrire)
	nbLigneText += 1
	insertionText = str(nbLigneText) + '.0'
	print('\tExtracting TE data from Repbase sequences')
	Repbase = ReadInfos_TE.LireRepbase('SCRIPTS/DATA/Repbase/Data_Repbase.txt')
	
	textAEcrire = 'Extracting TE data from ' + fichierTE + '\n'
	textProcess.insert(insertionText, textAEcrire)
	nbLigneText += 1
	insertionText = str(nbLigneText) + '.0'
	print('\tExtracting TE data from', fichierTE)
	if fichierTE[-3:] == 'out' :
		ReadInfos_RepeatMasker.ReadRepeatMasker(fichierTE, Repbase, pathVisualDATA, Interface_SettingVariables.root, progressTask, textProcess, nbLigneText, insertionText)
	else :
		print("PAS ENCORE FAIT")
		
	# wait 1 seconde before to start the processing
	time.sleep(1.0) 
	
	
	
	
	
	# Extrait les donnees des fichier GFF de NCBI : genes, ncRNA ...
	textAEcrire = 'Extracting NCBI Annotation data from ' + fileGFFgenome + '\n'
	textProcess.insert(insertionText, textAEcrire)
	nbLigneText += 1
	insertionText = str(nbLigneText) + '.0'
	print('\tExtracting NCBI Annotation data from', fileGFFgenome)        
	nbSeq_Assemble, nameOrganism, maxSize, taxon, nbLigneText, dataFrame_Gene = ReadInfos_NCBIAnnotations.ReadGFF(fileGFFgenome, pathVisualDATA, Interface_SettingVariables.root, progressTask, textProcess, nbLigneText, insertionText)    
	# wait 1 seconde before to start the processing
	time.sleep(1.0) 
	
	
	
	
	
	# Extract the GeneOntology file for the selected genome
	textAEcrire = 'Extracting GeneOntology file from go-basic.obo \n'
	textProcess.insert(insertionText, textAEcrire)
	nbLigneText += 1
	insertionText = str(nbLigneText) + '.0'
	print('\tExtracting GeneOntology file from go-basic.obo') 
	ReadInfos_GeneOntology.ParsingGeneOntologyDefinition(GeneOntologyOBO, pathVisualDATA, 2)
	# wait 1 seconde before to start the processingO.SelectGenomeGO(pathVisu
	time.sleep(1.0) 
	
	
	
	
	
	# Copy files SVG from WikiPathways
	textAEcrire = 'Copy SVG files for WikiPathways \n'
	textProcess.insert(insertionText, textAEcrire)
	nbLigneText += 1
	insertionText = str(nbLigneText) + '.0'
	print('\tCopy SVG files for WikiPathways') 
	ReadInfos_WikiPathways.CopyPathWaysFile(pathVisualDATA)
	time.sleep(1.0) 
	
	
	
	
	
	# Transform ChipSEQ DATA
	textAEcrire = 'Transform ChipSEQ data ... \n'
	textProcess.insert(insertionText, textAEcrire)
	nbLigneText += 1
	insertionText = str(nbLigneText) + '.0'
	pathVisualDATA2 = pathVisualDATA + '/ChipSeq/'
	ReadInfos_CHIPSeq.TransformChipSEQ(pathVisualDATA, pathVisualDATA2, Interface_SettingVariables.root, progressTask, textProcess, nbLigneText, insertionText)
	
	# wait 1 seconde before to start the processing
	time.sleep(1.0) 
	
	
	
	########################################################################################################################
	# Finish the processing data
	Interface_SettingVariables.root.destroy()
	
	
	
	
	
########################################################################################################################
# 	Create the main interface
########################################################################################################################
def InterfaceProcessDATA(pathVisualDATA, fileGFFgenome, fileFNAgenome, GeneOntologyOBO, GeneOntologyGI, fichierTE) :

	global progressTask
	
	### Style de l'interface
	Interface_SettingVariables.root = Tk()
	Interface_SettingVariables.root.configure(background='#F5F5FF')
	Interface_SettingVariables.root.title("Making VisualTE3 with your data")     # Add a title
	Interface_SettingVariables.root.minsize(800, 800)

	style = ttk.Style()
	style.theme_settings("default", {
		"TCombobox": {
			"configure": {"padding": 20, 'font':24},
			"map": {
				"background": [("active", "#8888FF"), ("!disabled", "#F5F5FF")],
				"fieldbackground": [("!disabled", "#F5F5FF")],
				"foreground": [("focus", "#8888FF"), ("!disabled", "black")]
	       		}
	   	},

		"TButton" : {
			"configure": {"padding": 20, 'relief':'flat', 'font':24},
			"map" : { 
				"foreground" : [('pressed', '#8888FF'), ('active', '#8888FF'), ('pressed', "#F5F5FF")],
				"background" : [("active", "#F5F5FF"), ("!disabled", "#F5F5FF"), ('pressed', "#F5F5FF")]
				},
		},
	})
	
	
	
	
	
	########################################################################################################################
	# separateur
	espaceLabel6 = Label(Interface_SettingVariables.root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel6.config(font=(12))
	espaceLabel6.grid(row = 0, column = 0, columnspan = 7, sticky=EW)
	
	# titre de la selection 
	Choix = Label(Interface_SettingVariables.root, text = 'Processing DATA ...', borderwidth=5, bg="#F5F5FF")
	Choix.config(font=(24))
	Choix.grid(row = 1, column = 0, columnspan = 7, sticky=EW)

	# separateur
	espaceLabel1 = Label(Interface_SettingVariables.root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel1.config(font=(12))
	espaceLabel1.grid(row = 2, column = 0, columnspan = 7, sticky=EW)
	
	
	
	
	
	########################################################################################################################
	# textnote that contains the processing step
	scrollbarX = Scrollbar(Interface_SettingVariables.root, orient='horizontal')
	scrollbarY = Scrollbar(Interface_SettingVariables.root)
	scrollbarX.grid(row = 10, column = 1, columnspan = 5, rowspan=1, sticky=NSEW)
	scrollbarY.grid(row = 3, column = 5, columnspan = 1, rowspan=7, sticky=NSEW)
	
	
	espaceLabel40 = Label(Interface_SettingVariables.root, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel40.config(font=(24))
	espaceLabel40.grid(row = 3, column = 0, columnspan = 1, rowspan=7, sticky=EW)
	
	textProcess = Text(Interface_SettingVariables.root, height=7, wrap=NONE, yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
	textProcess.grid(row = 3, column = 1, columnspan = 4, rowspan=7, sticky=NSEW)
	scrollbarY.config(command=textProcess.yview)
	scrollbarX.config(command=textProcess.xview)
	
	espaceLabel34 = Label(Interface_SettingVariables.root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel34.config(font=(12))
	espaceLabel34.grid(row = 3, column = 6, columnspan = 1, rowspan=7, sticky=EW)
	
	
	
	espaceLabel401 = Label(Interface_SettingVariables.root, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel401.config(font=(24))
	espaceLabel401.grid(row = 10, column = 0, columnspan = 1, rowspan=1, sticky=EW)
	
	espaceLabel341 = Label(Interface_SettingVariables.root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel341.config(font=(12))
	espaceLabel341.grid(row = 10, column = 6, columnspan = 1, rowspan=1, sticky=EW)
	
	
	
	
	
	########################################################################################################################
	# separateur
	espaceLabel63 = Label(Interface_SettingVariables.root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel63.config(font=(12))
	espaceLabel63.grid(row = 11, column = 0, columnspan = 7, sticky=EW)
			
			
			
			
			
	########################################################################################################################		
	espaceLabel13 = Label(Interface_SettingVariables.root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel13.config(font=(12))
	espaceLabel13.grid(row = 12, column = 0, columnspan = 1, sticky=EW)
	
	progressTask = ttk.Progressbar(Interface_SettingVariables.root, orient="horizontal", length=500, mode = 'determinate')
	progressTask.grid(row = 12, column = 1, columnspan = 5, sticky=EW)
	
	espaceLabel14 = Label(Interface_SettingVariables.root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel14.config(font=(12))
	espaceLabel14.grid(row = 12, column = 6, columnspan = 1, sticky=EW)
	
	
	
	
	
	########################################################################################################################
	# separateur
	espaceLabel633 = Label(Interface_SettingVariables.root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel633.config(font=(12))
	espaceLabel633.grid(row = 13, column = 0, columnspan = 7, sticky=EW)
	
	
	
	
	
	
			
	########################################################################################################################
	# Run the different processes
	time.sleep(1.0) 
	RunProcesses(pathVisualDATA, fileGFFgenome, fileFNAgenome, GeneOntologyOBO, GeneOntologyGI, fichierTE, textProcess)
	
	Interface_SettingVariables.root.mainloop()
	
	
	return nbSeq_Assemble, nameOrganism, maxSize, taxon, Interface_SettingVariables.dictionary_organ, Interface_SettingVariables.dictionary_tissue
