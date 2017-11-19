'''
The scipt works on s1p files with _one_ trough.
'''
import os
import numpy as np
from pip._vendor.distlib.compat import raw_input
import numpy as np 
import matplotlib.pyplot as plt
import my_func as mf
import sys
def find_nearest(array,value):
	'''Finds the closest value in an array and returns that array-value'''
	idx = (np.abs(array-value)).argmin()
	return array[idx]
def plot_fig(m,smallv, end1v): #fnp
	c=0
	leg=[]
	for i in m:
		small=smallv[c]
		end1=end1v[c]
		plt.figure(1)
		plt.plot(i[:,0],i[:,1])
		plt.plot(small[:,0],small[:,1],'+')
		#f0=i[i[:,1]==min(i[:,1])]
		#leg.append(fnp[c])
		leg.append(end1)
		c+=1		
	#print('The resonace frequence is:\n%f'%f0[0][0])
	print("SEE PLOT")
	#plt.xlim([f0[0][0]*0.999,f0[0][0]*1.001])
	plt.legend(leg)
	return
def print_file(m,tdb,in1,int1,out1, fnp):
	c=0
	smallv=[]
	end1v=[]
	for i in m:
		try:
			small=makesmall(i, toldb=float(tdb),inner=int(in1),inter=int(int1),outer=int(out1))
			if c<10:
				end1=fnp[c][0:-4]+"0"+str(c)+"n.s1p"
			else: end1=fnp[c][0:-4]+str(c)+"n.s1p"
			print('Saved to %s in current folder.'%end1)
			mf.print_to_file(small,fn=end1, header='', topheader="# Hz S DB R 50")
			smallv.append(small)
			end1v.append(end1)
			c+=1
		except:
			if c<10:
				end1=fnp[c][0:-4]+"0"+str(c)+"nE.s1p"
			else: end1=fnp[c][0:-4]+str(c)+"nE.s1p"
			print('WARNING! EMPTY. Saved to %s in current folder.'%end1)
			mf.print_to_file([[]],fn=end1, header='', topheader="# Hz S DB R 50")
			c+=1		
	return [smallv, end1v]
def makesmall(mtrix,toldb=-0.1,inner=1, inter=4, outer=0):
	'''Returns a smaller matrix from a larger matrix.
	The user specifies the steplenghts in different sections. "inner", "intermediate" and "outer"
	The sections are defined as:
	seq1: from the 1th element to the first element below the tolerance, tol-db
	seq2: from tol-db to mean(trough)
	seq3: from mean to min (trough) value
	seq4: min(trough)
	seq5: from min to mean
	seq6 from mean to tol-db
	seq7 from told-tb to end'''
	c=0
	cv=[]
	db=[]
	cx=range(0,len(mtrix))
	for i in mtrix:
		#print(i)
		try:
			if i[1]<toldb:
				cv.append(c)
				db.append(i[1])
		except:
			return np.array([])
		c+=1
	#print(cv)
	m=np.mean(db)
	minind=np.argmin(db)
	#print(minind)
	m1=find_nearest(db[0:minind],m) #finds the value closest to the mean value
	mind1=db[0:minind].index(m1)+cv[0]
	m2=find_nearest(db[minind:-1], m)
	mind2=db[minind:].index(m2)+cv[0]+minind
	minind=minind+cv[0]
	cv2=np.asarray(range(mind1-1,cx[cv[1]],-inter))
	cv3=np.asarray(range(minind-1,mind1,-inner))
	cv4=np.asarray(minind)
	cv5=np.asarray(range(minind+1, mind2,inner))
	cv6=np.asarray(range(mind2+1, cx[cv[-2]],inter))    
	if outer==0:
		#cv1=np.asarray(range(cx[0],cx[cv[0]],outer))
		#cv7=np.asarray(range(cx[cv[-1]], cx[-1],outer))
		#cvx=np.hstack((cv1,cv2,cv3,cv4,cv5,cv6,cv7))
		cvx=np.hstack((cv2,cv3,cv4,cv5,cv6))
		#print('No of outer steps to the left: %i' %len(cv2))
		#print('No of intermediate steps to the left: %i' %len(cv2))
		#print('No of inner steps to the left: %i' %len(cv3))
		#print('No of inner steps to the right: %i' %len(cv5))
		#print('No of intermediate steps to the right: %i' %len(cv6))
		draw(inter1=len(cv2), inner1=len(cv3), inner2=len(cv5), inter2=len(cv6))
	else:   
		cv1=np.asarray(range(cx[cv[0]],cx[0],-outer))
		cv7=np.asarray(range(cx[cv[-1]], cx[-1],outer))
		cvx=np.hstack((cv1,cv2,cv3,cv4,cv5,cv6,cv7))
		#print('No of outer steps to the left: %i' %len(cv2))
		#print('No of intermediate steps to the left: %i' %len(cv2))
		#print('No of inner steps to the left: %i' %len(cv3))
		#print('No of inner steps to the right: %i' %len(cv5))
		#print('No of intermediate steps to the right: %i' %len(cv6))
		#print('No of outer steps to the right: %i' %len(cv7))
		draw(out1=len(cv1), inter1=len(cv2), inner1=len(cv3), inner2=len(cv5), inter2=len(cv6), out2=len(cv7))
	print('Total number of steps: %i' %len(cvx))
	#mtrix=np.array(mtrix)    
	return mtrix[cvx][:]
