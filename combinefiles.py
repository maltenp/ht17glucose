import os
import numpy as np
import my_func as m
def runscript():
	'''Combines files of a specified file extension into one file'''
	os.path.abspath(__file__)
	fend=input('Specify file extension to combine, eg. ".DAT":\n')
	#fend=".s1p"
	ex=input('Specify unique str/char(s) in unwanted lines, eg. "#,!": \n')
	#ex="!,#"
	name=input('Specify the output name, eg. "out.txt":\n')
	#name="out.txt"
	
	if ex.find(',')!=-1:
		try:	
			exv=ex.split(',')
		except:
			print('ERROR, wrong delimiter, use ","')
			exit()
	else:
		exv=[]
		exv.append(ex)
	print(exv)
	fn1=m.find_file(fend)
	rf=[]
	h=[]
	for i in fn1:
		print('Opening %s'%i)
		r=m.read_file(i,exv)
		h.append(i+'='+str(r.shape))
		rf.append(r)
	h="!"+''.join(h)
	m.print_to_file(rf,fn=name, topheader=h)
	print('Files combined and saved in %s' %name)
	
	return
if __name__ == "__main__":
     runscript()