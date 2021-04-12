#!/usr/bin/python3
import os
import time
import sys
import shutil
import gzip
import urllib.request
import ftplib
import pandas as pd
from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox
import tkinter.ttk as ttk
import plotly.graph_objs as go

# import python script that create launching files
from Scripts import Interface_Main, Interface_DownloadGenomes, Interface_Processing, Interface_SelectTE
from Scripts import Create_MainFile,  Create_Color, Create_CommonHead
from Scripts import ReadInfos_TE, ReadInfos_RepeatMasker, ReadInfos_NCBIAnnotations, ReadInfos_GeneOntology, ReadInfos_Compresse
from Scripts import Create_CommonDATA
from Scripts import MakeFunction_GenomeBrowser
from Scripts import MakeFunction_ChromosomeDistribution
from Scripts import MakeFunction_GeneralFeaturesDistribution
from Scripts import Interface_Main_Dash





########################################################################################################################

# LISTE DE BUGS ou A FAIRE :
# VisualTE ne prend que RepeatMasker format, il ne prend pas les fichiers Repet et BLAST
# le pourcentage de ncRNA dans certains chromosome est trop grand
# bug aussi dans la creation des dataframes pour le TE selectionne ...
# VisualTE ne prend que les fichier ENCODE + pire il ne prend les fichiers locaux sous 1 seul format
# les noms des tissus organ et a changer modifier (majuscule minuscule par ex) : repetition a cause d'erreur de typographie
# nom des chromosomes ne commencent pas tous par chr
# https://maayanlab.cloud/Enrichr/#stats : liste des genes/GO pour enrichment mais en local pas le meme resultat qu'en reso ??



# la plupart des legendes sont a refaire !
# Pour le graphe circos, trouver une methode de clustering pour faire les clusters
# bug in MakeFunction_TEEnvironment : Columns (3,4) have mixed types. Specify dtype option on import or set low_memory=False.
# autre bug : il y a trop de tissue et d'organe difference dans ENCODE, surtout avec de simple faute d'orthographe
# Probleme d'affichage pour les TFBS des summarytable
# -349806 : bug dans la distance des positions de gene en random






########################################################################################################################

