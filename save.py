#!/usr/bin/python

import json

def linesJson(filename):
  f = open(filename,"r")
  linenumber = sum(1 for line in f)
  f.close()
  return linenumber

def saveJson(filename, entries, begin=0, nval=1):
	print ("[saveJson] filename: %s" % filename)
	print ("[saveJson] entries:")
	print (entries)
	length=len(entries)
	print ("[saveJson] number of entries: %d" % length)
	if length < 1:
		print ("[saveJson] ERROR no entries")
		return
	if not filename.endswith(".json"):
		print ("[saveJson] ERROR only .json files are supported")
		return
	of=open(filename,"r")
	#if (of < 0):
	#	print ("[saveJson] ERROR no file %s" % filename)
	#	return
	filelen=linesJson(filename)
	print ("[saveJson] number lines: %d" % filelen)

	# read header ...
	headerlen=1
	line=of.readline()
	while line.find("[") is -1:
		line=of.readline()
		headerlen+=1
	print ("[saveJson] headerlen: %d" % headerlen)

	# read values ...
	valuelen=0
	jsonstr=""
	line=of.readline()
#	jsonstr+=line.lstrip()
	while line.find("}\n") is -1:
		line=of.readline()
		jsonstr+=line.lstrip()
		valuelen+=1

	print ("[saveJson] json first value string:\n\n %s" % jsonstr)
	# with the the { and }, a value contains valulen + 2 lines
	valuelen+=2
	print ("[saveJson] valuelen: %d" % valuelen)

	# now we have to read all lines until begin (=first changed value)
	begin_of_change=headerlen+begin*valuelen
	end_of_change=begin_of_change+nval*valuelen
	print ("[saveJson] begin: %d" % begin_of_change)
	print ("[saveJson] end: %d" % end_of_change)
	length_of_change=nval*valuelen
	print ("[saveJson] changed: %d" % length_of_change)

	# go back to beginning of source file
	of.seek(0)

	# and write the lines until begin 
	# to newfile because they are unchanged ...

	newfile=filename.replace(".json",".new")
	print ("[saveJson] newfile: %s" % newfile)
	nf=open(newfile,"w")
	
	done=0
	line=of.readline()
	while done < begin_of_change:
		nf.write(line)
		line=of.readline()
		done+=1
	print ("[saveJson] done: %d" % done)

	# now we write the changed values instead of the original ones ...
	i=0
	while i < nval:
		of.readline()
		nf.write("		{\n")	
		ll=valuelen-3 
		j=0
		while j < ll:
			of.readline()
			nf.write("			{%s},\n" % entries[i][j])
			j+=1
			done+=1
		of.readline()
		nf.write("			{%s}\n" % entries[i][j])	
		i+=1
		line=of.readline()
		if done > filelen-2-valuelen: #  could be last value ...
			nf.write("		}\n")	
		else:
			nf.write("		},\n")	
		done+=3
	print ("[saveJson] done: %d" % done)
	print ("[saveJson] end: %d" %  end_of_change)

	#now we write the unchanged rest ...
	while line:
		nf.write(line)
		line=of.readline()
		done+=1
	print ("[saveJson] done: %d" % done)

	of.close()
	nf.close()

if __name__ == "__main__":
	changed=[]
	changed.append(("aaaa","aaaa","aaaa","aaaa","aaaa","aaaa"))
	changed.append(("bbbb","bbbb","bbbb","bbbb","bbbb","bbbb"))
	changed.append(("cccc","cccc","cccc","cccc","cccc","cccc"))
	saveJson("data.json",changed,2,1)

