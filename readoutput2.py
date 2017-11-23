import os
def find_file(end1=""):
	end1=end1+".DAT"
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
		
def read_file2(fn):
	f=open(fn,'r')
	mtrix=[]
	N=[]
	N.append("!")
	c=-1
	for line in f:
		try:
			name=line.split("PORT 1 DATA FILE")
			str1=name[1].split()[1]+name[1].split()[2]
			print("Evaluating: %s"%str1)
			N.append(str1)
			mtrix.append('')
			c+=1
		except:
			pass
		try:
			q=line.split("Q0 =")
			str1=' '.join(q[1].split())
			print("Q0= %s"%str1)
			Q=str1.split(" +- ")[0]
			Qe=str1.split(" +- ")[1]
		except:
			pass
		try:
			fl=line.split("FL =")
			str1=' '.join(fl[1].split())
			print("FL= %s"%str1)
			FL=str1.split()[0]
			mtrix[c]=(Q,Qe,FL)
		except:
			pass
	mtrix.insert(0,N)
	return mtrix
def read_file3(fn):
	f=open(fn,'r')
	mtrix=[]
	N=[]
	N.append("!")
	c=-1
	row =[]
	for line in f:
		if line.find("PORT 1 DATA FILE")!=-1:
			N.append(line.split(' ')[6])
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
	f=open(fn,'a')
	f.write('# Q0 Q0e FL Ke K\n')
	if h!='':
		f.write(' '.join(h))
	for i in lst:
		for j in range(0,len(i)):	
			f.write('%s '%i[j])
			if i[j]==i[-1]:
				f.write("\n")
	f.close()
	return
def main():
	fn=find_file()
	rf=[]
	leg=[]
	#read_file3(fn)
	for i in fn: #only neccesary if you have multiple .DAT files.
		print('Opening %s'%i)
		[m,N]=read_file3(i)
		rf.append(m)
		#leg.append(N)
		#print(rf)
	
	print_to_txt(rf[0],h=N) #only one .DAT
	
	return
main()	