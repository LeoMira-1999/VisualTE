#!/usr/bin/python3
import os
import sys
import importlib
import importlib.util
import pandas as pd
import subprocess




###############################################################################################################################################################
###	Extract the relative position of TE inside gene
###############################################################################################################################################################
def SelectPositionInside(dataFrame_Exon, GeneSelectInside, DEB, FIN) :
	
	posRelativeInside = ''
	Select_Exon = dataFrame_Exon.loc[ (dataFrame_Exon['geneID'] == GeneSelectInside), : ]	#listGeneSelectInside[j][k][5]
	DEB_exon = Select_Exon['Start'].tolist()
	FIN_exon = Select_Exon['End'].tolist()			
	for x in range(0, len(DEB_exon), 1) :
		if (int(DEB_exon[x]) <= DEB and FIN <= int(FIN_exon[x])) or (int(DEB_exon[x]) <= DEB and int(DEB_exon[x]) < FIN) or (DEB < int(FIN_exon[x]) and int(FIN_exon[x]) <= FIN)  :
			posRelativeInside = 'E' + str(x)							# E for exon 
			break
		else :
			if x == 0 :
				if FIN < int(DEB_exon[x]) :
					posRelativeInside = 'U5'
					break
			if x == (len(DEB_exon)-1) :
				if DEB > int(DEB_exon[x]) : 
					posRelativeInside = 'U3'
					break
			if 0 < x and x <= (len(DEB_exon)-1) :
				if int(FIN_exon[x-1]) <= DEB and FIN <= int(DEB_exon[x]) :
					posRelativeInside = 'I' + str(x-1)				# I for intron 
					break
	
	return posRelativeInside











###############################################################################################################################################################
###	Extract dataframe Exons
###############################################################################################################################################################
def dataframe_for_Exons(pathVisual, pathVisualNEW, geneID, geneComplet, dataFrame_Exon) :
	
	ExonList = []
	indexExon = 0
	for i in range(0, len(geneID), 1) :
		if geneID[i] == 'VIDE' :
			ExonList.append([])
			ExonList[indexExon].append(geneComplet[i][0])
			ExonList[indexExon].append(geneComplet[i][1])
			ExonList[indexExon].append('VIDE')
			ExonList[indexExon].append('VIDE')
			ExonList[indexExon].append('VIDE')
			indexExon += 1
		else :
			#geneID[i] = str(geneID[i])
			Select_Exon = dataFrame_Exon.loc[ (dataFrame_Exon['geneID'] == geneID[i]), : ]
			DEB_exon = Select_Exon['Start'].tolist()
			FIN_exon = Select_Exon['End'].tolist()
			for z in range(0, len(DEB_exon), 1) :
				ExonList.append([])
				ExonList[indexExon].append(geneComplet[i][0])
				ExonList[indexExon].append(geneComplet[i][1])
				ExonList[indexExon].append(DEB_exon[z])
				ExonList[indexExon].append(FIN_exon[z])
				ExonList[indexExon].append(geneID[i])
				indexExon += 1
				
	ExonFile = pathVisualNEW + "/Downloaded/DATA_Selected_GeneExon.txt"
	dataFrame_Exon2 = pd.DataFrame(ExonList, columns=['TE family', 'TE Index', 'Exon Start', 'Exon End', 'Gene ID'] ) 
	dataFrame_Exon2.to_csv(ExonFile, index = False) # relative position










