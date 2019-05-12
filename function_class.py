class isFloat:
    '''add your imports here
    if there are no imports, uncomment pass'''
    def __init__(self):
        import math
        ##add more imports
        #pass
    
    '''this function is a wrapper around the reference function. Add input parameters 
    and cast them to their types. You can add helper functions as part of the class. 
    Check example in github. DONOT CHANGE THE NAME OF THE FUNCTION'''
    def refFuncWrapper(self):
        return self.refFunc( int(raw_input()) ) #add more parameters here
 
    '''this is the reference function. Add input parameters and change function
    body. DONOT CHANGE THE NAME OF THE FUNCTION. You can change the names of 
    the input parameters'''
    def refFunc(self,inp1,inp2,inp3):
        return "insert reference function body" #add reference function here
 
    '''THIS SHOULD BE SIMILAR TO refFuncWrapper. This will be used to call
    the function that is being graded. DONOT CHANGE ANYTHING OTHER THAN
    THE INPUT PARAMETERS'''
    def inputFunc(self):
        import lab1
        return lab1.isFloat( int(raw_input()) )

       