###### PREMIERE PARTIE : OBTENTION ET MODIFICATION DES DONNEES GENOMIQUES
# Hierarchie - Graph d'appel des fichiers python :
# make_VisualTE3.py											# Fichier Python : Lancement de la creation de VisualTE
# ∟ CreateGenomeDATA() 											# Lance la premiere interface pour recupere les donnees bruts
#	Interface_Main.py										# Fichier Python : Lancement 1ere interface download des donnees pour 1 genome, cree le repertoire
#	∟ Interface()											# CHoix des donnees acquise ou non par l'utilisateur
#		availableDATA()										# Lance les programmes qui recupere les donnees
#			CloseVisualTEmake()								# Ferme l'interface si aucune donnees TE
#			Interface_Transposons.py							# Fichier Python : Lie le fichier des TEs a l'interface
#			∟ LocalTransposableElements()							# Interface pour selectionner les TEs
#				getTransposable()							# copie les donnees des TE dans le bon repertoire
#					Interface_SettingVariables.py					# Fichier Python : Sauvergarde le nom du fichier de TE
#			Interface_GenomeDATA.py								# Mini interface du choix du genome
#			∟ DownloadGenomeFiles()								# Select the genome name present in NCBI
#				downlaodNCBIgenome()							# Interface pour le telechargement sur le NCBI
#					Interface_DownloadGenomes.py					# Fichier Python : Interface de Telecharger le fichier passe en parametres
#					∟ lanceTelechargement()						# Lance les fonctions pour le telechargement
#						findGenomeFile()					# cherche l'adresse ftp du genome
#							RechercheGenomeFTP()				# parcours arborescence du ftp
#								getListeGenome()			# liste les genomes d'un repertoire ftp
#					∟ DownloadGenomeFile()						# Telecharge le GFF et FNA du genome
#						Interface_SettingVariables.py				# Fichier Python : memorize le nom du fichier genome et son new repertoire
#			∟ LocalGenomes()								# interface de localisation du genome
#				closeGenomeWindow()							# copies les fichiers genomes
#					Interface_SettingVariables.py					# Fichier Python : memorize le nom du fichier genome et son new repertoire
#			Interface_GeneOntology.py							# Fichier Python : Interface pour les geneOntology
#			∟ DownloadGO()									# interface de telechargement
#				DownloadGOFile()							# Telecharge les 2 fichier du NCBI
#					Interface_SettingVariables.py					# Fichier Python : memorize le nom du fichier genome et son new repertoire
#			∟ LocalGeneOntology()								# Interface de copies des GO
#				getGObasic() et getGOgene()						# recupere le chemin des 2 fichiers GO
#				closeGOWindow()								# Ferme l'interface apres les 2 copies
#					Interface_SettingVariables.py					# Fichier Python : memorize le nom du fichier genome et son new repertoire
#			Interface_ChipSeq.py								# Fichier Python : Interface pour les ChipSeq
#			∟ DownloadChipSEQ()								# Interface pour Telecharger les ChipSeq
#				downloadENCODE()							# Interface de deroulement du telechargment
#				ReadInfos_CHIPSeq.py							# Fichier Python : Recupere les TFBS d'ENCODE
#				TelechargeExperiments()							# Recupere la liste des ChipSeq
#				DownloadExperimentsDATA()						# Lits les details de chaque ChipSeq
#				readExperiments()							# Selectionne les ChipSeq
#				ExtractExperimentInfos() 						# Telecharge le ChipSeq
#					Decompress()							# decompress le ChipSeq
#					LectureFichier()						# Lit les infos ChipSeq et le met dans un dataframe
#				Interface_SettingVariables.py						# Fichier Python : memorize le nom du fichier TFBS et son new repertoire
#			∟ LocalChipSEQ()								# Interface pour copier les ChipSeq
#				getENCODE()								# Copie les fichier ChipSeq dans le bon repertoire
#				Interface_SettingVariables.py						# Fichier Python : memorize le nom du fichier genome et son new repertoire
#	InterfaceProcess.py										# Fichier Python : Inferface d'extraction des resultats
#	∟ InterfaceProcessDATA()									# Inferface d'extraction des resultats
#		RunProcesses()										# Lance les extractions des fichiers
#			ReadInfos_Compresse.py								# Fichier Python :  Decompresse les fichiers
#			UnzipFile()									# Decompresse les fichiers zip
#			ReadInfos_TE.py									# Fichier Python : extrait Repbase
#			LireRepbase()									# Lit le fichier d'information sur Repbase (dico TE - superfamille)
#			ReadInfos_RepeatMasker.py							# Fichier Python : extrait RepeatMasker data
#			∟ ReadRepeatMasker()								# Extract information TE au format RepeatMasker
#			ReadInfos_NCBIAnnotations.py							# Fichier Python : Extraction des annotations du genome
#			∟ ReadGFF()									# Lance l'extraction des annotations
#				LireChromosome()							# Prend les infos sur le chromosomes
#				LirePseudogene()							# Prend les infos sur les pseudogenes
#				lireGene()								# Prend les infos sur les genes
#				LirePseudoExon()							# Prend les infos sur les exons de pseudogenes
#				LireExon()								# Prend les infos sur les exons de genes
#				lireMiscRNA()								# Prend les infos sur les ncRNAs
#				LireOfficialName()							# Recupere de NCBI les infos sur le genome
#				prepareInfosOrganism()							# Formate les infos du NCBI
#				PrepareGenomeFileForDash()						# Mets les annotations en dataframe
#			ReadInfos_GeneOntology.py							# Fichier Python : Hierarchie des GO
#			∟ ParsingGeneOntologyDefinition()						# Lance les fonction de Hierarchie
#				DecoupeGeneOntologyListe()						# Lance extraction des infos des GO
#					MemorizeGO()							# Prend les infos sur les GO
#				GOHierarchy()								# Positionne le GO dans l'arbre de hierarchie des GO
#				EquivalentGeneOntology()						# Donne le GO equivalent correspondant a un niveau donne
#			∟ SelectGenomeGO()								# Create the GO list for the selected genome et table de comptage des GO
#			ReadInfos_WikiPathWays.py							# Fichier Python : File SVG des pathways
#			∟ CopyPathWaysFile()								# Copy les fichier SVG pour la fonction GeneOntology
#			ReadInfos_CHIPSeq.py								# Fichier Python : Modifie la structure des fichiers ChipSeq
#			∟ TransformChipSEQ()								# Change la forme du fichier des ChipSeq et cree un tableau de compatage tissue, organ
#	Create_MainFile.py										# Fichier Python : Create the python file qui relie tous les autres fonctions python de VisualTE
#	∟ EcrireApp()											# Ecris le fichier qui lie tous les fichiers Dash
#	Create_Color.py											# Fichier Python : les couleurs de l'application
#	∟ PrepareListeColor() 										# Cree la table des couleurs pour toutes les fonctions
#	Create_CommonDATA.py										# Fichier Python : Cree les tables qui contiennent des infos generales sur tout le genome
#	∟ PrepareCommonDATA()										# Ecris les donnees acquises des precedentes fonctions dans un fichier

