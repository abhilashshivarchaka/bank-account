# reference: geeks for geeks 
from collections import OrderedDict 
class lru:
    def __init__(self, capacity):
        self.capacity= capacity
        self.cache= OrderedDict()

    def get(self,key):
        if key in self.cache:
            value=self.cache[key]
            # self.cache[key]=value
            return value
        return -1

    def put(self,key,value):
        # if key in self.cache:
        self.cache[key]=value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
        # self.cache[key]=value

c = lru(2)

c.put(2,3)
c.put(1,4)
print(c.cache)
c.put(4,5)
print(c.cache)
print(c.get(1))