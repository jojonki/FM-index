import argparse
import sys
from fm_index import FMIndex


parser = argparse.ArgumentParser()
parser.add_argument('pat', metavar='N', type=str, nargs=1,
                    help='search words')
parser.add_argument('--f', type=str, metavar='PATH', help='text file')

args = parser.parse_args()
T = 'abaaba'
pat = args.pat[0]

if args.f is None:
    if len(sys.argv) >= 2:
        T = sys.argv[1]
    if len(sys.argv) >= 3:
        pat = sys.argv[2]
else:
    with open(args.f, 'r') as f:
        T = ''.join(f.readlines())

print('Input:', T[:10], ', pattern:', pat)

fmi = FMIndex()
print('encode fmi')
bw = fmi.encode(T)
# print('bwt:', bwt.bwt)
print('bwt:', bw)
decoded = fmi.decode(bw)
# print('Decoded:', decoded)
match = fmi.search(pat)
print('search({})'.format(pat))
print('match', match)
for m in match:
    print(decoded[m[0]:m[1]])
    # print(decoded[m[0]:])
print('aaaa')
