#!/usr/bin/python3
import os
import sys
import pandas as pd
import urllib.request
import ftplib
from html.parser import HTMLParser





########################################################################################################################
### Create the datafile for Dash
########################################################################################################################
def PrepareGenomeFileForDash(pathVisualDATA, AnnotationFile,
				dataFrame_Organism, dataFrame_Gene, dataFrame_GeneExon, dataFrame_PseudoGene, dataFrame_PseudoGeneExon, dataFrame_ncRNA, dataFrame_Regulator) :  

	tempFile = pathVisualDATA + '/DATA_Organism.txt'
	dataFrame_Organism.to_csv(tempFile, index = False) # relative position
	tempFile = pathVisualDATA + '/DATA_Gene.txt'
	dataFrame_Gene.to_csv(tempFile, index = False) # relative position
	tempFile = pathVisualDATA + '/DATA_GeneExon.txt'
	dataFrame_GeneExon.to_csv(tempFile, index = False) # relative position
	tempFile = pathVisualDATA + '/DATA_Pseudo.txt'
	dataFrame_PseudoGene.to_csv(tempFile, index = False) # relative position
	tempFile = pathVisualDATA + '/DATA_PseudoExon.txt'
	dataFrame_PseudoGeneExon.to_csv(tempFile, index = False) # relative position
	tempFile = pathVisualDATA + '/DATA_ncRNA.txt'
	dataFrame_ncRNA.to_csv(tempFile, index = False) # relative position
	tempFile = pathVisualDATA + '/DATA_Regulator.txt'
	dataFrame_Regulator.to_csv(tempFile, index = False) # relative position
	
	os.remove(AnnotationFile)
	
	
	
	
	
	
	
	
	
	
########################################################################################################################
###	Read chromosome information from 1 file (chromosome)
########################################################################################################################
def LireChromosome(Colonne):
	decoupe = Colonne[8].split(';')	

	taxon = ''
	chrNumber = 'NULL'
	# get the old ID of the sequence
	idNCBI = Colonne[0]
	# get the chromosome size
	sizeChromosome = int(Colonne[4])	
	# get the taxonomic number
	if len(decoupe) > 1 :
		if decoupe[1].find(':') != -1 :
			coupe = decoupe[1].split(':')
			taxon = coupe[1]
	# get the chromosome namea
	if len(decoupe) > 2 :
		if decoupe[2].find('=') != -1 :
			coupe = decoupe[2].split('=')
			chrNumber = coupe[1]

	return sizeChromosome, taxon, chrNumber, idNCBI










########################################################################################################################
###	HTML Parser for the genome name and table of genome information
########################################################################################################################
class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.data = []

	def handle_startendtag(self, tag, attrs):
		self.handle_starttag(tag, attrs)
		self.handle_endtag(tag)
	def handle_starttag(self, tag, attrs):
		tag = 'starttag ' + tag 
		self.data.append(tag)
	def handle_endtag(self, tag):
		tag = 'endtag ' + tag
		self.data.append(tag)
	def handle_data(self, data):
		self.data.append(data)











########################################################################################################################
###	Read organism name
########################################################################################################################
def LireOfficialName(oldURL):
	organism = []

	# https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=10090 	J'ai ca
	# https://www.ncbi.nlm.nih.gov/genome/?term=txid10090[Organism:exp] 	Je veux ca
	decoupe = oldURL.split('=')
	newURL = 'https://www.ncbi.nlm.nih.gov/genome/?term=txid' + decoupe[1] + '[Organism:exp]'
	response = urllib.request.urlopen(newURL)			
	dataURL = str(response.read())

	# parser of the genome information	
	p = MyHTMLParser()
	p.feed(dataURL)

	debTab = 0	
	nbCHR = 0
	tempString = ''
	# now parse the genome information
	for i in range(0, len(p.data), 1):
		# get the name of the genome
		if p.data[i-3] == 'Reference genome: ' and p.data[i-1] == 'starttag a' and debTab == 0:
			p.data[i] = p.data[i].replace('\\xc2', '')
			p.data[i] = p.data[i].replace('\\xa0', ' ')
			organism.append(p.data[i])

		if debTab == 1 :
			p.data[i] = p.data[i].replace('\\n', '')
			p.data[i] = p.data[i].replace('\t', '')
			p.data[i] = p.data[i].replace('  ', '')
			
			# start of the new line on the table excepted the first line
			if( p.data[i-7] == 'starttag tr' and p.data[i-6] == 'starttag td' and p.data[i-5] == 'starttag span' 
			and p.data[i-4] == 'endtag span' and p.data[i-3] == 'endtag td' and p.data[i-2] == 'starttag td' and p.data[i-1] == 'starttag span') :

				organism.append(tempString)

				if p.data[i] == 'endtag span' :				
					tempString = ' ' + '\t'
				else :
					tempString = ''

			# find information of the table
			if p.data[i].find('starttag') == -1 and p.data[i].find('endtag') == -1 :
				tempString += p.data[i] + '\t' 

		# start of the table with infos
		if p.data[i-3] == 'starttag table' and p.data[i-2] == 'starttag thead' and p.data[i] == 'starttag th' :
			debTab = 1
			tempString = ''
		# end to the table
		if debTab == 1 and p.data[i] == 'starttag script' :
			debTab = 0
			organism.append(tempString)
		
	# return a string list with the name of the genome and the characteristics of each chromosome
	return organism










