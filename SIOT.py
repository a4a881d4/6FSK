import utils
import numpy as np
from modu import modu,toComplex
import math

class SIOT:
	def __init__(self):
		Gpilot = utils.gold(0x211,0x21b)
		Epilot = Gpilot.toReal(Gpilot.seq(1,3)+[0])
		Opilot = Gpilot.toReal(Gpilot.seq(127,180)+[0])
		self.Pilot = []
		for k in range(len(Epilot)):
			self.Pilot.append(Epilot[k])
			self.Pilot.append(Opilot[k])
		self.CPilot = np.zeros((1024),dtype=complex)
		self.CPilot[::2]=1j*Epilot
		self.CPilot[1::2]=Opilot

	def modu(self,D):
		d = modu(D,self.Pilot,4,math.pi/8,18)
		return d
	
	def toComplex(self,d):
		c = toComplex(d[::64],18)
		return c

	def r1(self,c,k):
		t = c[k::16]
		return np.sum(t[:1024]*np.conj(self.CPilot))

def main():
	S = SIOT()
	D0 = utils.rsrc(1024)
	D1 = utils.rsrc(1024)
	d = S.modu(D0) + S.modu(D1)	
	c = S.toComplex(d)
	
	#x = np.correlate(ep,c,'full')
	
	x = np.zeros(16*1038)
	for k in range(len(x)):
		x[k]=np.abs(S.r1(c,k))

	import matplotlib.pyplot as plt
	plt.plot(np.abs(x))
	plt.show()

if __name__ == '__main__':
	main()