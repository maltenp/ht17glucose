import numpy as np
import os

def find_file(end1=""):
	'''Finds all files in directory with a specified ending, returns a list of filenames'''
	print('Looking for file ending with: %s in current folder.'%end1)
	fn=[]
	for file in os.listdir(os.getcwd()):
		if file.endswith(end1):
			fn.append(os.path.join(file))
	try:
		fn[0]
	except:
		print('File ending with %s not found' %end1)
		exit()
	return fn
def read_file(fn=".DAT", exv=['!','#']):
	'''Reads from file and returns a numpy array, The user specifies a unique char which is part of the unwanted lines.'''
	f=open(fn,'r')
	N=[]
	c=-1
	for line in f:
		if all(line.find(i) == -1 for i in exv):
			row=line.split()
			row=list(map(np.longfloat,row))
			N.append(np.array(row))
	return np.array(N)
def read_file2(fn=".DAT", exv=['!','#']):
	'''Reads from file and returns a numpy array, The user specifies a unique char which is part of the unwanted lines.'''
	f=open(fn,'r')
	N=[]
	c=-1
	str1=[]
	for line in f:
		if all(line.find(i) == -1 for i in exv):
			row=line.split(' ')
			row=list(map(np.longfloat,row))
			N.append(np.array(row))
		else: str1.append(line)
	return [np.array(N), str1]

def print_to_file(lst, fn='output.txt', topheader='! ', header=''):
	f=open(fn,'w')
	f.write((topheader+"\n"))
	f.close()
	f=open(fn,'a')
	if len(header)>0:
		f.write("#"+' '.join(header)+"\n")
	try:
		for i in lst:
			for k in i:
				for j in range(0,len(k)):	
					f.write('%s '%k[j])
					if k[j]==k[-1]:
						f.write("\n")
	except:
		for i in lst:
				for j in range(0,len(i)):	
					f.write('%s '%i[j])
					if i[j]==i[-1]:
						f.write("\n")		
	f.close()
	return
