#!/usr/bin/python3
import os
import sys
import importlib
import importlib.util
import pandas as pd
import plotly.graph_objs as go





########################################################################################################################
###	Create the Table that contains genome information
########################################################################################################################
def InformationGenome(temp) :

	f = open(temp, "a")

	f.write("#Put the invariable values that do not change with the slider \n")
	f.write("SelectionName   = CommonDATA.dataFrame_Organism['Name'].tolist() \n")
	f.write("SelectionSizeBP = CommonDATA.dataFrame_Organism['Size bp'].tolist() \n")
	f.write("SelectionRefseq = CommonDATA.dataFrame_Organism['RefSeq'].tolist() \n")
	f.write("SelectionNameID = CommonDATA.dataFrame_Organism['NameID'].tolist() \n")
	f.write("TailleChrom     = CommonDATA.dataFrame_Organism['Size bp'].tolist() \n")
	f.write("SelectionSize   = CommonDATA.dataFrame_Organism['Size Mb'].tolist() \n\n")

	f.close()











########################################################################################################################
###	Create the legend before the chromsome bar
########################################################################################################################
def LegendeChrom(temp):

	f = open(temp, "a")

	f.write("xLegend = [] \n")
	f.write("for z in range(len(SelectionSize)-1, -1, -1) : \n")
	f.write("	xLegend.append(50) \n")
	f.write("	xLegend.append(50) \n")

	f.write("k = 0 \n")
	f.write("yLegend = [] \n")
	f.write("for z in range(len(SelectionSize)-1, -1, -1) : \n")
	f.write("	yLegend.append(75 * k + 110) \n")
	f.write("	yLegend.append(75 * k + 85) \n")
	f.write("	k += 1 \n")

	f.write("textLegend = [] \n")
	f.write("for z in range(len(SelectionSize)-1, -1, -1) : \n")
	f.write("	textLegend.append(SelectionName[z]) \n")
	f.write("	textLegend.append(str(SelectionSizeBP[z]) + ' bp') \n")

	f.write("textfont_sizeLegend = [] \n")
	f.write("for z in range(len(SelectionSize)-1, -1, -1) : \n")
	f.write("	textfont_sizeLegend.append(18) \n")
	f.write("	textfont_sizeLegend.append(11) \n")

	f.write("LegendeChromosome = go.Scatter( x = xLegend, y = yLegend, text = textLegend, textfont_size = textfont_sizeLegend, mode='text' )\n")

	f.write("\n\n\n")
	f.close()











########################################################################################################################
###	Create the information for each chromosome and each annotations
########################################################################################################################
def LignesAnnotations(temp) :

	f = open(temp, "a")

	# prepare the datastructure
	f.write("classChrom = [] \n")
	f.write("AxisInterval = [] \n")
	f.write("posGene = [] \n")
	f.write("posPseudo = [] \n")
	f.write("posNcRNA = [] \n")
	f.write("posAllTEs = [] \n")
	f.write("for i in range(0, len(SelectionNameID), 1) : \n")
	f.write("	AxisInterval.append([]) \n")
	f.write("	posGene.append([]) \n")
	f.write("	posPseudo.append([]) \n")
	f.write("	posNcRNA.append([]) \n")
	f.write("	posAllTEs.append([]) \n")
	f.write("	for j in range(0, 100, 1) : \n")
	f.write("		AxisInterval[i].append(0) \n")
	f.write("		posGene[i].append(0) \n")
	f.write("		posPseudo[i].append(0) \n")
	f.write("		posNcRNA[i].append(0) \n")
	f.write("		posAllTEs[i].append(0) \n\n")


	# fill the datastructure with data
	f.write("for i in range(0, len(SelectionNameID), 1) : \n")
	f.write("	classChrom.append( round(TailleChrom[i] / 100) + 1 )\n")
	f.write("	if TailleChrom[i] >= 10000000 : \n")
	f.write("		for j in range(0, 99, 1) : \n")
	f.write("			AxisInterval[i][j] = '[' + str((round(classChrom[i]/1000000)+1) * j) + 'M - ' + str((round(classChrom[i]/1000000)+1) * (j+1)) + 'M [' \n")
	f.write("		AxisInterval[i][99] = '[' + str((round(classChrom[i]/1000000)+1) * j) + 'M - ' + str((round(TailleChrom[i]/1000000)+1) ) + 'M ]' \n")
	f.write("	elif TailleChrom[i] >= 1000000 : \n")
	f.write("		for j in range(0, 99, 1) : \n")
	f.write("			AxisInterval[i][j] = '[' + str((round(classChrom[i]/1000)+1) * j) + 'k - ' + str((round(classChrom[i]/1000)+1) * (j+1)) + 'k [' \n")
	f.write("		AxisInterval[i][99] = '[' + str((round(classChrom[i]/1000)+1) * j) + 'k - ' + str((round(TailleChrom[i]/1000)+1) ) + 'k ]' \n")
	f.write("	else : \n")
	f.write("		for j in range(0, 99, 1) : \n")
	f.write("			AxisInterval[i][j] = '[' + str(classChrom[i] * j) + ' - ' + str(classChrom[i] * (j+1)) + '[' \n")
	f.write("		AxisInterval[i][99] = '[' + str(classChrom[i] * j) + ' - ' + str(TailleChrom[i]) + ' ]' \n")



	f.write("	Select_Gene = CommonDATA.dataFrame_Gene.loc[ (CommonDATA.dataFrame_Gene['Chr ID'] == SelectionNameID[i]), ['Start', 'End'] ] \n")
	f.write("	deb = Select_Gene['Start'].tolist() \n")
	f.write("	fin = Select_Gene['End'].tolist() \n")
	f.write("	for j in range(0, len(deb), 1) : \n")
	f.write("		posTemp = fin[j] = deb[j] \n")
	f.write("		interval = round(posTemp / classChrom[i]) \n")
	f.write("		if interval > 99 : \n")
	f.write("			interval = 99 \n")
	f.write("		posGene[i][interval] += 1 \n\n")

	f.write("	Select_Pseudo = CommonDATA.dataFrame_Pseudo.loc[ (CommonDATA.dataFrame_Pseudo['Chr ID'] == SelectionNameID[i]), ['Start', 'End'] ] \n")
	f.write("	deb = Select_Pseudo['Start'].tolist() \n")
	f.write("	fin = Select_Pseudo['End'].tolist() \n")
	f.write("	for j in range(0, len(deb), 1) : \n")
	f.write("		posTemp = fin[j] = deb[j] \n")
	f.write("		interval = round(posTemp / classChrom[i]) \n")
	f.write("		if interval > 99 : \n")
	f.write("			interval = 99 \n")
	f.write("		posPseudo[i][interval] += 1 \n\n")

	f.write("	Select_ncRNA = CommonDATA.dataFrame_ncRNA.loc[ (CommonDATA.dataFrame_ncRNA['Chr ID'] == SelectionNameID[i]), ['Start', 'End'] ] \n")
	f.write("	deb = Select_ncRNA['Start'].tolist() \n")
	f.write("	fin = Select_ncRNA['End'].tolist() \n")
	f.write("	for j in range(0, len(deb), 1) : \n")
	f.write("		posTemp = fin[j] = deb[j] \n")
	f.write("		interval = round(posTemp / classChrom[i]) \n")
	f.write("		if interval > 99 : \n")
	f.write("			interval = 99 \n")
	f.write("		posNcRNA[i][interval] += 1 \n\n")

	f.write("	Select_otherTE = CommonDATA.dataFrame_otherTE.loc[ (CommonDATA.dataFrame_otherTE['Chr ID'] == SelectionNameID[i]), ['Start', 'End'] ] \n")
	f.write("	deb = Select_otherTE['Start'].tolist() \n")
	f.write("	fin = Select_otherTE['End'].tolist() \n")
	f.write("	for j in range(0, len(deb), 1) : \n")
	f.write("		posTemp = fin[j] = deb[j] \n")
	f.write("		interval = round(posTemp / classChrom[i]) \n")
	f.write("		if interval > 99 : \n")
	f.write("			interval = 99 \n")
	f.write("		posAllTEs[i][interval] += 1 \n\n")


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
	f.write("			MaxConsensus = CommonDATA_SelectTEs.TailleConsensus[i] \n\n")

	f.write("\n\n\n")
	f.close()