###############################################################################################################################################################
###	Create the dataframe for all Genes
###############################################################################################################################################################
def dataframe_for_Genes(pathVisualNEW, moduleSelectTE, list_selection_TE, TEDEB, listGeneSelect5, listGeneSelect3, listGeneSelectInside) :
	geneComplet = []
	geneID = []
	indexTE = 0
	for j in range(0, len(list_selection_TE), 1) :
		for k in range(0, len(TEDEB[j]), 1) :
			
			# Create the value for the 5' gene
			temp = []
			if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
				temp.append(moduleSelectTE.OfficialName)
			else : 
				temp.append(list_selection_TE[j])
			temp.append(indexTE)
			temp.append("5'")
			if listGeneSelect5[j][k][0] == 'VIDE' or listGeneSelect5[j][k][0] == 10000000000 :
				for z in range(0, 9, 1) :
					temp.append('VIDE')
				geneID.append('VIDE')
			else :
				for z in range(0, 9, 1) :
					temp.append(listGeneSelect5[j][k][z])
				geneID.append(listGeneSelect5[j][k][5])
			geneComplet.append(temp)
			
			
			# Create the value for the 3' gene
			temp = []
			if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
				temp.append(moduleSelectTE.OfficialName)
			else : 
				temp.append(list_selection_TE[j])
			temp.append(indexTE)
			temp.append("3'")
			if listGeneSelect3[j][k][0] == 'VIDE' or listGeneSelect3[j][k][0] == 10000000000 :
				for z in range(0, 9, 1) :
					temp.append('VIDE')
				geneID.append('VIDE')
			else :
				for z in range(0, 9, 1) :
					temp.append(listGeneSelect3[j][k][z])
				geneID.append(listGeneSelect3[j][k][5])
			geneComplet.append(temp)
			
			
			# Create the value for the inside gene
			temp = []
			if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
				temp.append(moduleSelectTE.OfficialName)
			else : 
				temp.append(list_selection_TE[j])
			temp.append(indexTE)
			temp.append("Inside")
			if listGeneSelectInside[j][k][0] == 'VIDE' or listGeneSelectInside[j][k][0] == 10000000000 :
				for z in range(0, 9, 1) :
					temp.append('VIDE')
				geneID.append('VIDE')
			else :
				for z in range(0, 9, 1) :
					temp.append(listGeneSelectInside[j][k][z])
				geneID.append(listGeneSelectInside[j][k][5])
			geneComplet.append(temp)
					
			indexTE += 1
			
	geneFile = pathVisualNEW + "/Downloaded/DATA_Selected_Genes.txt"
	dataFrame_Gene = pd.DataFrame(geneComplet, columns=['TE family', 'TE Index', 'TE-Gene Position', 'Gene Distance', 'Gene Name', 'Gene Start', 'Gene End', 'Gene Sens', 'Gene ID', 'Gene Function', 'Gene Chrom', 'Position Inside'] ) 
	dataFrame_Gene.to_csv(geneFile, index = False) # relative position

	return geneID, geneComplet











###############################################################################################################################################################
###	Create the dataframe for all Genes
###############################################################################################################################################################
def dataframe_for_ClosestGenes(pathVisualNEW, moduleSelectTE, list_selection_TE, TEDEB, listGeneSelect5, listGeneSelect3, listGeneSelectInside) :
	geneComplet = []
	indexTE = 0
	for j in range(0, len(list_selection_TE), 1) :
		for k in range(0, len(TEDEB[j]), 1) :
			
			# Create the value for the 5' gene
			temp = []
			if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
				temp.append(moduleSelectTE.OfficialName)
			else : 
				temp.append(list_selection_TE[j])
			temp.append(indexTE)
			if listGeneSelectInside[j][k][1] != 'VIDE' :
				temp.append("Inside")
				for z in range(0, 9, 1) :
					temp.append(listGeneSelectInside[j][k][z])
			elif listGeneSelect5[j][k][0] < listGeneSelect3[j][k][0] :
				temp.append("5'")
				for z in range(0, 9, 1) :
					temp.append(listGeneSelect5[j][k][z])
			else :
				temp.append("3'")
				for z in range(0, 9, 1) :
					temp.append(listGeneSelect3[j][k][z])
			geneComplet.append(temp)
					
			indexTE += 1
			
	geneFile = pathVisualNEW + "/Downloaded/DATA_Selected_ClosestGenes.txt"
	dataFrame_Gene = pd.DataFrame(geneComplet, columns=['TE family', 'TE Index', 'TE-Gene Position', 'Gene Distance', 'Gene Name', 'Gene Start', 'Gene End', 'Gene Sens', 'Gene ID', 'Gene Function', 'Gene Chrom', 'Position Inside'] ) 
	dataFrame_Gene.to_csv(geneFile, index = False) # relative position











