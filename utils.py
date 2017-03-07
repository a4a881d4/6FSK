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