########################################################################################################################
###	Make the list before the dataframeW
########################################################################################################################
def prepareInfosOrganism(organism, sizeChromosome, listID) :
	nbSeq_Assemble = 0
	nameOrganism = organism[0]
	InfosOrganism = [[]]
	for i in range(2, len(organism), 1) :
		decoupe = organism[i].split('\t')
		decoupe[6] = decoupe[6].replace(',', '')
		decoupe[9] = decoupe[9].replace(',', '')
		decoupe[10] = decoupe[10].replace(',', '')
		decoupe[11] = decoupe[11].replace(',', '')
		nom = decoupe[0] + decoupe[1]
		if decoupe[7] == '-' :
			decoupe[7] = 0
		if decoupe[8] == '-' :
			decoupe[8] = 0
		if decoupe[9] == '-' :
			decoupe[9] = 0
		if decoupe[10] == '-' :
			decoupe[10] = 0
		if decoupe[11] == '-' :
			decoupe[11] = 0
		tNCRNA = int(decoupe[7]) + int(decoupe[8]) + int(decoupe[9])

		tailleCHR = 0
		for j in range(0, len(listID), 1) :
			if listID[j] == decoupe[2] :	
				tailleCHR = sizeChromosome[j]
				break

		tList = [ nom, decoupe[2], decoupe[3], float(decoupe[4]), tailleCHR, float(decoupe[5]), int(decoupe[6]), int(decoupe[10]), int(decoupe[11]), tNCRNA ]	
		InfosOrganism.append(tList)
		if len(decoupe[2]) > 3 :
			nbSeq_Assemble += 1

	return nbSeq_Assemble, nameOrganism, InfosOrganism










########################################################################################################################
###	Read the pseudogene annotation
########################################################################################################################
def LirePseudogene(Colonne):
	PosDebPseudo = 0
	PosFinPseudo = 0
	OrientPseudo = '+' 
	PseudoID = 0 
	PseudoName = ''
	decoupe = Colonne[8].split(';')
	
	# get the start position
	PosDebPseudo = Colonne[3]
	# get the end position
	PosFinPseudo = Colonne[4]
	# get the orientation position
	OrientPseudo = Colonne[6]
	# get the IDname
	coupe = decoupe[1].split(':')
	PseudoID = coupe[1]
	if PseudoID.find("MGI") != -1:
		PseudoID = PseudoID[:-4]
	if PseudoID.find("HGNC") != -1:
		PseudoID = PseudoID[:-5]
	# get the pseudogene name
	coupe = decoupe[2].split('=')
	PseudoName = coupe[1]
	
	return PosDebPseudo, PosFinPseudo, OrientPseudo, PseudoID, PseudoName










########################################################################################################################
###	Read Exon from pseudogene annotation
########################################################################################################################
def LirePseudoExon(Colonne):
	PosDebPseudoExon = 0
	PosFinPseudoExon = 0
	PseudoIDExon = 0
	decoupe = Colonne[8].split(';')

	# get the start position
	PosDebPseudoExon = Colonne[3]
	# get the end position
	PosFinPseudoExon = Colonne[4]
	# get the IDname
	coupe = decoupe[2].split(':')
	PseudoIDExon = coupe[1]
	if PseudoIDExon.find("MGI") != -1:
		PseudoIDExon = PseudoID[:-4]
	if PseudoIDExon.find(',Genbank') != -1 :
		recoupe = PseudoIDExon.split(',')
		PseudoIDExon = recoupe[0]
	

	return PosDebPseudoExon, PosFinPseudoExon, PseudoIDExon










