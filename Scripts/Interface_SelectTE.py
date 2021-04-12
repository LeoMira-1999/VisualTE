#!/usr/bin/python3
import os
import sys
import threading
import shutil
import ftplib
import time 
import importlib
import importlib.util
from tkinter import *
import tkinter.font as tkFont
from tkinter.filedialog import *
from tkinter import messagebox
import tkinter.ttk as ttk
import urllib.request
import subprocess

from . import Interface_ProcessSelectionTE

from . import Create_CommonDATA2
from . import Create_MainFile
from . import Create_SelectedAnnotations
from . import Create_Random_Sequences
from . import Create_Overlap_TFBS
from . import Create_Alignment_and_Tree

from . import MakeFunction_GenomeBrowser
from . import MakeFunction_ChromosomeDistribution
from . import MakeFunction_GeneralFeaturesDistribution
from . import MakeFunction_SimilarityOccurrences
from . import MakeFunction_TEEnvironment
from . import MakeFunction_DistanceNeighboringGene
from . import MakeFunction_NeighboringGeneFunctions
from . import MakeFunction_OverlappingTFBS
from . import MakeFunction_SummaryTable



root = ''

numberOFselection = 0
ListeCompleteTE = []
ListeFamilleTE = []
ListeSuperFamilyTE = []
list_selection_TE = []		# list of selected TE family


# 1er ligne 1er interface
espaceLabel6 = ''
Choix = ''
Choix3 = ''
# 2eme ligne 1er interface
espaceLabel13 = ''
TEselection = ''
espaceLabel14 = ''
# 3eme ligne 1er interface
espaceLabel1 = ''
# 4eme ligne 1er interface
espaceLabel9 = ''
fDATA = ''
SubmitDATA = ''
espaceLabel10 = ''
# 5eme ligne 1er interface
espaceLabel311 = ''
Choix2 = ''
# 6eme ligne 1er interface
espaceLabel40 = ''
fText = ''
textProcess = ''
espaceLabel34 = ''
# 7eme ligne 1er interface
espaceLabel19 = ''
Merge = ''
R1 = ''
R2 = ''
espaceLabel110 = ''
# 8eme ligne 1er interface
espaceLabel312 = ''
# 9eme ligne 1er interface
espaceLabel9 = ''
fDATA2 = ''
SubmitDATA2 = ''
espaceLabel10 = ''
# 10eme ligne 1er interface
espaceLabel313 = ''











########################################################################################################################
###	New Interface for the selection of TEs (up to 3)
########################################################################################################################
def getListeTE(DATAListTE) :
	
	global ListeCompleteTE
	global ListeFamilleTE
	global ListeSuperFamilyTE
	
	# read the annotation file
	file = open(DATAListTE, "r")
	lignes = file.readlines()
	file.close()
	
	for i in range(1, len(lignes), 1) :
		lignes[i] = lignes[i][:-1]
		decoupe = lignes[i].split(',')
		ListeCompleteTE.append(decoupe[0] + '\t\t' + decoupe[1])
	ListeCompleteTE.sort()
	for i in range(0, len(ListeCompleteTE), 1) :
		decoupe = ListeCompleteTE[i].split('\t\t')
		nbEspace = 20 - len(decoupe[0])
		ListeCompleteTE[i] = decoupe[0] + nbEspace * ' ' + decoupe[1]
		ListeFamilleTE.append(decoupe[0])
		ListeSuperFamilyTE.append(decoupe[1])
	
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	IF the TE family are merged or not
########################################################################################################################
def getMergeFamily(value, pathVisual, pathVisualNEW) :

	global list_selection_TE
	global root
	
	OfficialName = ''
	if value == 1 and len(list_selection_TE) > 1 :	# Merged the family
		OfficialName = 'Merged '
	for i in range(0, len(list_selection_TE), 1) :
		if i > 0 :
			OfficialName += ', '
		OfficialName += str(list_selection_TE[i])
		
	if len(list_selection_TE) > 0 :
		DestroyPreviousWindow()
		Interface_ProcessSelectionTE.DrawNewWindow(root)
		Interface_ProcessSelectionTE.CreateFonctionDASH(pathVisual, pathVisualNEW, OfficialName, list_selection_TE)
		
	else :
		msg = messagebox.showinfo( "Error !", "You must select at least 1 TE family !")










