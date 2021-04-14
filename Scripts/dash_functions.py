#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import os.path
import requests, json
from . import ReadInfos_CHIPSeq

def online_download(url, saving_path):

    response = requests.get(url, stream=True)
    fileSize = int(response.headers['Content-length'])
    chunkSize = round(fileSize / 500)+1

    internetFile = open(saving_path, 'wb')
    for chunk in response.iter_content(chunk_size=chunkSize):
        internetFile.write(chunk)

def downloadENCODE(GenomeName, pathVisualDATA) :

    pathVisualDATA2 = pathVisualDATA + '/ChipSeq/'
    if not os.path.exists(pathVisualDATA2):
        os.mkdir(pathVisualDATA2)

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
