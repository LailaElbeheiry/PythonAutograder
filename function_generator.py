# -*- coding: utf-8 -*-
"""
@author: LailaElbeheiry
"""


import math
import lab1

#############This file should be editted to generate the autograding files
###In line 31, insert the function names in the list "names"

###In line 33, insert the name of the first function

###In lines 38 and 44, edit the function refFunWrapper, so that it correctly  
#casts the input to the actual input types

###In line 41, edit the refFun so that it has the body for the reference function 
#for that particular class

###Run this file to generate the autograders for each function

####Check the file template_generator.py for reference


###


#####################################################################################
####THIS PART SHOULD BE EDITTED AS DESCRIBED ABOVE
names = ["insert function 1 name", "insert function 2 name"]

class insertClass1Name:
    def __init__(self):
        pass
        
    def refFuncWrapper(self):
        return self.refFunc( int(raw_input()), int(raw_input()), int(raw_input()) )
    
    def refFunc(self,inp1,inp2,inp3):
        return "insert reference function body"
    
    def inputFunc(self):
        x =  lab1.whichTriangle( int(raw_input()), int(raw_input()), int(raw_input()) )
        return x
    
#####################################################################################


####THIS PART SHOULD NOT EDITTED AS DESCRIBED ABOVE
def generate(names):
    src = open("source.py")
    srcLines = list(map(lambda x: x.rstrip('\0'), src.readlines()))
    for name in names:
        f = open(name + ".py", 'w')
        srcLines[1] = "from functionGenerator import " + name + " as s"
        f.writelines(srcLines)
        f.close()   
        
if __name__ == "__main__":
    generate(names)    
    
