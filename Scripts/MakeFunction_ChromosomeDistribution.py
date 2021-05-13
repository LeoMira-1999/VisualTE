#!/usr/bin/python3
import os
import sys
import importlib
import importlib.util
import pandas as pd
import plotly.graph_objs as go





########################################################################################################################
###	Variables necessary in whole scripts
########################################################################################################################
def Invariable_Script(temp) :

	f = open(temp, "a")
	f.write("########################################################################################################################\n")

	f.write("newColorDict = [] 	# nouveau tableau des couleurs utilisees \n")
	f.write("couleurUsed = [] 	# verifie quelles couleurs sont utilisees\n")
	f.write("for i in range(0, len(CommonDATA.ListeObject), 1) : \n")
	f.write("	couleurUsed.append(0) \n")

	f.write("hauteurTableau = 250 + 30 * (CommonDATA.nbSeq_Assemble + 1) \n")
	f.write("SelectionName = CommonDATA.dataFrame_Organism['Name'].tolist() \n")
	f.write("SelectionNameID = CommonDATA.dataFrame_Organism['NameID'].tolist() \n")
	f.write("SelectionRefseq = CommonDATA.dataFrame_Organism['RefSeq'].tolist() \n")
	f.write("SelectionSize = CommonDATA.dataFrame_Organism['Size bp'].tolist() \n\n")

	# Select the column and tranform this column in list
	f.write("TabSelectionName = CommonDATA.dataFrame_Organism['Name'].tolist() \n")
	f.write("TabSelectionID = CommonDATA.dataFrame_Organism['NameID'].tolist() \n")
	f.write("TabSelectionSize = CommonDATA.dataFrame_Organism['Size Mb'].tolist() \n")
	f.write("TabSelectionGC = CommonDATA.dataFrame_Organism['GC%'].tolist() \n")
	f.write("TabSelectionProtein = CommonDATA.dataFrame_Organism['nb Protein'].tolist() \n")
	f.write("TabSelectionGene = CommonDATA.dataFrame_Organism['nb Gene'].tolist() \n")
	f.write("TabSelectionPseudogene = CommonDATA.dataFrame_Organism['nb Pseudo'].tolist() \n")
	f.write("TabSelectionncRNA = CommonDATA.dataFrame_Organism['nb ncRNA'].tolist() \n")
	f.write("Tabtotal_sizeSeq = 0 \n")
	f.write("Tabtotal_GCseq = 0 \n")
	f.write("Tabtotal_Protein = 0 \n")
	f.write("Tabtotal_Gene = 0 \n")
	f.write("Tabtotal_Pseudogene = 0 \n")
	f.write("Tabtotal_ncRNA = 0 \n")
	f.write("for z in range(0, len(SelectionSize), 1) :  \n")
	f.write("	Tabtotal_sizeSeq    += TabSelectionSize[z]  \n")
	f.write("	Tabtotal_GCseq      += TabSelectionGC[z] \n")
	f.write("	Tabtotal_Protein    += TabSelectionProtein[z] \n")
	f.write("	Tabtotal_Gene       += TabSelectionGene[z] \n")
	f.write("	Tabtotal_Pseudogene += TabSelectionPseudogene[z] \n")
	f.write("	Tabtotal_ncRNA      += TabSelectionncRNA[z] \n")
	f.write("TabSelectionName.append('Genome') \n")
	f.write("TabSelectionID.append('-') \n")
	f.write("TabSelectionSize.append(Tabtotal_sizeSeq) \n")
	f.write("TabSelectionGC.append(Tabtotal_GCseq) \n")
	f.write("TabSelectionProtein.append(Tabtotal_Protein) \n")
	f.write("TabSelectionGene.append(Tabtotal_Gene) \n")
	f.write("TabSelectionPseudogene.append(Tabtotal_Pseudogene) \n")
	f.write("TabSelectionncRNA.append(Tabtotal_ncRNA) \n")

	f.write("\n\n\n")
	f.close()











########################################################################################################################
###	Create the bar charts for the chromosome percentage
###	and the variables for the annotation
########################################################################################################################
def InvariableCHR_barchart(temp) :

	f = open(temp, "a")
	f.write("########################################################################################################################\n")
	f.write("# Ajout des commandes de plotly\n\n")

	f.write("percentCHR = [] \n")
	f.write("maxPercent = 0 \n")
	f.write("for i in range(0, len(SelectionSize), 1) : \n")
	f.write("	percentCHR.append( round((100 * SelectionSize[i] / CommonDATA.totalSizeGenome), 2) ) \n")
	f.write("	if maxPercent < percentCHR[i] :  \n")
	f.write("		maxPercent = percentCHR[i] \n")
	f.write("maxPercent = maxPercent / 10 \n")

	f.write("# ajout des couleurs \n")
	f.write("colorCHR = ['darkgrey'] * CommonDATA.nbSeq_Assemble \n")
	f.write("# creation des barres pour les chromosomes en % de la taille du genome\n")

	f.write("xGenome = [] \n")
	f.write("for i in range(0, len(SelectionSize), 1) : \n")
	f.write("	xGenome.append(SelectionName[i]) \n")
	f.write("xGenome.append(' ') \n")
	f.write("xGenome.append('Reset PieChart') \n")

	f.write("yGenome = [] \n")
	f.write("for i in range(0, len(SelectionSize), 1) : \n")
	f.write("	if percentCHR[i] < 0.1 : \n")
	f.write("		yGenome.append(0.1) \n")
	f.write("	else : \n")
	f.write("		yGenome.append(percentCHR[i]) \n")
	f.write("yGenome.append(0) \n")
	f.write("yGenome.append(1) \n")

	f.write("textGenome = [] \n")
	f.write("for i in range(0, len(SelectionSize), 1) : \n")
	f.write("	textGenome.append( SelectionName[i] + ' : ' + str(SelectionSize[i]) + ' bp, ' + str(percentCHR[i]) + ' %') \n")
	f.write("textGenome.append(' ') \n")
	f.write("textGenome.append('Reset PieChart') \n")

	f.write("GenomePercentBarChart = go.Bar( x = xGenome, y = yGenome, text = textGenome, hovertemplate = '%{text}', name='Genome', marker=dict(color=colorCHR) ) \n\n")

	f.write("\n\n")
	f.close()










