import json


class AutoVivification(dict):
    """
    Implementation of perl's autovivification feature, combined with a
    data structure similar to MUMPS/Cache arrays
    """
    null = None  # float('nan')

    def __init__(self, iterable=None):
        if iterable:
            # dict.__init__(self, iterable, **kwargs)  # can't find a way to run this without throwing error yet
            AutoVivification._load_dict_(iterable, self)
    '''
    def __getitem__(self, key):
        try:
            dict.__getitem__(self, key)
        except KeyError:
            self[key] = value = type(self)()
            return value
    '''
    
    def __missing__(self, key):
        self[key] = value = type(self)()
        return value
        
    def __setitem__(self, key, value):
        if isinstance(value, type(self)) or key == AutoVivification.null:
            dict.__setitem__(self, key, value)
        else:
            dict.__setitem__(self[key], AutoVivification.null, value)
            
    def get_item(self, *args):
        obj = self
        for arg in args:
            obj = obj[arg]
        return obj[AutoVivification.null]
        
    def set_item(self, keys, value):
        obj = self
        for key in keys[:-1]:
            obj = obj[key]
        obj[keys[-1]] = value

    def save(self, file_path):
        dump_string = json.dumps(self,
                                 sort_keys=True, indent=4)
        with open(file_path, 'w') as output:
            output.write(dump_string)

    @staticmethod
    def load(file_path):
        loaded_viv = AutoVivification()

        with open(file_path, 'r') as input_file:
            loaded = json.load(input_file)

        AutoVivification._load_dict_(loaded, loaded_viv)

        return loaded_viv

    @staticmethod
    def _load_dict_(iterable, out_object):
        for k, v, in iterable.iteritems():
            if k == 'null':
                k = None

            if isinstance(v, dict):
                AutoVivification._load_dict_(v, out_object[k])
            else:
                out_object[k] = v

# # # #


if __name__ == "__main__":
    from time import time
    start = time()

    iterate = {'a': 'Hello', 'b': 'World'}
    test_init = AutoVivification(iterate)
    print test_init

    test_save = AutoVivification()
    test_save['a'] = "hello"
    test_save['b'] = "world"
    test_save['a']['b'] = "hello world"
    print test_save.get_item('a', 'b')
    test_save.save("test.json")

    test_load = AutoVivification.load('test.json')
    print test_load.get_item('a', 'b')

    finished = time() - start
    print "finished in %f seconds" % finished
