import pandas as pd
import json
import os
import sys
import re
import pprint
import unidecode
import pickle


def eprint(*args, **kwargs):
    kwargs['file'] = sys.stderr
    print('--> ', *args, **kwargs)


def epprint(*args, **kwargs):
    pprint.pprint(*args, stream=sys.stderr, **kwargs)


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


def normalize_name(s, strong=False):
    assert isinstance(s, str), s
    initial_s = s
    # Project on ASCII
    s = unidecode.unidecode(s)
    # Project on lower-case letters
    s = s.lower()
    # Strip to remove extrem spaces
    s = s.strip()
    # Remove repeated spaces and make them '_'
    s = re.sub(r'\s+', r'_', s)
    # Remove repeated '_', if any left
    s = re.sub(r'_+', r'_', s)
    ##
    if not strong:
        return s
    # Remove all non-letters
    s = re.sub(r'[^a-z]', '', s)
    # Remove all repeated letters
    s = re.sub(r'(.)\1+', r'\1', s)
    assert s != '', initial_s
    return s

#############################################################


def extract_unique_elements(l):
    ll = list()
    for e in l:
        if l in ll:
            continue
        ll.append(e)
    return ll

#############################################################


class Cache:
    def __init__(self, cachename_dict=None,
                 dirname=None, dataname=None,
                 interval=100):
        self.update_counter = 0
        ##
        assert isinstance(interval, int), interval
        self.interval = interval
        # @
        if cachename_dict is not None:
            assert dirname is None
            assert dataname is None
            dirname = cachename_dict['dirname']
            dataname = cachename_dict['dataname']
        assert dirname is not None
        assert dataname is not None
        self.dirname = dirname
        self.dataname = dataname
        ##
        self.internal_cache_dict = None
        test = test_file_exists(self.dataname, dir=self.dirname)
        if not test:
            self.internal_cache_dict = dict()
        else:
            eprint(f'Loading cache {self.dataname}')
            self.internal_cache_dict = \
                load_file_to_data(self.dataname, dir=self.dirname)

    def save(self):
        assert self.internal_cache_dict is not None
        dump_data_to_file(self.internal_cache_dict,
                          self.dataname, dir=self.dirname)

    def holds_key(self, key):
        assert self.internal_cache_dict is not None
        return key in self.internal_cache_dict

    def get_key_value(self, key):
        assert self.internal_cache_dict is not None
        assert key in self.internal_cache_dict, key
        return self.internal_cache_dict[key]

    def update_key_value(self, key, value):
        assert self.internal_cache_dict is not None
        self.internal_cache_dict[key] = value
        self.update_counter += 1
        if self.update_counter > self.interval:
            # Save the cache after so many updates for safety
            assert self.dirname is not None
            assert self.dataname is not None
            eprint(f'Saving cache {self.dataname}')
            self.save()
            self.update_counter = 0