########################################################################################################################
###	Get the selection of the TE family
########################################################################################################################
def getTE(indexTE, pathVisual) :
	
	global root
	
	global TEselection
	global textProcess
	global numberOFselection
	global ListeCompleteTE
	global ListeFamilleTE
	global ListeSuperFamilyTE
	global list_selection_TE
	
	numberOFselection += 1
	selectedSuperfamily = ListeSuperFamilyTE[indexTE]
	selectedFamily = ListeFamilleTE[indexTE] + "\n"
	
	if numberOFselection == 1 or numberOFselection == 2 :
		tempC = []
		tempF = []
		tempS = []
		for i in range(0, len(ListeCompleteTE), 1) :
			if ListeSuperFamilyTE[i] == selectedSuperfamily and i != indexTE :
				tempC.append(ListeCompleteTE[i])
				tempF.append(ListeFamilleTE[i])
				tempS.append(ListeSuperFamilyTE[i])
		ListeCompleteTE = tempC
		ListeFamilleTE = tempF
		ListeSuperFamilyTE = tempS
		
	# Here the choice is finished It must change the interface
	if numberOFselection == 3 :
		ListeCompleteTE = []
		ListeFamilleTE = []
		ListeSuperFamilyTE = []
		root.update()
		
	
	# Update the list of TE families and the interface after each choice
	if numberOFselection < 4 :
		list_selection_TE.append(selectedFamily[:-1])
		insertionText = str(numberOFselection) + '.0'
		textProcess.insert(insertionText, selectedFamily)
		TEselection['values'] = ListeCompleteTE
		root.update()
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Destroy the widget 
########################################################################################################################
def DestroyPreviousWindow() :
	
	global root
	
	global espaceLabel6
	global Choix
	global Choix3
	
	global espaceLabel13 
	global TEselection
	global espaceLabel14
	
	global espaceLabel1 
	
	global espaceLabel9 
	global fDATA 
	global SubmitDATA 
	global espaceLabel10 
	
	global espaceLabel311 
	global Choix2 
	
	global espaceLabel40 
	global fText  
	global textProcess 
	global espaceLabel34 
	
	global espaceLabel19 
	global Merge 
	global R1 
	global R2 
	global espaceLabel110 
	
	global espaceLabel312 
	
	global espaceLabel9 
	global fDATA2 
	global SubmitDATA2 
	global espaceLabel10 
	
	global espaceLabel313
	
	
	espaceLabel6.destroy()
	Choix.destroy()
	Choix3.destroy()
	
	espaceLabel13.destroy()
	TEselection.destroy()
	espaceLabel14.destroy()
	
	espaceLabel1.destroy()
	
	espaceLabel9.destroy()
	fDATA.destroy()
	SubmitDATA.destroy()
	espaceLabel10.destroy()
	
	espaceLabel311.destroy()
	Choix2.destroy()
	
	espaceLabel40.destroy()
	fText.destroy()
	textProcess.destroy()
	espaceLabel34.destroy()
	
	espaceLabel19.destroy()
	Merge.destroy()
	R1.destroy()
	R2.destroy()
	espaceLabel110.destroy()
	
	espaceLabel312.destroy()
	
	espaceLabel9.destroy()
	fDATA2.destroy()
	SubmitDATA2.destroy()
	espaceLabel10.destroy()
	
	espaceLabel313.destroy()
	
	root.update()
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	New Interface for the selection of TEs (up to 3)
########################################################################################################################

