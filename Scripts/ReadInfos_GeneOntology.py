#!/usr/bin/python3
import sys
import os
import pandas as pd





####################################################################################################################################
###	Read the file lines and Create Dictionary
####################################################################################################################################
def LectureFichier(fichier, pathVisualDATA):

	f = open(fichier, "r")
	lignes = f.readlines()
	f.close()
	return lignes





####################################################################################################################################
###	Memorize the information about the GeneOntology
####################################################################################################################################
def MemorizeGO(NameGO, FunctionGO, TypeGO, IncludedGO, ObsoleteGO, HierarchieGO, ListeGOtemp, TypeGOtemp, FunctionGOtemp, ObsoleteGOtemp, InclusGOtemp, HierarchieGOtemp, nombreGO) :

	for i in range(0, len(ListeGOtemp), 1) :
		NameGO.append(ListeGOtemp[i])
		FunctionGO.append(FunctionGOtemp)
		TypeGO.append(TypeGOtemp)
		ObsoleteGO.append(ObsoleteGOtemp)
		if ObsoleteGOtemp == 0 and len(InclusGOtemp) == 0 :
			InclusGOtemp.append("NULL")
			HierarchieGOtemp.append(0)
		IncludedGO.append(InclusGOtemp)
		HierarchieGO.append(HierarchieGOtemp)
		nombreGO += 1
        
	return NameGO, FunctionGO, TypeGO, IncludedGO, ObsoleteGO, HierarchieGO, nombreGO
		




####################################################################################################################################
###	Split the line of GeneOntology file in different data
####################################################################################################################################
def DecoupeGeneOntologyListe(LigneFile, NameGO, FunctionGO, TypeGO, IncludedGO, ObsoleteGO, HierarchieGO, nombreGO) :

	ObsoleteGOtemp = 0
	FunctionGOtemp = ''
	TypeGOtemp = ''
	ListeGOtemp = []
	InclusGOtemp = []
	HierarchieGOtemp = []

	for i in range(0, len(LigneFile), 1) :
		# New GO initialise the memory variable
		if LigneFile[i][0:6] == '[Term]' :
			NameGO, FunctionGO, TypeGO, IncludedGO, ObsoleteGO, HierarchieGO, nombreGO = MemorizeGO(NameGO, FunctionGO, TypeGO, IncludedGO, ObsoleteGO, HierarchieGO, ListeGOtemp, TypeGOtemp, FunctionGOtemp, ObsoleteGOtemp, InclusGOtemp, HierarchieGOtemp, nombreGO)
			
			ObsoleteGOtemp = 0
			FunctionGOtemp = ''
			TypeGOtemp = ''
			ListeGOtemp = []
			InclusGOtemp = []	
			HierarchieGOtemp = []
						
		# Get the ID of the GO
		if LigneFile[i][0:6] == 'id: GO' :
			coupe = LigneFile[i].split(' ')
			ListeGOtemp.append(coupe[1][:-1])

		# Get the alternative ID of GO
		if LigneFile[i][0:10] == 'alt_id: GO' :
			coupe = LigneFile[i].split(' ')
			ListeGOtemp.append(coupe[1][:-1])

		# Get the obsolete or not for the GO
		if LigneFile[i][0:12] == 'is_obsolete:' :
			ObsoleteGOtemp = 1

		# Get the first step for the GO hierarchy
		if LigneFile[i][0:8] == 'is_a: GO' :
			coupe = LigneFile[i].split(' ')
			InclusGOtemp.append(coupe[1])
			HierarchieGOtemp.append(-1)

		# Get the function of the GO
		if LigneFile[i][0:6] == 'name: ' :
			coupe = LigneFile[i].split('name: ')
			FunctionGOtemp = coupe[1][:-1]

		# Get the type of GO
		if LigneFile[i][0:10] == 'namespace:' :
			coupe = LigneFile[i].split('namespace: ')
			TypeGOtemp = coupe[1][:-1]

		# End of the GO Data
		if LigneFile[i][0:9] == '[Typedef]' :
			NameGO, FunctionGO, TypeGO, IncludedGO, ObsoleteGO, HierarchieGO, nombreGO = MemorizeGO(NameGO, FunctionGO, TypeGO, IncludedGO, ObsoleteGO, HierarchieGO, ListeGOtemp, TypeGOtemp, FunctionGOtemp, ObsoleteGOtemp, InclusGOtemp, HierarchieGOtemp, nombreGO)
			i = len(LigneFile)-1

	return NameGO, FunctionGO, TypeGO, IncludedGO, ObsoleteGO, HierarchieGO, nombreGO





