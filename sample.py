import argparse
import os
import sys

from fm_index import FMIndex
from util import save_pickle, load_pickle, load_files, get_file_name_via_index


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, metavar='PATH', help='text file')
    parser.add_argument('--dir', type=str, metavar='PATH', help='text dir')
    parser.add_argument('--dict', type=str, metavar='PATH', help='dict file')
    parser.add_argument('-q', '--query', type=str, required=True, help='search text')
    args = parser.parse_args()

    query = args.query
    if args.dir is not None:
        T, db = load_files(args.dir)
    elif args.file is not None:
        db = []
        with open(args.file, 'r') as f:
            T = ''.join(f.readlines())
            db.append((args.file, len(T)))
    else:
        print('You need to specify either args.dir or args.file')
        sys.exit()

    fmi = FMIndex()
    if args.dict and os.path.isfile(args.dict):
        saved_data = load_pickle(args.dict)
        bw = saved_data['bwt']
        fmi.set_dict(saved_data)
    else:
        print('encode text...')
        bw, sa = fmi.encode(T)
        ranks, ch_count = fmi.rank_bwt(bw)
        save_pickle({'bwt': bw, 'sa': sa, 'text_len': len(T), 'ch_count': ch_count}, 'index.dict')
        fmi.ch_count = ch_count
        print('encode done!')
    match = fmi.search(query)

    print('Results of search("{}")'.format(query))
    print('match', match)
    rng = 15
    for i, m in enumerate(match):
        beg = m[0]
        end = m[1]
        f_name = get_file_name_via_index(db, beg)
        print('Result {} @ {} ({}, {})'.format(i, f_name, beg, end))
        print('...{}"{}"{}...'.format(T[beg-rng: beg], T[beg:end], T[end:end+rng]))


if __name__ == '__main__':
    main()
