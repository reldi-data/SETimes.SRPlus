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

depinfile = sys.argv[1]

depdata = codecs.open(depinfile, "r", "utf-8")

""" UPOS correction function """
def correct_upos(old, new):
	expr = r'.+'+re.escape(old)+ r'(.+)'
	if re.match(expr, deptable[i][8]):
		msd = re.search(expr, deptable[i][8]).group(1)
		deptable[i][8] = "UposTag="+new+msd

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
				dep = str(deprel[0]) 
				rel = ':'.join(deprel[1:])
#			""" upos corrections """
				if rel =="advmod":                          
					correct_upos('SCONJ','ADV')     # 'advmod' is 'SCONJ', ADP, NOUN, ...
					correct_upos('AUX','ADV')
					correct_upos('PRON','ADV')
					correct_upos('VERB','ADV')				
				if re.match(r'nummod(:gov)?', rel):       #'nummod(:gov)'  should be 'NUM'
					correct_upos('ADJ','NUM')
					correct_upos('ADV','NUM')
					correct_upos('DET','NUM')
				if rel =="det:numgov":                          #'det' is 'ADV'"
					correct_upos('ADV','DET')
				if rel =="det":                    # 'det' is ADJ, PART, CCONJ, X, NUM
					correct_upos('ADJ','DET')
					correct_upos('ADV','DET')				 	
					correct_upos('PART','DET')
					correct_upos('CCONJ','DET')
					correct_upos('X','DET')		
					correct_upos('NUM','DET')
				if rel == "goeswith":					# in hr500k, e.g. "do sada" 
					if re.match(r'.+ADP.+', deptable[i][8]):
						deptable[i][7] = deprel[0]+":"+"case"	
					else: 
						deptable[i][7] = deprel[0]+":"+"amod"
				if rel == "appos":                 # in hr500k mostly wrong rel appos
					if int(dep) >= i:
						deptable[i][7] = deprel[0]+":"+"amod"
				if rel == "flat:foreign":          # in hr500k mostly indeclinable
					if int(dep) >= i:
						deptable[i][7] = deprel[0]+":"+"nmod"
				if rel == "conj":                  # in hr500k coordinated modifiers 
					if int(dep) >= i:
						if re.match(r'.+NUM.+', deptable[i][8]):
							deptable[i][7] = deprel[0]+":"+"nummod"
						else:
							deptable[i][7] = deprel[0]+":"+"amod"
				if rel == "flat":
					correct_upos('PUNCT', 'X')																				
				if rel == "punct":
					if re.match(r'.+AD(V|J).+', deptable[i][8]):
						deptable[i][8] = "UposTag=PUNCT|_"
				if rel == "cop":
					correct_upos('VERB','AUX')
				if rel == "aux":
					correct_upos('VERB','AUX')       
					correct_upos('PRON','AUX')       # one case on hr500 but had to do it
				if rel == "cc":                       # one case on hr500 but had to do it
					correct_upos('DET','CCONJ')
				if rel == "case":                     # one case on hr500 but had to do it
					correct_upos('DET','ADP')
				if rel == "mark":                     # one case on hr500 but had to do it
					correct_upos('PRON','SCONJ')																				
																				
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
		
