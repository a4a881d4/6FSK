import random
import numpy as np

def  rsrcBin(L):
	r = []
	for k in range(L):
		r.append(random.randint(0,1))
	return r

def rsrc(L):
	r = rsrcBin(L)
	x = [1-2*x for x in r]
	return x

def fftOnce(x):
	W = len(x)
	hw = np.hamming(W)
	ss = np.fft.fft(x*hw)
	return np.conj(ss)*ss

def spectrum(x):
	W = 1024*32
	r = fftOnce(x[:W])
	for k in range(W/2,len(x)-W,W/2):
		r = r + fftOnce(x[k:k+W])
	return r

def xorsum(k):
	r = 0		
	for i in range(self.order):
		r = r^(k&1)
		k = k>>1
	return r&1
	
class mseq:
	def __init__(self,poly):
		self.p = poly
		k=0
		while poly!=0:
			k = k+1
			poly = poly>>1
		self.order = k-1
		print "M sequence order",k
		self.length = (1<<self.order)-1
		self.s = []
		state = 1
		for n in range(self.length):
			state = state<<1
			if state>self.length:
				state = state^self.p
				self.s.append(1)
			else:
				self.s.append(0)
			
	def printSeq(self,x=None):
		if x==None:
			x = self.s
		for k in x:
			print k,
		print ""

	def sum(self):
		ss = 0
		for x in self.s:
			ss = ss + x
		return ss


	def shift(self,l):
		return self.s[l:]+self.s[:l]

class gold:
	def __init__(self,p0,p1):
		self.m0 = mseq(p0)
		self.m1 = mseq(p1)

	def seq(self,k0,k1):
		s0 = self.m0.shift(k0)
		s1 = self.m1.shift(k1)
		r = [a^b for (a,b) in zip(s0,s1)]
		return r

	def toReal(self,s):
		return np.array([1-2*x for x in s])

	def xcorr(self,x,y):
		return np.correlate(np.array(x),np.array(y),'full')
		
def main():
	m = mseq(0x409)
	m.printSeq()
	y = m.shift(1)
	print "shift 1"
	m.printSeq(y)
	print m.sum()
	g = gold(0x409,0x40f)
	s = g.toReal(g.seq(1,3))
	x = g.xcorr(s,s)
	import matplotlib.pyplot as plt
	plt.plot(x)
	plt.show()


if __name__ == '__main__':
	main()
