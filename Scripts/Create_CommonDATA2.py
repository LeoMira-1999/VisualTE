#!/usr/bin/python3
import os
import os.path
import sys
import pandas as pd
import shutil
from . import ReadInfos_TE



########################################################################################################################
###	Add the last annotations
########################################################################################################################
def AjoutAnnotations(pathVisualNEW) :

	temp = pathVisualNEW + '/Functions/CommonDATA_SelectTEs.py'
	absolutePath = os.path.abspath(pathVisualNEW)

	f = open(temp, "a")
	f.write("tempFile = '" + absolutePath + "/Downloaded/DATA_Selected_Genes.txt' \n")
	f.write("dataFrame_MyGene = pd.read_csv(tempFile) \n")
	f.write("tempFile = '" + absolutePath + "/Downloaded/DATA_Selected_GeneExon.txt' \n")
	f.write("dataFrame_MyGeneExon = pd.read_csv(tempFile) \n")
	f.write("tempFile = '" + absolutePath + "/Downloaded/DATA_Selected_OtherTE.txt' \n")
	f.write("dataFrame_MyOtherTEs = pd.read_csv(tempFile) \n")
	f.write("tempFile = '" + absolutePath + "/Downloaded/DATA_Selected_Pseudo.txt' \n")
	f.write("dataFrame_MyPseudo = pd.read_csv(tempFile) \n")
	f.write("tempFile = '" + absolutePath + "/Downloaded/DATA_Selected_ncRNA.txt' \n")
	f.write("dataFrame_MyNcRNA = pd.read_csv(tempFile) \n")
	f.write("tempFile = '" + absolutePath + "/Downloaded/DATA_Selected_ClosestGenes.txt' \n")
	f.write("dataFrame_CloseGene = pd.read_csv(tempFile) \n")

	f.write("tempFile = '" + absolutePath + "/Downloaded/DATA_RandomSequences.txt' \n")
	f.write("dataFrame_RandomSeq = pd.read_csv(tempFile) \n")
	f.write("tempFile = '" + absolutePath + "/Downloaded/DATA_RandomGene.txt' \n")
	f.write("dataFrame_RandomGene = pd.read_csv(tempFile) \n")


	f.close()





########################################################################################################################
###	Create DATA for all selected TEs
########################################################################################################################