###### DEUXIEME PARTIE : OBTENTION ET MODIFICATION DES DONNEES DE LA FAMILLE D'ELEMENTS TRANSPOSABLES
# make_VisualTE3.py											# Fichier Python : Lancement de la creation de VisualTE
# ∟ SelectionTE()											# Lancement de la selection TE et des donnees qui sont adossees
#	Interface_SelectTE.py										# Interface pour les donnees lies au TE selectionner
#	∟ getListeTE()											# Get the list of TE selectionnes
#	∟ Interface_Selection()										# Interface lancant les recuperations des donnees specifiques
#		getTE()											# Memorize the TE selected name
#		getMergeFamily()									# Merge or nor the selected TE and open the new interface
#		DestroyPreviousWindow()									# Detruit l'interface pour creer la suivante
#		Interface_ProcessSelectionTE.py								# Fichier Python : Lance la selection des donnees
#		∟ DrawNewWindow()									# Cree la 2eme interface
#		∟ CreateFonctionDASH()									# Lance les processes de selection des donnees
#			ChangeCheckbutton()								# Modifie l'interface apres chaque fonction cree
#			Create_CommonDATA2.py								# Fichier Python : ecris des donnees communes a tous les tabs
#			∟ writeSelectTE()								# Ecris les donnees recuperes sur les TEs
#			ReadInfos_TE.py									# Fichier Python : Donnees sur les TE selectionnes et autres donnees communes
#			∟ GetSuperfamily()								# Recupere la superfamille des TEs selectionnes
#			Create_SelectedAnnotations.py							# Recupere l'ensemble de l'environnement genomique des TE (chaque sequence)
#			∟ SelectAnnotations()								# Recupere les positions des TEs selectionnes
#				SelectGenes()								# recupere les genes et exons autour des TE sequences
#					dataframe_for_Genes()						# Ecrit dans un dataframe les exons autours des TE sequences
#					dataframe_for_ClosestGenes()					# Ecrit seulement la liste des genes les plus proches
#					dataframe_for_Exons()						# Ecrit dans un dataframe les exons autours des TE sequences
#				SelectOtherTE()								# recupere les autres TE entre les gene 5' et 3'
#				SelectPseudo()								# recupere les pseudogenes entre les gene 5' et 3'
#				SelectNCRna()								# recupere les ncRNAs entre les gene 5' et 3'
#				SelectPositionInside()							# recupere la position relative du TE inside gene (si exist)
#			Create_Alignment_and_Tree.py							# Fichier Python : Creer alignement
#			∟ AlignETPhylogeny()								# Aligne les sequences de TE
#				ExtractSequences()							# Extrait les sequences de TE au format FASTA
#			Create_Random_Sequences.py							# Fichier Python : extrait les sequences aleatoires
#			∟ RandomSequences()								# Selectionne position aleatoires pour les genes et pour les TFBS (2 jeu de sequences)
#				randomSequenceForTFBS()							# Choisi aleatoirement des positions (pour TFBS)
#				RandomSameDistance()							# Selectionne position aleatoire en fonction de la position des genes des TE (pour GO et distance)
#					SelectPositionInsideRandom()					# donne la position relative de la sequence si inside
#			Create_Overlap_TFBS.py								# Fichier Python : Extraction des TFBS
#			∟ ExtractTFBS_forTE()								# Lance extraction TFBS pour les TEs
#				OverlapTFBS()								# Detecte si un TFBS est dans la zone du TE
#					memorizeDicoTFBS()						# memorize le TFBS
#			∟ ExtractTFBS_forRandom()							# Lance extraction TFBS pour les sequences random
#				OverlapTFBSRandom()							# Detecte si un TFBS est dans la zone de la sequences Random
#					memorizeDicoTFBS()						# memorize le TFBS
#			∟ PrintGlobalTFBS()								# Ecrit les resulats des TFBS
#			Create_MainFile.py								# Fichier Python : Lance toutes les fonctionsd du site web
#			∟ EcrireVisualTE()								# Ecrit le fichier python de lancement des fonctions
#			Create_CommonDATA2.py 								# Fichier Python : ecris des donnees communes a tous les tabs
#			∟ AjoutAnnotations()								# Ajoute les dataframes crees
#			MakeFunction_GenomeBrowser.py							# Fichier Python : Ecriture de la 1er function web (affiche les TE sur le genome)
#			∟ GenomeBrowser()								# Ecrit la fonction de base de la fonction et appelle les autres
#				InformationGenome()							# Ecrit la fonction qui prepare les dataframes
#				LegendeChrom()								# Ecrit la fonction de la legende du graphe principale !
#				LignesAnnotations()							# Ecrit la fonction qui ajoute un radiobox pour le deuxieme graphe
#				CreateLayout()								# Ecrit la fonction qui cree le cadre de tous les graphiques
#				CreateCallBack_Genome_Onglet1()						# Ecrit la fonction qui configure du 1er graphique et sa reponse a l'utilisateur
#					CreateTEbar()							# Ecrit la fonction des les barres representant les TEs sur le genome
#				CreatedCallBack_LineChromosome_Onglet1()				# Ecrit la fonction de configuration du deuxieme graphique et sa reponse a l'utilisateur
#					UpdateLine_Chrom()						# Ecrit la fonction qui cree les lignes sur le 2eme graphe en fonction de l'utilisateur
#			MakeFunction_ChromosomeDistribution.py						# Fichier Python : Ecriture de la 1er function web (affiche les TE sur le chromsome)
#			∟ ChromosomeDistribution()							# Ecrit la fonction qui ecrit le fichier pour la 2eme fonction web
#				Invariable_Script()							# Ecrit la fonction qui get the values from dataframe
#				InvariableCHR_barchart()						# Ecrit la fonction pour le barchart
#				InvariableValue_PieChart()						# Ecrit la fonction pour le piechart
#				CalculTEvalue_PieChartDATA()						# Ecrit la fonction qui calcule le piechart
#				Invariable_ChromosomeDistributionLayout()				# Ecrit la fonction qui realise les cadres de la fonction web
#				CreateCallBack_BarChart_Onglet2()					# Ecrit la fonction qui va dessiner le barchart
#					CalculTEvalue_ForBarchart()					# Ecrit la fonction qui calcule le % de TE pour chaque chromosome
#					Calculate_ChiSquare()						# Ecrit la fonction qui calcule le chisquare : biais or not TE insertion
#					TELine_In_Barchart()						# Ecrit la fonction qui dessine les courbes sur le barchart
# 				CreateCallBack_PieChart_Onglet2()					# Ecrit la fonction qui dessine le piechart
#				CreateCallBack_Tableau_Onglet2()					# Ecrit la fonction qui dessine la figure du tableau
#					TableauInCallback()						# Ecrit la fonction qui ecrit les valeurs du tableau (dataframe) et TE
#			MakeFunction_GeneralFeaturesDistribution.py					# Fichier Python : Ecriture de la 3eme function web (similarite et taille)
#			∟ GeneralFeatures_layout()							# Ecrit la fonction qui met en place la 3eme fonction web
#				NonUpdatedVariable_Onglet3()						# Ecrit la fonction qui calcule pour chaque similarite et chaque taille le % des TEs
#				CreateLayoutGeneralFeatures()						# Ecrit la fonction qui met la forme generale de la 3eme fonction
#				CreateCallBack_2D_Onglet3()						# Ecrit la fonction qui gere les 2 graphes 2D en fonction de l'utilisateur
#					DataFromSliders()						# Ecrit la fonction qui recupere les valeurs des slider generaux
#					LineChartSize()							# Ecrit la fonction qui calcule chaque point des graphes 2D
#					HTMLPosition_2D_Onglet3()					# Ecrit la fonction qui configure les 2 figures
#				CreateCallBack_3D_Onglet3()						# Ecrit la fonction qui gere le graphes 3D en fonction de l'utilisateur
#					SurfaceSizeSimilarity()						# Ecrit la fonction qui recupere les valeurs pour le graphe 3D
#					HTMLPosition_3D_Onglet3()					# Ecrit la fonction qui configure le graph 3D
#			MakeFunction_SimilarityOccurrences.py						# # Fichier Python : Ecriture de la 4eme function web : alignement et l'arbre phylogenique des TEs
#			∟ SimilarityOccurrences()							# Ecrit la fonction qui lance les fonctions d'ecriture de la 4eme fonction web
#				InvariableDATA()							# Ecrit la fonction qui recupere les donnees des sliders
#				InvariableCircos()							# Ecrit la fonction qui ecrit la base du circos comme les couleurs
#				NewickTree()								# Ecrit la fonction qui va lire le fichier newick (tree)
#					SplitTree()							# Ecrit la fonction qui decoupe l'arbre newick
#					TreeInVariable()						# Ecrit la fonction qui assigne a chaque membre de l'arbre a une variable
#				ReadAlignement()							# Ecrit la fonction qui memorise l'arbre dans des tableaux
#				Create_Invariable_layout()						# Ecrit la fonction qui configure l'affichage de la page web
#				CreateCallBack_Alignement_Onglet7()					# Ecrit la fonction qui affiche le graphe alignement en fonction de l'utilisateur
#					ValuesInCallback()						# Ecrit la fonction qui recupere les valeurs des sliders
#				CreateCallBack_Classification_Onglet7()					# Ecrit la fonction qui modifie le graphe phylogenique en fonction de l'utilisateur
#					ValuesInCallback()						# Ecrit la fonction qui recupere les valeurs des sliders
#					CreateDataTree()						# Ecrit la fonction qui les donnees au format de l'arbre pour Cytoscape
#					CreateCircosDATA()						# Ecrit la fonction qui les donnees au format de dash circos
#					CreateGraphClassification()					# Ecrit la fonction qui la configuration du graphe phylogenie/circos
#			MakeFunction_TEEnvironment.py							# Fichier Python : Ecriture de la 5eme function web : Affiche chaque TE avec toutes les annotations autour de lui
#			∟ TEEnvironment()								# Ecrit la fonction qui lance les fonctions d'ecriture de la 5eme fonction web
#				Create_layout()								# Ecrit la fonction qui ecrit le cadre de la figure
#				CreateCallBack_Environnemnt()						# Ecrit la fonction qui la page web et sa configuration
#					GetListeOccurrences()						# Ecrit la fonction qui recupere les donnees pour le graphe
#				CreateCallBack_Slider()							# Ecrit la fonction qui affiche et dessine le TE avec son environnement
#					GraduationInGraph()						# Ecrit la fonction qui affiche les graduations
#					OtherTEinGraph()						# Ecrit la fonction qui affiche les autres TEs
#					AddGenesInGraph()						# Ecrit la fonction qui affiche les genes
#					AddExonsInGraph()						# Ecrit la fonction qui affiche les exons dans les genes
#					AddncRNAinGraph()						# Ecrit la fonction qui affiche les ncRNAs
#					AddPseudogenesInGraph()						# Ecrit la fonction qui affiche les pseudogenes
#					AddCHiSepInGraph()						# Ecrit la fonction qui extrait les donnees ChipSeq et les affiches
#			MakeFunction_DistanceNeighboringGene.py						# Fichier Python : Ecriture de la 6eme function web : TE - Gene distribution
#			∟ DistanceNeighboringGene()							# Ecrit la fonction qui lance les fonctions d'ecriture de la 6eme fonction web
#				Create_layout()								# Ecrit la fonction qui ecrit le cadre des figures
#				CreationClasse()							# Ecrit la fonction qui va definir les differentes tailles de distance
#				CreationSelectionRandomSequences()					# Ecrit la fonction qui compte le nombre de TE ou random dans chaque classe de distance
#				CreationSelectionRandomSequencesInside()				# Ecrit la fonction qui compte le nombre de TE ou random dans classe inside
#				CreatedCallBack_Distplot_Onglet6()					# Ecrit la fonction qui lance la distribution de distance et la dessine
#					ValueSliderRecup()						# Ecrit la fonction qui recupere les valeurs des slides communs
#			MakeFunction_NeighboringGeneFunctions.py					# Fichier Python : Ecriture de la 7eme function web : Gene function arround TE
#			∟ NeighboringGeneFunctions()							# Ecrit la fonction qui lance les fonctions d'ecriture de la 6eme fonction web
#				Create_layout()								# Ecrit la fonction qui ecrit le cadre des figures
#				EnrichementGO()								# Ecrit la fonction qui lance l'Enrichement des GO et l'ecrit dans le tableau
#					ValueSliderRecup()						# Ecrit la fonction qui recupere les valeurs des slides communs
#				SupplementTable()							# Ecrit la fonction qui recupere la case du tableau clicque
#			MakeFunction_SummaryTable.py							# Fichier Python : Ecriture de la 8eme function web : affiche une table de type Excel qui synthetise les resultats
#			∟ SummaryTable()								# Ecrit la fonction qui lance les fonctions d'ecriture de la 8eme fonction web
#				Create_layout()								# Ecrit la fonction qui fait le cadre HTML de la fonction web
#				CreateCallBack_Tableau_Onglet9()					# Ecrit la fonction qui lances les fonctions pour faire le tableau excel via utilisateur
#					Dataframe_in_Table()						# Ecrit la fonction qui remplit le tableau en fonction des donnees choisi par utilisateur
#					StyleTableInCallback9()						# Ecrit la fonction qui le style d'affichage du tableau excel


