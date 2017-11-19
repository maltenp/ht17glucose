import ethcal as e
import metcal as mc
import my_func as mf
import numpy as np
import matplotlib.pyplot as plt
import sys
import pickle
import os
def dump2pickle(a):
	#a=[[m,h],[m,h]] etc	
	script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
	rel_path = "out.pickle"
	abs_file_path = os.path.join(script_dir, rel_path)
	with open(abs_file_path,"wb") as f:
		pickle.dump(a, f)
	return
def readpickle():
	script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
	rel_path = "out.pickle"
	abs_file_path = os.path.join(script_dir, rel_path)
	a= pickle.load(open(abs_file_path, "rb"))
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
def plot_e_re_glu(s,ere,leg):
	ss=np.sort(s)
	plt.figure(1)
	#plt.plot([range(0,len(ere))],[ere],'*')
	plt.legend(leg)
	plt.plot([ss],[ere],'*')
	plt.legend(leg)
	plt.xlabel('glucose conc [mg/dl]')
	plt.title('Real part of the complex permittivity')
	plt.ylabel('E_re')
	return
def plot_e_im_glu(s,eim,leg):
	ss=np.sort(s)
	plt.figure(2)
	plt.plot([ss],[eim],'*')
	plt.legend(leg)
	plt.xlabel('glucose conc [mg/dl]')
	#plt.plot([range(0,len(ere))],[eim],'*')
	plt.title('Imaginary part of the complex permittivity')	
	plt.ylabel('E_im')
	return
def plot_e_im_vs_ere(eim, ere, leg):
	plt.figure(3)
	plt.plot([eim],[ere],'x')
	plt.title('Real part vs the Imaginary part of the complex permittivity')
	plt.ylabel('E_re')
	plt.xlabel('E_im')
	plt.legend(leg)
	return
def get_fs(m):
	f_s=[]
	for i in m:
		f_s.append(i[2])
	return f_s
def plot_e(s, ere,eim, leg):
	ss=np.sort(s)
	ev=[]
	for i in range(0,len(eim)):
		E=(np.sqrt(np.complex(eim[i])**2*-1)+np.complex(ere[i]))
		ev.append(np.absolute(E))
	plt.figure(4)
	#plt.plot([range(0,len(ev))],[ev],'*')
	#plt.xticks(range(0,len(ev)), leg)
	plt.plot([ss],[ev],'*')
	plt.legend(leg)
	plt.xlabel('glucose conc [mg/dl]')
	plt.ylabel('E_tot')
	plt.title('The measured permittivity')	
	return
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
def plot_v_fs(f_s,s,leg):
	ss=np.sort(s)
	plt.figure(5) #[::-1] to sort in reversed order
	plt.plot(ss*3/2,e.sort_ind(s,f_s),'*')
	#plt.legend(leg)
	plt.title('f_s dependency on liquid surface level')
	plt.xlabel('Liquid surface level [mm]')
	#plt.xlabel('Liquid volume [ml]')
	plt.ylabel('f_s [Hz]')
	return
def plot_glucose_fs(s,f_s,leg):
	ss=np.sort(s)[::-1]
	plt.figure(6)
	plt.plot([ss],[e.sort_ind(s,f_s)],'*')
	plt.legend(leg)
	plt.title('Glucose conc, vs f_s')
	plt.xlabel('Glucose conc.[mg/dl]')
	plt.ylabel('f_s [Hz]')	
	return
def plot_tune(s,f_s,leg):
	ss=np.sort(s)
	plt.figure(7)
	plt.plot(ss,e.sort_ind(s,f_s),'*')
	#plt.legend(leg)
	plt.title('f_s depends on coupling level')
	#plt.xticks([], range(0,360,24))
	plt.xlabel('Coupling angle [deg]')
	plt.ylabel('f_s [Hz]')	
	return
def runscript(opt=["-opt"]):
	if opt[0]=="-opt":
		print('Options:')
		print('-erg: plot_e_re_glu(s,ere,leg)')
		print('-eig: plot_e_im_glu(s,eim,leg)')
		print('-imre: plot_e_im_vs_ere(eim,ere,leg)')
		print('-e: plot_e(s, ere,eim, leg)')
		print('-vfs: plot_v_fs(s,f_s,leg)')
		print('-gfs: plot_glucose_fs(s,f_s,leg)')
		print('-tune: plot_tune(s,f_s)')
		print('-drw: Rewrite pickle')
		print('-da: Append to pickle')
		print('-ra: read from pickle')		
		exit()
	try:
		fn=mf.find_file("output.txt")
	except:
		inp=input('Specify output file to evaluate: ')
		fn=mf.find_file(inp)		
	for i in fn:
		[m,h]=mf.read_file2(i)
	for i in h:
		if i.find('!')!=-1:
			stn=i[2:5]
			break
	[leg, s]=e.leg_and_s(h,start=stn)
	leg=e.sort_ind(s,leg)
	#print('%s will be sorted'%s)
	[dfv,dqv]=get_df_dq(m,s)
	[ere, eim]=get_e(dfv,dqv)
	f_s=get_fs(m)
	
	for i in opt:
		if i=="-erg":
			plot_e_re_glu(s,ere,leg)
		elif i=="-eig":
			plot_e_im_glu(s,eim,leg)
		elif i=="-imre":
			plot_e_im_vs_ere(eim,ere,leg)
		elif i=="-e":
			plot_e(s, ere,eim, leg)
		elif i=="-vfs":
			plot_v_fs(f_s,s,leg)
		elif i=="-gfs":
			plot_glucose_fs(s,f_s,leg)
		elif i=="-tune":
			plot_tune(s,f_s,leg)
		elif i=="-drw":
			input('Are you sure you want to rewrite pickle? (crtl+c to abort)')
			a=[[m,h]]
			dump2pickle(a)
		elif i=="-da":
			a=readpickle()
			a.append([m,h])
			dump2pickle(a)
		elif i=="-ra":
			runscript2()
		else: pass	
	plt.show()

	return
def runscript2():
	try:
		a=readpickle()
	except:
		print('You have to define a pickle first')
		exit()
	for i in a: #i=[m,h]
		m=i[0]
		h=i[1]
		for i in h:
			if i.find('!')!=-1:
				stn=i[2:5]
				break
		[leg, s]=e.leg_and_s(h,start=stn)
		leg=e.sort_ind(s,leg)
		#print('%s will be sorted'%s)
		[dfv,dqv]=get_df_dq(m,s)
		[ere, eim]=get_e(dfv,dqv)
		f_s=get_fs(m)
		plot_tune(s,f_s,leg)
	plt.legend(['Shorted coupling','Main coupling'])
	plt.title('Resonance frequency at different coupling angles')
	plt.xlabel('Degrees [deg]')
	plt.ylabel('f_s [Hz]')
	return
if __name__ == "__main__":
	try:
		runscript(sys.argv[1:])
	except IndexError:
		print(sys.argv)
		runscript()