import my_func as mf
import numpy as np
import matplotlib.pyplot as plt
import os
import ethcal as e
import pickle
'''finds and sorts on numbers YY the name of the input if input is named xxxYYxxxxxxxx, etc: eth88abcd.s1p'''
def leg_and_s(h, ustart=3,ustop=-8, start="met"):
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
	fn=mf.find_file('metcal2.txt')
	[m,h]=mf.read_file2(fn[0])
	with open("met.pickle","wb") as f:
		pickle.dump( [m,h], f)
	return
def readpickle():
	script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
	rel_path = "met.pickle"
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
	k=False
	if len(s)!=0:
		k=True
	[Q_0, f_0]=e.return_f0q0()
	#echar={'00''10','28','55','75','88','100'};
	e_p=[78.3,79.0,68.5,57.8,49.8,41.8,35.9];
	e_pp=[1.19,2.1,1.6,1.4,2.15,2.5,2.75];
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