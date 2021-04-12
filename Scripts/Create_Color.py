#!/usr/bin/python3
import os
import sys



#								rouge		blue		green		All		V2
			
#DNA Transposon			DNA Transposon			#C2938D		#E1EBEE		#DFFF00		#B284BE		Chartreuse	#7FFF00
#EnSpm/CACTA			DNA Transposon			#B53389		#B9D9EB		#00A693		#9966CC		LimeGreen	#32CD32
#Merlin				DNA Transposon			#614051		#89CFF0		#E4D00A		#8A2BE2		LightGreen	#90EE90
#MuDR Transposon		DNA Transposon			#CC33CC		#318CE7		#FFEFD5		#7851A9		MediumSeaGreen	#3CB371
#Tc1/Mariner			DNA Transposon			#DA70D6		#3F00FF		#DDD06A		#9683EC		ForestGreen	#228B22

#Crypton			DNA Transposon |||		#F19CBB		#9EB9D4		#AAF0D1		#CF71AF		DarkGreen	#006400
#Helitron			DNA Transposon |||		#FFA6C9		#B2CDEB		#7FFFD4		#DA70D6		OliveDrab	#6B8E23
#Polinton			DNA Transposon |||		#FFDAE9		#72A0C1		#29AB87		#800080		Olive		#808000

#BEL				LTR retrotransposon		#FF4500		#B2FFFF		#317873		#89CFF0		LightCyan	#E0FFFF
#Copia				LTR retrotransposon		#FAD6A5		#E6FFFF 	#00FF00		#00BFFF		PaleTurquoise	#AFEEEE
#DIRS				LTR retrotransposon		#FA8072		#CCE6E6 	#177245		#1E90FF		Turquoise	#40E0D0
#ERV				LTR retrotransposon		#FBCEB1		#AAF0D1		#4A5D23		#0000FF		SteelBlue	#4682B4
#Gypsy				LTR retrotransposon		#FF7518		#00CCCE		#808000		#1C39BB		PowderBlue	#B0E0E6
#LTR Retrotransposon		LTR retrotransposon		#BF5700		#008B8E		#D0F0C0		#000080		LightSkyBlue	#87CEFA
#CR1				Non-LTR retrotransposons	#E97451		#6F2DA8		#E3F988		#E3FF00		DodgerBlue	#1E90FF
#L1				Non-LTR retrotransposons	#FFC800		#B284BE		#00CCCC		#ADFF2F		CornflowerBlue	#6495ED
#Non-LTR retrotransposon	Non-LTR retrotransposons	#D2B48C		#9966CC		#A7FC00		#8DB600		Blue		#0000FF
#R2				Non-LTR retrotransposons	#674C47		#B57EDC		#4D5D53		#568203		Navy		#000080
#RTE				Non-LTR retrotransposons	#E0AB76		#8A2BE2		#4FFFB0		#03C03C		DarkSlateBlue	#483D8B
#SINE				Non-LTR retrotransposons	#800020		#7851A9		#228B22		#4A5D23		Indigo		#4B0082	

#(Micro)Satelitte		Unclassified TE			#DE3163		#1034A6		#F0FFF0		#FF004F		Gold		#FFD700		
#Unclassified TE		Unclassified TE			#C04000		#00008B		#F5F5DC		#DC143C		Light orange	#FED8B1		
#OtherTE							#EE82EE		#40E0D0		#66CDAA		#DAA520		Lemon Chiffon	#FFFACD		
			
#Gene								#8DB600		#FFBF00		#FE28A2		#F8DE7E		Crimson		#DC143C
#Pseudo								#00A550		#B8860B		#DE3163		#E0AB76		LightCoral	#F08080
#ncRNA								#568203		#FBCEB1		#FF3800		#B8860B		DarkOrange	#FF8C00
#Intergenic							#ACE1AF		#D1E231		#FF7518		#FFFACD		PeachPuff	#FFDAB9


#MyTE 1								#FF0800		#0000FF		#50C878		#0D98BA		BlueViolet	#8A2BE2
#MyTE 2																Orchid		#DA70D6
#MyTE 3																Mardi Gras	#880085


########################################################################################################################
###	Create Table for the piechart of OverRepresented
########################################################################################################################

