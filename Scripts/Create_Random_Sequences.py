#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd 
import random



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
###	Extract the relative position of TE inside gene
###############################################################################################################################################################
def SelectPositionInsideRandom(dataFrame_Exon, GeneSelectInside, DEB, FIN) :
	
	posRelativeInside = ''
	Select_Exon = dataFrame_Exon.loc[ (dataFrame_Exon['geneID'] == GeneSelectInside), : ]	#listGeneSelectInside[j][k][5]
	DEB_exon = Select_Exon['Start'].tolist()
	FIN_exon = Select_Exon['End'].tolist()			
	for x in range(0, len(DEB_exon), 1) :
		if (int(DEB_exon[x]) <= DEB and FIN <= int(FIN_exon[x])) or (int(DEB_exon[x]) <= DEB and int(DEB_exon[x]) < FIN) or (DEB < int(FIN_exon[x]) and int(FIN_exon[x]) <= FIN)  :
			posRelativeInside = 'E' + str(x)						# E for exon 
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
###	Extract random sequences for TFBS
###############################################################################################################################################################
def randomSequenceForTFBS(pathVisual, pathVisualNEW, moduleSelectTE, list_selection_TE, NameSeq, TEFIN, TEDEB) :
	
	tempFile = pathVisual + '/Downloaded/DATA_GeneExon.txt'
	dataFrame_Exon = pd.read_csv(tempFile)
	tempFile = pathVisual + '/Downloaded/DATA_Gene.txt'
	dataFrame_Gene = pd.read_csv(tempFile)
	tempFile = pathVisual + '/Downloaded/DATA_Organism.txt'
	dataFrame_Organism = pd.read_csv(tempFile)
	CHR_Size = dataFrame_Organism['Size bp'].tolist()
	CHR_Name = dataFrame_Organism['NameID'].tolist()
	
	randomSeqDEB = []
	randomSeqFIN = []
	randomSeqCHR = []
	randomGene = []
	randomGeneID = []
	randomDist = []
	randomFunction = []
	randomPosI = []
	for j in range(0, len(list_selection_TE), 1) :
		randomSeqDEB.append([])
		randomSeqFIN.append([])
		randomSeqCHR.append([])
		randomGene.append([])
		randomDist.append([])
		randomGeneID.append([])
		randomFunction.append([])
		randomPosI.append([])
		for k in range(0, len(NameSeq[j]), 1) :
			randomSeqDEB[j].append(0)
			randomSeqFIN[j].append(0)
			randomSeqCHR[j].append(NameSeq[j][k])
			randomGene[j].append('VIDE')
			randomDist[j].append(0)
			randomGeneID[j].append('VIDE')
			randomFunction[j].append('VIDE')
			randomPosI[j].append('VIDE')
	
	DEB_gene3 = ''
	FIN_gene3 = ''
	Name_gene3 = ''
	ID_gene3 = ''
	Function3 = ''
	DEB_gene5 = ''
	FIN_gene5 = ''
	Name_gene5 = ''
	ID_gene5 = ''
	Function5 = ''
	for j in range(0, len(list_selection_TE), 1) :
		for k in range(0, len(NameSeq[j]), 1) :
			tailleTE = (TEFIN[j][k] - TEDEB[j][k])
			dist5 = 10000000000
			dist3 = 10000000000
			for z in range(0, len(CHR_Name), 1) :
				if NameSeq[j][k] == CHR_Name[z] :
					posAleatoire = random.randint(0, (CHR_Size[z]-tailleTE))
					randomSeqDEB[j][k] = posAleatoire
					randomSeqFIN[j][k] = posAleatoire + tailleTE
					break
					
			# regarde le gene le plus proche en 5'
			Select_Gene5 = dataFrame_Gene.loc[ (dataFrame_Gene['Chr ID'] == NameSeq[j][k]) & (dataFrame_Gene['Start'] < randomSeqDEB[j][k]) , : ].sort_values(by='End')
			if Select_Gene5.empty :
				dist5 = 10000000000
			else :
				DernierGene5 = Select_Gene5.iloc[[-1]]
				DEB_gene5 = DernierGene5['Start'].tolist()
				FIN_gene5 = DernierGene5['Start'].tolist()
				Name_gene5 = DernierGene5['Gene Name'].tolist()
				ID_gene5 = DernierGene5['ID'].tolist()
				Function5 = DernierGene5['Function'].tolist()
				dist5 = abs(randomSeqDEB[j][k] - DEB_gene5[0])
			# regarde le gene le plus proche en 3'
			Select_Gene3 = dataFrame_Gene.loc[ (dataFrame_Gene['Chr ID'] == NameSeq[j][k]) & (dataFrame_Gene['End'] > randomSeqFIN[j][k]) , : ].sort_values(by='End')
			if Select_Gene3.empty :
				dist3 = 10000000000
			else :
				DernierGene3 = Select_Gene3.iloc[[0]]
				DEB_gene3 = DernierGene3['Start'].tolist()
				FIN_gene3 = DernierGene3['Start'].tolist()
				Name_gene3 = DernierGene3['Gene Name'].tolist()
				ID_gene3 = DernierGene3['ID'].tolist()
				Function3 = DernierGene5['Function'].tolist()
				dist3 = abs(DEB_gene3[0] - randomSeqDEB[j][k])
			
			if dist5 >= dist3 :
				randomGene[j][k]   = Name_gene5[0]
				randomGeneID[j][k] = ID_gene5[0]
				randomFunction[j][k] = Function5[0]
				
				if int(FIN_gene5[0]) <= randomSeqDEB[j][k] :
					randomDist[j][k]   = dist5
				else : 
					randomDist[j][k]   = -1
					randomPosI[j][k] = SelectPositionInside(dataFrame_Exon, ID_gene3[0], randomSeqDEB[j][k], randomSeqFIN[j][k])
			else :
				randomGene[j][k]   = Name_gene3[0]
				randomGeneID[j][k] = ID_gene3[0]
				randomFunction[j][k] = Function3[0]
				
				if int(DEB_gene5[0]) >= randomSeqFIN[j][k] :
					randomDist[j][k]   = dist3
				else : 
					randomDist[j][k]   = -1
					randomPosI[j][k] = SelectPositionInside(dataFrame_Exon, ID_gene3[0], randomSeqDEB[j][k], randomSeqFIN[j][k])
			
			
	
	
	randomList = []
	index = 0
	for j in range(0, len(list_selection_TE), 1) :
		for k in range(0, len(NameSeq[j]), 1) :
			temp = []
			if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
				temp.append(moduleSelectTE.OfficialName)
			else : 
				temp.append(list_selection_TE[j])
			temp.append(index)
			temp.append(randomSeqCHR[j][k])
			temp.append(randomSeqDEB[j][k])
			temp.append(randomSeqFIN[j][k])
			temp.append(randomGene[j][k])
			temp.append(randomDist[j][k])
			temp.append(randomGeneID[j][k])
			temp.append(randomFunction[j][k])
			temp.append(randomPosI[j][k])
			randomList.append(temp)
			index += 1
	
	# Now write the random coordinates for later uses
	randomFile = pathVisualNEW + "/Downloaded/DATA_RandomSequences.txt"
	dataFrame_Random = pd.DataFrame(randomList, columns=['TE family', 'TE Index', 'Chr ID', 'Start', 'End', 'Gene Name', 'Gene Distance', 'Gene ID', 'Gene Function', 'Position Inside'] ) 
	dataFrame_Random = dataFrame_Random.sort_values(by=['Chr ID', 'Start'])
	dataFrame_Random.to_csv(randomFile, index = False) # relative position

	return randomSeqCHR, randomSeqDEB, randomSeqFIN









