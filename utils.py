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

def spectrum(x):
	W = 1024*32
	hw = np.hamming(W)
	r = np.zeros((W,1))
	L = len(x)

	for k in range(0,L-W,W/2):
		ss = np.fft.fft(x[k:k+W]*hw)
		r = r + np.conj(ss)*ss
		print k
	return r

