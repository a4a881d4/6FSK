
DataA = 2
PilotA = 1
constellation = [2+1j,1+2j,-1+2j,-2+1j,-2-1j,-1-2j,1-2j,2-1j]

freq = [-3,-2,-1,1,2,3]

difTab = {
	-4-3j : -3,
	-5j   : -2,
	4-3j  : -1,
	4+3j  :  1,
	5j    :  2,
	-4+3j :  3
}

def invDict(dic):
	r = {}
	for k in dic:
		r[dic[k]] = k
	return r

transTab = [[(a+b)&7 for b in range(8)] for a in freq]

constellationIndex = { constellation[k]:k for k in range(8)}

c2f = [[0 for k in range(8) ] for l in range(8)]

for f in range(6):
	for l in range(8):
		c2f[l][transTab[f][l]] = freq[f] 

difInvTab = invDict(difTab)

Primary = {
	  5:[0x25,0x29]
	, 6:[0x43,0x49]
	, 7:[0x83,0x89]
	, 8:[0x11b,0x11d]
	, 9:[0x211,0x21b]
	,10:[0x409,0x40f]
	,11:[0x805,0x817]
	,12:[0x1009,0x1021]
}

def main():
	print constellationIndex
	print transTab
	print c2f


if __name__ == '__main__':
	main()