import ethcal as e
import metcal as mc
import my_func as mf
import numpy as np
import matplotlib.pyplot as plt
import sys
import pickle
import os
import mymenu
import scipy as sp
from scipy.interpolate import interp1d
from mpl_toolkits.mplot3d import Axes3D
global spl, col
spl=['+','o','*','.','x','s','d','^','v','>','<','p','h']
col=['b','r','g','c','m','y','k']

def dump2pickle(a, pname="out.pickle"):
	'''Creates a pickle in the directory of the script'''
	#a=[[m,h],[m,h]] etc	
	script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
	rel_path = pname
	abs_file_path = os.path.join(script_dir, rel_path)
	with open(abs_file_path,"wb") as f:
		pickle.dump(a, f)
	return
def readpickle(pname="out.pickle"):
	'''Reads a pickle in the directory of the script'''
	script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
	rel_path = pname
	abs_file_path = os.path.join(script_dir, rel_path)
	try:
		a= pickle.load(open(abs_file_path, "rb"))
	except FileNotFoundError:
		print("Couldnt find pickle")
		exit()
	return a
def get_df_dq(m,s=''):
	'''Calculates the dq and df from the matrix m and sorts it in s (the XXXX in (yyyXXXXyyy.yyy)'''
	k=False
	if len(s)!=0: k=True
	[Q_0, f_0]=e.return_f0q0()	
	dfv=[]
	dqv=[]
	for i in m:
		f_s=i[2]
		q_s=i[0]
		df=(f_0-f_s)
		dq=(1/q_s-1/Q_0)
		dfv.append(float(df))
		dqv.append(float(dq))
	if k:
		dfv=e.sort_ind(s,dfv)
		dqv=e.sort_ind(s,dqv)
	return [dfv,dqv]
def findep(df,kp):
	'''Calculate the real part of the complex permittivity'''
	[Q_0, f_0]=e.return_f0q0()	
	ep=[]
	for i in range(0,len(df)):
		ep.append(df[i]/f_0/kp[i]+1)
	return ep
def findepp(dq,kpp):
	'''Calculate the imaginary part of the complex permittivity'''
	epp=[]
	for i in range(0,len(dq)):
		epp.append(dq[i]/2/kpp[i])
	return epp
def get_e(dfv,dqv):
	'''Returns the complex permittivity found from the matrix m'''
	[Kpf,Kppf]=e.get_k()
	[Kpfm,Kppfm]=mc.get_k()
	kp=[]
	kpp=[]
	for i in range(0,len(dfv)):
		kp.append(np.mean([Kpf(dfv[i]),Kpfm(dfv[i])]))
		kpp.append(np.mean([Kppf(dqv[i]),Kppfm(dqv[i])]))
		#kp.append(Kpf(dfv[i]))
		#kpp.append(Kppf(dqv[i]))
		#kp.append(Kpfm(dfv[i]))
		#kpp.append(Kppfm(dqv[i]))
	ere=findep(dfv,kp)
	eim=findepp(dqv,kpp)
	return	[ere, eim]
def run_mh(mh):
	'''Evaluates the matrix m and the header h and returns a dict'''
	m=mh[0]
	h=mh[1]
	for i in h:
		if i.find('!')!=-1:
			stn=i[2:5]
			break
	[leg, s]=e.leg_and_s(h,start=stn)
	
	leg=e.sort_ind(s,leg)
	ss=np.sort(s)
	#print('%s will be sorted'%s)
	[dfv,dqv]=get_df_dq(m,s)
	[ere, eim]=get_e(dfv,dqv)
	Q0=m[:,0]
	Q0e=m[:,1]
	FL=m[:,2]
	try:
		Ke=m[:,3]
		K=m[:,4]
		#dict={"Q0":m[:,0],"Q0e":m[:,1],"FL":m[:,2],"Ke":m[:,3],"K":m[:,4],"leg":leg,"ss":ss,"dfv":dfv,"dqv":dqv,"ere":ere,"eim":eim}
	except IndexError:pass
	del stn,s,i,h,m,mh #remove copies and unncessesary items in the dict
	return locals()
def run_a(a):
	'''returns a vector of runs (dicts)'''
	run=[]
	for i in a:
		run.append(run_mh(i))
	return run
