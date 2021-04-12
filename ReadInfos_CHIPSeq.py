#!/usr/bin/python3
import os
import os.path
import sys
import requests, json
import gzip
import pandas as pd
import shutil
import urllib.request
import ftplib
import time
from . import Interface_SettingVariables



########################################################################################################################
###	Transform the ChipSEQ data in faster data for the extraction 
########################################################################################################################
def TransformChipSEQ(pathVisualDATA, pathVisualDATA2, root, progressTask, textProcess, nbLigneText, insertionText) :
	
	textProcess.insert(insertionText, '\tTransformation of ChipSEQ files in chromosome ChipSEQ files ...\n')
	nbLigneText += 1
	insertionText = str(nbLigneText) + '.0'
	root.update()
	print('\tTransformation of ChipSEQ files')
	
	CompteFichier = 0
	for nomFichier in os.listdir(pathVisualDATA2):
		if(os.path.isdir(nomFichier) != True):
			CompteFichier += 1
			
	# Create a dictionnary for the CHipSEQ
	dicoChipSEQ = {}
	cle = "All\tTissue\tAll"
	dicoChipSEQ[cle] = 0
	cle = "All\tOrgan\tAll"
	dicoChipSEQ[cle] = 0
	
	progressTask["value"] = 0
	progressTask["maximum"] = CompteFichier
	progressTask.start()
	
	dictionnaire_ficher = {}
	recompte = 0
	for nomFichier in os.listdir(pathVisualDATA2):
		if(os.path.isdir(nomFichier) != True):
			
			nomFichier2 = pathVisualDATA2 + '/' + nomFichier
			f = open(nomFichier2, "r")
			lignes = f.readlines()
			f.close()
			decoupe = nomFichier.split('_____')
			decoupe[2] = decoupe[2][:-4]
			decoupe[1] = decoupe[1].upper()
			decoupe[2] = decoupe[2].upper()
			# remove the cell word
			if decoupe[1][-4:] == '_CELL' :
				decoupe[1] = decoupe[1][:-4]
			if decoupe[2][-4:] == '_CELL' :
				decoupe[2] = decoupe[2][:-4]
				
			
			recompte += 1
			# Change the progress bar of the interfaces
			if recompte % 100 == 0 and recompte > 0 :
				progressTask.step(100)
				root.update()
			
			for i in range(1, len(lignes), 1) :
				lignes[i] = lignes[i].rstrip()
				coupe = lignes[i].split(',')
				coupe.append(decoupe[1])
				coupe.append(decoupe[2])
				coupe.append(decoupe[0])
					
				indice = round(int(coupe[1]) / 50000000)
				if coupe[0] in dictionnaire_ficher.keys() :
					if dictionnaire_ficher[coupe[0]] < indice :
						dictionnaire_ficher[coupe[0]] = indice
				else :
					dictionnaire_ficher[coupe[0]] = indice
					
				fname = pathVisualDATA2 + '/' + coupe[0] + "___part" + str(indice) + ".txt"
				if os.path.isfile(fname) :
					out_file = open(fname, 'a')
					out_file.write(coupe[0])
					for i in range(1, len(coupe), 1) :
						out_file.write('\t' + coupe[i])
					out_file.write('\n')
					out_file.close()
				else : 
					out_file = open(fname, 'w')
					out_file.write(coupe[0])
					for i in range(1, len(coupe), 1) :
						out_file.write('\t' + coupe[i])
					out_file.write('\n')
					out_file.close()
					
				# Fill the dictionnary for the CHipSEQ
				decoupeTissue = decoupe[1].split('__')
				for i in range(0, len(decoupeTissue), 1) :
					cle = coupe[0] + "\tTissue\t" + decoupeTissue[i]
					if cle in dicoChipSEQ.keys():
						dicoChipSEQ[cle] += 1
					else :
						dicoChipSEQ[cle] = 1
					cle = "All\tTissue\t" + decoupeTissue[i]
					if cle in dicoChipSEQ.keys():
						dicoChipSEQ[cle] += 1
					else :
						dicoChipSEQ[cle] = 1
					cle = coupe[0] + "\tTissue\tAll"
					if cle in dicoChipSEQ.keys():
						dicoChipSEQ[cle] += 1
					else :
						dicoChipSEQ[cle] = 1
					cle = "All\tTissue\tAll"
					dicoChipSEQ[cle] += 1
				decoupeOrgan  = decoupe[2].split('__')
				for i in range(0, len(decoupeOrgan), 1) :
					cle = coupe[0] + "\tOrgan\t" + decoupeOrgan[i]
					if cle in dicoChipSEQ.keys():
						dicoChipSEQ[cle] += 1
					else :
						dicoChipSEQ[cle] = 1
					cle = coupe[0] + "\tOrgan\tAll"
					if cle in dicoChipSEQ.keys():
						dicoChipSEQ[cle] += 1
					else :
						dicoChipSEQ[cle] = 1
					cle = "All\tOrgan\t" + decoupeOrgan[i]
					if cle in dicoChipSEQ.keys():
						dicoChipSEQ[cle] += 1
					else :
						dicoChipSEQ[cle] = 1
					cle = "All\tOrgan\tAll"
					dicoChipSEQ[cle] += 1
					
			os.remove(nomFichier2) 
			print('\t\t', recompte, 'ChipSEQ files transformed in', CompteFichier, 'total files')
	
	
	
	########################################################################################################################
	# Create the first version of the table of CHipSEQ
	dicoLigne = {}
	dicoColonne = {}
	for x in dicoChipSEQ :
		coupe = x.split('\t')
		dicoColonne[coupe[0]] = 1
		cle = coupe[1] + '\t' + coupe[2]
		dicoLigne[cle] = 1
		
	temp = pathVisualDATA + '/TableChipSeq.txt'
	f = open(temp, "a")
	f.write(' \t \t')
	for x in dicoColonne :
		f.write(x + '\t')
	f.write('\n')
	for y in dicoLigne :
		f.write(y +  '\t')
		for x in dicoColonne :
			cle = x + '\t' + y
			if cle in dicoChipSEQ.keys():
				f.write(str(dicoChipSEQ[cle]) + '\t')
			else :
				f.write('0' + '\t')
		f.write('\n')
	f.write('\n')
	f.close()
	
	
	
	# Here I will fill the dictionnary for the CommonData files
	Interface_SettingVariables.dictionary_organ = {}
	Interface_SettingVariables.dictionary_tissue = {}
	for y in dicoLigne :
		coupe = y.split('\t')
		if coupe[0] == 'Tissue' :
			Interface_SettingVariables.dictionary_tissue[coupe[1]] = 1
		else : 
			Interface_SettingVariables.dictionary_organ[coupe[1]] = 1
		
		
		
	
	
	########################################################################################################################
	# transform ChipSEQ files into dataframe and Merge them into one file
	CompteFichier = 0
	for nomFichier in os.listdir(pathVisualDATA2):
		if(os.path.isdir(nomFichier) != True) :
			CompteFichier += 1
	progressTask["value"] = 0
	progressTask["maximum"] = CompteFichier
	progressTask.start()
	tempString = '\t\tTransform ' + str(CompteFichier) + ' ChipSEQ files into dataFrame'
	print(tempString)
	tempString = tempString + '\n'
	textProcess.insert(insertionText, tempString)
	nbLigneText += 1
	insertionText = str(nbLigneText) + '.0'
	root.update()
	
	recompte = 0
	for nomFichier in os.listdir(pathVisualDATA2):
		if(os.path.isdir(nomFichier) != True) :
			nomFichier2 = pathVisualDATA2 + '/' + nomFichier
			f = open(nomFichier2, "r")
			lignes = f.readlines()
			f.close()
			
			fichierBED = nomFichier2 + '.bed'
			futurDataframe = []
			for x in range(0, len(lignes), 1) :
				lignes[x] = lignes[x].rstrip()
				coupe = lignes[x].split('\t')
				futurDataframe.append(coupe)
			dataFrame_For_Dash = pd.DataFrame(futurDataframe, columns = ['Chr ID', 'Start', 'End', 'Orientation', 'Score', 'Gene', 'Type', 'Tissue', 'Organ', 'ChipSeq Name'])
			dataFrame_For_Dash.Start = pd.to_numeric(dataFrame_For_Dash.Start, errors='coerce')
			dataFrame_For_Dash.End = pd.to_numeric(dataFrame_For_Dash.End, errors='coerce')
			sortedDF = dataFrame_For_Dash.sort_values(by=['Start', 'End'], ascending=True) 
			sortedDF.to_csv(fichierBED, index = False) # relative position
			
			recompte += 1
			# Change the progress bar of the interfaces
			if recompte % 100 == 0 and recompte > 0 :
				progressTask.step(100)
				root.update()
			
			os.remove(nomFichier2)
	
	tempString = '\t\tMerge ' + str(CompteFichier) + ' ChipSEQ files into dataFrame'
	print(tempString)
	tempString = tempString + '\n'
	textProcess.insert(insertionText, tempString)
	nbLigneText += 1
	insertionText = str(nbLigneText) + '.0'
	root.update()
	for x in dictionnaire_ficher :
		for y in range(0, dictionnaire_ficher[x]+1, 1) :
			nomAtrouver = x + "___part" + str(y) + ".txt.bed"
			for nomFichier in os.listdir(pathVisualDATA2):
				if(os.path.isdir(nomFichier) != True) :
					#print(nomAtrouver, ' <> ', nomFichier)
					if nomAtrouver == nomFichier :
						nomFichier2 = pathVisualDATA2 + '/' + nomFichier
						f = open(nomFichier2, "r")
						lignes = f.readlines()
						f.close()
						mergeFichier = pathVisualDATA2 + '/' + x + '.bed'
						f = open(mergeFichier, "a")
						start = 1
						if y == 0 :
							start = 0
						for i in range(start, len(lignes), 1) :
							f.write(lignes[i])
						f.close()
						os.remove(nomFichier2)



