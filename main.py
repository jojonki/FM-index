import sys
from bwt import BWT

T = 'cacao'
if len(sys.argv) >= 2:
    T = sys.argv[1]

print('Input:', T)

bwt = BWT(T)
print('bwt:', bwt.bwt)
print('Decoded:', bwt.decode())
