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
from . import Interface_SettingVariables, Interface_DownloadGenomes



# Global values for the Progressbar
progressFNA = ''
progressGFF = ''
newWindow2 = ''





# adress for genome annotation
# ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/latest_assembly_versions/GCF_000001405.39_GRCh38.p13/GCF_000001405.39_GRCh38.p13_genomic.gff.gz
# adress for genome sequence
# ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/latest_assembly_versions/GCF_000001405.39_GRCh38.p13/GCF_000001405.39_GRCh38.p13_genomic.fna.gz
# https://ftp.ncbi.nlm.nih.gov/genomes/refseq/protozoa/Babesia_bovis/latest_assembly_versions/GCF_000165395.1_ASM16539v1/





########################################################################################################################
# 	Download the data genome
########################################################################################################################
def DownloadGenomeFile(pathVisualDATA, FNAaTelecharger, FNAsize, GFFaTelecharger, GFFsize, ftpAdress, newWindow = None) :

	global newWindow2
	global progressFNA
	global progressGFF


	temp = pathVisualDATA + '/' + FNAaTelecharger
	url = ftpAdress + FNAaTelecharger
	response = requests.get(url, stream=True)
	fileSize = int(response.headers['Content-length'])
	chunkSize = round(fileSize / 500)+1
	progressFNA["value"] = 0
	progressFNA["maximum"] = FNAsize
	progressFNA.start()

	internetFile = open(temp, 'wb')
	for chunk in response.iter_content(chunk_size=chunkSize):
		internetFile.write(chunk)
		progressFNA.step(chunkSize)
		newWindow2.update()


	temp = pathVisualDATA + '/' + GFFaTelecharger
	url = ftpAdress + GFFaTelecharger
	response = requests.get(url, stream=True)
	fileSize = int(response.headers['Content-length'])
	chunkSize = round(fileSize / 500)+1
	progressGFF["value"] = 0
	progressGFF["maximum"] = GFFsize
	progressGFF.start()

	internetFile = open(temp, 'wb')
	for chunk in response.iter_content(chunk_size=chunkSize):
		internetFile.write(chunk)
		progressGFF.step(chunkSize)
		newWindow2.update()


	newWindow2.destroy()
	newWindow.destroy()
	Interface_SettingVariables.acessGene = 1
	if (Interface_SettingVariables.acessTE == 1 and Interface_SettingVariables.acessGene == 1
	and Interface_SettingVariables.acessGO and Interface_SettingVariables.acessChip == 1
	and Interface_SettingVariables.ChipSEQdirectory != '') :
		Interface_SettingVariables.root.destroy()





