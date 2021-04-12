#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import pandas as pd 






###############################################################################################################################################################
###	Print Comptage Global
###############################################################################################################################################################
def PrintGlobalTFBS(pathVisualNEW, list_selection_TE, tissue_dictionary_Global, organ_dictionary_Global, tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_RandomSeq, organ_dictionary_RandomSeq) :
	
	pathSelectTE = pathVisualNEW + '/Functions/CommonDATA_SelectTEs.py'
	f = open(pathSelectTE, "a")
	f.write("\n\n")
	f.write("######################################################################################################################## \n")
	
	
	SizeDict = len(tissue_dictionary_Global)
	f.write("Tissue_ChipSeq_Results = [[0 for x in range(6)] for y in range(" + str(SizeDict) + ")] \n")
	compteur = 0
	for i in tissue_dictionary_Global:
		f.write( "Tissue_ChipSeq_Results[" + str(compteur) + "] = ['" + str(i) + "'" )
		
		for z in range(0, len(list_selection_TE), 1) :
			f.write( ", '" + str(list_selection_TE[z]) + "'" )
		for z in range(0, len(list_selection_TE), 1) :
			temp = 'Random_for_' + list_selection_TE[z]
			f.write( ", '" + str(temp) + "'" )
		f.write( ", " + str(tissue_dictionary_Global[i]) )
		for z in range(0, len(list_selection_TE), 1) :
			#iD_dico_tissue = str(list_selection_TE[z]) + "\t" + str(i)
			if i in tissue_dictionary_SelectedTE.keys():
				f.write( ", " + str(tissue_dictionary_SelectedTE[i]) )
			else :
				f.write( ", 0" )
			if i in tissue_dictionary_RandomSeq.keys():
				f.write( ", " + str(tissue_dictionary_RandomSeq[i]) )
			else :
				f.write( ", 0" )
		f.write( "] \n" )
		compteur += 1
		
	SizeDict = len(organ_dictionary_Global)
	f.write("Organ_ChipSeq_Results = [[0 for x in range(6)] for y in range(" + str(SizeDict) + ")] \n")
	compteur = 0
	for i in organ_dictionary_Global:
		f.write( "Organ_ChipSeq_Results[" + str(compteur) + "] = ['" + str(i) + "'" )
		for z in range(0, len(list_selection_TE), 1) :
			f.write( ", '" + str(list_selection_TE[z]) + "'" )
		for z in range(0, len(list_selection_TE), 1) :
			temp = 'Random_for_' + list_selection_TE[z]
			f.write( ", '" + str(temp) + "'" )
		
		f.write( ", " + str(organ_dictionary_Global[i]) )
		for z in range(0, len(list_selection_TE), 1) :
			#iD_dico_tissue = str(list_selection_TE[z]) + "\t" + str(i)
			if i in organ_dictionary_SelectedTE.keys():
				f.write( ", " + str(organ_dictionary_SelectedTE[i]) )
			else :
				f.write( ", 0" )
			if i in organ_dictionary_RandomSeq.keys():
				f.write( ", " + str(organ_dictionary_RandomSeq[i]) )
			else :
				f.write( ", 0" )
		f.write( "] \n" )
		compteur += 1
		
	f.write("\n")
	f.write("######################################################################################################################## \n")
		
	f.write("\n")
	f.close()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
###############################################################################################################################################################
###	Calculates the TFBS that overlap TE and random sequences
###############################################################################################################################################################
def memorizeDicoTFBS(decoupeTissue, decoupeOrgan, list_selection_TE, z, tissue_Selected, organ_Selected, tissue_Global, organ_Global) :
	
	for a in range(0, len(decoupeTissue), 1) :
		iD_dico_tissue = str(list_selection_TE[z]) + "\t" + str(decoupeTissue[a])
		if iD_dico_tissue in tissue_Selected.keys():
			tissue_Selected[iD_dico_tissue] += 1
		else :
			tissue_Selected[iD_dico_tissue] = 1
		if iD_dico_tissue in tissue_Global.keys():
			tissue_Global[iD_dico_tissue] += 1
		else :
			tissue_Global[iD_dico_tissue] = 1
			
	for a in range(0, len(decoupeOrgan), 1) :
		iD_dico_organ = str(list_selection_TE[z]) + "\t" + str(decoupeOrgan[a])
		if iD_dico_organ in organ_Selected.keys():
			organ_Selected[iD_dico_organ] += 1
		else :
			organ_Selected[iD_dico_organ] = 1
		if iD_dico_organ in organ_Global.keys():
			organ_Global[iD_dico_organ] += 1
		else :
			organ_Global[iD_dico_organ] = 1
		
	
	
	
	
	
	
	
	
	
	
