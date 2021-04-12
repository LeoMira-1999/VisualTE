#!/usr/bin/python3
import os
import sys
import importlib
import importlib.util
import pandas as pd
import subprocess
from . import Interface_SelectTE


###############################################################################################################################################################
###	Extract the TE sequences 
###############################################################################################################################################################
def ExtractSequences(pathVisual, pathVisualNEW, moduleCommonDATA, moduleSelectTE, NomSeq, DEB, FIN, Sens, Size, Similarity, indiceTE, indexTE) :
	
	NameChr = moduleCommonDATA.dataFrame_Organism['Name'].tolist()
	NameID = moduleCommonDATA.dataFrame_Organism['NameID'].tolist()
	RefSeq = moduleCommonDATA.dataFrame_Organism['RefSeq'].tolist()
	
	# Read the sequence lines of the genome
	f = open(moduleCommonDATA.fileFNAgenome, "r")
	lignes = f.readlines()
	f.close()
	
	# Put the sequence in the list of string with the ID
	idSEQ = []
	sequenceNucl = []
	tempSeq = ''
	for i in range(0, len(lignes), 1) :
		lignes[i] = lignes[i].rstrip()
		if lignes[i][0] == '>' :
			decoupe = lignes[i].split(' ')
			idSEQ.append(decoupe[0][1:])
			if len(tempSeq) > 1 :
				sequenceNucl.append(tempSeq)
			tempSeq = ''
		else :
			tempSeq += lignes[i]
	sequenceNucl.append(tempSeq)		
		
		
		
	TEseq = []
	for k in range(0, len(DEB), 1) :
		TEseq.append('')
		
	for i in range(0, len(idSEQ), 1) :
		indiceJ = -1
		for j in range(0, len(NameID), 1) :
			if idSEQ[i] == NameID[j] or idSEQ[i] == RefSeq[j] or idSEQ[i] == NameChr[j]:
				indiceJ = j
				break
		for k in range(0, len(NomSeq), 1) :
			if NameID[indiceJ] == NomSeq[k] or RefSeq[indiceJ] == NomSeq[k] or NameChr[indiceJ] == NomSeq[k]:
				if Sens[k] == '+' :
					TEseq[k] = sequenceNucl[i][DEB[k]:FIN[k]+1].upper()
				else :
					tempSeq = sequenceNucl[i][DEB[k]:FIN[k]+1].upper()
					TEseq[k] = tempSeq[::-1]
					TEseq[k] = TEseq[k].replace('A', '1')
					TEseq[k] = TEseq[k].replace('C', '2')
					TEseq[k] = TEseq[k].replace('G', '3')
					TEseq[k] = TEseq[k].replace('T', 'A')
					TEseq[k] = TEseq[k].replace('1', 'T')
					TEseq[k] = TEseq[k].replace('2', 'G')
					TEseq[k] = TEseq[k].replace('3', 'C')	
		
		
		
	# Write the data 
	if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
		temp = pathVisualNEW + '/Downloaded/TEOccurrences0.fna'
	else :			
		temp = pathVisualNEW + '/Downloaded/TEOccurrences' + str(indiceTE) + '.fna'	
	
	f = open(temp, "a")
	for k in range(0, len(DEB), 1) :
		f.write('>' + moduleSelectTE.list_selection_TE[indiceTE] + '_' + str(indexTE) + ' ' + str(Size[k]) + ' ' + str(Similarity[k]) + ' ' + NomSeq[k] + '_' + str(DEB[k]) + '_' + str(FIN[k]) + '_' + Sens[k] + '\n')
		f.write(TEseq[k] + '\n')
		indexTE += 1
	f.close()
		
	return indexTE
	
	
###############################################################################################################################################################
###	Align the TE sequences and Create phylogenetics tree 
###############################################################################################################################################################
def AlignETPhylogeny(pathVisual, pathVisualNEW, moduleCommonDATA, moduleSelectTE, Seq, DEB, FIN, Sens, Size, Similarity) :
	
	indexTE = 0
	for j in range(0, len(moduleSelectTE.list_selection_TE), 1) :
		indexTE = ExtractSequences(pathVisual, pathVisualNEW, moduleCommonDATA, moduleSelectTE, Seq[j], DEB[j], FIN[j], Sens[j], Size[j], Similarity[j], j, indexTE)
	
	
	if moduleSelectTE.OfficialName[0:7] == 'Merged ' :
		# Create here the alignment of the TE occurrences
		tempInput = pathVisualNEW + '/Downloaded/TEOccurrences0.fna'
		tempOutputAlign = pathVisualNEW + '/Downloaded/TEOccurrences0.align'
		p1 = subprocess.Popen(["clustalo", "-i", tempInput, "-o", tempOutputAlign, "--outfmt=a2m", "--force" ])
		p1.wait()
		
		# Create here the Phylogenetic tree and the newick output
		tempOutputTree = pathVisualNEW + '/Downloaded/TEOccurrences0.newick'
		p2 = subprocess.run(["FastTree", "-nt", tempOutputAlign], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		f = open(tempOutputTree, "w")
		output = str(p2.stdout)
		f.write(output[2:-4])
		f.close()
	else :
		for j in range(0, len(moduleSelectTE.list_selection_TE), 1) :
			# Create here the alignment of the TE occurrences
			tempInput = pathVisualNEW + '/Downloaded/TEOccurrences' + str(j) + '.fna'
			tempOutputAlign = pathVisualNEW + '/Downloaded/TEOccurrences' + str(j) + '.align'
			p1 = subprocess.Popen(["clustalo", "-i", tempInput, "-o", tempOutputAlign, "--outfmt=a2m", "--force" ])
			p1.wait()
		
			# Create here the Phylogenetic tree and the newick output
			tempOutputTree = pathVisualNEW + '/Downloaded/TEOccurrences' + str(j) + '.newick'
			p2 = subprocess.run(["FastTree", "-nt", tempOutputAlign], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			f = open(tempOutputTree, "w")
			output = str(p2.stdout)
			f.write(output[2:-4])
			f.close()
			