###############################################################################################################################################################
###	Extract the Gene arround the TE occurrences
###############################################################################################################################################################
def SelectGenes(pathVisual, TESeq, TEDEB, TEFIN, TESens, moduleCommonDATA, pathVisualNEW, list_selection_TE, moduleSelectTE) :
	
	NameID = moduleCommonDATA.dataFrame_Organism['NameID'].tolist()
	SimpleName = moduleCommonDATA.dataFrame_Organism['Name'].tolist()
	tempFile = pathVisual + '/Downloaded/DATA_Gene.txt'
	dataFrame_Gene = pd.read_csv(tempFile)
	tempFile = pathVisual + '/Downloaded/DATA_GeneExon.txt'
	dataFrame_Exon = pd.read_csv(tempFile)
	
	
	
	# Create the data structure that contains the closest gene in 5' 3' and inside
	listGeneSelect5 = []
	listGeneSelect3 = []
	listGeneSelectInside = []
	for i in range(0, len(TEDEB), 1) :
		listGeneSelect5.append( [] )
		listGeneSelect3.append( [] )
		listGeneSelectInside.append([])
		for j in range(0, len(TEDEB[i]), 1) :
			listGeneSelect5[i].append( [] )
			listGeneSelect3[i].append( [] )
			listGeneSelectInside[i].append( [] )
			listGeneSelect5[i][j].append(10000000000)		# Distance par defaut
			listGeneSelect3[i][j].append(10000000000)
			listGeneSelectInside[i][j].append(10000000000)
			for k in range(1, 9, 1) :
				listGeneSelect5[i][j].append('VIDE')		# Valeur des genes par defaut
				listGeneSelect3[i][j].append('VIDE')
				listGeneSelectInside[i][j].append('VIDE')
	
	
	
	for z in range(0, len(TESeq), 1) :
		for i in range(0, len(TESeq[z]), 1) :
			for a in range(0, len(NameID), 1) :
				if TESeq[z][i] == SimpleName[a] :
					TESeq[z][i] = NameID[a]
					break
					
					
			########################################################################################################################
			# Gene in 5'
			Select_Gene5 = dataFrame_Gene.loc[ (dataFrame_Gene['Chr ID'] == TESeq[z][i]) & (dataFrame_Gene['End'] < TEDEB[z][i]) , : ].sort_values(by='End')
			if len(Select_Gene5.index) > 0 :
				DernierGene5 = Select_Gene5.iloc[[-1]]
				CHR_gene = DernierGene5['Chr ID'].tolist()
				DEB_gene = DernierGene5['Start'].tolist()
				FIN_gene = DernierGene5['End'].tolist()
				Sens_gene = DernierGene5['Sens'].tolist()
				Name_gene = DernierGene5['Gene Name'].tolist()
				ID_gene = DernierGene5['ID'].tolist()
				Function_gene = DernierGene5['Function'].tolist()
				
				if len(CHR_gene) > 0 :
					distanceGene = TEDEB[z][i] - DEB_gene[0]		# Prendre le TSS
					listGeneSelect5[z][i][0] = distanceGene
					listGeneSelect5[z][i][1] = Name_gene[0]
					listGeneSelect5[z][i][2] = DEB_gene[0]
					listGeneSelect5[z][i][3] = FIN_gene[0]
					listGeneSelect5[z][i][4] = Sens_gene[0]
					listGeneSelect5[z][i][5] = ID_gene[0]
					listGeneSelect5[z][i][6] = Function_gene[0]
					listGeneSelect5[z][i][7] = CHR_gene[0]
			
			
			########################################################################################################################
			# Gene inside
			Select_GeneInside = dataFrame_Gene.loc[ (dataFrame_Gene['Chr ID'] == TESeq[z][i]) & ( ((dataFrame_Gene['Start'] >= TEDEB[z][i]) & (dataFrame_Gene['End'] <= TEFIN[z][i])) | ((dataFrame_Gene['Start'] <= TEDEB[z][i]) & (dataFrame_Gene['End'] >= TEFIN[z][i])) ), : ]
			if len(Select_GeneInside.index) > 0 :
				CHR_gene = Select_GeneInside['Chr ID'].tolist()
				DEB_gene = Select_GeneInside['Start'].tolist()
				FIN_gene = Select_GeneInside['End'].tolist()
				Sens_gene = Select_GeneInside['Sens'].tolist()
				Name_gene = Select_GeneInside['Gene Name'].tolist()
				ID_gene = Select_GeneInside['ID'].tolist()
				Function_gene = Select_GeneInside['Function'].tolist()
				
				if len(CHR_gene) > 0 :
					distanceGene = -1		# Prendre le TSS
					listGeneSelectInside[z][i][0] = distanceGene
					listGeneSelectInside[z][i][1] = Name_gene[0]
					listGeneSelectInside[z][i][2] = DEB_gene[0]
					listGeneSelectInside[z][i][3] = FIN_gene[0]
					listGeneSelectInside[z][i][4] = Sens_gene[0]
					listGeneSelectInside[z][i][5] = ID_gene[0]
					listGeneSelectInside[z][i][6] = Function_gene[0]
					listGeneSelectInside[z][i][7] = CHR_gene[0]
					
					positionInside = SelectPositionInside(dataFrame_Exon, ID_gene[0], TEDEB[z][i], TEFIN[z][i])
					listGeneSelectInside[z][i][8] = positionInside
				
				
			########################################################################################################################
			# Gene in 3'
			Select_Gene3 = dataFrame_Gene.loc[ (dataFrame_Gene['Chr ID'] == TESeq[z][i]) & (dataFrame_Gene['Start'] > TEFIN[z][i]) , : ].sort_values(by='End')
			if len(Select_Gene3.index) > 0 :
				DernierGene3 = Select_Gene3.iloc[[0]]
				CHR_gene = DernierGene3['Chr ID'].tolist()
				DEB_gene = DernierGene3['Start'].tolist()
				FIN_gene = DernierGene3['End'].tolist()
				Sens_gene = DernierGene3['Sens'].tolist()
				Name_gene = DernierGene3['Gene Name'].tolist()
				ID_gene = DernierGene3['ID'].tolist()
				Function_gene = DernierGene3['Function'].tolist()
				
				if len(CHR_gene) > 0 :
					distanceGene = DEB_gene[0] - TEDEB[z][i]		# Prendre le TSS
					listGeneSelect3[z][i][0] = distanceGene
					listGeneSelect3[z][i][1] = Name_gene[0]
					listGeneSelect3[z][i][2] = DEB_gene[0]
					listGeneSelect3[z][i][3] = FIN_gene[0]
					listGeneSelect3[z][i][4] = Sens_gene[0]
					listGeneSelect3[z][i][5] = ID_gene[0]
					listGeneSelect3[z][i][6] = Function_gene[0]
					listGeneSelect3[z][i][7] = CHR_gene[0]
		
		
		
	########################################################################################################################
	# Extrait et ecrit les dataframe
	geneID, geneComplet = dataframe_for_Genes(pathVisualNEW, moduleSelectTE, list_selection_TE, TEDEB, listGeneSelect5, listGeneSelect3, listGeneSelectInside)
	dataframe_for_ClosestGenes(pathVisualNEW, moduleSelectTE, list_selection_TE, TEDEB, listGeneSelect5, listGeneSelect3, listGeneSelectInside)
	
	dataframe_for_Exons(pathVisual, pathVisualNEW, geneID, geneComplet, dataFrame_Exon)
	
	
	return listGeneSelect5, listGeneSelect3, listGeneSelectInside
	
	
	
	
	
	
	
	
	
	
	