####################################################################################################################################
###	Create the hierarchy of the GeneOntology
####################################################################################################################################
def GOHierarchy(nombreGO, NameGO, ObsoleteGO, IncludedGO, HierarchieGO) :
    
	# initialise the variable for the hierarchy
	dicoHierarchie = {}
	for i in range(0, nombreGO, 1) :
		if ObsoleteGO[i] == 0 :
			if IncludedGO[i][0] == "NULL" :
				dicoHierarchie[NameGO[i]] = 0

	# Create the GO hierarchy
	for k in range(0, 20, 1) :
		for i in range(0, nombreGO, 1) :
			if ObsoleteGO[i] == 0 :
				for j in range(0, len(IncludedGO[i]), 1) :
					# here the link GO was just hierarchized the previous loop
					if IncludedGO[i][j] in dicoHierarchie.keys() and HierarchieGO[i][j] == -1 :
						# the hierarchy of NameGO[i] from this link GO is +1 
						HierarchieGO[i][j] = dicoHierarchie[IncludedGO[i][j]] + 1
						# check if the NameGO[i] is already hierarchized, if yes just keep the lowest hierarchy
						if NameGO[i] in dicoHierarchie.keys() :
							if dicoHierarchie[NameGO[i]] > HierarchieGO[i][j] and HierarchieGO[i][j] > 0:
								dicoHierarchie[NameGO[i]] = HierarchieGO[i][j]
						else :
							dicoHierarchie[NameGO[i]] = HierarchieGO[i][j]
							
	bestHierarchy = []
	EquivalentGO = []
	EquivalentIndex = []
	for i in range(0, nombreGO, 1) :
		temp = 10000000
		EquivalentGO.append(NameGO[i])
		EquivalentIndex.append(i)
		if ObsoleteGO[i] == 0 :
			for j in range(0, len(HierarchieGO[i]), 1) :
				if temp > HierarchieGO[i][j] :
					temp = HierarchieGO[i][j]
			bestHierarchy.append(temp)
		else :
			bestHierarchy.append(-1)
			
	return bestHierarchy, EquivalentGO, EquivalentIndex
	
	
	
	
	
####################################################################################################################################
###	Create the synomim GO for a hierarchy
####################################################################################################################################
def EquivalentGeneOntology(LevelHierarchy, nombreGO, NameGO, ObsoleteGO, bestHierarchy, IncludedGO, HierarchieGO, EquivalentGO, EquivalentIndex) :
	
	dicoIndex = {}
	dicoHierarchie = {}
	for i in range(0, nombreGO, 1) :
		if ObsoleteGO[i] == 0 and bestHierarchy[i] == int(LevelHierarchy) :
			dicoHierarchie[NameGO[i]] = NameGO[i]
			dicoIndex[NameGO[i]] = i
		if ObsoleteGO[i] == 0 and bestHierarchy[i] < int(LevelHierarchy) :
			dicoHierarchie[NameGO[i]] = NameGO[i]
			dicoIndex[NameGO[i]] = i
	
	for k in range(3, 16, 1) :
		for i in range(0, nombreGO, 1) :
			if bestHierarchy[i] == k :
				# I pick the first GO that have the lowest hierarchy
				for z in range(0, len(HierarchieGO[i]), 1) :
					if HierarchieGO[i][z] == k :
						EquivalentGO[i] = dicoHierarchie[IncludedGO[i][z]]
						dicoHierarchie[NameGO[i]] = dicoHierarchie[IncludedGO[i][z]]
						EquivalentIndex[i] = dicoIndex[IncludedGO[i][z]]
						dicoIndex[NameGO[i]] = dicoIndex[IncludedGO[i][z]]
						break
	
	return EquivalentGO, EquivalentIndex





