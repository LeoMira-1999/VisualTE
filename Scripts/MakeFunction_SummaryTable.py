#!/usr/bin/python3
import os
import sys
import importlib
import importlib.util
import pandas as pd
import plotly.graph_objs as go



########################################################################################################################
###	Create the dataframe for the table
########################################################################################################################
def Dataframe_in_Table(temp, numberTE) :
	
	f = open(temp, "a")
	
	f.write("\tInfosTable = [] \n")
	f.write("\tSelect_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ ")
	f.write(" (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax)")
	f.write(" & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3])")
	f.write(", : ] \n")
	f.write("\tSeq = Select_myTE['Chr ID'].tolist() \n")
	f.write("\tIndexTE = Select_myTE['Index'].tolist() \n")
	f.write("\tFamily = Select_myTE['TE Family'].tolist() \n")
	f.write("\tDEB = Select_myTE['Start'].tolist() \n")
	f.write("\tFIN = Select_myTE['End'].tolist() \n")
	f.write("\tSens = Select_myTE['Sens'].tolist() \n")
	f.write("\tSimilarity = Select_myTE['Similarity'].tolist() \n")
	f.write("\tConsDeb = Select_myTE['Consensus Start'].tolist() \n")
	f.write("\tConsFin = Select_myTE['Consensus End'].tolist() \n\n")
	
	f.write("\tSelect_myGene = CommonDATA_SelectTEs.dataFrame_MyGene.loc[ CommonDATA_SelectTEs.dataFrame_MyGene['TE Index'].isin(IndexTE), : ] \n")
	f.write("\tIndexGene = Select_myGene['TE Index'].tolist() \n")
	f.write("\tTEGenePos = Select_myGene['TE-Gene Position'].tolist() \n")
	f.write("\tDistance = Select_myGene['Gene Distance'].tolist() \n")
	f.write("\tGeneName = Select_myGene['Gene Name'].tolist() \n")
	f.write("\tGeneStart = Select_myGene['Gene Start'].tolist() \n")
	f.write("\tGeneEnd = Select_myGene['Gene End'].tolist() \n")
	f.write("\tGeneOrient = Select_myGene['Gene Sens'].tolist() \n")
	f.write("\tGeneID = Select_myGene['Gene ID'].tolist() \n")
	f.write("\tGeneFunction = Select_myGene['Gene Function'].tolist() \n\n\n\n")
	
	
	f.write("\tfor z in range(0, len(Seq), 1) : \n")
	f.write("\t	rowList = [ IndexTE[z], Family[z], '', Seq[z], DEB[z], FIN[z], Sens[z], Similarity[z], ConsDeb[z], ConsFin[z], '' , '', '' , '', '', '', '', '' , '', '', '', '', '', '', '' , '', '', '', '', '', '', '' , '', '', '', '', '', ''] \n")   
	f.write("\t	for j in range(0, len(IndexGene), 1) : \n")
	f.write("\t		if IndexGene[j] == IndexTE[z] and GeneName[j] != 'VIDE' : \n")
	f.write("\t			if TEGenePos[j] == \"5'\" : \n")
	f.write("\t				rowList[15] = Distance[j] \n")
	f.write("\t				rowList[16] = GeneName[j] \n")
	f.write("\t				rowList[17] = GeneStart[j] \n")
	f.write("\t				rowList[18] = GeneEnd[j] \n")
	f.write("\t				rowList[19] = GeneOrient[j] \n")
	f.write("\t				rowList[20] = GeneID[j] \n")
	f.write("\t				rowList[21] = GeneFunction[j] \n")
	f.write("\t			if TEGenePos[j] == \"3'\" :  \n")
	f.write("\t				rowList[22] = Distance[j] \n")
	f.write("\t				rowList[23] = GeneName[j] \n")
	f.write("\t				rowList[24] = GeneStart[j] \n")
	f.write("\t				rowList[25] = GeneEnd[j] \n")
	f.write("\t				rowList[26] = GeneOrient[j] \n")
	f.write("\t				rowList[27] = GeneID[j] \n")
	f.write("\t				rowList[28] = GeneFunction[j] \n")
	f.write("\t			if TEGenePos[j] == \"Inside\" : \n")
	f.write("\t				rowList[29] = Distance[j] \n")
	f.write("\t				rowList[30] = GeneName[j] \n")
	f.write("\t				rowList[31] = GeneStart[j] \n")
	f.write("\t				rowList[32] = GeneEnd[j] \n")
	f.write("\t				rowList[33] = GeneOrient[j] \n")
	f.write("\t				rowList[34] = GeneID[j] \n")
	f.write("\t				rowList[35] = GeneFunction[j] \n")
	
	f.write("\t	###################################################################################### \n") 
	f.write("\t	# Now reads the Chipseq data for the TE Occurrences \n") 
	f.write("\t	# put all columns in list \n") 
	f.write("\t	chipSeqOverlap = '' \n") 
	f.write("\t	chipSeqDeb = '' \n") 
	f.write("\t	chipSeqFin = '' \n") 
	f.write("\t	chipSeqName = '' \n") 
	f.write("\t	chipSeqType = '' \n") 
	f.write("\t	chipSeqTissue = '' \n") 
	f.write("\t	chipSeqOrgan = '' \n") 
	f.write("\t	filename = 'Downloaded/Selected_ChipSeq/ChipSeq_for__' + Family[z] + '__occurrences_' + str(IndexTE[z]) + '_.txt' \n") 
	f.write("\t	# memorize lines from file \n") 
	f.write("\t	f = open(filename, 'r') \n") 
	f.write("\t	lignes = f.readlines() \n") 
	f.write("\t	f.close() \n\n")
	
	#dataFrame_ChipSEQ = pd.read_csv(filename)
	#Select_ChipSEQ = dataFrame_ChipSEQ.loc[ (int(DEB[z]) <= dataFrame_ChipSEQ['Start'] & dataFrame_ChipSEQ['End'] <= int(FIN[z])) | (dataFrame_ChipSEQ['Start'] <= int(DEB[z]) & int(FIN[z]) <= dataFrame_ChipSEQ['End']) | (int(DEB[z]) <= dataFrame_ChipSEQ['Start'] & dataFrame_ChipSEQ['Start'] <  int(FIN[z])) | (int(DEB[z]) <  dataFrame_ChipSEQ['End'] & dataFrame_ChipSEQ['Start'] <= int(FIN[z])), : ] 
	
	f.write("\t	for i in range(1, len(lignes), 1) : \n") 
	f.write("\t		lignes[i] = lignes[i].rstrip() \n") 
	f.write("\t		coupe = lignes[i].split(',') \n") 
	f.write("\t		if (int(DEB[z]) <= int(coupe[1]) and int(coupe[2]) <= int(FIN[z])) or (int(coupe[1]) <= int(DEB[z]) and int(FIN[z]) <= int(coupe[2])) or (int(DEB[z]) <= int(coupe[1]) and int(coupe[1]) <  int(FIN[z])) or (int(DEB[z]) <  int(coupe[2]) and int(coupe[1]) <= int(FIN[z])) : \n\n") 
	f.write("\t			valueOverlapNT = 0 \n") 
	f.write("\t			if int(DEB[z]) <= int(coupe[1]) and int(coupe[2]) <= int(FIN[z]) : \n") 
	f.write("\t				valueOverlapNT = int(coupe[2]) - int(coupe[1]) \n") 
	f.write("\t			elif int(coupe[1]) <= int(DEB[z]) and int(FIN[z]) <= int(coupe[2]) : \n") 
	f.write("\t				valueOverlapNT = int(FIN[z]) - int(DEB[z]) \n") 
	f.write("\t			elif int(DEB[z]) <= int(coupe[1]) and int(coupe[2]) <  int(FIN[z]) : \n") 
	f.write("\t				valueOverlapNT = int(FIN[z]) - int(coupe[1]) \n") 
	f.write("\t			elif int(DEB[z]) <  int(coupe[1]) and int(coupe[2]) <= int(FIN[z]) : \n") 
	f.write("\t				valueOverlapNT = int(coupe[2]) - int(DEB[z]) \n\n") 
					
	f.write("\t			if chipSeqDeb == '' : \n") 
	f.write("\t				chipSeqOverlap = str(valueOverlapNT) \n") 
	f.write("\t				chipSeqDeb = coupe[1] \n") 
	f.write("\t				chipSeqFin = coupe[2] \n") 
	f.write("\t				chipSeqName = coupe[5] \n") 
	f.write("\t				chipSeqType = coupe[6] \n") 
	f.write("\t				decoupe1 = coupe[7].split('__') \n") 
	f.write("\t				chipSeqTissue = decoupe1[0] \n") 
	f.write("\t				decoupe2 = coupe[8].split('__') \n") 
	f.write("\t				chipSeqOrgan = decoupe2[0] \n") 
	f.write("\t			else : \n") 
	f.write("\t				chipSeqOverlap = chipSeqOverlap + '                                                       \\n' + str(valueOverlapNT) \n") 
	f.write("\t				chipSeqDeb = chipSeqDeb         + '                                                       \\n' + coupe[1] \n") 
	f.write("\t				chipSeqFin = chipSeqFin         + '                                                       \\n' + coupe[2] \n") 
	f.write("\t				chipSeqName = chipSeqName       + '                                                       \\n' + coupe[3] \n") 
	f.write("\t				chipSeqType = chipSeqType       + '                                                       \\n' + coupe[4] \n") 
	f.write("\t				chipSeqTissue = chipSeqTissue   + '                                                       \\n' + decoupe1[0] \n") 
	f.write("\t				chipSeqOrgan = chipSeqOrgan     + '                                                       \\n' + decoupe2[0] \n") 
					
	f.write("\t			for j in range(1, len(decoupe1), 1) : \n") 
	f.write("\t				chipSeqTissue = chipSeqTissue   + '                                                       \\n' + decoupe1[j] \n") 
	f.write("\t			for j in range(1, len(decoupe2), 1) : \n") 
	f.write("\t				chipSeqOrgan = chipSeqOrgan     + '                                                       \\n' + decoupe2[j] \n") 
	f.write("\t	rowList[10] = chipSeqOverlap \n") 
	f.write("\t	rowList[11] = chipSeqDeb \n") 
	f.write("\t	rowList[12] = chipSeqFin \n") 
	f.write("\t	rowList[13] = chipSeqName \n") 
	f.write("\t	rowList[14] = chipSeqType \n") 
	f.write("\t	rowList[15] = chipSeqTissue \n") 
	f.write("\t	rowList[16] = chipSeqOrgan \n\n") 
		
	f.write("\t	InfosTable.append(rowList) \n\n\n")
					
					
	f.write("\t	dataFrame_Summary = pd.DataFrame(InfosTable, columns=[ \n")
	f.write("\t		\"Index\", \"TE Family\", \"Color\", \"Seq Name\", \"Start\", \"End\", \"Orientation\", \"Similarity\", \"Consensus Start\", \"Consensus End\", \n")
	f.write("\t		\"TFBS Overlap\", \"TFBS Start\", \"TFBS End\", \"TFBS Name\", \"TFBS Type\", \"TFBS Tissue\", \"TFBS Organ\", \n") 
	f.write("\t		\"5' Gene Distance\", \"5' Gene Name\", \"5' Gene Start\", \"5' Gene End\", \"5' Gene Orient.\", \"5' GeneID\", \"5' Gene Function\", \n")
	f.write("\t		\"3' Gene Distance\", \"3' Gene Name\", \"3' Gene Start\", \"3' Gene End\", \"3' Gene Orient.\", \"3' GeneID\", \"3' Gene Function\", \n")
	f.write("\t		\"Included Gene Distance\", \"Included Gene Name\", \"Included Gene Start\", \"Included Gene End\", \"Included Gene Orient.\", \"Included GeneID\", \"Included Gene Function\", \n") 
	f.write("\t	] ) \n\n")
	
	f.close()




