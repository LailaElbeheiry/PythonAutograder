# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 03:27:16 2019

@author: LailaElbeheiry
"""
import math
import lab1

class SetDigit:
    def __init__(self):
        self.name = "SetDigit.py"
        self.timeout = 2
        

    def refFuncWrapper(self):
        return self.refFunc( int(raw_input()), int(raw_input()), int(raw_input()) )
    
    def refFunc(self, n, k, d):
        return ((n >= 0) * (n - ((n / 10**k) % 10 * (10**k)) + 10**k * d) - (n < 0) * ((-n) - (((-n) / 10**k) % 10 * (10**k)) + 10**k * d))

    
    def inputFunc(self):
        x =  lab1.setKthDigit ( int(raw_input()), int(raw_input()), int(raw_input()) )
        return x
    
class Pop:
    def __init__(self):
        self.name = "Pop.py"
        self.timeout = 2
  
    def refFuncWrapper(self):
        return self.refFunc( int(raw_input()), float(raw_input()), int(raw_input()) )
    
    def refFunc(self,n, k, t):
        return int(n*math.e**(k*t))
    
    def inputFunc(self):
        x = lab1.populationEstimation( int(raw_input()), float(raw_input()), int(raw_input()) )
        return x
         
def generate(names):
    src = open("source.py")
    srcLines = list(map(lambda x: x.rstrip('\0'), src.readlines()))
    for name in names:
        f = open(name + ".py", 'w')
        srcLines[1] = "from functionGenerator import " + name + " as s"
        f.writelines(srcLines)
        f.close()    
  
    
    
if __name__ == "__main__":
    names = ["SetDigit", "Pop"]
    generate(names)