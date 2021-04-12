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
from . import Interface_SettingVariables, ReadInfos_CHIPSeq


progressChipSeq = ''
newWindow = ''


########################################################################################################################
###	Get the path of the ChipSeq files # temporary only ENCODE website
########################################################################################################################
def downloadENCODE(GenomeName, pathVisualDATA) :
	
	global progressChipSeq
	global newWindow
	
	pathVisualDATA2 = pathVisualDATA + '/ChipSeq/'
	os.mkdir(pathVisualDATA2)
	
	
	GenomeName = GenomeName.replace(' ', '+')
	premiereListe = ReadInfos_CHIPSeq.TelechargeExperiments(GenomeName)
	listeBed =  []
	for i in range(0, len(premiereListe), 1) :
		ReadInfos_CHIPSeq.DownloadExperimentsDATA(premiereListe[i])
		listeBedTemp = ReadInfos_CHIPSeq.readExperiments(premiereListe[i])
		if len(listeBedTemp) > 0 : 
			listeBed.extend(listeBedTemp)
	
	chunkSize = round(len(listeBed) / 1000)+1
	progressChipSeq["value"] = 0
	progressChipSeq["maximum"] = 1000
	progressChipSeq.start()
	
	# Download the complete set of file from ENCODE
	for i in range(0, len(listeBed), 1) :
		print(i+1, ' / ', len(listeBed), '  ', listeBed[i])
		time.sleep(0.1)
		ReadInfos_CHIPSeq.ExtractExperimentInfos(listeBed[i], pathVisualDATA, progressChipSeq, newWindow, chunkSize)
	
	Interface_SettingVariables.acessChip = 1
	Interface_SettingVariables.ChipSEQdirectory = pathVisualDATA
	newWindow.destroy()
	if (Interface_SettingVariables.acessTE == 1 and Interface_SettingVariables.acessGene == 1 
	and Interface_SettingVariables.acessGO and Interface_SettingVariables.acessChip == 1 
	and Interface_SettingVariables.ChipSEQdirectory != '') :
		Interface_SettingVariables.root.destroy()










