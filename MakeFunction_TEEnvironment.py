#!/usr/bin/python3
import os
import sys
import importlib
import importlib.util
import pandas as pd
import plotly.graph_objs as go






########################################################################################################################
###	Add the graduation for the graph
########################################################################################################################
def GraduationInGraph(temp) :
	
	f = open(temp, "a")

	f.write("		for i in range(0, NombreGraduation+1, 1) :  \n")
	f.write("			textGraduation.append( round(PosMin + (( (PosMax - PosMin) / NombreGraduation) * i)) ) \n")
	f.write("		xGraduation.append(debutLigne - 5) \n")
	f.write("		xGraduation.append(debutLigne - 10) \n")
	f.write("		xGraduation.append(None) \n")
	f.write("		xGraduation.append(debutLigne - 15) \n")
	f.write("		xGraduation.append(debutLigne - 20) \n")
	f.write("		xGraduation.append(None) \n")
	f.write("		xGraduation.append(debutLigne) \n")
	f.write("		xGraduation.append(debutLigne + (100 * NombreGraduation)) \n")
	f.write("		xGraduation.append(None) \n")
	f.write("		xGraduation.append(debutLigne + (100 * NombreGraduation) + 5) \n")
	f.write("		xGraduation.append(debutLigne + (100 * NombreGraduation) + 10) \n")
	f.write("		xGraduation.append(None) \n")
	f.write("		xGraduation.append(debutLigne + (100 * NombreGraduation) + 15) \n")
	f.write("		xGraduation.append(debutLigne + (100 * NombreGraduation) + 20) \n")
	f.write("		xGraduation.append(None) \n")
	f.write("		yGraduation.append(675) \n")
	f.write("		yGraduation.append(675) \n")
	f.write("		yGraduation.append(None) \n")
	f.write("		yGraduation.append(675) \n")
	f.write("		yGraduation.append(675) \n")
	f.write("		yGraduation.append(None) \n")
	f.write("		yGraduation.append(675) \n")
	f.write("		yGraduation.append(675) \n")
	f.write("		yGraduation.append(None) \n")
	f.write("		yGraduation.append(675) \n")
	f.write("		yGraduation.append(675) \n")
	f.write("		yGraduation.append(None) \n")
	f.write("		yGraduation.append(675) \n")
	f.write("		yGraduation.append(675) \n")
	f.write("		yGraduation.append(None) \n")
	f.write("		for i in range(0, NombreGraduation+1, 1) : \n")
	f.write("			xGraduation.append(debutLigne + (100 * i) ) \n")
	f.write("			xGraduation.append(debutLigne + (100 * i) ) \n")
	f.write("			xGraduation.append(None) \n")
	f.write("			yGraduation.append(700) \n")
	f.write("			yGraduation.append(650) \n")
	f.write("			yGraduation.append(None) \n")
	f.write("			xGraduation2.append(debutLigne + (100 * i) ) \n")
	f.write("			yGraduation2.append(710) \n\n")
	
	
	f.write("		Graduate =  go.Scatter(x = xGraduation,  y = yGraduation, mode='lines', line=dict(color='black', width=1)) \n")
	f.write("		Graduate2 = go.Scatter(x = xGraduation2, y = yGraduation2, text=textGraduation, mode='text', textfont=dict(size=10), textposition='top center') \n")
	f.write("		Lines =  go.Scatter( \n") 
	f.write("			x=[debutLigne,  (debutLigne + (100 * NombreGraduation)), None,  debutLigne, (debutLigne + (100 * NombreGraduation)), None,  debutLigne, (debutLigne + (100 * NombreGraduation)), None,  debutLigne, (debutLigne + (100 * NombreGraduation)), None,  debutLigne, (debutLigne + (100 * NombreGraduation)), None,  debutLigne, (debutLigne + (100 * NombreGraduation)), None,  debutLigne, (debutLigne + (100 * NombreGraduation)), None], \n") 
	f.write("			y=[600, 600, None, 525, 525, None, 400, 400, None, 325, 325, None, 250, 250, None, 175, 175, None, 50, 50, None], \n") 
	f.write("			mode='lines', line=dict(color='black', width=2), \n") 
	f.write("		) \n") 
	f.write("		textLines = go.Scatter(x=[50, 50, 50, 50, 50, 50, 50, 50, 50], y=[600, 535, 515, 400, 325, 250, 175, 60, 40], text=['Selected TE', 'Others', 'TEs', 'Genes', 'Exons', 'ncRNAs', 'Pseudos', 'Regulatory', 'Motifs'], mode='text') \n\n\n\n")    
	
	f.close()
	
	
	
	
	
	
	
	
	

