class whichTriangle:
    '''add your imports here
    if there are no imports, uncomment pass'''
    def __init__(self):
        import math
        ##add more imports
        #pass
    
    '''this function is a wrapper around the reference function
    Add input parameters and cast them to their types.
    DONOT CHANGE THE NAME OF THE FUNCTION'''
    def refFuncWrapper(self):
        return self.refFunc( int(raw_input()), int(raw_input()), int(raw_input()) ) #add more parameters here
 
    '''this is the reference function. Add input parameters and change function
    body. DONOT CHANGE THE NAME OF THE FUNCTION. You can change the names of 
    the input parameters'''
    def refFunc(self,a,b,c):
        return 77
        if a <= 0 or b <= 0 or c <= 0: # sides are negative
            return 0
        if ((a+b)<=c or (a+c)<=b or (b+c)<=a): # sides don't add up
            return 0
        # Right triangle
        if (a**2+b**2)==c**2 or (a**2+c**2)==b**2 or (b**2+c**2)==a**2:
            return 1
        if a==b and b==c: # Equilateral triangles
            return 3
        if self.isObtuse(a,b,c) and not self.isIsosceles(a,b,c): # Obtuse scalene triangle
            return 4
        if self.isObtuse(a,b,c) and self.isIsosceles(a,b,c): # Obtuse isosceles triangle
            return 5
        if self.isAcute(a,b,c) and not self.isIsosceles(a,b,c): # Acute scalene triangle
            return 6
        if self.isAcute(a,b,c) and self.isIsosceles(a,b,c): # Acute isosceles triangle
            return 7    
            
    def isAcute(self,a,b,c):
        if (a**2+b**2)>c**2 or (a**2+c**2)>b**2 or (b**2+c**2)>a**2:
            return True
        return False 
        
    def isObtuse(self,a,b,c):
        if (a**2+b**2)<c**2 or (a**2+c**2)<b**2 or (b**2+c**2)<a**2:
            return True
        return False
        
    def isIsosceles(self,a,b,c):
        if a==b or b==c or a==c:
            return True
        return False

        
                 
    '''THIS SHOULD BE SIMILAR TO refFuncWrapper. This will be used to call
    the function that is being graded. DONOT CHANGE ANYTHING OTHER THAN
    THE INPUT PARAMETERS'''
    def inputFunc(self):
        import lab1
        return lab1.whichTriangle( int(raw_input()), int(raw_input()), int(raw_input()) )


class isFloat:
    '''add your imports here
    if there are no imports, uncomment pass'''
    def __init__(self):
        ##add more imports
        pass
    
    '''this function is a wrapper around the reference function
    Add input parameters and cast them to their types.
    DONOT CHANGE THE NAME OF THE FUNCTION'''
    def refFuncWrapper(self):
        return self.refFunc( raw_input() ) #add more parameters here
 
    '''this is the reference function. Add input parameters and change function
    body. DONOT CHANGE THE NAME OF THE FUNCTION. You can change the names of 
    the input parameters'''
    def refFunc(self,string):
    
        string = self.clearSpace(string)
        # Clear signs on the first character
        if string[0] == '+' or string[0] == '-':
            string = string[1 : len(string)]
        # Check dot
        dotPos = [] #stores the indices of dot
        for i in range(len(string)):
            if string[i] == '.':
                dotPos.append(i)
        if len(dotPos) > 1: #there should not be more than 1 dot
            return False
        # Check if are numbers or dot
        numbers = ['0','1','2','3','4','5','6','7','8','9','.']
        for character in string:
             if character not in numbers:
                 return False
        return True
 
    def clearSpace(self, string): # clear leading and trailing spaces
        # Clear spaces in front the number
        isSpace = True
        counter = 0
        while(isSpace and counter<len(string)):
            if string[counter] == ' ':
                counter += 1
            else:
                isSpace = False
        string = string[counter:len(string)]
        # Clear spaces trailing the number
        isSpace = True
        counter = len(string) - 1
        while(isSpace and counter > 0): # no need to check string[0]
            if string[counter] == ' ':
                counter -= 1
            else:
                isSpace = False
        string = string[0:counter+1] 
        return string
 
 
 
    '''THIS SHOULD BE SIMILAR TO refFuncWrapper. This will be used to call
    the function that is being graded. DONOT CHANGE ANYTHING OTHER THAN
    THE INPUT PARAMETERS'''
    def inputFunc(self):
        import lab1
        return lab1.isFloat( raw_input() )
