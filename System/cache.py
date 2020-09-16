import os
from .file import load_file_to_data, dump_data_to_file, test_file_exists
from .print import eprint


class Cache:
    def __init__(self, *, cachedirname=None, cachename=None, interval=100):
        self.update_counter = 0
        ##
        assert isinstance(interval, int), interval
        self.interval = interval
        ##
        assert cachename is not None
        self.dataname = cachename
        ##
        if cachedirname is None:
            cachedirname = ""
        self.dirname = os.path.join("Cache", cachedirname)
        ##
        self._internal_cache_dict = None
        test = test_file_exists(self.dataname, dir=self.dirname)
        if not test:
            self._internal_cache_dict = dict()
        else:
            eprint(f"Loading cache {self.dataname}")
            self._internal_cache_dict = load_file_to_data(
                self.dataname, dir=self.dirname
            )

    def save(self):
        assert self._internal_cache_dict is not None
        dump_data_to_file(
            self._internal_cache_dict, self.dataname, dir=self.dirname
        )

    def holds_key(self, key):
        assert self._internal_cache_dict is not None
        return key in self._internal_cache_dict

    def get_key_value(self, key):
        assert self._internal_cache_dict is not None
        assert key in self._internal_cache_dict, key
        return self._internal_cache_dict[key]

    def update_key_value(self, key, value):
        assert self._internal_cache_dict is not None
        self._internal_cache_dict[key] = value
        self.update_counter += 1
        if self.update_counter > self.interval:
            # Save the cache after so many updates for safety
            assert self.dirname is not None
            assert self.dataname is not None
            eprint(f"Saving cache {self.dataname}")
            self.save()
            self.update_counter = 0