###############################################################################################################################################################
###	Extract the information about other TE
###############################################################################################################################################################
def SelectOtherTE(pathVisual, pathVisualNEW, listGeneSelect5, listGeneSelect3, list_selection_TE, TEDEB, TEFIN, moduleSelectTE) :
	
	tempFile = pathVisual + '/Downloaded/DATA_AllTEs.txt'
	dataFrame_OtherTE = pd.read_csv(tempFile)
	indexTE = 0
	dataForOtherTE = []
	for j in range(0, len(list_selection_TE), 1) :
		for k in range(0, len(TEDEB[j]), 1) :
			limit5 = listGeneSelect5[j][k][2]
			limit3 = listGeneSelect3[j][k][3]
			if limit5 == 'VIDE' :
				limit5 = TEDEB[j][k] - 100000
			if limit3 == 'VIDE' :
				limit3 = TEFIN[j][k] + 100000
				
			# recupere d'abord tout les TEs entre 2 gene
			Select_OtherTE = dataFrame_OtherTE.loc[ ( (~dataFrame_OtherTE['TE Family'].isin(list_selection_TE)) & (dataFrame_OtherTE['Chr ID'] == listGeneSelect3[j][k][7]) & (dataFrame_OtherTE['Start'] > int(limit5)) & (dataFrame_OtherTE['End'] < int(limit3)) ), : ]
			OtherTE_CHR = Select_OtherTE['Chr ID'].tolist()
			OtherTE_DEB = Select_OtherTE['Start'].tolist()
			OtherTE_FIN = Select_OtherTE['End'].tolist()
			OtherTE_Sens = Select_OtherTE['Sens'].tolist()
			OtherTE_Family = Select_OtherTE['TE Family'].tolist()
			OtherTE_Super = Select_OtherTE['TE group'].tolist()
			
			if len(OtherTE_CHR) > 0 :
				for i in range(0, len(OtherTE_CHR), 1) :
					# Create the value for the inside gene
					temp = []
					if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
						temp.append(moduleSelectTE.OfficialName)
					else : 
						temp.append(list_selection_TE[j])
					temp.append(indexTE)
					temp.append(OtherTE_CHR[i])
					temp.append(OtherTE_DEB[i])
					temp.append(OtherTE_FIN[i])
					temp.append(OtherTE_Sens[i])
					temp.append(OtherTE_Family[i])
					temp.append(OtherTE_Super[i])
					dataForOtherTE.append(temp)
			else :
				# Create the value for the inside gene
				temp = []
				if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
					temp.append(moduleSelectTE.OfficialName)
				else : 
					temp.append(list_selection_TE[j])
				temp.append(indexTE)
				temp.append('VIDE')
				temp.append('VIDE')
				temp.append('VIDE')
				temp.append('VIDE')
				temp.append('VIDE')
				temp.append('VIDE')
				dataForOtherTE.append(temp)
			
			indexTE += 1
		
	OtherTEFile = pathVisualNEW + "/Downloaded/DATA_Selected_OtherTE.txt"
	dataFrame_OtherTE = pd.DataFrame(dataForOtherTE, columns=['TE family', 'TE Index', 'Chr ID', 'Start', 'End', 'Sens', 'TE Family', 'TE group'] ) 
	dataFrame_OtherTE.to_csv(OtherTEFile, index = False) # relative position
	
	
	
	
	
	
	
	
	
	
