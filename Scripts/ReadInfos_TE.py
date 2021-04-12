#!/usr/bin/python3


########################################################################################################################
###	Read the Repbase database
########################################################################################################################

def LireRepbase(fichier):
	file = open(fichier, "r")
	lignes = file.readlines()
	file.close()

	dico = {}
	for i in range(0, len(lignes), 1):
		lignes[i] = lignes[i].rstrip()
		t = lignes[i].split('\t')
		t[0] = t[0].upper()
		dico[t[0]] = t[2]

	return dico



########################################################################################################################
###	Read the Repbase database and get the group TE
########################################################################################################################

def GetSuperfamily(fichier, TEname):
	file = open(fichier, "r")
	lignes = file.readlines()
	file.close()

	SuperfamilyTE = 'Unclassified TE'
	SequenceConsensus = ''
	for i in range(0, len(lignes), 1):
		lignes[i] = lignes[i].rstrip()
		t = lignes[i].split('\t')
		if(t[0] == TEname):
			SuperfamilyTE = t[2]
			SequenceConsensus = t[3]
			break

	return SuperfamilyTE, SequenceConsensus