#		MakeFunction_NeighboringGene.py							# Cree la fonction python qui calcule la distribution de la distance TE - Gene et la distribution des functions GO des genes
#		MakeFunction_OverlappingTFBS.py							# Cree la fonction python qui









########################################################################################################################
def CreateGenomeDATA(GenomeName, TEmethod) :

	########################################################################################################################
	###	Create the directories for the future files
	########################################################################################################################

	print("Create the directories for VisualTE3 ...")
	#tempsSeconde = int(time.time())
	#pathVisual = 'VisualTE3_' + str(tempsSeconde)
	pathVisual = 'VisualTE3__' + str(GenomeName) + '__' + str(TEmethod)
	os.mkdir(pathVisual)

	# Create the (sub) directories for VisualTE3
	pathVisualCSS = pathVisual + '/css'
	os.mkdir(pathVisualCSS)
	pathVisualCSS = pathVisualCSS + '/dash-wind-streaming.css'
	shutil.copyfile('Scripts/dash-wind-streaming.css', pathVisualCSS)

	pathVisualFunctions = pathVisual + '/Functions'
	os.mkdir(pathVisualFunctions)

	pathVisualDATA = pathVisual + '/Downloaded'
	os.mkdir(pathVisualDATA)





	########################################################################################################################
	###	Get the essential files
	########################################################################################################################

	fichierTE, fileGFFgenome, fileFNAgenome, GeneOntologyOBO, GeneOntologyGI = Interface_Main.Interface(pathVisualDATA)






	########################################################################################################################
	###	Read data files
	########################################################################################################################

	print("Got the necessary information, now prepare the data files ...")
	nbSeq_Assemble, nameOrganism, maxSize, taxon, dictionary_organ, dictionary_tissue = Interface_Processing.InterfaceProcessDATA(pathVisualDATA, fileGFFgenome, fileFNAgenome, GeneOntologyOBO, GeneOntologyGI, fichierTE)





	########################################################################################################################
	###	Create the necessary files
	########################################################################################################################

	print("Create the few main files ...\n")
	# file that get the css style for dash
	Create_MainFile.EcrireApp(pathVisual)

	# Create the color for all kind of stuff
	Create_Color.PrepareListeColor(pathVisual)

	print("Create the function files ...")
	# Make the data common to mostly all function scripts
	Create_CommonDATA.PrepareCommonDATA(pathVisual, nameOrganism, nbSeq_Assemble, maxSize, taxon, fileFNAgenome, dictionary_organ, dictionary_tissue)










