#!/usr/bin/python3
import os
import sys
import shutil
import gzip
import urllib.request
import ftplib

# adress for genome annotation
# ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/latest_assembly_versions/GCF_000001405.39_GRCh38.p13/GCF_000001405.39_GRCh38.p13_genomic.gff.gz  
# adress for genome sequence
# ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/latest_assembly_versions/GCF_000001405.39_GRCh38.p13/GCF_000001405.39_GRCh38.p13_genomic.fna.gz  





########################################################################################################################
###	Get the list of genome in this categoriy
########################################################################################################################
def getListeGenome(nomCategory, ftpNCBI, GenomeName):

	listGenomes = []
	trouveGenome = 0

	ftpNCBI.cwd(nomCategory)
	ftpNCBI.dir(listGenomes.append)
	for i in range(0, len(listGenomes), 1):
		decoupe = listGenomes[i].split(' ')
		if decoupe[len(decoupe)-1] == GenomeName :
			trouveGenome = 1

	return listGenomes, trouveGenome





########################################################################################################################
###	Get the genome name file and the file size (for interface)
########################################################################################################################
def RechercheGenomeFTP(ftpNCBI, GenomeName):

	trouveGenome = 0
	listGenomes = []
	ftpAdress = 'ftp.ncbi.nlm.nih.gov/genomes/refseq/'

	# Cherche d'abord chez les mamifere
	listGenomes, trouveGenome = getListeGenome('vertebrate_mammalian', ftpNCBI, GenomeName)
	if trouveGenome == 1 :
		ftpAdress = ftpAdress + 'vertebrate_mammalian/'

	# si non trouve
	# Cherche chez les autres vertebrate
	if trouveGenome == 0:
		ftpNCBI.cwd('..')
		listGenomes, trouveGenome = getListeGenome('vertebrate_other', ftpNCBI, GenomeName)
		if trouveGenome == 1 :
			ftpAdress = ftpAdress + 'vertebrate_other/'
	# si non trouve
	# Cherche chez les plantes
	if trouveGenome == 0:
		ftpNCBI.cwd('..')
		listGenomes, trouveGenome = getListeGenome('plant', ftpNCBI, GenomeName)
		if trouveGenome == 1 :
			ftpAdress = ftpAdress + 'plant/'
	# si non trouve
	# Cherche chez les invertebres
	if trouveGenome == 0:
		ftpNCBI.cwd('..')
		listGenomes, trouveGenome = getListeGenome('invertebrate', ftpNCBI, GenomeName)
		if trouveGenome == 1 :
			ftpAdress = ftpAdress + 'invertebrate/'
	# si non trouve
	# Cherche chez les champignons
	if trouveGenome == 0:
		ftpNCBI.cwd('..')
		listGenomes, trouveGenome = getListeGenome('fungi', ftpNCBI, GenomeName)
		if trouveGenome == 1 :
			ftpAdress = ftpAdress + 'fungi/'
	# si non trouve
	# Cherche chez les protozoaires
	if trouveGenome == 0:
		ftpNCBI.cwd('..')
		listGenomes, trouveGenome = getListeGenome('protozoa', ftpNCBI, GenomeName)
		if trouveGenome == 1 :
			ftpAdress = ftpAdress + 'protozoa/'

	return ftpAdress, trouveGenome





########################################################################################################################
###	Get the genome GFF name file and the file size (for interface)
########################################################################################################################
def findGenomeFile(ftpNCBI, GenomeName):

	FNAaTelecharger = ''
	FNAsize = 0
	GFFaTelecharger = ''
	GFFsize = 0
	trouveGenome = 0
	listGenomes = []
	ftpAdress = ''

	# Recherche le groupe taxonomique qui contient le genome recherche
	ftpAdress, trouveGenome = RechercheGenomeFTP(ftpNCBI, GenomeName)

	# j'ai trouve le genome !
	if trouveGenome == 1:
		listGenomes = []
		ftpNCBI.cwd(GenomeName)
		ftpNCBI.cwd('latest_assembly_versions')
		ftpNCBI.dir(listGenomes.append)
		decoupe = listGenomes[0].split(' ')
		lienUrlGCA = decoupe[len(decoupe)-3]
		ftpNCBI.cwd(lienUrlGCA)
		ftpAdress = ftpAdress + GenomeName + '/latest_assembly_versions/' + lienUrlGCA + '/'
		
		GFFaTelecharger = lienUrlGCA + '_genomic.gff.gz'
		FNAaTelecharger = lienUrlGCA + '_genomic.fna.gz'

		ftpNCBI.dir(listGenomes.append)
		for i in range(0, len(listGenomes), 1):
			listGenomes[i] = listGenomes[i].replace('  ', ' ')
			decoupe = listGenomes[i].split(' ')
			nomFichier = decoupe[len(decoupe)-1]
			if nomFichier == GFFaTelecharger :
				GFFsize = int(decoupe[len(decoupe)-5])
			if nomFichier == FNAaTelecharger :
				FNAsize = int(decoupe[len(decoupe)-5])
	else :
		ftpAdress = "Error ! Your genome name does not exist in NBCI Genbank !!"
		# ici je dois terminer le script python

	# Add the ftp for the full adress
	ftpAdress = 'https://' + ftpAdress
	return FNAaTelecharger, FNAsize, GFFaTelecharger, GFFsize, ftpAdress





########################################################################################################################
###	Run the download file in NCBI script
########################################################################################################################
def lanceTelechargement(GenomeName, DossierTelecharger) :

	FNAaTelecharger = ''
	FNAsize = 0
	ftpAdressFNA = ''
	GFFaTelecharger = ''
	GFFsize = 0
	ftpAdressGFF = ''
	# prepare le nom du genome pour le telechargement
	GenomeName2 = GenomeName.replace(' ', '_')

	# lancement du telechargement du fichier FNA et GFF : genome sequence (1 fichier) + genome annotation (1 fichier)
	ftpNCBI = ftplib.FTP('ftp.ncbi.nlm.nih.gov')
	ftpNCBI.login()
	ftpNCBI.cwd('genomes')
	ftpNCBI.cwd('refseq')
	FNAaTelecharger, FNAsize, GFFaTelecharger, GFFsize, ftpAdress = findGenomeFile(ftpNCBI, GenomeName2)
	ftpNCBI.quit()
	
	return FNAaTelecharger, FNAsize, GFFaTelecharger, GFFsize, ftpAdress
	
	
	
