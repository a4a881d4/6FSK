import const
import freqTab
import math

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
	
	for k in range(E):
		D.append(D[k])
		P.append(P[k])

	S,C,Mask = freqTab.freqTab(b,W)
	r,p = toFreq(D,P)

	d = []

	for k in range(len(r)):
		p0 = C[p[k]]
		for p1 in S[r[k]]:
			d.append((p0+p1)&Mask)

	return d

def main():
	D = [1,1,-1,1,-1,-1,1,-1]
	P = [1,-1,-1,-1,-1,1,1,1]
	d = modu(D,P,4,math.pi/8,18)
	import matplotlib.pyplot as plt
	plt.plot(d)
	plt.show()

if __name__ == '__main__':
	main()