def PrepareListeColor(pathVisual):

	temp = pathVisual + '/Functions/Couleur.py'
	f = open(temp, "w")

	f.write("#!/usr/bin/env python3\n")
	f.write("# -*- coding: utf-8 -*-\n\n")

	# table des couleurs a choisir
	f.write("couleurV3 = ['chartreuse', 'limegreen', 'lightgreen', 'mediumseagreen', 'forestgreen', 'darkgreen', 'olivedrab', 'olive',    'lightcyan', 'turquoise', 'steelblue', 'powderblue', 'lightskyblue', 'dodgerblue', 'cornflowerblue', 'blue', 'navy', 'darkslateblue', 'indigo', 'gold', 'orange', 'lemonchiffon', 'crimson', 'lightcoral', 'darkorange', 'peachpuff'] \n")
	f.write("couleurV2 = ['#7FFF00', '#32CD32', '#90EE90', '#3CB371', '#228B22', '#006400', '#6B8E23', '#808000', '#E0FFFF', '#AFEEEE', '#40E0D0', '#4682B4', '#B0E0E6', '#87CEFA', '#1E90FF', '#6495ED', '#0000FF', '#000080', '#483D8B', '#4B0082', '#FFD700', '#FED8B1', '#FFFACD', '#DC143C', '#F08080', '#FF8C00', '#FFDAB9'] \n")
	f.write("ListeObject = ['DNA Transposon', 'EnSpm/CACTA', 'Merlin', 'MuDR Transposon', 'Tc1/Mariner', 'Crypton', 'Helitron', 'Polinton', 'BEL', 'Copia', 'DIRS', 'ERV', 'Gypsy', 'LTR Retrotransposon', 'CR1', 'L1', 'Non-LTR retrotransposon', 'R2', 'RTE', 'SINE', '(Micro)Satelitte', 'Unclassified TE', 'OtherTE', 'Gene', 'Pseudo', 'ncRNA', 'Intergenic'] \n\n")  
	f.write("ListeCouleurPossible = ['#000080', '#00008B', '#0000FF', '#008B8E', '#00A550', '#00A693', '#00BFFF', '#00CCCC', '#00CCCE', '#00FF00', '#03C03C', '#0D98BA', '#1034A6', '#177245', '#1C39BB', '#1E90FF', '#228B22', '#29AB87', '#317873', '#318CE7', '#3F00FF', '#4A5D23', '#4D5D53', '#4FFFB0', '#50C878', '#568203', '#614051', '#674C47', '#6F2DA8', '#72A0C1', '#7851A9', '#7FFFD4', '#800020', '#800080', '#808000', '#89CFF0', '#8A2BE2', '#8DB600', '#9683EC', '#9966CC', '#9EB9D4', '#A7FC00', '#AAF0D1', '#ACE1AF', '#ADFF2F', '#B284BE', '#B2CDEB', '#B2FFFF', '#B53389', '#B57EDC', '#B8860B', '#B9D9EB', '#BF5700', '#C04000', '#C2938D', '#CC33CC', '#CCE6E6 ', '#CF71AF', '#D0F0C0', '#D1E231', '#D2B48C', '#DA70D6', '#DC143C', '#DDD06A', '#DE3163', '#DFFF00', '#E0AB76', '#E1EBEE', '#E3F988', '#E3FF00', '#E4D00A', '#E6FFFF ', '#E97451', '#F0FFF0', '#F19CBB', '#F5F5DC', '#F8DE7E', '#FA8072', '#FAD6A5', '#FBCEB1', '#FE28A2', '#FF004F', '#FF0800', '#FF3800', '#FF4500', '#FF7518', '#FFA6C9', '#FFBF00', '#FFC800', '#FFDAE9', '#FFEFD5', '#FFFACD'] \n\n")    

	f.write("couleurSelectTE = ['#8A2BE2', '#E0B0FF', '#B284BE'] ")

	#f.write("couleurRouge = ['#FF0800', '#C2938D', '#B53389', '#614051', '#CC33CC', '#DA70D6', '#F19CBB', '#FFA6C9', '#FFDAE9', '#FF4500', '#FAD6A5', '#FA8072', '#FBCEB1', '#FF7518', '#BF5700', '#E97451', '#FFC800', '#D2B48C', '#674C47', '#E0AB76', '#800020', '#DE3163', '#C04000', '#EE82EE', '#8DB600', '#00A550', '#568203', '#ACE1AF'] \n\n")   
	#f.write("couleurBleu  = ['#0000FF', '#E1EBEE', '#B9D9EB', '#89CFF0', '#318CE7', '#3F00FF', '#9EB9D4', '#B2CDEB', '#72A0C1', '#177245', '#E6FFFF', '#CCE6E6', '#AAF0D1', '#00CCCE', '#008B8E', '#6F2DA8', '#B284BE', '#9966CC', '#B57EDC', '#8A2BE2', '#7851A9', '#1034A6', '#00008B', '#40E0D0', '#FFBF00', '#B8860B', '#FBCEB1', '#D1E231'] \n\n")     
	#f.write("couleurVert  = ['#50C878', '#DFFF00', '#00A693', '#E4D00A', '#FFEFD5', '#DDD06A', '#AAF0D1', '#7FFFD4', '#29AB87', '#317873', '#00FF00', '#177245', '#4A5D23', '#808000', '#D0F0C0', '#E3F988', '#00CCCC', '#A7FC00', '#4D5D53', '#4FFFB0', '#228B22', '#F0FFF0', '#F5F5DC', '#008000', '#FE28A2', '#DE3163', '#FF3800', '#FF7518'] \n\n")   
	#f.write("couleurAll   = ['#0D98BA', '#B284BE', '#9966CC', '#8A2BE2', '#7851A9', '#9683EC', '#CF71AF', '#DA70D6', '#800080', '#89CFF0', '#00BFFF', '#1E90FF', '#0000FF', '#1C39BB', '#000080', '#E3FF00', '#ADFF2F', '#8DB600', '#568203', '#03C03C', '#4A5D23', '#FF004F', '#DC143C', '#DAA520', '#F8DE7E', '#E0AB76', '#B8860B', '#FFFACD'] \n\n")   
	
	f.close()

	#all = [22]


