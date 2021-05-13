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
	f.write("dataFrame_SummaryTE     = pd.DataFrame( [['', '', '', '', '']], columns=[ 'TE Term', 'TE ID', 'TE P-value', 'TE Gene Number', 'TE Gene List' ] ) \n")
	f.write("dataFrame_SummaryRandom = pd.DataFrame( [['', '', '', '', '']], columns=[ 'Random Term', 'Random ID', 'Random P-value', 'Random Gene Number', 'Random Gene List' ] ) \n\n\n")


	f.write("NeighboringGeneFunction_layout = html.Div([ \n")
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

	f.write("	# Here threre are also two graphs for the TE-gene function/GO \n")
	f.write("	html.Div([ \n")
	f.write("		html.Label('TE - Gene Function / TE - Gene Ontology') \n")
	f.write("	], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)', 'text-align': 'center'} ), \n\n")

	f.write("	html.Div([ \n")
	f.write("		html.Div([ \n")
	f.write("			html.Label('Choose GO Enrichment : ') \n")
	f.write("		], style={'width': '14%', 'display': 'inline-block',} ), \n")
	f.write("		html.Div([ \n")
	f.write("			dcc.RadioItems( \n")
	f.write("				id='Checklist_Onglet6', \n")
	f.write("				options=[ \n")
	f.write("					{'label': 'GO Biological Process  ', 	'value': 1}, \n")
	f.write("					{'label': 'GO Cellular Component  ', 	'value': 2},  \n")
	f.write("					{'label': 'GO Molecular Function  ', 	'value': 3},  \n")
	f.write("					{'label': 'Wiki Pathways  ', 		'value': 4}, \n")
	f.write("				], \n")
	f.write("				value = 1, \n")
	f.write("				labelStyle={'display': 'inline-block'}, \n")
	f.write("			), \n")
	f.write("		], style={'width': '85%', 'display': 'inline-block', 'text-align':'left'} ), \n")
	f.write("	], style={'width': '100%', 'vertical-align':'top', 'text-align':'center', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)'} ), \n\n\n")


	f.write("	########################################################################################################################\n")
	f.write("	html.Div([ \n")
	f.write("		html.Div(id='TableGO_Onglet6'), \n\n")

	f.write("		html.Div([ \n")
	f.write("			html.Label('TE - Gene Enrichment') \n")
	f.write("		], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)', 'text-align': 'center'} ), \n\n")

	f.write("		# affiche le tableau  \n")
	f.write("		dash_table.DataTable( \n")
	f.write("			id='TableTEGOEnrich_Onglet6', \n")
	f.write("			data=dataFrame_SummaryTE.to_dict('records'), \n")
	f.write("			columns = [ \n")
	f.write("				{'name': 'TE Term',		'id': 'TE Term' }, \n")
	f.write("				{'name': 'TE ID',		'id': 'TE ID' }, \n")
	f.write("				{'name': 'TE P-value',		'id': 'TE P-value' }, \n")
	f.write("				{'name': 'TE Gene Number',	'id': 'TE Gene Number' }, \n")
	f.write("				{'name': 'TE Gene List',	'id': 'TE Gene List' }, \n")
	f.write("			], \n")
	f.write("			style_table={'maxHeight': '400px', 'overflowY': 'auto', 'overflowX': 'None'}, \n")
	f.write("			style_data={ \n")
	f.write("				'textOverflow': 'ellipsis', \n")
	f.write("			}, \n")
	f.write("			style_data_conditional=[ \n")
	f.write("				{'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}, \n")
	f.write("			], \n")
	f.write("			style_cell_conditional=[ \n")
	f.write("				{'if': {'column_id': 'TE Term'}, 'minWidth': '300px', 'width': '300px', 'maxWidth': '300px',}, \n")
	f.write("				{'if': {'column_id': 'TE ID'}, 'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',}, \n")
	f.write("				{'if': {'column_id': 'TE P-value'}, 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',}, \n")
	f.write("				{'if': {'column_id': 'TE Gene Number'}, 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',}, \n")
	f.write("			], \n")
	f.write("			style_header={ \n")
	f.write("				'whiteSpace': 'normal', \n")
	f.write("				'height': 'auto', \n")
	f.write("				'backgroundColor': 'rgb(230, 230, 230)', \n")
	f.write("				'fontWeight': 'bold', \n")
	f.write("				'textAlign': 'center', \n")
	f.write("			}, \n")
	f.write("			tooltip_data=[ \n")
	f.write("			{ \n")
	f.write("				column: {'value': str(value), 'type': 'markdown'} \n")
	f.write("				for column, value in row.items() \n")
	f.write("			} for row in dataFrame_SummaryTE.to_dict('rows') \n")
	f.write("			], \n")
	f.write("			tooltip_duration=None, \n")
	f.write("			page_size = 100, \n")
	f.write("			merge_duplicate_headers = True, \n")
	f.write("			fixed_rows={'headers': True}, \n")
	f.write("		), \n")
	f.write("		html.Div([ \n")
	f.write("			html.Div(id='ClickTableTEGO'), \n")
	f.write("		], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n\n")


	f.write("		html.Div([ \n")
	f.write("			html.Label(' ') \n")
	f.write("		], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)', 'text-align': 'center'} ), \n\n\n")


	f.write("		html.Div([ \n")
	f.write("			html.Label('Random Position - Gene Enrichment') \n")
	f.write("		], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)', 'text-align': 'center'} ), \n\n")

	f.write("		# affiche le tableau \n")
	f.write("		dash_table.DataTable( \n")
	f.write("			id='TableRandomGOEnrich_Onglet6', \n")
	f.write("			data=dataFrame_SummaryRandom.to_dict('records'), \n")
	f.write("			columns = [ \n")
	f.write("				{'name': 'Random Term',		'id': 'Random Term' }, \n")
	f.write("				{'name': 'Random ID',		'id': 'Random ID' }, \n")
	f.write("				{'name': 'Random P-value',	'id': 'Random P-value' }, \n")
	f.write("				{'name': 'Random Gene Number',	'id': 'Random Gene Number' }, \n")
	f.write("				{'name': 'Random Gene List',	'id': 'Random Gene List' }, \n")
	f.write("			], \n")
	f.write("			style_table={'maxHeight': '400px', 'overflowY': 'auto', 'overflowX': 'None'}, \n")
	f.write("			style_data={ \n")
	f.write("				'textOverflow': 'ellipsis', \n")
	f.write("			}, \n")
	f.write("			style_data_conditional=[ \n")
	f.write("				{'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}, \n")
	f.write("			], \n")
	f.write("			style_cell_conditional=[ \n")
	f.write("				{'if': {'column_id': 'Random Term'}, 'minWidth': '300px', 'width': '300px', 'maxWidth': '300px',}, \n")
	f.write("				{'if': {'column_id': 'Random ID'}, 'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',}, \n")
	f.write("				{'if': {'column_id': 'Random P-value'}, 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',}, \n")
	f.write("				{'if': {'column_id': 'Random Gene Number'}, 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',}, \n")
	f.write("			], \n")
	f.write("			style_header={ \n")
	f.write("				'whiteSpace': 'normal', \n")
	f.write("				'height': 'auto', \n")
	f.write("				'backgroundColor': 'rgb(230, 230, 230)', \n")
	f.write("				'fontWeight': 'bold', \n")
	f.write("				'textAlign': 'center', \n")
	f.write("			}, \n")
	f.write("			tooltip_data=[ \n")
	f.write("			{ \n")
	f.write("				column: {'value': str(value), 'type': 'markdown'} \n")
	f.write("				for column, value in row.items() \n")
	f.write("			} for row in dataFrame_SummaryRandom.to_dict('rows') \n")
	f.write("			], \n")
	f.write("			tooltip_duration=None, \n")
	f.write("			page_size = 100, \n")
	f.write("			merge_duplicate_headers = True, \n")
	f.write("			fixed_rows={'headers': True}, \n")
	f.write("		), \n\n")

	f.write("		html.Div([ \n")
	f.write("			html.Div(id='ClickTableRandomGO'),\n")
	f.write("		], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n")

	f.write("	], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n")

	f.write("], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)'} )\n")
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
###	Create the Piechart and Table function for GO
########################################################################################################################
def EnrichementGO(temp) :

	f = open(temp, "a")

	f.write("######################################################################################################################## \n")
	f.write("# ajout du callback \n\n")

	f.write("# marcher avec un multi input !! mais il faut que 1 seul output \n")
	f.write("@app.callback( \n")
	f.write("	[Output('TableTEGOEnrich_Onglet6', 'data'), Output('TableRandomGOEnrich_Onglet6', 'data')], \n")
	f.write("	[Input('memory', 'data'), Input('SelectSequence_Dropdown_Onglet6', 'value'), Input('Checklist_Onglet6', 'value') ] \n")
	f.write(") \n\n")

	f.write("def update_TableGO_Onglet6(valueSliders, SelectSequence_Dropdown_Onglet6, Checklist_Onglet6) : \n\n")
	f.close()


	ValueSliderRecup(temp)


	f = open(temp, "a")
	f.write("	indiceCHR = 0 \n")
	f.write("	GeneName = [] \n")
	f.write("	RandomName = [] \n")
	f.write("	for j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("		GeneName.append([]) \n")
	f.write("		RandomName.append([]) \n\n")

	f.write("	if SelectSequence_Dropdown_Onglet6 == None or SelectSequence_Dropdown_Onglet6 == '0' : \n")
	f.write("		indiceCHR = 0 \n")
	f.write("		for j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("			Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[j]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3]), : ] \n")
	f.write("			IndexTE = Select_myTE['Index'].tolist() \n\n")

	f.write("			Select_myGene = CommonDATA_SelectTEs.dataFrame_CloseGene.loc[ CommonDATA_SelectTEs.dataFrame_CloseGene['TE Index'].isin(IndexTE), : ] \n")
	f.write("			GeneName[j] = Select_myGene['Gene Name'].tolist() \n")
	f.write("			Select_Positions = CommonDATA_SelectTEs.dataFrame_RandomGene.loc[ (CommonDATA_SelectTEs.dataFrame_RandomGene['TE Index'].isin(IndexTE)), : ] \n")
	f.write("			RandomName[j] = Select_Positions['Gene Name'].tolist() \n")
	f.write("	else : \n")
	f.write("		indiceCHR = int(SelectSequence_Dropdown_Onglet6) \n")
	f.write("		for j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("			Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[j]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Chr Name'] == SelectionNameID[indiceCHR]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3]), : ] \n")
	f.write("			IndexTE = Select_myTE['Index'].tolist() \n\n")

	f.write("			Select_myGene = CommonDATA_SelectTEs.dataFrame_CloseGene.loc[ CommonDATA_SelectTEs.dataFrame_CloseGene['TE Index'].isin(IndexTE), : ] \n")
	f.write("			GeneName[j] = Select_myGene['Gene Name'].tolist() \n")
	f.write("			Select_Positions = CommonDATA_SelectTEs.dataFrame_RandomGene.loc[ (CommonDATA_SelectTEs.dataFrame_RandomGene['TE Index'].isin(IndexTE)) & (CommonDATA_SelectTEs.dataFrame_RandomGene['Gene Chrom'] == SelectionNameID[indiceCHR]), : ] \n")
	f.write("			RandomName[j] = Select_Positions['Gene Name'].tolist() \n\n")

	f.write("	for j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("		for i in range(0, len(GeneName[j]), 1) : \n")
	f.write("			GeneName[j][i] = GeneName[j][i].upper() \n")
	f.write("			RandomName[j][i] = RandomName[j][i].upper() \n")
	f.write("\n\n\n\n")




	f.write("	######################################################################################################################## \n")
	f.write("	enr = ''  \n")
	f.write("	enr2 = ''  \n")
	f.write("	if Checklist_Onglet6 == 1 :  \n")
	f.write("		enr = gp.enrichr(gene_list=GeneName[0],  \n")
	f.write("			gene_sets=GO_Biological_Process_2018, \n")
	f.write("			description='test',  \n")
	f.write("			no_plot=True, # Skip plotting \n")
	f.write("			outdir='test/enrichr_kegg', \n")
	f.write("			cutoff=0.05 # test dataset, use lower value from range(0,1) \n")
	f.write("		) \n")
	f.write("		enr2 = gp.enrichr(gene_list=RandomName[0], \n")
	f.write("			gene_sets=GO_Biological_Process_2018, \n")
	f.write("			description='test', \n")
	f.write("			no_plot=True, # Skip plotting \n")
	f.write("			outdir='test/enrichr_kegg', \n")
	f.write("			cutoff=0.05 # test dataset, use lower value from range(0,1) \n")
	f.write("		) \n\n")

	f.write("	elif Checklist_Onglet6 == 2 : \n")
	f.write("		enr = gp.enrichr(gene_list=GeneName[0], \n")
	f.write("			gene_sets=GO_Cellular_Component_2018, \n")
	f.write("			description='test', \n")
	f.write("			no_plot=True, # Skip plotting \n")
	f.write("			outdir='test/enrichr_kegg', \n")
	f.write("			cutoff=0.05 # test dataset, use lower value from range(0,1) \n")
	f.write("		) \n")
	f.write("		enr2 = gp.enrichr(gene_list=RandomName[0], \n")
	f.write("			gene_sets=GO_Cellular_Component_2018, \n")
	f.write("			description='test', \n")
	f.write("			no_plot=True, # Skip plotting \n")
	f.write("			outdir='test/enrichr_kegg', \n")
	f.write("			cutoff=0.05 # test dataset, use lower value from range(0,1) \n")
	f.write("		) \n\n")

	f.write("	elif Checklist_Onglet6 == 3 : \n")
	f.write("		enr = gp.enrichr(gene_list=GeneName[0], \n")
	f.write("			gene_sets=GO_Molecular_Function_2018, \n")
	f.write("			description='test', \n")
	f.write("			no_plot=True, # Skip plotting \n")
	f.write("			outdir='test/enrichr_kegg', \n")
	f.write("			cutoff=0.05 # test dataset, use lower value from range(0,1) \n")
	f.write("		) \n")
	f.write("		enr2 = gp.enrichr(gene_list=RandomName[0], \n")
	f.write("			gene_sets=GO_Molecular_Function_2018, \n")
	f.write("			description='test', \n")
	f.write("			no_plot=True, # Skip plotting \n")
	f.write("			outdir='test/enrichr_kegg', \n")
	f.write("			cutoff=0.05 # test dataset, use lower value from range(0,1) \n")
	f.write("		) \n\n")

	f.write("	elif Checklist_Onglet6 == 4 : \n")
	f.write("		enr = gp.enrichr(gene_list=GeneName[0], \n")
	f.write("			gene_sets=WikiPathways_2016, \n")
	f.write("			description='test', \n")
	f.write("			no_plot=True, # Skip plotting \n")
	f.write("			outdir='test/enrichr_kegg', \n")
	f.write("			cutoff=0.05 # test dataset, use lower value from range(0,1) \n")
	f.write("		) \n")
	f.write("		enr2 = gp.enrichr(gene_list=RandomName[0], \n")
	f.write("			gene_sets=WikiPathways_2016, \n")
	f.write("			description='test', \n")
	f.write("			no_plot=True, # Skip plotting \n")
	f.write("			outdir='test/enrichr_kegg', \n")
	f.write("			cutoff=0.05 # test dataset, use lower value from range(0,1) \n")
	f.write("		) \n\n\n\n")



	f.write("	InfosTableTE = [] \n")
	f.write("	SelectTE_Term = enr.results['Term'].tolist() \n")
	f.write("	SelectTE_Pvalue = enr.results['P-value'].tolist() \n")
	f.write("	SelectTE_Genes = enr.results['Genes'].tolist() \n")
	f.write("	SelectTE_Number = enr.results['Overlap'].tolist() \n")
	f.write("	SelectTE_Pvalue, SelectTE_Term, SelectTE_Genes, SelectTE_Number = zip(*sorted(zip(SelectTE_Pvalue, SelectTE_Term, SelectTE_Genes, SelectTE_Number))) \n\n")

	f.write("	compteurT = 0 \n")
	f.write("	for i in range(0, len(SelectTE_Term), 1) : \n")
	f.write("		pvalueTE = round(float(SelectTE_Pvalue[i]), 3) \n")
	f.write("		if pvalueTE < 0.05 or compteurT < 5 : \n")
	f.write("			rowList = [] \n")
	f.write("			if Checklist_Onglet6 == 4 : \n")
	f.write("				cut = SelectTE_Term[i].split(' ') \n")
	f.write("				therme = cut[0] \n")
	f.write("				for z in range(1, len(cut)-1, 1) : \n")
	f.write("					therme = therme + ' ' + cut[z] \n")
	f.write("				rowList = [therme, cut[len(cut)-1], pvalueTE, SelectTE_Number[i], SelectTE_Genes[i] ] \n")
	f.write("			else : \n")
	f.write("				cut = SelectTE_Term[i].split('(') \n")
	f.write("				therme = cut[0] \n")
	f.write("				for z in range(1, len(cut)-1, 1) : \n")
	f.write("					therme = therme + ' ' + cut[z] \n")
	f.write("				rowList = [ therme, cut[len(cut)-1][:-1], pvalueTE, SelectTE_Number[i], SelectTE_Genes[i] ] \n")
	f.write("			InfosTableTE.append(rowList) \n")
	f.write("		else : \n")
	f.write("			break \n")
	f.write("		compteurT += 1 \n")
	f.write("	dataFrame_SummaryTE = pd.DataFrame(InfosTableTE, columns=[ 'TE Term', 'TE ID', 'TE P-value', 'TE Gene Number', 'TE Gene List' ] ) \n\n\n")


	f.write("	InfosTableRandom = [] \n")
	f.write("	SelectRandom_Term = enr2.results['Term'].tolist() \n")
	f.write("	SelectRandom_Pvalue = enr2.results['P-value'].tolist() \n")
	f.write("	SelectRandom_Genes = enr2.results['Genes'].tolist() \n")
	f.write("	SelectRandom_Number = enr2.results['Overlap'].tolist() \n")
	f.write("	SelectRandom_Pvalue, SelectRandom_Term, SelectRandom_Genes, SelectRandom_Number = zip(*sorted(zip(SelectRandom_Pvalue, SelectRandom_Term, SelectRandom_Genes, SelectRandom_Number))) \n")

	f.write("	compteurR = 0 \n")
	f.write("	for i in range(0, len(SelectRandom_Term), 1) : \n")
	f.write("		pvalueTE = round(float(SelectRandom_Pvalue[i]), 3) \n")
	f.write("		if pvalueTE < 0.05 or compteurR < 5 : \n")
	f.write("			rowList = [] \n")
	f.write("			if Checklist_Onglet6 == 4 : \n")
	f.write("				cut = SelectRandom_Term[i].split(' ') \n")
	f.write("				therme = cut[0] \n")
	f.write("				for z in range(1, len(cut)-1, 1) : \n")
	f.write("					therme = therme + ' ' + cut[z] \n")
	f.write("				rowList = [therme, cut[len(cut)-1], pvalueTE, SelectRandom_Number[i], SelectRandom_Genes[i] ] \n")
	f.write("			else : \n")
	f.write("				cut = SelectRandom_Term[i].split('(') \n")
	f.write("				therme = cut[0] \n")
	f.write("				for z in range(1, len(cut)-1, 1) : \n")
	f.write("					therme = therme + ' ' + cut[z] \n")
	f.write("				rowList = [ therme, cut[len(cut)-1][:-1], pvalueTE, SelectRandom_Number[i], SelectRandom_Genes[i] ] \n")
	f.write("			InfosTableRandom.append(rowList) \n")
	f.write("		else : \n")
	f.write("			break \n")
	f.write("		compteurR += 1 \n")
	f.write("	dataFrame_SummaryRandom = pd.DataFrame(InfosTableRandom, columns=[ 'Random Term', 'Random ID', 'Random P-value', 'Random Gene Number', 'Random Gene List' ] ) \n\n\n")


	f.write("	return dataFrame_SummaryTE.to_dict('records'), dataFrame_SummaryRandom.to_dict('records')\n")
	f.write("\n\n\n\n")
	f.close()










########################################################################################################################
###	Create the graphs that will appears depending of the Table
########################################################################################################################
def SupplementTable(temp) :

	f = open(temp, "a")

	f.write("######################################################################################################################## \n")
	f.write("@app.callback( \n")
	f.write("	Output('ClickTableTEGO', 'children'), \n")
	f.write("	[ Input('TableTEGOEnrich_Onglet6', 'active_cell') ] \n")
	f.write(") \n")
	f.write("def getActiveCellTE(active_cellTE): \n")
	f.write("	if active_cellTE : \n")
	f.write("		col = active_cellTE['column_id'] \n")
	f.write("		row = active_cellTE['row'] \n")
	f.write("		#cellData = data[row][col] \n")
	f.write("		return html.P(f' TE row: {row}, col: {col}') \n")
	f.write("	return html.P('no cell selected') \n")
	f.write("\n\n\n\n")


	f.write("######################################################################################################################## \n")
	f.write("@app.callback( \n")
	f.write("	Output('ClickTableRandomGO', 'children'), \n")
	f.write("	[ Input('TableRandomGOEnrich_Onglet6', 'active_cell') ] \n")
	f.write(") \n")
	f.write("def getActiveCellRandom(active_cellRandom): \n")
	f.write("	if active_cellRandom : \n")
	f.write("		col = active_cellRandom['column'] \n")
	f.write("		row = active_cellRandom['row'] \n")
	f.write("		return html.P(f' Random row: {row}, col: {col}') \n")
	f.write("	return html.P('no cell selected') \n")

	f.write("\n\n\n\n")
	f.close()










########################################################################################################################
###	Create the AnnotationDistance function
########################################################################################################################
def NeighboringGeneFunctions(pathVisual, pathVisualNEW, nbSeq_Assemble, numberTE):

	# Ajout des librairies python pour le serveur
	temp = pathVisualNEW + '/Functions/NeighboringGeneFunction.py'
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
	f.write("\n\n")

	absolutePath = os.getcwd() + '/Scripts/DATA/EnrichmentGO/'

	f.write("GO_Biological_Process_2018 = {} \n")
	tempFile = absolutePath + 'GO_Biological_Process_2018'
	f.write("f = open('" + tempFile + "', 'r') \n")
	f.write("lignes = f.readlines() \n")
	f.write("f.close() \n")
	f.write("for j in range(0, len(lignes), 1) : \n")
	f.write("	lignes[j] = lignes[j].rstrip('\\n') \n")
	f.write("	decoupe = lignes[j].split('	') \n")
	f.write("	recoupe = decoupe[0].split(' (') \n")
	f.write("	temp = [] \n")
	f.write("	for k in range(2, len(decoupe), 1) : \n")
	f.write("		temp.append(decoupe[k]) \n")
	f.write("	GO_Biological_Process_2018[recoupe[0]] = temp \n\n")

	f.write("GO_Cellular_Component_2018 = {} \n")
	tempFile = absolutePath + 'GO_Cellular_Component_2018'
	f.write("f = open('" + tempFile + "', 'r') \n")
	f.write("lignes = f.readlines() \n")
	f.write("f.close() \n")
	f.write("for j in range(0, len(lignes), 1) : \n")
	f.write("	lignes[j] = lignes[j].rstrip('\\n') \n")
	f.write("	decoupe = lignes[j].split('	') \n")
	f.write("	recoupe = decoupe[0].split(' (') \n")
	f.write("	temp = [] \n")
	f.write("	for k in range(2, len(decoupe), 1) : \n")
	f.write("		temp.append(decoupe[k]) \n")
	f.write("	GO_Cellular_Component_2018[recoupe[0]] = temp \n\n")

	f.write("GO_Molecular_Function_2018 = {} \n")
	tempFile = absolutePath + 'GO_Molecular_Function_2018'
	f.write("f = open('" + tempFile + "', 'r') \n")
	f.write("lignes = f.readlines() \n")
	f.write("f.close() \n")
	f.write("for j in range(0, len(lignes), 1) : \n")
	f.write("	lignes[j] = lignes[j].rstrip('\\n') \n")
	f.write("	decoupe = lignes[j].split('	') \n")
	f.write("	recoupe = decoupe[0].split(' (') \n")
	f.write("	temp = [] \n")
	f.write("	for k in range(2, len(decoupe), 1) : \n")
	f.write("		temp.append(decoupe[k]) \n")
	f.write("	GO_Molecular_Function_2018[recoupe[0]] = temp \n\n")

	f.write("WikiPathways_2016 = {} \n")
	tempFile = absolutePath + 'WikiPathways_2016'
	f.write("f = open('" + tempFile + "', 'r') \n")
	f.write("lignes = f.readlines() \n")
	f.write("f.close() \n")
	f.write("for j in range(0, len(lignes), 1) : \n")
	f.write("	lignes[j] = lignes[j].rstrip('\\n') \n")
	f.write("	decoupe = lignes[j].split('	') \n")
	f.write("	recoupe = decoupe[0].split(' (') \n")
	f.write("	temp = [] \n")
	f.write("	for k in range(2, len(decoupe), 1) : \n")
	f.write("		temp.append(decoupe[k]) \n")
	f.write("	WikiPathways_2016[recoupe[0]] = temp \n")

	f.write("\n\n\n\n\n")

	f.close()



	# get the data for the organism
	tempFile = pathVisual + '/Downloaded/DATA_Organism.txt'
	dataT = pd.read_csv(tempFile)
	# Create first a sud-dataframe that contains only the wanted values
	dataFrame_Organism = dataT.loc[(dataT['Size bp'] > 0)]



	# Create the initial layout that contains this fonction
	Create_layout(temp, dataFrame_Organism)

	# Create the two Enrichment Table and their supplemetary graphs
	EnrichementGO(temp)
	SupplementTable(temp)