def draw(out1=0,inter1=0,inner1=0,inner2=0,inter2=0,out2=0):
	print("______       ______\n%2i  %2i\     /%i  %2i\n       \   /\n      %2i\_/%i\n"%(out1,inter1,inter2,out2,inner1,inner2)) 
	return
def check_interv(iv,fn,m):
	iv=iv.split(":")
	iv=list(map(int,iv))
	if (iv[0]==iv[1] and iv[0]>0):
			iv[0]=iv[0]-1 
	elif iv[1]>iv[0] or iv[1]<0: pass
	else: iv[1]=1
	if len(fn)>1:
		m=m[iv[0]:iv[1]]
		fnp=fn[iv[0]:iv[1]]
	else: fnp=fn    
	return [fnp, m]
def re_matrix(fn):
	m=[]
	for i in fn:
		print('opening: %s'%i)
		array=mf.read_file(i)
		m.append(array)
	return m
def plot_freq_vs_db(m,fnp):
	c=0
	leg=[]
	plt.figure(1)
	for i in m:
		end1=fnp[c][0:-4]
		c+=1
		f=[]
		db=[]
		for j in i:
			f.append(j[0])
			db.append(j[1])
			#print(f)
			#print(db)
		plt.plot(f,db)
		leg.append(end1)
	plt.plot(f,db)
	#plt.legend(['-8mm','-6mm','-4mm','-2mm','0mm'])
	#plt.title('Exposed Volume')
	#plt.xlabel('f_s [Hz]')
	plt.title('Frequency response for empty sample')
	plt.xlabel('Frequency [Hz]')
	plt.ylabel('Gain [dB]')
	return
def plot_freq(m,fnp):
	c=0
	s=[]
	leg=[]
	plt.figure(1)
	for i in m:
		end1=fnp[c][0:-4]
		s.append(int(fnp[c][3:-5]))
		c+=1
		f=[]
		db=[]
		for j in i:
			f.append(j[0])
			#db.append(j[1])
			#print(f)
			#print(db)
		leg.append(end1)
	plt.plot(f)
	plt.legend(leg)
	plt.title('Exposed Volume')
	plt.xlabel('Frequency [Hz]')
	plt.ylabel('Gain [dB]')
	return
def runscript(opt=["-opt"]):
	if opt[0]=="-opt":
		print('Options:')
		print('-q: Quick run, all 1.s1p files tbd="-0.1", in1="25", int1="50", out1="0"')
		print('-qn: Quick run, all N.s1p files tbd="-0.1", in1="25", int1="50", out1="0"')
		print('-f: Custom setup')
		print('-p: plot, only works together with -q, -qn and -f (before -p)\n')
		print('-fdb: plots the frequency respons vs db')
		print('-pf: plot fs vs conc')
#		print('-gfs: plot_glucose_fs(s,f_s,leg)\n')
#		print('-pt: plot_tune(s,f_s)\n')
		exit()
#	os.path.abspath(__file__)
	#end1=raw_input('Enter unique last few characters of the file you want to open\n(etc. xxx.s1p)\n')
	#if len(fn)>1:
		#iv=raw_input('Opening %s.\nChoose interval, eg. 2:-1:\n'%fn)
		#iv="0:23"
	#else: iv="0:0"
	#[fnp, m]=check_interv(iv,fn,m)
	for i in opt:
		if i=="-q":
			end1="1"
			fn=mf.find_file(end1+".s1p")
			m=re_matrix(fn)
			tdb="-0.1"
			in1="25"
			int1="50"
			out1="0"
			[smallv, end1v]=print_file(m,tdb,in1,int1,out1,fn)
		elif i=="-qn":
			end1=raw_input('Enter the last, digit/character before file extension, (etc: N.s1p)\n')
			fn=mf.find_file(end1+".s1p")
			m=re_matrix(fn)
			tdb="-0.1"
			in1="25"
			int1="50"
			out1="0"
			[smallv, end1v]=print_file(m,tdb,in1,int1,out1,fn)
		elif i=="-f":
			end1=raw_input('Enter the last, digit(s)/character(s) before file extension, (etc: yyyyyXXX.s1p)\n')
			fn=mf.find_file(end1+".s1p")
			m=re_matrix(fn)			
			tdb=raw_input('Enter the tol-db:\n')
			in1=raw_input('Enter the inner step length\n(beween min and mean(trough):\n')
			int1=raw_input('Enter the intermediate step length\n(beween tol-db and mean(trough):\n')
			out1=raw_input('Enter the outer step length:\n')
			[smallv, end1v]=print_file(m,tdb,in1,int1,out1,fn)
		elif i=="-p":
			try:
				plot_fig(m, smallv, end1v)
			except UnboundLocalError:
				print('ERROR, this option has to be used together with one of the above, (-q,qn,f-)')
				exit()
		elif i=="-fdb":
			end1=raw_input('Enter the last, digit(s)/character(s) before file extension, (etc: yyyyyXXX.s1p)\n')
			fn=mf.find_file(end1+".s1p")
			m=re_matrix(fn)			
			plot_freq_vs_db(m,fn)
		elif i=="-pf":
			end1=raw_input('Enter the last, digit(s)/character(s) before file extension, (etc: yyyyyXXX.s1p)\n')
			fn=mf.find_file(end1+".s1p")
			m=re_matrix(fn)
			plot_freq(m,fn)
#		elif i=="-tune":
#			plot_tune(s,f_s,leg)
		else: pass	 
	plt.show()

	return
if __name__ == "__main__":
	try:
		runscript(sys.argv[1:])
	except IndexError:
		print(sys.argv)
		runscript()