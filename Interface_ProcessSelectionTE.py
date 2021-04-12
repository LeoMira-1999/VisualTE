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
progres = ''
check01 = ''
check02 = ''
check03 = ''
check04 = ''
check05 = ''
check06 = ''
check07 = ''
check08 = ''
check09 = ''
check10 = ''
check11 = ''
check12 = ''
check13 = ''
check14 = ''
check15 = ''
check16 = ''
check17 = ''
check18 = ''
check19 = ''





########################################################################################################################
###	Create new widget
########################################################################################################################
def DrawNewWindow(root2) :

	global check01
	global check02
	global check03
	global check04
	global check05
	global check06
	global check07
	global check08
	global check09
	global check10
	global check11
	global check12
	global check13
	global check14
	global check15
	global check16
	global check17
	global check18
	global check19

	global progres
	global root
	root = root2


	########################################################################################################################
	# separateur
	espaceLabel01 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel01.config(font=(12))
	espaceLabel01.grid(row = 0, column = 0, columnspan = 12, sticky=EW)



	########################################################################################################################
	# titre de l'interface
	espaceLabel02 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel02.config(font=(12))
	espaceLabel02.grid(row = 1, column = 0, columnspan = 1, sticky=EW)

	textLabel01 = Label(root, text = 'Processing for the selected TE(s)...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel01.config(font=(24))
	textLabel01.grid(row = 1, column = 1, columnspan = 10, sticky=EW)

	espaceLabel03 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel03.config(font=(12))
	espaceLabel03.grid(row = 1, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	# separateur
	espaceLabel04 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel04.config(font=(12))
	espaceLabel04.grid(row = 2, column = 0, columnspan = 7, sticky=EW)



	########################################################################################################################
	espaceLabel05 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel05.config(font=(12))
	espaceLabel05.grid(row = 3, column = 0, columnspan = 1, sticky=EW)

	textLabel02 = Label(root, text = 'Creating Selected TE File ...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel02.config(font=(24))
	textLabel02.grid(row = 3, column = 1, columnspan = 8, sticky=EW)

	espaceLabel06 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel06.config(font=(12))
	espaceLabel06.grid(row = 3, column = 9, columnspan = 1, sticky=EW)

	check01 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check01.grid(row = 3, column = 10, columnspan = 1, sticky=EW)

	espaceLabel07 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel07.config(font=(12))
	espaceLabel07.grid(row = 3, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel08 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel08.config(font=(12))
	espaceLabel08.grid(row = 4, column = 0, columnspan = 1, sticky=EW)

	textLabel03 = Label(root, text = 'Loading TE File ...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel03.config(font=(24))
	textLabel03.grid(row = 4, column = 1, columnspan = 8, sticky=EW)

	espaceLabel09 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel09.config(font=(12))
	espaceLabel09.grid(row = 4, column = 9, columnspan = 1, sticky=EW)

	check02 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check02.grid(row = 4, column = 10, columnspan = 1, sticky=EW)

	espaceLabel10 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel10.config(font=(12))
	espaceLabel10.grid(row = 4, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel14 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel14.config(font=(12))
	espaceLabel14.grid(row = 5, column = 0, columnspan = 1, sticky=EW)

	textLabel05 = Label(root, text = 'Creating Genic Environment File ...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel05.config(font=(24))
	textLabel05.grid(row = 5, column = 1, columnspan = 8, sticky=EW)

	espaceLabel15 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel15.config(font=(12))
	espaceLabel15.grid(row = 5, column = 9, columnspan = 1, sticky=EW)

	check03 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check03.grid(row = 5, column = 10, columnspan = 1, sticky=EW)

	espaceLabel16 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel16.config(font=(12))
	espaceLabel16.grid(row = 5, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel54 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel54.config(font=(12))
	espaceLabel54.grid(row = 6, column = 0, columnspan = 1, sticky=EW)

	textLabel55 = Label(root, text = 'Creating TE Alignment and Phylogenetic Tree Files ...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel55.config(font=(24))
	textLabel55.grid(row = 6, column = 1, columnspan = 8, sticky=EW)

	espaceLabel55 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel55.config(font=(12))
	espaceLabel55.grid(row = 6, column = 9, columnspan = 1, sticky=EW)

	check04 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check04.grid(row = 6, column = 10, columnspan = 1, sticky=EW)

	espaceLabel56 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel56.config(font=(12))
	espaceLabel56.grid(row = 6, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel14 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel14.config(font=(12))
	espaceLabel14.grid(row = 7, column = 0, columnspan = 1, sticky=EW)

	textLabel05 = Label(root, text = 'Creating Random Sequences and Their Genic Environment...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel05.config(font=(24))
	textLabel05.grid(row = 7, column = 1, columnspan = 8, sticky=EW)

	espaceLabel15 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel15.config(font=(12))
	espaceLabel15.grid(row = 7, column = 9, columnspan = 1, sticky=EW)

	check05 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check05.grid(row = 7, column = 10, columnspan = 1, sticky=EW)

	espaceLabel16 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel16.config(font=(12))
	espaceLabel16.grid(row = 7, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel11 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel11.config(font=(12))
	espaceLabel11.grid(row = 8, column = 0, columnspan = 1, sticky=EW)

	textLabel04 = Label(root, text = 'Looking for GeneOntology for TE Sequences ...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel04.config(font=(24))
	textLabel04.grid(row = 8, column = 1, columnspan = 8, sticky=EW)

	espaceLabel12 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel12.config(font=(12))
	espaceLabel12.grid(row = 8, column = 9, columnspan = 1, sticky=EW)

	check06 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check06.grid(row = 8, column = 10, columnspan = 1, sticky=EW)

	espaceLabel13 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel13.config(font=(12))
	espaceLabel13.grid(row = 8, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel14 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel14.config(font=(12))
	espaceLabel14.grid(row = 9, column = 0, columnspan = 1, sticky=EW)

	textLabel05 = Label(root, text = 'Selecting Overlap TFBS for TE Sequences ...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel05.config(font=(24))
	textLabel05.grid(row = 9, column = 1, columnspan = 8, sticky=EW)

	espaceLabel15 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel15.config(font=(12))
	espaceLabel15.grid(row = 9, column = 9, columnspan = 1, sticky=EW)

	check07 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check07.grid(row = 9, column = 10, columnspan = 1, sticky=EW)

	espaceLabel16 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel16.config(font=(12))
	espaceLabel16.grid(row = 9, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel14 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel14.config(font=(12))
	espaceLabel14.grid(row = 10, column = 0, columnspan = 1, sticky=EW)

	textLabel05 = Label(root, text = 'Selecting Overlap TFBS for Random Sequences...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel05.config(font=(24))
	textLabel05.grid(row = 10, column = 1, columnspan = 8, sticky=EW)

	espaceLabel15 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel15.config(font=(12))
	espaceLabel15.grid(row = 10, column = 9, columnspan = 1, sticky=EW)

	check08 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check08.grid(row = 10, column = 10, columnspan = 1, sticky=EW)

	espaceLabel16 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel16.config(font=(12))
	espaceLabel16.grid(row = 10, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel134 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel134.config(font=(12))
	espaceLabel134.grid(row = 11, column = 0, columnspan = 1, sticky=EW)

	textLabel035 = Label(root, text = 'Printing Overlap TFBS for TE/Random Sequences...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel035.config(font=(24))
	textLabel035.grid(row = 11, column = 1, columnspan = 8, sticky=EW)

	espaceLabel135 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel135.config(font=(12))
	espaceLabel135.grid(row = 11, column = 9, columnspan = 1, sticky=EW)

	check09 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check09.grid(row = 11, column = 10, columnspan = 1, sticky=EW)

	espaceLabel136 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel136.config(font=(12))
	espaceLabel136.grid(row = 11, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel11 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel11.config(font=(12))
	espaceLabel11.grid(row = 12, column = 0, columnspan = 1, sticky=EW)

	textLabel04 = Label(root, text = 'Creating Main File (VisualTE3.py) ...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel04.config(font=(24))
	textLabel04.grid(row = 12, column = 1, columnspan = 8, sticky=EW)

	espaceLabel12 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel12.config(font=(12))
	espaceLabel12.grid(row = 12, column = 9, columnspan = 1, sticky=EW)

	check10 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check10.grid(row = 12, column = 10, columnspan = 1, sticky=EW)

	espaceLabel13 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel13.config(font=(12))
	espaceLabel13.grid(row = 12, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel17 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel17.config(font=(12))
	espaceLabel17.grid(row = 13, column = 0, columnspan = 1, sticky=EW)

	textLabel06 = Label(root, text = 'Creating TE Genome Browser File Function ...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel06.config(font=(24))
	textLabel06.grid(row = 13, column = 1, columnspan = 8, sticky=EW)

	espaceLabel18 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel18.config(font=(12))
	espaceLabel18.grid(row = 13, column = 9, columnspan = 1, sticky=EW)

	check11 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check11.grid(row = 13, column = 10, columnspan = 1, sticky=EW)

	espaceLabel19 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel19.config(font=(12))
	espaceLabel19.grid(row = 13, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel20 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel20.config(font=(12))
	espaceLabel20.grid(row = 14, column = 0, columnspan = 1, sticky=EW)

	textLabel07 = Label(root, text = 'Creating TE Chromosome Distribution File Function ...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel07.config(font=(24))
	textLabel07.grid(row = 14, column = 1, columnspan = 8, sticky=EW)

	espaceLabel21 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel21.config(font=(12))
	espaceLabel21.grid(row = 14, column = 9, columnspan = 1, sticky=EW)

	check12 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check12.grid(row = 14, column = 10, columnspan = 1, sticky=EW)

	espaceLabel22 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel22.config(font=(12))
	espaceLabel22.grid(row = 14, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel23 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel23.config(font=(12))
	espaceLabel23.grid(row = 15, column = 0, columnspan = 1, sticky=EW)

	textLabel08 = Label(root, text = 'Creating TE General Features File Function ...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel08.config(font=(24))
	textLabel08.grid(row = 15, column = 1, columnspan = 8, sticky=EW)

	espaceLabel24 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel24.config(font=(12))
	espaceLabel24.grid(row = 15, column = 9, columnspan = 1, sticky=EW)

	check13 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check13.grid(row = 15, column = 10, columnspan = 1, sticky=EW)

	espaceLabel25 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel25.config(font=(12))
	espaceLabel25.grid(row = 15, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel32 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel32.config(font=(12))
	espaceLabel32.grid(row = 16, column = 0, columnspan = 1, sticky=EW)

	textLabel11 = Label(root, text = 'Creating TE Overlapping TFBS File Function ...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel11.config(font=(24))
	textLabel11.grid(row = 16, column = 1, columnspan = 8, sticky=EW)

	espaceLabel33 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel33.config(font=(12))
	espaceLabel33.grid(row = 16, column = 9, columnspan = 1, sticky=EW)

	check14 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check14.grid(row = 16, column = 10, columnspan = 1, sticky=EW)

	espaceLabel34 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel34.config(font=(12))
	espaceLabel34.grid(row = 16, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel35 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel35.config(font=(12))
	espaceLabel35.grid(row = 17, column = 0, columnspan = 1, sticky=EW)

	textLabel12 = Label(root, text = 'Creating TE Similarity Occurrences File Function ...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel12.config(font=(24))
	textLabel12.grid(row = 17, column = 1, columnspan = 8, sticky=EW)

	espaceLabel36 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel36.config(font=(12))
	espaceLabel36.grid(row = 17, column = 9, columnspan = 1, sticky=EW)

	check15 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check15.grid(row = 17, column = 10, columnspan = 1, sticky=EW)

	espaceLabel37 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel37.config(font=(12))
	espaceLabel37.grid(row = 17, column = 11, columnspan = 1, sticky=EW)




	########################################################################################################################
	espaceLabel38 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel38.config(font=(12))
	espaceLabel38.grid(row = 18, column = 0, columnspan = 1, sticky=EW)

	textLabel13 = Label(root, text = 'Creating TE Gene Distance file ...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel13.config(font=(24))
	textLabel13.grid(row = 18, column = 1, columnspan = 8, sticky=EW)

	espaceLabel39 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel39.config(font=(12))
	espaceLabel39.grid(row = 18, column = 9, columnspan = 1, sticky=EW)

	check16 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check16.grid(row = 18, column = 10, columnspan = 1, sticky=EW)

	espaceLabel40 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel40.config(font=(12))
	espaceLabel40.grid(row = 18, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel138 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel138.config(font=(12))
	espaceLabel138.grid(row = 19, column = 0, columnspan = 1, sticky=EW)

	textLabel113 = Label(root, text = 'Creating TE Genetic Functions File ...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel113.config(font=(24))
	textLabel113.grid(row = 19, column = 1, columnspan = 8, sticky=EW)

	espaceLabel139 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel139.config(font=(12))
	espaceLabel139.grid(row = 19, column = 9, columnspan = 1, sticky=EW)

	check17 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check17.grid(row = 19, column = 10, columnspan = 1, sticky=EW)

	espaceLabel140 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel140.config(font=(12))
	espaceLabel140.grid(row = 19, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	espaceLabel41 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel41.config(font=(12))
	espaceLabel41.grid(row = 20, column = 0, columnspan = 1, sticky=EW)

	textLabel14 = Label(root, text = 'Creating Summary Table File ...', borderwidth=5, bg="#F5F5FF", anchor='w')
	textLabel14.config(font=(24))
	textLabel14.grid(row = 20, column = 1, columnspan = 8, sticky=EW)

	espaceLabel42 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel42.config(font=(12))
	espaceLabel42.grid(row = 20, column = 9, columnspan = 1, sticky=EW)

	check18 = Checkbutton(root, borderwidth=5, bg="#F5F5FF")
	check18.grid(row = 20, column = 10, columnspan = 1, sticky=EW)

	espaceLabel43 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel43.config(font=(12))
	espaceLabel43.grid(row = 20, column = 11, columnspan = 1, sticky=EW)


	########################################################################################################################
	# separateur
	espaceLabel44 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel44.config(font=(12))
	espaceLabel44.grid(row = 21, column = 0, columnspan = 12, sticky=EW)



	########################################################################################################################
	# Progress bar de l'acquisition des datas
	espaceLabel45 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel45.config(font=(12))
	espaceLabel45.grid(row = 22, column = 0, columnspan = 1, sticky=EW)

	progres = progressbar = ttk.Progressbar(root, orient = HORIZONTAL, mode = 'determinate', length=1000 )
	progres.grid(row = 22, column = 1, columnspan = 10, sticky=EW)
	progres["value"] = 0
	progres["maximum"] = 1000
	progres.start()

	espaceLabel46 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel46.config(font=(12))
	espaceLabel46.grid(row = 22, column = 11, columnspan = 1, sticky=EW)



	########################################################################################################################
	# separateur
	espaceLabel47 = Label(root, text = '     ', borderwidth=5, bg="#F5F5FF")
	espaceLabel47.config(font=(12))
	espaceLabel47.grid(row = 23, column = 0, columnspan = 12, sticky=EW)

	root.update()










########################################################################################################################
# 	Change the Label and finish the processing
########################################################################################################################
def ChangeCheckbutton(number) :

	global root
	global progres

	global check01
	global check02
	global check03
	global check04
	global check05
	global check06
	global check07
	global check08
	global check09
	global check10
	global check11
	global check12
	global check13
	global check14
	global check15
	global check16
	global check17
	global check18
	global check19


	if number == 1 :
		check01.select()
		progres.step(50)
	elif number == 2 :
		check02.select()
		progres.step(50)		# somme 100 / 1000
	elif number == 3 :
		check03.select()
		progres.step(100)		# somme 200 / 1000
	elif number == 4 :
		check04.select()
		progres.step(100)		# somme 300 / 1000
	elif number == 5 :
		check05.select()
		progres.step(50)		# somme 350 / 1000
	elif number == 6 :
		check06.select()
		progres.step(100)		# somme 450 / 1000
	elif number == 7 :
		check07.select()
		progres.step(50)		# somme 500 / 1000
	elif number == 8 :
		check08.select()
		progres.step(25)		# somme 525 / 1000
	elif number == 9 :
		check09.select()
		progres.step(25)		# somme 550 / 1000
	elif number == 10 :
		check10.select()
		progres.step(50)		# somme 600 / 1000
	elif number == 11 :
		check11.select()
		progres.step(50)		# somme 650 / 1000
	elif number == 12 :
		check12.select()
		progres.step(50)		# somme 700 / 1000
	elif number == 13 :
		check13.select()
		progres.step(50)		# somme 750 / 1000
	elif number == 14 :
		check14.select()
		progres.step(50)		# somme 800 / 1000
	elif number == 15 :
		check15.select()
		progres.step(50)		# somme 850 / 1000
	elif number == 16 :
		check16.select()
		progres.step(50)		# somme 900 / 1000
	elif number == 17 :
		check17.select()
		progres.step(50)		# somme 950 / 1000
	elif number == 18 :
		check18.select()
		progres.step(50)		# somme 1000 / 1000
		time.sleep(2)

	root.update()










########################################################################################################################
###	Create the function (tab) files
########################################################################################################################
def CreateFonctionDASH(pathVisual, pathVisualNEW, OfficialName, list_selection_TE) :

	ListeConsensus = Create_CommonDATA2.writeSelectTE(pathVisual, pathVisualNEW, OfficialName, list_selection_TE)
	ChangeCheckbutton(1)



	# Import the recently created modules
	pathSelectTE = os.path.realpath(pathVisualNEW + '/Functions/CommonDATA_SelectTEs.py')
	loaderSelectTE = importlib.util.spec_from_file_location('CommonDATA_SelectTEs', pathSelectTE)
	moduleSelectTE = importlib.util.module_from_spec(loaderSelectTE)
	loaderSelectTE.loader.exec_module(moduleSelectTE)

	pathCommonDATA = os.path.realpath(pathVisualNEW + '/Functions/CommonDATA.py')
	loaderCommonDATA = importlib.util.spec_from_file_location('CommonDATA', pathCommonDATA)
	moduleCommonDATA = importlib.util.module_from_spec(loaderCommonDATA)
	loaderCommonDATA.loader.exec_module(moduleCommonDATA)
	ChangeCheckbutton(2)



	# Get the genetic Environment
	NameSeq, DEB, FIN, Sens, Size, Similarity, listGeneSelect5, listGeneSelect3, listGeneSelectInside = Create_SelectedAnnotations.SelectAnnotations(pathVisual, pathVisualNEW, moduleSelectTE, moduleCommonDATA, list_selection_TE, ListeConsensus)
	ChangeCheckbutton(3)


	# Extract the sequences from the genome and run the alignment
	Create_Alignment_and_Tree.AlignETPhylogeny(pathVisual, pathVisualNEW, moduleCommonDATA, moduleSelectTE, NameSeq, DEB, FIN, Sens, Size, Similarity)
	ChangeCheckbutton(4)



	# Create 'random sequences' from TE sequences
	randomSeqDEB, randomSeqFIN, randomSeqCHR = Create_Random_Sequences.RandomSequences(pathVisual, pathVisualNEW, moduleSelectTE, NameSeq, DEB, FIN, list_selection_TE, listGeneSelect5, listGeneSelect3, listGeneSelectInside)
	ChangeCheckbutton(5)



	# ici creer la fonction qui recupere les overlap TFBS pour TE et aleatoires
	tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_Global, organ_dictionary_Global = Create_Overlap_TFBS.ExtractTFBS_forTE(pathVisual, pathVisualNEW, list_selection_TE, moduleCommonDATA, NameSeq, DEB, FIN, listGeneSelect5, listGeneSelect3)
	ChangeCheckbutton(6)



	# ici creer la fonction qui recupere les overlap TFBS pour TE et aleatoires
	tissue_dictionary_RandomSeq, organ_dictionary_RandomSeq, tissue_dictionary_Global, organ_dictionary_Global = Create_Overlap_TFBS.ExtractTFBS_forRandom(pathVisual, pathVisualNEW, list_selection_TE, moduleCommonDATA, randomSeqCHR, randomSeqDEB, randomSeqFIN, tissue_dictionary_Global, organ_dictionary_Global)
	ChangeCheckbutton(7)



	# ici ecrit les resultats obtenus pour les TFBS
	Create_Overlap_TFBS.PrintGlobalTFBS(pathVisualNEW, list_selection_TE, tissue_dictionary_Global, organ_dictionary_Global, tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_RandomSeq, organ_dictionary_RandomSeq)
	ChangeCheckbutton(8)






	#######################################################################################################################################################################
	# Create the function for the TE selected
	# Add few lines in the CommonDATA_SelectTEs file
	Create_CommonDATA2.AjoutAnnotations(pathVisualNEW)
	# Cree le fichier principal qui lance tous les autres
	nbSeq_Assemble, numberTE = Create_MainFile.EcrireVisualTE(pathVisual, pathVisualNEW, moduleSelectTE, moduleCommonDATA)
	ChangeCheckbutton(9)



	# make the genome browser function
	MakeFunction_GenomeBrowser.GenomeBrowser(pathVisual, pathVisualNEW, nbSeq_Assemble, numberTE)
	ChangeCheckbutton(10)



	# make the chromosome + TE percentage function
	MakeFunction_ChromosomeDistribution.ChromosomeDistribution(pathVisualNEW, numberTE)
	ChangeCheckbutton(11)



	# make the genome / chromosome TE size Distribution function
	MakeFunction_GeneralFeaturesDistribution.GeneralFeatures_layout(pathVisual, pathVisualNEW, numberTE)
	ChangeCheckbutton(12)



	# make TE - Gene distance Distribution function
	MakeFunction_DistanceNeighboringGene.DistanceNeighboringGene(pathVisual, pathVisualNEW, nbSeq_Assemble, numberTE)
	ChangeCheckbutton(13)



	# make TE - Gene functions Distribution function
	MakeFunction_NeighboringGeneFunctions.NeighboringGeneFunctions(pathVisual, pathVisualNEW, nbSeq_Assemble, numberTE)
	ChangeCheckbutton(14)



	# make the genome / chromosome TE size Distribution function
	MakeFunction_OverlappingTFBS.OverlappingTFBS(pathVisualNEW, nbSeq_Assemble, numberTE)
	ChangeCheckbutton(15)



	# make the genome / chromosome TE size Distribution function
	MakeFunction_SimilarityOccurrences.SimilarityOccurrences(pathVisualNEW, nbSeq_Assemble, numberTE)
	ChangeCheckbutton(16)



	# make the genome / chromosome TE size Distribution function
	MakeFunction_TEEnvironment.TEEnvironment(pathVisualNEW, nbSeq_Assemble, numberTE)
	ChangeCheckbutton(17)



	# make the genome / chromosome TE size Distribution function
	MakeFunction_SummaryTable.SummaryTable(pathVisualNEW, nbSeq_Assemble, numberTE)
	ChangeCheckbutton(18)


	root.destroy()
