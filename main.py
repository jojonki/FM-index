import sys
from bwt import BWT1, BWT2

T = 'cacao'
if len(sys.argv) >= 2:
    T = sys.argv[1]

print('Input:', T)

print('BWT1-----')
bwt1 = BWT1(T)
# print('bwt:', bwt.bwt)
print('bwt:', ''.join(bwt1.bwt))
print('Decoded:', bwt1.decode())

print('BWT2-----')
bwt2 = BWT2(T)
# print('bwt:', bwt.bwt)
print('bwt:', ''.join(bwt2.bwt))
print('Decoded:', bwt2.decode())
