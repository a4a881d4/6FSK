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
		print k
		self.length = (1<<self.order)-1
		self.s = []
		state = 1
		for n in range(self.length):
			state = state<<1
			if state>self.length:
				#print "s+0x%x"%state
				state = state^self.p
				#print "s-0x%x"%state
				self.s.append(1)
			else:
				self.s.append(0)
			
	def printSeq(self,x=None):
		if x==None:
			x = self.s
		for k in x:
			print k,
		print ""

	def shift(self,l):
		return self.s[l:]+self.s[:l]

def main():
	m = mseq(0x211)
	m.printSeq()
	y = m.shift(1)
	print "shift 1"
	m.printSeq(y)

if __name__ == '__main__':
	main()