########################################################################################################################
###	Create the Over- Under- ChromosomeDistribution function
########################################################################################################################
def InvariableValue_PieChart(temp) :

	f = open(temp, "a")
	f.write("########################################################################################################################\n")

	f.write("NbHIT_AllTEs = [] \n")
	f.write("for i in range(0, len(SelectionSize), 1) : \n")
	f.write("	NbHIT_AllTEs.append(CommonDATA.NbHitTE_Type[i][len(CommonDATA.NbHitTE_Type[i])-1]) \n")

	f.write("Size_AllTEs = [] \n")
	f.write("for i in range(0, len(SelectionSize), 1) : \n")
	f.write("	Size_AllTEs.append(CommonDATA.SizeTE_Type[i][len(CommonDATA.SizeTE_Type[i])-1]) \n")

	# variable pour le Intergenic
	f.write("# Calculates the size of the intergenic sequence : the remaining sequence \n")
	f.write("Size_Intergenic = [] \n")
	f.write("for i in range(0, len(SelectionSize), 1) : \n")
	f.write("	Size_Intergenic.append( CommonDATA.TailleSequence[i] - ( CommonDATA.Size_Gene[i] + CommonDATA.Size_Pseudogene[i] + CommonDATA.Size_ncRNA[i] + Size_AllTEs[i] ) ) \n")
	f.write("Size_Intergenic.append( CommonDATA.totalSizeGenome - ( CommonDATA.Size_Gene[len(SelectionSize)] + CommonDATA.Size_Pseudogene[len(SelectionSize)] + CommonDATA.Size_ncRNA[len(SelectionSize)] + Size_AllTEs[i]) ) \n")

	f.write(" \n\n")
	f.close()











########################################################################################################################
###	Create the Pie chart for the genome and chromosome
########################################################################################################################
def CalculTEvalue_PieChartDATA(temp) :

	# Calculate percent for each type of TEs
	f = open(temp, "a")

	f.write("Somme_Hit_typeTE = [] \n")
	f.write("Somme_Size_typeTE = [] \n")
	f.write("Select_DASH = CommonDATA.dataFrame_infoGlobal_TE.loc[ (CommonDATA.dataFrame_infoGlobal_TE['Chr ID'] == SelectionNameID[0]), ['Type TEs', 'Nb Hit', 'Total Size'] ] \n")
	f.write("chr_Size = Select_DASH['Total Size'].tolist() \n")
	f.write("nombre_typeTEbyChrom = len(chr_Size) \n")
	f.write("for j in range(0, len(chr_Size)+1, 1) : \n")
	f.write("	Somme_Hit_typeTE.append(0) \n")
	f.write("	Somme_Size_typeTE.append(0) \n\n")

	f.write("# writing the percentage of each TE in each sequence \n")
	f.write("nbHit_Genome_typeTE = []	# list of list \n")
	f.write("Size_Genome_typeTE = []	# list of list \n")
	f.write("Label_Genome_typeTE = []	# list of list \n")
	f.write("Pull_Genome_typeTE = []	# list of list \n\n")

	f.write("# Get the data for all chromosomes \n")
	f.write("for i in range(0, len(SelectionSize), 1) : \n")
	f.write("	nbHit_TE = [] \n")
	f.write("	Size_TE = [] \n")
	f.write("	Label_TE = [] \n")
	f.write("	Pull_TE = [] \n")
	f.write("	otherTE_N = 0 \n")
	f.write("	otherTE_S = 0 \n")
	f.write("	otherTE_P = 0 \n")
	f.write("	# add all the kind of TEs that are higher than 1 % of the sequence \n")
	f.write("	Select_DASH = CommonDATA.dataFrame_infoGlobal_TE.loc[ (CommonDATA.dataFrame_infoGlobal_TE['Chr ID'] == SelectionNameID[i]), ['Type TEs', 'Nb Hit', 'Total Size'] ] \n")
	f.write("	chr_Size = Select_DASH['Total Size'].tolist() \n")
	f.write("	chr_typeTE = Select_DASH['Type TEs'].tolist() \n")
	f.write("	chr_nbHit = Select_DASH['Nb Hit'].tolist() \n")
	f.write("	for j in range(0, len(chr_Size)-1, 1) : \n")
	f.write("		# percentage pour le TE j in sequence i \n")
	f.write("		tt = round( (100 * chr_Size[j] / SelectionSize[i]), 2 ) \n")
	f.write("		Somme_Hit_typeTE[j] += chr_nbHit[j] \n")
	f.write("		Somme_Size_typeTE[j] += chr_Size[j] \n")
	f.write("		if tt >= 1.0 : \n")
	f.write("			nbHit_TE.append( chr_nbHit[j] ) \n")
	f.write("			Size_TE.append( chr_Size[j] ) \n")
	f.write("			Label_TE.append( CommonDATA.ListeObject[j] ) \n")
	f.write("			Pull_TE.append( 0 ) \n")
	f.write("		else : \n")
	f.write("			otherTE_N += chr_nbHit[j] \n")
	f.write("			otherTE_S += chr_Size[j] \n")
	f.write("			otherTE_P += tt \n")
	f.write("	if otherTE_P >= 1.0 : \n")
	f.write("		nbHit_TE.append( otherTE_N ) \n")
	f.write("		Size_TE.append( otherTE_S ) \n")
	f.write("		Label_TE.append( 'Other TEs' ) \n")
	f.write("		Pull_TE.append( 0 ) \n")
	f.write("	# add the annotations objects \n")
	f.write("	nbHit_TE.append( CommonDATA.NbHIT_Gene[i] ) \n")
	f.write("	nbHit_TE.append( CommonDATA.NbHIT_Pseudogene[i] ) \n")
	f.write("	nbHit_TE.append( CommonDATA.NbHIT_ncRNA[i] ) \n")
	f.write("	nbHit_TE.append( 0 ) \n")
	f.write("	Size_TE.append( CommonDATA.Size_Gene[i] ) \n")
	f.write("	Size_TE.append( CommonDATA.Size_Pseudogene[i] ) \n")
	f.write("	Size_TE.append( CommonDATA.Size_ncRNA[i] ) \n")
	f.write("	Size_TE.append( Size_Intergenic[i] ) \n")
	f.write("	Label_TE.append( 'Gene' ) \n")
	f.write("	Label_TE.append( 'Pseudo' ) \n")
	f.write("	Label_TE.append( 'ncRNA' ) \n")
	f.write("	Label_TE.append( 'Intergenic' ) \n")
	f.write("	Pull_TE.append( 0 ) \n")
	f.write("	Pull_TE.append( 0 ) \n")
	f.write("	Pull_TE.append( 0 ) \n")
	f.write("	Pull_TE.append( 0 ) \n")
	f.write("	nbHit_Genome_typeTE.append(nbHit_TE) \n")
	f.write("	Size_Genome_typeTE.append(Size_TE) \n")
	f.write("	Label_Genome_typeTE.append(Label_TE) \n")
	f.write("	Pull_Genome_typeTE.append(Pull_TE) \n\n")

	f.write("# Now I calculate for the whole genome \n")
	f.write("nbHit_TE = [] \n")
	f.write("Size_TE = [] \n")
	f.write("Label_TE = [] \n")
	f.write("Pull_TE = [] \n")
	f.write("otherTE_N = 0 \n")
	f.write("otherTE_S = 0 \n")
	f.write("otherTE_P = 0 \n")
	f.write("# add all the kind of TEs that are higher than 1 % of the sequence \n")
	f.write("for j in range(0, nombre_typeTEbyChrom, 1) : \n")
	f.write("	tt = round( (100 * Somme_Size_typeTE[j] / CommonDATA.totalSizeGenome), 2 ) \n")
	f.write("	if tt >= 1.0 : \n")
	f.write("		nbHit_TE.append( Somme_Hit_typeTE[j] ) \n")
	f.write("		Size_TE.append( Somme_Size_typeTE[j] ) \n")
	f.write("		Label_TE.append( CommonDATA.ListeObject[j] ) \n")
	f.write("		Pull_TE.append( 0 ) \n")
	f.write("		couleurUsed[j] = 1 \n")
	f.write("	else : \n")
	f.write("		otherTE_N += Somme_Hit_typeTE[j] \n")
	f.write("		otherTE_S += Somme_Size_typeTE[j] \n")
	f.write("		otherTE_P += tt \n")
	f.write("if otherTE_P >= 1.0 : \n")
	f.write("	nbHit_TE.append( otherTE_N ) \n")
	f.write("	Size_TE.append( otherTE_S ) \n")
	f.write("	Label_TE.append( 'Other TEs' ) \n")
	f.write("	Pull_TE.append( 0 ) \n")
	f.write("# add the annotations objects \n")
	f.write("nbHit_TE.append( CommonDATA.NbHIT_Gene[len(SelectionSize)] ) \n")
	f.write("nbHit_TE.append( CommonDATA.NbHIT_Pseudogene[len(SelectionSize)] ) \n")
	f.write("nbHit_TE.append( CommonDATA.NbHIT_ncRNA[len(SelectionSize)] ) \n")
	f.write("nbHit_TE.append( 0 ) \n")
	f.write("Size_TE.append( CommonDATA.Size_Gene[len(SelectionSize)] ) \n")
	f.write("Size_TE.append( CommonDATA.Size_Pseudogene[len(SelectionSize)] ) \n")
	f.write("Size_TE.append( CommonDATA.Size_ncRNA[len(SelectionSize)] ) \n")
	f.write("Size_TE.append( Size_Intergenic[len(SelectionSize)] ) \n")
	f.write("Label_TE.append( 'Gene' ) \n")
	f.write("Label_TE.append( 'Pseudo' ) \n")
	f.write("Label_TE.append( 'ncRNA' ) \n")
	f.write("Label_TE.append( 'Intergenic' ) \n")
	f.write("Pull_TE.append( 0 ) \n")
	f.write("Pull_TE.append( 0 ) \n")
	f.write("Pull_TE.append( 0 ) \n")
	f.write("Pull_TE.append( 0 ) \n")
	f.write("nbHit_Genome_typeTE.append(nbHit_TE) \n")
	f.write("Size_Genome_typeTE.append(Size_TE) \n")
	f.write("Label_Genome_typeTE.append(Label_TE) \n")
	f.write("Pull_Genome_typeTE.append(Pull_TE) \n\n")

	f.write("\n\n")
	f.close()










