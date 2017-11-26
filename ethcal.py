import my_func as mf
import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
def return_f0q0():
	'''Called by other scripts'''
	Q_0 =  4392.1 
	f_0 = 3.00875840E+08
	return [Q_0, f_0]
def return_e0eth():
	'''Return compl. perm. for eth at ~300Mhz'''
	# CONSTANTS FOUND IN PAPER FOR DIFFERENT CONC. OF ETHANOL ~300MHz
	#echar={'0','08','26','47','75','91','96'};
	e_p=[78.3,74.0,65.0,52.5,38.5,32.0,28.0];
	e_pp=[1.19,1.35,2.25,3.4,3.6,4.0,5.7];
	return [e_p, e_pp]
def leg_and_s(h,ustop=-8, start="eth"):
	'''Given filenames of the form _start_XXXyyyy.yyy in the header h, returns the number found in XXX and a legend made of the the name of each filename in the header '''
	ustart=len(start)
	leg=[]
	s=[]
	for i in h:
		j=i.split(' ')
		for k in j:
			if k.find(start)!=-1:
				k=k[0:ustop]
				leg.append(k)
				k=k[ustart:]
				s.append(int(k))
	return [leg, s]
def dump2pickle():
	fn=mf.find_file('ethcal2.txt')
	[m,h]=mf.read_file2(fn[0])
	with open("eth.pickle","wb") as f:
		pickle.dump( [m,h], f)
	return
def readpickle():
	script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
	rel_path = "eth.pickle"
	abs_file_path = os.path.join(script_dir, rel_path)
	[m,h] = pickle.load(open(abs_file_path, "rb"))
	return [m,h]
def sort_ind(s, v1i):
	'''sorts, s and then arrange vXo accordingly'''
	ind=np.argsort(s)
	v1o=[]
	for i in ind:
		v1o.append(v1i[i])
	return v1o
def find_df_dq_kp_kpp(m,s=[]):
	'''Calculates df,dq,kp,kpp from the matrix m'''
	k=False
	if len(s)!=0: k=True
	[Q_0, f_0]=return_f0q0()	
	[e_p, e_pp]=return_e0eth()
	c=0
	dfv=[]
	dqv=[]
	kp=[]
	kpp=[]
	for i in m:
		f_s=i[2]
		q_s=i[0]
		df=(f_0-f_s)
		dq=(1/q_s-1/Q_0)
		K_p = 1/(e_p[c] - 1)*df/f_0;
		K_pp = 1/(2*e_pp[c])*dq;
		dfv.append(float(df))
		dqv.append(float(dq))
		kp.append(float(K_p))
		kpp.append(float(K_pp))
		c+=1
	if k:
		dfv=sort_ind(s,dfv)
		dqv=sort_ind(s,dqv)
		kp=sort_ind(s,kp)
		kpp=sort_ind(s,kpp)
	return [dfv,dqv,kp,kpp]
def lin_fit(x,y):
	'''Returns a vector of the points on a linear fit'''
	p=np.poly1d(np.polyfit(x,y,1))
	px=np.linspace(min(x)*(1-1e-3), max(x)*(1+1e-3), 100)
	py=p(px)
	return [px,py]
def get_k():
	'''returns functions Kpf(df) and Kppf(dq)'''
	[m,h]=readpickle()
	[leg, s]=leg_and_s(h)
	leg=sort_ind(s,leg)
	[dfv,dqv,kp,kpp]=find_df_dq_kp_kpp(m,s)
	Kpf=np.poly1d(np.polyfit(dfv,kp,1))
	Kppf=np.poly1d(np.polyfit(dqv,kpp,1))	
	return [Kpf,Kppf]
def show_cal():
	'''Plots the calibration'''
	[m,h]=readpickle()
	#[ep, epp]=find_e(m #constant k
	[leg, s]=leg_and_s(h)
	#[legs, eps, epps]=sort_ind(s, leg, ep, epp) # constant k.
	[dfv,dqv,kp,kpp]=find_df_dq_kp_kpp(m,s)
	plt.figure(1)
	plt.plot([dfv],[kp],'*')
	plt.xlabel('$\Delta$f [Hz]')
	plt.ylabel("K'")
	plt.title("K'($\Delta$f)")
	plt.legend(sort_ind(s,leg))
	plt.ticklabel_format(style='sci', axis='y', scilimits=(1,3))
	[px,py]=lin_fit(dfv,kp)
	plt.plot(px,py)
	plt.figure(2)
	plt.plot([dqv],[kpp],'*')
	plt.xlabel('1/$\Delta$Q')
	plt.ticklabel_format(style='sci', axis='y', scilimits=(1,3))
	plt.ylabel("K''")
	plt.title("K''(1/$\Delta$Q)")
	plt.legend(sort_ind(s,leg))
	[px,py]=lin_fit(dqv,kpp)
	plt.plot(px,py)
	plt.show()
	return