#!/usr/bin/python3
import os
import sys
from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox
import tkinter.ttk as ttk
import urllib.request
import ftplib
from . import Interface_SettingVariables, Interface_GenomeDATA, Interface_GeneOntology, Interface_Transposons, Interface_ChipSeq


# faire une interface graphique :
# demande si l'utilisateur la source des donnees
	# Utisateur n'a aucune donnees
		# Arret de l'interface : relancer apres aquisition des donnees TE
	# Utilisateur n'a pas donnees TE
		# Arret de l'interface : relancer apres aquisition des donnees TE
	# Utilisateur a seulement TE
		# telechargement des sequences genomes sur NCBI
		# telechargement des annotation genomes sur NCBI
		# telechargement des gene2go
		# telechargement du fichier go-basic.obo
		# telechargement des ChipSeq
	# Utilisateur a TE + autres data
		# telechargement des donnees manquantes !






########################################################################################################################
# 	Select function depending of user choice
########################################################################################################################
def availableDATA(value1, value2, value3, value4, pathVisualDATA):
	if value1 == 0 :
		# It is obligatory to have the TE files
		# Give a warning and close the interface
		CloseVisualTEmake()
	else :
		# Create an interface to select the TE file
		Interface_Transposons.LocalTransposableElements(pathVisualDATA)
		
		
		# Create an interface and select a genome in the list and select the TE files
		if value2 == 0 :
			Interface_GenomeDATA.DownloadGenomeFiles(pathVisualDATA)
		# Create a interface and select the two genomes files
		else :
			Interface_GenomeDATA.LocalGenomes(pathVisualDATA)
		
		
		# Create an interface and download the two GeneOntology files
		if value3 == 0 :
			Interface_GeneOntology.DownloadGO(pathVisualDATA)
		# Create an interface and select the two GeneOntology files
		else :
			Interface_GeneOntology.LocalGeneOntology(pathVisualDATA)
		
		
		if value4 == 0 :
			Interface_ChipSeq.DownloadChipSEQ(pathVisualDATA)
		else :
			Interface_ChipSeq.LocalChipSEQ(pathVisualDATA)
			









