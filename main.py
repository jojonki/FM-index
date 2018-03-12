import os
import argparse
from fm_index import FMIndex

parser = argparse.ArgumentParser()
parser.add_argument('--f', type=str, metavar='PATH', help='text file')
parser.add_argument('--dir', type=str, metavar='PATH', help='text dir')
parser.add_argument('--t', type=str, help='raw text')
parser.add_argument('--s', type=str, help='search text')
parser.add_argument('--d', type=str, metavar='PATH', help='dict file')
args = parser.parse_args()

def load_files(f_dir):
    T = ''
    db = []
    for root, dirs, files in os.walk(f_dir):
        path = root.split(os.sep)
        for f_name in files:
            if f_name.endswith('.txt'):
                f_path = os.sep.join(path + [f_name])
                with open(f_path, 'r') as f:
                    T += ''.join(f.readlines())
                    db.append((f_name, len(T)))
                    if len(T) > 30000:
                        break
    print('len(T)', len(T))
    return T, db

def get_file_name_via_index(db, index):
    target_f_name = None
    for i, (f_name, ct) in enumerate(db):
        if index < ct:
            target_f_name = f_name
            break
    return target_f_name


pat = args.s
if args.dir is not None:
    T, db = load_files(args.dir)
    print('db', db)
    # print(T[:1000])
elif args.f is not None:
    with open(args.f, 'r') as f:
        T = ''.join(f.readlines())
else:
    T = args.t

print('Input:', T[:10], ', pattern:', pat)

fmi = FMIndex()
print('encode text...')
bw = fmi.encode(T)
print('encode done!')
dec = fmi.decode(bw)
# print('Decoded:', decoded)
match = fmi.search(pat)
print('search("{}")'.format(pat))
print('match', match)
for i, m in enumerate(match):
    beg = m[0]
    end = m[1]
    print('beg, end', beg, end)
    f_name = get_file_name_via_index(db, beg)
    print('{} [{}]: -{}"{}"{}-'.format(i, f_name, dec[beg-5: beg], dec[beg:end], dec[end:end+5]))
    # print(decoded[m[0]:])
