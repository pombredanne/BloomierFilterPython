#from core.bloomierHasher import *
#import bloomierHasher
from core.bloomierHasher import BloomierHasher
from core.orderAndMatch import *
from core.orderAndMatchFinder import *
from core.utilEncode import *
from core.util import *

class BloomierFilter:
    def __init__(self, hashSeed, keysDict, m, k, q):
        self.hashSeed = hashSeed
        self.keysDict = keysDict
        self.m = m
        self.k = k
        self.q = q
        self.hasher = BloomierHasher(hashSeed, m, k, q)
        self.byteSize = getByteSize(q)
        
        oamf = OrderAndMatchFinder(hashSeed, keysDict, m, k, q)
        oam =  oamf.find()
        
        self.table = [[0] * self.byteSize] * m
        self.valueTable = [0] * m

        self.create(keysDict, oam)
        
    def xorOperations(self, value, M, neighbors):
        #value = [0] * self.byteSize
        #print "???", value
        byteArrayXor(value, M)
        
        for v in neighbors:
            byteArrayXor(value, self.table[v])
        
        return value
        
    def get(self, key):
        neighbors = self.hasher.getNeighborhood(key)
        mask = self.hasher.getM(key)
        
        #print neighbors
        valueToGet = [0] * self.byteSize
        self.xorOperations(valueToGet, mask, neighbors)
        
        h = decode(valueToGet) # , self.byteSize)
        
        try:
            L = neighbors[h]
            return self.valueTable[L]
        except IndexError:
            return None
            
    def set(self, key, value):
        neighbors = self.hasher.getNeighborhood(key)
        mask = self.hasher.getM(key)
        
        #print neighbors
        valueToGet = [0] * self.byteSize
        self.xorOperations(valueToGet, mask, neighbors)
        
        h = decode(valueToGet) # , self.byteSize)
        
        try:
            L = neighbors[h]
            self.valueTable[L] = value
            return True
        except IndexError:
            return False    
            
    def create(self, map, oam):
        piList = oam.piList
        tauList = oam.tauList
        #print pi, tau
        
        for i, pi in enumerate(piList):
        #for pi in piList:
            key = pi
            value = map[key]
            #print value
            neighbors = self.hasher.getNeighborhood(key)
            mask = self.hasher.getM(key)
            l = tauList[i] # tauList contains the iota values
            L = neighbors[l]
            
            encodeValue = encode(l, self.byteSize)
            valueToStore = [0] * self.byteSize
            
            byteArrayXor(valueToStore, encodeValue)
            byteArrayXor(valueToStore, mask)
            
            for i, v in enumerate(neighbors):
                if i == l:
                    pass
                else:
                    # The h_value in the table should be applied
                    byteArrayXor(valueToStore, self.table[v])

            self.table[L] = valueToStore
            self.valueTable[L] = value
        #print self.valueTable
            
if __name__ == "__main__":
    sys.path.append("../test")
    from testBloomierFilter import *
    
    unittest.main(verbosity=2)