########################################################################################################################
###	Download the first list of all ChipSeq Experiments in genome 
########################################################################################################################
def TelechargeExperiments(genome) :
	
	# Force return from the server in JSON format
	headers = {'accept': 'application/json'}
	# This searches the ENCODE database for the phrase "human"
	url = 'https://www.encodeproject.org/search/?type=Experiment&replicates.library.biosample.donor.organism.scientific_name=' + genome + '&assay_title=TF+ChIP-seq&type=Replicate&status!=deleted&status!=revoked&status!=replaced&status=released&format=json&limit=all'  
	#GET the search result
	response = requests.get(url)
	
	# Extract the JSON response as a python dictionary
	search_results = response.json()
	premiereListe = json.dumps(search_results, indent=8)
	
	# Extract the list of experiments
	secondListe = []
	stringExperiment = "\"@id\": \"/experiments/ENC"
	decoupe = premiereListe.split("\n")
	for i in range(0, len(decoupe), 1) :
		if decoupe[i].find(stringExperiment) != -1 :
			recoupe = decoupe[i].split('/')
			secondListe.append(recoupe[len(recoupe)-2])
	
	return secondListe



########################################################################################################################
###	Download the Experiments information
########################################################################################################################
def DownloadExperimentsDATA(experimentName):

	url = 'https://www.encodeproject.org/experiments/' + experimentName + '/?format=json'
	response = requests.get(url)
	# Extract the JSON response as a python dictionary
	search_results = response.json()
	jsondata = json.dumps(search_results, indent=8)
	
	decoupe = jsondata.split("\n")
	filename = experimentName + '.txt'
	out_file = open(filename, 'w')
	for i in range(0, len(decoupe), 1) :
		out_file.write(decoupe[i] + '\n')
	out_file.close()





