#!/usr/bin/python3
import os
import sys
import pandas as pd
import plotly.graph_objs as go





########################################################################################################################
###	Create the line graph for ALL TE that do not change with the slider, like x-axis
########################################################################################################################
def NonUpdatedVariable_Onglet3(temp, numberTE) :

	f = open(temp, "a")

	f.write("tailleMinOther = CommonDATA_SelectTEs.dataFrame_superTE['Size'].min() \n")
	f.write("tailleMaxOther = CommonDATA_SelectTEs.dataFrame_superTE['Size'].max() \n")
	# prise en compte d'1 ou plusieurs familles de TEs
	f.write("MinConsensus = 1000000 \n")
	f.write("MaxConsensus = 0 \n")
	f.write("if len(CommonDATA_SelectTEs.list_selection_TE) == 1 : \n" )
	f.write("	MinConsensus = CommonDATA_SelectTEs.TailleConsensus[0] \n")
	f.write("	MaxConsensus = CommonDATA_SelectTEs.TailleConsensus[0] \n")
	f.write("else : \n")
	f.write("	for i in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write(" 		if MinConsensus > CommonDATA_SelectTEs.TailleConsensus[i] : \n")
	f.write(" 			MinConsensus = CommonDATA_SelectTEs.TailleConsensus[i] \n")
	f.write(" 		if MaxConsensus < CommonDATA_SelectTEs.TailleConsensus[i] : \n")
	f.write(" 			MaxConsensus = CommonDATA_SelectTEs.TailleConsensus[i] \n")


	# la definition de classe de taille doit etre fixe : plus visuelle que modifiable
	f.write("# Definition of size and similarity classes cannot be non updated, this is more visual \n")
	f.write("SelectionRefseq = CommonDATA.dataFrame_Organism['RefSeq'].tolist() \n")
	f.write("SelectionName = CommonDATA.dataFrame_Organism['Name'].tolist() \n")
	f.write("SelectionNameID = CommonDATA.dataFrame_Organism['NameID'].tolist() \n")
	f.write("AxisSim = [] \n")
	f.write("for k in range(0, 50, 1): \n")
	f.write("	AxisSim.append(\'[' + str(50+k) + ' - ' + str(50+k+1) + '[\') \n\n")

	if numberTE == 1 :
		f.write("genome_maxSize = [] \n")
		f.write("genome_sizeClass = [] \n")
		f.write("AxisSize = [] \n")
		f.write("otherTE_Size_Class = [] \n")
		f.write("otherTE_Sim_Class = [] \n")
		f.write("for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("	Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[a]), ['Size'] ] \n")
		f.write("	Selection_Size_myTE = Select_myTE['Size'].tolist() \n")
		f.write("	tempMaxSize = 0 \n")
		f.write("	for j in range(0, len(Selection_Size_myTE), 1) : \n")
		f.write("		if tempMaxSize < Selection_Size_myTE[j] : \n")
		f.write("			tempMaxSize = Selection_Size_myTE[j] \n")
		f.write("	genome_maxSize.append(tempMaxSize) \n")
		f.write("	# get the category size for the genome \n")
		f.write("	genome_sizeClass.append( round(tempMaxSize / 20) + 1) \n\n")

		f.write("tempMaxSize = 0 \n")
		f.write("for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("	if(genome_sizeClass[a] < 10): \n")
		f.write("		genome_sizeClass[a] = 10 \n")
		f.write("	if(genome_sizeClass[a] > 1000): \n")
		f.write("		genome_sizeClass[a] = 1000 \n")
		f.write("	if tempMaxSize < genome_maxSize[a] : \n")
		f.write("		tempMaxSize = genome_maxSize[a] \n")
		f.write("genome_sizeClass.append( round(tempMaxSize / 20) + 1) \n")
		f.write("if(genome_sizeClass[len(SelectionRefseq)] < 10): \n")
		f.write("	genome_sizeClass[len(SelectionRefseq)] = 10 \n")
		f.write("if(genome_sizeClass[len(SelectionRefseq)] > 1000): \n")
		f.write("	genome_sizeClass[len(SelectionRefseq)] = 1000 \n\n")

		f.write("for a in range(0, len(SelectionRefseq)+1, 1) : \n")
		f.write("	tt = [] \n")
		f.write("	for k in range(0, 20, 1): \n")
		f.write("		tt.append(\'[' + str(genome_sizeClass[a]*k) + ' - ' + str(genome_sizeClass[a]*(k+1)) + '[\') \n")
		f.write("	AxisSize.append(tt) \n")
		f.write("	tt.append(\'[' + str(genome_sizeClass[a]*19) + ' - +∞ [\') \n")
		f.write("	AxisSize.append(tt) \n\n")

		f.write("for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("	Select_otherTE = CommonDATA.dataFrame_otherTE.loc[ (CommonDATA.dataFrame_otherTE['Chr ID'] == SelectionNameID[a]), ['Size'] ] \n")
		f.write("	Selection_Size_otherTE = Select_otherTE['Size'].tolist() \n")
		f.write("	# get the data for the chromosome for the curve for all TEs \n")
		f.write("	tempClass = [] \n")
		f.write("	for k in range(0, 50, 1): \n")
		f.write("		tempClass.append(0) \n")
		f.write("	for j in range(0, len(Selection_Size_otherTE), 1) : \n")
		f.write("		classe = round(Selection_Size_otherTE[j] / genome_sizeClass[a]) \n")
		f.write("		if(classe > 19): \n")
		f.write("			classe = 19 \n")
		f.write("		tempClass[classe] += 1 \n")
		f.write("	otherTE_Size_Class.append(tempClass) \n")
		f.write("tempClass = [] \n")
		f.write("for k in range(0, 50, 1): \n")
		f.write("	tempClass.append(0) \n")
		f.write("	for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("		tempClass[k] += otherTE_Size_Class[a][k] \n")
		f.write("	otherTE_Size_Class.append(tempClass) \n\n")

		f.write("for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("	Select_otherTE = CommonDATA.dataFrame_otherTE.loc[ (CommonDATA.dataFrame_otherTE['Chr ID'] == SelectionNameID[a]), ['Similarity'] ] \n")
		f.write("	Selection_Sim_otherTE = Select_otherTE['Similarity'].tolist() \n")
		f.write("	# get the data for the chromosome for the curve for all TEs \n")
		f.write("	tempClass = [] \n")
		f.write("	for k in range(0, 50, 1): \n")
		f.write("		tempClass.append(0) \n")
		f.write("	for j in range(0, len(Selection_Sim_otherTE), 1) : \n")
		f.write("		classe = round(Selection_Sim_otherTE[j]) - 50 \n")
		f.write("		if(classe > 49): \n")
		f.write("			classe = 49 \n")
		f.write("		tempClass[classe] += 1 \n")
		f.write("	otherTE_Sim_Class.append(tempClass) \n")
		f.write("tempClass = [] \n")
		f.write("for k in range(0, 50, 1): \n")
		f.write("	tempClass.append(0) \n")
		f.write("	for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("		tempClass[k] += otherTE_Sim_Class[a][k] \n")
		f.write("	otherTE_Sim_Class.append(tempClass) \n\n")

	else :
		f.write("genome_maxSize = [] \n")
		f.write("genome_sizeClass = [] \n")
		f.write("AxisSize = [] \n")
		f.write("otherTE_Size_Class = [] \n")
		f.write("otherTE_Sim_Class = [] \n")
		f.write("for j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("	tempMaxSize = [] \n")
		f.write("	genome_maxSize.append([]) \n")
		f.write("	genome_sizeClass.append([]) \n")
		f.write("	for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("		Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA.dataFrame_otherTE['Chr ID'] == SelectionNameID[a]) & (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[j]) , ['Size'] ] \n")
		f.write("		Selection_Size_myTE = Select_myTE['Size'].tolist() \n")
		f.write("		tempMaxSize.append(0) \n")
		f.write("		for k in range(0, len(Selection_Size_myTE), 1) : \n")
		f.write("			if tempMaxSize[a] < Selection_Size_myTE[k] : \n")
		f.write("				tempMaxSize[a] = Selection_Size_myTE[k] \n")
		f.write("		genome_maxSize[j].append(tempMaxSize[a]) \n")
		f.write("		# get the category size for the genome \n")
		f.write("		genome_sizeClass[j].append( round(tempMaxSize[a] / 20) + 1) \n")

		f.write("	tempMaxSize[j] = 0 \n")
		f.write("	for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("		if(genome_sizeClass[j][a] < 10): \n")
		f.write("			genome_sizeClass[j][a] = 10 \n")
		f.write("		if(genome_sizeClass[j][a] > 1000): \n")
		f.write("			genome_sizeClass[j][a] = 1000 \n")
		f.write("		if tempMaxSize[j] < genome_maxSize[j][a] : \n")
		f.write("			tempMaxSize[j] = genome_maxSize[j][a] \n")
		f.write("	genome_sizeClass[j].append( round(tempMaxSize[j] / 20) + 1) \n")
		f.write("	if(genome_sizeClass[j][len(SelectionRefseq)] < 10): \n")
		f.write("		genome_sizeClass[j][len(SelectionRefseq)] = 10 \n")
		f.write("	if(genome_sizeClass[j][len(SelectionRefseq)] > 1000): \n")
		f.write("		genome_sizeClass[j][len(SelectionRefseq)] = 1000 \n")

		f.write("# Selection of the smallest Axis \n")
		f.write("Average_sizeClass = [] \n")
		f.write("for a in range(0, len(SelectionRefseq)+1, 1) : \n")
		f.write("	minAxis = 10000000 \n")
		f.write("	for j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("		if minAxis > genome_sizeClass[j][a] : \n")
		f.write("			minAxis = genome_sizeClass[j][a] \n")
		f.write("	tt = [] \n")
		f.write("	for k in range(0, 20, 1): \n")
		f.write("		tt.append(\'[' + str(minAxis*k) + ' - ' + str(minAxis*(k+1)) + '[\') \n")
		f.write("	Average_sizeClass.append(minAxis) \n")
		f.write("	AxisSize.append(tt) \n")
		f.write("	tt.append(\'[' + str(minAxis*19) + ' - +∞ [\') \n")
		f.write("	AxisSize.append(tt) \n\n")

		f.write("for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("	Select_otherTE = CommonDATA.dataFrame_otherTE.loc[ (CommonDATA.dataFrame_otherTE['Chr ID'] == SelectionNameID[a]), ['Size'] ] \n")
		f.write("	Selection_Size_otherTE = Select_otherTE['Size'].tolist() \n")
		f.write("	# get the data for the chromosome for the curve for all TEs \n")
		f.write("	tempClass = [] \n")
		f.write("	for k in range(0, 50, 1): \n")
		f.write("		tempClass.append(0) \n")
		f.write("	for j in range(0, len(Selection_Size_otherTE), 1) : \n")
		f.write("		classe = round(Selection_Size_otherTE[j] / Average_sizeClass[a]) \n")
		f.write("		if(classe > 19): \n")
		f.write("			classe = 19 \n")
		f.write("		tempClass[classe] += 1 \n")
		f.write("	otherTE_Size_Class.append(tempClass) \n")
		f.write("tempClass = [] \n")
		f.write("for k in range(0, 50, 1): \n")
		f.write("	tempClass.append(0) \n")
		f.write("	for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("		tempClass[k] += otherTE_Size_Class[a][k] \n")
		f.write("	otherTE_Size_Class.append(tempClass) \n\n")

		f.write("for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("	Select_otherTE = CommonDATA.dataFrame_otherTE.loc[ (CommonDATA.dataFrame_otherTE['Chr ID'] == SelectionNameID[a]), ['Similarity'] ] \n")
		f.write("	Selection_Sim_otherTE = Select_otherTE['Similarity'].tolist() \n")
		f.write("	# get the data for the chromosome for the curve for all TEs \n")
		f.write("	tempClass = [] \n")
		f.write("	for k in range(0, 50, 1): \n")
		f.write("		tempClass.append(0) \n")
		f.write("	for j in range(0, len(Selection_Sim_otherTE), 1) : \n")
		f.write("		classe = round(Selection_Sim_otherTE[j]) - 50 \n")
		f.write("		if(classe > 49): \n")
		f.write("			classe = 49 \n")
		f.write("		tempClass[classe] += 1 \n")
		f.write("	otherTE_Sim_Class.append(tempClass) \n")
		f.write("tempClass = [] \n")
		f.write("for k in range(0, 50, 1): \n")
		f.write("	tempClass.append(0) \n")
		f.write("	for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("		tempClass[k] += otherTE_Sim_Class[a][k] \n")
		f.write("	otherTE_Sim_Class.append(tempClass) \n\n")

	f.write("\n\n")
	f.close()










########################################################################################################################
###	Create the Layout
########################################################################################################################
def CreateLayoutGeneralFeatures(temp, dataFrame_Organism) :

	SelectionName = dataFrame_Organism['Name'].tolist()

	f = open(temp, "a")
	f.write("########################################################################################################################\n")
	f.write("# ajout des commandes de dash\n\n")
	f.write("# ajout du combo list pour choisir le chromosome ou le genome \n")
	f.write("GeneralFeatures_layout = html.Div([\n")

	f.write("\t# ajout du combobox et du graphique plotly montrant les tailles des TEs sur les chromosomes\n")
	f.write("\thtml.Div([ \n")

	f.write("\t	html.Div([ \n")
	f.write("\t		html.Div([ \n")
	f.write("\t			html.Label('Choose your sequence : ') \n")
	f.write("\t		], style={'width': '14%', 'vertical-align':'top', 'text-align':'center', 'display': 'inline-block'} ), \n\n")

	f.write("\t		html.Div([ \n")
	f.write("\t			# combolist \n")
	f.write("\t			dcc.Dropdown(\n")
	f.write("\t				id='SelectSequence_Onglet3', \n")
	f.write("\t				options=[ \n")
	f.write("\t					{'label': 'Whole Genome', 'value': '")
	f.write(str(len(SelectionName)))
	f.write("'}, \n")
	for z in range(0, len(SelectionName), 1) :
		f.write("\t				{'label': '")
		f.write(SelectionName[z])
		f.write("', 'value': '")
		f.write(str(z))
		f.write("'}, \n")
	f.write("\t				], \n")
	f.write("\t				value='")
	f.write(str(len(SelectionName)))
	f.write("', style={}, \n")
	f.write("\t				clearable=False, \n")
	f.write("\t			), \n")
	f.write("\t			html.Div(id='Onglet3_SelectSequence'), \n")
	f.write("\t		], style={'width': '35%', 'display': 'inline-block'} ), \n\n")

	f.write("\t		html.Div([ \n")
	f.write("\t			html.Label('Additional lines : ') \n")
	f.write("\t		], style={'width': '14%', 'vertical-align':'top', 'text-align':'center', 'display': 'inline-block'} ), \n\n")

	f.write("\t		html.Div([ \n")
	f.write("\t			# combolist \n")
	f.write("\t			dcc.Dropdown(\n")
	f.write("\t				id='AddtionalLines_Onglet3', \n")
	f.write("\t				options = [ \n")
	f.write("\t					{'label': 'No Additional Line', 'value': '0'}, \n")
	f.write("\t					{'label': 'TE Superfamily', 'value': '1'}, \n")
	f.write("\t					{'label': 'All TEs (non updated)', 'value': '2'}, \n")
	f.write("\t					{'label': 'TE Superfamily & All TEs (non updated)', 'value': '3'}, \n")
	f.write("\t				], \n")
	f.write("\t				value = '0', style={}, \n")
	f.write("\t				clearable=False, \n")
	f.write("\t			), \n")
	f.write("\t			html.Div(id='Onglet3_AddtionalLines'), \n")
	f.write("\t		], style={'width': '35%', 'display': 'inline-block'} ), \n\n")

	f.write("\t	html.Div(id='Onglet3_2D_graphique_Div'), \n")
	f.write("\t	], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)'} ), \n\n\n")

	f.write("\t], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)'} ), \n\n\n")
	f.write("\thtml.Br(), \n\n\n")



	f.write("\t# Ajout du div qui contiendra toute la page \n")
	f.write("\thtml.Div([ \n")

	f.write("\t	html.Div([ \n")
	f.write("\t		html.Label(' '), 	# Add space between blocks \n")
	f.write("\t	], style={'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px' } ), \n\n")

	f.write("\t	html.Div([ \n")
	f.write("\t		html.Div([ \n")
	f.write("\t			html.Label('Choose your graph type : '), \n")
	f.write("\t			html.Button('3D Surface Graph', id = 'Surface_Onglet3', n_clicks = 0), \n")
	f.write("\t			html.Button('Headmap Graph', id = 'Headmap_Onglet3', n_clicks = 0), \n")
	f.write("\t		], style={'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px' } ), \n")
	f.write("\t		html.Div(id='Onglet3_Button_Div'), \n")
	f.write("\t	], style={'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px' } ), \n\n")

	f.write("\t	html.Div([ \n")
	f.write("\t		html.Div(id='Onglet3_3D_graphique_Div'), \n")
	f.write("\t	], style={'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px' } ), \n\n")

	f.write("\t], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)'} ), \n")


	f.write("], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)'} ) \n\n\n\n\n\n")
	f.close()











########################################################################################################################
###	Create the data from the common slider
########################################################################################################################
def DataFromSliders(temp) :

	f = open(temp, "a")
	f.write("\t# memory[0] and memory[1] are boundary for the size slider\n")
	f.write("\t# memory[2] and memory[3] are boundary for the similarity slider\n")

	f.write("\t# Calcul pour les TEs \n")
	f.write("\tindiceCHR = int(SelectSequence_Onglet3) \n")

	f.write("\ttailleMin_myTE = 0 \n")
	f.write("\tif memory[0] == 1 : \n")
	f.write("\t	tailleMin_myTE = 0 \n")
	f.write("\telse : \n")
	f.write("\t	tailleMin_myTE = MinConsensus * memory[0] / 100 \n")
	f.write("\ttailleMax_myTE = 0 \n")
	f.write("\tif memory[1] == 100 : \n")
	f.write("\t	tailleMax_myTE = 10 * MaxConsensus \n")
	f.write("\telse : \n")
	f.write("\t	tailleMax_myTE = MaxConsensus * memory[1] / 100 \n\n")

	f.write("\ttailleMin_otherTE = 0 \n")
	f.write("\tif memory[0] == 1 : \n")
	f.write("\t\ttailleMin_otherTE = tailleMinOther - 1 \n")
	f.write("\telse : \n")
	f.write("\t\ttailleMin_otherTE = tailleMaxOther * memory[0] / 100 \n")
	f.write("\ttailleMax_otherTE = 0 \n")
	f.write("\tif memory[1] == 100 : \n")
	f.write("\t\ttailleMax_otherTE = 10 * tailleMaxOther \n")
	f.write("\telse : \n")
	f.write("\t\ttailleMax_otherTE = tailleMaxOther * memory[1] / 100 \n")
	f.write("\tSelectionName = CommonDATA.dataFrame_Organism['Name'].tolist() \n\n\n\n")

	f.close()











########################################################################################################################
###	Create the Size Pie chart for the chromosome
########################################################################################################################
def LineChartSize(temp, numberTE) :

	f = open(temp, "a")
	f.write("\t########################################################################################################################\n")
	f.write("\t# Calcul pour la distribution des tailles des TEs \n\n")

	if numberTE == 1 :
		f.write("\tmyTE_Size_Class = [] \n")  		# +1 for the genome
		f.write("\tsuperTE_Size_Class = [] \n")
		f.write("\tfor k in range(0, 20, 1): \n")
		f.write("\t	myTE_Size_Class.append(0) \n")
		f.write("\t	superTE_Size_Class.append(0) \n")

		f.write("\tif indiceCHR != CommonDATA.nbSeq_Assemble : \n")	# ici on selectionne le chromosome

		f.write("\t	Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[indiceCHR]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= memory[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= memory[3]), ['Size'] ] \n")
		f.write("\t	Selection_myTE = Select_myTE['Size'].tolist() \n")
		f.write("\t	# get the data for the chromosomes for the curve for my TE \n")
		f.write("\t	for j in range(0, len(Selection_myTE), 1) : \n")
		f.write("\t		classe = round(Selection_myTE[j] / genome_sizeClass[indiceCHR]) \n")
		f.write("\t		if(classe > 19): \n")
		f.write("\t			classe = 19 \n")
		f.write("\t		myTE_Size_Class[classe] += 1 \n\n")

		f.write("\t	# Only the Superfamily is affected by sliders not the global TEs \n")
		f.write("\t	if AddtionalLines_Onglet3 == '1' or AddtionalLines_Onglet3 == '3' : \n")
		f.write("\t		Select_superTE = CommonDATA_SelectTEs.dataFrame_superTE.loc[ (CommonDATA_SelectTEs.dataFrame_superTE['Chr ID'] == SelectionNameID[indiceCHR]) & (CommonDATA_SelectTEs.dataFrame_superTE['Similarity'] >= memory[2]) & (CommonDATA_SelectTEs.dataFrame_superTE['Similarity'] <= memory[3]), ['Size'] ] \n")
		f.write("\t		Selection_superTE = Select_superTE['Size'].tolist() \n")
		f.write("\t		# get the data for the chromosome for the curve for superfamily TEs \n")
		f.write("\t		for j in range(0, len(Selection_superTE), 1) : \n")
		f.write("\t			classe = round(Selection_superTE[j] / genome_sizeClass[indiceCHR]) \n")
		f.write("\t			if(classe > 19): \n")
		f.write("\t				classe = 19 \n")
		f.write("\t			superTE_Size_Class[classe] += 1 \n\n")

		f.write("\telse : \n")	# ici on selectionne le genome

		f.write("\t	for a in range(0, len(SelectionNameID), 1) : \n")
		f.write("\t		Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[a]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= memory[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= memory[3]), ['Size'] ] \n")
		f.write("\t		Selection_myTE = Select_myTE['Size'].tolist() \n")
		f.write("\t		# get the data for the genome for the curve for my TE \n")
		f.write("\t		for j in range(0, len(Selection_myTE), 1) : \n")
		f.write("\t			classe = round(Selection_myTE[j] / genome_sizeClass[a]) \n")
		f.write("\t			if(classe > 19): \n")
		f.write("\t				classe = 19 \n")
		f.write("\t			myTE_Size_Class[classe] += 1 \n\n")

		f.write("\t	# Only the Superfamily is affected by sliders not the global TEs \n")
		f.write("\t	if AddtionalLines_Onglet3 == '1' or AddtionalLines_Onglet3 == '3' : \n")
		f.write("\t		for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("\t			Select_superTE = CommonDATA_SelectTEs.dataFrame_superTE.loc[ (CommonDATA_SelectTEs.dataFrame_superTE['Chr ID'] == SelectionNameID[a]) & (CommonDATA_SelectTEs.dataFrame_superTE['Similarity'] >= memory[2]) & (CommonDATA_SelectTEs.dataFrame_superTE['Similarity'] <= memory[3]), ['Size'] ] \n")
		f.write("\t			Selection_superTE = Select_superTE['Size'].tolist() \n")
		f.write("\t			# get the data for the genome for the curve for superfamily TEs \n")
		f.write("\t			for j in range(0, len(Selection_superTE), 1) : \n")
		f.write("\t				classe = round(Selection_superTE[j] / genome_sizeClass[a]) \n")
		f.write("\t				if(classe > 19): \n")
		f.write("\t					classe = 19 \n")
		f.write("\t				superTE_Size_Class[classe] += 1 \n\n")

	else :
		f.write("\tmyTE_Size_Class = [] \n")  		# +1 for the genome
		f.write("\tsuperTE_Size_Class = [] \n")
		f.write("\tfor k in range(0, 21, 1): \n")
		f.write("\t	superTE_Size_Class.append(0) \n")
		f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("\t	myTE_Size_Class.append([]) \n")  		# +1 for the genome
		f.write("\t	for k in range(0, 20, 1): \n")
		f.write("\t		myTE_Size_Class[j].append(0) \n")

		f.write("\t	if indiceCHR != CommonDATA.nbSeq_Assemble : \n")	# ici on selectionne le chromosome
		f.write("\t		Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[indiceCHR]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= memory[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= memory[3]) & (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[j]), ['Size'] ] \n")
		f.write("\t		Selection_myTE = Select_myTE['Size'].tolist() \n")
		f.write("\t		# get the data for the chromosomes for the curve for my TE \n")
		f.write("\t		for k in range(0, len(Selection_myTE), 1) : \n")
		f.write("\t			classe = round(Selection_myTE[k] / Average_sizeClass[indiceCHR]) 	# I take the smallest class size \n")
		f.write("\t			if(classe > 19): \n")
		f.write("\t				classe = 19 \n")
		f.write("\t			myTE_Size_Class[j][classe] += 1 \n\n")

		f.write("\t	else : \n")	# ici on selectionne le genome
		f.write("\t		for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("\t			Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[a]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= memory[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= memory[3]) & (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[j]), ['Size'] ] \n")
		f.write("\t			Selection_myTE = Select_myTE['Size'].tolist() \n")
		f.write("\t			# get the data for the genome for the curve for my TE \n")
		f.write("\t			for k in range(0, len(Selection_myTE), 1) : \n")
		f.write("\t				classe = round(Selection_myTE[k] / Average_sizeClass[len(SelectionRefseq)]) \n")
		f.write("\t				if(classe > 19): \n")
		f.write("\t					classe = 19 \n")
		f.write("\t				myTE_Size_Class[j][classe] += 1 \n\n")

		f.write("\t# Only the Superfamily is affected by sliders not the global TEs \n")
		f.write("\tif AddtionalLines_Onglet3 == '1' or AddtionalLines_Onglet3 == '3' : \n")

		f.write("\t	if indiceCHR != CommonDATA.nbSeq_Assemble : \n")	# ici on selectionne le chromosome
		f.write("\t		Select_superTE = CommonDATA_SelectTEs.dataFrame_superTE.loc[ (CommonDATA_SelectTEs.dataFrame_superTE['Chr ID'] == SelectionNameID[indiceCHR]) & (CommonDATA_SelectTEs.dataFrame_superTE['Similarity'] >= memory[2]) & (CommonDATA_SelectTEs.dataFrame_superTE['Similarity'] <= memory[3]), ['Size'] ] \n")
		f.write("\t		Selection_superTE = Select_superTE['Size'].tolist() \n")
		f.write("\t		# get the data for the chromosome for the curve for superfamily TEs \n")
		f.write("\t		for j in range(0, len(Selection_superTE), 1) : \n")
		f.write("\t			classe = round(Selection_superTE[j] / Average_sizeClass[indiceCHR]) \n")
		f.write("\t			if(classe > 19): \n")
		f.write("\t				classe = 19 \n")
		f.write("\t			superTE_Size_Class[classe] += 1 \n\n")

		f.write("\t	else : \n")	# ici on selectionne le genome
		f.write("\t		for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("\t			Select_superTE = CommonDATA_SelectTEs.dataFrame_superTE.loc[ (CommonDATA_SelectTEs.dataFrame_superTE['Chr ID'] == SelectionNameID[a]) & (CommonDATA_SelectTEs.dataFrame_superTE['Similarity'] >= memory[2]) & (CommonDATA_SelectTEs.dataFrame_superTE['Similarity'] <= memory[3]), ['Size'] ] \n")
		f.write("\t			Selection_superTE = Select_superTE['Size'].tolist() \n")
		f.write("\t			# get the data for the genome for the curve for superfamily TEs \n")
		f.write("\t			for k in range(0, len(Selection_superTE), 1) : \n")
		f.write("\t				classe = round(Selection_superTE[k] / Average_sizeClass[len(SelectionRefseq)]) \n")
		f.write("\t				if(classe > 19): \n")
		f.write("\t					classe = 19 \n")
		f.write("\t				superTE_Size_Class[classe] += 1 \n\n")



	f.write("\t# prepare the graph for each sequence \n")
	f.write("\tsuperTE_LineSize = go.Scatter( x = AxisSize[indiceCHR], y = [], name = CommonDATA_SelectTEs.SuperfamilyTE, line = dict(color=CommonDATA_SelectTEs.CouleurSuperTE, width=2, dash='dot') ) \n")
	f.write("\totherTE_LineSize = go.Scatter( x = AxisSize[indiceCHR], y = [], name = 'All TEs', line = dict(color='black', width=1) ) \n")
	f.write("\tif AddtionalLines_Onglet3 == '1' or AddtionalLines_Onglet3 == '3' : \n")
	f.write("\t	superTE_LineSize = go.Scatter( x = AxisSize[indiceCHR], y = superTE_Size_Class, name = CommonDATA_SelectTEs.SuperfamilyTE, line = dict(color=CommonDATA_SelectTEs.CouleurSuperTE, width=2, dash='dot'), yaxis='y2' ) \n")
	f.write("\tif AddtionalLines_Onglet3 == '2' or AddtionalLines_Onglet3 == '3' : \n")
	f.write("\t	otherTE_LineSize = go.Scatter( x = AxisSize[indiceCHR], y = otherTE_Size_Class[indiceCHR], name = 'All TEs', line = dict(color='black', width=1), yaxis='y3' ) \n\n")

	if numberTE == 1 :
		f.write("\tMyTE_LineSize = go.Scatter( x = AxisSize[indiceCHR], y = myTE_Size_Class, name = CommonDATA_SelectTEs.OfficialName, line = dict(color=Couleur.couleurSelectTE[0], width=4, dash='dash'), yaxis='y1' ) \n")
	else :
		for j in range(0, numberTE, 1) :
			f.write("\tMyTE_LineSize_" + str(j) + " = go.Scatter( x = AxisSize[indiceCHR], y = myTE_Size_Class[" + str(j) + "], name = CommonDATA_SelectTEs.list_selection_TE[" + str(j) + "], line = dict(color=Couleur.couleurSelectTE[" + str(j) + "], width=4, dash='dash'), yaxis='y1' ) \n")

	f.write("\n\n\n")
	f.close()











########################################################################################################################
###	Create the Similarity Pie chart for the chromosome
########################################################################################################################
def LineChartSimilarity(temp, numberTE) :

	f = open(temp, "a")
	f.write("\t########################################################################################################################\n")

	if numberTE == 1 :
		f.write("\t# Calcul pour la distribution des similarites des TEs \n\n")
		f.write("\tmyTE_Sim_Class = [] \n")
		f.write("\tsuperTE_Sim_Class = [] \n")
		f.write("\tfor k in range(0, 50, 1): \n")
		f.write("\t	myTE_Sim_Class.append(0) \n")
		f.write("\t	superTE_Sim_Class.append(0) \n\n")

		f.write("\tif indiceCHR != CommonDATA.nbSeq_Assemble : \n")	# ici on selectionne le chromosome
		f.write("\t	Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[indiceCHR]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin_myTE) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax_myTE), ['Similarity'] ] \n")
		f.write("\t	Selection_myTE = Select_myTE['Similarity'].tolist() \n")
		f.write("\t	# get the data for the chromosomes for the curve for my TE \n")
		f.write("\t	for j in range(0, len(Selection_myTE), 1) : \n")
		f.write("\t		classe = round(Selection_myTE[j]) - 50 \n")
		f.write("\t		if(classe > 49): \n")
		f.write("\t			classe = 49 \n")
		f.write("\t		myTE_Sim_Class[classe] += 1 \n\n")

		f.write("\telse : \n")	# ici on selectionne le genome
		f.write("\t	for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("\t		Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[a]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin_myTE) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax_myTE), ['Similarity'] ] \n")
		f.write("\t		Selection_myTE = Select_myTE['Similarity'].tolist() \n")
		f.write("\t		# get the data for the genome for the curve for my TE \n")
		f.write("\t		for j in range(0, len(Selection_myTE), 1) : \n")
		f.write("\t			classe = round(Selection_myTE[j]) - 50 \n")
		f.write("\t			if(classe > 49): \n")
		f.write("\t				classe = 49 \n")
		f.write("\t			myTE_Sim_Class[classe] += 1 \n\n")

	else :
		f.write("\tmyTE_Sim_Class = [] \n")  		# +1 for the genome
		f.write("\tsuperTE_Sim_Class = [] \n")
		f.write("\tfor k in range(0, 50, 1): \n")
		f.write("\t	superTE_Sim_Class.append(0) \n\n")
		f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("\t	myTE_Sim_Class.append([]) \n")  		# +1 for the genome
		f.write("\t	for k in range(0, 50, 1): \n")
		f.write("\t		myTE_Sim_Class[j].append(0) \n")

		f.write("\t	if indiceCHR != CommonDATA.nbSeq_Assemble : \n")	# ici on selectionne le chromosome
		f.write("\t		Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[indiceCHR]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin_myTE) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax_myTE) & (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[j]) , ['Similarity'] ] \n")
		f.write("\t		Selection_myTE = Select_myTE['Similarity'].tolist() \n")
		f.write("\t		# get the data for the chromosomes for the curve for my TE \n")
		f.write("\t		for k in range(0, len(Selection_myTE), 1) : \n")
		f.write("\t			classe = round(Selection_myTE[k]) - 50 \n")
		f.write("\t			if(classe > 49): \n")
		f.write("\t				classe = 49 \n")
		f.write("\t			myTE_Sim_Class[j][classe] += 1 \n\n")

		f.write("\t	else : \n")	# ici on selectionne le genome
		f.write("\t		for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("\t			Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[a]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin_myTE) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax_myTE) & (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[j]) , ['Similarity'] ] \n")
		f.write("\t			Selection_myTE = Select_myTE['Similarity'].tolist() \n")
		f.write("\t			# get the data for the genome for the curve for my TE \n")
		f.write("\t			for k in range(0, len(Selection_myTE), 1) : \n")
		f.write("\t				classe = round(Selection_myTE[k]) - 50 \n")
		f.write("\t				if(classe > 49): \n")
		f.write("\t					classe = 49 \n")
		f.write("\t				myTE_Sim_Class[j][classe] += 1 \n\n")


	f.write("\tif AddtionalLines_Onglet3 == '1' or AddtionalLines_Onglet3 == '3' : \n")

	f.write("\t	if indiceCHR != CommonDATA.nbSeq_Assemble : \n")	# ici on selectionne le chromosome
	f.write("\t		Select_superTE = CommonDATA_SelectTEs.dataFrame_superTE.loc[ (CommonDATA_SelectTEs.dataFrame_superTE['Chr ID'] == SelectionNameID[indiceCHR]) & (CommonDATA_SelectTEs.dataFrame_superTE['Size'] >= tailleMin_otherTE) & (CommonDATA_SelectTEs.dataFrame_superTE['Size'] <= tailleMax_otherTE), ['Similarity'] ] \n")
	f.write("\t		Selection_superTE = Select_superTE['Similarity'].tolist() \n")
	f.write("\t		# get the data for the chromosome for the curve for superfamily TEs \n")
	f.write("\t		for j in range(0, len(Selection_superTE), 1) : \n")
	f.write("\t			classe = round(Selection_superTE[j]) - 50 \n")
	f.write("\t			if(classe > 49): \n")
	f.write("\t				classe = 49 \n")
	f.write("\t			superTE_Sim_Class[classe] += 1 \n\n")

	f.write("\t	else : \n")	# ici on selectionne le genome
	f.write("\t		for a in range(0, len(SelectionRefseq), 1) : \n")
	f.write("\t			Select_superTE = CommonDATA_SelectTEs.dataFrame_superTE.loc[ (CommonDATA_SelectTEs.dataFrame_superTE['Chr ID'] == SelectionNameID[a]) & (CommonDATA_SelectTEs.dataFrame_superTE['Size'] >= tailleMin_otherTE) & (CommonDATA_SelectTEs.dataFrame_superTE['Size'] <= tailleMax_otherTE), ['Similarity'] ] \n")
	f.write("\t			Selection_superTE = Select_superTE['Similarity'].tolist() \n")
	f.write("\t			# get the data for the chromosome for the curve for superfamily TEs \n")
	f.write("\t			for j in range(0, len(Selection_superTE), 1) : \n")
	f.write("\t				classe = round(Selection_superTE[j]) - 50 \n")
	f.write("\t				if(classe > 49): \n")
	f.write("\t					classe = 49 \n")
	f.write("\t				superTE_Sim_Class[classe] += 1 \n\n")



	f.write("\t# prepare the graph for each sequence \n")
	f.write("\tsuperTE_LineSimilarity = go.Scatter( x = AxisSim, y = [], name = CommonDATA_SelectTEs.SuperfamilyTE, line = dict(color=CommonDATA_SelectTEs.CouleurSuperTE, width=2, dash='dot') ) \n")
	f.write("\totherTE_LineSimilarity = go.Scatter( x = AxisSim, y = [], name = 'All TEs', line = dict(color='black', width=1) ) \n")
	f.write("\tif AddtionalLines_Onglet3 == '1' or AddtionalLines_Onglet3 == '3' : \n")
	f.write("\t	superTE_LineSimilarity = go.Scatter( x = AxisSim, y = superTE_Sim_Class, name = CommonDATA_SelectTEs.SuperfamilyTE, line = dict(color=CommonDATA_SelectTEs.CouleurSuperTE, width=2, dash='dot'), yaxis='y2' ) \n")
	f.write("\tif AddtionalLines_Onglet3 == '2' or AddtionalLines_Onglet3 == '3' : \n")
	f.write("\t	otherTE_LineSimilarity = go.Scatter( x = AxisSim, y = otherTE_Sim_Class[indiceCHR], name = 'All TEs', line = dict(color='black', width=1), yaxis='y3' ) \n\n")

	if numberTE == 1 :
		f.write("\tMyTE_LineSimilarity = go.Scatter( x = AxisSim, y = myTE_Sim_Class, name = CommonDATA_SelectTEs.OfficialName, line = dict(color=Couleur.couleurSelectTE[0], width=4, dash='dash'), yaxis='y1' ) \n")
	else :
		for j in range(0, numberTE, 1) :
			f.write("\tMyTE_LineSimilarity_" + str(j) + " = go.Scatter( x = AxisSim, y = myTE_Sim_Class[" + str(j) + "], name = CommonDATA_SelectTEs.list_selection_TE[" + str(j) + "], line = dict(color=Couleur.couleurSelectTE[" + str(j) + "], width=4, dash='dash'), yaxis='y1' ) \n")

	f.write("\n\n\n")
	f.close()











########################################################################################################################
###	Create the Size Distribution function in callback
########################################################################################################################
def HTMLPosition_2D_Onglet3(temp, numberTE) :

	f = open(temp, "a")

	f.write("\t########################################################################################################################\n")
	f.write("\tOnglet3_2D = html.Div([ \n")
	f.write("\t	# ajout des graphes pour les sequences : genome et chromosomes \n\n")

	f.write("\t	html.Div([ \n")
	f.write("\t		dcc.Graph( \n")
	f.write("\t			id='SequenceSize_Onglet3', \n")
	f.write("\t			figure={\n")
	f.write("\t				# ajout des donnees provenants de plotly \n")

	if numberTE == 1 :
		f.write("\t				'data': [superTE_LineSize, otherTE_LineSize, MyTE_LineSize], \n")
	else :
		f.write("\t				'data': [superTE_LineSize, otherTE_LineSize, ")
		for j in range(0, numberTE, 1) :
			f.write('MyTE_LineSize_' + str(j) + ', ')
		f.write("], \n")

	f.write("\t				'layout': {\n")
	f.write("\t					'legend':{'orientation':'h'}, \n")
	f.write("\t					# titre du graphique \n")
	f.write("\t					'title': TitreSize, \n")
	f.write("\t					'yaxis1':dict( \n")

	if numberTE == 1 :
		f.write("\t						titlefont=dict(color=Couleur.couleurSelectTE[0]), \n")
		f.write("\t						tickfont=dict(color=Couleur.couleurSelectTE[0]) \n")
	else :
		f.write("\t						titlefont=dict(color='black'), \n")
		f.write("\t						tickfont=dict(color='black') \n")

	f.write("\t					), \n")
	f.write("\t					'yaxis2':dict( \n")
	f.write("\t						titlefont=dict(color=CommonDATA_SelectTEs.CouleurSuperTE), \n")
	f.write("\t						tickfont=dict(color=CommonDATA_SelectTEs.CouleurSuperTE), \n")
	f.write("\t						anchor='x', \n")
	f.write("\t						overlaying='y', \n")
	f.write("\t						side='right', \n")
	f.write("\t					), \n")
	f.write("\t					'yaxis3':dict( \n")
	f.write("\t						titlefont=dict(color='black'), \n")
	f.write("\t						tickfont=dict(color='black'), \n")
	f.write("\t						anchor='free', \n")
	f.write("\t						overlaying='y', \n")
	f.write("\t						side='right', \n")
	f.write("\t						position = 0.99, \n")
	f.write("\t					), \n")
	f.write("\t					'hovermode':'x unified', \n")
	f.write("\t				} \n")
	f.write("\t			}, style = {'height':600} \n")
	f.write("\t		)\n")
	f.write("\t	], style = {'width': '49.5%', 'display':'inline-block'}),\n\n")

	f.write("\t	html.Div([ \n")
	f.write("\t		dcc.Graph( \n")
	f.write("\t			id='SequenceSimilarity_Onglet3', \n")
	f.write("\t			figure={\n")
	f.write("\t				# ajout des donnees provenants de plotly \n")

	if numberTE == 1 :
		f.write("\t				'data': [superTE_LineSimilarity, otherTE_LineSimilarity, MyTE_LineSimilarity], \n")
	else :
		f.write("\t				'data': [superTE_LineSimilarity, otherTE_LineSimilarity, ")
		for j in range(0, numberTE, 1) :
			f.write('MyTE_LineSimilarity_' + str(j) + ', ')
		f.write("], \n")

	f.write("\t				'layout': {\n")
	f.write("\t					'legend':{'orientation':'h'}, \n")
	f.write("\t					# titre du graphique \n")
	f.write("\t					'title': TitreSimilarity, \n")
	f.write("\t					'xaxis':dict( domain=[0, 0.95] ), \n")
	f.write("\t					'yaxis1':dict( \n")

	if numberTE == 1 :
		f.write("\t						titlefont=dict(color=Couleur.couleurSelectTE[0]), \n")
		f.write("\t						tickfont=dict(color=Couleur.couleurSelectTE[0]) \n")
	else :
		f.write("\t						titlefont=dict(color='black'), \n")
		f.write("\t						tickfont=dict(color='black') \n")

	f.write("\t					), \n")
	f.write("\t					'yaxis2':dict( \n")
	f.write("\t						titlefont=dict(color=CommonDATA_SelectTEs.CouleurSuperTE), \n")
	f.write("\t						tickfont=dict(color=CommonDATA_SelectTEs.CouleurSuperTE), \n")
	f.write("\t						anchor='x', \n")
	f.write("\t						overlaying='y', \n")
	f.write("\t						side='right', \n")
	f.write("\t					), \n")
	f.write("\t					'yaxis3':dict( \n")
	f.write("\t						titlefont=dict(color='black'), \n")
	f.write("\t						tickfont=dict(color='black'), \n")
	f.write("\t						anchor='free', \n")
	f.write("\t						overlaying='y', \n")
	f.write("\t						side='right', \n")
	f.write("\t						position = 0.99, \n")
	f.write("\t					), \n")
	f.write("\t					'hovermode':'x unified', \n")
	f.write("\t				} \n")
	f.write("\t			}, style = {'height':600}, \n")
	f.write("\t		)\n")
	f.write("\t	], style={'width':'49.5%', 'float':'right', 'display':'inline-block'})\n\n")

	f.write("\t], style={'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'}),\n\n")
	f.write("\treturn Onglet3_2D \n\n\n\n")

	f.close()











########################################################################################################################
###	Create the Size Distribution function in callback
########################################################################################################################
def CreateCallBack_2D_Onglet3(temp, numberTE) :

	# Correspondance entre le combobox et les graphes de distribution de taille
	f = open(temp, "a")
	f.write("########################################################################################################################\n")
	f.write("# Ensemble des callbacks\n")
	f.write("# Ajout du combobox de plotly pour le genome + l'ensemble des chromosomes size distribution\n\n")
	f.write("@app.callback(Output('Onglet3_2D_graphique_Div', 'children'), \n")
	f.write("	[Input('memory', 'data'), Input('SelectSequence_Onglet3', 'value'), Input('AddtionalLines_Onglet3', 'value')]) \n\n");
	f.write("def update_2D_Onglet3(memory, SelectSequence_Onglet3, AddtionalLines_Onglet3):\n\n")
	f.close()



	# Adding the transformed data from common sliders
	DataFromSliders(temp)

	# Creating the size data for each sequence
	LineChartSize(temp, numberTE)

	# Creating the size data for each sequence
	LineChartSimilarity(temp, numberTE)



	f = open(temp, "a")
	f.write("\t######################################################################################################################## \n")
	f.write("\t# Graphiques des distributions de taille et similarites \n\n")

	if numberTE == 1 :
		f.write("\tTitreSize = '' \n")
		f.write("\tif indiceCHR < len(SelectionName) : \n")
		f.write("\t	TitreSize = 'Size Distribution of ' + CommonDATA_SelectTEs.OfficialName + ' in ' + CommonDATA.nameOrganism + ' ' + SelectionName[indiceCHR] + ' sequence' \n")
		f.write("\telse : \n")
		f.write("\t	TitreSize = 'Size Distribution of ' + CommonDATA_SelectTEs.OfficialName + ' in ' + CommonDATA.nameOrganism + ' genome' \n")

		f.write("\tTitreSimilarity = '' \n")
		f.write("\tif indiceCHR < len(SelectionName) : \n")
		f.write("\t	TitreSimilarity = 'Similarity Distribution of ' + CommonDATA_SelectTEs.OfficialName + ' in ' + CommonDATA.nameOrganism + ' ' + SelectionName[indiceCHR] + ' sequence' \n")
		f.write("\telse : \n")
		f.write("\t	TitreSimilarity = 'Similarity Distribution of ' + CommonDATA_SelectTEs.OfficialName + ' in ' + CommonDATA.nameOrganism + ' genome' \n\n\n")
		f.close()

	else :
		f.write("\tTitreSize = '' \n")
		f.write("\tif indiceCHR < len(SelectionName) : \n")
		f.write("\t	TitreSize = 'Size Distribution of ' + ")
		for j in range(0, numberTE, 1) :
			if j > 0 :
				f.write(" + ' ' + ")
			f.write("CommonDATA_SelectTEs.list_selection_TE[" + str(j) + "] ")
		f.write(" + ' in ' + CommonDATA.nameOrganism + ' ' + SelectionName[indiceCHR] + ' sequence' \n")
		f.write("\telse : \n")
		f.write("\t	TitreSize = 'Size Distribution of ' + ")
		for j in range(0, numberTE, 1) :
			if j > 0 :
				f.write(" + ' ' + ")
			f.write("CommonDATA_SelectTEs.list_selection_TE[" + str(j) + "] ")
		f.write(" + ' in ' + CommonDATA.nameOrganism + ' genome' \n")

		f.write("\tTitreSimilarity = '' \n")
		f.write("\tif indiceCHR < len(SelectionName) : \n")
		f.write("\t	TitreSimilarity = 'Similarity Distribution of ' + ")
		for j in range(0, numberTE, 1) :
			if j > 0 :
				f.write(" + ' ' + ")
			f.write("CommonDATA_SelectTEs.list_selection_TE[" + str(j) + "] ")
		f.write(" + ' in ' + CommonDATA.nameOrganism + ' ' + SelectionName[indiceCHR] + ' sequence' \n")
		f.write("\telse : \n")
		f.write("\t	TitreSimilarity = 'Similarity Distribution of ' + ")
		for j in range(0, numberTE, 1) :
			if j > 0 :
				f.write(" + ' ' + ")
			f.write("CommonDATA_SelectTEs.list_selection_TE[" + str(j) + "] ")
		f.write(" + ' in ' + CommonDATA.nameOrganism + ' genome' \n\n\n")
		f.close()


	HTMLPosition_2D_Onglet3(temp, numberTE)











########################################################################################################################
###	Create the 3D Size Similarty Distribution function in callback : ONLY MYTE
########################################################################################################################
def SurfaceSizeSimilarity(temp,  numberTE) :

	f = open(temp, "a")
	f.write("\t########################################################################################################################\n")

	# # Creates a list containing 50 lists, each of 20 items, all set to 0
	f.write("\twidth3D, height3D = 20, 50; \n")
	f.write("\tindiceCHR = int(SelectSequence_Onglet3) \n")

	f.write("\ttailleMin_myTE = 0 \n")
	f.write("\tif memory[0] == 1 : \n")
	f.write("\t	tailleMin_myTE = 0 \n")
	f.write("\telse : \n")
	f.write("\t	tailleMin_myTE = MinConsensus * memory[0] / 100 \n")
	f.write("\ttailleMax_myTE = 0 \n")
	f.write("\tif memory[1] == 100 : \n")
	f.write("\t	tailleMax_myTE = 10 * MaxConsensus \n")
	f.write("\telse : \n")
	f.write("\t	tailleMax_myTE = MaxConsensus * memory[1] / 100 \n\n")

	f.write("\ttailleMin_otherTE = 0 \n")
	f.write("\tif memory[0] == 1 : \n")
	f.write("\t\ttailleMin_otherTE = tailleMinOther - 1 \n")
	f.write("\telse : \n")
	f.write("\t\ttailleMin_otherTE = tailleMaxOther * memory[0] / 100 \n")
	f.write("\ttailleMax_otherTE = 0 \n")
	f.write("\tif memory[1] == 100 : \n")
	f.write("\t\ttailleMax_otherTE = 10 * tailleMaxOther \n")
	f.write("\telse : \n")
	f.write("\t\ttailleMax_otherTE = tailleMaxOther * memory[1] / 100 \n\n")

	if numberTE == 1 :
		f.write("\tvalues3D = [[0 for x in range(width3D)] for y in range(height3D)] \n")

		f.write("\tif indiceCHR != CommonDATA.nbSeq_Assemble : \n")

		f.write("\t	Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[indiceCHR]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= memory[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= memory[3]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin_myTE) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax_myTE), ['Size', 'Similarity'] ] \n")
		f.write("\t	Selection_Size_myTE = Select_myTE['Size'].tolist() \n")
		f.write("\t	Selection_Sim_myTE = Select_myTE['Similarity'].tolist() \n")
		f.write("\t	for i in range(0, len(Selection_Size_myTE), 1) : \n")
		f.write("\t		classeSize = round(Selection_Size_myTE[i] / genome_sizeClass[indiceCHR]) \n")
		f.write("\t		if(classeSize > 19): \n")
		f.write("\t			classeSize = 19 \n")
		f.write("\t		classeSim = round(Selection_Sim_myTE[i]) - 50 \n")
		f.write("\t		if(classeSim > 49): \n")
		f.write("\t			classeSim = 49 \n")
		f.write("\t		values3D[classeSim][classeSize] += 1 \n\n")

		f.write("\telse : \n")

		f.write("\t	for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("\t		Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[a]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= memory[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= memory[3]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin_myTE) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax_myTE), ['Size', 'Similarity'] ] \n")
		f.write("\t		Selection_Size_myTE = Select_myTE['Size'].tolist() \n")
		f.write("\t		Selection_Sim_myTE = Select_myTE['Similarity'].tolist() \n")
		f.write("\t		for i in range(0, len(Selection_Size_myTE), 1) : \n")
		f.write("\t			classeSize = round(Selection_Size_myTE[i] / genome_sizeClass[indiceCHR]) \n")
		f.write("\t			if(classeSize > 19): \n")
		f.write("\t				classeSize = 19 \n")
		f.write("\t			classeSim = round(Selection_Sim_myTE[i]) - 50 \n")
		f.write("\t			if(classeSim > 49): \n")
		f.write("\t				classeSim = 49 \n")
		f.write("\t			values3D[classeSim][classeSize] += 1 \n")

	else :
		f.write("\tvalues3D = [[[0 for k in range(width3D)] for j in range(height3D)] for i in range(len(CommonDATA_SelectTEs.list_selection_TE))] \n")
		f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("\t	if indiceCHR != CommonDATA.nbSeq_Assemble : \n")

		f.write("\t		Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[indiceCHR]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= memory[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= memory[3]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin_myTE) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax_myTE) & (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[j]) , ['Size', 'Similarity'] ] \n")
		f.write("\t		Selection_Size_myTE = Select_myTE['Size'].tolist() \n")
		f.write("\t		Selection_Sim_myTE = Select_myTE['Similarity'].tolist() \n")
		f.write("\t		for i in range(0, len(Selection_Size_myTE), 1) : \n")
		f.write("\t			classeSize = round(Selection_Size_myTE[i] / Average_sizeClass[indiceCHR]) \n")
		f.write("\t			if(classeSize > 19): \n")
		f.write("\t				classeSize = 19 \n")
		f.write("\t			classeSim = round(Selection_Sim_myTE[i]) - 50 \n")
		f.write("\t			if(classeSim > 49): \n")
		f.write("\t				classeSim = 49 \n")
		f.write("\t			values3D[j][classeSim][classeSize] += 1 \n\n")

		f.write("\t	else : \n")

		f.write("\t		for a in range(0, len(SelectionRefseq), 1) : \n")
		f.write("\t			Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[a]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= memory[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= memory[3]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin_myTE) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax_myTE) & (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[j]) , ['Size', 'Similarity'] ] \n")
		f.write("\t			Selection_Size_myTE = Select_myTE['Size'].tolist() \n")
		f.write("\t			Selection_Sim_myTE = Select_myTE['Similarity'].tolist() \n")
		f.write("\t			for i in range(0, len(Selection_Size_myTE), 1) : \n")
		f.write("\t				classeSize = round(Selection_Size_myTE[i] / Average_sizeClass[a]) \n")
		f.write("\t				if(classeSize > 19): \n")
		f.write("\t					classeSize = 19 \n")
		f.write("\t				classeSim = round(Selection_Sim_myTE[i]) - 50 \n")
		f.write("\t				if(classeSim > 49): \n")
		f.write("\t					classeSim = 49 \n")
		f.write("\t				values3D[j][classeSim][classeSize] += 1 \n")


	f.write("\n\n\n")
	f.close()










########################################################################################################################
###	Create the Size Distribution function in callback
########################################################################################################################
def HTMLPosition_3D_Onglet3(temp, numberTE) :

	f = open(temp, "a")
	f.write("\t########################################################################################################################\n")
	f.write("\tOnglet3_3D = html.Div([ \n")

	if numberTE == 1 :

		f.write("\t	html.Div([ \n")
		f.write("\t		dcc.Graph( \n")
		f.write("\t			id='SimilaritySize_3D_Onglet3', \n")
		f.write("\t			figure={\n")
		f.write("\t				# ajout des donnees provenants de plotly \n")
		f.write("\t				'data': [SizeSimilarity3D], \n")
		f.write("\t				'layout': {\n")
		f.write("\t					'title' : '3D Size and Similarity Distribution of ' + CommonDATA_SelectTEs.OfficialName + '<br> in ' + CommonDATA.nameOrganism , \n")
		f.write("\t					'scene' : { \n")
		f.write("\t							'xaxis' : {'nticks' : 20}, \n")
		f.write("\t							'yaxis' : {'nticks' : 50}, \n")
		f.write("\t							'zaxis' : {'nticks' : 25}, \n")
		f.write("\t							'autosize':False, \n")
		f.write("\t							'aspectratio': {'x':3, 'y': 3, 'z': 1}, \n")
		f.write("\t							'camera':{ 'eye':{'x':-2.25, 'y':-2.25, 'z':0.25} }, \n")
		f.write("\t						}, \n")
		f.write("\t				}, \n")
		f.write("\t			}, style = {'height':800, 'width':'100%'}, \n")
		f.write("\t		), \n")
		f.write("\t	], style={'width':'100%', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),\n\n")

	else :

		for j in range(0, numberTE, 1) :
			f.write("\t	html.Div([ \n")
			f.write("\t		dcc.Graph( \n")
			f.write("\t			id='SimilaritySize_3D_Onglet3_" + str(j) + "', \n")
			f.write("\t			figure={\n")
			f.write("\t				# ajout des donnees provenants de plotly \n")
			f.write("\t				'data': [SizeSimilarity3D_" + str(j) + "], \n")
			f.write("\t				'layout': {\n")
			f.write("\t					'title' : '3D Size and Similarity Distribution of ' + CommonDATA_SelectTEs.list_selection_TE[" + str(j) + "] + '<br> in ' + CommonDATA.nameOrganism , \n")
			f.write("\t					'scene' : { \n")
			f.write("\t							'xaxis' : {'nticks' : 20}, \n")
			f.write("\t							'yaxis' : {'nticks' : 50}, \n")
			f.write("\t							'zaxis' : {'nticks' : 25}, \n")
			f.write("\t							'autosize':False, \n")
			f.write("\t							'aspectratio': {'x':3, 'y': 3, 'z': 1}, \n")
			f.write("\t							'camera':{ 'eye':{'x':-2.25, 'y':-2.25, 'z':0.25} }, \n")
			f.write("\t						}, \n")
			f.write("\t				}, \n")
			f.write("\t			}, style = {'height':800, 'width':'100%'}, \n")
			f.write("\t		), \n")
			widthDIV = 48.5
			if numberTE == 3 :
				widthDIV = 31.5
			f.write("\t	], style={'width':'" + str(widthDIV) + "%', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px', 'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center'}),\n\n")

	f.write("\t], style={'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px' } ),\n\n")
	f.write("\treturn Onglet3_3D \n")

	f.close()











########################################################################################################################
###	Create the Callback and Layout for the 3D graph
########################################################################################################################
def CreateCallBack_3D_Onglet3(temp, numberTE) :

	f = open(temp, "a")

	f.write("########################################################################################################################\n")
	f.write("@app.callback(Output('Onglet3_3D_graphique_Div', 'children'),\n")
	f.write("[Input('Surface_Onglet3', 'n_clicks'), Input('Headmap_Onglet3', 'n_clicks'), Input('SelectSequence_Onglet3', 'value'), Input('memory', 'data') ]) \n\n")

	f.write("def update_3D_Onglet3(Surface_Onglet3, Headmap_Onglet3, SelectSequence_Onglet3, memory): \n\n\n")
	f.close()


	# Creating 3D graph for size and similarity for each sequence only for MyTE
	SurfaceSizeSimilarity(temp, numberTE)



	f = open(temp, "a")
	f.write("\tchanged_id = [p['prop_id'] for p in dash.callback_context.triggered][0] \n")

	f.write("\tif 'Headmap_Onglet3' in changed_id : \n")
	if numberTE == 1 :
		f.write("\t	SizeSimilarity3D = go.Heatmap(x = AxisSize[indiceCHR], y = AxisSim, z = values3D )  \n")
	else :
		for j in range(0, numberTE, 1) :
			f.write("\t	SizeSimilarity3D_" + str(j) + " = go.Heatmap(x = AxisSize[indiceCHR], y = AxisSim, z = values3D[" + str(j) + "] )  \n")

	f.write("\telse : \n")
	if numberTE == 1 :
		f.write("\t	SizeSimilarity3D = go.Surface(x = AxisSize[indiceCHR], y = AxisSim, z = values3D, contours=dict(z=dict(show=True, color='rgb(150,150,150)')) )  \n")
	else :
		for j in range(0, numberTE, 1) :
			f.write("\t	SizeSimilarity3D_" + str(j) + " = go.Surface(x = AxisSize[indiceCHR], y = AxisSim, z = values3D[" + str(j) + "], contours=dict(z=dict(show=True, color='rgb(150,150,150)')) )  \n")


	f.write("\n\n\n")
	f.close()



	# Create the Layout for the 3D graph
	HTMLPosition_3D_Onglet3(temp, numberTE)











########################################################################################################################
###	Create the Size Distribution function
########################################################################################################################
def GeneralFeatures_layout(pathVisual, pathVisualNEW, numberTE):

	temp = pathVisualNEW + '/Functions/GeneralFeatures.py'
	f = open(temp, "w")
	f.write("#!/usr/bin/env python3 \n")
	f.write("# -*- coding: utf-8 -*- \n")
	f.write("import dash \n")
	f.write("import pandas as pd \n")
	f.write("import dash_core_components as dcc \n")
	f.write("import dash_html_components as html \n")
	f.write("import plotly.graph_objects as go \n")
	f.write("from dash.dependencies import Input, Output \n")
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

GenomeBrowser_raw = pathVisual+"/second_half/Functions/GenomeBrowser"####

GenomeBrowser_processed = GenomeBrowser_raw.replace("/",".")#####
# The file gets executed upon import, as expected.
GenomeBrowser = importlib.import_module(GenomeBrowser_processed)#####

ChromosomeDistribution_raw = pathVisual+"/second_half/Functions/ChromosomeDistribution"####

ChromosomeDistribution_processed = ChromosomeDistribution_raw.replace("/",".")#####
# The file gets executed upon import, as expected.
ChromosomeDistribution = importlib.import_module(ChromosomeDistribution_processed)#####

GeneralFeatures_raw = pathVisual+"/second_half/Functions/GeneralFeatures"####

GeneralFeatures_processed = GeneralFeatures_raw.replace("/",".")#####
# The file gets executed upon import, as expected.
GeneralFeatures = importlib.import_module(GeneralFeatures_processed)#####

""")



	# get the data for the organism
	tempFile = pathVisual + '/Downloaded/DATA_Organism.txt'
	dataT = pd.read_csv(tempFile)
	# Create first a sud-dataframe that contains only the wanted values
	dataFrame_Organism = dataT.loc[(dataT['Size bp'] > 0)]



	# Print in the python file the necessary data
	NonUpdatedVariable_Onglet3(temp, numberTE)
	# Add the basic of the layout
	CreateLayoutGeneralFeatures(temp, dataFrame_Organism)

	# Create the callback that updates the two first graph
	CreateCallBack_2D_Onglet3(temp, numberTE)

	# Create the callback that updates the two first graph
	CreateCallBack_3D_Onglet3(temp, numberTE)
	### dash.callback_context.inputs.values()	Liste the values of all input in callback


	'''
	Second, we used sequence divergence of TEs to estimate their age. We used the RepBase-consensus sequence29 of each TE subfamily as a proxy for the ancestral
	state of the TE30,31 and estimated the sequence divergence between the genomic copies of each TE subfamily to its corresponding RepBase-consensus sequence,
	using the Juke-Cantor model32 (see Methods)
	'''