###############################################################################################################################################################
###	Calculates the TFBS that overlap TE and random sequences
###############################################################################################################################################################
def OverlapTFBSRandom(pathVisual, nomFichier, list_selection_TE, NameSeq, DEB, FIN, tissue_dictionary_RandomSeq, organ_dictionary_RandomSeq, tissue_dictionary_Global, organ_dictionary_Global) :
	
	# Get the filename in the same format that the chromosome name memorized
	tempName = nomFichier[:-4] 
	tempName = tempName.title()
	
	for z in range(0, len(list_selection_TE), 1) :		# famille de TE
		indicesTE = [x for x in range(0, len(NameSeq[z]), 1) if NameSeq[z][x] == tempName]
		if len(indicesTE) > 0 :
			
			# Get the data from the sequence
			dataFrame_ChipSEQ = pathVisual + '/Downloaded/ChipSeq/' + nomFichier
			f = open(dataFrame_ChipSEQ, "r")
			lignes = f.readlines()
			f.close()
			
			# parcours seulement les sequences TE qui ont le meme chromosome
			limit5environ = 1
			for k in range(indicesTE[0], indicesTE[len(indicesTE)-1], 1) :
				
				for i in range(limit5environ, len(lignes), 1) :
					coupe = lignes[i].split(',')
					decoupeTissue = coupe[7].split('__')
					decoupeOrgan  = coupe[8].split('__')
					
					# Get the TFBS that genetic environment of TE sequences
					# Here the TFBS is before the 5' gene
					if int(coupe[2]) < int(DEB[z][k]) :
						limit5environ = i
				
					# Get the TFBS that overlaps Random sequences
					# Insertion
					if (int(DEB[z][k]) <= int(coupe[1]) and int(coupe[2]) <= int(FIN[z][k])) or (int(coupe[1]) <= int(DEB[z][k]) and int(FIN[z][k]) <= int(coupe[2])) : 
						memorizeDicoTFBS(decoupeTissue, decoupeOrgan, list_selection_TE, z, tissue_dictionary_RandomSeq, organ_dictionary_RandomSeq, tissue_dictionary_Global, organ_dictionary_Global)
					# Overlap 3'
					elif int(DEB[z][k]) <= int(coupe[1]) and int(coupe[1]) <= int(FIN[z][k]) and int(FIN[z][k]) - int(coupe[1]) >= 10 : 
						memorizeDicoTFBS(decoupeTissue, decoupeOrgan, list_selection_TE, z, tissue_dictionary_RandomSeq, organ_dictionary_RandomSeq, tissue_dictionary_Global, organ_dictionary_Global)
					# Overlap 5'
					elif int(DEB[z][k]) <= int(coupe[2]) and int(coupe[2]) <= int(FIN[z][k]) and int(coupe[2]) - int(DEB[z][k]) >= 10 : 
						memorizeDicoTFBS(decoupeTissue, decoupeOrgan, list_selection_TE, z, tissue_dictionary_RandomSeq, organ_dictionary_RandomSeq, tissue_dictionary_Global, organ_dictionary_Global)
						
					# TFBS are sorted so if the new TFBS is after the sequence, all other TFBS are also after it
					elif int(FIN[z][k]) < int(coupe[1]) :
						break
	
	
	
	
	
	
	
	
	
	

###############################################################################################################################################################
###	Extract all information about TFBS for random sequence
###############################################################################################################################################################
def ExtractTFBS_forRandom(pathVisual, pathVisualNEW, list_selection_TE, moduleCommonDATA, NameSeq, DEB, FIN, tissue_dictionary_Global, organ_dictionary_Global) :
	
	# Put again the good chromosome name
	NameID = moduleCommonDATA.dataFrame_Organism['NameID'].tolist()
	SimpleName = moduleCommonDATA.dataFrame_Organism['Name'].tolist()
	for i in range(0, len(list_selection_TE), 1) :
		for j in range(0, len(NameSeq[i]), 1) : 
			for z in range(0, len(NameID), 1) : 
				if NameSeq[i][j] == NameID[z] :
					NameSeq[i][j] = SimpleName[z]
					break
	
	
	tissue_dictionary_RandomSeq = {}
	organ_dictionary_RandomSeq = {}
	
	ChipSeqDirectory = pathVisual + '/Downloaded/ChipSeq/'
	for nomFichier in os.listdir(ChipSeqDirectory):
		if(os.path.isdir(nomFichier) != True):
				OverlapTFBSRandom(pathVisual, nomFichier, list_selection_TE, NameSeq, DEB, FIN, tissue_dictionary_RandomSeq, organ_dictionary_RandomSeq, tissue_dictionary_Global, organ_dictionary_Global)     
	
	return tissue_dictionary_RandomSeq, organ_dictionary_RandomSeq, tissue_dictionary_Global, organ_dictionary_Global
	
	
	
	
	
	
	
	
	
	