########################################################################################################################
###	Create the TABLE and the layout that contains the chromosomes
########################################################################################################################
def StyleTableInCallback9(temp, numberTE, moduleSelectTE) :

	f = open(temp, "a")

	f.write("\tOnglet9_Table = html.Div([ \n")
	f.write("\t	# affiche le tableau \n")
	f.write("\t	dash_table.DataTable( \n")
	f.write("\t		id='TableOnglet9', \n")
	f.write("\t		data=dataFrame_Summary.to_dict('records'), \n")
	f.write("\t		columns = [ \n")
	f.write("\t			{'name': [\"TE Occurrences\", \"Index\"],            'id': \"Index\" }, \n")
	f.write("\t			{'name': [\"TE Occurrences\", \"TE Family\"],        'id': \"TE Family\" }, \n")
	f.write("\t			{'name': [\"TE Occurrences\", \"Color\"],            'id': \"Color\" }, \n")
	f.write("\t			{'name': [\"TE Occurrences\", \"Seq Name\"],         'id': \"Seq Name\" }, \n")
	f.write("\t			{'name': [\"TE Occurrences\", \"Start\"],            'id': \"Start\" }, \n")
	f.write("\t			{'name': [\"TE Occurrences\", \"End\"],              'id': \"End\" }, \n")
	f.write("\t			{'name': [\"TE Occurrences\", \"Orientation\"],      'id': \"Orientation\" }, \n")
	f.write("\t			{'name': [\"TE Occurrences\", \"Similarity\"],       'id': \"Similarity\" }, \n")
	f.write("\t			{'name': [\"TE Occurrences\", \"Consensus Start\"],  'id': \"Consensus Start\" }, \n")
	f.write("\t			{'name': [\"TE Occurrences\", \"Consensus End\"],    'id': \"Consensus End\" }, \n")
	f.write("\t			{'name': [\"TFBS\", \"Overlap nt\"], 'id': \"TFBS Overlap\" }, \n") 
	f.write("\t			{'name': [\"TFBS\", \"Start\"],      'id': \"TFBS Start\" }, \n") 
	f.write("\t			{'name': [\"TFBS\", \"End\"],        'id': \"TFBS End\" }, \n") 
	f.write("\t			{'name': [\"TFBS\", \"Name\"],       'id': \"TFBS Name\" }, \n")
	f.write("\t			{'name': [\"TFBS\", \"Type\"],       'id': \"TFBS Type\" }, \n") 
	f.write("\t			{'name': [\"TFBS\", \"Tissue\"],     'id': \"TFBS Tissue\" }, \n") 
	f.write("\t			{'name': [\"TFBS\", \"Organ\"],      'id': \"TFBS Organ\" }, \n") 
	f.write("\t			{'name': [\"5' Gene\", \"Distance\"],    'id': \"5' Gene Distance\" }, \n")
	f.write("\t			{'name': [\"5' Gene\", \"Name\"],        'id': \"5' Gene Name\" }, \n")
	f.write("\t			{'name': [\"5' Gene\", \"Start\"],       'id': \"5' Gene Start\" }, \n")
	f.write("\t			{'name': [\"5' Gene\", \"End\"],         'id': \"5' Gene End\" }, \n")
	f.write("\t			{'name': [\"5' Gene\", \"Orient.\"],     'id': \"5' Gene Orient.\" }, \n")
	f.write("\t			{'name': [\"5' Gene\", \"ID\"],          'id': \"5' GeneID\" }, \n")
	f.write("\t			{'name': [\"5' Gene\", \"Function\"],    'id': \"5' Gene Function\" },  \n")
	f.write("\t			{'name': [\"3' Gene\", \"Distance\"],    'id': \"3' Gene Distance\" }, \n")
	f.write("\t			{'name': [\"3' Gene\", \"Name\"],        'id': \"3' Gene Name\" }, \n")
	f.write("\t			{'name': [\"3' Gene\", \"Start\"],       'id': \"3' Gene Start\" }, \n")
	f.write("\t			{'name': [\"3' Gene\", \"End\"],         'id': \"3' Gene End\" }, \n")
	f.write("\t			{'name': [\"3' Gene\", \"Orient.\"],     'id': \"3' Gene Orient.\" }, \n")
	f.write("\t			{'name': [\"3' Gene\", \"ID\"],          'id': \"3' GeneID\" }, \n")
	f.write("\t			{'name': [\"3' Gene\", \"Function\"],    'id': \"3' Gene Function\" }, \n")
	f.write("\t			{'name': [\"Included Gene\", \"Distance\"],    'id': \"Included Gene Distance\" }, \n")
	f.write("\t			{'name': [\"Included Gene\", \"Name\"],        'id': \"Included Gene Name\" }, \n")
	f.write("\t			{'name': [\"Included Gene\", \"Start\"],       'id': \"Included Gene Start\" }, \n")
	f.write("\t			{'name': [\"Included Gene\", \"End\"],         'id': \"Included Gene End\" }, \n")
	f.write("\t			{'name': [\"Included Gene\", \"Orient.\"],     'id': \"Included Gene Orient.\" }, \n")
	f.write("\t			{'name': [\"Included Gene\", \"ID\"],          'id': \"Included GeneID\" }, \n")
	f.write("\t			{'name': [\"Included Gene\", \"Function\"],    'id': \"Included Gene Function\" }, \n")
	f.write("\t		], \n\n")
	
	f.write("\t		style_data={ \n")
	f.write("\t			'textOverflow': 'ellipsis', \n")
	f.write("\t		}, \n")
	f.write("\t		style_data_conditional=[ \n")
	f.write("\t			{'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}, \n")
	if numberTE == 1:
		if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
			f.write("\t			{'if': {'column_id': 'Color'}, 'backgroundColor': Couleur.couleurSelectTE[0] }, \n")
		else :
			f.write("\t			{'if': {'column_id': 'Color', 'filter_query': '{TE Family} = ")
			f.write(moduleSelectTE.list_selection_TE[0])
			f.write("'}, 'backgroundColor': Couleur.couleurSelectTE[0] }, \n")
	else :
		for i in range(0, numberTE, 1) :
			f.write("\t			{'if': {'column_id': 'Color', 'filter_query': '{TE Family} = ")
			f.write(moduleSelectTE.list_selection_TE[i])
			f.write("'}, 'backgroundColor': Couleur.couleurSelectTE[")
			f.write(str(i))
			f.write("] }, \n")
	f.write("\t			{'if': {'column_id': 'Index'}, 'width': 25}, \n")
	f.write("\t			{'if': {'column_id': 'TE Family'}, 'width': 100}, \n")
	f.write("\t			{'if': {'column_id': 'Color'}, 'width': 25}, \n")
	f.write("\t			{'if': {'column_id': 'Seq Name'}, 'width': 60}, \n")
	f.write("\t			{'if': {'column_id': 'Start'}, 'width': 50}, \n")
	f.write("\t			{'if': {'column_id': 'End'}, 'width': 50}, \n")
	f.write("\t			{'if': {'column_id': 'Orientation'}, 'width': 20}, \n")
	f.write("\t			{'if': {'column_id': 'Similarity'}, 'width': 35}, \n")
	f.write("\t			{'if': {'column_id': 'Consensus Start'}, 'width': 40}, \n")
	f.write("\t			{'if': {'column_id': 'Consensus End'}, 'width': 40}, \n")
	f.write("\t			{'if': {'column_id': 'TFBS Overlap'}, 'width': 40}, \n")
	f.write("\t			{'if': {'column_id': 'TFBS Start'}, 'width': 45}, \n")
	f.write("\t			{'if': {'column_id': 'TFBS End'}, 'width': 45}, \n")
	f.write("\t			{'if': {'column_id': 'TFBS Name'}, 'width': 50}, \n")
	f.write("\t			{'if': {'column_id': 'TFBS Type'}, 'width': 150}, \n")
	f.write("\t			{'if': {'column_id': 'TFBS Tissue'}, 'width': 100}, \n")
	f.write("\t			{'if': {'column_id': 'TFBS Organ'}, 'width': 100}, \n")
	f.write("\t			{'if': {'column_id': \"5' Gene Distance\"}, 'width': 50}, \n")
	f.write("\t			{'if': {'column_id': \"5' Gene Name\"}, 'width': 60}, \n")
	f.write("\t			{'if': {'column_id': \"5' Gene Distance\"}, 'width': 50}, \n")
	f.write("\t			{'if': {'column_id': \"5' Gene Start\"}, 'width': 50}, \n")
	f.write("\t			{'if': {'column_id': \"5' Gene End\"}, 'width': 50}, \n")
	f.write("\t			{'if': {'column_id': \"5' Gene Orient.\"}, 'width': 20}, \n")
	f.write("\t			{'if': {'column_id': \"5' GeneID\"}, 'width': 30}, \n")
	f.write("\t			{'if': {'column_id': \"5' Gene Function\"}, 'width': 150}, \n")
	f.write("\t			{'if': {'column_id': \"3' Gene Distance\"}, 'width': 50}, \n")
	f.write("\t			{'if': {'column_id': \"3' Gene Name\"}, 'width': 60}, \n")
	f.write("\t			{'if': {'column_id': \"3' Gene Distance\"}, 'width': 50}, \n")
	f.write("\t			{'if': {'column_id': \"3' Gene Start\"}, 'width': 50}, \n")
	f.write("\t			{'if': {'column_id': \"3' Gene End\"}, 'width': 50}, \n")
	f.write("\t			{'if': {'column_id': \"3' Gene Orient.\"}, 'width': 20}, \n")
	f.write("\t			{'if': {'column_id': \"3' GeneID\"}, 'width': 30}, \n")
	f.write("\t			{'if': {'column_id': \"3' Gene Function\"}, 'width': 150}, \n")
	f.write("\t			{'if': {'column_id': \"Included Gene Distance\"}, 'width': 50}, \n")
	f.write("\t			{'if': {'column_id': \"Included Gene Name\"}, 'width': 60}, \n")
	f.write("\t			{'if': {'column_id': \"Included Gene Distance\"}, 'width': 50}, \n")
	f.write("\t			{'if': {'column_id': \"Included Gene Start\"}, 'width': 50}, \n")
	f.write("\t			{'if': {'column_id': \"Included Gene End\"}, 'width': 50}, \n")
	f.write("\t			{'if': {'column_id': \"Included Gene Orient.\"}, 'width': 20}, \n")
	f.write("\t			{'if': {'column_id': \"Included GeneID\"}, 'width': 30}, \n")
	f.write("\t			{'if': {'column_id': \"Included Gene Function\"}, 'width': 150}, \n")
	f.write("\t		], \n")
	
	f.write("\t		style_header={ \n")
	f.write("\t			'whiteSpace': 'normal', \n")
	f.write("\t			'height': 'auto', \n")
	f.write("\t			'backgroundColor': 'rgb(230, 230, 230)', \n")
	f.write("\t			'fontWeight': 'bold', \n")
	f.write("\t			'textAlign': 'center', \n")
	f.write("\t		}, \n")
	
	f.write("\t		style_cell={ \n")
	f.write("\t			'textAlign': 'left', \n")
	f.write("\t			'overflow': 'hidden', \n")
	f.write("\t			'whiteSpace': 'normal', \n")
	f.write("\t			'height': '20px', \n")
	f.write("\t			'lineHeight': '20px', \n")
	f.write("\t		}, \n")
	
	f.write("\t		style_table={ \n")
	f.write("\t			'height':850,\n")
	#f.write("\t			'overflowX': 'auto', 'overflowY': 'auto', \n")
	f.write("\t		}, \n")
	
	f.write("\t		tooltip_data=[ \n")
	f.write("\t		{ \n")
	f.write("\t			column: {'value': str(value), 'type': 'markdown'} \n")
	f.write("\t			for column, value in row.items() \n")
	f.write("\t		} for row in dataFrame_Summary.to_dict('rows') \n")
	f.write("\t		], \n")
	f.write("\t		tooltip_duration=None, \n\n")
	
	f.write("\t		page_size = 100, \n")
	f.write("\t		merge_duplicate_headers = True, \n")
	f.write("\t		fixed_rows={'headers': True}, \n")

	f.write("\t	),\n")
	f.write("\t], style={'width': '100%', 'display': 'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n")
	
	f.write("\treturn Onglet9_Table \n")
	f.close()
	
	
	
