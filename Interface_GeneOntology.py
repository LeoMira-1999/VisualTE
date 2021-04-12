#!/usr/bin/python3
import os
import sys
from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox
import tkinter.ttk as ttk
import shutil
import gzip
import urllib.request
import ftplib
import requests
from . import Interface_SettingVariables



progressGOBasic = ''
progressGENE2GO = ''
newWindow = ''

# Adresse pour les relations GO et GeneID
# http://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2go.gz
# Adresse pour la liste des GO
# http://purl.obolibrary.org/obo/go/go-basic.obo





########################################################################################################################
### 	Download the 2 GeneOntology
########################################################################################################################
def DownloadGOFile(pathVisualDATA) :
	
	global newWindow
	global progressGOBasic
	global progressGENE2GO
	
	temp = pathVisualDATA + '/go-basic.obo'
	url = 'http://purl.obolibrary.org/obo/go/go-basic.obo'
	response = requests.get(url, stream=True)
	fileSize = int(response.headers['Content-length'])
	chunkSize = round(fileSize / 500)+1
	progressGOBasic["value"] = 0
	progressGOBasic["maximum"] = fileSize
	progressGOBasic.start()
	
	internetFile = open(temp, 'wb')
	for chunk in response.iter_content(chunk_size=chunkSize):
		internetFile.write(chunk)
		progressGOBasic.step(chunkSize)
		newWindow.update()
	
	
	temp = pathVisualDATA + '/gene2go.gz'
	url = 'http://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2go.gz'
	response = requests.get(url, stream=True)
	fileSize = int(response.headers['Content-length'])
	chunkSize = round(fileSize / 500)+1
	progressGENE2GO["value"] = 0
	progressGENE2GO["maximum"] = fileSize
	progressGENE2GO.start()
	
	internetFile = open(temp, 'wb')
	for chunk in response.iter_content(chunk_size=chunkSize):
		internetFile.write(chunk)
		progressGENE2GO.step(chunkSize)
		newWindow.update()
	
	
	newWindow.destroy()
	Interface_SettingVariables.acessGO = 1
	if (Interface_SettingVariables.acessTE == 1 and Interface_SettingVariables.acessGene == 1 
	and Interface_SettingVariables.acessGO and Interface_SettingVariables.acessChip == 1 
	and Interface_SettingVariables.ChipSEQdirectory != '') :
		Interface_SettingVariables.root.destroy()
	
	
	
	
	
########################################################################################################################
# 	Interface for Downloading the 2 GeneOntology
########################################################################################################################
def DownloadGO(pathVisualDATA) :
	
	global newWindow
	global progressGOBasic
	global progressGENE2GO
	
	newWindow = Toplevel(Interface_SettingVariables.root, borderwidth=5)
	newWindow.configure(background='#F5F5FF')
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
	# Separateur
	espaceLabel11 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel11.config(font=(12))
	espaceLabel11.grid(row = 0, column = 0, columnspan = 7, sticky=EW)
	
	
	
	
	
	########################################################################################################################
	# Create the progressbar go-basic.obo
	espaceLabel33 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel33.config(font=(12))
	espaceLabel33.grid(row = 1, column = 0, columnspan = 1, sticky=EW)

	warningLabel5 = Label(newWindow, text = 'Downloading GeneOntology List file', borderwidth=5, bg="#F5F5FF")
	warningLabel5.config(font=(24))
	warningLabel5.grid(row = 1, column = 1, columnspan = 5, sticky=EW)
	
	espaceLabel34 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel34.config(font=(12))
	espaceLabel34.grid(row = 1, column = 6, columnspan = 1, sticky=EW)
	
	espaceLabel3 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel3.config(font=(12))
	espaceLabel3.grid(row = 2, column = 0, columnspan = 1, sticky=EW)
	
	progressGOBasic = ttk.Progressbar(newWindow, orient="horizontal", length=500, mode = 'determinate')
	progressGOBasic.grid(row = 2, column = 1, columnspan = 5, sticky=EW)
	
	espaceLabel4 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel4.config(font=(12))
	espaceLabel4.grid(row = 2, column = 6, columnspan = 1, sticky=EW)
	
	
	
	
	
	########################################################################################################################
	# Separateur
	espaceLabel21 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel21.config(font=(12))
	espaceLabel21.grid(row = 3, column = 0, columnspan = 7, sticky=EW)
	
	
	
	
	
	########################################################################################################################
	# Create the progressbar gene2go
	espaceLabel133 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel133.config(font=(12))
	espaceLabel133.grid(row = 4, column = 0, columnspan = 1, sticky=EW)

	warningLabel15 = Label(newWindow, text = 'Downloading the Gene2GO file', borderwidth=5, bg="#F5F5FF")
	warningLabel15.config(font=(24))
	warningLabel15.grid(row = 4, column = 1, columnspan = 5, sticky=EW)
	
	espaceLabel134 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel134.config(font=(12))
	espaceLabel134.grid(row = 4, column = 6, columnspan = 1, sticky=EW)
	
	espaceLabel13 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel13.config(font=(12))
	espaceLabel13.grid(row = 5, column = 0, columnspan = 1, sticky=EW)
	
	progressGENE2GO = ttk.Progressbar(newWindow, orient="horizontal", length=500, mode = 'determinate')
	progressGENE2GO.grid(row = 5, column = 1, columnspan = 5, sticky=EW)
	
	espaceLabel14 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel14.config(font=(12))
	espaceLabel14.grid(row = 5, column = 6, columnspan = 1, sticky=EW)
	
	
	
	
	
	########################################################################################################################
	# Download the files
	DownloadGOFile(pathVisualDATA)
	
	
	
	