###############################################################################################################################################################
###	Extract the relative position of TE inside gene
###############################################################################################################################################################
def RandomSameDistance(pathVisual, pathVisualNEW, moduleSelectTE, NameSeq, TEDEB, TEFIN, list_selection_TE, listGeneSelect5, listGeneSelect3, listGeneSelectInside) :
	
	tempFile = pathVisual + '/Downloaded/DATA_Gene.txt'
	dataFrame_Gene = pd.read_csv(tempFile)
	tempFile = pathVisual + '/Downloaded/DATA_GeneExon.txt'
	dataFrame_Exon = pd.read_csv(tempFile)
	
	
	
	randomGene = []
	for j in range(0, len(list_selection_TE), 1) :
		randomGene.append([])
		for k in range(0, len(NameSeq[j]), 1) :
			randomGene[j].append([])		# Distance par defaut
			randomGene[j][k].append(10000000000)		# Distance par defaut
			for z in range(1, 9, 1) :
				randomGene[j][k].append('VIDE')		# Valeur des genes par defaut
	
	
	
	# Enleve de la dataframe les genes deja pris par les TE (5', 3' and inside
	for j in range(0, len(list_selection_TE), 1) :
		for k in range(0, len(NameSeq[j]), 1) :
			dataFrame_Gene.drop(dataFrame_Gene.loc[ (dataFrame_Gene['Chr ID'] == listGeneSelect5[j][k][7]) & (dataFrame_Gene['Start'] == listGeneSelect5[j][k][2]) & (dataFrame_Gene['End'] == listGeneSelect5[j][k][3]) ].index, inplace=True)
			dataFrame_Gene.drop(dataFrame_Gene.loc[ (dataFrame_Gene['Chr ID'] == listGeneSelect3[j][k][7]) & (dataFrame_Gene['Start'] == listGeneSelect3[j][k][2]) & (dataFrame_Gene['End'] == listGeneSelect3[j][k][3]) ].index, inplace=True)
			if listGeneSelectInside[j][k][1] != 'VIDE' :
				dataFrame_Gene.drop(dataFrame_Gene.loc[ (dataFrame_Gene['Chr ID'] == listGeneSelectInside[j][k][7]) & (dataFrame_Gene['Start'] == listGeneSelectInside[j][k][2]) & (dataFrame_Gene['End'] == listGeneSelectInside[j][k][3]) ].index, inplace=True)
	
	indexGene = -1
	previousCHR = ""
	Selection_In_Chrom = ""
	CHR_gene = ""
	DEB_gene = ""
	FIN_gene = ""
	Sens_gene = ""
	Name_gene = ""
	ID_gene = ""
	Function_gene = ""
	for j in range(0, len(list_selection_TE), 1) :
		for k in range(0, len(NameSeq[j]), 1) :
			if previousCHR != listGeneSelect5[j][k][7] :
				previousCHR = listGeneSelect5[j][k][7]
				Selection_In_Chrom = dataFrame_Gene.loc[ (dataFrame_Gene['Chr ID'] == listGeneSelect5[j][k][7]) , : ]
				CHR_gene = Selection_In_Chrom['Chr ID'].tolist()
				DEB_gene = Selection_In_Chrom['Start'].tolist()
				FIN_gene = Selection_In_Chrom['End'].tolist()
				Sens_gene = Selection_In_Chrom['Sens'].tolist()
				Name_gene = Selection_In_Chrom['Gene Name'].tolist()
				ID_gene = Selection_In_Chrom['ID'].tolist()
				Function_gene = Selection_In_Chrom['Function'].tolist()
				
			positionInside = 'VIDE'
				
			if listGeneSelectInside[j][k][1] != 'VIDE' :
				# prendre un element au hasard et mettre la sequence random dedans !
				indexGene = random.randint(0, len(CHR_gene)-1)
				positionSeqRandom = random.randint(DEB_gene[indexGene], FIN_gene[indexGene])
				positionInside = SelectPositionInsideRandom(dataFrame_Exon, ID_gene[indexGene], positionSeqRandom, positionSeqRandom)
	
				distanceGene = -1		# Prendre le TSS
				randomGene[j][k][0] = distanceGene
				randomGene[j][k][1] = Name_gene[indexGene]
				randomGene[j][k][2] = DEB_gene[indexGene]
				randomGene[j][k][3] = FIN_gene[indexGene]
				randomGene[j][k][4] = Sens_gene[indexGene]
				randomGene[j][k][5] = ID_gene[indexGene]
				randomGene[j][k][6] = Function_gene[indexGene]
				randomGene[j][k][7] = CHR_gene[indexGene]
				randomGene[j][k][8] = positionInside
				
			else :
				indexGene = random.randint(0, (len(CHR_gene)-1))
				distanceGene = -1
				if listGeneSelect5[j][k][0] < listGeneSelect3[j][k][0] :
					positionSeqRandom = DEB_gene[indexGene] + listGeneSelect5[j][k][0]
					distanceGene = listGeneSelect5[j][k][0]
				else :
					positionSeqRandom = DEB_gene[indexGene] - listGeneSelect3[j][k][0]
					distanceGene = listGeneSelect3[j][k][0]
					
				randomGene[j][k][0] = distanceGene
				randomGene[j][k][1] = Name_gene[indexGene]
				randomGene[j][k][2] = DEB_gene[indexGene]
				randomGene[j][k][3] = FIN_gene[indexGene]
				randomGene[j][k][4] = Sens_gene[indexGene]
				randomGene[j][k][5] = ID_gene[indexGene]
				randomGene[j][k][6] = Function_gene[indexGene]
				randomGene[j][k][7] = CHR_gene[indexGene]
				randomGene[j][k][8] = positionInside
				
			# Enleve le gene choisi de la liste
			del Name_gene[indexGene]
			del DEB_gene[indexGene]
			del FIN_gene[indexGene]
			del Sens_gene[indexGene]
			del ID_gene[indexGene]
			del Function_gene[indexGene]
			del CHR_gene[indexGene]
	
	
	##########################################################################################################
	# Cree le dataframe des genes aleatoires
	aleatoire = []
	index = 0
	for j in range(0, len(list_selection_TE), 1) :
		for k in range(0, len(NameSeq[j]), 1) :
			temp = []
			if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
				temp.append(moduleSelectTE.OfficialName)
			else : 
				temp.append(list_selection_TE[j])
			temp.append(index)
			if listGeneSelectInside[j][k][1] != 'VIDE' :
				temp.append("Inside")
			elif listGeneSelect5[j][k][0] < listGeneSelect3[j][k][0] :
				temp.append("5'")
			else :
				temp.append("3'")
			temp.append(randomGene[j][k][0])
			temp.append(randomGene[j][k][1])
			temp.append(randomGene[j][k][2])
			temp.append(randomGene[j][k][3])
			temp.append(randomGene[j][k][4])
			temp.append(randomGene[j][k][5])
			temp.append(randomGene[j][k][6])
			temp.append(randomGene[j][k][7])
			temp.append(randomGene[j][k][8])
			aleatoire.append(temp)
			index += 1
			
	# Now write the random coordinates for later uses
	randomFile = pathVisualNEW + "/Downloaded/DATA_RandomGene.txt"
	dataFrame_Random = pd.DataFrame(aleatoire, columns=['TE family', 'TE Index', 'TE-Gene Position', 'Gene Distance', 'Gene Name', 'Gene Start', 'Gene End', 'Gene Sens', 'Gene ID', 'Gene Function', 'Gene Chrom', 'Position Inside'] ) 
	dataFrame_Random.to_csv(randomFile, index = False) # relative position
	
	
	
	
	
	
	
	
###############################################################################################################################################################
###	Extract the relative position of TE inside gene
###############################################################################################################################################################
def RandomSequences(pathVisual, pathVisualNEW, moduleSelectTE, NameSeq, TEDEB, TEFIN, list_selection_TE, listGeneSelect5, listGeneSelect3, listGeneSelectInside) :

	##########################################################################################################
	# Sequences aux positions aleatoire pour les TFBS
	randomSeqCHR, randomSeqDEB, randomSeqFIN = randomSequenceForTFBS(pathVisual, pathVisualNEW, moduleSelectTE, list_selection_TE, NameSeq, TEFIN, TEDEB)
	
	
	
	##########################################################################################################
	# Recupere des genes aleatoire en fonction de la position du TE avec le plus proche gene
	RandomSameDistance(pathVisual, pathVisualNEW, moduleSelectTE, NameSeq, TEDEB, TEFIN, list_selection_TE, listGeneSelect5, listGeneSelect3, listGeneSelectInside)
	
	
	return randomSeqDEB, randomSeqFIN, randomSeqCHR