###############################################################################################################################################################
###	Calculates the TFBS that overlap TE and random sequences
###############################################################################################################################################################
def OverlapTFBS(pathVisual, nomFichier, list_selection_TE, pathSelectTE, NameSeq, DEB, FIN, listGeneSelect5, listGeneSelect3, tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_Global, organ_dictionary_Global) :
	
	# Get the filename in the same format that the chromosome name memorized
	tempName = nomFichier[:-4] 
	tempName = tempName.title()
	
	for z in range(0, len(list_selection_TE), 1) :		# famille de TE
		indicesTE = [x for x in range(0, len(NameSeq[z]), 1) if NameSeq[z][x] == tempName]
		if len(indicesTE) > 0 :
			
			# Get the data from the sequence
			dataFrame_ChipSEQ = pathVisual + '/Downloaded/ChipSeq/' + nomFichier
			f = open(dataFrame_ChipSEQ, "r")
			lignes = f.readlines()
			f.close()
			
			# parcours seulement les sequences TE qui ont le meme chromosome
			limit5environ = 1
			for k in range(indicesTE[0], indicesTE[len(indicesTE)-1], 1) :
				
				pathSelectTE2 = pathSelectTE + 'ChipSeq_for__' + str(list_selection_TE[z]) + '__occurrences_' + str(k) + '_.txt'
				fichier = open(pathSelectTE2, "a")
				
				for i in range(limit5environ, len(lignes), 1) :
					coupe = lignes[i].split(',')
					decoupeTissue = coupe[7].split('__')
					decoupeOrgan  = coupe[8].split('__')
					
					# Get the TFBS that genetic environment of TE sequences
					# Here the TFBS is before the 5' gene
					if int(coupe[2]) < int(listGeneSelect5[z][k][2]) :
						limit5environ = i
				
					# Insertion
					elif (int(listGeneSelect5[z][k][2]) <= int(coupe[1]) and int(coupe[2]) <= int(listGeneSelect3[z][k][3])) or (int(coupe[1]) <= int(listGeneSelect5[z][k][2]) and int(listGeneSelect3[z][k][3]) <= int(coupe[2])) : 
						fichier.write(lignes[i])
						# Get the TFBS that overlaps TE sequences
						# Insertion
						if (int(DEB[z][k]) <= int(coupe[1]) and int(coupe[2]) <= int(FIN[z][k])) or (int(coupe[1]) <= int(DEB[z][k]) and int(FIN[z][k]) <= int(coupe[2])) : 
							memorizeDicoTFBS(decoupeTissue, decoupeOrgan, list_selection_TE, z, tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_Global, organ_dictionary_Global)
						# Overlap 3'
						elif int(DEB[z][k]) <= int(coupe[1]) and int(coupe[1]) <= int(FIN[z][k]) and int(FIN[z][k]) - int(coupe[1]) >= 10 : 
							memorizeDicoTFBS(decoupeTissue, decoupeOrgan, list_selection_TE, z, tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_Global, organ_dictionary_Global)
						# Overlap 5'
						elif int(DEB[z][k]) <= int(coupe[2]) and int(coupe[2]) <= int(FIN[z][k]) and int(coupe[2]) - int(DEB[z][k]) >= 10 : 
							memorizeDicoTFBS(decoupeTissue, decoupeOrgan, list_selection_TE, z, tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_Global, organ_dictionary_Global)
						
					# Overlap 3'
					elif int(listGeneSelect5[z][k][2]) <= int(coupe[1]) and int(coupe[1]) <= int(listGeneSelect3[z][k][3]) and int(listGeneSelect3[z][k][3]) - int(coupe[1]) >= 10 : 
						fichier.write(lignes[i])
						# Get the TFBS that overlaps TE sequences
						# Insertion
						if (int(DEB[z][k]) <= int(coupe[1]) and int(coupe[2]) <= int(FIN[z][k])) or (int(coupe[1]) <= int(DEB[z][k]) and int(FIN[z][k]) <= int(coupe[2])) : 
							memorizeDicoTFBS(decoupeTissue, decoupeOrgan, list_selection_TE, z, tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_Global, organ_dictionary_Global)
						# Overlap 3'
						elif int(DEB[z][k]) <= int(coupe[1]) and int(coupe[1]) <= int(FIN[z][k]) and int(FIN[z][k]) - int(coupe[1]) >= 10 : 
							memorizeDicoTFBS(decoupeTissue, decoupeOrgan, list_selection_TE, z, tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_Global, organ_dictionary_Global)
						# Overlap 5'
						elif int(DEB[z][k]) <= int(coupe[2]) and int(coupe[2]) <= int(FIN[z][k]) and int(coupe[2]) - int(DEB[z][k]) >= 10 : 
							memorizeDicoTFBS(decoupeTissue, decoupeOrgan, list_selection_TE, z, tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_Global, organ_dictionary_Global)
					# Overlap 5'
					elif int(listGeneSelect5[z][k][2]) <= int(coupe[2]) and int(coupe[2]) <= int(listGeneSelect3[z][k][3]) and int(coupe[2]) - int(listGeneSelect5[z][k][2]) >= 10 :
						fichier.write(lignes[i])
						# Get the TFBS that overlaps TE sequences
						# Insertion
						if (int(DEB[z][k]) <= int(coupe[1]) and int(coupe[2]) <= int(FIN[z][k])) or (int(coupe[1]) <= int(DEB[z][k]) and int(FIN[z][k]) <= int(coupe[2])) : 
							memorizeDicoTFBS(decoupeTissue, decoupeOrgan, list_selection_TE, z, tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_Global, organ_dictionary_Global)
						# Overlap 3'
						elif int(DEB[z][k]) <= int(coupe[1]) and int(coupe[1]) <= int(FIN[z][k]) and int(FIN[z][k]) - int(coupe[1]) >= 10 : 
							memorizeDicoTFBS(decoupeTissue, decoupeOrgan, list_selection_TE, z, tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_Global, organ_dictionary_Global)
						# Overlap 5'
						elif int(DEB[z][k]) <= int(coupe[2]) and int(coupe[2]) <= int(FIN[z][k]) and int(coupe[2]) - int(DEB[z][k]) >= 10 : 
							memorizeDicoTFBS(decoupeTissue, decoupeOrgan, list_selection_TE, z, tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_Global, organ_dictionary_Global)
						
					# TFBS are sorted so if the new TFBS is after the sequence, all other TFBS are also after it
					elif int(listGeneSelect3[z][k][3]) < int(coupe[1]) :
						break
					
				fichier.close()
			
	
	
	
	
	
	
	
	
	
	