###############################################################################################################################################################
###	Extract the information about pseudogene
###############################################################################################################################################################
def SelectPseudo(pathVisual, pathVisualNEW, listGeneSelect5, listGeneSelect3, list_selection_TE, TEDEB, TEFIN, moduleSelectTE) :
	
	tempFile = pathVisual + '/Downloaded/DATA_Pseudo.txt'
	dataFrame_Pseudo = pd.read_csv(tempFile)
	indexTE = 0
	dataForPseudo = []
	for j in range(0, len(list_selection_TE), 1) :
		for k in range(0, len(TEDEB[j]), 1) :
			limit5 = listGeneSelect5[j][k][2]
			limit3 = listGeneSelect3[j][k][3]
			if limit5 == 'VIDE' :
				limit5 = TEDEB[j][k] - 100000
			if limit3 == 'VIDE' :
				limit3 = TEFIN[j][k] + 100000
			
			# recupere d'abord tout les TEs entre 2 gene
			Select_Pseudo = dataFrame_Pseudo.loc[ ( (dataFrame_Pseudo['Chr ID'] == listGeneSelect3[j][k][7]) & (dataFrame_Pseudo['Start'] > int(limit5)) & (dataFrame_Pseudo['End'] < int(limit3)) ), : ]
			Pseudo_CHR = Select_Pseudo['Chr ID'].tolist()
			Pseudo_DEB = Select_Pseudo['Start'].tolist()
			Pseudo_FIN = Select_Pseudo['End'].tolist()
			Pseudo_Sens = Select_Pseudo['Sens'].tolist()
			Pseudo_ID = Select_Pseudo['ID'].tolist()
			Pseudo_Name = Select_Pseudo['Pseudo Name'].tolist()
			
			if len(Pseudo_CHR) > 0 :
				for i in range(0, len(Pseudo_CHR), 1) :
					# Create the value for the inside gene
					temp = []
					if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
						temp.append(moduleSelectTE.OfficialName)
					else : 
						temp.append(list_selection_TE[j])
					temp.append(indexTE)
					temp.append(Pseudo_CHR[i])
					temp.append(Pseudo_DEB[i])
					temp.append(Pseudo_FIN[i])
					temp.append(Pseudo_Sens[i])
					temp.append(Pseudo_ID[i])
					temp.append(Pseudo_Name[i])
					dataForPseudo.append(temp)
			else :
				# Create the value for the inside gene
				temp = []
				if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
					temp.append(moduleSelectTE.OfficialName)
				else : 
					temp.append(list_selection_TE[j])
				temp.append(indexTE)
				temp.append('VIDE')
				temp.append('VIDE')
				temp.append('VIDE')
				temp.append('VIDE')
				temp.append('VIDE')
				temp.append('VIDE')
				dataForPseudo.append(temp)
			
			indexTE += 1
		
	
	PseudoFile = pathVisualNEW + "/Downloaded/DATA_Selected_Pseudo.txt"
	dataFrame_Pseudo = pd.DataFrame(dataForPseudo, columns=['TE family', 'TE Index', 'Chr ID', 'Start', 'End', 'Sens', 'ID', 'Pseudo Name'] ) 
	dataFrame_Pseudo.to_csv(PseudoFile, index = False) # relative position
	
	
	
	
	
	
	
	
	
	