########################################################################################################################
### 	Open a new interface for selecting the Genomes files
########################################################################################################################
def getGObasic() :
	Interface_SettingVariables.GeneOntologyOBO = askopenfilename( filetypes=( ("All files", "*.*"), ("GeneOntology files", "*.obo") ) )
	
def getGOgene() :
	Interface_SettingVariables.GeneOntologyGI = askopenfilename( )





########################################################################################################################
# 	Save the sequence file 
########################################################################################################################
def closeGOWindow(newWindow, pathVisualDATA) :
	
	if Interface_SettingVariables.GeneOntologyOBO == '' or Interface_SettingVariables.GeneOntologyGI == '' :
		msg = messagebox.showinfo( "Error !", "One or two genome file is missing !")
	else :
		decoupe = Interface_SettingVariables.GeneOntologyOBO.split('/')
		copyFile = pathVisualDATA + '/' + decoupe[len(decoupe)-1]
		shutil.copyfile(Interface_SettingVariables.GeneOntologyOBO, copyFile)
		Interface_SettingVariables.GeneOntologyOBO = copyFile

		decoupe = Interface_SettingVariables.GeneOntologyGI.split('/')
		copyFile = pathVisualDATA + '/' + decoupe[len(decoupe)-1]
		shutil.copyfile(Interface_SettingVariables.GeneOntologyGI, copyFile)
		Interface_SettingVariables.GeneOntologyGI = copyFile
		
		newWindow.destroy()
		Interface_SettingVariables.acessGO = 1
		
		if Interface_SettingVariables.acessTE == 1 and Interface_SettingVariables.acessGene == 1 and Interface_SettingVariables.acessGO and Interface_SettingVariables.acessChip == 1:
			Interface_SettingVariables.root.destroy()
		
		
		
		
		
########################################################################################################################
### 	Open a new interface for selecting the Genomes files
########################################################################################################################
def LocalGeneOntology(pathVisualDATA) :

	newWindow = Toplevel(Interface_SettingVariables.root, borderwidth=5)
	newWindow.configure(background='#F5F5FF')
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
	
	
	
	
	##########################################################################################################################################
	# separateur
	espaceLabel1 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel1.config(font=(12))
	espaceLabel1.grid(row = 0, column = 0, columnspan = 7, sticky=EW)
	
	
	
	
	
	##########################################################################################################################################
	# label de selection de l'annotation
	espaceLabel50 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel50.config(font=(12))
	espaceLabel50.grid(row = 1, column = 0, columnspan = 1, sticky=EW)

	warningLabel = Label(newWindow, text = 'Select your two GeneOntology files', borderwidth=5, bg="#F5F5FF")
	warningLabel.config(font=(24))
	warningLabel.grid(row = 1, column = 1, columnspan = 7, sticky=EW)

	espaceLabel51 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel51.config(font=(12))
	espaceLabel51.grid(row = 1, column = 8, columnspan = 1, sticky=EW)
	

	
	
	
	# button de choix de l'annotation
	espaceLabel20 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel20.config(font=(12))
	espaceLabel20.grid(row = 2, column = 0, columnspan = 1, sticky=EW)
		
	GObasic = Frame(newWindow, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	GObasic.grid(row = 2, column = 1, columnspan = 7, sticky=EW)
	buttonBasic = ttk.Button(GObasic, text="GO basic List", command = getGObasic)
	buttonBasic.pack(expand=TRUE, fill=BOTH)

	espaceLabel21 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel21.config(font=(12))
	espaceLabel21.grid(row = 2, column = 8, columnspan = 1, sticky=EW)
	
	
	
	
	
	# button de choix de l'annotation
	espaceLabel230 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel230.config(font=(12))
	espaceLabel230.grid(row = 3, column = 0, columnspan = 1, sticky=EW)
		
	GOgene = Frame(newWindow, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	GOgene.grid(row = 3, column = 1, columnspan = 7, sticky=EW)
	buttonBasic = ttk.Button(GOgene, text="Gene2GO", command = getGOgene)
	buttonBasic.pack(expand=TRUE, fill=BOTH)

	espaceLabel231 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel231.config(font=(12))
	espaceLabel231.grid(row = 3, column = 8, columnspan = 1, sticky=EW)
	
	
	
	
	
	##########################################################################################################################################
	# separateur
	espaceLabel11 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel11.config(font=(12))
	espaceLabel11.grid(row = 4, column = 0, columnspan = 7, sticky=EW)
	
	
	
	
	
	##########################################################################################################################################
	# Creation du boutton submit Genomes choice
	espaceLabel41 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel41.config(font=(12))
	espaceLabel41.grid(row = 5, column = 0, columnspan = 1, sticky=EW)
	
	fDATA = Frame(newWindow, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	fDATA.grid(row = 5, column = 1, columnspan = 7, sticky=NSEW)
	
	SubmitDATA = ttk.Button(fDATA, text="Submit GeneOntology Files", command = lambda: closeGOWindow(newWindow, pathVisualDATA) )
	SubmitDATA.pack(expand=TRUE, fill=BOTH)

	espaceLabel42 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel42.config(font=(12))
	espaceLabel42.grid(row = 5, column = 8, columnspan = 1, sticky=EW)





	##########################################################################################################################################
	# separateur
	espaceLabel3 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel3.config(font=(24))
	espaceLabel3.grid(row = 6, column = 0, columnspan = 9, sticky=EW)
	
	
	
	
