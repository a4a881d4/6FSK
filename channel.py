import numpy as np
import math
import random

class channel:
	def __init__(self,Fe,Rs,N0,Os):
		self.Fe = Fe
		self.Rs = Rs
		self.N0 = N0
		self.df = Fe/Rs*2.*math.pi
		self.sigm = math.sqrt(N0*Os/2.)

	def ferr(self,x):
		phase = np.arange( len(x) )*self.df
		y = np.exp( 1j * phase)*x
		return y

	def awgn(self,x):
		n = np.random.randn(len(x))+1j*np.random.randn(len(x))
		n *= self.sigm
		return x+n

def main():
	c = channel(1.,6.,1,16)
	x = np.array([1]*16)
	print c.ferr(x)
	print c.awgn(x)

if __name__ == '__main__':
	main()