########################################################################################################################
###	Get the path of the ChipSeq files # temporary only ENCODE website
########################################################################################################################
def DownloadChipSEQ(pathVisualDATA) :
	
	global progressChipSeq
	global newWindow
	
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
	espaceLabel1.grid(row = 0, column = 0, columnspan = 9, sticky=EW)
	
	
	
	##########################################################################################################################################
	# label de selection de l'annotation
	espaceLabel50 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel50.config(font=(12))
	espaceLabel50.grid(row = 1, column = 0, columnspan = 1, sticky=EW)

	warningLabel = Label(newWindow, text = 'Select your ENCODE genome', borderwidth=5, bg="#F5F5FF")
	warningLabel.config(font=(24))
	warningLabel.grid(row = 1, column = 1, columnspan = 7, sticky=EW)

	espaceLabel51 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel51.config(font=(12))
	espaceLabel51.grid(row = 1, column = 8, columnspan = 1, sticky=EW)
	
	
	
	##########################################################################################################################################
	# separateur
	espaceLabel4 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel4.config(font=(12))
	espaceLabel4.grid(row = 2, column = 0, columnspan = 9, sticky=EW)
	
	
	
	
	espaceLabel33 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel33.config(font=(12))
	espaceLabel33.grid(row = 3, column = 0, columnspan = 1, sticky=EW)

	fGenome = Frame(newWindow, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	fGenome.grid(row = 3, column = 1, columnspan = 7, sticky=EW)

	GenomeName = StringVar()
	GenomeName.set('')
	familleTE = Entry(fGenome, borderwidth=5, bg="#F5F5FF", textvariable = GenomeName)	
	familleTE.config(font=(24))
	familleTE.pack(expand=TRUE, fill=BOTH)
	
	espaceLabel171 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel171.config(font=(12))
	espaceLabel171.grid(row = 3, column = 8, columnspan = 1, sticky=EW)
	
	
	
	##########################################################################################################################################
	# separateur
	espaceLabel5 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel5.config(font=(12))
	espaceLabel5.grid(row = 4, column = 0, columnspan = 9, sticky=EW)
	
	
	
	########################################################################################################################
	# Creation du boutton submit Genomes choice
	espaceLabel9 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel9.config(font=(12))
	espaceLabel9.grid(row = 5, column = 0, columnspan = 1, sticky=EW)

	fDATA = Frame(newWindow, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	fDATA.grid(row = 5, column = 1, columnspan = 7, sticky=EW)
	
	SubmitDATA = ttk.Button(fDATA, text="Submit Genome", command = lambda: downloadENCODE(GenomeName.get(), pathVisualDATA) )
	SubmitDATA.pack(expand=TRUE, fill=BOTH)

	espaceLabel10 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel10.config(font=(12))
	espaceLabel10.grid(row = 5, column = 8, columnspan = 1, sticky=EW)
	
	
	
	##########################################################################################################################################
	# separateur
	espaceLabel35 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel35.config(font=(12))
	espaceLabel35.grid(row = 6, column = 0, columnspan = 9, sticky=EW)
	
	
	
	##########################################################################################################################################
	# Progress BAR
	espaceLabel36 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel36.config(font=(12))
	espaceLabel36.grid(row = 7, column = 0, columnspan = 1, sticky=EW)
	
	progressChipSeq = ttk.Progressbar(newWindow, orient="horizontal", length=500, mode = 'determinate')
	progressChipSeq.grid(row = 7, column = 1, columnspan = 7, sticky=EW)
	
	espaceLabel46 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel46.config(font=(12))
	espaceLabel4.grid(row = 7, column = 8, columnspan = 1, sticky=EW)
	
	
	
	##########################################################################################################################################
	# separateur
	espaceLabel535 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel535.config(font=(12))
	espaceLabel535.grid(row = 8, column = 0, columnspan = 9, sticky=EW)
	
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Get the path of the ChipSeq files
########################################################################################################################
def getENCODE(pathVisualDATA) :
	
	global progressChipSeq
	global newWindow
	
	Interface_SettingVariables.ChipSEQdirectory = askdirectory( )
	if Interface_SettingVariables.ChipSEQdirectory == '' :
		msg = messagebox.showinfo( "Error !", "The ChipSeq directory is missing !")
	else :
		Interface_SettingVariables.acessChip = 1
		pathVisualDATA2 = pathVisualDATA + '/ChipSeq/'
		os.mkdir(pathVisualDATA2)
					
		# copy the local files in VisualTE directory
		for nomFichier in os.listdir(Interface_SettingVariables.ChipSEQdirectory):
			if(os.path.isdir(nomFichier) != True):
				originFile = Interface_SettingVariables.ChipSEQdirectory + '/' + nomFichier
				copyFile = pathVisualDATA2 + nomFichier
				shutil.copyfile(originFile, copyFile)
	
		newWindow.destroy()
		Interface_SettingVariables.ChipSEQdirectory = pathVisualDATA2
		if (Interface_SettingVariables.acessTE == 1 and Interface_SettingVariables.acessGene == 1 
		and Interface_SettingVariables.acessGO and Interface_SettingVariables.acessChip == 1 
		and Interface_SettingVariables.ChipSEQdirectory != '') :
			Interface_SettingVariables.root.destroy()
	
	
	
########################################################################################################################
### 	Select and Copy the TE file
########################################################################################################################
def LocalChipSEQ(pathVisualDATA) :
	
	global progressChipSeq
	global newWindow
	global dict_organ
	global dict_tissue
	
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
	espaceLabel1.grid(row = 0, column = 0, columnspan = 9, sticky=EW)
	
	
	
	
	
	##########################################################################################################################################
	# label de selection de l'annotation
	espaceLabel50 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel50.config(font=(12))
	espaceLabel50.grid(row = 1, column = 0, columnspan = 1, sticky=EW)

	warningLabel = Label(newWindow, text = 'Select your ChipSeq directory (bed file)', borderwidth=5, bg="#F5F5FF")
	warningLabel.config(font=(24))
	warningLabel.grid(row = 1, column = 1, columnspan = 7, sticky=EW)

	espaceLabel51 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel51.config(font=(12))
	espaceLabel51.grid(row = 1, column = 8, columnspan = 1, sticky=EW)
	
	
	
	
	
	##########################################################################################################################################
	# separateur
	espaceLabel2 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel2.config(font=(12))
	espaceLabel2.grid(row = 2, column = 0, columnspan = 9, sticky=EW)
	
	
	
	
	
	########################################################################################################################
	# Creation du boutton submit Genomes choice
	espaceLabel9 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel9.config(font=(12))
	espaceLabel9.grid(row = 3, column = 0, columnspan = 1, sticky=EW)

	fDATA = Frame(newWindow, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	fDATA.grid(row = 3, column = 1, columnspan = 7, sticky=EW)
	
	SubmitDATA = ttk.Button(fDATA, text="Submit ChipSeq directory", command = lambda: getENCODE(pathVisualDATA) )
	SubmitDATA.pack(expand=TRUE, fill=BOTH)

	espaceLabel10 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel10.config(font=(12))
	espaceLabel10.grid(row = 3, column = 8, columnspan = 1, sticky=EW)
	
	
	
	
	
	##########################################################################################################################################
	# separateur
	espaceLabel4 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel4.config(font=(12))
	espaceLabel4.grid(row = 4, column = 0, columnspan = 9, sticky=EW)