########################################################################################################################
###	Create le graph et le layout
########################################################################################################################
def Invariable_ChromosomeDistributionLayout(temp) :

	f = open(temp, "a")
	f.write("########################################################################################################################\n")
	f.write("# ajout des commandes de dash\n\n")

	f.write("ChromosomeDistribution_layout = html.Div([\n\n")

	f.write("\thtml.Div([ \n")
	f.write("\t	# ajout des sliders qui vous modifer le graph barchart et le tableau \n")
	f.write("\t	html.Div([ \n")
	f.write("\t		html.Label('Additional lines : ') \n")
	f.write("\t	], style={'width': '15%', 'vertical-align':'top', 'text-align':'center', 'display': 'inline-block'} ), \n\n")
	f.write("\t	html.Div([ \n")
	f.write("\t		# combolist \n")
	f.write("\t		dcc.Dropdown(\n")
	f.write("\t			id='AddtionalLines_Onglet2', \n")
	f.write("\t			options = [ \n")
	f.write("\t				{'label': 'No Additional Line', 'value': '0'}, \n")
	f.write("\t				{'label': 'TE Superfamily', 'value': '1'}, \n")
	f.write("\t				{'label': 'All TEs (non updated)', 'value': '2'}, \n")
	f.write("\t				{'label': 'TE Superfamily & All TEs (non updated)', 'value': '3'}, \n")
	f.write("\t			], \n")
	f.write("\t			value = '0', style={}, \n")
	f.write("\t			clearable=False, \n")
	f.write("\t		), \n")
	f.write("\t		html.Div(id='Onglet2_AddtionalLines'), \n")
	f.write("\t	], style={'width': '50%', 'display': 'inline-block'} ), \n")
	f.write("\t], style={'width': '100%', 'display': 'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n\n")



	f.write("\t# Ajout du div les 2 premiers graphes \n")
	f.write("\thtml.Div([ \n")


	# ici on place le graphe barchart : de tous les barres de chromosome et des courbes de TE
	f.write("\t	html.Div([ \n")
	f.write("\t		dcc.Graph(\n")
	f.write("\t			id = 'BarChart_Onglet2',\n")
	f.write("\t			figure={ \n")
	f.write("\t				'data': [], \n")
	f.write("\t				'layout': { \n")
	f.write("\t					'legend':{'orientation':'h'}, \n")
	f.write("\t					'title': 'Proportion of ' + CommonDATA_SelectTEs.OfficialName + ' in ' + CommonDATA.nameOrganism, \n")
	f.write("\t					'render_mode':'webgl', \n")
	f.write("\t				}, \n")
	f.write("\t			}, \n")
	f.write("\t			style = {'overflowX': 'scroll', 'overflowY': 'scroll', 'height': 720}\n")
	f.write("\t		), \n")
	f.write("\t		html.Div(id='Onglet2_BarChartLines'), \n")
	f.write("\t	], style = {'width': '66%', 'display':'inline-block'}), \n\n")


	# ici on placera le camembert de repartitions de type d'annotation
	f.write("\t	html.Div([ \n")
	f.write("\t		dcc.Graph(\n")
	f.write("\t			id = 'PieChart_Onglet2',\n")
	f.write("\t			figure={ \n")
	f.write("\t				'data' : [], \n")
	f.write("\t				'layout' : {'legend':{'orientation':'h', 'x':-0.2}, 'plot_bgcolor':'rgba(255,255,255,1)'}, \n")
	f.write("\t			}, \n")
	f.write("\t			style={'overflowX':'scroll', 'overflowY':'scroll', 'height':720}\n")
	f.write("\t		),\n")
	f.write("\t		html.Div(id='Onglet2_PieChart'), \n")
	f.write("\t	], style={'width':'33%', 'float':'right', 'display':'inline-block'}), \n\n")


	f.write("\t	html.Div(id='Onglet2_BarChart_PieChart_Div'), \n")
	f.write("\t], style={'width': '100%', 'display': 'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n")



	f.write("\t# Ajout du div qui contiendra le tableu \n")
	f.write("\thtml.Div([ \n")
	f.write("\t	# affiche le tableau \n")
	f.write("\t	dcc.Graph(\n")
	f.write("\t		id='TableOrganism_onglet2',\n")
	f.write("\t		figure={\n")
	f.write("\t			# ajout des donnees provenants de plotly \n")
	f.write("\t			'data': [], \n")
	f.write("\t			'layout': {} \n")
	f.write("\t		},\n")
	f.write("\t		style={'height': hauteurTableau, 'overflowX': 'scroll', 'overflowY': 'scroll'}\n")
	f.write("\t	),\n")
	f.write("\t	html.Div(id='Onglet2_Tableau_Div'), \n")
	f.write("\t], style={'width': '100%', 'display': 'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n")

	f.write("], style={'width': '100%', 'display': 'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'} ) \n\n\n\n")
	f.close()











