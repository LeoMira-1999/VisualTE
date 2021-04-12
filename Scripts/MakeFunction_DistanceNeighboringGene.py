#!/usr/bin/python3
import os
import sys
import importlib
import importlib.util
import pandas as pd
import plotly.graph_objs as go





########################################################################################################################
###	Create the general layout
########################################################################################################################
def Create_layout(temp, dataFrame_Organism):
	
	SelectionName = dataFrame_Organism['Name'].tolist()
	
	f = open(temp, "a")
	# cree le layout qui va tout contenir
	f.write("########################################################################################################################\n")
	f.write("# Creation du Layout pour dash \n\n")
	
	f.write("TEGeneDistance_layout = html.Div([ \n")
	f.write("	html.Div([ \n")
	
	f.write("		html.Div([ \n")
	f.write("			html.Label('Choose your sequence : ') \n")
	f.write("		], style={'width': '9%', 'vertical-align':'top', 'text-align':'center', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)'} ), \n\n")

	f.write("		html.Div([ \n")
	f.write("			# ajout du combolist et du graphique pour chaque chromosome \n")
	f.write("			dcc.Dropdown(\n")
	f.write("				id='SelectSequence_Dropdown_Onglet6', \n")
	f.write("				options=[ \n")
	f.write("					{'label': 'All', 'value': '0'}, \n")
	for z in range(0, len(SelectionName), 1) : 
		f.write("					{'label': '")
		f.write(SelectionName[z])
		f.write("', 'value': '")
		f.write(str(z+1))
		f.write("'}, \n")
	f.write("				], \n")
	f.write("				value='0', style={}, \n")
	f.write("				clearable=False, \n")
	f.write("			), \n")
	f.write("			html.Div(id='SelectSequence_Onglet6'), \n")
	f.write("		], style={'width': '90%', 'display': 'inline-block'} ), \n\n")
	
	f.write("	], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n")
	
	f.write("	# Here there are two graphs for the TE-gene distance \n") 
	f.write("	html.Div([ \n") 
	f.write("		html.Label('Distance TE - Genes') \n")
	f.write("	], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)', 'text-align': 'center'} ), \n\n")
	
	f.write("	html.Div([ \n") 
	f.write("		html.Div([ \n") 
	f.write("			html.Div(id='Onglet6_Gene_Div'), \n") 
	f.write("		], style={'width': '99%', 'display': 'inline-block'} ), \n") 
	f.write("	], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n\n\n")
	
	f.write("	html.Div([ \n")
	f.write("		html.Div(id='PieChart_Onglet6'), \n")
	f.write("	], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n")
						
	f.write("], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)'} )\n")
	f.write("\n\n\n\n\n")
	
	f.close()
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Create the general distance classes
########################################################################################################################
def CreationClasse(temp) :
	
	f = open(temp, "a")
	
	f.write("########################################################################################################################\n")
	f.write("# Creation des classes de distances \n") 
	f.write("def CreateClasseDist() : \n\n") 
	
	f.write("\tdistClass = [] \n")
	f.write("\tdistClass.append('Included') \n")
	f.write("\tdistClass.append('[1-10K[') \n")
	f.write("\tdistClass.append('[10K-20K[') \n")
	f.write("\tdistClass.append('[20K-30K[') \n")
	f.write("\tdistClass.append('[30K-40K[') \n")
	f.write("\tdistClass.append('[40K-50K[') \n")
	f.write("\tdistClass.append('[50K-60K[') \n")
	f.write("\tdistClass.append('[60K-70K[') \n")
	f.write("\tdistClass.append('[70K-80K[') \n")
	f.write("\tdistClass.append('[80K-90K[') \n")
	f.write("\tdistClass.append('[90K-100K[') \n")
	f.write("\tdistClass.append('[100K-110K[') \n")
	f.write("\tdistClass.append('[110K-120K[') \n")
	f.write("\tdistClass.append('[120K-130K[') \n")
	f.write("\tdistClass.append('[130K-140K[') \n")
	f.write("\tdistClass.append('[140K-150K[') \n")
	f.write("\tdistClass.append('[150K-160K[') \n")
	f.write("\tdistClass.append('[160K-170K[') \n")
	f.write("\tdistClass.append('[170K-180K[') \n")
	f.write("\tdistClass.append('[180K-190K[') \n")
	f.write("\tdistClass.append('[190K-200K[') \n")
	f.write("\tdistClass.append('[200K-300K[') \n")
	f.write("\tdistClass.append('[300K-400K[') \n")
	f.write("\tdistClass.append('[400K-500K[') \n")
	f.write("\tdistClass.append('[500K-600K[') \n")
	f.write("\tdistClass.append('[600K-700K[') \n")
	f.write("\tdistClass.append('[700K-800K[') \n")
	f.write("\tdistClass.append('[800K-900K[') \n")
	f.write("\tdistClass.append('[900K-1M[') \n")
	f.write("\tdistClass.append('[1M-+[') \n\n")
	
	f.write("\tdistClassGene = [] \n") 
	f.write("\tdistClassGene.append(\"5' UTR\") \n") 
	f.write("\tdistClassGene.append('Exon 1') \n") 
	f.write("\tdistClassGene.append('Intron 1') \n") 
	f.write("\tdistClassGene.append('Exon 2')  \n")
	f.write("\tdistClassGene.append('Intron 2') \n") 
	f.write("\tdistClassGene.append('Exon 3') \n") 
	f.write("\tdistClassGene.append('Intron 3') \n") 
	f.write("\tdistClassGene.append('Exon 4') \n") 
	f.write("\tdistClassGene.append('Intron 4') \n") 
	f.write("\tdistClassGene.append('Exon 5+') \n") 
	f.write("\tdistClassGene.append('Intron 5+') \n") 
	f.write("\tdistClassGene.append(\"3' UTR\") \n\n") 

	f.write("\treturn distClass, distClassGene \n\n")

	f.write("\n\n\n\n")
	f.close()
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Calculate the distribution of TE positions outside genes
########################################################################################################################
def CreationSelectionRandomSequences(temp) :
	
	f = open(temp, "a")
		
	f.write("########################################################################################################################  \n") 
	f.write("# Calcule pour chaque classe le nombre de sequences random ou TE \n") 
	f.write("def NbSequence_by_ClasseDistance(sommeDistanceClass, ClasseDistance, DistanceReelle) : \n\n")    
	
	f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("\t	for i in range(0, len(DistanceReelle[j]), 1) :  \n")
	f.write("\t		minDist = 0 \n")
	f.write("\t		if DistanceReelle[j][i] == '10000000000' or DistanceReelle[j][i] != 'VIDE' : \n")
	f.write("\t			minDist = int(DistanceReelle[j][i]) \n")
	f.write("\t		else : \n")
	f.write("\t			minDist = -1 \n")
	f.write("\t		if minDist == -1 : \n")
	f.write("\t			ClasseDistance[j][0] += 1 \n")
	f.write("\t		elif minDist < 10000 : \n")
	f.write("\t			ClasseDistance[j][1] += 1 \n")
	f.write("\t		elif minDist < 20000 : \n")
	f.write("\t			ClasseDistance[j][2] += 1 \n")
	f.write("\t		elif minDist < 30000 : \n")
	f.write("\t			ClasseDistance[j][3] += 1 \n")
	f.write("\t		elif minDist < 40000 : \n")
	f.write("\t			ClasseDistance[j][4] += 1 \n")
	f.write("\t		elif minDist < 50000 : \n")
	f.write("\t			ClasseDistance[j][5] += 1 \n")
	f.write("\t		elif minDist < 60000 : \n")
	f.write("\t			ClasseDistance[j][6] += 1 \n")
	f.write("\t		elif minDist < 70000 : \n")
	f.write("\t			ClasseDistance[j][7] += 1 \n")
	f.write("\t		elif minDist < 80000 : \n")
	f.write("\t			ClasseDistance[j][8] += 1 \n")
	f.write("\t		elif minDist < 90000 : \n")
	f.write("\t			ClasseDistance[j][9] += 1 \n")
	f.write("\t		elif minDist < 100000 : \n")
	f.write("\t			ClasseDistance[j][10] += 1 \n")
	f.write("\t		elif minDist < 110000 : \n")
	f.write("\t			ClasseDistance[j][11] += 1 \n")
	f.write("\t		elif minDist < 120000 : \n")
	f.write("\t			ClasseDistance[j][12] += 1 \n")
	f.write("\t		elif minDist < 130000 : \n")
	f.write("\t			ClasseDistance[j][13] += 1 \n")
	f.write("\t		elif minDist < 140000 : \n")
	f.write("\t			ClasseDistance[j][14] += 1 \n")
	f.write("\t		elif minDist < 150000 : \n")
	f.write("\t			ClasseDistance[j][15] += 1 \n")
	f.write("\t		elif minDist < 160000 : \n")
	f.write("\t			ClasseDistance[j][16] += 1 \n")
	f.write("\t		elif minDist < 170000 : \n")
	f.write("\t			ClasseDistance[j][17] += 1 \n")
	f.write("\t		elif minDist < 180000 : \n")
	f.write("\t			ClasseDistance[j][18] += 1 \n")
	f.write("\t		elif minDist < 190000 : \n")
	f.write("\t			ClasseDistance[j][19] += 1 \n")
	f.write("\t		elif minDist < 200000 : \n")
	f.write("\t			ClasseDistance[j][20] += 1 \n")
	f.write("\t		elif minDist < 300000 : \n")
	f.write("\t			ClasseDistance[j][21] += 1 \n")
	f.write("\t		elif minDist < 400000 : \n")
	f.write("\t			ClasseDistance[j][22] += 1 \n")
	f.write("\t		elif minDist < 500000 : \n")
	f.write("\t			ClasseDistance[j][23] += 1 \n")
	f.write("\t		elif minDist < 600000 : \n")
	f.write("\t			ClasseDistance[j][24] += 1 \n")
	f.write("\t		elif minDist < 700000 : \n")
	f.write("\t			ClasseDistance[j][25] += 1 \n")
	f.write("\t		elif minDist < 800000 : \n")
	f.write("\t			ClasseDistance[j][26] += 1 \n")
	f.write("\t		elif minDist < 900000 : \n")
	f.write("\t			ClasseDistance[j][27] += 1 \n")
	f.write("\t		elif minDist < 1000000 : \n")
	f.write("\t			ClasseDistance[j][28] += 1 \n")
	f.write("\t		else : \n")
	f.write("\t			ClasseDistance[j][29] += 1 \n")
	f.write("\t		sommeDistanceClass[j] += 1 \n\n")
	f.write("\n\n\n\n\n")
	
	
	
	f.write("########################################################################################################################  \n") 
	f.write("# Calcule pour chaque classe le nombre de sequences random ou TE \n") 
	f.write("def NbSequence_by_ClasseDistanceRandom(sommeDistanceClass, ClasseDistance, DistanceReelle) : \n\n")    
	
	f.write("\tfor i in range(0, len(DistanceReelle), 1) :  \n")
	f.write("\t	minDist = 0 \n")
	f.write("\t	if DistanceReelle[i] == '10000000000' or DistanceReelle[i] != 'VIDE' : \n")
	f.write("\t		minDist = int(DistanceReelle[i]) \n")
	f.write("\t	else : \n")
	f.write("\t		minDist = -1 \n")
	f.write("\t	if minDist == -1 : \n")
	f.write("\t		ClasseDistance[0] += 1 \n")
	f.write("\t	elif minDist < 10000 : \n")
	f.write("\t		ClasseDistance[1] += 1 \n")
	f.write("\t	elif minDist < 20000 : \n")
	f.write("\t		ClasseDistance[2] += 1 \n")
	f.write("\t	elif minDist < 30000 : \n")
	f.write("\t		ClasseDistance[3] += 1 \n")
	f.write("\t	elif minDist < 40000 : \n")
	f.write("\t		ClasseDistance[4] += 1 \n")
	f.write("\t	elif minDist < 50000 : \n")
	f.write("\t		ClasseDistance[5] += 1 \n")
	f.write("\t	elif minDist < 60000 : \n")
	f.write("\t		ClasseDistance[6] += 1 \n")
	f.write("\t	elif minDist < 70000 : \n")
	f.write("\t		ClasseDistance[7] += 1 \n")
	f.write("\t	elif minDist < 80000 : \n")
	f.write("\t		ClasseDistance[8] += 1 \n")
	f.write("\t	elif minDist < 90000 : \n")
	f.write("\t		ClasseDistance[9] += 1 \n")
	f.write("\t	elif minDist < 100000 : \n")
	f.write("\t		ClasseDistance[10] += 1 \n")
	f.write("\t	elif minDist < 110000 : \n")
	f.write("\t		ClasseDistance[11] += 1 \n")
	f.write("\t	elif minDist < 120000 : \n")
	f.write("\t		ClasseDistance[12] += 1 \n")
	f.write("\t	elif minDist < 130000 : \n")
	f.write("\t		ClasseDistance[13] += 1 \n")
	f.write("\t	elif minDist < 140000 : \n")
	f.write("\t		ClasseDistance[14] += 1 \n")
	f.write("\t	elif minDist < 150000 : \n")
	f.write("\t		ClasseDistance[15] += 1 \n")
	f.write("\t	elif minDist < 160000 : \n")
	f.write("\t		ClasseDistance[16] += 1 \n")
	f.write("\t	elif minDist < 170000 : \n")
	f.write("\t		ClasseDistance[17] += 1 \n")
	f.write("\t	elif minDist < 180000 : \n")
	f.write("\t		ClasseDistance[18] += 1 \n")
	f.write("\t	elif minDist < 190000 : \n")
	f.write("\t		ClasseDistance[19] += 1 \n")
	f.write("\t	elif minDist < 200000 : \n")
	f.write("\t		ClasseDistance[20] += 1 \n")
	f.write("\t	elif minDist < 300000 : \n")
	f.write("\t		ClasseDistance[21] += 1 \n")
	f.write("\t	elif minDist < 400000 : \n")
	f.write("\t		ClasseDistance[22] += 1 \n")
	f.write("\t	elif minDist < 500000 : \n")
	f.write("\t		ClasseDistance[23] += 1 \n")
	f.write("\t	elif minDist < 600000 : \n")
	f.write("\t		ClasseDistance[24] += 1 \n")
	f.write("\t	elif minDist < 700000 : \n")
	f.write("\t		ClasseDistance[25] += 1 \n")
	f.write("\t	elif minDist < 800000 : \n")
	f.write("\t		ClasseDistance[26] += 1 \n")
	f.write("\t	elif minDist < 900000 : \n")
	f.write("\t		ClasseDistance[27] += 1 \n")
	f.write("\t	elif minDist < 1000000 : \n")
	f.write("\t		ClasseDistance[28] += 1 \n")
	f.write("\t	else : \n")
	f.write("\t		ClasseDistance[29] += 1 \n")
	f.write("\t	sommeDistanceClass += 1 \n")
	f.write("\treturn sommeDistanceClass \n")
	f.write("\n\n\n\n\n")
	
	f.close()
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Calculate the distribution of TE positions inside genes
########################################################################################################################
def CreationSelectionRandomSequencesInside(temp) :
	
	f = open(temp, "a")
		
	f.write("########################################################################################################################  \n") 
	f.write("# Calcule pour chaque classe le nombre de sequences random ou TE dans le gene \n") 
	f.write("def NbSequenceInside(PosInside, InsideGeneClass, somme) : \n\n")
	
	f.write("\t# Get the position of the TE sequences inside the genes : UTR, intron or exons \n") 
	f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")  
	f.write("\t	for i in range(0, len(PosInside[j]), 1) : \n") 
	f.write("\t		if PosInside[j][i] != 'VIDE' : \n") 
	f.write("\t			typeRelative = PosInside[j][i][:1] \n") 
	f.write("\t			relativePos = PosInside[j][i][1:] \n") 
	f.write("\t			somme[j] += 1 \n") 
	f.write("\t			if typeRelative == 'U' : \n") 
	f.write("\t				if relativePos == '5' : \n") 
	f.write("\t					InsideGeneClass[j][0] += 1 \n") 
	f.write("\t				else : \n") 
	f.write("\t					InsideGeneClass[j][11] += 1 \n") 
	f.write("\t			elif typeRelative == 'I' : \n") 
	f.write("\t				if int(relativePos) <= 5 : \n") 
	f.write("\t					InsideGeneClass[j][2*int(relativePos)] += 1  \n") 
	f.write("\t				else : \n") 
	f.write("\t					InsideGeneClass[j][10] += 1 \n") 
	f.write("\t			else : \n")
	f.write("\t				if int(relativePos) <= 5 : \n") 
	f.write("\t					InsideGeneClass[j][2*int(relativePos)-1] += 1 \n") 
	f.write("\t				else : \n") 
	f.write("\t					InsideGeneClass[j][9] += 1  \n") 
	f.write("\n\n\n\n\n")
	
	
	
	f.write("########################################################################################################################  \n") 
	f.write("# Calcule pour chaque classe le nombre de sequences random ou TE dans le gene \n") 
	f.write("def NbSequenceInsideRandom(PosInside, InsideGeneClass, somme) : \n\n")
	
	f.write("\t# Get the position of the TE sequences inside the genes : UTR, intron or exons \n") 
	f.write("\tfor i in range(0, len(PosInside), 1) : \n") 
	f.write("\t	if PosInside[i] != 'VIDE' : \n") 
	f.write("\t		typeRelative = PosInside[i][:1] \n") 
	f.write("\t		relativePos = PosInside[i][1:] \n") 
	f.write("\t		somme += 1 \n") 
	f.write("\t		if typeRelative == 'U' : \n") 
	f.write("\t			if relativePos == '5' : \n") 
	f.write("\t				InsideGeneClass[0] += 1 \n") 
	f.write("\t			else : \n") 
	f.write("\t				InsideGeneClass[11] += 1 \n") 
	f.write("\t		elif typeRelative == 'I' : \n") 
	f.write("\t			if int(relativePos) <= 5 : \n") 
	f.write("\t				InsideGeneClass[2*int(relativePos)] += 1  \n") 
	f.write("\t			else : \n") 
	f.write("\t				InsideGeneClass[10] += 1 \n") 
	f.write("\t		else : \n")
	f.write("\t			if int(relativePos) <= 5 : \n") 
	f.write("\t				InsideGeneClass[2*int(relativePos)-1] += 1 \n") 
	f.write("\t			else : \n") 
	f.write("\t				InsideGeneClass[9] += 1  \n") 
	f.write("\treturn somme \n") 
	f.write("\n\n\n\n\n")
	
	f.close()
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Get the values for the sliders
########################################################################################################################
def ValueSliderRecup(temp) :
	
	f = open(temp, "a")
	
	f.write("	# Calcul pour les TEs \n") 
	f.write("	tailleMinOther = CommonDATA_SelectTEs.dataFrame_superTE['Size'].min() \n") 
	f.write("	tailleMaxOther = CommonDATA_SelectTEs.dataFrame_superTE['Size'].max() \n") 
	f.write("	tailleMin = 0 \n") 
	f.write("	if valueSliders[0] == 1 : \n") 
	f.write("		tailleMin = 0 \n") 
	f.write("	else : \n") 
	f.write("		tailleMin = MinConsensus * valueSliders[0] / 100 \n") 
	f.write("	tailleMax = 0 \n") 
	f.write("	if valueSliders[1] == 100 : \n") 
	f.write("		tailleMax = 10 * MaxConsensus \n") 
	f.write("	else : \n") 
	f.write("		tailleMax = MaxConsensus * valueSliders[1] / 100 \n") 
	f.write("	tailleMin_otherTE = 0 \n") 
	f.write("	if valueSliders[0] == 1 : \n") 
	f.write("		tailleMin_otherTE = tailleMinOther - 1 \n") 
	f.write("	else : \n") 
	f.write("		tailleMin_otherTE = tailleMaxOther * valueSliders[0] / 100 \n") 
	f.write("	tailleMax_otherTE = 0 \n") 
	f.write("	if valueSliders[1] == 100 : \n") 
	f.write("		tailleMax_otherTE = 10 * tailleMaxOther \n") 
	f.write("	else : \n") 
	f.write("		tailleMax_otherTE = tailleMaxOther * valueSliders[1] / 100 \n\n\n\n") 
	
	f.close()
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Callback that will updates the first graph inside
########################################################################################################################
def CreatedCallBack_Distplot_Onglet6(temp, numberTE) :
	
	f = open(temp, "a")

	f.write("########################################################################################################################\n")
	f.write("# ajout du callback\n\n")
	f.write("# marcher avec un multi input !! mais il faut que 1 seul output \n")
	f.write("@app.callback( \n")
	f.write("	Output('Onglet6_Gene_Div', 'children'), \n")
	f.write("	[Input('memory', 'data'), Input('SelectSequence_Dropdown_Onglet6', 'value') ] \n")
	f.write(")\n\n")

	f.write("def update_Chromosome_Onglet6(valueSliders, SelectSequence_Dropdown_Onglet6) : \n")
	f.write("\t# valueSliders[0] and valueSliders[1] are boundary for the size slider\n")
	f.write("\t# valueSliders[2] and valueSliders[3] are boundary for the similarity slider\n\n")
	f.close()
	
	
	ValueSliderRecup(temp)
	
	
	f = open(temp, "a")
	f.write("\tindiceCHR = 0 \n")
	f.write("\tSeqTE = [] \n")
	f.write("\tIndexTE = [] \n")
	f.write("\tSimilarityTE = [] \n")
	f.write("\tIndexGene = [] \n")
	f.write("\tTEGenePos = [] \n")
	f.write("\tDistance = [] \n")
	f.write("\tGeneFunctionID = [] \n")
	f.write("\tDebTE = [] \n")
	f.write("\tPositions = [] \n")
	f.write("\tIndexTEGlobal = [] \n")
	f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n") 
	f.write("\t	SeqTE.append([]) \n") 
	f.write("\t	IndexTE.append([]) \n") 
	f.write("\t	SimilarityTE.append([]) \n") 
	f.write("\t	IndexGene.append([]) \n") 
	f.write("\t	TEGenePos.append([]) \n") 
	f.write("\t	Distance.append([]) \n")
	f.write("\t	GeneFunctionID.append([]) \n")
	f.write("\t	DebTE.append([]) \n")
	f.write("\t	Positions.append([]) \n\n")
		
	f.write("\tif SelectSequence_Dropdown_Onglet6 == None or SelectSequence_Dropdown_Onglet6 == '0' : \n")
	f.write("\t	indiceCHR = 0 \n")
	f.write("\t	for j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("\t		Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[j]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3]), : ]  \n")  
	f.write("\t		SeqTE[j] = Select_myTE['Chr ID'].tolist() \n")
	f.write("\t		IndexTE[j] = Select_myTE['Index'].tolist() \n")
	f.write("\t		SimilarityTE[j] = Select_myTE['Similarity'].tolist() \n")
	f.write("\t		DebTE[j] = Select_myTE['Start'].tolist() \n\n")
	
	f.write("\t		Select_myGene = CommonDATA_SelectTEs.dataFrame_CloseGene.loc[ CommonDATA_SelectTEs.dataFrame_CloseGene['TE Index'].isin(IndexTE[j]), : ] \n")
	f.write("\t		IndexGene[j] = Select_myGene['TE Index'].tolist() \n")
	f.write("\t		TEGenePos[j] = Select_myGene['TE-Gene Position'].tolist() \n")
	f.write("\t		Distance[j] = Select_myGene['Gene Distance'].tolist() \n")
	f.write("\t		GeneFunctionID[j] = Select_myGene['Gene ID'].tolist() \n") 
	f.write("\t		Positions[j] = Select_myGene['Position Inside'].tolist() \n") 
	f.write("\telse : \n")
	f.write("\t	indiceCHR = int(SelectSequence_Dropdown_Onglet6) \n")
	f.write("\t	for j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("\t		Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[j]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Chr Name'] == SelectionNameID[indiceCHR]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3]), : ] \n")     
	f.write("\t		SeqTE[j] = Select_myTE['Chr ID'].tolist() \n")
	f.write("\t		IndexTE[j] = Select_myTE['Index'].tolist() \n")
	f.write("\t		SimilarityTE[j] = Select_myTE['Similarity'].tolist() \n")
	f.write("\t		DebTE[j] = Select_myTE['Start'].tolist() \n\n")
	
	f.write("\t		Select_myGene = CommonDATA_SelectTEs.dataFrame_CloseGene.loc[ CommonDATA_SelectTEs.dataFrame_CloseGene['TE Index'].isin(IndexTE[j]), : ] \n")
	f.write("\t		IndexGene[j] = Select_myGene['TE Index'].tolist() \n")
	f.write("\t		TEGenePos[j] = Select_myGene['TE-Gene Position'].tolist() \n")
	f.write("\t		Distance[j] = Select_myGene['Gene Distance'].tolist() \n")
	f.write("\t		GeneFunctionID[j] = Select_myGene['Gene ID'].tolist() \n") 
	f.write("\t		Positions[j] = Select_myGene['Position Inside'].tolist() \n\n")
	
	f.write("\t# Put all selected TE index in the same list \n")
	f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("\t	for i in range(0, len(IndexTE[j]), 1) : \n")
	f.write("\t		IndexTEGlobal.append(IndexTE[j][i]) \n\n\n")
	
	
	
	f.write("\trandomPositions = [] \n")
	f.write("\trandomInside = [] \n")
	f.write("\trandomID = [] \n")
	f.write("\trandomFunction = [] \n")
	f.write("\tif SelectSequence_Dropdown_Onglet6 == None or SelectSequence_Dropdown_Onglet6 == '0' : \n")
	f.write("\t	indiceCHR = 0 \n")
	f.write("\t	Select_Positions = CommonDATA_SelectTEs.dataFrame_RandomSeq.loc[ (CommonDATA_SelectTEs.dataFrame_RandomSeq['TE Index'].isin(IndexTEGlobal)), : ] \n")
	f.write("\t	randomPositions = Select_Positions['Gene Distance'].tolist() \n") 
	f.write("\t	randomInside = Select_Positions['Position Inside'].tolist() \n") 
	f.write("\t	randomID = Select_Positions['Gene ID'].tolist() \n")
	f.write("\t	randomFunction = Select_Positions['Gene Function'].tolist() \n")
	f.write("\telse : \n")
	f.write("\t	indiceCHR = int(SelectSequence_Dropdown_Onglet6) \n") 
	f.write("\t	Select_Positions = CommonDATA_SelectTEs.dataFrame_RandomSeq.loc[ (CommonDATA_SelectTEs.dataFrame_RandomSeq['TE Index'].isin(IndexTEGlobal)) & (CommonDATA_SelectTEs.dataFrame_RandomSeq['Gene Chrom'] == SelectionNameID[indiceCHR]), : ] \n")
	f.write("\t	randomPositions = Select_Positions['Gene Distance'].tolist() \n") 
	f.write("\t	randomInside = Select_Positions['Position Inside'].tolist() \n")  
	f.write("\t	randomID = Select_Positions['Gene ID'].tolist() \n")
	f.write("\t	randomFunction = Select_Positions['Gene Function'].tolist() \n")
	f.write("\n\n\n")
	
	
	
	f.write("\t########################################################################################################## \n") 
	f.write("\t# Create the two array for the distance class (inside outside gene) \n") 
	f.write("\tdistClass, distClassGene = CreateClasseDist() \n") 
	f.write("\n\n\n")



	f.write("\t########################################################################################################## \n") 
	f.write("\tnbTEinclassDistance = [] \n")
	f.write("\tsommeTEdistanceClass = [] \n")
	f.write("\tpercentTEdistanceClass = [] \n")
	f.write("\taffichageTE = [] \n")
	f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("\t	nbTEinclassDistance.append([]) \n")
	f.write("\t	percentTEdistanceClass.append([]) \n")
	f.write("\t	affichageTE.append([]) \n")
	f.write("\t	sommeTEdistanceClass.append(0) \n")
	f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("\t	for i in range(0, 30, 1) : \n")
	f.write("\t		nbTEinclassDistance[j].append(0) \n")
	f.write("\t		percentTEdistanceClass[j].append(0) \n")
	f.write("\t		affichageTE[j].append(0) \n")
	f.write("\tNbSequence_by_ClasseDistance(sommeTEdistanceClass, nbTEinclassDistance, Distance) \n")
	f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n") 
	f.write("\t	for i in range(0, 30, 1) : \n")
	f.write("\t		percentTEdistanceClass[j][i] = round((100 * nbTEinclassDistance[j][i] / sommeTEdistanceClass[j]), 2) \n")
	f.write("\t		affichageTE[j][i] = str(nbTEinclassDistance[j][i]) + ' (' + str(percentTEdistanceClass[j][i]) + '%)' \n\n")
	
	f.write("\trandomInclassDistance = [] \n")
	f.write("\tsommerandomdistanceClass = 0 \n")
	f.write("\tpercentrandomdistanceClass = [] \n")
	f.write("\taffichageRandom = [] \n")
	f.write("\tfor i in range(0, 30, 1) : \n")
	f.write("\t	randomInclassDistance.append(0) \n")
	f.write("\t	percentrandomdistanceClass.append(0) \n")
	f.write("\t	affichageRandom.append(0) \n") 
	f.write("\tsommerandomdistanceClass = NbSequence_by_ClasseDistanceRandom(sommerandomdistanceClass, randomInclassDistance, randomPositions) \n")
	f.write("\tfor i in range(0, 30, 1) : \n")
	f.write("\t	percentrandomdistanceClass[i] = round((100 * randomInclassDistance[i] / sommerandomdistanceClass), 2) \n")
	f.write("\t	affichageRandom[i] = str(randomInclassDistance[i]) + ' (' + str(percentrandomdistanceClass[i]) + '%)' \n")
	f.write("\n\n\n")
	
	
	
	
	f.write("\t########################################################################################################## \n")
	f.write("\t# Calculate the over- under- reprensation of your distance TE distribution \n")
	f.write("\tlisteObs1 = [] \n") 
	f.write("\tlistTheo1 = [] \n") 
	f.write("\tOverRepresented1 = [] \n") 
	f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n") 
	f.write("\t	listeObs1.append([]) \n")
	f.write("\t	listTheo1.append([]) \n")
	f.write("\t	OverRepresented1.append([]) \n")
	f.write("\t	for i in range(0, 30, 1) : \n") 
	f.write("\t		if (nbTEinclassDistance[j][i] >= 5 and randomInclassDistance[i] > 0) or (nbTEinclassDistance[j][i] > 0 and randomInclassDistance[i] >= 5) : \n") 
	f.write("\t			listeObs1[j].append( nbTEinclassDistance[j][i] ) \n") 
	f.write("\t			listTheo1[j].append( randomInclassDistance[i] ) \n") 
	f.write("\t		OverRepresented1[j].append('white') \n")
	f.write("\t	chi_statistic, p_value = chisquare(listeObs1[j], listTheo1[j]) \n") 
	f.write("\t	critique = chi2.ppf(q = 0.99, df = len(listeObs1[j])) \n") 
	f.write("\t	if float(critique) < float(chi_statistic) and float(p_value) <= 0.01 :	# There are over- and under- represented bias in chromosome \n") 
	f.write("\t		for i in range(0, 30, 1) : \n") 
	f.write("\t			if percentrandomdistanceClass[i] > 0 : \n") 
	f.write("\t				if float(percentrandomdistanceClass[i] + percentrandomdistanceClass[i]/2) <= float(percentTEdistanceClass[j][i]) : \n")
	f.write("\t					OverRepresented1[j][i] = Couleur.couleurSelectTE[j] \n")
	f.write("\t	for i in range(0, 30, 1) : \n") 
	f.write("\t		if percentrandomdistanceClass[i] == 0 and percentTEdistanceClass[j][i] > 5 : \n")
	f.write("\t			OverRepresented1[j][i] = Couleur.couleurSelectTE[j] \n\n\n")


	for i in range (0, numberTE, 1) :
		f.write("\tDistanceBarChart" + str(i) + " = go.Bar(name=CommonDATA_SelectTEs.list_selection_TE["  + str(i) + "], x = distClass, y = percentTEdistanceClass["  + str(i) + "], text = affichageTE["  + str(i) + "], hovertemplate = '%{text}', marker=dict(color = OverRepresented1["  + str(i) + "], line=dict(width=2, color=Couleur.couleurSelectTE["  + str(i) + "])) ) \n")    
	f.write("\tAverageDistanceChart = go.Scatter(name='Normal distribution', x = distClass, y = percentrandomdistanceClass, text = affichageRandom, hovertemplate = '%{text}', marker=dict(color = 'darkgrey'), mode='lines', line_shape='spline' ) \n")
	f.write("\n\n\n\n\n")
	
	
	
	
	f.write("\t##########################################################################################################  \n")
	f.write("\tTEInsideGeneClass = [] \n")
	f.write("\tTEsommeInsideGene = [] \n")
	f.write("\tTEpercentInsideGene = [] \n")
	f.write("\taffichageTEInsideGene = [] \n")
	f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE)+1, 1) : \n")
	f.write("\t	TEInsideGeneClass.append([]) \n")
	f.write("\t	TEpercentInsideGene.append([]) \n")
	f.write("\t	affichageTEInsideGene.append([]) \n")
	f.write("\t	TEsommeInsideGene.append(0) \n")
	f.write("\t	for i in range(0, 12, 1) : \n")
	f.write("\t		TEInsideGeneClass[j].append(0) \n")
	f.write("\t		TEpercentInsideGene[j].append(0) \n")
	f.write("\t		affichageTEInsideGene[j].append(0) \n")
	f.write("\tNbSequenceInside(Positions, TEInsideGeneClass, TEsommeInsideGene) \n")
	f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE)+1, 1) : \n")
	f.write("\t	if TEsommeInsideGene[j] > 0 : \n")
	f.write("\t		for i in range(0, 12, 1) : \n")
	f.write("\t			TEpercentInsideGene[j][i] = round((100 * TEInsideGeneClass[j][i] / TEsommeInsideGene[j]), 2) \n") 
	f.write("\t			affichageTEInsideGene[j][i] = str(TEInsideGeneClass[j][i]) + ' (' + str(TEpercentInsideGene[j][i]) + '%)' \n")
	f.write("\t	else : \n")
	f.write("\t		for i in range(0, 12, 1) : \n") 
	f.write("\t			TEpercentInsideGene[j][i] = 0.0 \n")
	f.write("\t			affichageTEInsideGene[j][i] = '0 (0.0%)' \n\n")
	
	f.write("\tRandomInsideGeneClass = [] \n")
	f.write("\tRandomsommeInsideGene = 0 \n")
	f.write("\tRandompercentInsideGene = [] \n")
	f.write("\taffichageRandomInsideGene = [] \n")
	f.write("\tfor i in range(0, 12, 1) : \n")
	f.write("\t	RandomInsideGeneClass.append(0) \n")
	f.write("\t	RandompercentInsideGene.append(0) \n")
	f.write("\t	affichageRandomInsideGene.append(0) \n")
	f.write("\tRandomsommeInsideGene = NbSequenceInsideRandom(randomInside, RandomInsideGeneClass, RandomsommeInsideGene) \n")
	f.write("\tfor i in range(0, 12, 1) : \n")
	f.write("\t	RandompercentInsideGene[i] = round((100 * RandomInsideGeneClass[i] / RandomsommeInsideGene), 2) \n") 
	f.write("\t	affichageRandomInsideGene[i] = str(RandomInsideGeneClass[i]) + ' (' + str(RandompercentInsideGene[i]) + '%)' \n")
	f.write("\n\n\n\n")
	
	
	
	
	
	f.write("\t########################################################################################################## \n")
	f.write("\t# Calculate the over- under- reprensation of your distance TE distribution \n")
	f.write("\tlisteObs2 = [] \n") 
	f.write("\tlistTheo2 = [] \n") 
	f.write("\tOverRepresented2 = [] \n") 
	f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n") 
	f.write("\t	listeObs2.append([]) \n")
	f.write("\t	listTheo2.append([]) \n")
	f.write("\t	OverRepresented2.append([]) \n")
	f.write("\t	for i in range(0, 12, 1) : \n")  
	f.write("\t		if (TEInsideGeneClass[j][i] >= 5 and RandomInsideGeneClass[i] > 0) or (TEInsideGeneClass[j][i] > 0 and RandomInsideGeneClass[i] >= 5) : \n") 
	f.write("\t			listeObs2[j].append( TEInsideGeneClass[j][i] ) \n") 
	f.write("\t			listTheo2[j].append( RandomInsideGeneClass[i] ) \n") 
	f.write("\t		OverRepresented2[j].append('white') \n")
	f.write("\t	chi_statistic, p_value = chisquare(listeObs2[j], listTheo2[j]) \n") 
	f.write("\t	critique = chi2.ppf(q = 0.99, df = len(listeObs2[j])) \n") 
	f.write("\t	if float(critique) < float(chi_statistic) and float(p_value) <= 0.01 :	# There are over- and under- represented bias in chromosome \n") 
	f.write("\t		for i in range(0, 12, 1) : \n")  
	f.write("\t			if RandomInsideGeneClass[i] > 0 : \n") 
	f.write("\t				if float(RandompercentInsideGene[i] + RandompercentInsideGene[i]/2) <= float(TEpercentInsideGene[j][i]) : \n")
	f.write("\t					OverRepresented2[j][i] = Couleur.couleurSelectTE[j] \n")
	f.write("\t	for i in range(0, 12, 1) : \n")
	f.write("\t		if RandompercentInsideGene[i] == 0 and TEpercentInsideGene[j][i] > 5 : \n")
	f.write("\t			OverRepresented2[j][i] = Couleur.couleurSelectTE[j] \n\n\n")
	
	
	for i in range (0, numberTE, 1) :
		f.write("\tInsideBarChart" + str(i) + " = go.Bar(name=CommonDATA_SelectTEs.list_selection_TE[" + str(i) + "], x = distClassGene, y = TEpercentInsideGene[" + str(i) + "], text = affichageTEInsideGene[" + str(i) + "], hovertemplate = '%{text}', marker=dict(color = OverRepresented2[" + str(i) + "], line=dict(width=2, color=Couleur.couleurSelectTE["  + str(i) + "])) ) \n") 
	f.write("\tAverageInsideChart = go.Scatter(name='Normal distribution', x = distClassGene, y = RandompercentInsideGene, text = affichageRandomInsideGene, hovertemplate = '%{text}', marker=dict(color = 'darkgrey'), mode='lines', line_shape='spline' ) \n") 
	f.write("\n\n\n\n\n")
	
	
	
	
	
	f.write("\t########################################################################################################## \n") 
	f.write("\ttitreInside = 'TE Distribution inside genes for ' + CommonDATA_SelectTEs.OfficialName + ' families' \n")  
	f.write("\ttitreDistance = 'Distribution of the TE-genes distance for ' + CommonDATA_SelectTEs.OfficialName + ' families' \n")  
	f.write("\tOnglet6Voisin = html.Div([ \n\n") 
	
	f.write("\t	html.Div([ \n")  
	f.write("\t		dcc.Graph( \n") 
	f.write("\t			id = 'Details_Distance', \n") 
	f.write("\t			figure = { \n") 
	f.write("\t				'data': [AverageInsideChart ")
	for i in range (0, numberTE, 1) :
		f.write(", InsideBarChart" + str(i))
	f.write("], \n") 
	f.write("\t				'layout': { \n")  
	f.write("\t					'title':titreInside, \n")
	f.write("\t					'plot_bgcolor':'rgba(255,255,255,1)', \n")  
	f.write("\t					'render_mode':'webgl', \n")  
	f.write("\t					'xaxis_tickangle':'90', \n") 
	f.write("\t					'yaxis':dict(title='Distance class percentage', titlefont_size=16), \n")  
	f.write("\t					'barmode':'group', \n")  
	f.write("\t					'hovermode':'x unified', \n")  
	f.write("\t					'margin' : dict(l=40, r=20, t=30, b=80),  \n")  
	f.write("\t					'legend':dict(orientation='h', yanchor='top', y=-0.13),  \n") 
	f.write("\t				}, \n") 
	f.write("\t			}, \n") 
	f.write("\t			style = {'overflowX': 'scroll', 'overflowY': 'scroll'} \n") 
	f.write("\t		), \n") 
	f.write("\t	], style={'overflowX':'scroll', 'overflowY':'scroll', 'width':'30%', 'height':'820', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)'}), \n\n") 
		
	f.write("\t	html.Div([ \n") 
	f.write("\t		# affiche le graphe barplot des distances \n")		
	f.write("\t		dcc.Graph( \n")
	f.write("\t			id = 'NeighboringGene_Distance', \n")
	f.write("\t			figure = { \n") 
	f.write("\t				'data': [AverageDistanceChart ")
	for i in range (0, numberTE, 1) :
		f.write(", DistanceBarChart" + str(i))
	f.write("], \n") 
	f.write("\t				'layout': { \n") 
	f.write("\t					'title':titreDistance, \n")
	f.write("\t					'plot_bgcolor':'rgba(255,255,255,1)', \n") 
	f.write("\t					'render_mode':'webgl', \n") 
	f.write("\t					'xaxis_tickangle':'90', \n") 
	f.write("\t					'yaxis':dict(title='Distance class percentage', titlefont_size=16), \n")
	f.write("\t					'barmode':'group', \n")
	f.write("\t					'hovermode':'x unified', \n")
	f.write("\t					'margin' : dict(l=40, r=20, t=30, b=80),  \n")
	f.write("\t					'legend':dict(orientation='h', yanchor='top', y=-0.13),  \n")
	f.write("\t				}, \n") 
	f.write("\t			}, \n") 
	f.write("\t			style = {'overflowX': 'scroll', 'overflowY': 'scroll'} \n") 
	f.write("\t		), \n") 
	f.write("\t	], style={'overflowX':'scroll', 'overflowY':'scroll', 'width':'70%', 'height':'820', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)'}), \n\n") 
		
	f.write("\t], style={'overflowX':'scroll', 'overflowY':'scroll', 'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'}), \n")

	f.write("\treturn Onglet6Voisin \n\n\n\n\n\n") 
	f.close()
	
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Create the AnnotationDistance function
########################################################################################################################
def DistanceNeighboringGene(pathVisual, pathVisualNEW, nbSeq_Assemble, numberTE):
	
	# Ajout des librairies python pour le serveur
	temp = pathVisualNEW + '/Functions/TEGeneDistance.py'
	f = open(temp, "w")

	f.write("#!/usr/bin/env python3\n")
	f.write("# -*- coding: utf-8 -*-\n")
	f.write("import math\n")
	f.write("from scipy.stats import chisquare \n")
	f.write("from scipy.stats import chi2 \n")
	f.write("import gseapy as gp \n")
	f.write("import dash\n")
	f.write("import dash_table \n")
	f.write("import dash_daq as daq\n")
	f.write("import dash_core_components as dcc\n")
	f.write("import dash_html_components as html\n")
	f.write("import plotly.graph_objects as go\n")
	f.write("import plotly.figure_factory as ff\n")
	f.write("import pandas as pd \n")
	f.write("from dash.dependencies import Input, Output\n")
	f.write("from app import app \n")
	f.write("from Functions import CommonDATA, CommonDATA_SelectTEs, Couleur\n\n\n\n")


	f.write("########################################################################################################################\n")
	f.write("# Data that does not change with the sliders \n\n")
	
	f.write("SelectionNameID = CommonDATA.dataFrame_Organism['NameID'].tolist() \n")
	f.write("SelectionNameID.insert(0, 'All') \n\n")
	
	f.write("# Calcul pour les TEs \n")
	# prise en compte d'1 ou plusieurs familles de TEs
	f.write("MinConsensus = 1000000 \n")
	f.write("MaxConsensus = 0 \n")
	f.write("if len(CommonDATA_SelectTEs.list_selection_TE) == 1 : \n" )
	f.write("	MinConsensus = CommonDATA_SelectTEs.TailleConsensus[0] \n")
	f.write("	MaxConsensus = CommonDATA_SelectTEs.TailleConsensus[0] \n")
	f.write("else : \n")
	f.write("	for i in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("		if MinConsensus > CommonDATA_SelectTEs.TailleConsensus[i] : \n")
	f.write("			MinConsensus = CommonDATA_SelectTEs.TailleConsensus[i] \n")
	f.write("		if MaxConsensus < CommonDATA_SelectTEs.TailleConsensus[i] : \n")
	f.write("			MaxConsensus = CommonDATA_SelectTEs.TailleConsensus[i] \n")
	f.write("\n\n\n\n\n")
	
	f.close()
	
	
	
	# get the data for the organism
	tempFile = pathVisual + '/Downloaded/DATA_Organism.txt'
	dataT = pd.read_csv(tempFile)
	# Create first a sud-dataframe that contains only the wanted values
	dataFrame_Organism = dataT.loc[(dataT['Size bp'] > 0)]
	
	
	
	# Create the initial layout that contains this fonction
	Create_layout(temp, dataFrame_Organism)
	
	# Create the two distances graphs and its supplementary figure
	CreationClasse(temp)
	CreationSelectionRandomSequences(temp)
	CreationSelectionRandomSequencesInside(temp)
	CreatedCallBack_Distplot_Onglet6(temp, numberTE)
	
	
	
	
	
	
	'''
	# initializing string representation of a list 
	ini_list = "[1, 2, 3, 4, 5]"
	
	# printing initialized string of list and its type 
	print ("initial string", ini_list) 
	print (type(ini_list)) 
	
	# Converting string to list 
	res = ini_list.strip('][').split(', ') 
	'''

		

	