def remove_from_pickle(a):
	c=0
	for i in a:
		print("[%i] : %s "%(c,i[2]))
		c+=1
	inp=input("which ones do you want to remove? (etc: '0,1,..')\n")
	try:
		inpv=inp.split(",")
		for i in inpv:
			a.pop(int(i))
	except:
		print("Wrong input")
		exit()
	return a
def sort_a(a):
	c=0
	for i in a:
		print("[%i] : %s "%(c,i[2]))
		c+=1
	inp=input("How do you want to sort the pickle?(etc: '3,0,2,1,..')\n")
	try:
		inpv=inp.split(",")
		inpv=list(map(int,inpv))
		new=[]
		for i in inpv:
			new.append(a[i])
	except:
		print("Wrong input")
		exit()
	return new
def get_mh(fn='output.txt'):
	try:
		fn=mf.find_file(fn)
	except:
		inp=input('Specify output file to evaluate: ')
		fn=mf.find_file(inp)	
	for i in fn:
		[m,h]=read_file(fn=i)
		fname=i
		print(i)
	return [m,h,fname]
def save_all_mh():
	try:
		fn=mf.find_file(".txt")
	except:
		inp=input('No .txt files in current directory:')
		exit()
	a=[]
	for i in fn:
		print("Opening file %s"%i)
		[m,h]=read_file(fn=i)
		a.append([m,h,i])
	return a
def read_file(fn=".txt", exv=['!','#']):
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
def print_any(a):
	print("Choose what to print:")
	#print("[Q0, Q0e, FL, Ke, K, leg, ss, dfv, dqv, ere, eim]")
	print(run_mh(a[0]).keys())
	inp1=input("What would you like to print/save? 'a,{b,c,..}', {}:optional\n")
	try:
		inpv=inp1.split(",")
	except:
		print("Wrong input")
		exit()
	data=[]
	c=0
	for i in run_a(a): # i=dict[Q0, Q0e, FL, Ke, K, leg, ss, dfv, dqv, ere, eim]
		row=[]
		c+=1
		for k in inpv:
			row={k:i[k]}
			#print(row)
			#print(row)
			data.append(row)
	print("data saved")
	#for i in data:
	#	print(i.get('ss'))
	return data
def plot_any(a):
	'''Plot anything everything within one run.'''
	qu=False
	c=1

	while qu==False:
		print("Choose what to plot:")
		#print("[Q0, Q0e, FL, Ke, K, leg, ss, dfv, dqv, ere, eim]")
		print(run_mh(a[0]).keys())
		ltru=False
		ztru=False
		inp1=input("What would you like to plot? 'X,Y,{Z,leg}', {}:optional\n")
		try:
			x=inp1.split(",")[0]
			y=inp1.split(",")[1]
		except: 
			print("Wrong input")
			exit()
		try:
			z=inp1.split(",")[2]
			if z=="leg":
				ltru=True
			else:
				ztru=True
		except: pass
		plt.figure(c)
		sc=0
		cc=0
		for i in run_a(a): # i=dict[Q0, Q0e, FL, Ke, K, leg, ss, dfv, dqv, ere, eim]
			plt.figure(c)
			if ltru:
				plt.plot([i[x]],[i[y]],spl[sc])
				plt.legend(i["leg"])
			elif ztru:
				fig=plt.figure(c)
				ax=fig.add_subplot(111,projection='3d')
				ax.scatter(i[x],i[y],i[z])
			else:			
				x1=i[x]
				y1=i[y]
				points = zip(x1, y1)
				points = sorted(points, key=lambda point: point[0])
				x1, y1 = zip(*points)
				new_length = 200
				new_x = np.linspace(min(x1), max(x1), new_length)
				new_y = sp.interpolate.interp1d(x1, y1, kind='cubic')(new_x)
				plt.plot(x1,y1,(spl[sc]+col[cc]))
				plt.plot(new_x,new_y,col[cc],label='_nolegend_')

			sc+=1
			cc+=1
			if sc==len(spl):
				sc=0
			if cc==len(col):
				cc=0
		c+=1
		qin=input("Press enter to plot again('any_key+enter' to exit)")
		if qin!='':
			qu=True
	for i in range(1,c):
		print("Figure: %i" %i)
		plt.figure(i)
		t=input("Enter title:")
		xl=input("Enter xlabel:")
		yl=input("Enter ylabel:")
		if ztru:
			zl=input("Enter zlabel:")
			ax.set_zlabel(zl)
		plt.title(t)
		plt.xlabel(xl)
		plt.ylabel(yl)
		print("The order plotted are the same as the appended pickle order.")
		print("The following files were used to make the plot(s)\n")
		for i in a:
			print(i[2])
		cl=input("\nDo you want to make a custom legend? ('leg1,leg2,leg3'  etc.)\n")
		if cl!='':
			try:
				cleg=cl.split(",")
				plt.legend(cleg)
			except:
				print("Wrong input")

	return