########################################################################################################################
###	Create the Over- Under- ChromosomeDistribution function
########################################################################################################################
def CalculTEvalue_ForBarchart(temp, numberTE) :

	f = open(temp, "a")

	# Calculates the values and put in list for the selected TE
	if numberTE == 1 :
		f.write("\t# Here I make only 1 bar for 1 TE family or 1 Merged TE families \n")
		f.write("\tnbHit_myTE = [] \n")
		f.write("\ttotalHit_myTE = 0 \n")
		f.write("\tPercentHit_myTE = [] \n")
		f.write("\tText_Hit_myTE = [] \n")
		f.write("\tfor i in range(0, len(SelectionRefseq), 1) : \n")
		f.write("\t	Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[i])")
		f.write(" & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax)")
		f.write(" & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3])")
		f.write(", ['Size'] ] \n")
		f.write("\t	Selection_myTE = Select_myTE['Size'].tolist() \n")
		f.write("\t	nbHit_myTE.append(len(Selection_myTE)) \n")
		f.write("\t	totalHit_myTE += len(Selection_myTE) \n")

		f.write("\tfor i in range(0, len(SelectionRefseq), 1) : \n")
		f.write("\t	if totalHit_myTE > 0 : \n")
		f.write("\t		PercentHit_myTE.append( round( (100 * nbHit_myTE[i] / totalHit_myTE), 2 ) ) \n")
		f.write("\t		Text_Hit_myTE.append(str(nbHit_myTE[i]) + ' occurrences : ' + str(PercentHit_myTE[i]) + ' %') \n")
		f.write("\t	else : \n")
		f.write("\t		PercentHit_myTE.append(0) \n")
		f.write("\t		Text_Hit_myTE.append('0 occurrence : 0 %') \n")
		f.write("\tPercentHit_myTE.append( 0.0 ) \n")
		f.write("\tText_Hit_myTE.append(str(totalHit_myTE) + ' occurrences' ) \n\n\n")

	else :
		f.write("\t# Here I have many TE families \n")
		f.write("\tnbHit_myTE = [] \n")
		f.write("\ttotalHit_myTE = [] \n")
		f.write("\tPercentHit_myTE = [] \n")
		f.write("\tText_Hit_myTE = [] \n")
		f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("\t	nbHit_myTE.append([]) \n")
		f.write("\t	totalHit_myTE.append(0) \n")
		f.write("\t	PercentHit_myTE.append([]) \n")
		f.write("\t	Text_Hit_myTE.append([]) \n")

		f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("\t	for i in range(0, len(SelectionRefseq), 1) : \n")
		f.write("\t		Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[i]) & (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[j])")
		f.write(" & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax)")
		f.write(" & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3])")
		f.write(", ['Size'] ] \n")
		f.write("\t		Selection_myTE = Select_myTE['Size'].tolist() \n")
		f.write("\t		nbHit_myTE[j].append(len(Selection_myTE)) \n")
		f.write("\t		totalHit_myTE[j] += len(Selection_myTE) \n")

		f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("\t	for i in range(0, len(SelectionRefseq), 1) : \n")
		f.write("\t		if totalHit_myTE[j] > 0 : \n")
		f.write("\t			PercentHit_myTE[j].append( round( (100 * nbHit_myTE[j][i] / totalHit_myTE[j]), 2 ) ) \n")
		f.write("\t			Text_Hit_myTE[j].append(str(nbHit_myTE[j][i]) + ' occurrences : ' + str( round( (100 * nbHit_myTE[j][i] / totalHit_myTE[j]), 2 ) ) + ' %') \n")
		f.write("\t		else : \n")
		f.write("\t			PercentHit_myTE[j].append(0) \n")
		f.write("\t			Text_Hit_myTE[j].append('0 occurrence : 0 %') \n")
		f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("\t	PercentHit_myTE[j].append( 0.0 ) \n")
		f.write("\t	Text_Hit_myTE[j].append(str(totalHit_myTE[j]) + ' occurrences' ) \n\n\n")



	# Calculates the values and put in list for the superfamily TEs of selected TE
	f.write("\ttotalHit_SuperTE = 0 \n")
	f.write("\tnbHit_SuperTE = [] \n")
	f.write("\tPercentHit_SuperTE = [] \n")
	f.write("\tText_Hit_SuperTE = [] \n")

	f.write("\tif AddtionalLines_Onglet2 == '1' or AddtionalLines_Onglet2 == '3' : \n")
	f.write("\t	for i in range(0, len(SelectionRefseq), 1) : \n")
	f.write("\t		Select_superTE = CommonDATA_SelectTEs.dataFrame_superTE.loc[ (CommonDATA_SelectTEs.dataFrame_superTE['Chr ID'] == SelectionNameID[i])")
	f.write(" & (CommonDATA_SelectTEs.dataFrame_superTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_superTE['Size'] <= tailleMax)")
	f.write(" & (CommonDATA_SelectTEs.dataFrame_superTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_superTE['Similarity'] <= valueSliders[3])")
	f.write(", ['Size'] ] \n")
	f.write("\t		Selection_superTE = Select_superTE['Size'].tolist() \n")
	f.write("\t		nbHit_SuperTE.append(len(Selection_superTE)) \n")
	f.write("\t		totalHit_SuperTE += len(Selection_superTE) \n")

	f.write("\t	for i in range(0, len(SelectionRefseq), 1) : \n")
	f.write("\t		if totalHit_SuperTE > 0 : \n")
	f.write("\t			PercentHit_SuperTE.append( round( (100 * nbHit_SuperTE[i] / totalHit_SuperTE), 2 ) ) \n")
	f.write("\t			Text_Hit_SuperTE.append(str(nbHit_SuperTE[i]) + ' occurrences : ' + str(PercentHit_SuperTE[i]) + ' %') \n")
	f.write("\t		else : \n")
	f.write("\t			PercentHit_SuperTE.append(0) \n")
	f.write("\t			Text_Hit_SuperTE.append('0 occurrence : 0 %') \n")
	f.write("\t	PercentHit_SuperTE.append( 0.0 ) \n")
	f.write("\t	Text_Hit_SuperTE.append(str(totalHit_SuperTE) + ' occurrences' ) \n\n\n")



	# Get the value from the dataframe_DASH and put here for the graph
	f.write("\tPercentHit_AllTE = [] \n")
	f.write("\ttext_Hit_AllTE = [] \n")
	f.write("\tif AddtionalLines_Onglet2 == '2' or AddtionalLines_Onglet2 == '3' : \n")
	f.write("\t	for i in range(0, len(SelectionRefseq), 1) : \n")
	f.write("\t		PercentHit_AllTE.append( round( (100 * CommonDATA.NbHitTE_Type[i][len(CommonDATA.NbHitTE_Type[i])-1] / CommonDATA.Total_Hit_AllTEs), 2 ) ) \n")
	f.write("\t		text_Hit_AllTE.append( \"str(CommonDATA.NbHitTE_Type[i][len(CommonDATA.NbHitTE_Type[i])-1]) occurrences : str(PercentHit_AllTE[0]) %\" ) \n")
	f.write("\t	PercentHit_AllTE.append( 0.0 ) \n")

	f.write("\n\n\n")
	f.close()










