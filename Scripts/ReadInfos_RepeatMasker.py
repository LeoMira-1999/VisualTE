#!/usr/bin/python3
import os
import sys
import pandas as pd

########################################################################################################################
###	Read RepeatMasker file
########################################################################################################################

# Example of RepeatMasker Lines
# 1776   13.4  0.6  5.0  CM000686.2     15187    15499 (57211916) C ALU             Unspecified   (11)    301      2     7  
#  641   24.1  0.6  9.0  CM000686.2     15500    15668 (57211747) + ALU             Unspecified     13    168  (144)     8  
# 2886   13.5  0.4  3.5  CM000686.2     15692    16167 (57211248) + LTR2C           Unspecified      1    462    (0)     9  

def ReadRepeatMasker(fileTE, Repbase, pathVisualDATA, root, progressTask, textProcess, nbLigneText, insertionText):

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
		
		progressTask["value"] = 0
		progressTask["maximum"] = len(lignes)
		progressTask.start()
	
		# do not read  the three first line
		for i in range(0, len(lignes), 1):
			
			if i % 100 == 0 and i > 0 :
				progressTask.step(100)
				root.update()
			
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
						
	
	textAEcrire = 'Writing Alls TE hits from RepeatMasker... \n'
	textProcess.insert(insertionText, textAEcrire)
	nbLigneText += 1
	insertionText = str(nbLigneText) + '.0'
	root.update()
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
	
	
	textAEcrire = 'Writing Summary TE data from RepeatMasker... \n'
	textProcess.insert(insertionText, textAEcrire)
	nbLigneText += 1
	insertionText = str(nbLigneText) + '.0'
	root.update()
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



