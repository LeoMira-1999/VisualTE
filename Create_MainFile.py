#!/usr/bin/python3
import os
import sys
import importlib
import importlib.util
from . import Create_CommonHead




########################################################################################################################
### Create app.py
########################################################################################################################

def EcrireApp(pathVisual):
	temp = pathVisual + '/app.py'
	f = open(temp, "w")

	f.write("#!/usr/bin/env python3\n")
	f.write("# -*- coding: utf-8 -*-\n")
	f.write("import dash \n")
	f.write("import pandas as pd \n\n")

	f.write("# ajout des commandes de dash\n\n")

	f.write("# recuperation d'un style CSS pour dash\n")
	f.write("external_stylesheets = ['../css/dash-wind-streaming.css']\n")
	f.write("app = dash.Dash(__name__, external_stylesheets=external_stylesheets)\n")
	f.write("server = app.server\n\n")

	f.write("# elime les erreurs fait par callback ?\n")
	f.write("app.config.suppress_callback_exceptions = True\n\n")

	f.close()





########################################################################################################################
### Create VisualTE3.py
########################################################################################################################

def EcrireVisualTE(pathVisual, pathVisualNEW, moduleSelectTE, moduleCommonDATA):

	temp = pathVisualNEW + '/VisualTE3.py'
	f = open(temp, "w")

	f.write("#!/usr/bin/env python3\n")
	f.write("# -*- coding: utf-8 -*-\n\n")

	f.write("# import les differentes librairies et fichier python\n")
	f.write("import dash\n")
	f.write("import pandas as pd \n")
	f.write("import dash_html_components as html\n")
	f.write("import dash_core_components as dcc\n")
	f.write("import plotly.graph_objects as go\n")
	f.write("from dash.dependencies import Input, Output\n\n")

	f.write("# importe 1 fichier par function\n")
	f.write("from app import app\n")
	f.write("from Functions import Couleur \n")
	f.write("from Functions import GenomeBrowser, ChromosomeDistribution, GeneralFeatures, SimilarityOccurrences, TEEnvironment \n")
	f.write("from Functions import TEGeneDistance, NeighboringGeneFunction, OverlappingTFBS, SummaryTable\n\n\n\n")



	###############################################################################################################################################################
	####	Prepare le style pour les pages HTML
	###############################################################################################################################################################
	f.write("########################################################################################################################\n")
	f.write("# ajout d'un style CSS pour les onglets ! Temporaire !\n")
	f.write("tabs_styles = {\n")
	f.write("	'height': '40px'\n")
	f.write("}\n")
	f.write("tab_style = {\n")
	f.write("	'borderBottom': '1px solid #d6d6d6',\n")
	f.write("	'padding': '6px',\n")
	f.write("	'fontWeight': 'bold'\n")
	f.write("}\n")
	f.write("tab_selected_style = {\n")
	f.write("	'borderTop': '1px solid #d6d6d6',\n")
	f.write("	'borderBottom': '1px solid #d6d6d6',\n")
	f.write("	'backgroundColor': '#119DFF',\n")
	f.write("	'color': 'white',\n")
	f.write("	'padding': '6px'\n")
	f.write("}\n")
	f.write("hr = {\n")
	f.write("	'border': '1px dotted #8A2BE2'\n")
	f.write("}\n")
	f.write("\n\n\n")



	###############################################################################################################################################################
	####	Prepare les liens URL pour toutes les fonctions
	###############################################################################################################################################################
	f.write("########################################################################################################################\n")
	f.write("# ajout des commandes de dash\n")
	f.write("app.layout = html.Div([ \n")
	f.close()

	# Variables a changer avec les nouvelles fonctions !
	otherOnglets = ['TE Genome Browser', 'TE Chromosome Distribution', 'TE General Features', 'TE Similarity Occurrences', 'TE Genetic Environment', 'TE - Neighboring Gene Distance', 'TE - Neighboring Gene Function', 'Overlapping TFBS', 'Summary Table']   
	urlOnglets = ['GenomeBrowser', 'ChromosomeDistribution', 'GeneralFeatures', 'SimilarityOccurrences', 'TEEnvironment', 'TEDistance', 'NeighboringGeneFunction', 'OverlappingTFBS', 'SummaryTable']
	# Afficher la partie 'commune' des fonctions
	Create_CommonHead.CommonLink(temp, otherOnglets, urlOnglets)

	f = open(temp, "a")
	f.write("	dcc.Location(id='url', refresh=False), \n")
	f.write("	html.Div(id='page-content') \n")
	f.write("], style={'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'} )\n\n\n\n\n\n")


	f.write("########################################################################################################################\n")
	f.write("@app.callback( \n")
	f.write("	Output('page-content', 'children'), \n")
	f.write("	[Input('tabs-function', 'value')] \n")
	f.write(") \n\n")

	f.write("def display_page(tab) : \n")
	f.write("	if tab == 'Introduction / Help' : \n")
	f.write("		welcome = html.Div([ \n")
	f.write("			html.H4('Welcome to VisualTE v3 for the ")
	f.write(moduleSelectTE.OfficialName)
	f.write(" family in ")
	f.write(moduleCommonDATA.nameOrganism)
	f.write("'), \n")
	f.write("			html.H4('Click on the link above to start the analysis !'), \n")
	f.write("		]) \n")
	f.write("		return welcome \n")
	f.write("	elif tab == 'TE Genome Browser' : \n")
	f.write("		return GenomeBrowser.GenomeBrowser_layout \n")
	f.write("	elif tab == 'TE Chromosome Distribution' : \n")
	f.write("		return ChromosomeDistribution.ChromosomeDistribution_layout \n")
	f.write("	elif tab == 'TE General Features' : \n")
	f.write("		return GeneralFeatures.GeneralFeatures_layout \n")
	f.write("	elif tab == 'Relationship Between TE Occurrences' : \n")
	f.write("		return SimilarityOccurrences.SimilarityOccurrences_layout \n")
	f.write("	elif tab == 'TE Genetic Environment' : \n")
	f.write("		return TEEnvironment.TEEnvironment_layout \n")
	f.write("	elif tab == 'TE - Neighboring Gene Distance' : \n")
	f.write("		return TEGeneDistance.TEGeneDistance_layout \n")
	f.write("	elif tab == 'TE - Neighboring Gene Function' : \n")
	f.write("		return NeighboringGeneFunction.NeighboringGeneFunction_layout \n")
	f.write("	elif tab == 'Overlapping TFBS' : \n")
	f.write("		return OverlappingTFBS.OverlappingTFBS_layout \n")
	f.write("	elif tab == 'Summary Table' : \n")
	f.write("		return SummaryTable.SummaryTable_layout \n")
	f.write("	else: \n")
	f.write("		welcome = html.Div([ \n")
	f.write("			html.H4('Welcome to VisualTE v3 for the ")
	f.write(moduleSelectTE.OfficialName)
	f.write(" family in ")
	f.write(moduleCommonDATA.nameOrganism)
	f.write("'), \n")
	f.write("			html.H4('Click on the link above to start the analysis !'), \n")
	f.write("		]) \n")
	f.write("		return welcome \n")
	f.write("\n\n\n\n\n\n")
	
	f.write("########################################################################################################################\n")
	f.write("# ici le callback qui donne le result via le store a tous les callback \n")
	f.write("@app.callback( \n")
	f.write("	Output('memory', 'data'), \n")
	f.write("	[Input('SizeSlider_commun', 'value'), Input('SimilaritySlider_commun', 'value')] \n")
	f.write(") \n")
	f.write("def update_output(x, y) : \n")
	
	#tempFile = pathVisualNEW + '/Functions/Sliders.txt'
	#f.write("	file = open('" + str(tempFile) + "', 'w') \n")
	#f.write("	file.write(str(x[0]) + '\\n') \n")
	#f.write("	file.write(str(x[1]) + '\\n') \n")
	#f.write("	file.write(str(y[0]) + '\\n') \n")
	#f.write("	file.write(str(y[1]) + '\\n') \n")
	#f.write("	file.close() \n\n")
	
	f.write("	L = [ x[0], x[1], y[0], y[1] ] \n")
	f.write("	return L \n\n\n\n")




	###############################################################################################################################################################
	####	Lancement du serveur	
	###############################################################################################################################################################
	f.write("########################################################################################################################\n")
	f.write("# Lancement du 'serveur' de dash - plotly\n")
	f.write("if __name__ == '__main__':\n")
	f.write("	app.run_server(debug=True, host='0.0.0.0', port=8050)\n\n\n")
	f.close()
	
	numberTE = 1
	if len(moduleSelectTE.list_selection_TE) > 1 and moduleSelectTE.OfficialName[0:5] != 'Merge' :
		numberTE = len(moduleSelectTE.list_selection_TE)
	
	return moduleCommonDATA.nbSeq_Assemble, numberTE



