import utils
import numpy as np
from modu import modu,toComplex,dpmap
import math
from channel import channel
from rfir import rfir
from const import Primary
class SIOT:
	def __init__(self,k):
		self.length = 1<<k
		self.Gpilot = utils.gold(Primary[k][0],Primary[k][1])
		self.Pilot = self.Gpilot.toReal(self.Gpilot.seq(1,3)+[0]).tolist()
		self.CPilot = np.array(dpmap([0]*self.length,self.Pilot))
		
		
	def modu(self,D):
		d = modu(D,self.Pilot,4,math.pi/8,18)
		return d
	
	def toComplex(self,d):
		c = toComplex(d[::64],18)
		return c

	def xcorr(self,r):
		c = np.zeros(r.shape,dtype=complex)
		c[:16*len(self.CPilot):16]=self.CPilot
		fc = np.fft.fft(c)
		fr = np.fft.fft(r)
		return np.fft.ifft(fr*np.conj(fc))

	def r1(self,c,k):
		t = c[k::16]
		r = t[:self.length]*np.conj(self.CPilot)
		return np.sum(r[:-1]*np.conj(r[1:]))

	def r4(self,c,k):
		t = c[k::16]
		rr = t[:self.length]*np.conj(self.CPilot)
		r = rr[::8]+rr[1::8]+rr[2::8]+r[3::8]+rr[4::8]+rr[5::8]+rr[6::8]+r[7::8]
		return np.sum(r[:-1]*np.conj(r[1:]))

def main0():
	S = SIOT()
	D0 = utils.rsrc(1024)
	D1 = utils.rsrc(1024)
	d = S.modu(D0) + S.modu(D1)	
	cc = S.toComplex(d)
	ch = channel(0.1,6.,0.5,16)
	c = ch.ferr(cc)
	c = ch.awgn(c)    
	f = rfir()
	c = f.filter(c)
	
	x = np.zeros(16*1042)
	for k in range(len(x)):
		x[k]=np.abs(S.r1(c,k))

	import matplotlib.pyplot as plt
	plt.plot(np.abs(x))
	plt.show()

def main():
	S = SIOT(12)
	D0 = utils.rsrc(S.length)
	D1 = utils.rsrc(S.length)
	d = S.modu(D0) + S.modu(D1)	
	cc = S.toComplex(d)
	ch = channel(0.000,6.,1.,16)
	c = ch.ferr(cc)
	c = ch.awgn(c)    
	f = rfir()
	c = f.filter(c)
	x = S.xcorr(c)

	import matplotlib.pyplot as plt
	plt.plot(np.abs(x))
	plt.show()


if __name__ == '__main__':
	main()