########################################################################################################################
###	READ the Experiments information
########################################################################################################################
def readExperiments(experimentName) : 
	
	filename = experimentName + '.txt'
	# memorize lines from file
	f = open(filename, "r")
	lignes = f.readlines()
	f.close()
	
	for i in range(0, len(lignes), 1) :
		lignes[i] = lignes[i].rstrip()
	
	listeBed = []
	for i in range(0, len(lignes)-2, 1) :
		if lignes[i] == "                {" and lignes[i-1] == "                }," and lignes[i+1].find('accession') != -1 :
			j = i+1
			data_from_experiment = []
			while lignes[j+1] != "                }," and j+1 < len(lignes)-1 :
				data_from_experiment.append(lignes[j])
				j = j + 1
			filters = 0
			filtre_format = "\"file_format\": \"bed\","
			filtre_format_type = "\"file_format_type\": \"narrowPeak\","
			filtre_output1 = "\"output_type\": \"optimal IDR thresholded peaks\","
			filtre_output2 = "\"output_type\": \"conservative IDR thresholded peaks\","
			filtre_output3 = "\"output_type\": \"conservative IDR peaks\","
			for z in range(0, len(data_from_experiment), 1) :
				if data_from_experiment[z].find(filtre_format) != -1 :
					filters = filters + 1
				if data_from_experiment[z].find(filtre_format_type) != -1 :
					filters = filters + 1
				if data_from_experiment[z].find(filtre_output1) != -1 or data_from_experiment[z].find(filtre_output2) != -1 or data_from_experiment[z].find(filtre_output3) != -1 :
					filters = filters + 1	
			
			if filters >= 3 :
				recoupe = data_from_experiment[0].split('\"')
				listeBed.append(recoupe[len(recoupe)-2])
	
	os.remove(filename) 
	return listeBed
	
	
	
	
	
	
