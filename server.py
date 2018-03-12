import os
import argparse
from fm_index import FMIndex
from util import save_pickle, load_pickle, load_files, get_file_name_via_index
from flask import Flask, render_template, request, redirect, url_for

parser = argparse.ArgumentParser()
parser.add_argument('--f', type=str, metavar='PATH', help='text file')
parser.add_argument('--dir', type=str, metavar='PATH', help='text dir')
parser.add_argument('--dict', type=str, metavar='PATH', help='dict file')
parser.add_argument('--t', type=str, help='raw text')
parser.add_argument('--s', type=str, help='search text')
parser.add_argument('--d', type=str, metavar='PATH', help='dict file')
args = parser.parse_args()
app = Flask(__name__)

T, fmi, db = None, None, None

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        # message = 'hi'
        pat = request.args.get('keyword')
        # request.form['keyword'])
        # return render_template('index.html', message=message)

        if pat:
            # pat = request.form['keyword']
            # pat = '日本の'
            match = fmi.search(pat)
            print('Results of search("{}")'.format(pat))
            print('match', match)
            rng = 15
            results = []
            for i, m in enumerate(match):
                beg = m[0]
                end = m[1]
                # print('(beg, end) = ({}, {})'.format(beg, end))
                f_name = get_file_name_via_index(db, beg)
                print('{} [{}]: ({}, {})'.format(i, f_name, beg, end))
                # print('---{}"{}"{}---'.format(dec[beg-rng: beg], dec[beg:end], dec[end:end+rng]))
                print('---{}"{}"{}---'.format(T[beg-rng: beg], T[beg:end], T[end:end+rng]))
                v = '{}<span class="match">{}</span>{}'.format(T[beg-rng: beg], T[beg:end], T[end:end+rng])
                results.append((f_name, v))
                # print(decoded[m[0]:])
            return render_template('index.html', results=results)
        else:
            return render_template('index.html')
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('index'))


def load_database():
    global T, fmi, db
    pat = args.s
    if args.dir is not None:
        T, db = load_files(args.dir)
        print('db', db)
        # print(T[:1000])
    elif args.f is not None:
        db = []
        with open(args.f, 'r') as f:
            T = ''.join(f.readlines())
            db.append((args.f, len(T)))
    else:
        T = args.t

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
    return 
    # return T, fmi
    # print('decoding...')
    # dec = fmi.decode(bw)
    # print('decoding done')
    match = fmi.search(pat)
    print('Results of search("{}")'.format(pat))
    print('match', match)
    rng = 5
    for i, m in enumerate(match):
        beg = m[0]
        end = m[1]
        # print('(beg, end) = ({}, {})'.format(beg, end))
        f_name = get_file_name_via_index(db, beg)
        print('{} [{}]: ({}, {})'.format(i, f_name, beg, end))
        # print('---{}"{}"{}---'.format(dec[beg-rng: beg], dec[beg:end], dec[end:end+rng]))
        print('---{}"{}"{}---'.format(T[beg-rng: beg], T[beg:end], T[end:end+rng]))
        # print(decoded[m[0]:])


if __name__ == '__main__':
    load_database()
    app.debug = True
    app.run(host='0.0.0.0')