########################################################################################################################
###	Calculate the Chi Square for the chromosome distribution
########################################################################################################################
def Calculate_ChiSquare(temp, numberTE) :

	f = open(temp, "a")
	f.write("\t#Calculate the Chi2 of over- under-represented in chromosome \n")
	f.write("\tglobal GenomePercentBarChart \n")
	f.write("\tGenomePercentBarChart2 = GenomePercentBarChart \n")
	f.write("\tOverRepresented = [] \n")

	if numberTE == 1 :
		f.write("\tlisteObs = [] \n")
		f.write("\tlistTheo = [] \n")
		f.write("\tfor i in range(0, len(SelectionSize), 1) : \n")
		f.write("\t	OverRepresented.append(0) \n")
		f.write("\t	observedValue = int( round( totalHit_myTE * percentCHR[i] / 100) ) \n")
		f.write("\t	if observedValue >= 5 : \n")
		f.write("\t		listeObs.append( nbHit_myTE[i] ) \n")
		f.write("\t		listTheo.append( observedValue ) \n")
		f.write("\tif len(listeObs) > 0 : \n")
		f.write("\t	chi_statistic, p_value = chisquare(listeObs, listTheo) \n")
		f.write("\t	critique = chi2.ppf(q = 0.99, df = len(listeObs)) \n")
		f.write("\t	if float(critique) < float(chi_statistic) and float(p_value) <= 0.01 :	# There are over- and under- represented bias in chromosome \n")
		f.write("\t		k = 0 \n")
		f.write("\t		for i in range(0, len(SelectionSize), 1) : \n")
		f.write("\t			observedValue = int( round( totalHit_myTE * percentCHR[i] / 100) ) \n")
		f.write("\t			if observedValue >= 5 : \n")
		f.write("\t				if float(observedValue + observedValue/4) <= float(listeObs[k]) : 	# Over-represented more thant 25% than theoric \n")
		f.write("\t					OverRepresented[i] += 1 \n")
		f.write("\t				k += 1\n")
		f.write("\t		for i in range(0, len(SelectionSize), 1) : \n")
		f.write("\t			if OverRepresented[i] == 1 : \n")
		f.write("\t				colorCHR[i] = Couleur.couleurSelectTE[0] \n")
		f.write("\t		GenomePercentBarChart2 = go.Bar( x = xGenome, y = yGenome, text = textGenome, hovertemplate = '%{text}', name='Genome', marker=dict(color=colorCHR) ) \n\n")
	else  :
		f.write("\tfor i in range(0, len(SelectionSize), 1) : \n")
		f.write("\t	OverRepresented.append(0) \n")
		f.write("\tlisteObs = [[]] \n")
		f.write("\tlistTheo = [[]] \n")
		f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("\t	listeObs.append([]) \n")
		f.write("\t	listTheo.append([]) \n")
		f.write("\t	for i in range(0, len(SelectionSize), 1) : \n")
		f.write("\t		observedValue = int( round( totalHit_myTE[j] * percentCHR[i] / 100) ) \n")
		f.write("\t		if observedValue >= 5 : \n")
		f.write("\t			listeObs[j].append( nbHit_myTE[j][i] ) \n")
		f.write("\t			listTheo[j].append( observedValue ) \n")
		f.write("\t	if len(listeObs[j]) > 0 : \n")
		f.write("\t		chi_statistic, p_value = chisquare(listeObs[j], listTheo[j]) \n")
		f.write("\t		critique = chi2.ppf(q = 0.99, df = len(listeObs[j])) \n")
		f.write("\t	if float(critique) < float(chi_statistic) and float(p_value) <= 0.01 :	# There are over- and under- represented bias in chromosome \n")
		f.write("\t		k = 0 \n")
		f.write("\t		for i in range(0, len(SelectionSize), 1) : \n")
		f.write("\t			observedValue = int( round( totalHit_myTE[j] * percentCHR[i] / 100) ) \n")
		f.write("\t			if observedValue >= 5 : \n")
		f.write("\t				if float(observedValue + observedValue/4) <= float(listeObs[j][k]) : 	# Over-represented more thant 25% than theoric \n")
		f.write("\t					OverRepresented[i] += (j+1) * (j+1) \n")
		f.write("\t				k += 1\n")
		f.write("\t		for i in range(0, len(SelectionSize), 1) : \n")
		f.write("\t			if OverRepresented[i] == 1 : \n")
		f.write("\t				colorCHR[i] = Couleur.couleurSelectTE[0] \n")
		f.write("\t			elif OverRepresented[i] == 4 : \n")
		f.write("\t				colorCHR[i] = Couleur.couleurSelectTE[1] \n")
		f.write("\t			elif OverRepresented[i] == 9 : \n")
		f.write("\t				colorCHR[i] = Couleur.couleurSelectTE[2] \n")
		f.write("\t			else : \n")
		f.write("\t				if OverRepresented[i] != 0 : \n")
		f.write("\t					colorCHR[i] = CommonDATA_SelectTEs.CouleurSuperTE \n")
		f.write("\t		GenomePercentBarChart2 = go.Bar( x = xGenome, y = yGenome, text = textGenome, hovertemplate = '%{text}', name='Genome', marker=dict(color=colorCHR) ) \n\n")

	f.write("\n\n\n")
	f.close()