def Interface_Selection(pathVisual, pathVisualNEW, tempsSeconde):

	### Style de l'interface
	global root
	
	global espaceLabel6
	global Choix
	global Choix3
	
	global espaceLabel13 
	global TEselection
	global espaceLabel14 
	
	global espaceLabel1 
	
	global espaceLabel9 
	global fDATA 
	global SubmitDATA 
	global espaceLabel10 
	
	global espaceLabel311 
	global Choix2 
	
	global espaceLabel40 
	global fText 
	global textProcess
	global espaceLabel34 
	
	global espaceLabel19 
	global Merge 
	global R1 
	global R2 
	global espaceLabel110 
	
	global espaceLabel312 
	
	global espaceLabel9 
	global fDATA2 
	global SubmitDATA2 
	global espaceLabel10 
	
	global espaceLabel313 

	root = Tk()
	root.configure(background='#F5F5FF')
	root.title("Making VisualTE3 with your data")     # Add a title

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
	# separateur and titre
	espaceLabel6 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel6.config(font=(12))
	espaceLabel6.grid(row = 0, column = 0, columnspan = 8, sticky=EW)
	
	# titre de la selection 
	Choix = Label(root, text = 'Select your TE(s) from this list', borderwidth=5, bg="#F5F5FF")
	Choix.config(font=(24))
	Choix.grid(row = 1, column = 0, columnspan = 8, sticky=EW)

	# titre de la selection 
	Choix3 = Label(root, text = 'Up to 3 families (same superfamily)', borderwidth=5, bg="#F5F5FF")
	Choix3.config(font=(8))
	Choix3.grid(row = 2, column = 0, columnspan = 8, sticky=EW)
	
	
	
	########################################################################################################################
	# Combobox
	espaceLabel13 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel13.config(font=(12))
	espaceLabel13.grid(row = 3, column = 0, columnspan = 1, sticky=EW)
	
	# Combobox creation 
	SelectedTE = StringVar(root)
	text_font = tkFont.Font(family="Courier New",size=14)
	root.option_add("*TCombobox*Listbox*Font", text_font)
	TEselection = ttk.Combobox(root, textvariable = SelectedTE, width = 40, values = ListeCompleteTE, font = text_font) 
	TEselection.current(0) 
	TEselection.grid(row = 3, column = 1, columnspan = 6, sticky=EW)
	
	espaceLabel14 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel14.config(font=(12))
	espaceLabel14.grid(row = 3, column = 7, columnspan = 1, sticky=EW)
	
	
	
	########################################################################################################################
	# separateur
	espaceLabel1 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel1.config(font=(12))
	espaceLabel1.grid(row = 4, column = 0, columnspan = 8, sticky=EW)
	
	
	
	########################################################################################################################
	# Creation du boutton submit TE family
	espaceLabel9 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel9.config(font=(12))
	espaceLabel9.grid(row = 5, column = 0, columnspan = 1, sticky=EW)

	fDATA = Frame(root, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	fDATA.grid(row = 5, column = 1, columnspan = 6, sticky=EW)
	
	SubmitDATA = ttk.Button(fDATA, text="Select TE name", command = lambda: getTE( TEselection.current(), pathVisual ) )
	SubmitDATA.pack(expand=TRUE, fill=BOTH)

	espaceLabel10 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel10.config(font=(12))
	espaceLabel10.grid(row = 5, column = 7, columnspan = 1, sticky=EW)
	
	
	
	########################################################################################################################
	# separateur
	espaceLabel311 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel311.config(font=(12))
	espaceLabel311.grid(row = 6, column = 0, columnspan = 8, sticky=EW)
	
	# titre de la selection 
	Choix2 = Label(root, text = 'List of Selected TE(s)', borderwidth=5, bg="#F5F5FF")
	Choix2.config(font=(24))
	Choix2.grid(row = 7, column = 0, columnspan = 8, sticky=EW)
	
	
	
	########################################################################################################################
	# Text widget to show the selected TE
	espaceLabel40 = Label(root, text = '          ', borderwidth=5, bg="#F5F5FF")
	espaceLabel40.config(font=(24))
	espaceLabel40.grid(row = 8, column = 0, columnspan = 1, rowspan=4, sticky=EW)
	
	fText = Frame(root, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	fText.grid(row = 8, column = 1, columnspan = 6, rowspan=4, sticky=NSEW)
	textProcess = Text(fText, height=4, wrap=NONE)
	textProcess.pack(expand=TRUE, fill=BOTH)
	
	espaceLabel34 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel34.config(font=(12))
	espaceLabel34.grid(row = 8, column = 7, columnspan = 1, rowspan=4, sticky=EW)
	
	
	
	########################################################################################################################
	# Radiobuttons
	espaceLabel19 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel19.config(font=(12))
	espaceLabel19.grid(row = 12, column = 0, columnspan = 1, sticky=EW)
	
	Merge = Label(root, text = 'Merge TE families : ', borderwidth=5, bg="#F5F5FF")
	Merge.config(font=(24))
	Merge.grid(row = 12, column = 1, columnspan = 2, sticky=EW)
	
	varRadio = IntVar()
	R1 = Radiobutton(root, text="Yes", variable=varRadio, value=1, bg="#F5F5FF")
	R1.grid(row = 12, column = 3, columnspan = 2, sticky=EW)
	R1.config(font=(24))
	R2 = Radiobutton(root, text="No", variable=varRadio, value=2, bg="#F5F5FF")
	R2.grid(row = 12, column = 5, columnspan = 2, sticky=EW)
	R2.config(font=(24))
	R2.select()
	
	espaceLabel110 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel110.config(font=(12))
	espaceLabel110.grid(row = 12, column = 7, columnspan = 1, sticky=EW)
	
	
	
	########################################################################################################################
	# separateur
	espaceLabel312 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel312.config(font=(12))
	espaceLabel312.grid(row = 13, column = 0, columnspan = 7, sticky=EW)
	
	
	
	########################################################################################################################
	# Creation du boutton submit TE family
	espaceLabel9 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel9.config(font=(12))
	espaceLabel9.grid(row = 14, column = 0, columnspan = 1, sticky=EW)

	fDATA2 = Frame(root, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	fDATA2.grid(row = 14, column = 1, columnspan = 6, sticky=EW)
	
	SubmitDATA2 = ttk.Button(fDATA2, text="Finish the Selection", command = lambda: getMergeFamily( varRadio.get(), pathVisual, pathVisualNEW ) )
	SubmitDATA2.pack(expand=TRUE, fill=BOTH)

	espaceLabel10 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel10.config(font=(12))
	espaceLabel10.grid(row = 14, column = 7, columnspan = 1, sticky=EW)
	
	
	
	########################################################################################################################
	# separateur
	espaceLabel313 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel313.config(font=(12))
	espaceLabel313.grid(row = 15, column = 0, columnspan = 7, sticky=EW)
	
	root.mainloop()