########################################################################################################################
###	Read Gene annotation (means DNA transcript)
########################################################################################################################
# lecture de l'annotation gene
def lireGene(Colonne):
	posDEB = 0
	posFIN = 0
	orientation = '+'
	iDName = ''
	geneName = ''
	typeObject = ''
	product = 'UNKNOWN'
	Colonne[8] = Colonne[8][:-1]
	decoupe = Colonne[8].split(';')

	# get the start position
	posDEB = Colonne[3]
	# get the end position
	posFIN = Colonne[4]
	# get the orientation
	orientation = Colonne[6]
	# get the IDname
	coupe = decoupe[1].split(':')
	iDName = coupe[1]
	if iDName.find("MGI") != -1:
		iDName = iDName[:-4]
	if iDName.find(',') != -1 :
		recoupe = iDName.split(',')
		iDName = recoupe[0]

	for i in range(2, len(decoupe), 1) :
		# get the type of the biological objet	
		if decoupe[i].find("gene_biotype") != -1 :
			coupe = decoupe[i].split('=')
			typeObject = coupe[1]
		# get the description of gene product
		if decoupe[i].find("description") != -1 :
			coupe = decoupe[i].split('=')
			product = coupe[1]
		# get the description of gene name
		if decoupe[i].find("Name=") != -1 :
			coupe = decoupe[i].split('=')
			geneName = coupe[1]

	return posDEB, posFIN, orientation, typeObject, iDName, geneName, product










########################################################################################################################
###	Read Exon from gene annotation
########################################################################################################################
def LireExon(Colonne):
	PosDebExon = 0
	PosFinExon = 0
	IDExon = 0
	decoupe = Colonne[8].split(';')

	# get the start position
	PosDebExon = Colonne[3]
	# get the end position
	PosFinExon = Colonne[4]
	# get the IDname
	#temp = ''
	#temp2 = ''
	for i in range(0, len(decoupe), 1) :
		if decoupe[i].find("GeneID") != -1:
			coupe = decoupe[i].split(':')
			IDExon = coupe[1]
			#temp = coupe[1]
			if IDExon.find("GeneID") != -1 :		# pas normal donc prendre le suivant
				IDExon = coupe[2]
				#temp2 = coupe[2]
			break
	if IDExon.find("MGI") != -1:
		IDExon = IDExon[:-4]
	if IDExon.find(',') != -1 :
		recoupe = IDExon.split(',')
		IDExon = recoupe[0]
		
	#if Colonne[8].find("GeneID:219770") != -1 :
	#print(temp, temp2, '  ', PosDebExon, PosFinExon, IDExon)

	return PosDebExon, PosFinExon, IDExon










########################################################################################################################
###	Read miscRNA annotation
########################################################################################################################
def lireMiscRNA(Colonne):
	posDEB = 0
	posFIN = 0
	iDName = ''
	geneName = ''
	orientation = '+'
	typeObject = ''
	product = 'UNKNOWN'
	decoupe = Colonne[8].split(';')

	# get the type of object
	typeObject = Colonne[2]
	# get the start position
	posDEB = Colonne[3]
	# get the end position
	posFIN = Colonne[4]
	# get the orientation
	orientation = Colonne[6]
	# get the IDname
	coupe = decoupe[2].split(':')
	iDName = coupe[1]
	if iDName.find("MGI") != -1:
		iDName = iDName[:-4]
	if iDName.find(',') != -1 :
		recoupe = iDName.split(',')
		iDName = recoupe[0]
	for i in range(2, len(decoupe), 1) :
		# get gene name
		if decoupe[i].find('gene=') != -1 :
			coupe = decoupe[i].split('=')
			geneName = coupe[1]
		# get product name
		if decoupe[i].find('product=') != -1 :
			decoupe[i] = decoupe[i][:-1]
			coupe = decoupe[i].split('=')
			product = coupe[1]

	return posDEB, posFIN, iDName, geneName, orientation, typeObject, product
	