########################################################################################################################
###	Create TE Lines for the barchart
########################################################################################################################
def TELine_In_Barchart(temp, numberTE) :

	f = open(temp, "a")

	f.write("\t# creation de la ligne de % des TE par chromosome du nombre de TE dans le genome\n")
	if numberTE == 1 :
		f.write("\txLine_MyTE = go.Scatter( x = xGenome, y = PercentHit_myTE"", text = Text_Hit_myTE, hovertemplate = '<b>%{text}</b>', name = CommonDATA_SelectTEs.OfficialName, mode = 'lines+markers', line=dict(color=Couleur.couleurSelectTE[0], width=3, dash='dash') ) \n\n")
	else :
		for i in range(0, numberTE, 1) :
			f.write("\txLine_MyTE_" + str(i) + " = go.Scatter( x = xGenome, y = PercentHit_myTE[" + str(i) + "], text = Text_Hit_myTE[" + str(i) + "], hovertemplate = '<b>%{text}</b>', name = CommonDATA_SelectTEs.list_selection_TE[" + str(i) + "], mode = 'lines+markers', line=dict(color=Couleur.couleurSelectTE[" + str(i) + "], width=3, dash='dash') ) \n")
		f.write("\n")

	f.write("\txLine_SuperTE = go.Scatter( x = xGenome, y = [], text = Text_Hit_SuperTE, hovertemplate = '%{text}', name = CommonDATA_SelectTEs.SuperfamilyTE, mode='lines+markers', line=dict(color = CommonDATA_SelectTEs.CouleurSuperTE, width=2, dash='dot'), marker=dict(symbol='square-dot') ) \n")
	f.write("\tif AddtionalLines_Onglet2 == '1' or AddtionalLines_Onglet2 == '3' : \n")
	f.write("\t	xLine_SuperTE = go.Scatter( x = xGenome, y = PercentHit_SuperTE, text = Text_Hit_SuperTE, hovertemplate = '%{text}', name = CommonDATA_SelectTEs.SuperfamilyTE, mode='lines+markers', line=dict(color = CommonDATA_SelectTEs.CouleurSuperTE, width=2, dash='dot'), marker=dict(symbol='square-dot', size=3) ) \n\n")

	f.write("\txLine_AllTE = go.Scatter( x = xGenome, y = [], text = Text_Hit_SuperTE, hovertemplate = '%{text}', name = 'All TEs', mode='lines+markers', line=dict(color='black', width=2), marker=dict(symbol='diamond-dot', size=3) ) \n")
	f.write("\tif AddtionalLines_Onglet2 == '2' or AddtionalLines_Onglet2 == '3' : \n")
	f.write("\t	xLine_AllTE = go.Scatter( x = xGenome, y = PercentHit_AllTE, text = Text_Hit_SuperTE, hovertemplate = '%{text}', name = 'All TEs', mode='lines+markers', line=dict(color='black', width=2), marker=dict(symbol='diamond-dot', size=3) ) \n\n")

	f.write("\n\n\n")
	f.close()










