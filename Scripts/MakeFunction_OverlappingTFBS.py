#!/usr/bin/python3
import os
import sys
import importlib
import importlib.util
import pandas as pd
import plotly.graph_objs as go



########################################################################################################################
###
########################################################################################################################
def Create_layout(temp):

	f = open(temp, "a")
	# cree le layout qui va tout contenir
	f.write("########################################################################################################################\n")
	f.write("# Creation du Layout pour dash\n\n")
	f.write("OverlappingTFBS_layout = html.Div([ \n")

	f.write("], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)'} )\n")
	f.write("\n\n\n\n")
	f.close()





########################################################################################################################
###	Create the OverlappingTFBS function
########################################################################################################################
def OverlappingTFBS(pathVisual, nbSeq_Assemble, numberTE):

	# Ajout des librairies python pour le serveur
	temp = pathVisual + '/Functions/OverlappingTFBS.py'
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

	f.close()



	Create_layout(temp)
