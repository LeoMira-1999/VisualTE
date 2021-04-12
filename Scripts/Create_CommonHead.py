#!/usr/bin/python3
import os
import sys
import plotly.graph_objs as go		



###############################################################################################################################################################
####	Debut commun dans chaque page HTML
###############################################################################################################################################################
def CommonLink(temp, otherOnglets, urlOnglets) :

	f = open(temp, "a")
	# Ajoute le nom de la fonction
	f.write("\thtml.Div([ \n")
	f.write("\t	html.H4('VisualTE v3'), \n")
	f.write("\t	html.Hr(), \n")
	f.write("\t	# le truc pour que les tabs aient acces au input \n")
	f.write("\t	dcc.Store(id='memory'), \n")
	f.write("\t], style={'width':'100%', 'display':'inline-block', 'vertical-align':'middle', 'text-align':'center'} ), \n\n")

	# Ajout slider pour la taille des hits en fonction du consensus 
	f.write("\t# ajout des sliders qui modifie \n")
	f.write("\thtml.Div([ \n")
	f.write("\t\thtml.Div([ \n")
	f.write("\t\t	html.Div([ \n")
	f.write("\t\t		html.Label('Consensus Size Range : '), \n")
	f.write("\t\t	], style={'width':'15%', 'display':'inline-block', 'vertical-align':'middle', 'text-align':'right'} ), \n")
	f.write("\t\t	html.Div([ \n")
	f.write("\t\t		dcc.RangeSlider(  \n")
	f.write("\t\t			id='SizeSlider_commun',  \n")
	f.write("\t\t			min=1, \n")
	f.write("\t\t			max=100, \n")
	f.write("\t\t			value=[1, 100], \n")
	f.write("\t\t 			marks={ \n")
	f.write("\t\t 				1  : '  1%', \n")
	f.write("\t\t 				20 : ' 20%', \n")
	f.write("\t\t 				40 : ' 40%', \n")
	f.write("\t\t 				60 : ' 60%', \n")
	f.write("\t\t 				80 : ' 80%', \n")
	f.write("\t\t 				100: '100%+', \n")
	f.write("\t\t 			}, \n")
	f.write("\t\t 			allowCross=False, \n")
	f.write("\t\t 			pushable=1, \n")
	f.write("\t\t			step=1, \n")
	f.write("\t\t		),  \n")
	f.write("\t\t	], style={'width':'35%', 'display':'inline-block', 'vertical-align':'middle'} ), \n")

	# Ajout slider pour la similarite des hits avec le consensus (valeur en memoire)
	f.write("\t\t	html.Div([ \n")
	f.write("\t\t		html.Label('Similarity Range : '), \n")
	f.write("\t\t	], style={'width':'15%', 'display':'inline-block', 'vertical-align':'middle', 'text-align':'right'} ), \n")
	f.write("\t\t	html.Div([ \n")
	f.write("\t\t		dcc.RangeSlider(  \n")
	f.write("\t\t			id='SimilaritySlider_commun',  \n")
	f.write("\t\t			min=30, \n")
	f.write("\t\t			max=100, \n")
	f.write("\t\t			value=[30, 100], \n")
	f.write("\t\t			step=1, \n")
	f.write("\t\t 			marks={ \n")
	f.write("\t\t 				30 : ' 30%', \n")
	f.write("\t\t 				40 : ' 40%', \n")
	f.write("\t\t 				50 : ' 50%', \n")
	f.write("\t\t 				60 : ' 60%', \n")
	f.write("\t\t 				70 : ' 70%', \n")
	f.write("\t\t 				80 : ' 80%', \n")
	f.write("\t\t 				90 : ' 90%', \n")
	f.write("\t\t 				100: '100%', \n")
	f.write("\t\t 			}, \n")
	f.write("\t\t 			allowCross=False, \n")
	f.write("\t\t 			pushable=1, \n")
	f.write("\t\t		),  \n")
	f.write("\t\t	], style={'width':'35%', 'display':'inline-block', 'vertical-align':'middle'} ), \n")
	f.write("\t\t], style={'width':'100%', 'display':'inline-block'}), \n")
	f.write("\t], style={'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'}),\n\n\n")


	# Ajout des liens avec les autres fonctions
	f.write("\thtml.Div([ \n")
	f.write("\t	html.Hr(), \n")
	
	f.write("\t	html.Div([ \n")
	f.write("\t		dcc.Tabs( id='tabs-function', value='Introduction / Help', \n")
	f.write("\t			children=[ \n")
	f.write("\t				dcc.Tab(label = 'Introduction / Help', value = 'Introduction / Help'), \n")
	f.write("\t				dcc.Tab(label = 'TE Genome Browser', value = 'TE Genome Browser'), \n")
	f.write("\t				dcc.Tab(label = 'TE Chromosome Distribution', value = 'TE Chromosome Distribution'), \n")
	f.write("\t				dcc.Tab(label = 'TE General Features', value = 'TE General Features'), \n")
	f.write("\t				dcc.Tab(label = 'Relationship Between TE Occurrences', value = 'Relationship Between TE Occurrences'), \n")
	f.write("\t				dcc.Tab(label = 'TE Genetic Environment', value = 'TE Genetic Environment'), \n")
	f.write("\t				dcc.Tab(label = 'TE - Neighboring Gene Distance', value = 'TE - Neighboring Gene Distance'), \n")
	f.write("\t				dcc.Tab(label = 'TE - Neighboring Gene Function', value = 'TE - Neighboring Gene Function'), \n")
	f.write("\t				dcc.Tab(label = 'Overlapping TFBS', value = 'Overlapping TFBS'), \n")
	f.write("\t				dcc.Tab(label = 'Summary Table', value = 'Summary Table'), \n")
	f.write("\t			] \n")
	f.write("\t		), \n")
	f.write("\t	], style={'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px', 'vertical-align':'middle'} ),  \n")
	f.write("\t], style={'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px', 'vertical-align':'middle'} ),  \n")

	f.write("\t \n\n\n")

	f.close()