########################################################################################################################
def SelectionTE(pathVisual) :

	########################################################################################################################
	### Selection of TEs
	########################################################################################################################

	print("Selection of TE families and creation of missing scripts...")
	pathVisualDATA = pathVisual + '/Downloaded'
	dataTE = pathVisualDATA + '/DATA_List_TE_families.txt'
	#tempsSeconde = int(time.time())
	tempsSeconde = 63

	pathVisualNEW = pathVisual + '/' + str(tempsSeconde)
	os.mkdir(pathVisualNEW)
	pathVisualFunctions = pathVisualNEW + '/Functions'
	os.mkdir(pathVisualFunctions)
	# Copy the app.py file
	originalFile = pathVisual + '/app.py'
	copyFile = pathVisualNEW + '/app.py'
	shutil.copyfile(originalFile, copyFile)
	# Copy the CommonDATA file
	originalFile = pathVisual + '/Functions/CommonDATA.py'
	copyFile = pathVisualNEW + '/Functions/CommonDATA.py'
	shutil.copyfile(originalFile, copyFile)
	# Copy the Couleur file
	originalFile = pathVisual + '/Functions/Couleur.py'
	copyFile = pathVisualNEW + '/Functions/Couleur.py'
	shutil.copyfile(originalFile, copyFile)


	# Read the list of TE available for this genome
	Interface_SelectTE.getListeTE(dataTE)
	# Run the process of data selection
	Interface_SelectTE.Interface_Selection(pathVisual, pathVisualNEW, tempsSeconde)


	pathVisualNEW = pathVisualNEW + '/css'
	os.mkdir(pathVisualNEW)
	# Copy the css file
	originalFile = pathVisual + '/css/dash-wind-streaming.css'
	copyFile = pathVisualNEW + '/dash-wind-streaming.css'
	shutil.copyfile(originalFile, copyFile)










