#!/usr/bin/python3
import os
import sys
import importlib
import importlib.util
import pandas as pd
import plotly.graph_objs as go
import dash_bio as dashbio
	
	
	
	
	
########################################################################################################################
###	Create JSON file and Circos
########################################################################################################################
def CreateCircosDATA(temp, numberTE, moduleSelectTE) :

	f = open(temp, "a")
	f.write("\t######################################################################################################################## \n\n")
	
	f.write("\t	Select_myTE.sort_values(by=['Similarity'], inplace=True) \n") 
	f.write("\t	SelectionIndex_myTE = Select_myTE['Index'].tolist() \n") 
	f.write("\t	SelectionChr_myTE = Select_myTE['Chr ID'].tolist() \n") 
	f.write("\t	SelectionPosDeb_myTE = Select_myTE['Start'].tolist() \n")
	f.write("\t	SelectionPosFin_myTE = Select_myTE['End'].tolist() \n")
	f.write("\t	SelectionSim_myTE = Select_myTE['Similarity'].tolist() \n")
	f.write("\t	for i in range(0, len(SelectionIndex_myTE), 1) : \n")
	f.write("\t		SelectionIndex_myTE[i] = Selection_Family[i] + '_' + str(i) \n\n")
	f.write("\t	corde = [] \n")
	f.write("\t	oneDegre = round( (CommonDATA.totalSizeGenome + CommonDATA.totalSizeGenome / CommonDATA.nbSeq_Assemble) / 720)  \n\n\n")
	
	
	
	f.write("\t	# Create the cluster of sequences based only on similarity \n")
	f.write("\t	clusterFeuille = [] \n")
	f.write("\t	clusterIndex = [] \n")
	f.write("\t	nbCluster = -1 \n")
	f.write("\t	similariteFeuille = 0 \n")
	f.write("\t	margeCluster = 1.0 		# the value 1 can be change with some statistical test \n")
	f.write("\t	for i in range(0, len(SelectionIndex_myTE), 1) : \n")
	f.write("\t		if SelectionSim_myTE[i] - similariteFeuille < margeCluster : \n")
	f.write("\t			clusterFeuille[nbCluster].append(SelectionIndex_myTE[i]) \n")
	f.write("\t			clusterIndex[nbCluster].append(i) \n")
	f.write("\t			similariteFeuille = SelectionSim_myTE[i] \n")
	f.write("\t		else : \n")
	f.write("\t			nbCluster += 1 \n")
	f.write("\t			clusterFeuille.append([]) \n")
	f.write("\t			clusterIndex.append([]) \n")
	f.write("\t			clusterFeuille[nbCluster].append(SelectionIndex_myTE[i]) \n")
	f.write("\t			clusterIndex[nbCluster].append(i) \n")
	f.write("\t			similariteFeuille = SelectionSim_myTE[i] \n\n")
	
	f.write("\t 	# create the arc from the cluster of leaves \n")
	f.write("\t	for i in range(0, len(clusterFeuille), 1) : \n")
	f.write("\t		posDebFictiveSource = SelectionPosDeb_myTE[clusterIndex[i][0]] \n") 
	f.write("\t		posFinFictiveSource = SelectionPosFin_myTE[clusterIndex[i][0]] + oneDegre \n") 
	f.write("\t		chrFictiveSource = SelectionChr_myTE[clusterIndex[i][0]] \n")
	f.write("\t		for j in range(1, len(clusterFeuille[i]), 1) : \n")
	f.write("\t			posDebFictiveTarget = SelectionPosDeb_myTE[clusterIndex[i][j]] \n") 
	f.write("\t			posFinFictiveTarget = SelectionPosFin_myTE[clusterIndex[i][j]] + oneDegre \n") 
	f.write("\t			chrFictiveTarget = SelectionChr_myTE[clusterIndex[i][j]] \n") 
	f.write("\t			cordeSimple = { 'source': { 'id':chrFictiveSource, 'start':posDebFictiveSource, 'end':posFinFictiveSource }, 'target': { 'id':chrFictiveTarget, 'start':posDebFictiveTarget, 'end':posFinFictiveTarget } } \n")  
	f.write("\t			corde.append(cordeSimple) \n")
	
	f.write("\t	circosDATA = { 'genome':genomeDATACircos, 'chords':corde} \n")
	f.write("\t	# convert into JSON: \n")
	f.write("\t	jsonDATA = json.dumps(circosDATA) \n")
	f.write("\t	circos_graph_data.append( json.loads(jsonDATA) ) \n\n\n")
	
	f.write("\n\n\n")
	f.close()
	
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Create the phylogenic tree and the coordinate
########################################################################################################################
def CreateDataTree(temp, numberTE, moduleSelectTE) :
	
	f = open(temp, "a")
	f.write("\t######################################################################################################################## \n\n")
	
	
	if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
		f.write("\tfor z in range(0, 1, 1) : \n")
	else :
		f.write("\tfor z in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	
	f.write("\t	XNodePos.append([]) \n")
	f.write("\t	YNodePos.append([]) \n")
	f.write("\t	nbFeuille.append(0) \n")
	f.write("\t	nodes.append([]) \n")
	f.write("\t	edges.append([]) \n")
	f.write("\t	elementsCyto.append([]) \n\n")
	
	if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
		f.write("\t	Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3]), ['Index', 'Chr ID', 'Start', 'End', 'Similarity', 'TE Family'] ] \n")  
		f.write("\t	Selection_myTE = Select_myTE['Index'].tolist() \n") 
		f.write("\t	Selection_Family = Select_myTE['TE Family'].tolist() \n")
		f.write("\t	for i in range(0, len(Selection_myTE), 1) : \n")  
		f.write("\t		Selection_myTE[i] = Selection_Family[i] + '_' + str(i) \n\n") 
	else :
		f.write("\t	Select_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['TE Family'] == CommonDATA_SelectTEs.list_selection_TE[z]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3]), ['Index', 'Chr ID', 'Start', 'End', 'Similarity', 'TE Family'] ]  \n") 
		f.write("\t	Selection_myTE = Select_myTE['Index'].tolist() \n")
		f.write("\t	Selection_Family = Select_myTE['TE Family'].tolist() \n")
		f.write("\t	for i in range(0, len(Selection_myTE), 1) :  \n")
		f.write("\t		Selection_myTE[i] = CommonDATA_SelectTEs.list_selection_TE[z] + '_' + str(i) \n\n")
	
	f.write("\t	Temp_idNode = [] \n") 
	f.write("\t	Temp_nameNode = [] \n") 
	f.write("\t	Temp_parentNode = [] \n") 
	f.write("\t	Temp_profondeurNode = [] \n") 
	f.write("\t	Temp_branchLength = [] \n") 
	f.write("\t	Temp_filsNode = [] \n\n")
	
	f.write("\t	# Ajout des feuilles restantes \n")
	f.write("\t	for j in range(0, len(nameNode[z]), 1) : \n") 
	f.write("\t		for i in range(0, len(Selection_myTE), 1) : \n")
	f.write("\t			if Selection_myTE[i] == nameNode[z][j] : \n")
	f.write("\t				Temp_idNode.append(idNode[z][j]) \n")
	f.write("\t				Temp_nameNode.append(nameNode[z][j]) \n")
	f.write("\t				Temp_parentNode.append(parentNode[z][j]) \n")
	f.write("\t				Temp_profondeurNode.append(profondeurNode[z][j]) \n")
	f.write("\t				Temp_branchLength.append(branchLength[z][j]) \n")
	f.write("\t				Temp_filsNode.append(filsNode[z][j]) \n\n")
	
	f.write("\t	for i in range(maxProfound[z]-1, -1, -1) : \n")
	f.write("\t		for j in range(len(nameNode[z])-1, -1, -1) : \n")
	f.write("\t			# the node correspond to the good profound \n")
	f.write("\t			if profondeurNode[z][j] == i : \n")
	f.write("\t				# check if the node exists already in this new tree \n")
	f.write("\t				trouveNode = 0 \n")
	f.write("\t				for k in range(0, len(Temp_nameNode), 1) : \n")
	f.write("\t					if Temp_nameNode[k] == nameNode[z][j] and Temp_idNode[k] == idNode[z][j] : \n")
	f.write("\t						trouveNode = 1 \n")
	f.write("\t				if trouveNode == 0 : \n")
	f.write("\t					# and its son must exist in the new tree \n")
	f.write("\t					trouveFils = 0 \n")
	f.write("\t					for a in range(0, len(filsNode[z][j]), 1) : \n")
	f.write("\t						for k in range(0, len(Temp_nameNode), 1) : \n")
	f.write("\t							if int(Temp_idNode[k]) == int(filsNode[z][j][a]) : \n")
	f.write("\t								trouveFils = 1 \n")
	f.write("\t					if trouveFils == 1 : \n")
	f.write("\t						Temp_idNode.append(idNode[z][j]) \n")
	f.write("\t						Temp_nameNode.append(str(nameNode[z][j])) \n")
	f.write("\t						Temp_parentNode.append(parentNode[z][j]) \n")
	f.write("\t						Temp_profondeurNode.append(profondeurNode[z][j]) \n")
	f.write("\t						Temp_branchLength.append(branchLength[z][j]) \n")
	f.write("\t						Temp_filsNode.append(filsNode[z][j]) \n\n")
	
	f.write("\t	idNodeNEW = Temp_idNode \n") 
	f.write("\t	nameNodeNEW = Temp_nameNode \n") 
	f.write("\t	parentNodeNEW = Temp_parentNode \n") 
	f.write("\t	profondeurNodeNEW = Temp_profondeurNode \n") 
	f.write("\t	branchLengthNEW = Temp_branchLength \n")
	f.write("\t	filsNodeNEW = Temp_filsNode \n\n\n\n")
	
	
	
	f.write("\t	for i in range(0, len(nameNodeNEW)+1, 1) : \n") 
	f.write("\t		XNodePos[z].append(0) \n")
	f.write("\t		YNodePos[z].append(0) \n")
	f.write("\t	# Create the Y position from the NewickTree \n")
	f.write("\t	nbFeuille[z] = 0 \n")
	if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
		f.write("\t	for i in range(0, len(nameNodeNEW), 1) : \n")
		f.write("\t		for j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n") 
		f.write("\t			if str(nameNodeNEW[i]).find(CommonDATA_SelectTEs.list_selection_TE[j]) != -1 : \n")
		f.write("\t				YNodePos[z][i] = 100 + 50 * nbFeuille[z] \n")
		f.write("\t				nbFeuille[z] += 1 \n\n")
	else :
		f.write("\t	for i in range(0, len(nameNodeNEW), 1) : \n")
		f.write("\t		if str(nameNodeNEW[i]).find(CommonDATA_SelectTEs.list_selection_TE[z]) != -1 : \n")
		f.write("\t			YNodePos[z][i] = 100 + 50 * nbFeuille[z] \n")
		f.write("\t			nbFeuille[z] += 1 \n\n")
	
	f.write("\t	for k in range(maxProfound[z]-1, -1, -1) : 		# all node except and last leaves \n")
	f.write("\t		for i in range(0, len(nameNodeNEW), 1) : \n")
	f.write("\t			if int(profondeurNodeNEW[i]) == k and YNodePos[z][i] == 0 : \n")
	f.write("\t				YpositionFils = [] \n")
	f.write("\t				for j in range(0, len(filsNodeNEW[i]), 1) : \n")
	f.write("\t					for x in range(0, len(idNodeNEW), 1) : \n")
	f.write("\t						if int(filsNodeNEW[i][j]) == int(idNodeNEW[x]) : \n")
	f.write("\t							YpositionFils.append(YNodePos[z][x]) \n")
	f.write("\t				maxX = max(YpositionFils) \n")
	f.write("\t				minX = min(YpositionFils) \n")
	f.write("\t				YNodePos[z][i] = round((maxX + minX) / 2) \n\n")
	
	f.write("\t	# Create the X position from the NewickTree \n")
	f.write("\t	XNodePos[z][len(nameNodeNEW)-1] = 100	# X position for the root \n")
	f.write("\t	for i in range(0, maxProfound[z], 1) : \n")
	f.write("\t		for j in range(len(nameNodeNEW)-2, -1, -1) : # avoid root \n")
	f.write("\t			if int(profondeurNodeNEW[j]) == i and XNodePos[z][j] == 0 : # found a node in good profound \n")
	f.write("\t				for k in range(0, len(idNodeNEW), 1) : # look for its parent \n")
	f.write("\t					if int(parentNodeNEW[j]) == int(idNodeNEW[k]) : # found the parent \n")
	f.write("\t						if str(nameNodeNEW[j]).find('intermediary') != -1 or str(nameNodeNEW[j]) == '0' :	# this node j is an intermediary node \n")
	f.write("\t							XNodePos[z][j] = XNodePos[z][k] \n")
	f.write("\t						else : \n")
	f.write("\t							XNodePos[z][j] = round(XNodePos[z][k] + 2500 * float(branchLengthNEW[j]) ) + 10 \n\n\n\n")
	#f.write("\t							XNodePos[z][j] = XNodePos[z][k] + 50 \n\n\n\n")
	
	f.write("\t	numberNode = len(nameNodeNEW) \n")
	f.write("\t	for i in range(0, len(nameNodeNEW), 1) :  \n")
	f.write("\t		nested_Node = {} \n")
	f.write("\t		if len(filsNodeNEW[i]) == 0 : \n") 
	f.write("\t			nested_Node = { 'data': {'id': idNodeNEW[i], 'label':nameNodeNEW[i]}, 'position': {'x': XNodePos[z][i], 'y': YNodePos[z][i]}, 'classes': 'feuille' } \n")
	f.write("\t		else : \n")
	f.write("\t			nested_Node = { 'data': {'id': idNodeNEW[i], 'label':idNodeNEW[i]}, 'position': {'x': XNodePos[z][i], 'y': YNodePos[z][i]}, 'classes': 'internalNode' } \n")
	f.write("\t		nodes[z].append(nested_Node) \n\n")
	
	f.write("\t		if int(idNodeNEW[i]) != int(parentNodeNEW[i]) and int(parentNodeNEW[i]) >= 0: \n")
	f.write("\t			indexParent = i \n")
	f.write("\t			for j in range(0, len(nameNodeNEW), 1) : \n")
	f.write("\t				if int(parentNodeNEW[i]) == int(idNodeNEW[j]) : \n")
	f.write("\t					indexParent = j \n")
	f.write("\t			if str(nameNodeNEW[indexParent]).find('intermediary') != -1 or str(nameNodeNEW[indexParent]) == '0' : \n")
	f.write("\t				nested_Edge = { 'data': {'source': idNodeNEW[i], 'target': idNodeNEW[indexParent], 'weight':branchLengthNEW[i] }, 'classes':'edge' } \n")
	f.write("\t			else : \n")
	f.write("\t				nested_Edge = { 'data': {'source': idNodeNEW[i], 'target': idNodeNEW[indexParent] }, 'classes':'edge' } \n")
	f.write("\t			edges[z].append(nested_Edge) \n")
	f.write("\t			numberNode += 1 \n")
	
	f.write("\t	elementsCyto[z] = nodes[z] + edges[z] \n\n\n\n")
	f.close()
	
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Create the Values necessary to select the sequence in alignement
########################################################################################################################
def CreateGraphClassification(temp, numberTE, moduleSelectTE) :

	f = open(temp, "a")
	f.write("\t######################################################################################################################## \n\n")
	
	f.write("\tif 'Circos_Onglet7' in changed_id : \n")
	f.write("\t	Onglet7_Circos = html.Div([ \n")
	
	if numberTE == 1 :
		f.write("\t		html.P(CommonDATA_SelectTEs.OfficialName + ' Circos Graph', style={'text-align':'center'}), \n")
		f.write("\t		dashbio.Circos( \n")
		f.write("\t			id='my-dashbio-circos', \n")
		f.write("\t			layout=circos_graph_data[0]['genome'], \n")
		f.write("\t			selectEvent={'0':'hover', '1':'click', '2':'both'}, \n")
		f.write("\t			size = 950, \n")
		f.write("\t			tracks=[{ \n")
		f.write("\t				'type': 'CHORDS', \n")
		f.write("\t				'data': circos_graph_data[0]['chords'], \n")
		f.write("\t				'config': { \n")
		f.write("\t					'tooltipContent': { \n")
		f.write("\t						'source': 'source', \n")
		f.write("\t						'sourceID': 'id', \n")
		f.write("\t						'target': 'target', \n")
		f.write("\t						'targetID': 'id', \n")
		f.write("\t						'targetEnd': 'end' \n")
		f.write("\t					}, \n")
		f.write("\t				'color':Couleur.couleurSelectTE[0], \n")
		f.write("\t				} \n")
		f.write("\t			}], \n")
		f.write("\t			config={ \n")
		f.write("\t				'innerRadius': 350, \n")
		f.write("\t				'outerRadius': 400, \n")
		f.write("\t				'ticks': {	# ici c'est pour la graduation \n")
		f.write("\t					'display': True, \n")
		f.write("\t					'color': 'black', \n")
		f.write("\t					'spacing': 5000000, \n")
		f.write("\t					'labels': True, \n")
		f.write("\t					'labelSpacing': 10, \n")
		f.write("\t					'labelSuffix': ' Mb', \n")
		f.write("\t					'labelDenominator': 500000, \n")
		f.write("\t					'labelDisplay0': True, \n")
		f.write("\t					'labelSize': 7, \n")
		f.write("\t					'labelColor': 'black', \n")
		f.write("\t					'labelFont': 'default', \n")
		f.write("\t					'majorSpacing': 10, \n")
		f.write("\t					'size': { \n")
		f.write("\t						'minor': 2, \n")
		f.write("\t						'major': 5, \n")
		f.write("\t					} \n")
		f.write("\t				}, \n")
		f.write("\t			}, \n")
		f.write("\t		), \n")
		
		f.write("\t	], style={'width':'100%', 'height':'1000px', 'backgroundColor':'rgb(255, 255, 255)', 'overflowX': 'scroll', 'overflowY': 'scroll'} ) \n\n")
	else :
		for j in range(0, numberTE, 1) :
			titreAligne = moduleSelectTE.list_selection_TE[j]
			if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
				titreAligne = moduleSelectTE.OfficialName
			f.write("\t		html.Div([ \n")
			f.write("\t			html.P('" + titreAligne + " Circos Graph', style={'text-align':'center'}), \n")
			f.write("\t			dashbio.Circos( \n")
			f.write("\t				id='my-dashbio-circos-" + str(j) + "', \n")
			f.write("\t				layout=circos_graph_data[" + str(j) + "]['genome'], \n")
			f.write("\t				selectEvent={'0':'hover', '1':'click', '2':'both'}, \n")
			f.write("\t				size = 950, \n")
			f.write("\t				tracks=[{ \n")
			f.write("\t					'type': 'CHORDS', \n")
			f.write("\t					'data': circos_graph_data[" + str(j) + "]['chords'], \n")
			f.write("\t					'config': { \n")
			f.write("\t						'tooltipContent': { \n")
			f.write("\t							'source': 'source', \n")
			f.write("\t							'sourceID': 'id', \n")
			f.write("\t							'target': 'target', \n")
			f.write("\t							'targetID': 'id', \n")
			f.write("\t							'targetEnd': 'end' \n")
			f.write("\t						}, \n")
			f.write("\t					'color':Couleur.couleurSelectTE[" + str(j) + "], \n")
			f.write("\t					} \n")
			f.write("\t				}], \n")
			f.write("\t				config={ \n")
			f.write("\t					'innerRadius': 350, \n")
			f.write("\t					'outerRadius': 400, \n")
			f.write("\t					'ticks': {	# ici c'est pour la graduation \n")
			f.write("\t						'display': True, \n")
			f.write("\t						'color': 'black', \n")
			f.write("\t						'spacing': 5000000, \n")
			f.write("\t						'labels': True, \n")
			f.write("\t						'labelSpacing': 10, \n")
			f.write("\t						'labelSuffix': ' Mb', \n")
			f.write("\t						'labelDenominator': 500000, \n")
			f.write("\t						'labelDisplay0': True, \n")
			f.write("\t						'labelSize': 7, \n")
			f.write("\t						'labelColor': 'black', \n")
			f.write("\t						'labelFont': 'default', \n")
			f.write("\t						'majorSpacing': 10, \n")
			f.write("\t						'size': { \n")
			f.write("\t							'minor': 2, \n")
			f.write("\t							'major': 5, \n")
			f.write("\t						} \n")
			f.write("\t					}, \n")
			f.write("\t				}, \n")
			f.write("\t			), \n")
			
			if numberTE == 2 :
				widthDIV = 48.5
				f.write("\t		], style={'width':'" + str(widthDIV) + "%', 'backgroundColor':'rgb(255, 255, 255)', 'padding':'5px 5px', 'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center', ")
				if j == 0 :
					f.write("'float':'left', ")
				else :
					f.write("'float':'right', ")
			if numberTE == 3 :
				widthDIV = 31.5
				f.write("\t		], style={'width':'" + str(widthDIV) + "%', 'backgroundColor':'rgb(255, 255, 255)', 'padding':'5px 5px', 'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center', ") 
				if j == 0 :
					f.write("'float':'left', ")
				if j == 2 :
					f.write("'float':'right', ")
			f.write("}), \n\n")
			
		f.write("\t	], style={'width':'100%', 'height':'1000px', 'backgroundColor':'rgb(245, 245, 255)', 'overflowX': 'scroll', 'overflowY': 'scroll'} ) \n\n")
	f.write("\t	return Onglet7_Circos \n\n\n")
	
	
	
	f.write("\telse : \n")
	f.write("\t	Onglet7_Classif = html.Div([ \n")
	
	if numberTE == 1 :
		f.write("\t		html.Div([ \n")
		f.write("\t			html.P(CommonDATA_SelectTEs.OfficialName + ' Phylogenetic Tree', style={'text-align':'center'}), \n")
		f.write("\t			cyto.Cytoscape( \n")
		f.write("\t				id='cytoscape-phylogeny0', \n")
		f.write("\t				layout={'name': 'preset', 'fit':'true', 'pan':1}, \n")
		f.write("\t				style={'width':'100%', 'height':'1000px', 'autolock':'true'}, \n")
		f.write("\t				pan={ 'x':'0', 'y':'0' }, \n")
		f.write("\t				stylesheet=[ \n")
		f.write("\t					{'selector': 'edge', 'style': {'label': 'data(weight)', 'line-color': Couleur.couleurSelectTE[0]} }, \n")
		f.write("\t					{'selector': '.feuille', 'style': {'content': 'data(label)', 'text-halign':'right', 'text-valign':'center', 'shape':'round-rectangle'} },  \n") 
		f.write("\t					{'selector': '.internalNode', 'style': {'background-color': 'transparent', 'size':'0', 'opacity':'0'} },  \n")
		f.write("\t				], \n")
		f.write("\t				# Write now the nodes and leaves \n")
		f.write("\t				elements = elementsCyto[0], \n")
		f.write("\t			) \n")
		f.write("\t		], style={'width':'100%', 'backgroundColor':'rgb(255, 255, 255)', 'padding':'5px 5px', 'display': 'inline-block',}) ")
	else :
		for j in range(0, numberTE, 1) :
			titreAligne = moduleSelectTE.list_selection_TE[j]
			if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
				titreAligne = moduleSelectTE.OfficialName
			f.write("\t		html.Div([ \n")
			f.write("\t			html.P('" + titreAligne + " Phylogenetic Tree', style={'text-align':'center'}), \n")
			f.write("\t			cyto.Cytoscape( \n")
			f.write("\t				id='cytoscape-phylogeny-" + str(j) + "', \n")
			f.write("\t				layout={'name': 'preset', 'fit':'true', 'pan':1}, \n")
			f.write("\t				style={'width':'100%', 'height':'1000px', 'autolock':'true'}, \n")
			f.write("\t				pan={ 'x':'0', 'y':'0' }, \n")
			f.write("\t				stylesheet=[ \n")
			f.write("\t					{'selector': 'edge', 'style': {'label': 'data(weight)', 'line-color': Couleur.couleurSelectTE[" + str(j) + "]} }, \n")
			f.write("\t					{'selector': '.feuille', 'style': {'content': 'data(label)', 'text-halign':'right', 'text-valign':'center', 'shape':'round-rectangle'} },  \n") 
			f.write("\t					{'selector': '.internalNode', 'style': {'background-color': 'transparent', 'size':'0', 'opacity':'0'} },  \n")
			f.write("\t				], \n")
			f.write("\t				# Write now the nodes and leaves \n")
			f.write("\t				elements = elementsCyto[" + str(j) + "], \n")
			f.write("\t			) \n")
			
			if numberTE == 2 :
				widthDIV = 48.5
				f.write("\t		], style={'width':'" + str(widthDIV) + "%', 'backgroundColor':'rgb(255, 255, 255)', 'padding':'5px 5px', 'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center', ")
				if j == 0 :
					f.write("'float':'left', ")
				else :
					f.write("'float':'right', ")
			if numberTE == 3 :
				widthDIV = 31.5
				f.write("\t		], style={'width':'" + str(widthDIV) + "%', 'backgroundColor':'rgb(255, 255, 255)', 'padding':'5px 5px', 'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center', ") 
				if j == 0 :
					f.write("'float':'left', ")
				if j == 2 :
					f.write("'float':'right', ")
			f.write("}), \n\n")
			
	f.write("\t	], style={'width':'100%', 'height':'1000px', 'backgroundColor':'rgb(245, 245, 255)', 'overflowX': 'scroll', 'overflowY': 'scroll'} ) \n\n")
	f.write("\t	return Onglet7_Classif \n\n\n")
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Create the Values necessary to select the sequence in alignement
########################################################################################################################
def ValuesInCallback(temp) :
	
	f = open(temp, "a")
	
	f.write("\t#Sliders values \n")
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
	
	f.write("\t#Tree Cytoscape values \n")
	f.write("\tYNodePos = [[]] \n")
	f.write("\tXNodePos = [[]] \n")
	f.write("\tnbFeuille = [] \n")
	f.write("\tnodes = [[]] \n")
	f.write("\tedges = [[]] \n")
	f.write("\telementsCyto = [[]] \n\n")
	
	f.write("\t#Circos values \n")
	f.write("\tcircos_graph_data = [] \n")
	f.write("\tchanged_id = [p['prop_id'] for p in dash.callback_context.triggered][0] \n\n")
	
	f.write("\n\n\n")
	f.close()
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Create Phylogenetic tree or the Circos DATA
########################################################################################################################
def CreateCallBack_Classification_Onglet7(temp, numberTE, pathVisual, moduleSelectTE) :
	
	f = open(temp, "a")
	f.write("######################################################################################################################## \n")	
	f.write("# Callbacks for the Classification Tree\n")
	f.write("@app.callback( \n")
	f.write("	Output('Onglet7_Phylogeny_Circos_Div', 'children'), \n")
	f.write("	[Input('Phylogenetic_Onglet7', 'n_clicks'), Input('Circos_Onglet7', 'n_clicks'),  Input('memory', 'data')] \n")
	f.write(")\n\n")
	
	f.write("def updateClassication(Phylogenetic_Onglet7, Circos_Onglet7, valueSliders) : \n\n")
	
	f.write("	global idNode \n")
	f.write("	global nameNode \n")
	f.write("	global parentNode \n")
	f.write("	global profondeurNode \n")
	f.write("	global branchLength \n")
	f.write("	global filsNode \n")
	f.write("	global maxProfound \n\n")
	
	f.close()
	
	
	# Value for the modification of graph
	ValuesInCallback(temp)
	
	# Create the phylogenetic tree with the X et Y position
	CreateDataTree(temp, numberTE, moduleSelectTE)
	# Create also the Circos graph
	CreateCircosDATA(temp, numberTE, moduleSelectTE)
	# Create the graph based on user clicks
	CreateGraphClassification(temp, numberTE, moduleSelectTE)
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Create The table with the data
########################################################################################################################
def CreateCallBack_Alignement_Onglet7(temp, numberTE, pathVisual, moduleSelectTE) :
	
	f = open(temp, "a")
	f.write("########################################################################################################################\n")	
	f.write("# Callbacks for the Table\n")
	
	f.write("@app.callback( \n")
	f.write("	Output('Onglet7_Alignment_Div', 'children'), \n")
	f.write("	[Input('memory', 'data')]\n")
	f.write(")\n\n")
	
	f.write("def updateAlignement(valueSliders) : \n\n")
	f.close()
	
	
	
	# Create the variable for alignement
	ValuesInCallback(temp)
	
	
	
	# selection of data
	f = open(temp, "a")
	
	for j in range(0, numberTE, 1) :
		f.write("\tdataAlign" + str(j) + " = '' \n")
		f.write("\tnbSEQtotal" + str(j) + " = 15 \n")
		f.write("\tif len(idSEQ[" + str(j) + "]) == 0 : \n")
		f.write("\t	dataAlign" + str(j) + " = '>EMPTY\\n \\n'	# si vide \n")
		f.write("\telse : \n")
		f.write("\t	nbSEQtotal" + str(j) + " = 15 * (nbSEQtotal" + str(j) + "+1) \n")
		f.write("\t	for i in range(0, len(idSEQ[" + str(j) + "]), 1) : \n")
		f.write("\t		if sizeSEQ[" + str(j) + "][i] >= tailleMin and sizeSEQ[" + str(j) + "][i] <= tailleMax and simSEQ[" + str(j) + "][i] >= valueSliders[2] and simSEQ[" + str(j) + "][i] <= valueSliders[3] : \n")
		f.write("\t			nbSEQtotal" + str(j) + " += 15 \n")
		f.write("\t			dataAlign" + str(j) + " += idSEQ[" + str(j) + "][i] + '\\n' \n")
		f.write("\t			dataAlign" + str(j) + " += sequence[" + str(j) + "][i] + '\\n' \n")
		f.write("\t\n\n\n")
	
	
	f.write("\tOnglet7Align = html.Div([ \n\n")
	for j in range(0, numberTE, 1) :
		titreAligne = moduleSelectTE.list_selection_TE[j]
		if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
			titreAligne = moduleSelectTE.OfficialName
		
		f.write("\t	# affiche l'Alignement " + str(j) + " \n")
		f.write("\t	html.Div([ \n")
		f.write("\t		html.P('Alignment of ' + '" + titreAligne + "'), \n")
		f.write("\t		dashbio.AlignmentChart( \n")
		f.write("\t			id = 'Alignment " + str(j) + "', \n")
		f.write("\t			data = dataAlign" + str(j) + ", \n")
		f.write("\t			showconservation = False, \n")
		f.write("\t			showgap = False, \n")
		f.write("\t			showconsensus = False, \n")
		f.write("\t			colorscale = 'clustal2', \n")
		f.write("\t			height = nbSEQtotal" + str(j) + ",	# ((len(idSEQ[" + str(j) + "])+1)*15) \n")
		f.write("\t			overview = 'heatmap', \n")
		f.write("\t			textsize = 10, \n")
		f.write("\t			tilewidth = 10, \n")
		f.write("\t			tileheight = 15, \n")
		f.write("\t		), \n")
		
		f.write("\t	], style={'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(255, 255, 255)'} ),\n\n")
		f.write("\t	html.P(''), \n")
		
	f.write("\t], style={'width':'100%', 'height':'800px', 'backgroundColor':'rgb(245, 245, 255)', 'overflowX': 'scroll', 'overflowY': 'scroll'} ),\n\n")
	f.write("\treturn Onglet7Align \n\n\n\n")
	
	f.close()
	
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Create Invariable DATA
########################################################################################################################
def InvariableDATA(temp) :
	
	f = open(temp, "a")
	
	f.write("# get the total of all TE for each chromosome and in genome \n")
	f.write("# get the total of the same superfamily TE for each chromosome and in genome \n")
	f.write("# get the percentage for each chromosome and in genome \n")
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
	f.write("			MaxConsensus = CommonDATA_SelectTEs.TailleConsensus[i] \n\n\n\n")
	
	f.close()
	
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Create the Values for the circos circle
########################################################################################################################
def InvariableCircos(temp, numberTE) :
	
	f = open(temp, "a")
	f.write("######################################################################################################################## \n\n")
	f.write("#Put the invariable values that do not change with the slider for circos \n")
	f.write("SelectionName   = CommonDATA.dataFrame_Organism['Name'].tolist() \n")
	f.write("SelectionSizeBP = CommonDATA.dataFrame_Organism['Size bp'].tolist() \n\n")
	
	f.write("genomeDATACircos = [] \n")
	f.write("couleurC = 0 \n")
	f.write("for i in range(0, len(SelectionName), 1) :  \n")
	f.write("	if i % 2 == 0 : \n")
	f.write("		couleurC = 230 \n")
	f.write("	else : \n")
	f.write("		couleurC = 190 \n")
	f.write("	if SelectionName[i].find('Chr') != -1 : \n")
	f.write("		dimitif = SelectionName[i][3:] \n")
	f.write("	else : \n")
	f.write("		dimitif = SelectionName[i] \n")
	f.write("	couleurRGB = 'rgb(' + str(couleurC) + ', ' + str(couleurC) + ', ' + str(couleurC) + ')' \n")
	f.write("	chromDATA = {} \n")
	f.write("	chromDATA = { 'id':SelectionName[i], 'label':dimitif, 'color':couleurRGB, 'len':SelectionSizeBP[i] } \n")
	f.write("	genomeDATACircos.append(chromDATA) \n\n")
	
	f.write("\n\n\n")
	f.close()
	
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	SplitTree Newick Tree
########################################################################################################################
def SplitTree(temp) :
	f = open(temp, "a")
	
	f.write("########################################################################################################################\n")
	f.write("def RecursiveTree(nextid = 0, parentid = -1): # one node \n")
	f.write("	thisid = nextid \n")
	f.write("	children = [] \n")
	f.write("	name, length, delim, ch = tokens.pop(0) \n")
	f.write("	if ch == '(': \n")
	f.write("		while ch in '(,': \n")
	f.write("			node, ch, nextid = RecursiveTree(nextid+1, thisid) \n")
	f.write("			children.append(node) \n")
	f.write("		name, length, delim, ch = tokens.pop(0) \n")
	f.write("	return {'id': thisid, 'name': name, 'length': float(length) if length else None, 'parentid': parentid, 'children': children}, delim, nextid \n\n\n\n")
	
	f.close()











########################################################################################################################
###	Assign tree in list
########################################################################################################################
def TreeInVariable(temp) :
	
	f = open(temp, "a")
	
	f.write("########################################################################################################################\n")
	f.write("def TreeDecomposition(v, prefix, indexFamily) : \n\n")
	f.write("	global idNode \n")
	f.write("	global nameNode \n")
	f.write("	global parentNode \n")
	f.write("	global profondeurNode \n")
	f.write("	global branchLength \n")
	f.write("	if isinstance(v, dict):  \n")
	f.write("		for k, v2 in v.items(): \n") 
	f.write("			p2 = \"{}['{}']\".format(prefix, k) \n") 
	f.write("			TreeDecomposition(v2, p2, indexFamily)  \n")
	f.write("	elif isinstance(v, list):  \n")
	f.write("		for i, v2 in enumerate(v): \n") 
	f.write("			p2 = \"{}[{}]\".format(prefix, i) \n") 
	f.write("			TreeDecomposition(v2, p2, indexFamily) \n") 
	f.write("	else:  \n")
	f.write("		decoupe = prefix.split('[') \n")
	f.write("		profond = [] \n")
	f.write("		for i in range(0, len(decoupe), 1) : \n")
	f.write("			decoupe[i] = decoupe[i][:-1] \n")
	f.write("			if decoupe[i].find('children') != -1 : \n")
	f.write("				profond.append(decoupe[i]) \n")
	f.write("		if decoupe[len(decoupe)-1] == \"'id'\" : \n")
	f.write("			profondeurNode[indexFamily].append(len(profond)) \n")
	f.write("			idNode[indexFamily].append( str(repr(v)) ) \n")
	f.write("		if decoupe[len(decoupe)-1] == \"'name'\" : \n")
	f.write("			tempName = str(repr(v)) \n")
	f.write("			tempName = tempName[1:-1] \n")
	f.write("			if len(tempName) > 0 : \n")
	f.write("				nameNode[indexFamily].append( tempName ) \n")
	f.write("			else : \n")
	f.write("				nameNode[indexFamily].append( 0 ) \n")
	f.write("		if decoupe[len(decoupe)-1] == \"'length'\" : \n")
	f.write("			tempName = str(repr(v))  \n")
	f.write("			if tempName[1:2] == '.' : \n")
	f.write("				branchLength[indexFamily].append( round(float(tempName), 3) ) \n")
	f.write("			else : \n")
	f.write("				branchLength[indexFamily].append( 0 ) \n")
	f.write("		if decoupe[len(decoupe)-1] == \"'parentid'\" : \n")
	f.write("			parentNode[indexFamily].append( int(str(repr(v))) ) \n")
	f.write("\n\n\n")

	f.close()










########################################################################################################################
###	Read Newick Trees
########################################################################################################################
def NewickTree(temp, pathVisualNEW, numberTE) :
	
	# Cut the tree in small pieces for each node
	SplitTree(temp)
	# Put the variable of the tree in lists
	TreeInVariable(temp)
	
	f = open(temp, "a")
	f.write("########################################################################################################################\n")
	f.write("idNode = [[]] \n")
	f.write("filsNode = [[[]]] \n")
	f.write("nameNode = [[]] \n")
	f.write("parentNode = [[]] \n")
	f.write("profondeurNode = [[]] \n")
	f.write("branchLength = [[]] \n")
	f.write("maxProfound = [] \n")
	f.write("for j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("	idNode.append([]) \n")
	f.write("	filsNode.append([[]]) \n")
	f.write("	nameNode.append([]) \n")
	f.write("	parentNode.append([]) \n")
	f.write("	profondeurNode.append([]) \n")
	f.write("	branchLength.append([]) \n")
	f.write("	maxProfound.append(0) \n\n\n")
		
		
	for j in range(0, numberTE, 1) :
		absolutePath = os.path.abspath(pathVisualNEW)
		tempTree = absolutePath + '/Downloaded/TEOccurrences' + str(j) + '.newick'
	
		f.write("fichierTree = '" + tempTree + "' \n")
		f.write("f = open(fichierTree, 'r') \n")
		f.write("Newick = f.readline() \n")
		f.write("f.close() \n")
		f.write("tokens = re.findall(r'([^:;,()\s]*)(?:\s*:\s*([\d.]+)\s*)?([,);])|(\S)', Newick+';') \n")
		f.write("tree = RecursiveTree()[0] \n")
		f.write("TreeDecomposition(tree, '', " + str(j) + ") \n\n")
	
		f.write("# Add the daugthers of each internal node \n")
		f.write("for i in range(0, len(nameNode[" + str(j) +"]), 1) : \n")
		f.write("	filsNode[" + str(j) +"].append([]) \n")
		f.write("for i in range(1, len(nameNode[" + str(j) +"]), 1) : \n")
		f.write("	filsNode[" + str(j) +"][parentNode[" + str(j) +"][i]].append(idNode[" + str(j) +"][i]) \n")
	
		f.write("for i in range(0, len(nameNode[" + str(j) +"]), 1) : \n")	
		f.write("	if maxProfound[" + str(j) +"] < profondeurNode[" + str(j) +"][i] : \n")
		f.write("		maxProfound[" + str(j) +"] = profondeurNode[" + str(j) +"][i] \n")
		f.write("maxProfound[" + str(j) +"] += 1 \n\n")
	
		f.write("# Add the intermediary nodes : for the (orthogonal) edges \n")
		f.write("numberNode = len(nameNode[" + str(j) +"]) \n")
		f.write("for i in range(len(nameNode[" + str(j) +"])-1, -1, -1) : \n") 
		f.write("	if str(nameNode[" + str(j) +"][i]).find('intermediary') == -1 and len(filsNode[" + str(j) +"][i]) > 0:	# avoid the intermediary node \n")
		f.write("		for j in range (0, len(filsNode[" + str(j) +"][i]), 1) : \n")
		f.write("			idFils = filsNode[" + str(j) +"][i][j] \n\n")
	
		f.write("			# create the new node \n")
		f.write("			nameNode[" + str(j) +"].insert((i+1), 'intermediary' + str(numberNode)) \n")
		f.write("			idNode[" + str(j) +"].insert((i+1), str(numberNode)) \n")
		f.write("			branchLength[" + str(j) +"].insert((i+1), 0) \n")
		f.write("			profondeurNode[" + str(j) +"].insert((i+1), profondeurNode[" + str(j) +"][i]) \n")
		f.write("			parentNode[" + str(j) +"].insert((i+1), idNode[" + str(j) +"][i]) \n")
		f.write("			filsNode[" + str(j) +"].insert((i+1), []) \n")
		f.write("			filsNode[" + str(j) +"][i+1].append(idFils) \n\n")
		
		f.write("			# change some parameters of the parent node and children \n")
		f.write("			filsNode[" + str(j) +"][i][j] = numberNode \n")
		f.write("			for k in range (0, len(nameNode[" + str(j) +"]), 1) : \n")
		f.write("				if idNode[" + str(j) +"][k] == idFils and str(nameNode[" + str(j) +"][i]).find('intermediary') == -1 : \n")
		f.write("					parentNode[" + str(j) +"][k] = numberNode \n")
					
		f.write("			numberNode += 1 \n")
		f.write("\n\n\n")
			
	f.close()
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Read the alignement file
########################################################################################################################
def ReadAlignement(pathVisual, temp, numberTE) :
	
	absolutePath = os.path.abspath(pathVisual)
	
	f = open(temp, "a")
	f.write("########################################################################################################################\n")
	f.write("idSEQ = [[]] \n")
	f.write("sizeSEQ = [[]] \n")
	f.write("simSEQ = [[]] \n")
	f.write("sequence = [[]] \n")
	f.write("for j in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("	idSEQ.append([]) \n")
	f.write("	sizeSEQ.append([]) \n")
	f.write("	simSEQ.append([]) \n")
	f.write("	sequence.append([]) \n")
	
	for j in range(0, numberTE, 1) :
		fichierAlign = absolutePath + '/Downloaded/TEOccurrences' + str(j) + '.align'
		
		f.write("fichierAlign" + str(j) + " = '" + fichierAlign + "'\n")
		f.write("f = open(fichierAlign" + str(j) + ", 'rt') \n")
		f.write("dataAlign" + str(j) + " = f.readlines() \n")
		f.write("f.close() \n\n")
		
		f.write("for i in range(0, len(dataAlign" + str(j) + "), 1) : \n")
		f.write("	dataAlign" + str(j) + "[i].rstrip() \n")
		f.write("	if dataAlign" + str(j) + "[i][0] == '>' : \n")
		f.write("		decoupe = dataAlign" + str(j) + "[i].split(' ') \n")
		f.write("		idSEQ[" + str(j) + "].append(decoupe[0]) \n")
		f.write("		sizeSEQ[" + str(j) + "].append(float(decoupe[1])) \n")
		f.write("		simSEQ[" + str(j) + "].append(float(decoupe[2])) \n")
		f.write("		sequence[" + str(j) + "].append('') \n")
		f.write("	else : \n")
		f.write("		sequence[" + str(j) + "][len(sequence[" + str(j) + "])-1] += dataAlign" + str(j) + "[i] \n")
		
	f.write("\n\n\n")
	f.close()
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Create invariable layout that contains all
########################################################################################################################
def Create_Invariable_layout(temp, pathVisual):
	
	f = open(temp, "a")
	# cree le layout qui va tout contenir
	f.write("########################################################################################################################\n")
	f.write("# Creation du Layout pour dash\n\n")
	f.write("SimilarityOccurrences_layout = html.Div([ \n")
	
	f.write("\thtml.Div([ \n\n") 
	f.write("\t	html.Div(id='Onglet7_Alignment_Div'), \n") 
	f.write("\t], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)', 'height':810, 'overflowY': 'scroll'} ), \n\n") 
	
	f.write("\thtml.P(''), \n\n") 
	
	f.write("\thtml.Div([ \n\n") 
	
	f.write("\t	html.Div([ \n")
	f.write("\t		html.Div([ \n")
	f.write("\t			html.Label('Choose your classification type : '), \n")
	f.write("\t			html.Button('Phylogenetic Tree', id = 'Phylogenetic_Onglet7', n_clicks = 0), \n")
	f.write("\t			html.Button('Circos Graph', id = 'Circos_Onglet7', n_clicks = 0), \n")
	f.write("\t		], style={'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px' } ), \n")
	f.write("\t		html.Div(id='Onglet7_Button_Div'), \n")
	f.write("\t	], style={'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n")
	
	f.write("\t	html.Div([ \n\n")
	f.write("\t		html.Div(id='Onglet7_Phylogeny_Circos_Div'), \n")
	f.write("\t	], style={'width':'100%', 'display':'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px', 'height':1010, 'overflowY': 'scroll', 'overflowX': 'scroll' } ), \n\n")
	
	f.write("\t], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)'} ), \n") 
	
	f.write("]) \n")
	f.write("\n\n\n\n")
	f.close()
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Create the SimilarityOccurrences function
########################################################################################################################
def SimilarityOccurrences(pathVisual, nbSeq_Assemble, numberTE):
	
	###############################################################################################################################################################
	# Import the recently created modules
	pathSelectTE = os.path.realpath(pathVisual + '/Functions/CommonDATA_SelectTEs.py')
	loaderSelectTE = importlib.util.spec_from_file_location('CommonDATA_SelectTEs', pathSelectTE)
	moduleSelectTE = importlib.util.module_from_spec(loaderSelectTE)
	loaderSelectTE.loader.exec_module(moduleSelectTE)
	
	# Ajout des librairies python pour le serveur
	temp = pathVisual + '/Functions/SimilarityOccurrences.py'
	f = open(temp, "w")

	f.write("#!/usr/bin/env python3\n")
	f.write("# -*- coding: utf-8 -*-\n")
	f.write("import re \n")
	f.write("import json \n")
	f.write("import dash\n")
	f.write("import dash_daq as daq\n")
	f.write("import dash_bio as dashbio\n")
	f.write("import dash_cytoscape as cyto\n")
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
	
	
	
	# Create the invariable data about sliders
	InvariableDATA(temp)
	# Create the invariable data for Circos
	InvariableCircos(temp, numberTE)
	# Read the newick tree
	NewickTree(temp, pathVisual, numberTE)
	# Read the alignment sequence file (FASTA)
	ReadAlignement(pathVisual, temp, numberTE)
	# Create the minimal layout
	Create_Invariable_layout(temp, pathVisual)
	
	
	# Create the new layout
	CreateCallBack_Alignement_Onglet7(temp, numberTE, pathVisual, moduleSelectTE)
	# Create a second layout
	CreateCallBack_Classification_Onglet7(temp, numberTE, pathVisual, moduleSelectTE)
	
	
	