########################################################################################################################
# 	Download the data genome
########################################################################################################################
def downlaodNCBIgenome(GenomeName, pathVisualDATA, newWindow) :

	FNAaTelecharger, FNAsize, GFFaTelecharger, GFFsize, ftpAdress = Interface_DownloadGenomes.lanceTelechargement(GenomeName, pathVisualDATA)

	global newWindow2
	global progressFNA
	global progressGFF



	newWindow2 = Toplevel(newWindow, borderwidth=5)
	newWindow2.configure(background='#F5F5FF')
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
	espaceLabel11 = Label(newWindow2, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel11.config(font=(12))
	espaceLabel11.grid(row = 0, column = 0, columnspan = 7, sticky=EW)





	########################################################################################################################
	# Create the progressbar FNA
	espaceLabel33 = Label(newWindow2, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel33.config(font=(12))
	espaceLabel33.grid(row = 1, column = 0, columnspan = 1, sticky=EW)

	warningLabel5 = Label(newWindow2, text = 'Downloading your Sequence file', borderwidth=5, bg="#F5F5FF")
	warningLabel5.config(font=(24))
	warningLabel5.grid(row = 1, column = 1, columnspan = 5, sticky=EW)

	espaceLabel34 = Label(newWindow2, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel34.config(font=(12))
	espaceLabel34.grid(row = 1, column = 6, columnspan = 1, sticky=EW)

	espaceLabel3 = Label(newWindow2, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel3.config(font=(12))
	espaceLabel3.grid(row = 2, column = 0, columnspan = 1, sticky=EW)

	progressFNA = ttk.Progressbar(newWindow2, orient="horizontal", length=500, mode = 'determinate')
	progressFNA.grid(row = 2, column = 1, columnspan = 5, sticky=EW)

	espaceLabel4 = Label(newWindow2, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel4.config(font=(12))
	espaceLabel4.grid(row = 2, column = 6, columnspan = 1, sticky=EW)





	########################################################################################################################
	# Separateur
	espaceLabel21 = Label(newWindow2, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel21.config(font=(12))
	espaceLabel21.grid(row = 3, column = 0, columnspan = 7, sticky=EW)





	########################################################################################################################
	# Create the progressbar FNA
	espaceLabel133 = Label(newWindow2, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel133.config(font=(12))
	espaceLabel133.grid(row = 4, column = 0, columnspan = 1, sticky=EW)

	warningLabel15 = Label(newWindow2, text = 'Downloading your Annotation file', borderwidth=5, bg="#F5F5FF")
	warningLabel15.config(font=(24))
	warningLabel15.grid(row = 4, column = 1, columnspan = 5, sticky=EW)

	espaceLabel134 = Label(newWindow2, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel134.config(font=(12))
	espaceLabel134.grid(row = 4, column = 6, columnspan = 1, sticky=EW)

	espaceLabel13 = Label(newWindow2, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel13.config(font=(12))
	espaceLabel13.grid(row = 5, column = 0, columnspan = 1, sticky=EW)

	progressGFF = ttk.Progressbar(newWindow2, orient="horizontal", length=500, mode = 'determinate')
	progressGFF.grid(row = 5, column = 1, columnspan = 5, sticky=EW)

	espaceLabel14 = Label(newWindow2, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel14.config(font=(12))
	espaceLabel14.grid(row = 5, column = 6, columnspan = 1, sticky=EW)





	########################################################################################################################
	# Download the files
	DownloadGenomeFile(pathVisualDATA, FNAaTelecharger, FNAsize, GFFaTelecharger, GFFsize, ftpAdress, newWindow)





########################################################################################################################
# 	Open a new interface for choosing to download the genome and select TE directory
########################################################################################################################
def DownloadGenomeFiles(pathVisualDATA):

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
	# combobox pour la selection du nom du genome a telecharger
	espaceLabel3 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel3.config(font=(12))
	espaceLabel3.grid(row = 1, column = 0, columnspan = 1, sticky=EW)

	warningLabel5 = Label(newWindow, text = 'Enter Your Genome Name', borderwidth=5, bg="#F5F5FF")
	warningLabel5.config(font=(24))
	warningLabel5.grid(row = 1, column = 1, columnspan = 5, sticky=EW)

	espaceLabel4 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel4.config(font=(12))
	espaceLabel4.grid(row = 1, column = 6, columnspan = 1, sticky=EW)



	espaceLabel113 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel113.config(font=(12))
	espaceLabel113.grid(row = 2, column = 0, columnspan = 1, sticky=EW)

	warningLabel2 = Label(newWindow, text = 'I.E : Mouse => Mus musculus', borderwidth=5, bg="#F5F5FF")
	warningLabel2.config(font=(24))
	warningLabel2.grid(row = 2, column = 1, columnspan = 5, sticky=EW)

	espaceLabel4 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel4.config(font=(12))
	espaceLabel4.grid(row = 2, column = 6, columnspan = 1, sticky=EW)



	espaceLabel33 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel33.config(font=(12))
	espaceLabel33.grid(row = 3, column = 0, columnspan = 1, sticky=EW)

	fGenome = Frame(newWindow, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	fGenome.grid(row = 3, column = 1, columnspan = 5, sticky=EW)

	GenomeName = StringVar()
	GenomeName.set('')
	familleTE = Entry(fGenome, borderwidth=5, bg="#F5F5FF", textvariable = GenomeName)
	familleTE.config(font=(24))
	familleTE.pack(expand=TRUE, fill=BOTH)

	espaceLabel171 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel171.config(font=(12))
	espaceLabel171.grid(row = 3, column = 6, columnspan = 1, sticky=EW)





	########################################################################################################################
	# Separateur
	espaceLabel5 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel5.config(font=(12))
	espaceLabel5.grid(row = 4, column = 0, columnspan = 7, sticky=EW)




	########################################################################################################################
	# Creation du boutton submit Genomes choice
	espaceLabel9 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel9.config(font=(12))
	espaceLabel9.grid(row = 5, column = 0, columnspan = 1, sticky=EW)

	fDATA = Frame(newWindow, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	fDATA.grid(row = 5, column = 1, columnspan = 5, sticky=EW)

	SubmitDATA = ttk.Button(fDATA, text="Submit Genome", command = lambda: downlaodNCBIgenome(GenomeName.get(), pathVisualDATA, newWindow) )
	SubmitDATA.pack(expand=TRUE, fill=BOTH)

	espaceLabel10 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel10.config(font=(12))
	espaceLabel10.grid(row = 5, column = 6, columnspan = 1, sticky=EW)





	########################################################################################################################
	# separateur
	espaceLabel11 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel11.config(font=(24))
	espaceLabel11.grid(row = 6, column = 0, columnspan = 7, sticky=EW)




















########################################################################################################################
# 	Save the annotation file
########################################################################################################################
def getAnnotationNCBIfile() :
	Interface_SettingVariables.fileGFFgenome = askopenfilename( filetypes=( ("All files", "*.*"), ("Annotation files", "*.gff") ) )





########################################################################################################################
# 	Save the sequence file
########################################################################################################################
def getSequenceNCBIfile() :
	Interface_SettingVariables.fileFNAgenome = askopenfilename( filetypes=( ("All files", "*.*"), ("Sequences files", "*.fna") ) )





########################################################################################################################
# 	Save the sequence file
########################################################################################################################
def closeGenomeWindow(newWindow, pathVisualDATA) :

	if Interface_SettingVariables.fileGFFgenome == '' or Interface_SettingVariables.fileFNAgenome == '' :
		msg = messagebox.showinfo( "Error !", "One or two genome file is missing !")
	else :
		decoupe = Interface_SettingVariables.fileGFFgenome.split('/')
		copyFile = pathVisualDATA + '/' + decoupe[len(decoupe)-1]
		shutil.copyfile(Interface_SettingVariables.fileGFFgenome, copyFile)
		Interface_SettingVariables.fileGFFgenome = copyFile

		decoupe = Interface_SettingVariables.fileFNAgenome.split('/')
		copyFile = pathVisualDATA + '/' + decoupe[len(decoupe)-1]
		shutil.copyfile(Interface_SettingVariables.fileFNAgenome, copyFile)
		Interface_SettingVariables.fileFNAgenome = copyFile

		newWindow.destroy()
		Interface_SettingVariables.acessGene = 1

		if Interface_SettingVariables.acessTE == 1 and Interface_SettingVariables.acessGene == 1 and Interface_SettingVariables.acessGO and Interface_SettingVariables.acessChip == 1:
			Interface_SettingVariables.root.destroy()





########################################################################################################################
# 	Open a new interface for selecting the Genomes files
########################################################################################################################
def LocalGenomes(pathVisualDATA) :

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
	# label de selection de l'annotation
	espaceLabel50 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel50.config(font=(12))
	espaceLabel50.grid(row = 0, column = 0, columnspan = 1, sticky=EW)

	warningLabel = Label(newWindow, text = 'Select your NCBI Annotation file (gff file)', borderwidth=5, bg="#F5F5FF")
	warningLabel.config(font=(24))
	warningLabel.grid(row = 0, column = 1, columnspan = 7, sticky=EW)

	espaceLabel51 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel51.config(font=(12))
	espaceLabel51.grid(row = 0, column = 8, columnspan = 1, sticky=EW)



	# button de choix de l'annotation
	espaceLabel20 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel20.config(font=(12))
	espaceLabel20.grid(row = 1, column = 0, columnspan = 1, sticky=EW)

	fGenome = Frame(newWindow, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	fGenome.grid(row = 1, column = 1, columnspan = 7, sticky=EW)
	buttonGenome = ttk.Button(fGenome, text="Annotation file", command = getAnnotationNCBIfile)
	buttonGenome.pack(expand=TRUE, fill=BOTH)

	espaceLabel21 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel21.config(font=(12))
	espaceLabel21.grid(row = 1, column = 8, columnspan = 1, sticky=EW)





	##########################################################################################################################################
	# separateur
	espaceLabel1 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel1.config(font=(12))
	espaceLabel1.grid(row = 2, column = 0, columnspan = 7, sticky=EW)





	##########################################################################################################################################
	# label de selection de la sequence
	espaceLabel55 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel55.config(font=(12))
	espaceLabel55.grid(row = 3, column = 0, columnspan = 1, sticky=EW)

	warningLabel2 = Label(newWindow, text = 'Select your NCBI Sequence file (FNA file)', borderwidth=5, bg="#F5F5FF")
	warningLabel2.config(font=(24))
	warningLabel2.grid(row = 3, column = 1, columnspan = 7, sticky=EW)

	espaceLabel514 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel514.config(font=(12))
	espaceLabel514.grid(row = 3, column = 8, columnspan = 1, sticky=EW)



	# button de choix de l'annotation
	espaceLabel240 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel240.config(font=(12))
	espaceLabel240.grid(row = 4, column = 0, columnspan = 1, sticky=EW)

	fGenome2 = Frame(newWindow, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	fGenome2.grid(row = 4, column = 1, columnspan = 7, sticky=EW)
	buttonGenome2 = ttk.Button(fGenome2, text="Sequence file", command = getSequenceNCBIfile)
	buttonGenome2.pack(expand=TRUE, fill=BOTH)

	espaceLabel221 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel221.config(font=(12))
	espaceLabel221.grid(row = 4, column = 8, columnspan = 1, sticky=EW)




	##########################################################################################################################################
	# separateur
	espaceLabel5 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel5.config(font=(12))
	espaceLabel5.grid(row = 5, column = 0, columnspan = 7, sticky=EW)





	##########################################################################################################################################
	# Creation du boutton submit Genomes choice
	espaceLabel41 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel41.config(font=(12))
	espaceLabel41.grid(row = 6, column = 0, columnspan = 1, sticky=EW)

	fDATA = Frame(newWindow, highlightbackground="#8888FF", highlightcolor="#8888FF", highlightthickness=2, bd=2, bg="#8888FF")
	fDATA.grid(row = 6, column = 1, columnspan = 7, sticky=NSEW)

	SubmitDATA = ttk.Button(fDATA, text="Submit Genomes Files", command = lambda: closeGenomeWindow(newWindow, pathVisualDATA) )
	SubmitDATA.pack(expand=TRUE, fill=BOTH)

	espaceLabel42 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel42.config(font=(12))
	espaceLabel42.grid(row = 6, column = 8, columnspan = 1, sticky=EW)





	##########################################################################################################################################
	# separateur
	espaceLabel3 = Label(newWindow, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel3.config(font=(24))
	espaceLabel3.grid(row = 7, column = 0, columnspan = 9, sticky=EW)
