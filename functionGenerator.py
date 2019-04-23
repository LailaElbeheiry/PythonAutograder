# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 05:32:18 2019

@author: LailaElbeheiry
"""

# -*- coding: utf-8 -*-

import math
import lab1

#############This file

class whichTriangle:
    def __init__(self):
        pass
        
    def refFuncWrapper(self):
        return self.refFunc( int(raw_input()), int(raw_input()), int(raw_input()) )
    
    def refFunc(self,a,b,c):
        if (a >= b + c) or (b >= a + c) or (c >= a + b):
            return 0        # Side cannot be a triangle
        elif (a**2 == b**2 + c**2) or (b**2 == a**2 + c**2) or (c**2 == a**2 + b**2):
            return 1        # Right triangle
        elif a == b == c:
            return 3        # Equilateral triangle
        elif (a**2 > b**2 + c**2) or (b**2 > a**2 + c**2) or (c**2 > a**2 + b**2):
            if a != b and b != c and c != a:
                return 4    # Obtuse angled scalene triangle
            else:
                return 5    # Obtuse angled isosceles triangle
        elif (a**2 < b**2 + c**2) or (b**2 < a**2 + c**2) or (c**2 < a**2 + b**2):
            if a != b and b != c and c != a:
                return 6    # Acute angled scalene triangle
            else:
                return 7    # Acute angled isosceles triangle
    
    def inputFunc(self):
        x =  lab1.whichTriangle( int(raw_input()), int(raw_input()), int(raw_input()) )
        return x
    
class isFloat:
    def __init__(self):
        pass
  
    def refFuncWrapper(self):
        return self.refFunc( raw_input() )
    
    def refFunc(self,inp):
        if inp == "":
            return False
        inp = inp.strip()
        plusminus = ["+", "-"]
        if inp[0] in plusminus:
            inp = inp[1:]
        inp = inp.replace(".", "", 1)
        return inp.isdigit()  
    
    def inputFunc(self):
        x = lab1.isFloat( raw_input() )
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
    names = ["whichTriangle", "isFloat"]
    generate(names)