###############################################################################################################################################################
###	Extract the information about ncRNA
###############################################################################################################################################################
def SelectNCRna(pathVisual, pathVisualNEW, listGeneSelect5, listGeneSelect3, list_selection_TE, TEDEB, TEFIN, moduleSelectTE) :
	
	tempFile = pathVisual + '/Downloaded/DATA_ncRNA.txt'
	dataFrame_ncRNA = pd.read_csv(tempFile)
	indexTE = 0
	dataFor_ncRNA = []
	for j in range(0, len(list_selection_TE), 1) :
		for k in range(0, len(TEDEB[j]), 1) :
			limit5 = listGeneSelect5[j][k][2]
			limit3 = listGeneSelect3[j][k][3]
			if limit5 == 'VIDE' :
				limit5 = TEDEB[j][k] - 100000
			if limit3 == 'VIDE' :
				limit3 = TEFIN[j][k] + 100000
				
			# recupere d'abord tout les TEs entre 2 gene
			Select_ncRNA = dataFrame_ncRNA.loc[ ( (dataFrame_ncRNA['Chr ID'] == listGeneSelect3[j][k][7]) & (dataFrame_ncRNA['Start'] > int(limit5)) & (dataFrame_ncRNA['End'] < int(limit3)) ), : ]
			ncRNA_CHR = Select_ncRNA['Chr ID'].tolist()
			ncRNA_DEB = Select_ncRNA['Start'].tolist()
			ncRNA_FIN = Select_ncRNA['End'].tolist()
			ncRNA_Sens = Select_ncRNA['Sens'].tolist()
			ncRNA_Type = Select_ncRNA['Type'].tolist()
			ncRNA_ID = Select_ncRNA['ID'].tolist()
			
			if len(ncRNA_CHR) > 0 :
				for i in range(0, len(ncRNA_CHR), 1) :
					# Create the value for the inside gene
					temp = []
					if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
						temp.append(moduleSelectTE.OfficialName)
					else : 
						temp.append(list_selection_TE[j])
					temp.append(indexTE)
					temp.append(ncRNA_CHR[i])
					temp.append(ncRNA_DEB[i])
					temp.append(ncRNA_FIN[i])
					temp.append(ncRNA_Sens[i])
					temp.append(ncRNA_Type[i])
					temp.append(ncRNA_ID[i])
					dataFor_ncRNA.append(temp)
			else :
				# Create the value for the inside gene
				temp = []
				if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
					temp.append(moduleSelectTE.OfficialName)
				else : 
					temp.append(list_selection_TE[j])
				temp.append(indexTE)
				temp.append('VIDE')
				temp.append('VIDE')
				temp.append('VIDE')
				temp.append('VIDE')
				temp.append('VIDE')
				dataFor_ncRNA.append(temp)
			
			indexTE += 1
		
	
	ncRNAFile = pathVisualNEW + "/Downloaded/DATA_Selected_ncRNA.txt"
	dataFrame_ncRNA = pd.DataFrame(dataFor_ncRNA, columns=['TE family', 'TE Index', 'Chr ID', 'Start', 'End', 'Sens', 'Type', 'ID'] ) 
	dataFrame_ncRNA.to_csv(ncRNAFile, index = False) # relative position
	
	
	
	
	
	
	
	
	
	
