import math

def Qfuncx(t):
	a = 0.
	T = int(t*10000)
	for x in range(T,100*10000):
		v = x/10000.
		a = a + (1/math.sqrt(2.*math.pi))*math.exp(0-v*v/2.)
	return a/10000.

def Qfunc(t):
	return 0.5-0.5*math.erf(t/math.sqrt(2.))

def Ffunc(t,B):
	a = 2.*math.pi*B/math.sqrt(math.log(2.))
	return 0.5*(Qfunc((t-0.5)*a)-Qfunc((t+0.5)*a))

def _Fserial(B,OS,R,W):
	X=[]
	rr = int(OS*R)
	for t in range(-rr,rr):
		X.append(Ffunc(t/float(OS),B))
	sum = 0.
	for T in range(0,len(X)):
		sum = sum + X[T]
	all = sum
	#print 'error',math.pi*2-all
	Y=[]
	sum = 0.
	for T in range(0,len(X)):
		sum = sum + X[T]
		Y.append(int(sum/all*float(W-1)+.5))
	return Y

def Fserial(beta):
	alf = int(beta/math.pi*4.*2.*65536.)
	S = {}
	S['-'] = _Fserial(0.5,1024,0.5,65536*2-alf)
	S['0'] = _Fserial(0.5,1024,0.5,65536*2)
	S['+'] = _Fserial(0.5,1024,0.5,65536*2+alf)
	return S


if __name__ == '__main__':
	S = _Fserial(0.5,1024,0.5,65536)
	print "#",len(S)
	for T in range(0,len(S)):
		print T,S[T]

S = Fserial(math.pi/8.)
