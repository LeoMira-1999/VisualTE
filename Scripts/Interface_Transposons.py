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




########################################################################################################################
###	Get the path of the TE file
########################################################################################################################

def getTransposable(newWindow, pathVisualDATA) :
	
	Interface_SettingVariables.fichierTE = askopenfilename( )
	if Interface_SettingVariables.fichierTE == '' :
		msg = messagebox.showinfo( "Error !", "The TE file is missing !")
	else :
		decoupe = Interface_SettingVariables.fichierTE.split('/')
		copyFile = pathVisualDATA + '/' + decoupe[len(decoupe)-1]
		shutil.copyfile(Interface_SettingVariables.fichierTE, copyFile)
		Interface_SettingVariables.fichierTE = copyFile
		
		newWindow.destroy()
		Interface_SettingVariables.acessTE = 1
		if (Interface_SettingVariables.acessTE == 1 and Interface_SettingVariables.acessGene == 1 
		and Interface_SettingVariables.acessGO and Interface_SettingVariables.acessChip == 1 
		and Interface_SettingVariables.ChipSEQdirectory != '') :
			Interface_SettingVariables.root.destroy()
	
	
	
	
	
########################################################################################################################
### 	Select and Copy the TE file
########################################################################################################################

def LocalTransposableElements(pathVisualDATA) :
	
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

	warningLabel = Label(newWindow, text = 'Select your Transposable Element file', borderwidth=5, bg="#F5F5FF")
	warningLabel.config(font=(24))
	warningLabel.grid(row = 1, column = 1, columnspan = 7, sticky=EW)

	espaceLabel51 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel51.config(font=(12))
	espaceLabel51.grid(row = 1, column = 8, columnspan = 1, sticky=EW)
	
	
	
	
	
	# button de choix de l'annotation
	espaceLabel20 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel20.config(font=(12))
	espaceLabel20.grid(row = 2, column = 0, columnspan = 1, sticky=EW)
		
	TE = Frame(newWindow, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	TE.grid(row = 2, column = 1, columnspan = 7, sticky=EW)
	buttonTE = ttk.Button(TE, text="Tranposable Element File", command = lambda: getTransposable(newWindow, pathVisualDATA) )
	buttonTE.pack(expand=TRUE, fill=BOTH)

	espaceLabel21 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel21.config(font=(12))
	espaceLabel21.grid(row = 2, column = 8, columnspan = 1, sticky=EW)
	
	
	
	
	
	##########################################################################################################################################
	# separateur
	espaceLabel1 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel1.config(font=(12))
	espaceLabel1.grid(row = 3, column = 0, columnspan = 7, sticky=EW)
	
	