########################################################################################################################
# 	Close the interface
########################################################################################################################
def CloseVisualTEmake():

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
	# Title of the window
	espaceLabel2 = Label(newWindow, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel2.config(font=(24))
	espaceLabel2.grid(row = 0, column = 0, columnspan = 1, sticky=EW)

	warningLabel = Label(newWindow, text = 'Without TE file(s) \nVisualTE3 cannot be created !', borderwidth=5, bg="#F5F5FF")
	warningLabel.config(font=(24))
	warningLabel.grid(row = 0, column = 1, columnspan = 4, sticky=EW)

	espaceLabel2 = Label(newWindow, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel2.config(font=(24))
	espaceLabel2.grid(row = 0, column = 5, columnspan = 1, sticky=EW)

	# separateur
	espaceLabel1 = Label(newWindow, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel1.config(font=(24))
	espaceLabel1.grid(row = 1, column = 0, columnspan = 6, sticky=EW)
	
	
	
	
	
	##########################################################################################################################################
	# bouton de fin du programme
	espaceLabel2 = Label(newWindow, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel2.config(font=(24))
	espaceLabel2.grid(row = 2, column = 0, columnspan = 1, sticky=EW)

	fDATA = Frame(newWindow, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	fDATA.grid(row = 2, column = 1, columnspan = 4, sticky=EW)

	warningButton = ttk.Button(fDATA, text="I got it !", command = Interface_SettingVariables.root.destroy)
	warningButton.pack(expand=TRUE, fill=BOTH)

	espaceLabel3 = Label(newWindow, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel3.config(font=(24))
	espaceLabel3.grid(row = 2, column = 5, columnspan = 1, sticky=EW)

	# separateur
	espaceLabel4 = Label(newWindow, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel4.config(font=(24))
	espaceLabel4.grid(row = 3, column = 0, columnspan = 6, sticky=EW)
	
	
	
	
	





########################################################################################################################
# 	Create the main interface
########################################################################################################################
def Interface(pathVisualDATA):

	### Style de l'interface
	Interface_SettingVariables.root = Tk()
	Interface_SettingVariables.root.configure(background='#F5F5FF')
	Interface_SettingVariables.root.title("Making VisualTE3 with your data")     # Add a title

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
	# titre de la selection 
	Choix = Label(Interface_SettingVariables.root, text = 'Selection of available data', borderwidth=5, bg="#F5F5FF")
	Choix.config(font=(24))
	Choix.grid(row = 0, column = 0, columnspan = 7, sticky=EW)

	# separateur
	espaceLabel6 = Label(Interface_SettingVariables.root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel6.config(font=(12))
	espaceLabel6.grid(row = 1, column = 0, columnspan = 7, sticky=EW)
	
	
	
	
	
	##########################################################################################################################################
	# Selection des donnees TE 
	espaceLabel40 = Label(Interface_SettingVariables.root, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel40.config(font=(24))
	espaceLabel40.grid(row = 2, column = 0, columnspan = 1, sticky=EW)

	Intro1 = Label(Interface_SettingVariables.root, text = 'You had : ', borderwidth=5, bg="#F5F5FF")
	Intro1.config(font=(24))
	Intro1.grid(row = 2, column = 1, columnspan = 1, sticky=EW)

	CheckTE = IntVar()
	CheckTE.set(0)
	TECheckbutton = Checkbutton(Interface_SettingVariables.root, text = "Transposable Element file(s)", variable = CheckTE, onvalue = 1, offvalue = 0, height=3, width = 35, activeforeground='#8888FF', borderwidth=5, anchor=W, bg="#F5F5FF")       
	TECheckbutton.config(font=(24))
	TECheckbutton.grid(row = 2, column = 2, columnspan = 3, sticky=NSEW)

	espaceLabel41 = Label(Interface_SettingVariables.root, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel41.config(font=(24))
	espaceLabel41.grid(row = 2, column = 5, columnspan = 2, sticky=EW)
	
	
	
	
	##########################################################################################################################################
	# Selection des donnees genomes
	espaceLabel30 = Label(Interface_SettingVariables.root, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel30.config(font=(24))
	espaceLabel30.grid(row = 3, column = 0, columnspan = 1, sticky=EW)

	Intro2 = Label(Interface_SettingVariables.root, text = 'You had : ', borderwidth=5, bg="#F5F5FF")
	Intro2.config(font=(24))
	Intro2.grid(row = 3, column = 1, columnspan = 1, sticky=EW)

	CheckGenomes = IntVar()
	CheckGenomes.set(0)
	GenomesCheckbutton = Checkbutton(Interface_SettingVariables.root, text = "Genomes files (FNA and GFF)", variable = CheckGenomes, onvalue = 1, offvalue = 0, height=3, width = 35, activeforeground='#8888FF', borderwidth=5, anchor=W, bg="#F5F5FF")   
	GenomesCheckbutton.config(font=(24))
	GenomesCheckbutton.grid(row = 3, column = 2, columnspan = 3, sticky=NSEW)

	espaceLabel31 = Label(Interface_SettingVariables.root, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel31.config(font=(24))
	espaceLabel31.grid(row = 3, column = 5, columnspan = 2, sticky=EW)





	##########################################################################################################################################
	# Selection des donnes GeneOntology
	espaceLabel30 = Label(Interface_SettingVariables.root, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel30.config(font=(24))
	espaceLabel30.grid(row = 4, column = 0, columnspan = 1, sticky=EW)

	Intro2 = Label(Interface_SettingVariables.root, text = 'You had : ', borderwidth=5, bg="#F5F5FF")
	Intro2.config(font=(24))
	Intro2.grid(row = 4, column = 1, columnspan = 1, sticky=EW)

	CheckGeneOntology = IntVar()
	CheckGeneOntology.set(0)
	GeneOntologybutton = Checkbutton(Interface_SettingVariables.root, text = "GeneOntology files (x2)", variable = CheckGeneOntology, onvalue = 1, offvalue = 0, height=3, width = 35, activeforeground='#8888FF', borderwidth=5, anchor=W, bg="#F5F5FF")   
	GeneOntologybutton.config(font=(24))
	GeneOntologybutton.grid(row = 4, column = 2, columnspan = 3, sticky=NSEW)

	espaceLabel31 = Label(Interface_SettingVariables.root, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel31.config(font=(24))
	espaceLabel31.grid(row = 4, column = 5, columnspan = 2, sticky=EW)
	
	
	
	
	
	##########################################################################################################################################
	# Selection des donnes GeneOntology
	espaceLabel30 = Label(Interface_SettingVariables.root, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel30.config(font=(24))
	espaceLabel30.grid(row = 5, column = 0, columnspan = 1, sticky=EW)

	Intro2 = Label(Interface_SettingVariables.root, text = 'You had : ', borderwidth=5, bg="#F5F5FF")
	Intro2.config(font=(24))
	Intro2.grid(row = 5, column = 1, columnspan = 1, sticky=EW)

	CheckChipSEQ = IntVar()
	CheckChipSEQ.set(0)
	ChipSEQbutton = Checkbutton(Interface_SettingVariables.root, text = "ChipSeq files (ENCODE)", variable = CheckChipSEQ, onvalue = 1, offvalue = 0, height=3, width = 35, activeforeground='#8888FF', borderwidth=5, anchor=W, bg="#F5F5FF")   
	ChipSEQbutton.config(font=(24))
	ChipSEQbutton.grid(row = 5, column = 2, columnspan = 3, sticky=NSEW)

	espaceLabel31 = Label(Interface_SettingVariables.root, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel31.config(font=(24))
	espaceLabel31.grid(row = 5, column = 5, columnspan = 2, sticky=EW)





	##########################################################################################################################################
	# separateur
	espaceLabel13 = Label(Interface_SettingVariables.root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel13.config(font=(12))
	espaceLabel13.grid(row = 6, column = 0, columnspan = 7, sticky=EW)
	
	
	
	
	
	##########################################################################################################################################
	# Creation du boutton submit data
	espaceLabel3 = Label(Interface_SettingVariables.root, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel3.config(font=(24))
	espaceLabel3.grid(row = 7, column = 0, columnspan = 1, sticky=EW)

	fDATA = Frame(Interface_SettingVariables.root, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	fDATA.grid(row = 7, column = 1, columnspan = 4, sticky=NSEW)
	SubmitDATA = ttk.Button(fDATA, text="Submit Available Data", command = lambda: availableDATA(CheckTE.get(), CheckGenomes.get(), CheckGeneOntology.get(), CheckChipSEQ.get(), pathVisualDATA ) )
	SubmitDATA.pack(expand=TRUE, fill=BOTH)

	espaceLabel4 = Label(Interface_SettingVariables.root, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel4.config(font=(24))
	espaceLabel4.grid(row = 7, column = 5, columnspan = 2, sticky=EW)





	##########################################################################################################################################
	# separateur
	espaceLabel5 = Label(Interface_SettingVariables.root, text = '           ', borderwidth=5, bg="#F5F5FF")
	espaceLabel5.config(font=(12))
	espaceLabel5.grid(row = 8, column = 0, columnspan = 7, sticky=EW)




	##########################################################################################################################################
	Interface_SettingVariables.root.mainloop()
	return Interface_SettingVariables.fichierTE, Interface_SettingVariables.fileGFFgenome, Interface_SettingVariables.fileFNAgenome, Interface_SettingVariables.GeneOntologyOBO, Interface_SettingVariables.GeneOntologyGI      




