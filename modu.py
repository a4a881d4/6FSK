import const
import freqTab
import math
import numpy as np
import utils
import matplotlib.pyplot as plt

def map(D,P):
	r = []
	for k in range(len(D)):
		if k%2 == 0:
			r.append(D[k]*const.DataA+P[k]*const.PilotA*1j)
		else:
			r.append(D[k]*const.DataA*1j+P[k]*const.PilotA)
	return r

def toFreq(D,P):
	m = map(D,P)
	p = [const.constellationIndex[c] for c in m]
	r = [const.c2f[p[k]][p[k+1]] for k in range(len(p)-1)]
	return r,p

def modu(D,P,E,b,W):
	if len(D)>len(P):
		for k in range(len(P),len(D)):
			P.append(1)
	if len(P)>len(D):
		for k in range(len(D),len(P)):
			D.append(1)
	if len(D)%2 == 1:
		P.append(1)
		D.append(1)
	hD = D[:E]
	tD = D[-E:]
	D = tD + D + hD
	hP = P[:E]
	tP = P[-E:]
	P = tP + P + hP
	
	#for k in range(E):
	#	D.append(D[k])
	#	P.append(P[k])

	S,C,Mask = freqTab.freqTab(b,W)
	r,p = toFreq(D,P)

	d = []

	for k in range(len(r)):
		p0 = C[p[k]]
		for p1 in S[r[k]]:
			d.append((p0+p1)&Mask)

	return d

def toComplex(s,W):
	M = 2.*math.pi/float(1<<W)
	r = [1j*float(a)*M for a in s]
	return np.exp(np.array(r))

def showSpectrum(c,l):
	pc = utils.spectrum(c)
	rs = float(1024)/float(len(pc))
	x = np.arange(100)*rs
	plt.plot(x,20.*np.log10(pc[:100]),l)

def showTiming(c,l):
	import matplotlib.pyplot as plt
	x = c[l::1024]
	plt.plot(x.real,x.imag,'.')
	plt.show()

def main():
	D = utils.rsrc(1024*64)
	P = utils.rsrc(1024*64)
	d = modu(D,P,4,math.pi/8,18)
	c = toComplex(d,18)
	showSpectrum(c,'r')
	d = modu(D,P,4,math.pi/6,18)
	c = toComplex(d,18)
	showSpectrum(c,'b')
	d = modu(D,P,4,math.pi/5,18)
	c = toComplex(d,18)
	showSpectrum(c,'y')
	d = modu(D,P,4,math.pi/4,18)
	c = toComplex(d,18)
	showSpectrum(c,'g')
	
	#showTiming(c,1024/16)
	plt.show()
	return c

if __name__ == '__main__':
	c = main()