########################################################################################################################
###	Read regulatory element annotation
########################################################################################################################
def lireRegulatory(Colonne):
	PosDeb = 0
	PosFin = 0
	Orient = '+'
	ID = ''
	Class = ''
	Name = ''
	Function = ''
	decoupe = Colonne[8].split(';')

	# get the start position
	PosDeb = Colonne[3]
	# get the end position
	PosFin = Colonne[4]
	# get the orientation 
	Orient = Colonne[6]
	
	# get the class of regulatory motif
	Class = Colonne[0]
	Name = Colonne[0]
	for i in range(0, len(decoupe), 1) :
		# get the IDname
		if decoupe[i].find('Dbxref') != -1 :
			coupe = decoupe[i].split(':')	
			ID = coupe[1]
			if ID.find("MGI") != -1:
				ID = ID[:-4]
		# get function name
		if decoupe[i].find('function=') != -1 :
			coupe = decoupe[i].split('=')
			Function = coupe[1]
		# get gene name
		if decoupe[i].find('standard_name=') != -1 :
			coupe = decoupe[i].split('=')
			Name = coupe[1]

	return PosDeb, PosFin, Orient, ID, Class, Name, Function










########################################################################################################################
###	Read the genome annotations
###	One file contains annotation for all chromosome
########################################################################################################################
def ReadGFF(AnnotationFile, pathVisualDATA, root, progressTask, textProcess, nbLigneText, insertionText):

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
	
	
	
	progressTask["value"] = 0
	progressTask["maximum"] = len(lignes)
	progressTask.start()
	previous_ncRNA = 0
	finLastObject = 0
	typeLastObject = ''
	
	for ij in range(0, len(lignes), 1) :
		
		if ij % 100 == 0 and ij > 0 :
			progressTask.step(100)
			root.update()
		
		# here it is not a annotation
		if lignes[ij][0] != '#' :
			Colonne = lignes[ij].split('\t')
			# Split the lignes[ij] is different categories :

			# Here I found the annotation for the chromosome
			if Colonne[2] == 'region' :

				size, tax, chrNumber, idNCBI = LireChromosome(Colonne)
				sizeChromosome.append(size)
				listID.append(idNCBI)
				taxon = tax
				if maxSize < size :
					maxSize	= size

			

			# Here I found a pseudogene, it can contain exons...
			elif Colonne[2] == 'pseudogene' :	
				posDEB, posFIN, Orient, ID, Name = LirePseudogene(Colonne)
				tList = [chrNumber, idNCBI, posDEB, posFIN, Orient, ID, Name]
				InfosPseudoGene.append(tList)
				typeLastObject = 'pseudogene'
				finLastObject = int(posFIN)


			# Here I found a gene, it can contain exons...
			elif Colonne[2] == 'gene' :
				posDEB, posFIN, orient, typeObj, iDName, geneName, product = lireGene(Colonne)
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
					posDEB, posFIN, IDExon = LirePseudoExon(Colonne)
					tList = [chrNumber, idNCBI, posDEB, posFIN, IDExon]
					InfosPseudoGeneExon.append(tList)

				if typeLastObject == 'gene' and finLastObject >= int(Colonne[4]) :
					posDEB, posFIN, IDExon = LireExon(Colonne)
					tList = [chrNumber, idNCBI, posDEB, posFIN, IDExon]
					InfosGeneExon.append(tList)
					

			# Here I found a strang ncRNA...
			elif(Colonne[2] == 'lnc_RNA' or Colonne[2] == 'snoRNA' or Colonne[2] == 'snRNA' or Colonne[2] == 'miRNA' or Colonne[2] == 'tRNA' 
			  or Colonne[2] == 'rRNA' or Colonne[2] == 'scRNA' or Colonne[2] == 'guide_RNA') :
				if previous_ncRNA < int(Colonne[3]) :
					posDEB, posFIN, iDName, geneName, orient, typeObject, product = lireMiscRNA(Colonne)
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
				posDEB, posFIN, Orient, ID, Class, Name, Function = lireRegulatory(Colonne)
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
	textProcess.insert(insertionText, '\tGet Missing Genome Information from NCBI ...\n')
	nbLigneText += 1
	insertionText = str(nbLigneText) + '.0'
	root.update()
	organism = LireOfficialName(oldURL)
	nbSeq_Assemble, nameOrganism, InfosOrganism = prepareInfosOrganism(organism, sizeChromosome, listID)
	
	
	textProcess.insert(insertionText, '\tWriting Annotation DATA ...\n')
	nbLigneText += 1
	insertionText = str(nbLigneText) + '.0'
	root.update()
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
	
	PrepareGenomeFileForDash(pathVisualDATA, AnnotationFile, dataFrame_Organism, dataFrame_Gene, dataFrame_GeneExon, dataFrame_PseudoGene, dataFrame_PseudoGeneExon, dataFrame_ncRNA, dataFrame_Regulator)     

	return nbSeq_Assemble, nameOrganism, maxSize, taxon, nbLigneText, dataFrame_Gene