########################################################################################################################
###	Create the graph and the layout that contains the chromosomes
########################################################################################################################
def CreateLayout(temp, dataFrame_Organism):

	SelectionName = dataFrame_Organism['Name'].tolist()

	f = open(temp, "a")
	# cree le layout qui va tout contenir
	f.write("########################################################################################################################\n")
	f.write("# Creation du Layout pour dash\n\n")
	f.write("GenomeBrowser_layout = html.Div([ \n")

	f.write("	html.Div([ \n")
	f.write("		html.Div(id='Onglet1_GenomeBrowser_Div'), \n\n")
	f.write("	], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n")



	f.write("	# ajout du combobox et du graphique pour chaque chromosome \n")
	f.write("	html.Div([ \n")

	f.write("		html.Div([ \n")
	f.write("			html.Div([ \n")
	f.write("				html.Label('Choose your sequence : ') \n")
	f.write("			], style={'width': '9%', 'vertical-align':'top', 'text-align':'center', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)'} ), \n\n")

	f.write("			html.Div([ \n")
	f.write("				# combolist \n")
	f.write("				dcc.Dropdown(\n")
	f.write("					id='SelectSequence_Onglet1', \n")
	f.write("					options=[ \n")
	for z in range(0, len(SelectionName), 1) :
		f.write("						{'label': '")
		f.write(SelectionName[z])
		f.write("', 'value': '")
		f.write(str(z))
		f.write("'}, \n")
	f.write("					], \n")
	f.write("					value='0', style={}, \n")
	f.write("					clearable=False, \n")
	f.write("				), \n")
	f.write("				html.Div(id='Onglet1_SelectSequence'), \n")
	f.write("			], style={'width': '90%', 'display': 'inline-block'} ), \n\n")
	f.write("		], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n")

	f.write("		html.Div([ \n")

	f.write("			html.Div([ \n")
	f.write("				html.Div([ \n")
	f.write("				], style={'width': '100%', 'height':50, 'display': 'inline-block', } ), \n")

	f.write("				html.Div([ \n")
	f.write("					dcc.Checklist( \n")
	f.write("						id='Checklist_Onglet1', \n")
	f.write("						options=[ \n")
	f.write("							{'label': 'TE superfamily', 	'value': 1}, \n")
	f.write("							{'label': 'All TEs', 		'value': 2}, \n")
	f.write("							{'label': 'Genes', 		'value': 3},  \n")
	f.write("							{'label': 'Pseudos', 		'value': 4},  \n")
	f.write("							{'label': 'ncRNAs', 		'value': 5},  \n")
	f.write("						], \n")
	f.write("						value=[], \n")
	f.write("						labelStyle={'display': 'block'}, \n")
	f.write("					), \n")
	f.write("				], style={'width': '100%', 'display': 'inline-block',} ), \n")

	f.write("				html.Div(id='Onglet1_ChecklistChrom_Div'), \n")
	f.write("			], style={'width': '10%', 'display': 'inline-block', 'vertical-align':'top'} ), \n\n")



	f.write("			html.Div([ \n")

	f.write("				html.Div(id='Onglet1_Chromosome_Div'), \n")
	f.write("			], style={'width': '89%', 'display': 'inline-block'} ), \n\n")

	f.write("		], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n")

	f.write("	], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)'} )\n")

	f.write("], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)'} )\n")
	f.write("\n\n\n\n")
	f.close()











