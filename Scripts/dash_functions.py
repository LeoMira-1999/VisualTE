#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import os.path
import base64
import requests, json
import pandas as pd
from . import ReadInfos_CHIPSeq
from . import ReadInfos_NCBIAnnotations

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


def ReadGFF(AnnotationFile, pathVisualDATA):

	# general information about genome and chromosome
	maxSize = 0
	oldURL = ''
	idNCBI = ''
	chrNumber = ''
	taxon = ''
	organism = []
	sizeChromosome = []
	listID = []

	# information about the pseudogene
	InfosPseudoGene = [[]]
	InfosPseudoGeneExon = [[]]
	# information about the gene
	InfosGene = [[]]
	InfosGeneExon = [[]]
	# information about the ncRNA
	Infos_ncRNA =[[]]
	# information about regulator motif
	InfosRegulator = [[]]



	# read the annotation file
	file = open(AnnotationFile, "r")
	lignes = file.readlines()
	file.close()

	previous_ncRNA = 0
	finLastObject = 0
	typeLastObject = ''

	for ij in range(0, len(lignes), 1) :


		# here it is not a annotation
		if lignes[ij][0] != '#' :
			Colonne = lignes[ij].split('\t')
			# Split the lignes[ij] is different categories :

			# Here I found the annotation for the chromosome
			if Colonne[2] == 'region' :

				size, tax, chrNumber, idNCBI = ReadInfos_NCBIAnnotations.LireChromosome(Colonne)
				sizeChromosome.append(size)
				listID.append(idNCBI)
				taxon = tax
				if maxSize < size :
					maxSize	= size



			# Here I found a pseudogene, it can contain exons...
			elif Colonne[2] == 'pseudogene' :
				posDEB, posFIN, Orient, ID, Name = ReadInfos_NCBIAnnotations.LirePseudogene(Colonne)
				tList = [chrNumber, idNCBI, posDEB, posFIN, Orient, ID, Name]
				InfosPseudoGene.append(tList)
				typeLastObject = 'pseudogene'
				finLastObject = int(posFIN)


			# Here I found a gene, it can contain exons...
			elif Colonne[2] == 'gene' :
				posDEB, posFIN, orient, typeObj, iDName, geneName, product = ReadInfos_NCBIAnnotations.lireGene(Colonne)
				if typeObj == 'protein_coding' :
					tList = [chrNumber, idNCBI, posDEB, posFIN, orient, typeObj, iDName, geneName, product]
					InfosGene.append(tList)
					typeLastObject = 'gene'
					finLastObject = int(posFIN)
				else :
					tList = [chrNumber, idNCBI, posDEB, posFIN, orient, typeObj, iDName, geneName, product]
					Infos_ncRNA.append(tList)
					typeLastObject = 'ncRNA'
					finLastObject = int(posFIN)


			## Here I found an exon, but it can belongs to many biological kind
			elif Colonne[2] == 'exon' :
				# Here Exon belongs to pseudogene
				if typeLastObject == 'pseudogene' and finLastObject >= int(Colonne[4]) :
					posDEB, posFIN, IDExon = ReadInfos_NCBIAnnotations.LirePseudoExon(Colonne)
					tList = [chrNumber, idNCBI, posDEB, posFIN, IDExon]
					InfosPseudoGeneExon.append(tList)

				if typeLastObject == 'gene' and finLastObject >= int(Colonne[4]) :
					posDEB, posFIN, IDExon = ReadInfos_NCBIAnnotations.LireExon(Colonne)
					tList = [chrNumber, idNCBI, posDEB, posFIN, IDExon]
					InfosGeneExon.append(tList)


			# Here I found a strang ncRNA...
			elif(Colonne[2] == 'lnc_RNA' or Colonne[2] == 'snoRNA' or Colonne[2] == 'snRNA' or Colonne[2] == 'miRNA' or Colonne[2] == 'tRNA'
			  or Colonne[2] == 'rRNA' or Colonne[2] == 'scRNA' or Colonne[2] == 'guide_RNA') :
				if previous_ncRNA < int(Colonne[3]) :
					posDEB, posFIN, iDName, geneName, orient, typeObject, product = ReadInfos_NCBIAnnotations.lireMiscRNA(Colonne)
					tList = [chrNumber, idNCBI, posDEB, posFIN, orient, typeObject, iDName, geneName, product]
					Infos_ncRNA.append(tList)
					typeLastObject = 'ncRNA'
					finLastObject = int(posFIN)
					previous_ncRNA = int(posDEB)


			# Here many useless annotation
			elif(Colonne[2] == 'CDS' or Colonne[2] == 'mRNA' or Colonne[2] == 'cDNA_match' or Colonne[2] == 'match'
			  or Colonne[2] == 'transcript' or Colonne[2] == 'primary_transcript' or Colonne[2] == 'sequence_feature'
			  or Colonne[2] == 'conserved_region' or Colonne[2] == 'sequence_alteration'  or Colonne[2] == 'origin_of_replication'
			  or Colonne[2] == 'C_gene_segment' or Colonne[2] == 'J_gene_segment' or Colonne[2] == 'V_gene_segment' or Colonne[2] == 'D_gene_segment'
			  or Colonne[2] == 'mobile_genetic_element' or Colonne[2] == 'nucleotide_motif') :
				print('',end='')


			# Here found regulator sequence
			elif(Colonne[2] == 'enhancer' or Colonne[2] == 'biological_region' or Colonne[2] == 'protein_binding_site' or Colonne[2] == 'promoter'
			  or Colonne[2] == 'transcriptional_cis_regulatory_region' or Colonne[2] == 'matrix_attachment_site'
			  or Colonne[2] == 'DNAseI_hypersensitive_site' or Colonne[2] == 'locus_control_region' or Colonne[2] == 'TATA_box'
			  or Colonne[2] == 'silencer' or Colonne[2] == 'enhancer_blocking_element' or Colonne[2] == 'response_element' or Colonne[2] == 'CAAT_signal'):
				posDEB, posFIN, Orient, ID, Class, Name, Function = ReadInfos_NCBIAnnotations.lireRegulatory(Colonne)
				tList = [chrNumber, idNCBI, posDEB, posFIN, Orient, ID, Class, Name, Function]
				InfosRegulator.append(tList)


			# Here many useless annotation
			else :
				print('',end='')

		else:
			if lignes[ij].find("Taxonomy") != -1 :
				decoupe = lignes[ij].split(" ")
				oldURL = decoupe[1][:-1]


	########################################################################################################################
	# read the html file with the official name of the genome
	organism = ReadInfos_NCBIAnnotations.LireOfficialName(oldURL)
	nbSeq_Assemble, nameOrganism, InfosOrganism = ReadInfos_NCBIAnnotations.prepareInfosOrganism(organism, sizeChromosome, listID)

	# get the dataframe
	list1 = [x for x in InfosGene if x != []]
	dataFrame_Gene           = pd.DataFrame(list1, columns=['Chr Name', 'Chr ID', 'Start', 'End', 'Sens', 'Type', 'ID', 'Gene Name', 'Function'] )
	list2 = [x for x in InfosGeneExon if x != []]
	dataFrame_GeneExon       = pd.DataFrame(list2, columns=['Chr Name', 'Chr ID', 'Start', 'End', 'geneID'] )
	list3 = [x for x in InfosPseudoGene if x != []]
	dataFrame_PseudoGene     = pd.DataFrame(list3, columns=['Chr Name', 'Chr ID', 'Start', 'End', 'Sens', 'ID', 'Pseudo Name'] )
	list4 = [x for x in InfosPseudoGeneExon if x != []]
	dataFrame_PseudoGeneExon = pd.DataFrame(list4, columns=['Chr Name', 'Chr ID', 'Start', 'End', 'ID'] )
	list5 = [x for x in Infos_ncRNA if x != []]
	dataFrame_ncRNA          = pd.DataFrame(list5, columns=['Chr Name', 'Chr ID', 'Start', 'End', 'Sens', 'Type', 'ID', 'ncRNA Name', 'Function'] )
	list6 = [x for x in InfosRegulator if x != []]
	dataFrame_Regulator      = pd.DataFrame(list6, columns=['Chr Name', 'Chr ID', 'Start', 'End', 'Sens', 'ID', 'Type', 'Regulator Name', 'Function'] )
	list7 = [x for x in InfosOrganism if x != []]
	dataFrame_Organism       = pd.DataFrame(list7, columns=['Name', 'NameID', 'RefSeq', 'Size Mb', 'Size bp', 'GC%', 'nb Protein', 'nb Gene', 'nb Pseudo', 'nb ncRNA'] )

	ReadInfos_NCBIAnnotations.PrepareGenomeFileForDash(pathVisualDATA, AnnotationFile, dataFrame_Organism, dataFrame_Gene, dataFrame_GeneExon, dataFrame_PseudoGene, dataFrame_PseudoGeneExon, dataFrame_ncRNA, dataFrame_Regulator)

	return nbSeq_Assemble, nameOrganism, maxSize, taxon, dataFrame_Gene



