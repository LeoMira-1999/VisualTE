#!/usr/bin/python3
import os
import sys
import pandas as pd
import shutil

########################################################################################################################
###	Create DATA for all the functions
########################################################################################################################

def PrepareCommonDATA(pathVisual, nameOrganism, nbSeq_Assemble, maxSize, taxon, fileFNAgenome, dictionary_organ, dictionary_tissue):
	
	# get the data for the organism
	tempFile = pathVisual + '/Downloaded/DATA_Organism.txt'
	dataT = pd.read_csv(tempFile)
	# Create first a sud-dataframe that contains only the wanted values
	dataFrame_Organism = dataT.loc[(dataT['Size bp'] > 0)]

	# get the data for the gene
	tempFile = pathVisual + '/Downloaded/DATA_GeneExon.txt'
	dataFrame_Gene = pd.read_csv(tempFile, dtype={"Chr Name": object})

	# get the data for the pseudogene
	tempFile = pathVisual + '/Downloaded/DATA_Pseudo.txt'
	dataFrame_Pseudogene = pd.read_csv(tempFile)

	# get the data for the ncRNA
	tempFile = pathVisual + '/Downloaded/DATA_ncRNA.txt'
	dataFrame_ncRNA = pd.read_csv(tempFile)

	# get the data for the ALL TEs
	tempFile = pathVisual + '/Downloaded/DATA_TE_forDash.txt'
	dataFrame_ALLTEs = pd.read_csv(tempFile)

	SelectionID = dataFrame_Organism['NameID'].tolist()
	SelectionSize = dataFrame_Organism['Size bp'].tolist()
	SelectionName = dataFrame_Organism['Name'].tolist()
	


	########################################################################################################################
	# Now write down the data ...
	temp = pathVisual + '/Functions/CommonDATA.py'
	absolutePath = os.path.abspath(pathVisual)

	f = open(temp, "w")
	f.write("#!/usr/bin/env python3 \n")
	f.write("# -*- coding: utf-8 -*- \n")
	f.write("import os \n")
	f.write("import sys \n")
	f.write("import pandas as pd \n")
	#f.write("from Functions import Couleur \n\n")


	
	f.write("######################################################################################################################## \n")
	# Write the 'simple' data
	f.write("nameOrganism = '")
	f.write(nameOrganism)
	f.write("'\n")
	f.write("nbSeq_Assemble = ")
	f.write(str(nbSeq_Assemble))
	f.write("\n")
	f.write("maxSize = ")
	f.write(str(maxSize))
	f.write("\n")
	f.write("taxon = ")
	f.write(str(taxon))
	f.write("\n")
	f.write("echelleFor1bp = (1500 + 200) / maxSize \n")
	
	totalSizeGenome = 0
	for i in range(0, len(SelectionSize), 1) :
		totalSizeGenome = totalSizeGenome + SelectionSize[i]
	f.write("totalSizeGenome = ")
	f.write(str(totalSizeGenome))
	f.write("\n")
	f.write("TailleSequence = [")
	for i in range(0, len(SelectionSize), 1) :
		f.write(str(SelectionSize[i]) + ', ')
	f.write(str(totalSizeGenome) + ",] \n\n")
	f.write("\n\n\n\n")
	
	
	
	f.write("######################################################################################################################## \n")
	f.write("# get the dataframe for the plotly and sliders \n")
	f.write("tempFile = '" + absolutePath + "/Downloaded/DATA_Organism.txt' \n")
	f.write("dataT = pd.read_csv(tempFile) \n")
	f.write("# Create first a sud-dataframe that contains only the wanted values \n")
	f.write("dataFrame_Organism = dataT.loc[(dataT['Size bp'] > 0)] \n")
	f.write("tempFile = '" + absolutePath + "/Downloaded/DATA_AllTEs.txt' \n")
	f.write("dataFrame_otherTE = pd.read_csv(tempFile) \n")
	f.write("tempFile = '" + absolutePath + "/Downloaded/DATA_TE_forDash.txt' \n")
	f.write("dataFrame_infoGlobal_TE = pd.read_csv(tempFile) \n")
	f.write("tempFile = '" + absolutePath + "/Downloaded/DATA_Gene.txt' \n")
	f.write("dataFrame_Gene = pd.read_csv(tempFile) \n")
	f.write("tempFile = '" + absolutePath + "/Downloaded/DATA_Pseudo.txt' \n")
	f.write("dataFrame_Pseudo = pd.read_csv(tempFile) \n")
	f.write("tempFile = '" + absolutePath + "/Downloaded/DATA_ncRNA.txt' \n")
	f.write("dataFrame_ncRNA = pd.read_csv(tempFile) \n")
	tempFile = fileFNAgenome.split('/')
	fileFNAgenome = tempFile[len(tempFile)-1]
	f.write("fileFNAgenome = '" + absolutePath + "/Downloaded/" + fileFNAgenome + "'\n")	
	
	f.write("\n\n\n")


	
	f.write("######################################################################################################################## \n")
	NbHit_Gene_chr = []
	NbHit_Pseudo_chr = []
	NbHit_ncRNA_chr = []
	Size_Gene_chr = []
	Size_Pseudo_chr = []
	Size_ncRNA_chr = []
	percent_Size_Gene_chr = []
	percent_Size_Pseudo_chr = []
	percent_Size_ncRNA_chr = []

	# Get the values for the genes
	for i in range(0, len(SelectionID), 1) :
		Select_Gene = dataFrame_Gene.loc[ (dataFrame_Gene['Chr ID'] == SelectionID[i]), ['Start', 'End'] ] 
		GeneDEB = Select_Gene['Start'].tolist()
		GeneFIN = Select_Gene['End'].tolist()
		Size_Gene_chr.append(0)
		NbHit_Gene_chr.append(len(GeneDEB))
		for j in range(0, len(GeneDEB), 1) :
			Size_Gene_chr[i] += GeneFIN[j] - GeneDEB[j]
	Size_Gene_chr.append(0)
	NbHit_Gene_chr.append(0)
	for i in range(0, len(SelectionID), 1) :
		Size_Gene_chr[len(Size_Gene_chr)-1] += Size_Gene_chr[i]	
		NbHit_Gene_chr[len(Size_Gene_chr)-1] += NbHit_Gene_chr[i]	

	for i in range(0, len(SelectionID), 1) :
		Select_Gene = dataFrame_Gene.loc[ (dataFrame_Gene['Chr ID'] == SelectionID[i]), ['Start', 'End'] ] 
		GeneDEB = Select_Gene['Start'].tolist()
		GeneFIN = Select_Gene['Start'].tolist()
		percent_Size_Gene_chr.append( round( (100 * Size_Gene_chr[i] / SelectionSize[i]), 2 ) )
	percent_Size_Gene_chr.append( round( (100 * Size_Gene_chr[len(Size_Gene_chr)-1] / totalSizeGenome), 2 ) )

	# Get the values for the pseudogenes
	for i in range(0, len(SelectionID), 1) :
		Select_Pseudo = dataFrame_Pseudogene.loc[ (dataFrame_Pseudogene['Chr ID'] == SelectionID[i]), ['Start', 'End'] ] 
		PseudoDEB = Select_Pseudo['Start'].tolist()
		PseudoFIN = Select_Pseudo['End'].tolist()
		Size_Pseudo_chr.append(0)
		NbHit_Pseudo_chr.append(len(PseudoDEB))
		for j in range(0, len(PseudoDEB), 1) :
			Size_Pseudo_chr[i] += PseudoFIN[j] - PseudoDEB[j]
	Size_Pseudo_chr.append(0)
	NbHit_Pseudo_chr.append(0)
	for i in range(0, len(SelectionID), 1) :
		Size_Pseudo_chr[len(Size_Pseudo_chr)-1] += Size_Pseudo_chr[i]
		NbHit_Pseudo_chr[len(Size_Pseudo_chr)-1] += NbHit_Pseudo_chr[i]

	for i in range(0, len(SelectionID), 1) :
		Select_Pseudo = dataFrame_Pseudogene.loc[ (dataFrame_Pseudogene['Chr ID'] == SelectionID[i]), ['Start', 'End'] ] 
		PseudoDEB = Select_Pseudo['Start'].tolist()
		PseudoFIN = Select_Pseudo['Start'].tolist()
		percent_Size_Pseudo_chr.append( round( (100 * Size_Pseudo_chr[i] / SelectionSize[i]), 2 ) )
	percent_Size_Pseudo_chr.append( round( (100 * Size_Pseudo_chr[len(Size_Gene_chr)-1] / totalSizeGenome), 2 ) )

	# Get the values for the ncRNA
	for i in range(0, len(SelectionID), 1) :
		Select_ncRNA = dataFrame_ncRNA.loc[ (dataFrame_ncRNA['Chr ID'] == SelectionID[i]), ['Start', 'End'] ] 
		ncRNADEB = Select_ncRNA['Start'].tolist()
		ncRNAFIN = Select_ncRNA['End'].tolist()
		Size_ncRNA_chr.append(0)
		NbHit_ncRNA_chr.append(len(ncRNADEB))
		for j in range(0, len(ncRNADEB), 1) :
			Size_ncRNA_chr[i] += ncRNAFIN[j] - ncRNADEB[j]
	Size_ncRNA_chr.append(0)
	NbHit_ncRNA_chr.append(0)
	for i in range(0, len(SelectionID), 1) :
		Size_ncRNA_chr[len(Size_ncRNA_chr)-1] += Size_ncRNA_chr[i]
		NbHit_ncRNA_chr[len(Size_ncRNA_chr)-1] += NbHit_ncRNA_chr[i]

	for i in range(0, len(SelectionID), 1) :
		Select_ncRNA = dataFrame_ncRNA.loc[ (dataFrame_ncRNA['Chr ID'] == SelectionID[i]), ['Start', 'End'] ] 
		ncRNADEB = Select_ncRNA['Start'].tolist()
		ncRNAFIN = Select_ncRNA['Start'].tolist()
		percent_Size_ncRNA_chr.append( round( (100 * Size_ncRNA_chr[i] / SelectionSize[i]), 2 ) )
	percent_Size_ncRNA_chr.append( round( (100 * Size_ncRNA_chr[len(Size_ncRNA_chr)-1] / totalSizeGenome), 2 ) )

	# Write the data for the NCBI Annotations
	f.write("NbHIT_Gene = [")
	for i in range(0, len(SelectionID)+1, 1) :
		f.write(str(NbHit_Gene_chr[i]))
		f.write(", ")
	f.write("] \n")
	f.write("NbHIT_Pseudogene = [")
	for i in range(0, len(SelectionID)+1, 1) :
		f.write(str(NbHit_Pseudo_chr[i]))
		f.write(", ")
	f.write("] \n")
	f.write("NbHIT_ncRNA = [")
	for i in range(0, len(SelectionID)+1, 1) :
		f.write(str(NbHit_ncRNA_chr[i]))
		f.write(", ")
	f.write("] \n")

	f.write("Size_Gene = [")
	for i in range(0, len(SelectionID)+1, 1) :
		f.write(str(Size_Gene_chr[i]))
		f.write(", ")
	f.write("] \n")
	f.write("Size_Pseudogene = [")
	for i in range(0, len(SelectionID)+1, 1) :
		f.write(str(Size_Pseudo_chr[i]))
		f.write(", ")
	f.write("] \n")
	f.write("Size_ncRNA = [")
	for i in range(0, len(SelectionID)+1, 1) :
		f.write(str(Size_ncRNA_chr[i]))
		f.write(", ")
	f.write("] \n")

	f.write("Percent_Gene = [")
	for i in range(0, len(SelectionID)+1, 1) :
		f.write(str(percent_Size_Gene_chr[i]))
		f.write(", ")
	f.write("] \n")
	f.write("Percent_Pseudogene = [")
	for i in range(0, len(SelectionID)+1, 1) :
		f.write(str(percent_Size_Pseudo_chr[i]))
		f.write(", ")
	f.write("] \n")
	f.write("Percent_ncRNA = [")
	for i in range(0, len(SelectionID)+1, 1) :
		f.write(str(percent_Size_ncRNA_chr[i]))
		f.write(", ")
	f.write("] \n\n\n\n")



	ListeObject = ['MyTE', 'DNA Transposon', 'EnSpm/CACTA', 'Merlin', 'MuDR Transposon', 'Tc1/Mariner', 'Crypton', 'Helitron', 'Polinton', 'BEL', 'Copia', 'DIRS', 'ERV', 'Gypsy', 'LTR Retrotransposon', 'CR1', 'L1', 'Non-LTR retrotransposon', 'R2', 'RTE', 'SINE', '(Micro)Satelitte', 'Unclassified TE', 'Gene', 'Pseudo', 'ncRNA', 'Intergenic']      
	f.write("######################################################################################################################## \n")
	# Write the general data that do not change with slider for the DASH plot
	SelectionRefSeq = dataFrame_Organism['NameID'].tolist()
	Select_DASH = dataFrame_ALLTEs.loc[ (dataFrame_ALLTEs['Chr ID'] == SelectionRefSeq[0]), ['Type TEs', 'Nb Hit', 'Total Size'] ] 
	chr_typeTE = Select_DASH['Type TEs'].tolist()
	tailleListe = len(chr_typeTE)
	f.write("ListeObject = [")
	for j in range(0, len(chr_typeTE), 1) :
		f.write("'" + chr_typeTE[j] + "', ")
	f.write("] \n\n")
			
	f.write("SizeTE_Type = [[0 for x in range(len(ListeObject)+1)] for y in range(nbSeq_Assemble+1)] \n")
	for i in range(0, len(SelectionRefSeq), 1) :
		Select_DASH = dataFrame_ALLTEs.loc[ (dataFrame_ALLTEs['Chr ID'] == SelectionRefSeq[i]), ['Type TEs', 'Nb Hit', 'Total Size'] ] 
		chr_Size = Select_DASH['Total Size'].tolist()
		if len(chr_Size) > 0 :
			f.write("SizeTE_Type[" + str(i) + "] = [")
			for j in range(0, len(chr_Size), 1) :
				f.write(str(chr_Size[j]) + ", ")
			f.write("] \n")
		else :
			f.write("SizeTE_Type[" + str(i) + "] = [")
			for j in range(0, tailleListe, 1) :
				f.write("0, ")
			f.write("] \n")
	f.write("\n")
	
	Total_Hit_AllTEs = 0 
	f.write("NbHitTE_Type = [[0 for x in range(len(ListeObject)+1)] for y in range(nbSeq_Assemble+1)] \n")
	for i in range(0, len(SelectionRefSeq), 1) :
		Select_DASH = dataFrame_ALLTEs.loc[ (dataFrame_ALLTEs['Chr ID'] == SelectionRefSeq[i]), ['Type TEs', 'Nb Hit', 'Total Size'] ]
		chr_nbHit = Select_DASH['Nb Hit'].tolist()
		if len(chr_nbHit) > 0 :
			Total_Hit_AllTEs += chr_nbHit[len(chr_nbHit) - 1]
			f.write("NbHitTE_Type[" + str(i) + "] = [")
			for j in range(0, len(chr_nbHit), 1) :
				f.write(str(chr_nbHit[j]) + ", ")
			f.write("] \n")
		else :
			f.write("NbHitTE_Type[" + str(i) + "] = [")
			for j in range(0, tailleListe, 1) :
				f.write("0, ")
			f.write("] \n")
	f.write("Total_Hit_AllTEs = ")
	f.write(str(Total_Hit_AllTEs) + "\n\n\n")
	
	
	
	f.write("######################################################################################################################## \n")
	tissue = []
	for i in dictionary_tissue.keys():
		tissue.append(i)
	organ = [] 
	for i in dictionary_organ.keys():
		organ.append(i)
	f.write("Tissu_ChipSeq = ")
	f.write(str(tissue) + "\n")
	f.write("Organ_ChipSeq = ")
	f.write(str(organ) + "\n\n\n")
	

	f.write("\n\n")
	f.close()


