import json


class AutoVivification(dict):
    """
    Implementation of perl's autovivification feature, combined with a
    data structure similar to MUMPS/Cache arrays
    """
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
        if isinstance(value, type(self)):
            dict.__setitem__(self, key, value)
        else:
            dict.__setitem__(self[key], None, value)
            
    def get_item(self, *args):
        obj = self
        for arg in args:
            obj = obj[arg]
        return obj[None]
        
    def set_item(self, keys, value):
        obj = self
        for key in keys[:-1]:
            obj = obj[key]
        obj[keys[-1]] = value
        
# # # #


if __name__ == "__main__":
    from time import time
    
    test_viv = AutoVivification()
    
    start = time()
    
    test_viv["Hello"] = "a"
    # print test_viv
    
    test_viv.set_item(["Hello", "World"], "b")    
    print test_viv.get_item("Hello", "World")
    
    test_viv["Hello"]["Good Bye"] = "c"
    print test_viv
    
    n = 1000000
    test_viv.set_item([i for i in range(n)], "long test")
    print test_viv.get_item(*[i for i in range(n)])

    finished = time() - start
    print "finished in %f seconds" % finished
