import pandas as pd
import json
import os
import sys
import re
import unidecode
import pickle

from ..print import eprint
from ..normalize import normalize_name


#############################################################
pkl_dir = 'PKL'


def _internal_dataname_to_path(dataname, dir=''):
    dirname = os.path.join(pkl_dir, dir)
    filename = dataname + '.pkl'
    # eprint(dirname, filename)
    path = os.path.join(dirname, filename)
    return (path, dirname, filename)


def list_dir_contents(dir='Cache'):
    (_, dirname, _) = _internal_dataname_to_path('NONAME', dir)
    assert os.path.exists(dirname), dirname
    l = list()
    for (root, _, files) in os.walk(dirname):
        for file in files:
            (_, ext) = os.path.splitext(file)
            if ext.lower() != '.pkl':
                continue
            path = os.path.join(root, file)
            assert os.path.exists(path), path
            l.append(path)
    return l


def test_file_exists(dataname, dir=''):
    (path, _, _) = _internal_dataname_to_path(dataname, dir)
    return os.path.exists(path)


def load_file_to_data(dataname, dir=''):
    (path, _, _) = _internal_dataname_to_path(dataname, dir)
    assert os.path.exists(path), path
    with open(path, 'rb') as input:
        eprint(f'Loading {dataname} from: {path}', end='... ')
        data = pickle.load(input)
    eprint('Done!')
    return data


def is_target_newer_than_source(source=None, dataname=None, dir=''):
    assert source is not None, source
    assert dataname is not None, dataname
    assert os.path.exists(source), source
    (path, _, _) = _internal_dataname_to_path(dataname, dir)
    target = path
    if not os.path.exists(target):
        eprint(f'is_dump_newer: Target {target} does not exist, yet')
        return False
    source_mtime = os.path.getmtime(source)
    target_mtime = os.path.getmtime(target)
    if target_mtime > source_mtime:
        eprint(
            f'is_dump_newer: Target {target} is actually newer than Source {source}')
        return True
    eprint(f'is_dump_newer: Target {target} is not newer than Source {source}')
    return False


def dump_data_to_file(data, dataname, dir=''):
    (path, dirname, _) = _internal_dataname_to_path(dataname, dir)
    os.makedirs(dirname, exist_ok=True)
    assert os.path.exists(dirname)
    with open(path, 'wb') as output:
        eprint(f'Dumping {dataname} to: {path}', end='... ')
        pickle.dump(data, output)
    eprint('Done!')
    assert os.path.exists(path), path
    return None

#############################################################


def extract_unique_elements(l):
    ll = list()
    for e in l:
        if l in ll:
            continue
        ll.append(e)
    return ll

#############################################################