###############################################################################################################################################################
###	Extract all information about TFBS
###############################################################################################################################################################
def ExtractTFBS_forTE(pathVisual, pathVisualNEW, list_selection_TE, moduleCommonDATA, NameSeq,  DEB, FIN, listGeneSelect5, listGeneSelect3) :
	
	# Create the chipseq directory and all files for each TE inside
	pathSelectTE = pathVisualNEW + '/Downloaded/Selected_ChipSeq/'
	os.mkdir(pathSelectTE)
	# Create a TFBS file for each TE selected
	for z in range(0, len(list_selection_TE), 1) :		# famille de TE
		for k in range(0, len(NameSeq[z]), 1) :
			pathSelectTE2 = pathSelectTE + 'ChipSeq_for__' + str(list_selection_TE[z]) + '__occurrences_' + str(k) + '_.txt'
			f = open(pathSelectTE2, "w")
			f.write("Chr ID,Start,End,Orientation,Score,Gene,Type,Tissue,Organ,ChipSeq Name\n")
			f.close()
			
			
	# Put again the good chromosome name
	NameID = moduleCommonDATA.dataFrame_Organism['NameID'].tolist()
	SimpleName = moduleCommonDATA.dataFrame_Organism['Name'].tolist()
	for i in range(0, len(list_selection_TE), 1) :
		for j in range(0, len(NameSeq[i]), 1) : 
			for z in range(0, len(NameID), 1) : 
				if NameSeq[i][j] == NameID[z] :
					NameSeq[i][j] = SimpleName[z]
					break
	
	tissue_dictionary_SelectedTE = {}
	organ_dictionary_SelectedTE = {}
	tissue_dictionary_Global = {}
	organ_dictionary_Global = {}
	ChipSeqDirectory = pathVisual + '/Downloaded/ChipSeq/'
	for nomFichier in os.listdir(ChipSeqDirectory):
		if(os.path.isdir(nomFichier) != True):
				OverlapTFBS(pathVisual, nomFichier, list_selection_TE, pathSelectTE, NameSeq, DEB, FIN, listGeneSelect5, listGeneSelect3, tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_Global, organ_dictionary_Global)     
					
	return tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_Global, organ_dictionary_Global
