import json


class AutoVivification(dict):
    """
    Implementation of perl's autovivification feature, combined with a
    data structure similar to MUMPS/Cache arrays
    """
    null = None  # float('nan')

    def __init__(self, iterable=None):
        dict.__init__(self)
        if iterable:
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
        
    def put_item(self, keys, value):
        obj = self
        for key in keys[:-1]:
            obj = obj[key]
        obj[keys[-1]] = value

    def merge(self, iterable):
        AutoVivification._load_dict_(iterable, self)

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
            if k == 'null':  # Translating JSON to Python
                k = None

            if isinstance(v, dict):
                AutoVivification._load_dict_(v, out_object[k])
            else:
                out_object[k] = v

# # # #


if __name__ == "__main__":
    from time import time
    start = time()

    # test that we can initialize an object
    iterate = {'a': 'Hello',
               'b': 'World',
               'c': ['this', 'is', 'a', 'list']}
    test_init = AutoVivification(iterate)
    '''
    {
        "a": {
            "null": "Hello"
            },
        "b": {
            "null": "World"
            },
        "c": {
            "null": [
                "this",
                "is",
                "a",
                "list"
                ]
            }
    }
    '''

    # test that we actually have an auto-viv object
    test_init['a']['hello'] = "world"
    '''
       {
           "a": {
               "null": "Hello",
               "hello": {
                   "null": "world"
                   }
               },
           "b": {
               "null": "World"
               },
           "c": {
               "null": [
                   "this",
                   "is",
                   "a",
                   "list"
                   ]
               }
       }
    '''

    # test saving
    test_init.save("test.json")

    # then test loading that object back in - should use same functionality as initializing
    test_load = AutoVivification.load('test.json')
    print test_load.get_item('a', 'hello')

    # can we merge a dict into the auto-viv?
    test_load['a'].merge({'test': 'merged'})
    print test_load.get_item('a', 'test')
    '''
       {
           "a": {
               "null": "Hello",
               "hello": {
                   "null": "world"
                   },
               "test": {
                   "null": "merged"
                   }
               },
           "b": {
               "null": "World"
               },
           "c": {
               "null": [
                   "this",
                   "is",
                   "a",
                   "list"
                   ]
               }
       }
       '''

    # can we merge another auto-viv into the auto-viv?
    test_load['b'].merge(AutoVivification({'test': 'merged'}))
    print test_load.get_item('b', 'test')
    '''
       {
           "a": {
               "null": "Hello",
               "hello": {
                   "null": "world"
                   },
               "test": {
                   "null": "merged"
                   }
               },
           "b": {
               "null": "World",
               "test": {
                   "null": "merged"
                   }
               },
           "c": {
               "null": [
                   "this",
                   "is",
                   "a",
                   "list"
                   ]
               }
       }
       '''

    print test_load

    finished = time() - start
    print "finished in %f seconds" % finished