########################################################################################################################
###	Create the TE bar inside the chromosome
########################################################################################################################
def CreateTEbar(temp, nbSeq_Assemble, numberTE) :

	# afficher les TE sur les chromosomes
	f = open(temp, "a")

	f.write("\t# Calcul pour les TEs \n")

	# 3 Case :
	# - Just 1 TE : make 1 line
	# - Merge TEs : make 1 line
	# - Many TEs : make a line for each TE

	if numberTE == 1 :
		f.write("\t# Here I make only 1 bar for 1 TE family or 1 Merged TE families \n")

		f.write("\tvarX = [] \n")
		f.write("\tvarY = [] \n")
		f.write("\tvarBase = [] \n")
		f.write("\tvarWidth = [] \n")
		f.write("\tvarText = [] \n")
		f.write("\tvarHover = [] \n")
		f.write("\tfor i in range(0, len(SelectionRefseq), 1) : \n")
		f.write("\t	varX.append([]) \n")
		f.write("\t	varY.append([]) \n")
		f.write("\t	varBase.append([]) \n")
		f.write("\t	varWidth.append([]) \n")
		f.write("\t	varText.append([]) \n")
		f.write("\t	varHover.append([]) \n")

		f.write("\tk = 0 \n")
		f.write("\tfor i in range(len(SelectionRefseq)-1, -1, -1) : \n")
		f.write("\t	Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ ")
		f.write("(CommonDATA_SelectTEs.dataFrame_MyTE['Chr Name'] == SelectionNameID[i])")
		f.write(" & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax)")
		f.write(" & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3])")
		f.write(", : ] \n")
		f.write("\t	debTE = Select_myTE['Start'].tolist() \n")
		f.write("\t	finTE = Select_myTE['End'].tolist() \n")
		f.write("\t	sensTE = Select_myTE['Sens'].tolist() \n")
		f.write("\t	nbHit = len(debTE) \n")

		f.write("\t	# Prepare les barres verticales des TEs \n")
		f.write("\t	previousDEB = 0 \n")
		f.write("\t	tempX = [] \n")
		f.write("\t	tempY = [] \n")
		f.write("\t	tempBase = [] \n")
		f.write("\t	tempWidth = [] \n")
		f.write("\t	tempText = [] \n")
		f.write("\t	tempHover = [] \n")
		f.write("\t	for j in range(0, nbHit, 1) : \n")
		f.write("\t		# recupere la taille en pixel de l'ET \n")
		f.write("\t		pixelD = round(int(debTE[j]) * CommonDATA.echelleFor1bp) + 100 \n")
		f.write("\t		pixelF = round(int(finTE[j]) * CommonDATA.echelleFor1bp) + 100 \n")
		f.write("\t		sizeTE = pixelF - pixelD \n")
		f.write("\t		if(sizeTE < 1): \n")
		f.write("\t			sizeTE = 1 \n")

		f.write("\t		# Cree une barre sur le graph que si elle est separe d'au moins 1 pixel de la precedent \n")
		f.write("\t		if(previousDEB != pixelD) : \n")
		f.write("\t			tempX.append( (str(pixelD) + ', ') ) \n")
		f.write("\t			tempY.append('50, ') \n")
		f.write("\t			tempBase.append( (str(75 * k + 75) + ', ') ) \n")
		f.write("\t			tempWidth.append(sizeTE) \n")
		f.write("\t			tempHover.append('<b>%{text}</b>') \n")
		f.write("\t			tempText.append( SelectionName[i] + \" : \" + str(debTE[j]) + \" - \" + str(finTE[j]) + \" (\" + sensTE[j] + \")\" ) \n")
		f.write("\t		else: \n")
		f.write("\t			tText = tempText[len(tempText)-1][:-3] \n")
		f.write("\t			tText += \"<br>\" + SelectionName[i] + \" : \" + str(debTE[j]) + \" - \" + str(finTE[j]) + \" (\" + sensTE[j] + \")\" \n")
		f.write("\t			tempText[len(tempText)-1] = tText \n")
		f.write("\t		previousDEB = pixelD \n")

		f.write("\t	varX[i] = tempX \n")
		f.write("\t	varY[i] = tempY \n")
		f.write("\t	varWidth[i] = tempWidth \n")
		f.write("\t	varBase[i] = tempBase \n")
		f.write("\t	varText[i] = tempText \n")
		f.write("\t	varHover[i] = tempHover \n")
		f.write("\t	k += 1 \n\n")

		f.write("\t# creation des barres de TE sur les chromosomes\n")
		for i in range(nbSeq_Assemble-1, -1, -1) :
			f.write("\tTEonChromosome_")
			f.write(str(i))
			f.write(" = go.Bar(x = varX[")
			f.write(str(i))
			f.write("], y = varY[")
			f.write(str(i))
			f.write("], base = varBase[")
			f.write(str(i))
			f.write("], width = varWidth[")
			f.write(str(i))
			f.write("], text = varText[")
			f.write(str(i))
			f.write("], hoverinfo = 'text', name = CommonDATA_SelectTEs.list_selection_TE[0], marker=dict(color = Couleur.couleurSelectTE[0]) ) \n")

	else :
		f.write("\t# Here I created a bar for each TE families \n")
		f.write("\tz = 0 \n")
		f.write("\tvarX = [[0 for x in range(len(CommonDATA_SelectTEs.list_selection_TE)+1)] for y in range(len(SelectionRefseq)+1)] \n")
		f.write("\tvarY = [[0 for x in range(len(CommonDATA_SelectTEs.list_selection_TE)+1)] for y in range(len(SelectionRefseq)+1)] \n")
		f.write("\tvarBase = [[0 for x in range(len(CommonDATA_SelectTEs.list_selection_TE)+1)] for y in range(len(SelectionRefseq)+1)] \n")
		f.write("\tvarWidth = [[0 for x in range(len(CommonDATA_SelectTEs.list_selection_TE)+1)] for y in range(len(SelectionRefseq)+1)] \n")
		f.write("\tvarText = [[0 for x in range(len(CommonDATA_SelectTEs.list_selection_TE)+1)] for y in range(len(SelectionRefseq)+1)] \n")
		f.write("\tvarHover = [[0 for x in range(len(CommonDATA_SelectTEs.list_selection_TE)+1)] for y in range(len(SelectionRefseq)+1)] \n")

		f.write("\tfor i in range(len(SelectionRefseq)-1, -1, -1) : \n")
		f.write("\t	for j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("\t		Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[")
		f.write("(CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[i]) & (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[j])")
		f.write(" & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax)")
		f.write(" & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3])")
		f.write(", : ] \n")
		f.write("\t		debTE = Select_myTE['Start'].tolist() \n")
		f.write("\t		finTE = Select_myTE['End'].tolist() \n")
		f.write("\t		sensTE = Select_myTE['Sens'].tolist() \n")
		f.write("\t		nbHit = len(debTE) \n")

		f.write("\t		# Prepare les barres verticales des TEs \n")
		f.write("\t		previousDEB = 0 \n")
		f.write("\t		tempX = [] \n")
		f.write("\t		tempY = [] \n")
		f.write("\t		tempBase = [] \n")
		f.write("\t		tempWidth = [] \n")
		f.write("\t		tempText = [] \n")
		f.write("\t		tempHover = [] \n")
		f.write("\t		for k in range(0, nbHit, 1) : \n")
		f.write("\t			# recupere la taille en pixel de l'ET \n")
		f.write("\t			pixelD = round(int(debTE[k]) * CommonDATA.echelleFor1bp) + 100 \n")
		f.write("\t			pixelF = round(int(finTE[k]) * CommonDATA.echelleFor1bp) + 100 \n")
		f.write("\t			sizeTE = pixelF - pixelD \n")
		f.write("\t			if(sizeTE < 1): \n")
		f.write("\t				sizeTE = 1 \n")

		f.write("\t			# Cree une barre sur le graph que si elle est separe d'au moins 1 pixel de la precedent \n")
		f.write("\t			if(previousDEB != pixelD) : \n")
		f.write("\t				tempX.append( (str(pixelD) + ', ') ) \n")
		f.write("\t				tempY.append('50, ') \n")
		f.write("\t				tempBase.append( (str(75 * z + 75) + ', ') ) \n")
		f.write("\t				tempWidth.append(sizeTE) \n")
		f.write("\t				tempHover.append('<b>%{text}</b>') \n")
		f.write("\t				tempText.append( SelectionName[i] + \" : \" + str(debTE[k]) + \" - \" + str(finTE[k]) + \" (\" + sensTE[k] + \")\" ) \n")
		f.write("\t			else: \n")
		f.write("\t				tText = tempText[len(tempText)-1][:-3] \n")
		f.write("\t				tText += \"<br>\" + SelectionName[i] + \" : \" + str(debTE[k]) + \" - \" + str(finTE[k]) + \" (\" + sensTE[k] + \")\" \n")
		f.write("\t				tempText[len(tempText)-1] = tText \n")
		f.write("\t			previousDEB = pixelD \n")

		f.write("\t		varX[i][j] = tempX \n")
		f.write("\t		varY[i][j] = tempY \n")
		f.write("\t		varWidth[i][j] = tempWidth \n")
		f.write("\t		varBase[i][j] = tempBase \n")
		f.write("\t		varText[i][j] = tempText \n")
		f.write("\t		varHover[i][j] = tempHover \n")
		f.write("\t	z += 1 \n\n")

		f.write("\t# creation des barres de TE sur les chromosomes\n")
		for i in range(nbSeq_Assemble-1, -1, -1) :
			for j in range(0, numberTE, 1) :
				f.write("\tTEonChromosome_" + str(i) + "_" + str(j) )
				f.write(" = go.Bar(")
				f.write("x = varX[" + str(i) + "][" + str(j) + "], ")
				f.write("y = varY[" + str(i) + "][" + str(j) + "], ")
				f.write("base = varBase[" + str(i) + "][" + str(j) + "], ")
				f.write("width = varWidth[" + str(i) + "][" + str(j) + "], ")
				f.write("text = varText[" + str(i) + "][" + str(j) + "], ")
				f.write("hoverinfo = 'text', name = CommonDATA_SelectTEs.list_selection_TE[" + str(j) + "], marker=dict(color = Couleur.couleurSelectTE[" + str(j) + "]) )\n")

	f.write('\n\n\n')
	f.close()











########################################################################################################################
###	Callback that will updates the global view of GenomeBrowser
########################################################################################################################
def CreateCallBack_Genome_Onglet1(temp, nbSeq_Assemble, numberTE) :

	f = open(temp, "a")

	f.write("########################################################################################################################\n")
	f.write("# ajout du callback\n\n")
	f.write("# marcher avec un multi input !! mais il faut que 1 seul output \n")
	f.write("@app.callback( \n")
	f.write("	Output('Onglet1_GenomeBrowser_Div', 'children'), \n")
	f.write("	[Input('memory', 'data')] \n")
	f.write(")\n\n")

	f.write("def update_Genome_Onglet1(valueSliders) : \n")
	f.write("\t# valueSliders[0] and valueSliders[1] are boundary for the size slider\n")
	f.write("\t# valueSliders[2] and valueSliders[3] are boundary for the similarity slider\n\n")

	f.write("\t# get the total of all TE for each chromosome and in genome \n")
	f.write("\t# get the total of the same superfamily TE for each chromosome and in genome \n")
	f.write("\t# get the percentage for each chromosome and in genome \n")
	f.write("\ttailleMin = 0 \n")
	f.write("\tif valueSliders[0] == 1 : \n")
	f.write("\t\ttailleMin = 0 \n")
	f.write("\telse : \n")
	f.write("\t\ttailleMin = MinConsensus * valueSliders[0] / 100 \n")
	f.write("\ttailleMax = 0 \n")
	f.write("\tif valueSliders[1] == 100 : \n")
	f.write("\t\ttailleMax = 10 * MaxConsensus \n")
	f.write("\telse : \n")
	f.write("\t\ttailleMax = MaxConsensus * valueSliders[1] / 100 \n\n")
	f.close()



	# Create the bar that represented the chromosome
	CreateTEbar(temp, nbSeq_Assemble, numberTE)



	# j'ecris ici le graphe du chromosome
	f = open(temp, "a")
	f.write("\thauteurFig = CommonDATA.nbSeq_Assemble * 75 + 125 \n")

	f.write("\tOnglet1Genome = html.Div([ \n\n")

	f.write("\t	# affiche le graphe GenomeBrowser\n")
	f.write("\t	dcc.Graph(\n")
	f.write("\t		id='Graph_Genome_Onglet1',\n")
	f.write("\t		figure={\n")
	f.write("\t			'data': [LegendeChromosome, \n")

	# ici il faut ajouter les donnees pour TEs
	if numberTE == 1 :
		f.write("\t				")
		for i in range(nbSeq_Assemble-1, -1, -1) :
			f.write("TEonChromosome_" + str(i) + ', ')
		f.write("\n")
	else :
		for i in range(nbSeq_Assemble-1, -1, -1) :
			f.write("\t				")
			for j in range(0, numberTE, 1) :
				f.write("TEonChromosome_" + str(i) + "_" + str(j) + ', ')
			f.write("\n")
	f.write("\n")

	f.write("\t			],\n")
	f.write("\t			'layout': {\n")
	f.write("\t				# titre du graphique\n")
	f.write("\t				'title': CommonDATA_SelectTEs.OfficialName + ' Distribution in ' + CommonDATA.nameOrganism , \n")
	f.write("\t				'legend':{'orientation':'h'}, \n")
	f.write("\t				# modification de l'axes des abscisses\n")
	f.write("\t				'xaxis':{'showgrid':False, 'zeroline':False, 'showticklabels':False},\n")
	f.write("\t				'yaxis':{'showgrid':False, 'zeroline':False, 'showticklabels':False}, \n")
	f.write("\t				'render_mode':'webgl',\n")

	# ici mettre des shapes (rectangle) pour les chromosomes
	f.write("\t				'shapes':[\n")
	k = 0
	for i in range(nbSeq_Assemble-1, -1, -1) :
		hauteur1 = str(75 * k + 75)
		hauteur2 = str(75 * k + 125)
		k += 1
		f.write("\t					dict({ 'type': 'rect', 'x0':100, 'y0':")	# la valeur 100 permet d'ecrire devant le chromosome
		f.write(hauteur1)
		f.write(", 'x1': round( CommonDATA.TailleSequence[")
		f.write(str(i))
		f.write("] * CommonDATA.echelleFor1bp + 100 ) ")
		f.write(", 'y1':")
		f.write(hauteur2)
		f.write(", 'line': { 'width': 1, 'color': 'black' }, 'fillcolor':'darkgrey', 'opacity':0.5, 'layer':'below', }),\n")
	f.write("\t				],\n")
	f.write("\t			},\n")
	f.write("\t		},\n")

	f.write("\t		config={\n")
	f.write("\t			# affiche constamment la barre de manipulation\n")
	f.write("\t			'displayModeBar': True, \n")
	f.write("\t			# la molette de la souris permet de faire des zooms\n")
	f.write("\t			'scrollZoom': True,\n")
	f.write("\t		},\n")
	f.write("\t		style={\n")
	f.write("\t			# met un scroll sur la barre des X et Y !\n")
	f.write("\t			'overflowX': 'scroll',\n")
	f.write("\t			'overflowY': 'scroll',\n")
	f.write("\t			#determine la taille du graph\n")
	f.write("\t			'height': hauteurFig, 'width': 1850+100 \n")
	f.write("\t		},\n")
	f.write("\t	),\n\n")

	f.write("\t], style={'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'}),\n\n")
	f.write("\treturn Onglet1Genome \n\n\n\n")
	f.close()











########################################################################################################################
###	Create the lines based on widget
########################################################################################################################
def UpdateLine_Chrom(temp, numberTE) :

	f = open(temp, "a")

	if numberTE == 1 :
		f.write("\tpos_myTE = [] \n")
		f.write("\tfor k in range(0, 100, 1) : \n")
		f.write("\t	pos_myTE.append(0) \n\n")

		f.write("\tSelect_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr Name'] == SelectionNameID[indiceCHR]) ")
		f.write("& (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3]) ")
		f.write("& (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax), ")
		f.write("['Start', 'End'] ] \n")
		f.write("\tdeb = Select_myTE['Start'].tolist() \n")
		f.write("\tfin = Select_myTE['End'].tolist() \n")
		f.write("\tfor j in range(0, len(deb), 1) : \n")
		f.write("\t	posTemp = fin[j] = deb[j] \n")
		f.write("\t	interval = round(posTemp / classChrom[indiceCHR]) \n")
		f.write("\t	if interval > 99 : \n")
		f.write("\t		interval = 99 \n")
		f.write("\t	pos_myTE[interval] += 1 \n\n")

	else :
		f.write("\tpos_myTE = [] \n")
		f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("\t	pos_myTE.append([]) \n")
		f.write("\t	for k in range(0, 100, 1) : \n")
		f.write("\t		pos_myTE[j].append(0) \n\n")

		f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("\t	Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr Name'] == SelectionNameID[indiceCHR]) & (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[j]) ")
		f.write("& (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3]) ")
		f.write("& (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax), ")
		f.write("['Start', 'End'] ] \n")
		f.write("\t	deb = Select_myTE['Start'].tolist() \n")
		f.write("\t	fin = Select_myTE['End'].tolist() \n")
		f.write("\t	for k in range(0, len(deb), 1) : \n")
		f.write("\t		posTemp = fin[k] = deb[k] \n")
		f.write("\t		interval = round(posTemp / classChrom[indiceCHR]) \n")
		f.write("\t		if interval > 99 : \n")
		f.write("\t			interval = 99 \n")
		f.write("\t		pos_myTE[j][interval] += 1 \n\n")


	f.write("\tpos_SuperTE = [] \n")
	f.write("\tfor j in range(0, 100, 1) : \n")
	f.write("\t	pos_SuperTE.append(0) \n\n")

	f.write("\tSelect_superTE = CommonDATA_SelectTEs.dataFrame_superTE.loc[ (CommonDATA_SelectTEs.dataFrame_superTE['Chr ID'] == SelectionNameID[indiceCHR]) ")
	f.write("& (CommonDATA_SelectTEs.dataFrame_superTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_superTE['Similarity'] <= valueSliders[3]) ")
	f.write("& (CommonDATA_SelectTEs.dataFrame_superTE['Size'] >= tailleMin_otherTE) & (CommonDATA_SelectTEs.dataFrame_superTE['Size'] <= tailleMax_otherTE), ")
	f.write("['Start', 'End'] ] \n")
	f.write("\tdeb = Select_superTE['Start'].tolist() \n")
	f.write("\tfin = Select_superTE['End'].tolist() \n")
	f.write("\tfor k in range(0, len(deb), 1) : \n")
	f.write("\t	posTemp = fin[k] = deb[k] \n")
	f.write("\t	interval = round(posTemp / classChrom[indiceCHR]) \n")
	f.write("\t	if interval > 99 : \n")
	f.write("\t		interval = 99 \n")
	f.write("\t	pos_SuperTE[interval] += 1 \n\n")



	if numberTE == 1 :
		f.write("\tchromLine_SelectedTEs = go.Scatter( x = AxisInterval[indiceCHR], y = pos_myTE, name = CommonDATA_SelectTEs.list_selection_TE[0], line = dict(color=Couleur.couleurSelectTE[0], width=3, dash='dash', shape='spline') ) \n")
	else :
		for j in range(0, numberTE, 1) :
			f.write("\tchromLine_SelectedTEs_" + str(j) + " = go.Scatter( x = AxisInterval[indiceCHR], y = pos_myTE[" + str(j) + "], name = CommonDATA_SelectTEs.list_selection_TE[" + str(j) + "], line = dict(color=Couleur.couleurSelectTE[" + str(j) + "], width=3, dash='dash', shape='spline') ) \n")

	f.write("\tchromLine_ncRNA = go.Scatter( x = AxisInterval[indiceCHR], y = [], name = 'ncRNAs', line = dict(color=Couleur.couleurV2[25], width=2) ) \n")
	f.write("\tchromLine_Pseudo = go.Scatter( x = AxisInterval[indiceCHR], y = [], name = 'Pseudos', line = dict(color=Couleur.couleurV2[24], width=2) ) \n")
	f.write("\tchromLine_Gene = go.Scatter( x = AxisInterval[indiceCHR], y = [], name = 'Genes', line = dict(color=Couleur.couleurV2[23], width=2) ) \n")
	f.write("\tchromLine_AllTEs = go.Scatter( x = AxisInterval[indiceCHR], y = [], name = 'All TEs', line = dict(color='black', width=2) ) \n")
	f.write("\tchromLine_SuperTE = go.Scatter( x = AxisInterval[indiceCHR], y = [], name = 'SuperFamily TE', line = dict(color=CommonDATA_SelectTEs.CouleurSuperTE, width=2) ) \n")

	f.write("\tfor k in range(0, len(Checklist_Onglet1), 1) : \n")
	f.write("\t	if Checklist_Onglet1[k] == 1 : \n")
	f.write("\t		chromLine_SuperTE = go.Scatter( x = AxisInterval[indiceCHR], y = pos_SuperTE, name = 'SuperFamily TE', line = dict(color=CommonDATA_SelectTEs.CouleurSuperTE, width=2, dash='dash', shape='spline'), yaxis='y2' ) \n")
	f.write("\t	elif Checklist_Onglet1[k] == 2 : \n")
	f.write("\t		chromLine_AllTEs = go.Scatter( x = AxisInterval[indiceCHR], y = posAllTEs[indiceCHR], name = 'All TEs', line = dict(color='black', width=2, shape='spline'), yaxis='y3' ) \n")
	f.write("\t	elif Checklist_Onglet1[k] == 3 : \n")
	f.write("\t		chromLine_Gene = go.Scatter( x = AxisInterval[indiceCHR], y = posGene[indiceCHR], name = 'Genes', line = dict(color=Couleur.couleurV2[23], width=2, dash='dot', shape='spline'), yaxis='y4' ) \n")
	f.write("\t	elif Checklist_Onglet1[k] == 4 : \n")
	f.write("\t		chromLine_Pseudo = go.Scatter( x = AxisInterval[indiceCHR], y = posPseudo[indiceCHR], name = 'Pseudos', line = dict(color=Couleur.couleurV2[24], width=2, dash='dot', shape='spline'), yaxis='y5' ) \n")
	f.write("\t	elif Checklist_Onglet1[k] == 5 : \n")
	f.write("\t		chromLine_ncRNA = go.Scatter( x = AxisInterval[indiceCHR], y = posNcRNA[indiceCHR], name = 'ncRNAs', line = dict(color=Couleur.couleurV2[25], width=2, dash='dot', shape='spline'), yaxis='y6' ) \n")

	f.write("\n\n")
	f.close()











########################################################################################################################
###	Callback that will updates all the page and the graph inside
########################################################################################################################
def CreatedCallBack_LineChromosome_Onglet1(temp, numberTE) :

	f = open(temp, "a")

	f.write("########################################################################################################################\n")
	f.write("# ajout du callback\n\n")
	f.write("# marcher avec un multi input !! mais il faut que 1 seul output \n")
	f.write("@app.callback( \n")
	f.write("	Output('Onglet1_Chromosome_Div', 'children'), \n")
	f.write("	[Input('memory', 'data'), Input('Checklist_Onglet1', 'value'), Input('SelectSequence_Onglet1', 'value') ] \n")
	f.write(")\n\n")

	f.write("def update_Chromosome_Onglet1(valueSliders, Checklist_Onglet1, SelectSequence_Onglet1) : \n")
	f.write("\t# valueSliders[0] and valueSliders[1] are boundary for the size slider\n")
	f.write("\t# valueSliders[2] and valueSliders[3] are boundary for the similarity slider\n\n")

	f.write("\t# Calcul pour les TEs \n")
	# prise en compte d'1 ou plusieurs familles de TEs
	f.write("\ttailleMinOther = CommonDATA_SelectTEs.dataFrame_superTE['Size'].min() \n")
	f.write("\ttailleMaxOther = CommonDATA_SelectTEs.dataFrame_superTE['Size'].max() \n")
	f.write("\ttailleMin = 0 \n")
	f.write("\tif valueSliders[0] == 1 : \n")
	f.write("\t\ttailleMin = 0 \n")
	f.write("\telse : \n")
	f.write("\t\ttailleMin = MinConsensus * valueSliders[0] / 100 \n")
	f.write("\ttailleMax = 0 \n")
	f.write("\tif valueSliders[1] == 100 : \n")
	f.write("\t\ttailleMax = 10 * MaxConsensus \n")
	f.write("\telse : \n")
	f.write("\t\ttailleMax = MaxConsensus * valueSliders[1] / 100 \n\n")

	f.write("\ttailleMin_otherTE = 0 \n")
	f.write("\tif valueSliders[0] == 1 : \n")
	f.write("\t\ttailleMin_otherTE = tailleMinOther - 1 \n")
	f.write("\telse : \n")
	f.write("\t\ttailleMin_otherTE = tailleMaxOther * valueSliders[0] / 100 \n")
	f.write("\ttailleMax_otherTE = 0 \n")
	f.write("\tif valueSliders[1] == 100 : \n")
	f.write("\t\ttailleMax_otherTE = 10 * tailleMaxOther \n")
	f.write("\telse : \n")
	f.write("\t\ttailleMax_otherTE = tailleMaxOther * valueSliders[1] / 100 \n\n")

	f.write("\tindiceCHR = int(SelectSequence_Onglet1) \n\n\n")

	f.close()



	# Create or update lines chromosomes based on sliders
	UpdateLine_Chrom(temp, numberTE)



	f = open(temp, "a")
	f.write("\tOnglet1CHR = html.Div([ \n\n")

	f.write("\t	# affiche le graphe GenomeBrowser\n")
	f.write("\t	dcc.Graph(\n")
	f.write("\t		id = 'LinesChart_Onglet1',\n")
	f.write("\t		figure={ \n")
	f.write("\t			'data' : [chromLine_ncRNA, chromLine_Pseudo, chromLine_Gene, chromLine_AllTEs, chromLine_SuperTE, ")
	if numberTE == 1 :
		f.write("chromLine_SelectedTEs, ")
	else :
		for j in range(0, numberTE, 1) :
			f.write("chromLine_SelectedTEs_" + str(j) + ", ")
	f.write("], \n")
	f.write("\t			'layout' : { \n")
	f.write("\t				'title':'Annotations and TEs Distribution in chromosome', \n")
	f.write("\t				'plot_bgcolor':'rgba(255,255,255,1)', \n")
	f.write("\t				'legend':{'orientation':'h'}, \n")
	f.write("\t				'xaxis':dict( domain=[0, 0.91] ), \n")
	f.write("\t				'yaxis1':dict( \n")
	f.write("\t				title='TE Number by Interval', \n")
	if numberTE == 1 :
		f.write("\t					titlefont=dict(color=Couleur.couleurSelectTE[0]), \n")
		f.write("\t					tickfont=dict(color=Couleur.couleurSelectTE[0]) \n")
	else :
		f.write("\t					titlefont=dict(color='black'), \n")
		f.write("\t					tickfont=dict(color='black') \n")
	f.write("\t					), \n")

	f.write("\t				'yaxis2':dict( \n")
	f.write("\t					titlefont=dict(color=CommonDATA_SelectTEs.CouleurSuperTE), \n")
	f.write("\t					tickfont=dict(color=CommonDATA_SelectTEs.CouleurSuperTE), \n")
	f.write("\t					anchor='x', \n")
	f.write("\t					overlaying='y', \n")
	f.write("\t					side='right', \n")
	f.write("\t				), \n")

	f.write("\t				'yaxis3':dict( \n")
	f.write("\t					titlefont=dict(color='black'), \n")
	f.write("\t					tickfont=dict(color='black'), \n")
	f.write("\t					anchor='free', \n")
	f.write("\t					overlaying='y', \n")
	f.write("\t					side='right', \n")
	f.write("\t					position = 0.93, \n")
	f.write("\t				), \n")

	f.write("\t				'yaxis4':dict( \n")
	f.write("\t					titlefont=dict(color=Couleur.couleurV2[23]), \n")
	f.write("\t					tickfont=dict(color=Couleur.couleurV2[23]), \n")
	f.write("\t					anchor='free', \n")
	f.write("\t					overlaying='y', \n")
	f.write("\t					side='right', \n")
	f.write("\t					position = 0.95, \n")
	f.write("\t				), \n")

	f.write("\t				'yaxis5':dict( \n")
	f.write("\t					titlefont=dict(color=Couleur.couleurV2[24]), \n")
	f.write("\t					tickfont=dict(color=Couleur.couleurV2[24]), \n")
	f.write("\t					anchor='free', \n")
	f.write("\t					overlaying='y', \n")
	f.write("\t					side='right', \n")
	f.write("\t					position = 0.97, \n")
	f.write("\t				), \n")

	f.write("\t				'yaxis6':dict( \n")
	f.write("\t					titlefont=dict(color=Couleur.couleurV2[25]), \n")
	f.write("\t					tickfont=dict(color=Couleur.couleurV2[25]), \n")
	f.write("\t					anchor='free', \n")
	f.write("\t					overlaying='y', \n")
	f.write("\t					side='right', \n")
	f.write("\t					position = 0.99, \n")
	f.write("\t				), \n")

	f.write("\t			}, \n")
	f.write("\t		}, \n")
	f.write("\t		style={'overflowX':'scroll', 'overflowY':'scroll', 'height':650}, \n")
	f.write("\t		config={\n")
	f.write("\t			# affiche constamment la barre de manipulation\n")
	f.write("\t			'displayModeBar': True, \n")
	f.write("\t			# la molette de la souris permet de faire des zooms\n")
	f.write("\t			'scrollZoom': True,\n")
	f.write("\t		},\n")
	f.write("\t	),\n")

	f.write("\t], style={'overflowX':'scroll', 'overflowY':'scroll', 'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'}),\n\n")
	f.write("\treturn Onglet1CHR \n\n\n\n")
	f.close()









########################################################################################################################
###	Create the GenomeBrowser function
########################################################################################################################
def GenomeBrowser(pathVisual, pathVisualNEW, nbSeq_Assemble, numberTE):

	# Ajout des librairies python pour le serveur
	temp = pathVisualNEW + '/Functions/GenomeBrowser.py'
	f = open(temp, "w")

	f.write("#!/usr/bin/env python3\n")
	f.write("# -*- coding: utf-8 -*-\n")
	f.write("import dash\n")
	f.write("import dash_daq as daq\n")
	f.write("import dash_core_components as dcc\n")
	f.write("import dash_html_components as html\n")
	f.write("import plotly.graph_objects as go\n")
	f.write("import pandas as pd \n")
	f.write("from dash.dependencies import Input, Output\n")
	f.write("from app import app \n")
	f.close()
	with open(temp, "a") as file:
		file.write("""
from Scripts.Interface_Main_Dash import pathVisual#########
import importlib
Couleur_raw = pathVisual+"/second_half/Functions/Couleur"####

Couleur_processed = Couleur_raw.replace("/",".")#####
# The file gets executed upon import, as expected.
Couleur = importlib.import_module(Couleur_processed)#####

CommonDATA_SelectTEs_raw = pathVisual+"/second_half/Functions/CommonDATA_SelectTEs"####

CommonDATA_SelectTEs_processed = CommonDATA_SelectTEs_raw.replace("/",".")#####
# The file gets executed upon import, as expected.
CommonDATA_SelectTEs = importlib.import_module(CommonDATA_SelectTEs_processed)#####

CommonDATA_raw = pathVisual+"/second_half/Functions/CommonDATA"####

CommonDATA_processed = CommonDATA_raw.replace("/",".")#####
# The file gets executed upon import, as expected.
CommonDATA = importlib.import_module(CommonDATA_processed)#####


""")
	f = open(temp, "a")
	f.write("########################################################################################################################\n")
	f.write("# Data that does not change with the sliders \n\n")





	# get the data for the organism
	tempFile = pathVisual + '/Downloaded/DATA_Organism.txt'
	dataT = pd.read_csv(tempFile)
	# Create first a sud-dataframe that contains only the wanted values
	dataFrame_Organism = dataT.loc[(dataT['Size bp'] > 0)]

	# Ajout les donnees pour le genome
	InformationGenome(temp)
	# Ajout du texte avant les chromosomes
	LegendeChrom(temp)
	# Ajout des donnees annotations pour les lignes
	LignesAnnotations(temp)

	# Cree le div qui va contenir les graphes et tableaux
	CreateLayout(temp, dataFrame_Organism)



	# Cree ici le graphique genome en fonction du slider
	CreateCallBack_Genome_Onglet1(temp, nbSeq_Assemble, numberTE)
	# Cree ici le graphique pour chaque chromosome
	CreatedCallBack_LineChromosome_Onglet1(temp, numberTE)
