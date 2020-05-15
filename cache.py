from .utilities import load_file_to_data, dump_data_to_file, test_file_exists


class Cache:
    def __init__(self, cachename_dict=None,
                 dirname=None, dataname=None,
                 interval=100):
        self.update_counter = 0
        ##
        assert isinstance(interval, int), interval
        self.interval = interval
        ##

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
