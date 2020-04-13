# !/usr/bin/python
# -*- coding: utf8 -*-

# usage: e.g.  python v2.4correct.py set.sr.plus.conll replacements.txt > temp.txt
# assumes "original" conll file format 
# print might need to be adjusted for running with python3


import re
import codecs
import sys

deptable = []
dep_replace = {}
rel_replace = {}

corrinfile = sys.argv[2]
depinfile = sys.argv[1]

corrections = codecs.open(corrinfile, "r", "utf-8")
depdata = codecs.open(depinfile, "r", "utf-8")

""" Import specific corrections from a file """
for line in corrections:						#read the list of replacements from a file 
	items = line.split()
	if items[0] == "rel":                        # e.g. replacements.txt
		rel_replace[(items[1],items[2])] = items[3]
	else:
		dep_replace[(items[1],items[2])] = items[3]

""" MAIN """
for line in depdata:							#read the file to be corrected
	line = re.sub(r'\n', '', line)					# instead of chomp in Perl				
	
#	"""if the input line is empty, process and delete the table"""  #triple quotes don't work within a block
	if len(line) == 0:
		metalines = 0
		for i in range(len(deptable)):		
			if 	deptable[i][0][0] == "#":         # extract metadata
				metalines += 1
				metadata = deptable[i][0].split()	
				if metadata[1] == "sent_id":
					sent_ID = metadata[3]
				print deptable[i][0].encode("utf-8")                  #print metadata
			else:
				line = "" 
				word_ID = str(i - metalines + 1) # for sentID and text that precede the table
				deprel = deptable[i][7].split(":") 
#			""" general deprel replacements"""				
				if deprel[1] =="advmod":                          
					if re.match(r'.+ADP.+', deptable[i][8]):  
						deprel[1] = "case"
					if re.match(r'.+NOUN.+', deptable[i][8]):  
						deprel[1] = "nmod"
				if deprel[1] == "mark":                      #'mark' should not be 'PRON'
					if re.match(r'.+(PRON|DET).+', deptable[i][8]):  
						deprel[1] = "nsubj"
				if deprel[1] == 'aux':                        # 'aux' is 'PRON'
					if re.match(r'.+PRON.+', deptable[i][8]):						             
						deprel[1] = 'expl'
					if re.match(r'.+PART.+', deptable[i][8]):						             
						deprel[1] = 'discourse'
				if len(deprel) > 2:								
					if deprel[2] == "pass":				# in HR, not needed, often wrong
						del deprel[2]
					if deprel[2] == "pv":
						del deprel[2]
				if deprel[1] == 'compound':               # make reflexive expl in SR
					deprel[1] = 'expl'			
#			""" deprel replacements from an external file"""
				if (sent_ID, word_ID) in dep_replace:   #e.g. punct-causes-nonproj 
					deprel[0] = dep_replace[(sent_ID, word_ID)]
				if (sent_ID, word_ID) in rel_replace:
					deprel[1] = rel_replace[(sent_ID, word_ID)]
				deptable[i][7] = ":".join(deprel)
#			""" concatenate and print the result without the last tab """
				for j in range(len(deptable[i])):
					line = line + deptable[i][j]+"\t"
				line = line[:-1]    # remove the last tab				
				print line.encode("utf-8")					
		print												
		deptable = []
	
#	""" for all the other lines, store the input into a table"""	
	else:
		lineitems = line.split("\t")
		deptable.append(lineitems)
		
