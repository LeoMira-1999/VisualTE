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
	f.write("from Functions import CommonDATA, CommonDATA_SelectTEs, Couleur\n\n\n\n")

	f.write("########################################################################################################################\n")
	f.write("# Data that does not change with the sliders \n\n")

	f.close()
	
	
	
	Create_layout(temp)
	
	