########################################################################################################################
def Help() :
	print("\n\tThis is the basic help of VisualTE version 3")
	print("\tVisualTE 3 is splitted in tree parts :")
	print("\t- The first part download and extract the data for a selected genome")
	print("\t\tIt will be launch with the '-Genome' option")
	print("\t- Two more arguments are necessary : the genome name (I.e Human) and the TE detection method name (I.e. Repet, RepeatMasker or Blast)")
	print("\t- The second part will create the analysis function for the selected TE family")
	print("\t\tIt will be lauch with the '-TE' option and the directory created by the first part")
	print("\t- The last part will launch the VisualTE 3 itself")
	print("\t\tThe two first parts will create a directory that contains all data and necessary functions")
	print("\t\tThis directory will contain a 'VisualTE3.py' file that will launch everything \n\n")










########################################################################################################################
########################################################################################################################
# Choice of the make_VisualTE3 uses :
if len(sys.argv) == 1 :
	Help()
else :
	if sys.argv[1] == '-Dash':
		Interface_Main_Dash.Dash_CreateGenomeDATA()

	elif sys.argv[1] == '-TE' :
		SelectionTE(sys.argv[2])

	elif sys.argv[1] == '-Genome' :
		CreateGenomeDATA(sys.argv[2], sys.argv[3])

	elif sys.argv[1] == '-h' or sys.argv[1] == '-help' :
		Help()
	else :
		Help()



# Species divergence times were based on [Impacts of the Cretaceous Terrestrial Revolution and KPg extinction on mammal diversification]. Repeat ages were estimated by dividing the percent divergence of extant copies from the consensus sequence by the species
# neutral substitution rate. Substitution rates (mutations/year) used were as follows: humans: 2.2 × 10− 9; mouse: 4.5 × 10− 9, from [Initial sequencing and comparative analysis of the mouse genome.]. Jukes-Cantor and Kimura distances were
# calculated by aligning each TE to its consensus sequence and counting all possible mutations (see below). Single nucleotide substitution counts were normalized by the length
# of the genomic TE minus the number of insertions (gaps in the consensus). These mutation rates were then used to calculate the Jukes-Cantor and Kimura distances for each genomic TE.

# Hossain, Shammamah. (2019). Visualization of Bioinformatics Data with Dash Bio. 126-133. 10.25080/Majora-7ddc1dd1-012.
# Retrotransposons spread potential cis-regulatory elements during mammary gland evolution.


#figurePlot.update_layout(title_text='Customized Distplot', hovermode='x unified', margin=dict(l=40, r=20, t=30, b=80), legend=dict(orientation='h', yanchor='top', y=-0.13) ),
# mettre howertemplat x-unified partout
