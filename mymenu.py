class menu:
	'''a simple menu.'''
	def __init__(self):
		self.boolopt=[]
		self.opts=[]
		self.defins=[]
	def defoption(self,op="-test",defin="test menu input"):
		self.defins.append(defin)
		self.boolopt.append(False)
		self.opts.append(op)
		return
	def option(self,arg1="-test"):
		c=0
		for i in self.opts:
			if arg1==i:
				self.boolopt[c]=True
			else: 
				self.boolopt[c]=False
			c+=1
		return
	def print_menu(self):
		print("\nOptions:")
		for i in range(0,len(self.opts)):
			print("%s : %s" %(self.opts[i],self.defins[i]))
		return