########################################################################################################################
###	Uncompress File
########################################################################################################################
def Decompress(fichierAtelecharger, pathVisualDATA, listeFichier) :
	
	#GET the search result
	response = requests.get(fichierAtelecharger)
	emplacement = pathVisualDATA + listeFichier + '.bed.gz'
	with open(emplacement, 'wb') as f:
		f.write(response.content)
	decompressFile = pathVisualDATA + listeFichier + '.bed'
	
	fichier = open(decompressFile, 'wb')
	f = gzip.GzipFile(emplacement, 'rb')
	file_content = f.read()
	fichier.write(file_content)
	fichier.close()
	os.remove(emplacement)
	
	return decompressFile





####################################################################################################################################
# lecture simple des lignes du fichier
def LectureFichier(pathVisualDATA, fichier, assemblage, dataset, developmental, tissueGeneral, organ, cellule, gene, target):
	
	dict_tissue = {}
	dict_organ = {}
	
	# memorize lines from file
	f = open(fichier, "r")
	lignes = f.readlines()
	f.close()
	
	futurDataframe = [[]]
	for i in range(0, len(lignes), 1) :
		decoupe = lignes[i].split('\t')
		temp = []
		for j in range(0, 5, 1) :
			temp.append(decoupe[j])
		temp.append(gene)
		temp.append(target)
		futurDataframe.append(temp)
	del(futurDataframe[0])
		
		
		
	# create the name of the bed file
	fichierBED = pathVisualDATA
	coupe = fichier.split("/")
	recoupe = coupe[len(coupe)-1].split(".")
	fichierBED = fichierBED + recoupe[0] + '___'
	
	# get the tissue name
	if len(tissueGeneral) > 0 :
		for z in range(0, len(tissueGeneral), 1) :
			tissueGeneral[z] = tissueGeneral[z].replace(' ', '_')
			tissueGeneral[z] = tissueGeneral[z].upper()
			if tissueGeneral[z][-4:] == '_CELL' :
				tissueGeneral[z] = tissueGeneral[z][:-4]
			fichierBED += '__' + tissueGeneral[z]
	else :
		fichierBED += '__' + "UNKNOWN"
		
	# get the organ name
	fichierBED = fichierBED + '___'
	if len(organ) > 0 :
		for z in range(0, len(organ), 1) :
			organ[z] = organ[z].replace(' ', '_')
			organ[z] = organ[z].upper()
			if organ[z][-4:] == '_CELL' :
				organ[z] = organ[z][:-4]
			fichierBED += '__' + organ[z]
	else :
		fichierBED += '__' + "UNKNOWN"
		
	fichierBED = fichierBED + '.bed'
	
	
	
	# ajout du dataframe dans un nouveau fichier ou un ancien
	if os.path.exists(fichierBED) :
		dataFrame_temp = pd.read_csv(fichierBED)
		A = dataFrame_temp['Chr ID'].tolist()
		B = dataFrame_temp['Start'].tolist()
		C = dataFrame_temp['End'].tolist()
		D = dataFrame_temp['Orientation'].tolist()
		E = dataFrame_temp['Score'].tolist()
		J = dataFrame_temp['Gene'].tolist()
		K = dataFrame_temp['Target'].tolist()
		for i in range(0, len(A), 1) :
			B[i] = round(B[i])
			C[i] = round(C[i])
			temp = [A[i], B[i], C[i], D[i], E[i], H[i], I[i], J[i], K[i]]
			futurDataframe.append(temp)
	dataFrame_For_Dash = pd.DataFrame(futurDataframe, columns = ['Chr ID', 'Start', 'End', 'Orientation', 'Score', 'Gene', 'Target'])
	dataFrame_For_Dash.to_csv(fichierBED, index = False) # relative position
	os.remove(fichier)
	
	
	
	
	
