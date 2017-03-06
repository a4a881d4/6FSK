
from Qfunc import Fserial
import math

def freqTab(beta,W):
	P2pi = 1<<W
	alf = int(beta/math.pi*float(P2pi))
	S = {}
	S[1] = Fserial(0.5,1024,0.5,P2pi/4-alf)
	S[2] = Fserial(0.5,1024,0.5,P2pi/4)
	S[3] = Fserial(0.5,1024,0.5,P2pi/4+alf)
	S[-1] = [ -k for k in S[1]]
	S[-2] = [ -k for k in S[2]]
	S[-3] = [ -k for k in S[3]]
	C = [0 for k in range(8)]
	Mask = P2pi-1
	for k in range(4):
		C[k*2] = k*P2pi/4+alf/2
		C[(k*2-1)&7] = k*P2pi/4-alf/2
	for k in range(8):
		C[k] = C[k]&Mask
	return S,C,Mask

def main():
	S,C,Mask = FreqTab(math.pi/8.,18)
	print S
	print Mask
	print C

if __name__ == '__main__':
	main()