###############################################################################################################################################################
###	Extract the sequences and the annotation arround the TE occurrences
###############################################################################################################################################################
def SelectAnnotations(pathVisual, pathVisualNEW, moduleSelectTE, moduleCommonDATA, list_selection_TE, ListeConsensus) :
	
	# Get the TE information about the selected TE
	Select_myTE = []
	Seq = []
	NameSeq = []
	DEB = []
	FIN = []
	Sens = []
	Size = []
	Similarity = []
	for j in range(0, len(list_selection_TE), 1) :
		Select_myTE = moduleSelectTE.dataFrame_MyTE.loc[ (moduleSelectTE.dataFrame_MyTE['TE Family'] == list_selection_TE[j]), : ]
		Seq.append(Select_myTE['Chr ID'].tolist())
		NameSeq.append(Select_myTE['Chr Name'].tolist())
		DEB.append(Select_myTE['Start'].tolist())
		FIN.append(Select_myTE['End'].tolist())
		Sens.append(Select_myTE['Sens'].tolist())
		Size.append(Select_myTE['Size'].tolist())
		Similarity.append(Select_myTE['Similarity'].tolist())
	
	
	
	# Extract the gene annotation arround the TE occurrences
	listGeneSelect5, listGeneSelect3, listGeneSelectInside = SelectGenes(pathVisual, Seq, DEB, FIN, Sens, moduleCommonDATA, pathVisualNEW, list_selection_TE, moduleSelectTE)
	
	# Extract the other TE present between the 2 DATA_Selected_Genes
	SelectOtherTE(pathVisual, pathVisualNEW, listGeneSelect5, listGeneSelect3, list_selection_TE, DEB, FIN, moduleSelectTE)
	
	# Extract the pseudogene present between the 2 DATA_Selected_Genes
	SelectPseudo(pathVisual, pathVisualNEW, listGeneSelect5, listGeneSelect3, list_selection_TE, DEB, FIN, moduleSelectTE)
	
	# Extract the ncRNA present between the 2 DATA_Selected_Genes
	SelectNCRna(pathVisual, pathVisualNEW, listGeneSelect5, listGeneSelect3, list_selection_TE, DEB, FIN, moduleSelectTE)
	
	return Seq, DEB, FIN, Sens, Size, Similarity, listGeneSelect5, listGeneSelect3, listGeneSelectInside
	
