import os
import sys
def find_file(end1=".DAT"):
	'''Finds the file in the working directory'''
	if end1.rfind("."):	end1=end1+".DAT"
	print('Looking for file ending with: %s in current folder.'%end1)
	fn=[]
	for file in os.listdir():
		if file.endswith(end1):# and len(fn)<len(os.path.join(file)): #if not unique, the longest filename will be opened.
			fn.append(os.path.join(file))
	try:
		fn[0]
	except:
		print('File ending with %s not found' %end1)
		exit()
	return fn
def read_file(fn):
	'''Reads the short output .DAT from qdemow and extracts Q0,Qe,FL,Ke,K'''
	f=open(fn,'r')
	mtrix=[]
	N=[]
	N.append("!")
	c=-1
	row =[]
	for line in f:
		if line.find("PORT 1 DATA FILE")!=-1:
			N.append(line.split(' ')[6]+".s1p")
		if line.find(" Q0 =")!=-1:
			str1=' '.join(line.split())
			row.append(str1.split(" ")[2])
			row.append(str1.split(" ")[4])
			if float(str1.split(" ")[4])/float(str1.split(" ")[2])>0.1:
				print("WARNING, large relative Q error in %s"%N[-1])
			str1.split(" +- ")[1]	
		if line.find(" K = ")!=-1:
			str1=' '.join(line.split())
			row.append(str1.split(" ")[2])
			row.append(str1.split(" ")[4])
			if float(str1.split(" ")[4])/float(str1.split(" ")[2])>0.1:
				print("WARNING, large relative K error in %s"%N[-1])
		if line.find(" FL =")!=-1:
			str1=' '.join(line.split(' '))
			row.append(str1.split(' ')[4])
			# compatible with earlier versions:    
			t=row[2]
			row[2]=row[4]
			row[4]=t
			#end compatible fix
			mtrix.append(row)
			row=[]
				
	return [mtrix, N]
def print_to_txt(lst, fn='output.txt', h=''):
	'''Prints to a file in the local directory'''
	f=open(fn,'a')
	f.write('# Q0 Q0e FL Ke K\n')
	if h!='':
		f.write(' '.join(h)+" \n")
	for i in lst:
		for j in range(0,len(i)):	
			f.write('%s '%i[j])
			if i[j]==i[-1]:
				f.write("\n")
	f.close()
	return
def readout(ar=[]):
	'''Reads .DAT files and saves them to the _filename_r.txt'''
	if len(ar)==0: fn=["OUT.DAT"]
	for i in ar:
		fn=find_file(i)

	for i in fn:
		print('Opening %s'%i)
		[m,N]=read_file(i)
		nfn=i[:-4]+"r.txt"
		print("Writing to: %s"%nfn)
		print_to_txt(m,h=N,fn=nfn)
	
	return
if __name__ == "__main__":
	readout(sys.argv[1:])