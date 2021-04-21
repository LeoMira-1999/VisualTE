#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import os.path
import base64
import requests, json
import pandas as pd
from . import ReadInfos_CHIPSeq

def online_download(url, saving_path):

    response = requests.get(url, stream=True)
    fileSize = int(response.headers['Content-length'])
    chunkSize = round(fileSize / 500)+1

    internetFile = open(saving_path, 'wb')
    for chunk in response.iter_content(chunk_size=chunkSize):
        internetFile.write(chunk)

def downloadENCODE(GenomeName, pathVisualDATA2) :

    GenomeName = GenomeName.replace(' ', '+')

    print("----START----")
    print(GenomeName)
    print("-"*10)
    premiereListe = ReadInfos_CHIPSeq.TelechargeExperiments(GenomeName)
    print(len(premiereListe))
    print("-"*10)
    listeBed =  []
    for i in range(0, len(premiereListe), 1) :
        ReadInfos_CHIPSeq.DownloadExperimentsDATA(premiereListe[i])
        listeBedTemp = ReadInfos_CHIPSeq.readExperiments(premiereListe[i])
        if len(listeBedTemp) > 0 :
            listeBed.extend(listeBedTemp)

    # Download the complete set of file from ENCODE
    for i in range(0, len(listeBed), 1) :
        print(i+1, ' / ', len(listeBed), '  ', listeBed[i])
        ExtractExperimentInfos(listeBed[i], pathVisualDATA2)

def ExtractExperimentInfos(listeFichier, pathVisualDATA) :

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
		decompressFile = ReadInfos_CHIPSeq.Decompress(fichierAtelecharger, pathVisualDATA, listeFichier)
		# read the file and add the information
		ReadInfos_CHIPSeq.LectureFichier(pathVisualDATA, decompressFile, assemblage, dataset, developmental, tissueGeneral, organ, cellule, gene, target)





def ReadRepeatMasker(fileTE, Repbase, pathVisualDATA):

	# first read the file lines
	file = open(fileTE, "r")
	lignes = file.readlines()
	file.close()

	# list of data structure
	Infos_MyTE = [[]]
	Infos_OtherTE = [[]]
	SequenceID = ''
	dico_FamilleTE = {}



	########################################################################################################################
	previousIDsequence = ''
	if lignes[0].find('There were no repetitive sequences detected') == -1 :

		# do not read  the three first line
		for i in range(0, len(lignes), 1):

			# remove the unnecessary blank spaces
			lignes[i] = lignes[i].rstrip()
			lignes[i] = ' '.join(lignes[i].split())
			decoupe = lignes[i].split(' ')

			if len(decoupe) >= 12 :
				if decoupe[1] != 'perc' and decoupe[1] != 'div.' :

					# get the whole chromosome of data
					if previousIDsequence != decoupe[4] :
						previousIDsequence = decoupe[4]

					# for each line get the different value
					SequenceID = decoupe[4]
					#print(decoupe[1], decoupe[2], decoupe[3], '  ', lignes[i])
					divergence = 100 - round(float(decoupe[1]) + float(decoupe[2]) + float(decoupe[3]), 2)
					posDEB = decoupe[5]
					posFIN = decoupe[6]
					orientation = decoupe[8]
					if orientation == 'C' :
						orientation = '-'
					nomTE = decoupe[9]
					posDEBinRepeat = decoupe[11]
					posDEBinRepeat = posDEBinRepeat.replace('(', '')
					posDEBinRepeat = posDEBinRepeat.replace(')', '')
					posFINinRepeat = decoupe[12]
					posFINinRepeat = posFINinRepeat.replace('(', '')
					posFINinRepeat = posFINinRepeat.replace(')', '')
					size = int(posFIN) - int(posDEB)

					# assign value to data structure
					dicoType_other = ''
					if nomTE in Repbase:
						dicoType_other = Repbase[nomTE]
					else:
						dicoType_other = 'Unclassified TE'
					tList = [SequenceID, posDEB, posFIN, size, orientation, divergence, posDEBinRepeat, posFINinRepeat, nomTE, dicoType_other ]
					Infos_OtherTE.append(tList)

					# dictionnary of TE families
					if nomTE in dico_FamilleTE.keys():
						print('', end='')
					else :
						dico_FamilleTE[nomTE] = dicoType_other

	list2 = [x for x in Infos_OtherTE if x != []]
	dataFrame_OtherTE = pd.DataFrame(list2, columns=['Chr ID', 'Start', 'End', 'Size', 'Sens', 'Similarity', 'Consensus Start', 'Consensus End', 'TE Family', 'TE group'] )
	tempFile = pathVisualDATA + '/DATA_AllTEs.txt'
	dataFrame_OtherTE.to_csv(tempFile, index = False) # relative position





	########################################################################################################################
	# print all TE families

	dataFrame_ListTE = pd.DataFrame(dico_FamilleTE.items(), columns=['TE family', 'TE group'] )
	ListeTEfichier = pathVisualDATA + '/DATA_List_TE_families.txt'
	dataFrame_ListTE.to_csv(ListeTEfichier, index = False) # relative position





	########################################################################################################################
	# Create a dataframe for general result in dash
	ListeObject = ["DNA Transposon", "EnSpm/CACTA", "Merlin", "MuDR Transposon", "Tc1/Mariner", "Crypton", "Helitron", "Polinton", "BEL", "Copia", "DIRS", "ERV", "Gypsy", "LTR Retrotransposon", "CR1", "L1", "Non-LTR retrotransposon", "R2", "RTE", "SINE", "(Micro)Satelitte", "Unclassified TE"]
	totalHit = 0
	totalSize = 0
	previous = ''
	nbHit_Type = []
	size_Type = []
	data_For_Dash = [[]]
	for x in range(0, len(ListeObject), 1) :
		nbHit_Type.append(0)
		size_Type.append(0)

	for i in range(1, len(Infos_OtherTE), 1) :

		if Infos_OtherTE[i][0] != previous :
			if previous != '' :
				for j in range(0, len(ListeObject), 1) :
					tt = [previous, ListeObject[j], nbHit_Type[j], size_Type[j]]
					data_For_Dash.append(tt)
				tt = [previous, 'All TEs', totalHit, totalSize]
				data_For_Dash.append(tt)

			totalHit = 0
			totalSize = 0
			previous = Infos_OtherTE[i][0]
			for x in range(0, len(ListeObject), 1) :
				nbHit_Type[x] = 0
				size_Type[x] = 0

		for j in range(0, len(ListeObject), 1) :
			if ListeObject[j] == Infos_OtherTE[i][9] :
				nbHit_Type[j] += 1
				totalHit += 1
				size_Type[j] += Infos_OtherTE[i][3]
				totalSize += Infos_OtherTE[i][3]
				break

	for j in range(0, len(ListeObject), 1) :
		tt = [previous, ListeObject[j], nbHit_Type[j], size_Type[j]]
		data_For_Dash.append(tt)
	tt = [previous, 'All TEs', totalHit, totalSize]
	data_For_Dash.append(tt)
	list1 = [x for x in data_For_Dash if x != []]
	dataFrame_For_Dash = pd.DataFrame(list1, columns = ['Chr ID', 'Type TEs', 'Nb Hit', 'Total Size'])
	tempFile = pathVisualDATA + '/DATA_TE_forDash.txt'
	dataFrame_For_Dash.to_csv(tempFile, index = False) # relative position
	os.remove(fileTE)
