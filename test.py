import argparse
from fm_index import FMIndex

parser = argparse.ArgumentParser()
parser.add_argument('--f', type=str, metavar='PATH', help='text file')
parser.add_argument('--t', type=str, help='raw text')
parser.add_argument('--s', type=str, help='search text')
parser.add_argument('--d', type=str, metavar='PATH', help='dict file')
args = parser.parse_args()

T = 'abaaba'
pat = args.s

if args.f is None:
    T = args.t
else:
    with open(args.f, 'r') as f:
        T = ''.join(f.readlines())

print('Input:', T[:10], ', pattern:', pat)

fmi = FMIndex()
print('encode text...')
bw = fmi.encode(T)
print('encode done!')
# print('bwt:', bwt.bwt)
# print('bwt:', bw)
decoded = fmi.decode(bw)
# print('Decoded:', decoded)
match = fmi.search(pat)
print('search("{}")'.format(pat))
print('match', match)
for i, m in enumerate(match):
    print('Match{}: ---{}"{}"{}---'.format(i, decoded[m[0]-5: m[0]], decoded[m[0]:m[1]], decoded[m[1]:m[1]+5]))
    # print(decoded[m[0]:])