def TransformChipSEQ(pathVisualDATA, pathVisualDATA2) :

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
	dictionary_organ = {}
	dictionary_tissue = {}
	for y in dicoLigne :
		coupe = y.split('\t')
		if coupe[0] == 'Tissue' :
			dictionary_tissue[coupe[1]] = 1
		else :
			dictionary_organ[coupe[1]] = 1





	########################################################################################################################
	# transform ChipSEQ files into dataframe and Merge them into one file
	CompteFichier = 0
	for nomFichier in os.listdir(pathVisualDATA2):
		if(os.path.isdir(nomFichier) != True) :
			CompteFichier += 1

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

			os.remove(nomFichier2)

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

	return dictionary_organ, dictionary_tissue





def getListeTE(DATAListTE) :

	dict_dash_TE = []
	ListeCompleteTE = []
	ListeFamilleTE = []
	ListeSuperFamilyTE = []

	# read the annotation file
	file = open(DATAListTE, "r")
	lignes = file.readlines()
	file.close()

	for i in range(1, len(lignes), 1) :
		lignes[i] = lignes[i][:-1]
		decoupe = lignes[i].split(',')
		ListeCompleteTE.append(decoupe[0] + '\t\t' + decoupe[1])
	ListeCompleteTE.sort()
	for i in range(0, len(ListeCompleteTE), 1) :
		decoupe = ListeCompleteTE[i].split('\t\t')
		nbEspace = 20 - len(decoupe[0])
		ListeCompleteTE[i] = decoupe[0] + nbEspace * ' ' + decoupe[1]
		ListeFamilleTE.append(decoupe[0])
		ListeSuperFamilyTE.append(decoupe[1])

	for TE in ListeCompleteTE:
		dict_dash_TE.append({"label":TE,"value":TE})

	return ListeCompleteTE, ListeFamilleTE, ListeSuperFamilyTE, dict_dash_TE