########################################################################################################################
###	Extract the information about the bed file
########################################################################################################################
def ExtractExperimentInfos(listeFichier, pathVisualDATA, progressChipSeq, newWindow, chunkSize) :
	
	url = 'https://www.encodeproject.org/files/'+ listeFichier + '/?format=json'
	# GET the search result
	response = requests.get(url)
	# Extract the JSON response as a python dictionary
	search_results = response.json()
	jsondata = json.dumps(search_results, indent=8)
		
	dataset = ''
	assemblage = ''
	tissueGeneral = []
	developmental = ''
	organ = []
	cellule = []
	gene = ''
	target = ''
	affirmatif = 0
	ligneTelecharge = '/files/' + listeFichier + '/@@download/'  + listeFichier + '.bed.gz'
	# check if the experiment is a chip-seq and the results have already 'cleaned'
	decoupe = jsondata.split("\n")
	for j in range(0, len(decoupe), 1) :
		if decoupe[j].find(ligneTelecharge) != -1 :
			affirmatif = 1
		if decoupe[j].find('assembly') != -1 :
			if decoupe[j].find('\"') != -1 :
				recoupe = decoupe[j].split("\"")
				assemblage = recoupe[len(recoupe)-2] 
		if decoupe[j].find('dataset') != -1 :
			if decoupe[j].find("\"") != -1 :
				recoupe = decoupe[j].split("\"")
				if recoupe[3].find("/") != -1 :
					coupe = recoupe[3].split('/')
					dataset = coupe[2]
		if decoupe[j].find('developmental_slims') != -1 :
			recoupe = decoupe[j+1].split("\"")
			developmental = recoupe[1]
		if decoupe[j].find('\"genes\": [') != -1 :
			k = j+1
			while decoupe[k].find('label') == -1 and k < len(decoupe)-1:
				k = k + 1
			recoupe = decoupe[k].split("\"")
			gene = recoupe[3]
		if decoupe[j].find('investigated_as') != -1 :
			recoupe = decoupe[j+1].split("\"")
			target = recoupe[1]	
		if decoupe[j].find('system_slims') != -1 :
			k = j+1
			while decoupe[k].find('slims') == -1 and k < len(decoupe)-3:
				if decoupe[k].find('\"') != -1 :
					recoupe = decoupe[k].split("\"")
					if recoupe[1].find("exocrine system") == -1 and recoupe[1].find("endocrine system") == -1 :
						tissueGeneral.append(recoupe[1])
				else :
					if decoupe[k+2].find('\"') != -1 :
						recoupe = decoupe[k+2].split("\"")
						tissueGeneral.append(recoupe[1])
					break
				k += 1
		if decoupe[j].find('organ_slims') != -1 :
			k = j+1
			while decoupe[k].find('slims') == -1 and k < len(decoupe)-1:
				if decoupe[k].find('\"') != -1 :
					recoupe = decoupe[k].split("\"")
					organ.append(recoupe[1])
				else :
					break
				k += 1
		if decoupe[j].find('cell_slims') != -1 :
			k = j+1
			while decoupe[k].find('slims') == -1 and k < len(decoupe)-1:
				if decoupe[k].find('\"') != -1 :
					recoupe = decoupe[k].split("\"")
					cellule.append(recoupe[1])
				else :
					break
				k += 1
			
	if affirmatif ==  1 :			
		fichierAtelecharger = 'https://www.encodeproject.org/files/' + listeFichier + '/@@download/' + listeFichier + '.bed.gz'
		# Get and unzip the file
		decompressFile = Decompress(fichierAtelecharger, pathVisualDATA, listeFichier)
		# read the file and add the information
		LectureFichier(pathVisualDATA, decompressFile, assemblage, dataset, developmental, tissueGeneral, organ, cellule, gene, target)
		
	progressChipSeq.step(1 / chunkSize)
	newWindow.update()



#pathVisualDATA = sys.argv[1]
#pathVisualDATA2 = pathVisualDATA + '/ChipSeq/'
#TransformChipSEQ(pathVisualDATA, pathVisualDATA2)
