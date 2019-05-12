# Python Autograder
=======

Python Autograder is a Python tool that for generating tests and autograding python labs.

## Dependencies:
=======

* code
* re
* pickle
* ttk
* tkMessageBox

## Installing
=======

Clone or download this github repository.

## Running the tests
=======

* In the same directory, copy the python script to be graded and name it "lab1.py"
* Run interface.py and add your test cases, and reference functions
* Run allTests.py

## Example
=======

 The following is an example for a reference function with a helper function.
 
 ```
 class incrAdd:

    def __init__(self):
        pass
    
    def refFuncWrapper(self):
        return self.refFunc(int(raw_input()), int(raw_input()))
        
    def refFunc(self,x,y):
        a,b = self.incrementHelper(x,y)
        return a + b
        
    def incrementHelper(self, x, y):
        return x+1,y+1
        
    def inputFunc(self):
        import lab1
        return lab1.incrAdd( int(raw_input()), int(raw_input()) )
```