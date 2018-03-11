import sys
from fm_index import FMIndex

T = 'abaaba'
pat = 'aba'
if len(sys.argv) >= 2:
    T = sys.argv[1]
if len(sys.argv) >= 3:
    pat = sys.argv[2]

print('Input:', T)

fmi = FMIndex()
bw = fmi.encode(T)
# print('bwt:', bwt.bwt)
print('bwt:', bw)
decoded = fmi.decode(bw)
print('Decoded:', decoded)
match = fmi.search(pat)
print('search({})'.format(pat))
for m in match:
    print(decoded[m[0]:m[1]])

