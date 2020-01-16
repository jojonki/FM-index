import os
import pickle


def save_pickle(d, path):
    print('save pickle to', path)
    with open(path, mode='wb') as f:
        pickle.dump(d, f)


def load_pickle(path):
    print('load', path)
    with open(path, mode='rb') as f:
        return pickle.load(f)


def load_files(f_dir):
    T = ''
    db = []
    for root, dirs, files in os.walk(f_dir):
        path = root.split(os.sep)
        for f_name in files:
            if f_name.endswith('.txt'):
                f_path = os.sep.join(path + [f_name])
                with open(f_path, 'r', encoding='utf-8') as f:
                    T += ''.join(f.readlines()).replace('\r', '').replace('\n', '')
                    db.append((f_name, len(T)))
                    if len(T) > 1300000: # TODO
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