########################################################################################################################
###	Create the Size Distribution function in callback
########################################################################################################################
def CreateCallBack_BarChart_Onglet2(temp, numberTE) :

	# Correspondance entre le combobox et les graphes de distribution de taille
	f = open(temp, "a")
	f.write("########################################################################################################################\n")
	f.write("# Callbacks for the Barchart\n")
	f.write("# Ajout du combobox de plotly pour le genome + l'ensemble des chromosomes size distribution\n\n")
	f.write("@app.callback(Output('BarChart_Onglet2', 'figure'), \n")
	f.write("	[Input('memory', 'data'), Input('AddtionalLines_Onglet2', 'value')], ) \n\n")

	f.write("def update_Onglet2(valueSliders, AddtionalLines_Onglet2):\n")
	f.write("\t# valueSliders[0] and valueSliders[1] are boundary for the size slider\n")
	f.write("\t# valueSliders[2] and valueSliders[3] are boundary for the similarity slider\n\n")

	# prise en compte d'1 ou plusieurs familles de TEs
	f.write("\t# get the total of all TE for each chromosome and in genome \n")
	f.write("\t# get the total of the same superfamily TE for each chromosome and in genome \n")
	f.write("\t# get the percentage for each chromosome and in genome \n")
	f.write("\tMinConsensus = 1000000 \n")
	f.write("\tMaxConsensus = 0 \n")
	f.write("\tif len(CommonDATA_SelectTEs.list_selection_TE) == 1 : \n" )
	f.write("\t	MinConsensus = CommonDATA_SelectTEs.TailleConsensus[0] \n")
	f.write("\t	MaxConsensus = CommonDATA_SelectTEs.TailleConsensus[0] \n")
	f.write("\telse : \n")
	f.write("\t	for i in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("\t 		if MinConsensus > CommonDATA_SelectTEs.TailleConsensus[i] : \n")
	f.write("\t 			MinConsensus = CommonDATA_SelectTEs.TailleConsensus[i] \n")
	f.write("\t 		if MaxConsensus < CommonDATA_SelectTEs.TailleConsensus[i] : \n")
	f.write("\t 			MaxConsensus = CommonDATA_SelectTEs.TailleConsensus[i] \n")
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



	# Prepare data for the graphs
	CalculTEvalue_ForBarchart(temp, numberTE)
	# Calculate the bias or not of the TE distribution in chromosome
	Calculate_ChiSquare(temp, numberTE)
	# Create the TE lines for the barchart
	TELine_In_Barchart(temp, numberTE)



	f = open(temp, "a")
	f.write("\tfig = { \n")

	if numberTE == 1 :
		f.write("\t	'data': [GenomePercentBarChart2, xLine_AllTE, xLine_SuperTE, xLine_MyTE], \n")
	else :
		f.write("\t	'data': [GenomePercentBarChart2, xLine_AllTE, xLine_SuperTE, ")
		for i in range(0, numberTE, 1) :
			f.write("xLine_MyTE_" + str(i) + ", ")
		f.write("], \n")

	f.write("\t	'layout': { \n")
	f.write("\t		'legend':{'orientation':'h'}, \n")

	if numberTE == 1 :
		f.write("\t		'title': 'Proportion of ' + CommonDATA_SelectTEs.OfficialName + ' in ' + CommonDATA.nameOrganism, \n")
	else :
		f.write("\t		'title': 'Proportion of ' ")
		for i in range(0, numberTE, 1) :
			f.write("+ CommonDATA_SelectTEs.list_selection_TE[" + str(i) + "] + ', ' ")
		f.write("+ ' in ' + CommonDATA.nameOrganism, \n")

	f.write("\t	}, \n")
	f.write("\t} \n")
	f.write("\treturn fig\n")
	f.write("\n\n\n\n\n")
	f.close()











########################################################################################################################
###	Create The Piechart with the data
########################################################################################################################
def CreateCallBack_PieChart_Onglet2(temp) :

	f = open(temp, "a")
	f.write("########################################################################################################################\n")
	f.write("# Callbacks for the PieChart\n")

	f.write("@app.callback( \n")
	f.write("\tOutput('PieChart_Onglet2', 'figure'), \n")
	f.write("\t[Input('BarChart_Onglet2', 'hoverData')]\n")
	f.write(")\n\n")

	f.write("def updatePiechart(BarChart_Onglet2) : \n\n")
	f.write("\t# creation de la figure \n")
	f.write("\tchromsomeID = 0 \n")
	f.write("\tsequenceID = '' \n")
	f.write("\tif BarChart_Onglet2 == None : \n")
	f.write("\t	chromsomeID = len(SelectionSize) \n")
	f.write("\t	sequenceID = 'Detailed distribution of TEs and Annotations <br> in Genome of ' + CommonDATA.nameOrganism \n")
	f.write("\telse: \n")
	f.write("\t	chromsomeID = int(BarChart_Onglet2['points'][0]['pointIndex']) \n")
	f.write("\t	sequenceID = str(BarChart_Onglet2['points'][0]['x']) \n")
	f.write("\t	sequenceID = 'Detailed distribution of TEs and Annotations <br> in ' + sequenceID + ' of ' + CommonDATA.nameOrganism \n")
	f.write("\t	if chromsomeID >= len(SelectionSize) : \n")
	f.write("\t		chromsomeID = len(SelectionSize) \n")
	f.write("\t		sequenceID = 'Detailed distribution of Genome'\n")

	# Adding the TEname value to the list
	f.write("\tLabels = Label_Genome_typeTE[chromsomeID] \n")
	f.write("\tPourcentage = Size_Genome_typeTE[chromsomeID] \n")
	f.write("\tDecroche = Pull_Genome_typeTE[chromsomeID] \n")

	# Bug ICI sur les couleurs : Ex les doivent etre rouge ils sont en bleus
	f.write("\t# nouveau tableau des couleurs utilisees \n")
	f.write("\tfor z in range(0, len(couleurUsed), 1) : \n")
	f.write("\t	if couleurUsed[z] == 1 : \n")
	f.write("\t		newColorDict.append(Couleur.couleurV2[z]) \n")
	f.write("\tnewColorDict.append(Couleur.couleurV2[23]) \n")
	f.write("\tnewColorDict.append(Couleur.couleurV2[24]) \n")
	f.write("\tnewColorDict.append(Couleur.couleurV2[25]) \n")
	f.write("\tnewColorDict.append(Couleur.couleurV2[26]) \n")

	f.write("\tPieCharDetails_onglet2 = go.Pie( labels = Labels, values = Pourcentage, hole=.33, marker=dict(colors=newColorDict), pull=Decroche, sort=False ) \n\n")

	f.write("\tfig = { \n")
	f.write("\t	'data': [PieCharDetails_onglet2], \n")
	f.write("\t	'layout':{ \n")
	f.write("\t		'title':sequenceID, \n")
	f.write("\t		'legend':{'orientation':'h', 'x':-0.2} \n")
	f.write("\t	} \n")
	f.write("\t} \n")
	f.write("\treturn fig\n")

	f.write("\n\n\n\n\n")
	f.close()











########################################################################################################################
###	Create the graph and the layout that contains the chromosomes
########################################################################################################################
def TableauInCallback(temp, numberTE, pathVisualNEW) :

	f = open(temp, "a")

	f.write("\t# get the total of all TE for each chromosome and in genome \n")
	f.write("\t# get the total of the same superfamily TE for each chromosome and in genome \n")
	f.write("\t# get the percentage for each chromosome and in genome \n")
	f.write("\tMinConsensus = 1000000 \n")
	f.write("\tMaxConsensus = 0 \n")
	f.write("\tif len(CommonDATA_SelectTEs.list_selection_TE) == 1 : \n" )
	f.write("\t	MinConsensus = CommonDATA_SelectTEs.TailleConsensus[0] \n")
	f.write("\t	MaxConsensus = CommonDATA_SelectTEs.TailleConsensus[0] \n")
	f.write("\telse : \n")
	f.write("\t	for i in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("\t 		if MinConsensus > CommonDATA_SelectTEs.TailleConsensus[i] : \n")
	f.write("\t 			MinConsensus = CommonDATA_SelectTEs.TailleConsensus[i] \n")
	f.write("\t 		if MaxConsensus < CommonDATA_SelectTEs.TailleConsensus[i] : \n")
	f.write("\t 			MaxConsensus = CommonDATA_SelectTEs.TailleConsensus[i] \n")
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

	# Calculates the values and put in list for the selected TE
	if numberTE == 1 :
		f.write("\t# Here I make only 1 bar for 1 TE family or 1 Merged TE families \n")
		f.write("\tnbHit_myTE = [] \n")
		f.write("\ttotalHit_myTE = 0 \n")
		f.write("\tfor i in range(0, len(SelectionRefseq), 1) : \n")
		f.write("\t	Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[i])")
		f.write(" & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax)")
		f.write(" & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3])")
		f.write(", ['Size'] ] \n")
		f.write("\t	Selection_myTE = Select_myTE['Size'].tolist() \n")
		f.write("\t	nbHit_myTE.append(len(Selection_myTE)) \n")
		f.write("\t	totalHit_myTE += len(Selection_myTE) \n")
		f.write("\tnbHit_myTE.append(totalHit_myTE) \n\n\n")

	else :
		f.write("\t# Here I have many TE families \n")
		f.write("\tnbHit_myTE = [] \n")
		f.write("\ttotalHit_myTE = [] \n")
		f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("\t	nbHit_myTE.append([]) \n")
		f.write("\t	totalHit_myTE.append(0) \n")
		f.write("\tfor i in range(0, len(SelectionRefseq), 1) : \n")
		f.write("\t	for j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("\t		Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Chr ID'] == SelectionName[i]) & (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[j])")
		f.write(" & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax)")
		f.write(" & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3])")
		f.write(", ['Size'] ] \n")
		f.write("\t		Selection_myTE = Select_myTE['Size'].tolist() \n")
		f.write("\t		nbHit_myTE[j].append(len(Selection_myTE)) \n")
		f.write("\t		totalHit_myTE[j] += len(Selection_myTE) \n")
		f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("\t	nbHit_myTE[j].append(totalHit_myTE[j]) \n\n\n")

	f.write("\t# Ecriture des variables qui vont remplir le tableau \n")
	f.write("\ttemp = [] \n")
	f.write("\tfor i in range(0, len(TabSelectionSize), 2) : \n")
	f.write("\t	temp.append('GhostWhite') \n")
	f.write("\t	temp.append('LightGrey') \n")
	f.write("\tif(len(TabSelectionSize) % 2 == 1) : \n")
	f.write("\t	temp.append('GhostWhite') \n")
	f.write("\tCouleurCell = []  \n")
	f.write("\tfor j in range(0, 9+")
	f.write(str(numberTE))
	f.write(", 1) : \n")
	f.write("\t	CouleurCell.append(temp) \n")

	f.write("\tNameCell = []  						# 1st column : name of chromosome \n")
	f.write("\tfor i in range(0, len(TabSelectionSize), 1) : \n")
	f.write("\t	NameCell.append(TabSelectionName[i]) \n")
	f.write("\tIDCell = []  						# 2nd column : ID of the sequence \n")
	f.write("\tfor i in range(0, len(TabSelectionSize), 1) : \n")
	f.write("\t	IDCell.append(TabSelectionID[i]) \n")
	f.write("\tSizeCell = []  						# 3rd column : size of the sequence \n")
	f.write("\tfor i in range(0, len(TabSelectionSize), 1) : \n")
	f.write("\t	SizeCell.append(TabSelectionSize[i]) \n")
	f.write("\tGCCell = []  						# 4th column : GC % the sequence \n")
	f.write("\tfor i in range(0, len(TabSelectionSize), 1) : \n")
	f.write("\t	GCCell.append(TabSelectionGC[i]) \n")
	f.write("\tProteinCell = []  						# 5th column : proteins in the sequence \n")
	f.write("\tfor i in range(0, len(TabSelectionSize), 1) : \n")
	f.write("\t	ProteinCell.append(TabSelectionProtein[i]) \n")
	f.write("\tGeneCell = []  						# 6th column : genes in the sequence \n")
	f.write("\tfor i in range(0, len(TabSelectionSize), 1) : \n")
	f.write("\t	GeneCell.append(TabSelectionGene[i]) \n")
	f.write("\tPseudoCell = []  						# 7th column : Pseudogene in the sequence \n")
	f.write("\tfor i in range(0, len(TabSelectionSize), 1) : \n")
	f.write("\t	PseudoCell.append(TabSelectionPseudogene[i]) \n")
	f.write("\tRNACell = []  						# 8th column : ncRNAs in the sequence \n")
	f.write("\tfor i in range(0, len(TabSelectionSize), 1) : \n")
	f.write("\t	RNACell.append(TabSelectionncRNA[i]) \n")

	if numberTE == 1 :
		f.write("\tmyTECell = []  						# 9th column : my TE \n")
		f.write("\tfor i in range(0, len(TabSelectionSize), 1) : \n")
		f.write("\t	myTECell.append(nbHit_myTE[i]) \n")
	else :
		f.write("\tmyTECell = []  						# 9th, 10th ... column : my TEs \n")
		f.write("\tfor j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
		f.write("\t	myTECell.append([]) \n")
		f.write("\t	for i in range(0, len(TabSelectionSize), 1) : \n")
		f.write("\t		myTECell[j].append(nbHit_myTE[j][i]) \n")

	f.write("\tAllTEsCell = []  						# 10th column : ALL TEs \n")
	f.write("\tfor i in range(0, len(SelectionSize), 1) : \n")
	f.write("\t	AllTEsCell.append(CommonDATA.NbHitTE_Type[i][len(CommonDATA.NbHitTE_Type[i])-1]) \n")
	f.write("\tAllTEsCell.append(CommonDATA.Total_Hit_AllTEs) \n")


	# ecriture du tableau qui resume les valeurs
	###############################################################################################################################################################
	# Import the recently created modules
	pathSelectTE = os.path.realpath(pathVisualNEW + '/Functions/CommonDATA_SelectTEs.py')
	loaderSelectTE = importlib.util.spec_from_file_location('CommonDATA_SelectTEs', pathSelectTE)
	moduleSelectTE = importlib.util.module_from_spec(loaderSelectTE)
	loaderSelectTE.loader.exec_module(moduleSelectTE)


	if numberTE > 1 :
		dictCell = '\t	cells = dict(values = [ NameCell, IDCell, SizeCell, GCCell, ProteinCell, GeneCell, PseudoCell, RNACell, '
		for i in range(0, numberTE, 1) :
			dictCell += 'myTECell[' + str(i) + '], '
		dictCell += 'AllTEsCell ], \n'

	f.write("\t# creation du tableau avec les valeurs obtenus\n")
	f.write("\tTableTE_onglet2 = go.Table(\n")

	if numberTE == 1 :
		f.write("\t	header=dict(values=[ '<b>Chromosome</b>', '<b>Name Seq</b>', '<b>Size (Mb)</b>', '<b>GC %</b>', '<b>Proteins</b>', '<b>Genes</b>', '<b>Pseudo</b>', '<b>ncRNAs</b>', '<b>' + CommonDATA_SelectTEs.OfficialName + '</b>', '<b>All TEs</b>' ], \n")
	else :
		f.write("\t	header=dict(values=[ '<b>Chromosome</b>', '<b>Name Seq</b>', '<b>Size (Mb)</b>', '<b>GC %</b>', '<b>Proteins</b>', '<b>Genes</b>', '<b>Pseudo</b>', '<b>ncRNAs</b>', ")
		for i in range(0, numberTE, 1) :
			f.write('\'<b>' + moduleSelectTE.list_selection_TE[i] + '</b>\', ')
		f.write(" '<b>All TEs</b>' ], \n")

	f.write("\t		line_color='black',\n")
	f.write("\t		fill_color='darkgrey',\n")
	f.write("\t		font=dict(color='white', size=16), \n")
	f.write("\t		align='center'),\n")

	if numberTE == 1 :
		f.write("\t	cells=dict(values=[ NameCell, IDCell, SizeCell, GCCell, ProteinCell, GeneCell, PseudoCell, RNACell, myTECell, AllTEsCell ],  \n")
	else :
		f.write(dictCell)

	f.write("\t	line_color='darkslategray',\n")
	f.write("\t	fill_color = CouleurCell, \n")	# le nombre de colonnes
	f.write("\t	font=dict(size=14), \n")
	f.write("\t	align='center', height=30) \n")
	f.write("\t) \n")

	f.write("\n\n\n\n")
	f.close()










########################################################################################################################
###	Create The table with the data
########################################################################################################################
def CreateCallBack_Tableau_Onglet2(temp, numberTE, pathVisualNEW) :

	f = open(temp, "a")
	f.write("########################################################################################################################\n")
	f.write("# Callbacks for the Table\n")

	f.write("@app.callback( \n")
	f.write("\tOutput('TableOrganism_onglet2', 'figure'), \n")
	f.write("\t[Input('memory', 'data')]\n")
	f.write(")\n\n")

	f.write("def updateTable(valueSliders) : \n\n")
	f.close()


	TableauInCallback(temp, numberTE, pathVisualNEW)


	f = open(temp, "a")
	f.write("\tfig = { \n")
	f.write("\t	'data': [TableTE_onglet2], \n")
	f.write("\t	'layout':{ \n")
	f.write("\t		'title': 'Table of biological objects in ' + CommonDATA.nameOrganism , \n")
	f.write("\t		'legend':{} \n")
	f.write("\t	} \n")
	f.write("\t} \n")
	f.write("\treturn fig\n")

	f.write("\n\n\n\n")
	f.close()










########################################################################################################################
###	Create the Over- Under- ChromosomeDistribution function
########################################################################################################################
def ChromosomeDistribution(pathVisualNEW, numberTE):

	# taille de la figure et echelle des chromosomes
	#largeurFig = nbSeq_Assemble * 50 + 100
	#hauteurFig = 1000

	# Ajout des librairies python pour le serveur
	temp = pathVisualNEW + '/Functions/ChromosomeDistribution.py'
	f = open(temp, "w")

	f.write("#!/usr/bin/env python3\n")
	f.write("# -*- coding: utf-8 -*-\n")
	f.write("from scipy.stats import chisquare \n")
	f.write("from scipy.stats import chi2 \n")
	f.write("import dash\n")
	f.write("import dash_daq as daq\n")
	f.write("import dash_core_components as dcc\n")
	f.write("import dash_html_components as html\n")
	f.write("import plotly.graph_objects as go\n")
	f.write("from dash.dependencies import Input, Output\n")
	f.close()
	with open(temp, "a") as file:
		file.write("""
from app import app
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


	# Adding permanent data for the whole script
	Invariable_Script(temp)
	# Adding permanent data for barchart graph
	InvariableCHR_barchart(temp)
	# adding permanent data for the piechart
	InvariableValue_PieChart(temp)
	# Adding permanent for piechart graph
	CalculTEvalue_PieChartDATA(temp)

	# Adding the Hiv that will contains the HTML page
	Invariable_ChromosomeDistributionLayout(temp)



	# Updates the graph based on sliders and dropdown
	CreateCallBack_BarChart_Onglet2(temp, numberTE)
	# Update the piechart
	CreateCallBack_PieChart_Onglet2(temp)
	# Update the table chart
	CreateCallBack_Tableau_Onglet2(temp, numberTE, pathVisualNEW)