def writeSelectTE(pathVisual, pathVisualNEW, OfficialName, list_selection_TE) :


	print('Now Extracting TE Data from files ...')
	########################################################################################################################
	# Now write down the data ...
	temp = pathVisualNEW + '/Functions/CommonDATA_SelectTEs.py'
	absolutePath = os.path.abspath(pathVisualNEW)
	temp2 = pathVisual + '/Functions/CommonDATA.py'
	absolutePathOLD = os.path.abspath(pathVisual)

	f = open(temp, "w")

	f.write("#!/usr/bin/env python3 \n")
	f.write("# -*- coding: utf-8 -*- \n")
	f.write("import os \n")
	f.write("import sys \n")
	f.write("import pandas as pd \n")
	#f.write("from Functions import Couleur \n\n")

	f.write("######################################################################################################################## \n")
	f.write("OfficialName = '")
	f.write(OfficialName + "' \n")
	f.write("list_selection_TE = [")
	for i in range(0,len(list_selection_TE), 1) :
		f.write("'" + list_selection_TE[i] + "', ")
	f.write("] \n")

	# Extract the TE group the user sequence belongs
	SuperfamilyTE = ''
	ListeConsensus = []
	TailleConsensus = 'TailleConsensus = ['
	MinTaille = 10000000
	MaxTaille = 0
	f.write('SequenceTEs = [ \n')
	for i in range(0,len(list_selection_TE), 1) :
		SuperfamilyTE, SequenceConsensus = ReadInfos_TE.GetSuperfamily('Scripts/DATA/Repbase/Data_Repbase.txt', list_selection_TE[i])
		ListeConsensus.append(SequenceConsensus)
		f.write("\t'" + SequenceConsensus + "', \n")
		TailleConsensus += str(len(SequenceConsensus)) + ', '
		if MinTaille > len(SequenceConsensus) :
			MinTaille = len(SequenceConsensus)
		if MaxTaille < len(SequenceConsensus) :
			MaxTaille = len(SequenceConsensus)
	TailleConsensus += '] '
	f.write('] \n')
	f.write("SuperfamilyTE = '")
	f.write(SuperfamilyTE + "' \n")
	f.write(TailleConsensus + ' \n')
	f.write("MinTaille = ")
	f.write(str(MinTaille) + " \n")
	f.write("MaxTaille = ")
	f.write(str(MaxTaille) + " \n")

	couleurV2 = ['#7FFF00', '#32CD32', '#90EE90', '#3CB371', '#228B22', '#006400', '#6B8E23', '#808000', '#E0FFFF', '#AFEEEE', '#40E0D0', '#4682B4', '#B0E0E6', '#87CEFA', '#1E90FF', '#6495ED', '#0000FF', '#000080', '#483D8B', '#4B0082', '#FFD700', '#FED8B1', '#FFFACD', '#DC143C', '#F08080', '#FF8C00', '#FFDAB9']
	ListeObject = ['DNA Transposon', 'EnSpm/CACTA', 'Merlin', 'MuDR Transposon', 'Tc1/Mariner', 'Crypton', 'Helitron', 'Polinton', 'BEL', 'Copia', 'DIRS', 'ERV', 'Gypsy', 'LTR Retrotransposon', 'CR1', 'L1', 'Non-LTR retrotransposon', 'R2', 'RTE', 'SINE', '(Micro)Satelitte', 'Unclassified TE', 'Gene', 'Pseudo', 'ncRNA', 'Intergenic']
	f.write("CouleurSuperTE = ")
	indiceSuper = 0
	for z in range(0, len(ListeObject), 1):	# 27 number of color
		if ListeObject[z] == SuperfamilyTE :
			indiceSuper = z
			break
	f.write("'" + couleurV2[indiceSuper] + "'\n\n")


	f.write("######################################################################################################################## \n")
	f.write("tempFile = '" + absolutePath + "/Downloaded/DATA_SelectedTE.txt' \n")
	f.write("dataFrame_MyTE = pd.read_csv(tempFile) \n")
	f.write("tempFile = '" + absolutePathOLD + "/Downloaded/DATA_AllTEs.txt' \n")
	f.write("dataT = pd.read_csv(tempFile) \n")
	f.write("dataFrame_superTE =  dataT.loc[(dataT['TE group'] == SuperfamilyTE)] \n")

	f.close()





	# get the data for the organism
	dataFrame_AllTEs = ''
	tempFile = pathVisual + '/Downloaded/DATA_AllTEs.txt'
	dataT = pd.read_csv(tempFile)
	# Create first a sud-dataframe that contains only the wanted values
	for i in range(0,len(list_selection_TE), 1) :
		if i == 0 :
			dataFrame_AllTEs = dataT.loc[ (dataT['TE Family'] == list_selection_TE[i]), : ]
		else :
			temp = dataT.loc[ (dataT['TE Family'] == list_selection_TE[i]), : ]
			dataFrame_AllTEs = pd.concat([dataFrame_AllTEs, temp])

	total_rows = len(dataFrame_AllTEs)
	NameID = dataFrame_AllTEs['Chr ID'].tolist()
	listIndex = []
	listID = []
	for i in range(0, total_rows, 1) :
		listIndex.append(i)
		listID.append(NameID[i])
	dataFrame_AllTEs.insert(0, "Index", listIndex, True)
	dataFrame_AllTEs.insert(2, "Chr Name", listID, True)

	tempFile = pathVisual + '/Downloaded/DATA_Organism.txt'
	dataT = pd.read_csv(tempFile)
	# Create first a sud-dataframe that contains only the wanted values
	dataFrame_Organism = dataT.loc[(dataT['Size bp'] > 0)]
	SimpleName = dataFrame_Organism['Name'].tolist()
	NameID = dataFrame_Organism['NameID'].tolist()
	RefSeq = dataFrame_Organism['RefSeq'].tolist()
	for i in range(0, len(SimpleName), 1) :
		dataFrame_AllTEs.loc[dataFrame_AllTEs['Chr ID'] == RefSeq[i], 'Chr ID'] = SimpleName[i]
		dataFrame_AllTEs.loc[dataFrame_AllTEs['Chr ID'] == NameID[i], 'Chr ID'] = SimpleName[i]

	pathVisualDownload = pathVisualNEW + '/Downloaded'
	if not os.path.exists(pathVisualDownload):
		os.mkdir(pathVisualDownload)
	tempFile = pathVisualDownload + '/DATA_SelectedTE.txt'
	dataFrame_AllTEs.to_csv(tempFile, index = False) # relative position

	return ListeConsensus
