import ethcal as e
import metcal as mc
import my_func as mf
import numpy as np
import matplotlib.pyplot as plt
import sys
import pickle
import os
import mymenu
from mpl_toolkits.mplot3d import Axes3D

def dump2pickle(a, pname="out.pickle"):
	#a=[[m,h],[m,h]] etc	
	script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
	rel_path = pname
	abs_file_path = os.path.join(script_dir, rel_path)
	with open(abs_file_path,"wb") as f:
		pickle.dump(a, f)
	return
def readpickle(pname="out.pickle"):
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
	k=False
	if len(s)!=0:
		k=True
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
	[Q_0, f_0]=e.return_f0q0()	
	ep=[]
	for i in range(0,len(df)):
		ep.append(df[i]/f_0/kp[i]+1)
	return ep
def findepp(dq,kpp):
	epp=[]
	for i in range(0,len(dq)):
		epp.append(dq[i]/2/kpp[i])
	return epp
def get_e(dfv,dqv):
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
	try:
		dict={"Q0":m[:,0],"Q0e":m[:,1],"FL":m[:,2],"Ke":m[:,3],"K":m[:,4],"leg":leg,"ss":ss,"dfv":dfv,"dqv":dqv,"ere":ere,"eim":eim}
	except IndexError:
		dict={"Q0":m[:,0],"Q0e":m[:,1],"FL":m[:,2],"leg":leg,"ss":ss,"dfv":dfv,"dqv":dqv,"ere":ere,"eim":eim}
	return dict
def run_a(a):
	#a[3]
	run=[]
	for i in a:
		run.append(run_mh(i))
	return run
def get_mh():
	try:
		fn=mf.find_file("output.txt")
	except:
		inp=input('Specify output file to evaluate: ')
		fn=mf.find_file(inp)	
	for i in fn:
		[m,h]=read_file(fn=i)
	return [m,h]
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

def menu(opt=["-opt"]):
	menu=mymenu.menu()
	menu.defoption('-rw','Rewrite pickle')
	menu.defoption('-a','Append to pickle')
	menu.defoption('-r','read from pickle')	
	menu.defoption('-cplot','Plot a with a custom setup')	
	#menu.defoption('-erg','plot_e_re_glu(s,ere,leg)')
	#menu.defoption('-eig','plot_e_im_glu(s,eim,leg)')
	#menu.defoption('-imre','plot_e_im_vs_ere(eim,ere,leg)')
	#menu.defoption('-e','plot_e(s, ere,eim, leg)')
	#menu.defoption('-vfs','plot_v_fs(s,f_s,leg)')
	#menu.defoption('-gfs','plot_glucose_fs(s,f_s,leg)')
	#menu.defoption('-tune','plot_tune(s,f_s)')
	#menu.defoption('-test','hejhej')
	if opt[0]=="-opt":
		menu.print_menu()
		exit()
	for i in opt:
		menu.option(i)
	runopt(menu)
	return
def plot_any(a):
	qu=False
	c=1

	while qu==False:
		print("Choose what to plot:")
		print("[Q0, Q0e, FL, Ke, K, leg, ss, dfv, dqv, ere, eim]")
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
		for i in run_a(a): # i=dict[Q0, Q0e, FL, Ke, K, leg, ss, dfv, dqv, ere, eim]
				plt.figure(c)
				if ltru:
					plt.plot([i[x]],[i[y]],'*')
					plt.legend(i["leg"])
				elif ztru:
					fig=plt.figure(c)
					ax=fig.add_subplot(111,projection='3d')
					ax.plot_trisurf(i[x],i[y],i[z])
				else:
					plt.plot(i[x],i[y],'*')
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
	return
def runopt(menu):
	boo=[i for i, x in enumerate(menu.boolopt) if x]
	for i in (menu.opts[i] for i in boo):
		if i==menu.opts[0]:
			a=[get_mh()]
			input("Are you sure you want to rewrite pickle? (crtl+c to cancel)")
			dump2pickle(a)
		elif i==menu.opts[1]:
			a=readpickle()
			a.append(get_mh())
			print("Appending pickle")
			dump2pickle(a)
		elif i==menu.opts[2]:
			a=readpickle()
		elif i==menu.opts[3]:
			a=readpickle()
			plot_any(a)
	plt.show()
	return
if __name__ == "__main__":
	#try:
	menu(sys.argv[1:])
	#except IndexError:
	#	print(sys.argv)
	#	menu()