########################################################################################################################
###	Add the other TEs for the graph
########################################################################################################################
def OtherTEinGraph(temp) :
	
	f = open(temp, "a")
	
	f.write(" 		###################################################################################### \n")
	f.write("		# Now creates the other TE elements in the graph \n")
	
	f.write("		TEtext = [] \n")
	f.write("		TEposTextX = [] \n")
	f.write("		TEposTextY = [] \n")
	f.write("		listOtherTEsX = [] \n") 
	f.write("		listOtherTEsY = [] \n") 
	f.write("		colorOtherTEs = [] \n")
	f.write("		for i in range(0, 23, 1) : \n") 
	f.write("			TEtext.append([]) \n")
	f.write("			TEposTextX.append([]) \n")
	f.write("			TEposTextY.append([]) \n")
	f.write("			listOtherTEsX.append([]) \n") 
	f.write("			listOtherTEsY.append([]) \n") 
	f.write("			colorOtherTEs.append([]) \n")
	
	f.write("		for i in range(0, len(SelectionOtherTEs_PosDeb), 1) : \n") 
	f.write("			if SelectionOtherTEs_PosDeb[i] != 'VIDE' and int(SelectionOtherTEs_TEindex[i]) == valueOccurrences-1 : \n") 
	f.write("				if PosMin <= int(SelectionOtherTEs_PosFin[i]) and int(SelectionOtherTEs_PosFin[i]) <= PosMax : \n") 
	f.write("					for j in range(1, NombreGraduation+1, 1) : \n") 
	f.write("						if textGraduation[j-1] < SelectionOtherTEs_PosDeb[i] and SelectionOtherTEs_PosDeb[i] <= textGraduation[j] : \n") 
	f.write("							distanceDebutLigneEtGraduation = (100 * (j-1)) \n") 
	f.write("							distanceDerniereGraduationDEB = round( (SelectionOtherTEs_PosDeb[i] - textGraduation[j-1]) * Echelle1bp) \n") 
	f.write("							distanceDerniereGraduationFIN = round( (SelectionOtherTEs_PosFin[i] - textGraduation[j-1]) * Echelle1bp) \n") 
	f.write("							if valueRadio != 'Linear' : \n") 
	f.write("								distanceDerniereGraduationDEB = sqrt(distanceDerniereGraduationDEB) \n") 
	f.write("								distanceDerniereGraduationFIN = sqrt(distanceDerniereGraduationFIN) \n") 
	f.write("							posDebPixel_otherTEs = debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationDEB \n") 
	f.write("							posFinPixel_otherTEs = debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationFIN \n") 
	f.write("							if posFinPixel_otherTEs - posDebPixel_otherTEs >= 1 : \n")  
	f.write("								for k in range(0, len(Couleur.couleurV2), 1) : \n")  
	f.write("									if Couleur.ListeObject[k] == SelectionOtherTEs_Group[i] : \n") 
	f.write("										colorOtherTEs[k].append(Couleur.couleurV2[k]) \n")
	f.write("										listOtherTEsX[k].append( posDebPixel_otherTEs ) \n")
	f.write("										listOtherTEsX[k].append( posDebPixel_otherTEs ) \n")
	f.write("										listOtherTEsX[k].append( posFinPixel_otherTEs ) \n")
	f.write("										listOtherTEsX[k].append( posFinPixel_otherTEs ) \n")
	f.write("										listOtherTEsX[k].append( posDebPixel_otherTEs ) \n")
	f.write("										listOtherTEsX[k].append( None ) \n")
	f.write("										listOtherTEsY[k].append( 500 ) \n")
	f.write("										listOtherTEsY[k].append( 550 ) \n")
	f.write("										listOtherTEsY[k].append( 550 ) \n")
	f.write("										listOtherTEsY[k].append( 500 ) \n")
	f.write("										listOtherTEsY[k].append( 500 ) \n") 
	f.write("										listOtherTEsY[k].append( None ) \n")
	f.write("										TEtext[k].append( 'TE family: ' + SelectionOtherTEs_Family[i] + ' (' + SelectionOtherTEs_Group[i] + ') <br> Positions : ' + str(SelectionOtherTEs_PosDeb[i]) + ' - ' + str(SelectionOtherTEs_PosFin[i]) + ' ' + SelectionOtherTEs_Sens[i]) \n")
	f.write("										TEposTextX[k].append( (posDebPixel_otherTEs+posFinPixel_otherTEs)/2 ) \n")
	f.write("										TEposTextY[k].append( 525 ) \n")
	f.write("										break \n") 
	f.write("							break \n\n") 

	f.write("		OtherTEsElement0 = go.Scatter( x = listOtherTEsX[0], y = listOtherTEsY[0], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[0]) ) \n") 
	f.write("		OtherTEtext0     = go.Scatter( x = TEposTextX[0],    y = TEposTextY[0], mode = None, name = '', textposition='top center', text = TEtext[0], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[0])) ) \n")
	f.write("		OtherTEsElement1 = go.Scatter( x = listOtherTEsX[1], y = listOtherTEsY[1], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[1]) ) \n")
	f.write("		OtherTEtext1     = go.Scatter( x = TEposTextX[1],    y = TEposTextY[1], mode = None, name = '', textposition='top center', text = TEtext[1], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[1])) ) \n")
	f.write("		OtherTEsElement2 = go.Scatter( x = listOtherTEsX[2], y = listOtherTEsY[2], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[2]) ) \n")
	f.write("		OtherTEtext2     = go.Scatter( x = TEposTextX[2],    y = TEposTextY[2], mode = None, name = '', textposition='top center', text = TEtext[2], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[2])) ) \n")
	f.write("		OtherTEsElement3 = go.Scatter( x = listOtherTEsX[3], y = listOtherTEsY[3], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[3]) ) \n")
	f.write("		OtherTEtext3     = go.Scatter( x = TEposTextX[3],    y = TEposTextY[3], mode = None, name = '', textposition='top center', text = TEtext[3], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[3])) ) \n")
	f.write("		OtherTEsElement4 = go.Scatter( x = listOtherTEsX[4], y = listOtherTEsY[4], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[4]) ) \n")
	f.write("		OtherTEtext4     = go.Scatter( x = TEposTextX[4],    y = TEposTextY[4], mode = None, name = '', textposition='top center', text = TEtext[4], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[4])) ) \n")
	f.write("		OtherTEsElement5 = go.Scatter( x = listOtherTEsX[5], y = listOtherTEsY[5], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[5]) ) \n")
	f.write("		OtherTEtext5     = go.Scatter( x = TEposTextX[5],    y = TEposTextY[5], mode = None, name = '', textposition='top center', text = TEtext[5], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[5])) ) \n")
	f.write("		OtherTEsElement6 = go.Scatter( x = listOtherTEsX[6], y = listOtherTEsY[6], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[6]) ) \n")
	f.write("		OtherTEtext6     = go.Scatter( x = TEposTextX[6],    y = TEposTextY[6], mode = None, name = '', textposition='top center', text = TEtext[6], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[6])) ) \n")
	f.write("		OtherTEsElement7 = go.Scatter( x = listOtherTEsX[7], y = listOtherTEsY[7], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[7]) ) \n")
	f.write("		OtherTEtext7     = go.Scatter( x = TEposTextX[7],    y = TEposTextY[7], mode = None, name = '', textposition='top center', text = TEtext[7], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[7])) ) \n")
	f.write("		OtherTEsElement8 = go.Scatter( x = listOtherTEsX[8], y = listOtherTEsY[8], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[8]) ) \n")
	f.write("		OtherTEtext8     = go.Scatter( x = TEposTextX[8],    y = TEposTextY[8], mode = None, name = '', textposition='top center', text = TEtext[8], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[8])) ) \n")
	f.write("		OtherTEsElement9 = go.Scatter( x = listOtherTEsX[9], y = listOtherTEsY[9], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[9]) ) \n")
	f.write("		OtherTEtext9     = go.Scatter( x = TEposTextX[9],    y = TEposTextY[9], mode = None, name = '', textposition='top center', text = TEtext[9], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[9])) ) \n")
	f.write("		OtherTEsElement10 = go.Scatter( x = listOtherTEsX[10], y = listOtherTEsY[10], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[10]) ) \n")
	f.write("		OtherTEtext10     = go.Scatter( x = TEposTextX[10],    y = TEposTextY[10], mode = None, name = '', textposition='top center', text = TEtext[10], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[10])) ) \n")
	f.write("		OtherTEsElement11 = go.Scatter( x = listOtherTEsX[11], y = listOtherTEsY[11], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[11]) ) \n")
	f.write("		OtherTEtext11     = go.Scatter( x = TEposTextX[11],    y = TEposTextY[11], mode = None, name = '', textposition='top center', text = TEtext[11], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[11])) ) \n")
	f.write("		OtherTEsElement12 = go.Scatter( x = listOtherTEsX[12], y = listOtherTEsY[12], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[12]) ) \n")
	f.write("		OtherTEtext12     = go.Scatter( x = TEposTextX[12],    y = TEposTextY[12], mode = None, name = '', textposition='top center', text = TEtext[12], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[12])) ) \n")
	f.write("		OtherTEsElement13 = go.Scatter( x = listOtherTEsX[13], y = listOtherTEsY[13], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[13]) ) \n")
	f.write("		OtherTEtext13     = go.Scatter( x = TEposTextX[13],    y = TEposTextY[13], mode = None, name = '', textposition='top center', text = TEtext[13], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[13])) ) \n")
	f.write("		OtherTEsElement14 = go.Scatter( x = listOtherTEsX[14], y = listOtherTEsY[14], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[14]) ) \n")
	f.write("		OtherTEtext14     = go.Scatter( x = TEposTextX[14],    y = TEposTextY[14], mode = None, name = '', textposition='top center', text = TEtext[14], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[14])) ) \n")
	f.write("		OtherTEsElement15 = go.Scatter( x = listOtherTEsX[15], y = listOtherTEsY[15], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[15]) ) \n")
	f.write("		OtherTEtext15     = go.Scatter( x = TEposTextX[15],    y = TEposTextY[15], mode = None, name = '', textposition='top center', text = TEtext[15], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[15])) ) \n")
	f.write("		OtherTEsElement16 = go.Scatter( x = listOtherTEsX[16], y = listOtherTEsY[16], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[16]) ) \n")
	f.write("		OtherTEtext16     = go.Scatter( x = TEposTextX[16],    y = TEposTextY[16], mode = None, name = '', textposition='top center', text = TEtext[16], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[16])) ) \n")
	f.write("		OtherTEsElement17 = go.Scatter( x = listOtherTEsX[17], y = listOtherTEsY[17], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[17]) ) \n")
	f.write("		OtherTEtext17     = go.Scatter( x = TEposTextX[17],    y = TEposTextY[17], mode = None, name = '', textposition='top center', text = TEtext[17], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[17])) ) \n")
	f.write("		OtherTEsElement18 = go.Scatter( x = listOtherTEsX[18], y = listOtherTEsY[18], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[18]) ) \n")
	f.write("		OtherTEtext18     = go.Scatter( x = TEposTextX[18],    y = TEposTextY[18], mode = None, name = '', textposition='top center', text = TEtext[18], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[18])) ) \n")
	f.write("		OtherTEsElement19 = go.Scatter( x = listOtherTEsX[19], y = listOtherTEsY[19], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[19]) ) \n")
	f.write("		OtherTEtext19     = go.Scatter( x = TEposTextX[19],    y = TEposTextY[19], mode = None, name = '', textposition='top center', text = TEtext[19], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[19])) ) \n")
	f.write("		OtherTEsElement20 = go.Scatter( x = listOtherTEsX[20], y = listOtherTEsY[20], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[20]) ) \n")
	f.write("		OtherTEtext20     = go.Scatter( x = TEposTextX[20],    y = TEposTextY[20], mode = None, name = '', textposition='top center', text = TEtext[20], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[20])) ) \n")
	f.write("		OtherTEsElement21 = go.Scatter( x = listOtherTEsX[21], y = listOtherTEsY[21], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[21]) ) \n")
	f.write("		OtherTEtext21     = go.Scatter( x = TEposTextX[21],    y = TEposTextY[21], mode = None, name = '', textposition='top center', text = TEtext[21], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[21])) ) \n")
	f.write("		OtherTEsElement22 = go.Scatter( x = listOtherTEsX[22], y = listOtherTEsY[22], fill='toself', mode='lines', marker=dict(color=colorOtherTEs[22]) ) \n")
	f.write("		OtherTEtext22     = go.Scatter( x = TEposTextX[22],    y = TEposTextY[22], mode = None, name = '', textposition='top center', text = TEtext[22], hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=colorOtherTEs[22])) ) \n")
	f.write("\n\n\n")
	
	f.close()
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Add the genes to the graph
########################################################################################################################
def AddGenesInGraph(temp) :
	
	f = open(temp, "a")
	
	f.write(" 		###################################################################################### \n")
	f.write("		# Now creates the genes elements in the graph \n")
	f.write("		limit5prime = -1 \n")
	f.write("		limit3prime = -1 \n")		
	f.write("		posDebPixel_Gene = 0 \n")
	f.write("		posFinPixel_Gene = 0 \n")
	f.write("		PosFlecheX_Gene = [] \n")
	f.write("		PosFlecheY_Gene = [] \n")
	f.write("		informationGenes = [] \n")
	f.write("		infosGeneX = [] \n")
	f.write("		infosGeneY = [] \n\n")
			
	f.write("		if indiceGeneMin != -1 : \n\n") 
			
	f.write("			indiceDebJ = -1 \n")
	f.write("			indiceFinJ = -1 \n")
	f.write("			distanceDebutLigneEtGraduation = -1 \n")
	f.write("			distanceDerniereGraduationDEB = 0 \n")
	f.write("			distanceDerniereGraduationFIN = 0 \n")
	f.write("			for j in range(1, NombreGraduation+1, 1) : \n")
	f.write("				if textGraduation[j-1] < int(SelectionGene_PosDeb[indiceGeneMin]) and int(SelectionGene_PosDeb[indiceGeneMin]) <= textGraduation[j] : \n")
	f.write("					indiceDebJ = j \n")
	f.write("				if textGraduation[j-1] < int(SelectionGene_PosFin[indiceGeneMin]) and int(SelectionGene_PosFin[indiceGeneMin]) <= textGraduation[j] : \n")
	f.write("					indiceFinJ = j \n")
	f.write("			if indiceDebJ != -1 : \n")
	f.write("				distanceDerniereGraduationDEB = round( (int(SelectionGene_PosDeb[indiceGeneMin]) - textGraduation[indiceDebJ-1]) * Echelle1bp) \n")
	f.write("				distanceDerniereGraduationFIN = round( (int(SelectionGene_PosFin[indiceGeneMin]) - textGraduation[indiceFinJ-1]) * Echelle1bp) \n")
	f.write("				if valueRadio != 'Linear' : \n")
	f.write("					distanceDerniereGraduationDEB = sqrt(distanceDerniereGraduationDEB) \n")
	f.write("					distanceDerniereGraduationFIN = sqrt(distanceDerniereGraduationFIN) \n")
	f.write("				distanceDebutLigneEtGraduation = (100 * (indiceDebJ-1)) \n")
	f.write("				posDebPixel_Gene = debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationDEB \n")
	f.write("				distanceDebutLigneEtGraduation = (100 * (indiceFinJ-1)) \n")
	f.write("				posFinPixel_Gene = debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationFIN \n")
	f.write("			elif indiceDebJ == -1 and indiceFinJ != -1 : \n")
	f.write("				distanceDebutLigneEtGraduation = (100 * (indiceFinJ-1)) \n")
	f.write("				distanceDerniereGraduationDEB = 0 \n")
	f.write("				distanceDerniereGraduationFIN = round( (int(SelectionGene_PosFin[indiceGeneMin]) - textGraduation[indiceFinJ-1]) * Echelle1bp) \n")
	f.write("				if valueRadio != 'Linear' : \n")
	f.write("					distanceDerniereGraduationDEB = sqrt(distanceDerniereGraduationDEB) \n")
	f.write("					distanceDerniereGraduationFIN = sqrt(distanceDerniereGraduationFIN) \n")
	f.write("				posDebPixel_Gene = debutLigne \n")
	f.write("				posFinPixel_Gene = debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationFIN \n")
	f.write("				limit5prime = 1 \n\n")
				
	f.write("			if distanceDebutLigneEtGraduation != -1 : \n")
	f.write("				if SelectionGene_Sens[indiceGeneMin] == '+' : \n")
	f.write("					if limit5prime == 1 : \n")
	f.write("						PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400) \n")
	f.write("						PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400 + 25) \n")
	f.write("						PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400 + 15) \n")
	f.write("						PosFlecheX_Gene.append(posDebPixel_Gene - 20) \n")
	f.write("						PosFlecheY_Gene.append(400 + 15) \n")
	f.write("						PosFlecheX_Gene.append(posDebPixel_Gene - 20) \n")
	f.write("						PosFlecheY_Gene.append(400 - 15) \n")
	f.write("						PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400 - 15) \n")
	f.write("						PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400 - 25) \n")
	f.write("						PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400) \n")
	f.write("					else : \n")
	f.write("						PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400) \n") 
	f.write("						PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("						PosFlecheY_Gene.append(400 + 25) \n")
	f.write("						PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("						PosFlecheY_Gene.append(400 + 15) \n")
	f.write("						PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400 + 15) \n")
	f.write("						PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400 - 15) \n")
	f.write("						PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("						PosFlecheY_Gene.append(400 - 15) \n")
	f.write("						PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("						PosFlecheY_Gene.append(400 - 25) \n")
	f.write("						PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400) \n")
	f.write("				else : \n")
	f.write("					if limit5prime == 1 : \n")
	f.write("						PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400 + 15) \n")
	f.write("						PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400 + 15) \n")
	f.write("						PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400 + 25) \n")
	f.write("						PosFlecheX_Gene.append(posDebPixel_Gene - 20) \n")
	f.write("						PosFlecheY_Gene.append(400) \n")
	f.write("						PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400 - 25) \n")
	f.write("						PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400 - 15) \n")
	f.write("						PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400 - 15) \n")
	f.write("						PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400 + 15) \n")
	f.write("					else : \n")
	f.write("						PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400) \n") 
	f.write("						PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("						PosFlecheY_Gene.append(400 + 25) \n") 
	f.write("						PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("						PosFlecheY_Gene.append(400 + 15) \n")
	f.write("						PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400 + 15) \n")
	f.write("						PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400 - 15) \n")
	f.write("						PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("						PosFlecheY_Gene.append(400 - 15) \n")
	f.write("						PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("						PosFlecheY_Gene.append(400 - 25) \n")
	f.write("						PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("						PosFlecheY_Gene.append(400) \n")
	f.write("				PosFlecheX_Gene.append(None) \n")
	f.write("				PosFlecheY_Gene.append(None) \n")
	f.write("				if isinstance(SelectionGene_Function[indiceGeneMin], numbers.Number) == True:  \n")
	f.write("					SelectionGene_Function[indiceGeneMin] = 'UNKNOWN' \n")
	f.write("				informationGenes.append(SelectionGene_Name[indiceGeneMin] + ' ; ' + SelectionGene_Function[indiceGeneMin] + '<br>' + SelectionGene_PosDeb[indiceGeneMin] + ' - ' + SelectionGene_PosFin[indiceGeneMin] + ' (' + SelectionGene_Sens[indiceGeneMin] + ')' ) \n")  
	f.write("				infosGeneX.append( (posFinPixel_Gene + posDebPixel_Gene) / 2 ) \n")
	f.write("				infosGeneY.append( 435 ) \n\n\n")
				
	f.write("		if indiceGeneMax != -1 : \n \n")
			
	f.write("			indiceDebJ = -1 \n")
	f.write("			indiceFinJ = -1 \n")
	f.write("			distanceDebutLigneEtGraduation = -1 \n")
	f.write("			distanceDerniereGraduationDEB = 0 \n")
	f.write("			distanceDerniereGraduationFIN = 0 \n")
	f.write("			for j in range(1, NombreGraduation+1, 1) : \n")
	f.write("				if textGraduation[j-1] < int(SelectionGene_PosDeb[indiceGeneMax]) and int(SelectionGene_PosDeb[indiceGeneMax]) <= textGraduation[j] : \n")
	f.write("					indiceDebJ = j \n")
	f.write("				if textGraduation[j-1] < int(SelectionGene_PosFin[indiceGeneMax]) and int(SelectionGene_PosFin[indiceGeneMax]) <= textGraduation[j] : \n")
	f.write("					indiceFinJ = j \n")
	f.write("			if indiceFinJ != -1 : \n")
	f.write("				distanceDerniereGraduationDEB = round( (int(SelectionGene_PosDeb[indiceGeneMax]) - textGraduation[indiceDebJ-1]) * Echelle1bp) \n")
	f.write("				distanceDerniereGraduationFIN = round( (int(SelectionGene_PosFin[indiceGeneMax]) - textGraduation[indiceFinJ-1]) * Echelle1bp) \n")
	f.write("				if valueRadio != 'Linear' : \n")
	f.write("					distanceDerniereGraduationDEB = sqrt(distanceDerniereGraduationDEB) \n")
	f.write("					distanceDerniereGraduationFIN = sqrt(distanceDerniereGraduationFIN) \n")
	f.write("				distanceDebutLigneEtGraduation = (100 * (indiceDebJ-1)) \n")
	f.write("				posDebPixel_Gene = debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationDEB \n")
	f.write("				distanceDebutLigneEtGraduation = (100 * (indiceFinJ-1)) \n")
	f.write("				posFinPixel_Gene = debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationFIN \n")
	f.write("			elif indiceFinJ == -1 and indiceDebJ != -1 : \n")
	f.write("				distanceDerniereGraduationDEB = round( (int(SelectionGene_PosDeb[indiceGeneMax]) - textGraduation[indiceDebJ-1]) * Echelle1bp) \n")
	f.write("				distanceDerniereGraduationFIN = 0 \n")
	f.write("				if valueRadio != 'Linear' : \n")
	f.write("					distanceDerniereGraduationDEB = sqrt(distanceDerniereGraduationDEB) \n")
	f.write("					distanceDerniereGraduationFIN = sqrt(distanceDerniereGraduationFIN) \n")
	f.write("				distanceDebutLigneEtGraduation = (100 * (indiceDebJ-1)) \n")
	f.write("				posDebPixel_Gene = debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationDEB \n")
	f.write("				posFinPixel_Gene = debutLigne + (100 * (NombreGraduation)) \n")
	f.write("				limit3prime = 1 \n\n")
			
	f.write("			if SelectionGene_Sens[indiceGeneMax] == '+' : \n")
	f.write("				if limit3prime == 1 : \n")
	f.write("					PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("					PosFlecheY_Gene.append(400 + 15) \n")
	f.write("					PosFlecheX_Gene.append(posFinPixel_Gene + 20) \n")
	f.write("					PosFlecheY_Gene.append(400 + 15) \n")
	f.write("					PosFlecheX_Gene.append(posFinPixel_Gene + 20) \n")
	f.write("					PosFlecheY_Gene.append(400 - 15) \n")
	f.write("					PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("					PosFlecheY_Gene.append(400 - 15) \n")
	f.write("					PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("					PosFlecheY_Gene.append(400 + 15) \n")
	f.write("				else : \n")
	f.write("					PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("					PosFlecheY_Gene.append(400) \n")
	f.write("					PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("					PosFlecheY_Gene.append(400 + 25) \n")
	f.write("					PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("					PosFlecheY_Gene.append(400 + 15) \n")
	f.write("					PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("					PosFlecheY_Gene.append(400 + 15) \n")
	f.write("					PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("					PosFlecheY_Gene.append(400 - 15) \n")
	f.write("					PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("					PosFlecheY_Gene.append(400 - 15) \n") 
	f.write("					PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("					PosFlecheY_Gene.append(400 - 25) \n")
	f.write("					PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("					PosFlecheY_Gene.append(400) \n")
	f.write("			else : \n")
	f.write("				if limit3prime == 1 : \n")
	f.write("					PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("					PosFlecheY_Gene.append(400) \n")
	f.write("					PosFlecheX_Gene.append(posFinPixel_Gene + 20) \n")
	f.write("					PosFlecheY_Gene.append(400 - 25) \n")
	f.write("					PosFlecheX_Gene.append(posFinPixel_Gene + 20) \n")
	f.write("					PosFlecheY_Gene.append(400 + 25) \n")
	f.write("					PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("					PosFlecheY_Gene.append(400) \n")
	f.write("				else : \n")
	f.write("					PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("					PosFlecheY_Gene.append(400) \n") 
	f.write("					PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("					PosFlecheY_Gene.append(400 + 25) \n") 
	f.write("					PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("					PosFlecheY_Gene.append(400 + 15) \n")
	f.write("					PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("					PosFlecheY_Gene.append(400 + 15) \n")
	f.write("					PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("					PosFlecheY_Gene.append(400 - 15) \n")
	f.write("					PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("					PosFlecheY_Gene.append(400 - 15) \n")
	f.write("					PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("					PosFlecheY_Gene.append(400 - 25) \n")
	f.write("					PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("					PosFlecheY_Gene.append(400) \n")
	f.write("			PosFlecheX_Gene.append(None) \n")
	f.write("			PosFlecheY_Gene.append(None) \n")
	f.write("			if isinstance(SelectionGene_Function[indiceGeneMax], numbers.Number) == True:  \n")
	f.write("				SelectionGene_Function[indiceGeneMax] = 'UNKNOWN' \n")
	f.write("			informationGenes.append( SelectionGene_Name[indiceGeneMax] + ' ; ' + SelectionGene_Function[indiceGeneMax] + '<br>' + SelectionGene_PosDeb[indiceGeneMax] + ' - ' + SelectionGene_PosFin[indiceGeneMax] + ' (' + SelectionGene_Sens[indiceGeneMax] + ')' ) \n") 
	f.write("			infosGeneX.append( (posFinPixel_Gene + posDebPixel_Gene) / 2 ) \n")
	f.write("			infosGeneY.append( 435 ) \n\n\n")
				
		
	f.write("		if indiceGeneInside != -1 : \n\n")
			
	f.write("			indiceDebJ = -1 \n") 
	f.write("			indiceFinJ = -1 \n")
	f.write("			distanceDebutLigneEtGraduation = -1 \n")
	f.write("			distanceDerniereGraduationDEB = 0 \n")
	f.write("			distanceDerniereGraduationFIN = 0 \n")
	f.write("			posDebPixel_Gene = 0 \n")
	f.write("			posFinPixel_Gene = 0 \n")
	f.write("			for j in range(1, NombreGraduation+1, 1) : \n")
	f.write("				if textGraduation[j-1] < int(SelectionGene_PosDeb[indiceGeneInside]) and int(SelectionGene_PosDeb[indiceGeneInside]) <= textGraduation[j] : \n")
	f.write("					indiceDebJ = j \n")
	f.write("				if textGraduation[j-1] < int(SelectionGene_PosFin[indiceGeneInside]) and int(SelectionGene_PosFin[indiceGeneInside]) <= textGraduation[j] : \n")
	f.write("					indiceFinJ = j \n")
	f.write("			if indiceDebJ != -1 : \n")
	f.write("				distanceDebutLigneEtGraduation = (100 * (indiceDebJ-1)) \n")
	f.write("				distanceDerniereGraduationDEB = round( (int(SelectionGene_PosDeb[indiceGeneInside]) - textGraduation[indiceDebJ-1]) * Echelle1bp) \n")
	f.write("				if valueRadio != 'Linear' : \n")
	f.write("					distanceDerniereGraduationDEB = sqrt(distanceDerniereGraduationDEB) \n")
	f.write("				posDebPixel_Gene = debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationDEB \n")
	f.write("			else : \n")
	f.write("				posDebPixel_Gene = debutLigne - 20 \n")
	f.write("			if indiceFinJ != -1 : \n")
	f.write("				distanceDebutLigneEtGraduation = (100 * (indiceFinJ-1)) \n")
	f.write("				distanceDerniereGraduationFIN = round( (int(SelectionGene_PosFin[indiceGeneInside]) - textGraduation[indiceFinJ-1]) * Echelle1bp) \n")
	f.write("				if valueRadio != 'Linear' : \n")
	f.write("					distanceDerniereGraduationFIN = sqrt(distanceDerniereGraduationFIN) \n")
	f.write("				posFinPixel_Gene = debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationFIN \n")
	f.write("			else : \n")
	f.write("				posFinPixel_Gene = debutLigne + (100 * (NombreGraduation)) + 20 \n\n")
	
	f.write("			if SelectionGene_Sens[indiceGeneInside] == '+' : \n")
	f.write("				PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("				PosFlecheY_Gene.append(400) \n") 
	f.write("				PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("				PosFlecheY_Gene.append(400 + 25) \n")
	f.write("				PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("				PosFlecheY_Gene.append(400 + 15) \n")
	f.write("				PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("				PosFlecheY_Gene.append(400 + 15) \n")
	f.write("				PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("				PosFlecheY_Gene.append(400 - 15) \n")
	f.write("				PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("				PosFlecheY_Gene.append(400 - 15) \n") 
	f.write("				PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("				PosFlecheY_Gene.append(400 - 25) \n")
	f.write("				PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("				PosFlecheY_Gene.append(400) \n")
	f.write("			else : \n")
	f.write("				PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("				PosFlecheY_Gene.append(400) \n") 
	f.write("				PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("				PosFlecheY_Gene.append(400 + 25) \n") 
	f.write("				PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("				PosFlecheY_Gene.append(400 + 15) \n")
	f.write("				PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("				PosFlecheY_Gene.append(400 + 15) \n")
	f.write("				PosFlecheX_Gene.append(posFinPixel_Gene) \n")
	f.write("				PosFlecheY_Gene.append(400 - 15) \n")
	f.write("				PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("				PosFlecheY_Gene.append(400 - 15) \n")
	f.write("				PosFlecheX_Gene.append((posFinPixel_Gene + posDebPixel_Gene) / 2) \n")
	f.write("				PosFlecheY_Gene.append(400 - 25) \n")
	f.write("				PosFlecheX_Gene.append(posDebPixel_Gene) \n")
	f.write("				PosFlecheY_Gene.append(400) \n")
	f.write("			PosFlecheX_Gene.append(None) \n")
	f.write("			PosFlecheY_Gene.append(None) \n")
	f.write("			if isinstance(SelectionGene_Function[indiceGeneInside], numbers.Number) == True:  \n")
	f.write("				SelectionGene_Function[indiceGeneInside] = 'UNKNOWN' \n")
	f.write("			informationGenes.append( SelectionGene_Name[indiceGeneInside] + ' ; ' + SelectionGene_Function[indiceGeneInside] + '<br>' + SelectionGene_PosDeb[indiceGeneInside] + ' - ' + SelectionGene_PosFin[indiceGeneInside] + ' (' + SelectionGene_Sens[indiceGeneInside] + ')' ) \n") 
	f.write("			infosGeneX.append( (posFinPixel_Gene + posDebPixel_Gene) / 2 ) \n")
	f.write("			infosGeneY.append( 435 ) \n\n")
			
	f.write("		GeneElements = go.Scatter( x= PosFlecheX_Gene, y = PosFlecheY_Gene, fill='toself', fillcolor='white', mode='lines', marker_color=Couleur.couleurV2[23] ) \n")
	f.write("		Genesinfo = go.Scatter( x=infosGeneX, y=infosGeneY, mode = 'text', name = '', textposition='top center', text = informationGenes, textfont=dict(color=Couleur.couleurV2[23]) ) \n\n\n\n")		
	
	f.close()
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Add the Exons to the graph
########################################################################################################################
def AddExonsInGraph(temp) :
	
	f = open(temp, "a")	
	
	f.write(" 		###################################################################################### \n")
	f.write("		# Now creates the exon elements from gene in the graph \n")
	f.write("		listExonX = [] \n")
	f.write("		listExonY = [] \n")
	f.write("		infoXExon = [] \n")
	f.write("		infoYExon = [] \n")
	f.write("		infoTextExon = [] \n")
			
	f.write("		for i in range(0, len(SelectionExon_PosDeb), 1) : \n")
	f.write("			distanceDebutLigneEtGraduation = -1 \n")
	f.write("			distanceDerniereGraduationDEB = 0 \n")
	f.write("			distanceDerniereGraduationFIN = 0 \n")
	f.write("			posDebPixel_Exons = 0 \n")
	f.write("			posFinPixel_Exons = 0 \n")
	f.write("			if SelectionExon_PosDeb[i] != 'VIDE' and int(SelectionExon_TEindex[i]) == valueOccurrences-1 : \n")
	f.write("				if PosMin <= int(SelectionExon_PosDeb[i]) and int(SelectionExon_PosFin[i]) <= PosMax :  \n")
	f.write("					for j in range(1, NombreGraduation+1, 1) : \n")
	f.write("						if textGraduation[j-1] < int(SelectionExon_PosDeb[i]) and int(SelectionExon_PosDeb[i]) <= textGraduation[j] : \n")
	f.write("							distanceDebutLigneEtGraduation = (100 * (j-1)) \n")
	f.write("							distanceDerniereGraduationDEB = round( (int(SelectionExon_PosDeb[i]) - textGraduation[j-1]) * Echelle1bp) \n")
	f.write("							distanceDerniereGraduationFIN = round( (int(SelectionExon_PosFin[i]) - textGraduation[j-1]) * Echelle1bp) \n")
	f.write("							if valueRadio != 'Linear' : \n")
	f.write("								distanceDerniereGraduationDEB = sqrt(distanceDerniereGraduationDEB) \n")
	f.write("								distanceDerniereGraduationFIN = sqrt(distanceDerniereGraduationFIN) \n")
	f.write("							posDebPixel_Exons = round(debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationDEB) \n")
	f.write("							posFinPixel_Exons = round(debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationFIN) \n")
	f.write("							if posFinPixel_Exons - posDebPixel_Exons >= 1 : \n")
	f.write("								listExonX.append( posDebPixel_Exons ) \n")
	f.write("								listExonX.append( posDebPixel_Exons ) \n")
	f.write("								listExonX.append( posFinPixel_Exons ) \n")
	f.write("								listExonX.append( posFinPixel_Exons ) \n")
	f.write("								listExonX.append( posDebPixel_Exons ) \n")
	f.write("								listExonX.append( None ) \n")
	f.write("								listExonY.append( 300 ) \n")
	f.write("								listExonY.append( 350 ) \n")
	f.write("								listExonY.append( 350 ) \n")
	f.write("								listExonY.append( 300 ) \n")
	f.write("								listExonY.append( 300 ) \n")
	f.write("								listExonY.append( None ) \n")
	f.write("								infoXExon.append( (posFinPixel_Exons+posDebPixel_Exons) / 2 ) \n")
	f.write("								infoYExon.append( 325 ) \n")
	f.write("								infoTextExon.append( str(SelectionExon_PosDeb[i]) + ' - ' + str(SelectionExon_PosFin[i]) ) \n")
	f.write("							break \n\n")

	f.write("		ExonElement = go.Scatter( x = listExonX, y = listExonY, fill='toself', fillcolor=Couleur.couleurV2[23], mode='lines', marker_color=Couleur.couleurV2[23] ) \n")
	f.write("		ExonInfos = go.Scatter( x = infoXExon, y = infoYExon, mode = 'markers', name = '', textposition='top center', text = infoTextExon, hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=Couleur.couleurV2[23])) ) \n\n\n\n")  
	f.close()
				
				
				
				
				
				
				
				
				
				
########################################################################################################################
###	Add the ncRNAs to the graph
########################################################################################################################
def AddncRNAinGraph(temp) :
	
	f = open(temp, "a")
				
	f.write("		###################################################################################### \n")
	f.write("		# Now creates the ncRNAs elements in the graph \n")
	f.write("		list_ncRNA_X = [] \n")
	f.write("		list_ncRNA_Y = [] \n")
	f.write("		ncRNA_infosX = [] \n")
	f.write("		ncRNA_infosY = [] \n")
	f.write("		ncRNA_infosText = [] \n")
	f.write("		for i in range(0, len(Selection_ncRNAs_PosDeb), 1) : \n")
	f.write("			posDeb_ncRNA = 0 \n")
	f.write("			posFin_ncRNA = 0 \n")
	f.write("			distanceDebutLigneEtGraduation = -1 \n")
	f.write("			distanceDerniereGraduationDEB = 0 \n")
	f.write("			distanceDerniereGraduationFIN = 0 \n")
	f.write("			if Selection_ncRNAs_PosDeb[i] != 'VIDE' and int(Selection_ncRNAs_TEindex[i]) == valueOccurrences-1 : \n")
	f.write("				if PosMin <= int(Selection_ncRNAs_PosDeb[i]) and int(Selection_ncRNAs_PosFin[i]) <= PosMax : \n")
	f.write("					for j in range(1, NombreGraduation+1, 1) : \n")
	f.write("						if textGraduation[j-1] < int(Selection_ncRNAs_PosDeb[i]) and int(Selection_ncRNAs_PosDeb[i]) <= textGraduation[j] : \n")
	f.write("							distanceDebutLigneEtGraduation = (100 * (j-1)) \n")
	f.write("							distanceDerniereGraduationDEB = round( (int(Selection_ncRNAs_PosDeb[i]) - textGraduation[j-1]) * Echelle1bp) \n")
	f.write("							distanceDerniereGraduationFIN = round( (int(Selection_ncRNAs_PosFin[i]) - textGraduation[j-1]) * Echelle1bp) \n")
	f.write("							if valueRadio != 'Linear' : \n")
	f.write("								distanceDerniereGraduationDEB = sqrt(distanceDerniereGraduationDEB) \n")
	f.write("								distanceDerniereGraduationFIN = sqrt(distanceDerniereGraduationFIN) \n")
	f.write("							posDeb_ncRNA = round(debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationDEB) \n")
	f.write("							posFin_ncRNA = round(debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationFIN) \n")
	f.write("							if posFin_ncRNA - posDeb_ncRNA >= 1 : \n")
	f.write("								list_ncRNA_X.append( posDeb_ncRNA ) \n") 
	f.write("								list_ncRNA_X.append( posDeb_ncRNA ) \n") 
	f.write("								list_ncRNA_X.append( posFin_ncRNA ) \n")
	f.write("								list_ncRNA_X.append( posFin_ncRNA ) \n")
	f.write("								list_ncRNA_X.append( posDeb_ncRNA ) \n")
	f.write("								list_ncRNA_X.append( None ) \n")
	f.write("								list_ncRNA_Y.append( 275 ) \n")
	f.write("								list_ncRNA_Y.append( 225 ) \n")
	f.write("								list_ncRNA_Y.append( 225 ) \n")
	f.write("								list_ncRNA_Y.append( 275 ) \n")
	f.write("								list_ncRNA_Y.append( 275 ) \n")
	f.write("								list_ncRNA_Y.append( None ) \n")
	f.write("								ncRNA_infosX.append( (posFin_ncRNA+posDeb_ncRNA)/2 ) \n")
	f.write("								ncRNA_infosY.append( 250 ) \n")
	f.write("								ncRNA_infosText.append( Selection_ncRNAs_Type[i] + ' : ' + str(Selection_ncRNAs_PosDeb[i]) + ' - ' + str(Selection_ncRNAs_PosFin[i]) + ' (' + Selection_ncRNAs_Sens[i] + ')' ) \n\n")
			
	f.write("		ncRNAElement = go.Scatter( x = list_ncRNA_X, y = list_ncRNA_Y, fill='toself', fillcolor=Couleur.couleurV2[25], mode='lines', marker_color=Couleur.couleurV2[25] ) \n") 
	f.write("		ncRNA_Infos = go.Scatter( x = ncRNA_infosX, y = ncRNA_infosY, mode = 'markers', name = '', textposition='top center', text = ncRNA_infosText, hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=Couleur.couleurV2[25])) ) \n\n\n\n") 
	f.close()
			
		
		
		
		
		
		
		
		
		
		
########################################################################################################################
###	Add the Pseudogenes to the graph
########################################################################################################################
def AddPseudogenesInGraph(temp) :
	
	f = open(temp, "a")		
		
	f.write("		###################################################################################### \n")
	f.write("		# Now creates the Pseudogenes elements in the graph \n")
	f.write("		listPseudo_X = [] \n")
	f.write("		listPseudo_Y = [] \n")
	f.write("		Pseudo_Xinfos = [] \n")
	f.write("		Pseudo_Yinfos = [] \n")
	f.write("		Pseudo_text = [] \n")
	f.write("		for i in range(0, len(SelectionPseudos_PosDeb), 1) : \n")
	f.write("			posDeb_Pseudo = 0 \n")
	f.write("			posFin_Pseudo = 0 \n")
	f.write("			distanceDebutLigneEtGraduation = -1 \n")
	f.write("			distanceDerniereGraduationDEB = 0 \n")
	f.write("			distanceDerniereGraduationFIN = 0 \n")
	f.write("			if SelectionPseudos_PosDeb[i] != 'VIDE' and int(SelectionPseudos_TEindex[i]) == valueOccurrences-1 : \n")
	f.write("				if PosMin <= int(SelectionPseudos_PosDeb[i]) and int(SelectionPseudos_PosFin[i]) <= PosMax : \n")
	f.write("					for j in range(1, NombreGraduation+1, 1) : \n")
	f.write("						if textGraduation[j-1] < int(SelectionPseudos_PosDeb[i]) and int(SelectionPseudos_PosDeb[i]) <= textGraduation[j] : \n")
	f.write("							distanceDebutLigneEtGraduation = (100 * (j-1)) \n")
	f.write("							distanceDerniereGraduationDEB = round( (int(SelectionPseudos_PosDeb[i]) - textGraduation[j-1]) * Echelle1bp) \n")
	f.write("							distanceDerniereGraduationFIN = round( (int(SelectionPseudos_PosFin[i]) - textGraduation[j-1]) * Echelle1bp) \n")
	f.write("							if valueRadio != 'Linear' : \n")
	f.write("								distanceDerniereGraduationDEB = sqrt(distanceDerniereGraduationDEB) \n")
	f.write("								distanceDerniereGraduationFIN = sqrt(distanceDerniereGraduationFIN) \n")
	f.write("							posDeb_Pseudo = round(debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationDEB) \n")
	f.write("							posFin_Pseudo = round(debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationFIN) \n")
	f.write("							if posFin_Pseudo - posDeb_Pseudo >= 1 : \n")
	f.write("								listPseudo_X.append( posDeb_Pseudo ) \n")
	f.write("								listPseudo_X.append( posDeb_Pseudo ) \n")
	f.write("								listPseudo_X.append( posFin_Pseudo ) \n")
	f.write("								listPseudo_X.append( posFin_Pseudo ) \n")
	f.write("								listPseudo_X.append( posDeb_Pseudo ) \n")
	f.write("								listPseudo_X.append( None ) \n")
	f.write("								listPseudo_Y.append( 200 ) \n")
	f.write("								listPseudo_Y.append( 150 ) \n")
	f.write("								listPseudo_Y.append( 150 ) \n")
	f.write("								listPseudo_Y.append( 200 ) \n")
	f.write("								listPseudo_Y.append( 200 ) \n")
	f.write("								listPseudo_Y.append( None ) \n")
	f.write("								Pseudo_Xinfos.append( (posFin_Pseudo+posDeb_Pseudo)/2 ) \n")
	f.write("								Pseudo_Yinfos.append( 175 ) \n")
	f.write("								Pseudo_text.append( SelectionPseudos_Name[i] + ' : ' + str(SelectionPseudos_PosDeb[i]) + ' - ' + str(SelectionPseudos_PosFin[i]) + ' (' + SelectionPseudos_Sens[i] + ')' ) \n\n")
		
	f.write("		PseudoElement = go.Scatter( x = listPseudo_X, y = listPseudo_Y, fill='toself', fillcolor='white', mode='lines', marker_color=Couleur.couleurV2[24] ) \n")
	f.write("		Pseudo_Infos = go.Scatter( x = Pseudo_Xinfos, y = Pseudo_Yinfos, mode = 'markers', name = '', textposition='top center', text = Pseudo_text, hovertemplate = '%{text}', hoverlabel_align = 'right', hoverinfo='none', hoverlabel=dict(bgcolor='white', font_size=16, font=dict(color=Couleur.couleurV2[24])) ) \n\n\n\n") 
	f.close()		
			
			
			
			
			
			
			
			
			
			
			
########################################################################################################################
###	Add the Pseudogenes to the graph
########################################################################################################################
def AddCHiSepInGraph(temp) :
	
	f = open(temp, "a")		
		
	f.write("		###################################################################################### \n") 
	f.write("		# Now reads the Chipseq data for the TE Occurrences \n")
	f.write("		filename = 'Downloaded/Selected_ChipSeq/ChipSeq_for__' + Selection_Family[valueOccurrences-1] + '__occurrences_' + str(valueOccurrences-1) + '_.txt' \n")
	f.write("		# memorize lines from file \n")
	f.write("		f = open(filename, 'r') \n")
	f.write("		lignes = f.readlines() \n\n")
	
	f.write("		f.close() \n")
	f.write("		# put all columns in list \n")
	f.write("		chipSeqDeb = [] \n")
	f.write("		chipSeqFin = [] \n")
	f.write("		chipSeqSens = [] \n")
	f.write("		chipSeqScore = [] \n")
	f.write("		chipSeqName = [] \n")
	f.write("		chipSeqType = [] \n")
	f.write("		chipSeqTissue = [] \n")
	f.write("		chipSeqOrgan = [] \n")
	f.write("		for i in range(1, len(lignes), 1) :  \n")
	f.write("			lignes[i] = lignes[i].rstrip() \n")
	f.write("			coupe = lignes[i].split(',') \n\n")
	
	f.write("			getChipSEQ = 0 \n")
	f.write("			decoupe = coupe[7].split('__') \n")
	f.write("			for j in range(0, len(decoupe), 1) : \n")
	f.write("				test = dict(optionsTissue[valueTissue]) \n")
	f.write("				typeTissue = list(test.values()) \n") 
	f.write("				if valueTissue == 0 or typeTissue[0] == decoupe[j] : \n") 
	f.write("					getChipSEQ = 1 \n")
	f.write("					break \n")
	f.write("			if getChipSEQ == 1 : \n")
	f.write("				decoupe = coupe[8].split('__') \n")
	f.write("				for j in range(0, len(decoupe), 1) : \n")
	f.write("					test = dict(optionsOrgan[valueOrgan]) \n")
	f.write("					typeOrgan = list(test.values()) \n") 
	f.write("					if valueOrgan == 0 or typeOrgan[0] == decoupe[j] : \n") 
	f.write("						getChipSEQ = 2 \n")
	f.write("						break \n")
	f.write("			if getChipSEQ == 2 : \n")
	f.write("				chipSeqDeb.append( coupe[1] ) \n")
	f.write("				chipSeqFin.append( coupe[2] ) \n")
	f.write("				chipSeqSens.append( coupe[3] ) \n")
	f.write("				chipSeqScore.append( coupe[4] ) \n")
	f.write("				chipSeqName.append( coupe[5] ) \n")
	f.write("				chipSeqType.append( coupe[6] ) \n")
	f.write("				chipSeqTissue.append( coupe[7] ) \n")
	f.write("				chipSeqOrgan.append( coupe[8] ) \n\n")
			
	f.write("		chipSeqX = [] \n")
	f.write("		chipSeqY = [] \n")
	f.write("		for i in range(0, len(chipSeqDeb)-1, 1) : \n") 
	f.write("			posDeb_ChipSEQ = 0 \n")
	f.write("			posFin_ChipSEQ = 0 \n") 
	f.write("			distanceDebutLigneEtGraduation = -1 \n") 
	f.write("			distanceDerniereGraduationDEB = 0 \n") 
	f.write("			distanceDerniereGraduationFIN = 0 \n") 
	f.write("			if PosMin <= int(chipSeqDeb[i]) and int(chipSeqFin[i]) <= PosMax : \n") 
	f.write("					for j in range(1, NombreGraduation+1, 1) : \n") 
	f.write("						if textGraduation[j-1] < int(chipSeqDeb[i]) and int(chipSeqDeb[i]) <= textGraduation[j] : \n") 
	f.write("							distanceDebutLigneEtGraduation = (100 * (j-1)) \n") 
	f.write("							distanceDerniereGraduationDEB = round( (int(chipSeqDeb[i]) - textGraduation[j-1]) * Echelle1bp) \n") 
	f.write("							distanceDerniereGraduationFIN = round( (int(chipSeqFin[i]) - textGraduation[j-1]) * Echelle1bp) \n") 
	f.write("							if valueRadio != 'Linear' : \n") 
	f.write("								distanceDerniereGraduationDEB = sqrt(distanceDerniereGraduationDEB) \n") 
	f.write("								distanceDerniereGraduationFIN = sqrt(distanceDerniereGraduationFIN) \n") 
	f.write("							posDeb_ChipSEQ = round(debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationDEB) \n") 
	f.write("							posFin_ChipSEQ = round(debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationFIN) \n") 
	f.write("							if posFin_ChipSEQ - posDeb_ChipSEQ >= 1 : \n") 
	f.write("								chipSeqX.append( posDeb_ChipSEQ ) \n")
	f.write("								chipSeqX.append( (posDeb_ChipSEQ + posFin_ChipSEQ)/2 ) \n")
	f.write("								chipSeqX.append( posFin_ChipSEQ ) \n")
	f.write("								chipSeqX.append( posDeb_ChipSEQ ) \n")
	f.write("								chipSeqX.append( None ) \n")
	f.write("								chipSeqY.append( 50 ) \n")
	f.write("								if int(chipSeqScore[i]) <= 100 : \n")
	f.write("									chipSeqY.append( 60 ) \n")
	f.write("								elif int(chipSeqScore[i]) <= 200 : \n")
	f.write("									chipSeqY.append( 65 ) \n")
	f.write("								elif int(chipSeqScore[i]) <= 300 : \n")
	f.write("									chipSeqY.append( 70 ) \n")
	f.write("								elif int(chipSeqScore[i]) <= 400 : \n")
	f.write("									chipSeqY.append( 75 ) \n")
	f.write("								elif int(chipSeqScore[i]) <= 500 : \n")
	f.write("									chipSeqY.append( 80 ) \n")
	f.write("								elif int(chipSeqScore[i]) <= 600 : \n")
	f.write("									chipSeqY.append( 85 ) \n")
	f.write("								elif int(chipSeqScore[i]) <= 700 : \n")
	f.write("									chipSeqY.append( 90 ) \n")
	f.write("								elif int(chipSeqScore[i]) <= 800 : \n")
	f.write("									chipSeqY.append( 95 ) \n")
	f.write("								elif int(chipSeqScore[i]) <= 900 : \n")
	f.write("									chipSeqY.append( 100 ) \n")
	f.write("								else : \n")
	f.write("									chipSeqY.append( 105 ) \n")
	f.write("								chipSeqY.append( 50 ) \n")
	f.write("								chipSeqY.append( 50 ) \n")
	f.write("								chipSeqY.append( None ) \n")
	f.write("							break \n\n")
			
	f.write("		ChipSEQgraph = go.Scatter( x = chipSeqX, y = chipSeqY, fill='toself', opacity=0.5, fillcolor='grey', mode='lines', marker=dict(color='rgba(200, 200, 200, 0.1)', line=dict( color='rgba(0, 0, 0, 0.25)', width=1) ) )  \n\n\n\n")   
	f.close()	











########################################################################################################################
###	Create the graph with the combobox
########################################################################################################################
def CreateCallBack_Slider(temp, numberTE) :
	
	f = open(temp, "a")
	
	f.write("########################################################################################################################\n")
	
	f.write("@app.callback( \n")
	f.write("	[Output('Choix_TFBS_Tissue', 'options'), Output('Choix_TFBS_Tissue', 'value'), Output('Choix_TFBS_Organ', 'options'), Output('Choix_TFBS_Organ', 'value') ], \n")
	f.write("	[Input('Choix_TE_occurrences', 'value'),], \n")
	f.write(") \n\n")
	
	f.write("def update_ChipSeq(valueOccurrences): \n\n")
	
	f.write("	global Selection_Family \n")
	f.write("	valueOccurrences = int(valueOccurrences) \n")
	f.write("	options_Tissue = [ {'label': 'Tissue, Nothing Yet', 'value': 0}, ] \n")
	f.write("	options_Organ  = [ {'label': 'Organ, Nothing Yet', 'value': 0}, ] \n")
	f.write("	valeur = 0 \n\n")
	
	f.write("	if valueOccurrences != 0 : \n")
	f.write("		filename = 'Downloaded/Selected_ChipSeq/ChipSeq_for__' + Selection_Family[valueOccurrences-1] + '__occurrences_' + str(valueOccurrences-1) + '_.txt' \n")
	f.write("		# memorize lines from file \n")
	f.write("		f = open(filename, 'r') \n")
	f.write("		lignes = f.readlines() \n")
	f.write("		f.close() \n\n")
		
	f.write("		nbTissue = 1 \n")
	f.write("		nbOrgan = 1 \n")
	f.write("		dicoTissue = {'All': 0} \n")
	f.write("		dicoOrgan = {'All': 0} \n")
	f.write("		for i in range(1, len(lignes), 1) : \n")
	f.write("			lignes[i] = lignes[i].rstrip() \n")
	f.write("			coupe = lignes[i].split(',') \n\n")
			
	f.write("			decoupe = coupe[7].split('__') \n")
	f.write("			for j in range(0, len(decoupe), 1) : \n")
	f.write("				if decoupe[j] in dicoTissue.keys() : \n")
	f.write("					print('',end='') \n")
	f.write("				else : \n")
	f.write("					dicoTissue[decoupe[j]] = nbTissue \n")
	f.write("					nbTissue += 1 \n\n")
				
	f.write("			decoupe = coupe[8].split('__') \n")
	f.write("			for j in range(0, len(decoupe), 1) : \n")
	f.write("				if decoupe[j] in dicoOrgan.keys() : \n")
	f.write("					print('',end='') \n")
	f.write("				else :  \n")
	f.write("					dicoOrgan[decoupe[j]] = nbOrgan \n")
	f.write("					nbOrgan += 1 \n\n")
			
	f.write("		options_Tissue = [ {'label': x, 'value': dicoTissue[x]} for x in dicoTissue ] \n")
	f.write("		options_Organ  = [ {'label': x, 'value': dicoOrgan[x]}  for x in dicoOrgan ] \n\n")
	
	f.write("	return options_Tissue, valeur, options_Organ, valeur \n\n\n\n")
	
	
	
	f.write("########################################################################################################################\n")
	f.write("# Lecture du Dropdown pour le choix du TE \n\n")
	f.write("@app.callback( \n")
	f.write("	Output('UCSC_like', 'figure'), \n")
	f.write("	[Input('Choix_TE_occurrences', 'value'), Input('Choix_graphique', 'value'), Input('Choix_TFBS_Tissue', 'options'), Input('Choix_TFBS_Tissue', 'value'), Input('Choix_TFBS_Organ', 'options'), Input('Choix_TFBS_Organ', 'value'), ] ) \n\n")
	
	f.write("def update_FigureOccurrences(valueOccurrences, valueRadio, optionsTissue, valueTissue, optionsOrgan, valueOrgan) : \n\n")
	
	f.write("	global SelectionIndex_myTE \n")
	f.write("	global SelectionChr_myTE \n")
	f.write("	global SelectionPosDeb_myTE \n")
	f.write("	global SelectionPosFin_myTE \n")
	f.write("	global SelectionSens_myTE \n")
	f.write("	global SelectionSim_myTE \n")
	f.write("	global Selection_Family \n")
	f.write("	global SelectionCombobox_myTE \n\n")
	
	f.write("	global SelectionGene_TEindex \n")
	f.write("	global SelectionGene_relation \n")
	f.write("	global SelectionGene_TEfamily \n")
	f.write("	global SelectionGene_Name \n")
	f.write("	global SelectionGene_PosDeb \n")
	f.write("	global SelectionGene_PosFin \n")
	f.write("	global SelectionGene_Sens \n")
	f.write("	global SelectionGene_ID \n")
	f.write("	global SelectionGene_Function \n\n")
	
	f.write("	global SelectionExon_TEindex \n")
	f.write("	global SelectionExon_TEfamily \n")
	f.write("	global SelectionExon_PosDeb \n")
	f.write("	global SelectionExon_PosFin \n\n") 
	
	f.write("	global Select_OtherTEs \n")
	f.write("	global SelectionOtherTEs_TEindex \n")
	f.write("	global SelectionOtherTEs_TEfamily \n")
	f.write("	global SelectionOtherTEs_PosDeb \n")
	f.write("	global SelectionOtherTEs_PosFin \n")
	f.write("	global SelectionOtherTEs_Sens \n")
	f.write("	global SelectionOtherTEs_Family \n")
	f.write("	global SelectionOtherTEs_Group \n\n")  
		
	f.write("	global Select_ncRNAs \n")
	f.write("	global Selection_ncRNAs_TEindex \n") 
	f.write("	global Selection_ncRNAs_TEfamily \n")
	f.write("	global Selection_ncRNAs_PosDeb \n")
	f.write("	global Selection_ncRNAs_PosFin \n")
	f.write("	global Selection_ncRNAs_Sens \n")
	f.write("	global Selection_ncRNAs_Type \n")
	f.write("	global Selection_ncRNAs_ID \n\n")  
		
	f.write("	global Select_Pseudos \n")
	f.write("	global SelectionPseudos_TEindex \n") 
	f.write("	global SelectionPseudos_TEfamily \n")
	f.write("	global SelectionPseudos_PosDeb \n")
	f.write("	global SelectionPseudos_PosFin \n")
	f.write("	global SelectionPseudos_Sens \n")
	f.write("	global SelectionPseudos_ID \n")
	f.write("	global SelectionPseudos_Name \n\n")
	
	
	f.write("	if int(valueOccurrences) > 0 : \n\n")
	
	f.write("		indiceOccurrence = int(SelectionIndex_myTE[valueOccurrences-1]) \n")
	f.write("		numeroTE = 0 \n")
	f.write("		for y in range(0, len(CommonDATA_SelectTEs.list_selection_TE), 1) : \n")
	f.write("			if CommonDATA_SelectTEs.list_selection_TE[y] == SelectionGene_TEfamily[valueOccurrences-1] : \n")
	f.write("				numeroTE = y \n\n")
		
	f.write("		# Calculate a distance for each TE occurrences \n")
	f.write("		PosMin = 1000000000 \n")
	f.write("		PosMax = 0 \n")
	f.write("		indiceGeneMin = -1 \n")
	f.write("		indiceGeneMax = -1 \n")
	f.write("		indiceGeneInside = -1 \n")
	f.write("		for j in range(0, len(SelectionGene_PosDeb), 1) : \n") 
	f.write("			if int(SelectionGene_TEindex[j]) == indiceOccurrence : \n") 
	f.write("				if SelectionGene_relation[j] == \"5'\" and SelectionGene_PosDeb[j] != \"VIDE\" and indiceGeneMin == -1 : \n") 
	f.write("					PosMin = int(SelectionGene_PosFin[j])	# Fin du 1er gene \n") 
	f.write("					indiceGeneMin = j \n") 
	f.write("				if SelectionGene_relation[j] == \"3'\" and SelectionGene_PosDeb[j] != \"VIDE\" and indiceGeneMax == -1 : \n") 
	f.write("					PosMax = int(SelectionGene_PosDeb[j])	# Debut du 2eme gene \n") 
	f.write("					indiceGeneMax = j \n") 
	f.write("				if SelectionGene_relation[j] == \"Inside\" and SelectionGene_PosDeb[j] != \"VIDE\" and indiceGeneInside == -1 :	# gene indiceGeneInside \n") 
	f.write("					indiceGeneInside = j \n")
	f.write("		if PosMin == 1000000000 and SelectionPosDeb_myTE[valueOccurrences-1] - PosMin > 100000000 :\n")
	f.write("			PosMin = SelectionPosDeb_myTE[valueOccurrences-1] - 100000 \n")
	f.write("		else : \n")
	f.write("			PosMin = PosMin - 10000 # pour dessiner gene en - 1 \n")
	f.write("			if PosMin < 1 : \n")
	f.write("				PosMin = 1 \n")
	f.write("		if PosMax == 0 :\n")
	f.write("			PosMax = SelectionPosFin_myTE[valueOccurrences-1] + 100000 \n")
	f.write("		else : \n")
	f.write("			PosMax = PosMax + 10000 # pour dessiner gene en + 1 \n")
	f.write("\n\n\n")
	
	
	f.write("		DistanceMax = PosMax - PosMin \n")
	f.write("		TailleGraphique = 0 \n")
	f.write("		textGraduation = [] \n")
	f.write("		xGraduation = [] \n")
	f.write("		yGraduation = [] \n")
	f.write("		xGraduation2 = [] \n")
	f.write("		yGraduation2 = [] \n")
	f.write("		Echelle1bp = 1 \n")
	f.write("		debutLigne = 150 \n\n\n")
	
	
	f.write("		if valueRadio == 'Linear' : \n\n")
	f.write("			if DistanceMax < 20000 : \n")
	f.write("				TailleGraphique = DistanceMax + 200 \n")
	f.write("				NombreGraduation = round(DistanceMax / 100) + 1 \n")
	f.write("			else : \n")
	f.write("				TailleGraphique = 20200 \n")
	f.write("				NombreGraduation = 200 \n")
	f.write("				Echelle1bp = TailleGraphique / DistanceMax  \n\n")
	f.write("		else : \n\n")
	f.write("			DistanceMax = round(sqrt(PosMax - PosMin)) + 1 \n")
	f.write("			NombreGraduation = round(DistanceMax / 100) + 1 \n")
	f.write("			TailleGraphique = DistanceMax + 200 \n")
	f.write("			Echelle1bp = sqrt(TailleGraphique / (PosMax - PosMin)) \n\n\n\n")
	f.close()
	
	
	GraduationInGraph(temp)
	
	
	f = open(temp, "a")
	
	f.write(" 		###################################################################################### \n")
	f.write("		# Now creates the selected TE elements in the graph \n")
	f.write("		distanceDebutLigneEtGraduation = 0 \n")
	f.write("		distanceDerniereGraduationDEB = 0 \n")
	f.write("		distanceDerniereGraduationFIN = 0 \n")
	f.write("		for i in range(1, NombreGraduation+1, 1) : \n")
	f.write("			if textGraduation[i-1] < SelectionPosDeb_myTE[valueOccurrences-1] and SelectionPosDeb_myTE[valueOccurrences-1] <= textGraduation[i] : \n")
	f.write("				distanceDebutLigneEtGraduation = (100 * (i-1)) \n") 
	f.write("				distanceDerniereGraduationDEB = round( (SelectionPosDeb_myTE[valueOccurrences-1] - textGraduation[i-1]) * Echelle1bp) \n")
	f.write("				distanceDerniereGraduationFIN = round( (SelectionPosFin_myTE[valueOccurrences-1] - textGraduation[i-1]) * Echelle1bp) \n")
	f.write("		if valueRadio != 'Linear' : \n")
	f.write("			distanceDerniereGraduationDEB = sqrt(distanceDerniereGraduationDEB) \n")
	f.write("			distanceDerniereGraduationFIN = sqrt(distanceDerniereGraduationFIN) \n")
	f.write("		posDebPixel_TE = debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationDEB \n")
	f.write("		posFinPixel_TE = debutLigne + distanceDebutLigneEtGraduation + distanceDerniereGraduationFIN \n")
	f.write("		if (posFinPixel_TE - posDebPixel_TE) < 1 : \n")
	f.write("			posFinPixel_TE = posDebPixel_TE + 1 \n")
	f.write("		TransposableElement = go.Scatter( \n")
	f.write("			x=[posDebPixel_TE, posDebPixel_TE, posFinPixel_TE, posFinPixel_TE, posDebPixel_TE], \n")
	f.write("			y=[575, 625, 625, 575, 575], \n")
	f.write("			fill='toself', mode='lines', marker_color=Couleur.couleurSelectTE[numeroTE] \n")
	f.write("		) \n\n\n\n")
	f.close()
	
	
	OtherTEinGraph(temp)
	
	
	AddGenesInGraph(temp)
	
	
	AddExonsInGraph(temp)
	
	
	AddncRNAinGraph(temp)
	
	
	AddPseudogenesInGraph(temp)
	
	
	AddCHiSepInGraph(temp)
	
	
	f = open(temp, "a")
	
	f.write("		fig = {  \n")
	f.write("			'data': [Graduate, Graduate2, Lines, textLines, \n")
	f.write("				OtherTEsElement0, OtherTEtext0, OtherTEsElement1, OtherTEtext1, \n")
	f.write("				OtherTEsElement2, OtherTEtext2, OtherTEsElement3, OtherTEtext3, \n")
	f.write("				OtherTEsElement4, OtherTEtext4, OtherTEsElement5, OtherTEtext5, \n")
	f.write("				OtherTEsElement6, OtherTEtext6, OtherTEsElement7, OtherTEtext7, \n")
	f.write("				OtherTEsElement8, OtherTEtext8, OtherTEsElement9, OtherTEtext9, \n")
	f.write("				OtherTEsElement10, OtherTEtext10, OtherTEsElement11, OtherTEtext11, \n")
	f.write("				OtherTEsElement12, OtherTEtext12, OtherTEsElement13, OtherTEtext13, \n")
	f.write("				OtherTEsElement14, OtherTEtext14, OtherTEsElement15, OtherTEtext15, \n")
	f.write("				OtherTEsElement16, OtherTEtext16, OtherTEsElement17, OtherTEtext17, \n")
	f.write("				OtherTEsElement18, OtherTEtext18, OtherTEsElement19, OtherTEtext19, \n")
	f.write("				OtherTEsElement20, OtherTEtext20, OtherTEsElement21, OtherTEtext21, \n") 
	f.write("				OtherTEsElement22, OtherTEtext22, \n")
	f.write("				GeneElements, Genesinfo, ExonInfos, ExonElement, \n")
	f.write("				ncRNA_Infos, ncRNAElement, Pseudo_Infos, PseudoElement, \n") 
	f.write("				ChipSEQgraph, \n")
	f.write("				TransposableElement], \n")
	f.write("			'layout': { \n") 
	f.write("				'xaxis' : dict(showgrid=False, showline=False, zeroline=False, ticks='', showticklabels=False, rangemode='tozero'), \n") 
	f.write("				'yaxis' : dict(showgrid=False, showline=False, zeroline=False, ticks='', showticklabels=False, rangemode='tozero'), \n") 
	f.write("				'legend':{'orientation':'h'}, \n") 
	f.write("				'width':TailleGraphique, \n")
	f.write("				'height':725, \n")
	f.write("				'title': SelectionCombobox_myTE[int(valueOccurrences)], \n") 
	f.write("				'render_mode':'webgl',  \n")
	f.write("				'plot_bgcolor':'rgba(255,255,255,1)', \n") 
	f.write("				'margin' : dict(l=10, r=10, t=50, b=10), \n")
	f.write("				#'showlegend' : False \n")
	f.write("			},  \n")
	f.write("		}  \n")
	f.write("		return fig \n\n")
	
	f.write("	else : \n") 
	f.write("		fig = {  \n")
	f.write("			'data': [], \n") 
	f.write("			'layout': { \n") 
	f.write("				'xaxis' : dict(showgrid=False, showline=False, zeroline=False, ticks='', showticklabels=False, rangemode='tozero'), \n") 
	f.write("				'yaxis' : dict(showgrid=False, showline=False, zeroline=False, ticks='', showticklabels=False, rangemode='tozero'), \n") 
	f.write("				'legend':{'orientation':'h'},  \n")
	f.write("				'width':1000, \n")
	f.write("				'height':725, \n")
	f.write("				'title': 'No TE Occurrences Chosen Yet!', \n") 
	f.write("				'render_mode':'webgl', \n") 
	f.write("				'plot_bgcolor':'rgba(255,255,255,1)', \n") 
	f.write("				'margin' : dict(l=10, r=10, t=50, b=10, pad=1), \n")
	f.write("				#'showlegend' : False \n")
	f.write("			},  \n")
	f.write("		}  \n")
	f.write("		return fig \n\n\n\n")
		
	f.close()
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Create the graph with the combobox
########################################################################################################################
def GetListeOccurrences(temp) :
	
	f = open(temp, "a")
	
	# prise en compte d'1 ou plusieurs familles de TEs
	f.write("	######################################################################################################################## \n")
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
	f.write("\t\ttailleMax = MaxConsensus * valueSliders[1] / 100 \n\n\n")
	
	
	# bug ici : Columns (3,4) have mixed types. Specify dtype option on import or set low_memory=False.
	# Selection of TE occurrences
	f.write("	######################################################################################################################## \n")
	f.write("\tSelect_myTE = CommonDATA_SelectTEs.dataFrame_MyTE.loc[ (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] >= tailleMin) & (CommonDATA_SelectTEs.dataFrame_MyTE['Size'] <= tailleMax) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] >= valueSliders[2]) & (CommonDATA_SelectTEs.dataFrame_MyTE['Similarity'] <= valueSliders[3]), ['Index', 'Chr ID', 'Start', 'End', 'Sens', 'Similarity', 'TE Family'] ] \n")     
	f.write("\tSelectionIndex_myTE = Select_myTE['Index'].tolist() \n")
	f.write("\tSelectionChr_myTE = Select_myTE['Chr ID'].tolist() \n")
	f.write("\tSelectionPosDeb_myTE = Select_myTE['Start'].tolist() \n")
	f.write("\tSelectionPosFin_myTE = Select_myTE['End'].tolist() \n")
	f.write("\tSelectionSens_myTE = Select_myTE['Sens'].tolist() \n")
	f.write("\tSelectionSim_myTE = Select_myTE['Similarity'].tolist() \n")
	f.write("\tSelection_Family = Select_myTE['TE Family'].tolist() \n")
	f.write("\tSelectionCombobox_myTE = [] \n")
	f.write("\tSelectionCombobox_myTE.append('Choose a TE occurrence') \n")
	f.write("\tfor i in range(0, len(SelectionIndex_myTE), 1) : \n")
	f.write("\t	SelectionCombobox_myTE.append( Selection_Family[i] + '_' + str(SelectionIndex_myTE[i]) + '\t-\t' + SelectionChr_myTE[i] + '\t-\t' + str(SelectionPosDeb_myTE[i]) + ' - ' + str(SelectionPosFin_myTE[i]) + ' (' + SelectionSens_myTE[i] + ')' ) \n\n")  
	
	f.write("\tSelect_myGene = CommonDATA_SelectTEs.dataFrame_MyGene.loc[ (CommonDATA_SelectTEs.dataFrame_MyGene['TE Index'].isin(SelectionIndex_myTE)), ['TE family', 'TE Index', 'TE-Gene Position', 'Gene Name', 'Gene Start', 'Gene End', 'Gene Sens', 'Gene ID', 'Gene Function'] ] \n")
	f.write("\tSelectionGene_TEindex = Select_myGene['TE Index'].tolist() \n")
	f.write("\tSelectionGene_relation = Select_myGene['TE-Gene Position'].tolist() \n")
	f.write("\tSelectionGene_TEfamily = Select_myGene['TE family'].tolist() \n")
	f.write("\tSelectionGene_Name = Select_myGene['Gene Name'].tolist() \n")
	f.write("\tSelectionGene_PosDeb = Select_myGene['Gene Start'].tolist() \n")
	f.write("\tSelectionGene_PosFin = Select_myGene['Gene End'].tolist() \n")
	f.write("\tSelectionGene_Sens = Select_myGene['Gene Sens'].tolist() \n")
	f.write("\tSelectionGene_ID = Select_myGene['Gene ID'].tolist() \n")
	f.write("\tSelectionGene_Function = Select_myGene['Gene Function'].tolist() \n\n")
	
	f.write("\tSelect_myExon = CommonDATA_SelectTEs.dataFrame_MyGeneExon.loc[ (CommonDATA_SelectTEs.dataFrame_MyGeneExon['TE Index'].isin(SelectionIndex_myTE)), ['TE family', 'TE Index', 'Exon Start', 'Exon End'] ] \n")   
	f.write("\tSelectionExon_TEindex = Select_myExon['TE Index'].tolist() \n")  
	f.write("\tSelectionExon_TEfamily = Select_myExon['TE family'].tolist() \n")  
	f.write("\tSelectionExon_PosDeb = Select_myExon['Exon Start'].tolist() \n")  
	f.write("\tSelectionExon_PosFin = Select_myExon['Exon End'].tolist() \n\n") 
	
	f.write("\tSelect_OtherTEs = CommonDATA_SelectTEs.dataFrame_MyOtherTEs.loc[ (CommonDATA_SelectTEs.dataFrame_MyOtherTEs['TE Index'].isin(SelectionIndex_myTE)), ['TE family', 'TE Index', 'Start', 'End', 'Sens', 'TE Family', 'TE group'] ] \n") 
	f.write("\tSelectionOtherTEs_TEindex = Select_OtherTEs['TE Index'].tolist() \n") 
	f.write("\tSelectionOtherTEs_TEfamily = Select_OtherTEs['TE family'].tolist() \n") 
	f.write("\tSelectionOtherTEs_PosDeb = Select_OtherTEs['Start'].tolist() \n") 
	f.write("\tSelectionOtherTEs_PosFin = Select_OtherTEs['End'].tolist() \n") 
	f.write("\tSelectionOtherTEs_Sens = Select_OtherTEs['Sens'].tolist() \n") 
	f.write("\tSelectionOtherTEs_Family = Select_OtherTEs['TE Family'].tolist() \n") 
	f.write("\tSelectionOtherTEs_Group = Select_OtherTEs['TE group'].tolist() \n\n") 
	
	f.write("\tSelect_ncRNAs = CommonDATA_SelectTEs.dataFrame_MyNcRNA.loc[ (CommonDATA_SelectTEs.dataFrame_MyNcRNA['TE Index'].isin(SelectionIndex_myTE)), ['TE family', 'TE Index', 'Start', 'End', 'Sens', 'Type', 'ID'] ] \n") 
	f.write("\tSelection_ncRNAs_TEindex = Select_ncRNAs['TE Index'].tolist() \n") 
	f.write("\tSelection_ncRNAs_TEfamily = Select_ncRNAs['TE family'].tolist() \n") 
	f.write("\tSelection_ncRNAs_PosDeb = Select_ncRNAs['Start'].tolist() \n") 
	f.write("\tSelection_ncRNAs_PosFin = Select_ncRNAs['End'].tolist() \n") 
	f.write("\tSelection_ncRNAs_Sens = Select_ncRNAs['Sens'].tolist() \n") 
	f.write("\tSelection_ncRNAs_Type = Select_ncRNAs['Type'].tolist() \n") 
	f.write("\tSelection_ncRNAs_ID = Select_ncRNAs['ID'].tolist() \n\n") 
	
	f.write("\tSelect_Pseudos = CommonDATA_SelectTEs.dataFrame_MyPseudo.loc[ (CommonDATA_SelectTEs.dataFrame_MyPseudo['TE Index'].isin(SelectionIndex_myTE)), ['TE family', 'TE Index', 'Start', 'End', 'Sens', 'ID', 'Pseudo Name'] ] \n") 
	f.write("\tSelectionPseudos_TEindex = Select_Pseudos['TE Index'].tolist() \n") 
	f.write("\tSelectionPseudos_TEfamily = Select_Pseudos['TE family'].tolist() \n") 
	f.write("\tSelectionPseudos_PosDeb = Select_Pseudos['Start'].tolist() \n") 
	f.write("\tSelectionPseudos_PosFin = Select_Pseudos['End'].tolist() \n") 
	f.write("\tSelectionPseudos_Sens = Select_Pseudos['Sens'].tolist() \n") 
	f.write("\tSelectionPseudos_ID = Select_Pseudos['ID'].tolist() \n") 
	f.write("\tSelectionPseudos_Name = Select_Pseudos['Pseudo Name'].tolist() \n\n")
		
	f.write("\t\n\n\n")
	
	f.close()
	
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Create the graph with the combobox
########################################################################################################################
def CreateCallBack_Environnemnt(temp, numberTE, pathVisualNEW) :

	f = open(temp, "a")
	f.write("######################################################################################################################## \n")
	f.write("# Callbacks for the TE Environment \n")
	f.write("@app.callback( \n")
	f.write("\tOutput('Onglet8_UCSC', 'children'), \n")
	f.write("\t[Input('memory', 'data')]\n")
	f.write(")\n\n")

	f.write("def updateEnvironmentTE(valueSliders) : \n\n")
	f.write("	global SelectionIndex_myTE \n")
	f.write("	global SelectionChr_myTE \n")
	f.write("	global SelectionPosDeb_myTE \n")
	f.write("	global SelectionPosFin_myTE \n")
	f.write("	global SelectionSens_myTE \n")
	f.write("	global SelectionSim_myTE \n")
	f.write("	global Selection_Family \n")
	f.write("	global SelectionCombobox_myTE \n\n")
	
	f.write("	global SelectionGene_TEindex \n")
	f.write("	global SelectionGene_relation \n")
	f.write("	global SelectionGene_TEfamily \n")
	f.write("	global SelectionGene_Name \n")
	f.write("	global SelectionGene_PosDeb \n")
	f.write("	global SelectionGene_PosFin \n")
	f.write("	global SelectionGene_Sens \n")
	f.write("	global SelectionGene_ID \n")
	f.write("	global SelectionGene_Function \n\n")
	
	f.write("	global SelectionExon_TEindex \n")
	f.write("	global SelectionExon_TEfamily \n")
	f.write("	global SelectionExon_PosDeb \n")
	f.write("	global SelectionExon_PosFin \n\n") 
	
	f.write("	global Select_OtherTEs \n")
	f.write("	global SelectionOtherTEs_TEindex \n")
	f.write("	global SelectionOtherTEs_TEfamily \n")
	f.write("	global SelectionOtherTEs_PosDeb \n")
	f.write("	global SelectionOtherTEs_PosFin \n")
	f.write("	global SelectionOtherTEs_Sens \n")
	f.write("	global SelectionOtherTEs_Family \n")
	f.write("	global SelectionOtherTEs_Group \n\n")  
		
	f.write("	global Select_ncRNAs \n")
	f.write("	global Selection_ncRNAs_TEindex \n") 
	f.write("	global Selection_ncRNAs_TEfamily \n")
	f.write("	global Selection_ncRNAs_PosDeb \n")
	f.write("	global Selection_ncRNAs_PosFin \n")
	f.write("	global Selection_ncRNAs_Sens \n")
	f.write("	global Selection_ncRNAs_Type \n")
	f.write("	global Selection_ncRNAs_ID \n\n")  
		
	f.write("	global Select_Pseudos \n")
	f.write("	global SelectionPseudos_TEindex \n") 
	f.write("	global SelectionPseudos_TEfamily \n")
	f.write("	global SelectionPseudos_PosDeb \n")
	f.write("	global SelectionPseudos_PosFin \n")
	f.write("	global SelectionPseudos_Sens \n")
	f.write("	global SelectionPseudos_ID \n")
	f.write("	global SelectionPseudos_Name \n\n") 
	
	f.close()
	
	
	# Get the information about the list of occurrences
	GetListeOccurrences(temp)
	
	
	f = open(temp, "a")
	f.write("	######################################################################################################################## \n")
	f.write("\tOnglet8_Environment = html.Div([ \n")
	
	f.write("\t	html.Div([ \n")
	f.write("\t		html.Div([ \n")
	f.write("\t			dcc.RadioItems( \n")
	f.write("\t				id='Choix_graphique', \n")
	f.write("\t				options=[ \n")
	f.write("\t					{'label': 'Linear scale', 'value': 'Linear'}, \n")
	f.write("\t					{'label': 'Square root scale', 'value': 'Logarithmic'}, \n")
	f.write("\t				], \n")
	f.write("\t				value='Linear', \n")
	f.write("\t				labelStyle={'display': 'inline-block'}, \n")
	f.write("\t			), \n")  
	f.write("\t		], style={'width': '99%', 'display': 'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n") 
	
	f.write("\t		# combolist \n")
	f.write("\t		dcc.Dropdown(\n")
	f.write("\t			id='Choix_TE_occurrences', \n")
	f.write("\t			options=[{'label':SelectionCombobox_myTE[i], 'value':i} for i in range(0, len(SelectionCombobox_myTE), 1)], \n")
	
	f.write("\t			value = '0', style={}, \n")
	f.write("\t			clearable=False, \n")
	f.write("\t		), \n\n")
	
	f.write("\t	], style={'width': '99%', 'display': 'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n")
	
	f.write("\t	html.Div([ \n")
	f.write("\t		dcc.Graph(\n")
	f.write("\t			id = 'UCSC_like',\n")
	f.write("\t			figure={ \n")
	f.write("\t				'data': [], \n")
	f.write("\t				'layout': { }, \n")
	f.write("\t			}, \n")
	f.write("\t			style = {'overflowX': 'scroll', 'overflowY': 'scroll', 'height': 750}\n")
	f.write("\t		), \n")
	f.write("\t		html.Div(id='Onglet8_FigTEEnvironment'), \n")
	f.write("\t	], style={'width': '99.5%', 'display': 'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n")
	
	f.write("\t	html.Div([ \n")
	f.write("\t		# radio_items \n")
	f.write("\t		html.Div(children='ChipSeq Tissue : '), \n")
	f.write("\t		dcc.RadioItems(  \n")
	f.write("\t			id='Choix_TFBS_Tissue', \n") 
	f.write("\t			options=[ {'label': 'Tissue, Nothing Yet', 'value': 'NULL'}, ], \n") 
	f.write("\t			value='NULL', \n") 
	f.write("\t			labelStyle={'display': 'inline-block'}, \n") 
	f.write("\t		), \n\n") 
				
	f.write("\t		html.Div(children='ChipSeq Organ : '), \n")
	f.write("\t		dcc.RadioItems( \n") 
	f.write("\t			id='Choix_TFBS_Organ', \n") 
	f.write("\t			options=[ {'label': 'Organ, Nothing Yet', 'value': 'NULL'}, ], \n") 
	f.write("\t			value='NULL', \n") 
	f.write("\t			labelStyle={'display': 'inline-block'}, \n") 
	f.write("\t		), \n\n")
				
	f.write("\t	], style={'width': '99%', 'display': 'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n") 
	
	f.write("\t], style={'width': '100%', 'display': 'inline-block', 'backgroundColor':'rgb(245, 245, 255)', 'padding':'5px 5px'} ), \n\n")
	
	
	f.write("\treturn Onglet8_Environment \n\n\n\n")
	f.close()
	
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Create the layout  that contains everything
########################################################################################################################
def Create_layout(temp):
	
	f = open(temp, "a")
	# cree le layout qui va tout contenir
	f.write("########################################################################################################################\n")
	f.write("# Creation du Layout pour dash\n\n")
	f.write("TEEnvironment_layout = html.Div([ \n")
	f.write("	html.Div(id='Onglet8_UCSC'), \n")
	f.write("], style={'width': '100%', 'display': 'inline-block', 'backgroundColor': 'rgb(245, 245, 255)'} )\n")
	f.write("\n\n\n\n")
	f.close()
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Create the TEEnvironment function
########################################################################################################################
def TEEnvironment(pathVisual, nbSeq_Assemble, numberTE):
	
	# Ajout des librairies python pour le serveur
	temp = pathVisual + '/Functions/TEEnvironment.py'
	f = open(temp, "w")

	f.write("#!/usr/bin/env python3\n")
	f.write("# -*- coding: utf-8 -*-\n")
	f.write("import os \n")
	f.write("import sys \n")
	f.write("import numbers \n")
	f.write("from math import * \n")
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
	f.write("# Data that does not change with the sliders or global variable \n\n")
	f.write("SelectionIndex_myTE = [] \n")
	f.write("SelectionChr_myTE = [] \n")
	f.write("SelectionPosDeb_myTE = [] \n")
	f.write("SelectionPosFin_myTE = [] \n")
	f.write("SelectionSens_myTE = [] \n")
	f.write("SelectionSim_myTE = [] \n")
	f.write("Selection_Family = [] \n")
	f.write("SelectionCombobox_myTE = [] \n\n")
	
	f.write("SelectionExon_TEindex = [] \n") 
	f.write("SelectionExon_TEfamily = [] \n") 
	f.write("SelectionExon_PosDeb = [] \n") 
	f.write("SelectionExon_PosFin = [] \n\n") 
	
	f.write("SelectionGene_TEindex = [] \n")
	f.write("SelectionGene_relation = [] \n")
	f.write("SelectionGene_TEfamily = [] \n")
	f.write("SelectionGene_Name = [] \n")
	f.write("SelectionGene_PosDeb = [] \n")
	f.write("SelectionGene_PosFin = [] \n")
	f.write("SelectionGene_Sens = [] \n")
	f.write("SelectionGene_ID = [] \n")
	f.write("SelectionGene_Function = [] \n\n")
	
	f.write("Select_OtherTEs = [] \n")
	f.write("SelectionOtherTEs_TEindex = [] \n")
	f.write("SelectionOtherTEs_TEfamily = [] \n")
	f.write("SelectionOtherTEs_PosDeb = [] \n")
	f.write("SelectionOtherTEs_PosFin = [] \n")
	f.write("SelectionOtherTEs_Sens = [] \n")
	f.write("SelectionOtherTEs_Family = [] \n")
	f.write("SelectionOtherTEs_Group = [] \n\n")  
		
	f.write("Select_ncRNAs = [] \n")
	f.write("Selection_ncRNAs_TEindex = [] \n") 
	f.write("Selection_ncRNAs_TEfamily = [] \n")
	f.write("Selection_ncRNAs_PosDeb = [] \n")
	f.write("Selection_ncRNAs_PosFin = [] \n")
	f.write("Selection_ncRNAs_Sens = [] \n")
	f.write("Selection_ncRNAs_Type = [] \n")
	f.write("Selection_ncRNAs_ID = [] \n\n")  
		
	f.write("Select_Pseudos = [] \n")
	f.write("SelectionPseudos_TEindex = [] \n") 
	f.write("SelectionPseudos_TEfamily = [] \n")
	f.write("SelectionPseudos_PosDeb = [] \n")
	f.write("SelectionPseudos_PosFin = [] \n")
	f.write("SelectionPseudos_Sens = [] \n")
	f.write("SelectionPseudos_ID = [] \n")
	f.write("SelectionPseudos_Name = [] \n\n\n") 

	f.close()
	
	
	# Create the layout that contains everything
	Create_layout(temp)
	
	# Create the layout figure
	CreateCallBack_Environnemnt(temp, numberTE, pathVisual)
	CreateCallBack_Slider(temp, numberTE)