####################################################################################################################################
### Parsing the first GeneOntology file
####################################################################################################################################
def ParsingGeneOntologyDefinition(GeneOntologyOBO, pathVisualDATA, LevelHierarchy) :

	#GeneOntologyOBO = sys.argv[1]
	#LevelHierarchy = sys.argv[2]

	# Get the raw GO data list
	LigneFile = LectureFichier(GeneOntologyOBO, pathVisualDATA)

	# Get the GeneOntology data
	NameGO = []
	FunctionGO = []
	TypeGO = []
	IncludedGO = []
	ObsoleteGO = []
	HierarchieGO = []
	nombreGO = 0
	NameGO, FunctionGO, TypeGO, IncludedGO, ObsoleteGO, HierarchieGO, nombreGO = DecoupeGeneOntologyListe(LigneFile, NameGO, FunctionGO, TypeGO, IncludedGO, ObsoleteGO, HierarchieGO, nombreGO)
		
		
		
	# Make the hierarchy between GO
	bestHierarchy, EquivalentGO, EquivalentIndex = GOHierarchy(nombreGO, NameGO, ObsoleteGO, IncludedGO, HierarchieGO)
	# Make the synonym of the GeneOntology
	EquivalentGO, EquivalentIndex = EquivalentGeneOntology(LevelHierarchy, nombreGO, NameGO, ObsoleteGO, bestHierarchy, IncludedGO, HierarchieGO, EquivalentGO, EquivalentIndex)
		
	
		
	grandListe = []
	for i in range(0, len(NameGO), 1) :
		tp = []
		tp.append(NameGO[i])
		tp.append(TypeGO[i])
		tp.append(FunctionGO[i])
		tp.append(ObsoleteGO[i])
		tp.append(IncludedGO[i])
		tp.append(HierarchieGO[i])
		tp.append(bestHierarchy[i])
		tp.append(EquivalentGO[i])
		tp.append(EquivalentIndex[i])
		grandListe.append(tp)

	pathVisualDATA = pathVisualDATA + "/DATA_List_GeneOntology.txt"
	dataFrame_Ontology = pd.DataFrame(grandListe, columns=['GO Name', 'Type GO', 'Function GO', 'Obsolete', 'GO Included', 'GO Hierarchy', 'GO Best Hierarchy', 'Equivalent', 'Equiv Index'] ) 
	dataFrame_Ontology.to_csv(pathVisualDATA, index = False) # relative position
	os.remove(GeneOntologyOBO)





	# ECRIT TOUS LES GO, LEUR NOM, FUNCTION, TYPE ET HIERARCHY
	#print("#GO ID\t#Type GO\t#Function\t#Obsolete GO\t#Hierarchy in GO Tree\t#Is Part of\t#All GO Tree Position")
	#for i in range(0, nombreGO, 1) :
	#	print(NameGO[i] + "\t" + TypeGO[i] + "\t" + FunctionGO[i] + "\t" + str(ObsoleteGO[i]) + "\t" + str(bestHierarchy[i]) + "\t" + str(IncludedGO[i]) + "\t" + str(HierarchieGO[i]) + "\t" + EquivalentGO[i] + "\t" + str(EquivalentIndex[i]) )

	# ECRIT LES DIFFERENTS GO EN FONCTION DE LA HIERARCHIE
	#for k in range(-1, 20, 1) :
	#	temp = "GO_Hierarchy" + str(k) + ".txt"
	#	f = open(temp, "w")
	#	f.write("#GO ID\t#Type GO\t#Function\t#Obsolete GO\t#Hierarchy in GO Tree\t#Is Part of\t#All GO Tree Position")
	#	for i in range(0, nombreGO, 1) :
	#		if bestHierarchy[i] == k :
	#			f.write(NameGO[i] + "\t" + TypeGO[i] + "\t" + FunctionGO[i] + "\t" + str(ObsoleteGO[i]) + "\t" + str(bestHierarchy[i]) + "\t" + str(IncludedGO[i]) + "\t" + str(HierarchieGO[i]) + "\n")
	#	f.close()