def custom_plot(a):
	sc=0
	cc=0
	'''Not yet complete, will be used to plot vs different runs'''
	sbool=False
	temp=run_mh(a[0])
	print(temp.keys())
	#print("Data length : %s" %len(temp['ss']))
	#print("Pickle length: %s" %len(a))
	for i in a:
		print(i[2])
	inpu=input('Specify the vector you want to plot againts (~foldername?)\nThe order should be the pickle order shown above\n(etc: 11,222,3333)\n')
	inp=input("what do you want to plot? 'y'\n")
	try:
		inpv2=inpu.split(",")
		xx=list(map(int,inpv2))
	except:
		print("Wrong input")
		exit()
	yy=[]
	for i in a:
		d=run_mh(i)
		y=d.get(inp)
		try:
			len(y)
			yy.append(y)
		except TypeError:
			pass
	
	plt.plot(xx,yy)
	plt.legend(temp['leg'])
	return
def runopt(menu):
	'''The function defines the content of each menu item, the order is the same as the when the the menu was created.'''	
	if menu.boolopt[0]: #0th menu item
		a=[get_mh()]
		input("Are you sure you want to rewrite pickle? (crtl+c to cancel)")
		dump2pickle(a)
		print("%s saved to pickle"%a[0][2])
	elif menu.boolopt[1]: #1th menu item.. etc
		a=readpickle()
		a.append(get_mh())
		print("Appending pickle")
		dump2pickle(a)
	elif menu.boolopt[2]:
		a=readpickle()
		b=save_all_mh()
		for i in b:
			a.append(i)
		print("Saving to pickle")
		dump2pickle(a)
	elif menu.boolopt[3]:
		a=readpickle()
		a=remove_from_pickle(a)
		dump2pickle(a)
		
	elif menu.boolopt[4]:
		a=readpickle()
		for i in a:
			print(i[2])
	elif menu.boolopt[5]:
		a=readpickle()
		plot_any(a)
		plt.show()
	elif menu.boolopt[6]:
		a=readpickle()
		data=print_any(a)
		print(data)
	elif menu.boolopt[7]:
		a=readpickle()
		custom_plot(a)
		plt.show()
	elif menu.boolopt[8]:
		a=readpickle()
		a=sort_a(a)
		print("\nRearranging pickle:\n")
		for i in a:
			print(i[2])
		dump2pickle(a)
		print("\nExiting")
	return

def gotomenu(opt=["-opt"]):
	'''Creates a menu of input arguments'''
	menu=mymenu.menu()
	menu.defoption('-rw','Rewrite pickle') # 0th menu item
	menu.defoption('-a','Append to pickle') # 1th menu item... etc.
	menu.defoption('-aa','Append all .txt files in the folder to pickle')
	menu.defoption('-rm','Remove element in pickle')	
	menu.defoption('-c','Check whats in the pickle')	
	menu.defoption('-cplot','Plot with a custom setup')	
	menu.defoption('-print','Print values')
	menu.defoption('-plcustom','Plot custom')
	menu.defoption('-sorta','sort a by manually specifying the order')
	#menu.defoption('-vfs','plot_v_fs(s,f_s,leg)')
	#menu.defoption('-gfs','plot_glucose_fs(s,f_s,leg)')
	#menu.defoption('-tune','plot_tune(s,f_s)')
	#menu.defoption('-test','hejhej')
	for i in opt:
		menu.option(i)
	if not any(menu.boolopt):
		print("Wrong or no input arguments given")
		print(opt)
		menu.print_menu()
		exit()		
	runopt(menu)
	return
if __name__ == "__main__":
	gotomenu(sys.argv[1:])