########################################################################################################################
###	Create The table with the data
########################################################################################################################
def CreateCallBack_Tableau_Onglet9(temp, numberTE, moduleSelectTE) :

	f = open(temp, "a")
	f.write("########################################################################################################################\n")	
	f.write("# Callbacks for the Table\n")
	
	f.write("@app.callback( \n")
	f.write("\tOutput('Onglet9_Tableau_Div', 'children'), \n")
	f.write("\t[Input('memory', 'data')]\n")
	f.write(")\n\n")

	f.write("def updateTable_Onglet9(valueSliders) : \n")
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
	
	
	
	# Create the dataframe for the table
	Dataframe_in_Table(temp, numberTE)
	# Create the table
	StyleTableInCallback9(temp, numberTE, moduleSelectTE)
	
	
	
	
	
	
	
########################################################################################################################
###	
########################################################################################################################
def Create_layout(temp):
	
	f = open(temp, "a")
	# cree le layout qui va tout contenir
	f.write("########################################################################################################################\n")
	f.write("# Creation du Layout pour dash\n\n")
	f.write("SummaryTable_layout = html.Div([ \n")
	
	f.write("\t	html.Div(id='Onglet9_Tableau_Div'), \n")
	f.write("], style={'width': '99%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)'} )\n")
	f.write("\n\n\n\n")
	f.close()
	
	
	
	
	
########################################################################################################################
###	Create the SummaryTable function
########################################################################################################################
def SummaryTable(pathVisualNEW, nbSeq_Assemble, numberTE):
	
	###############################################################################################################################################################
	# Import the recently created modules
	pathSelectTE = os.path.realpath(pathVisualNEW + '/Functions/CommonDATA_SelectTEs.py')
	loaderSelectTE = importlib.util.spec_from_file_location('CommonDATA_SelectTEs', pathSelectTE)
	moduleSelectTE = importlib.util.module_from_spec(loaderSelectTE)
	loaderSelectTE.loader.exec_module(moduleSelectTE)
	
	# Ajout des librairies python pour le serveur
	temp = pathVisualNEW + '/Functions/SummaryTable.py'
	f = open(temp, "w")

	f.write("#!/usr/bin/env python3\n")
	f.write("# -*- coding: utf-8 -*-\n")
	f.write("import dash\n")
	f.write("import dash_table\n")
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
	
	
	# Create invariable layout
	Create_layout(temp)
	
	
	
	# Create the layout with the table 
	CreateCallBack_Tableau_Onglet9(temp, numberTE, moduleSelectTE)
	
	
	
