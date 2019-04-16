
from functionGenerator import SetDigit as s

f = s()


def test():
        refFuncWrapper = f.refFuncWrapper
        testClasses = f.generateTests()

        #[THIS FILE, timeout, num cases (AUTO)]
        retVal = [f.name, f.timeout, len ( testClasses )]
        for i in testClasses:
                retVal.append (i[0]) # the test calss error
                retVal.append (i[1])
                retVal.append (i[2])
        for _i in range ( 0, len ( testClasses ) ):
                i = testClasses[_i]
                for j in range ( 3, len ( i ) ):
                        #MODIFY FOR INPUT OF FUNCTION
                        retVal += [  [_i, refFuncWrapper ( i[j] )] + i[j] ]


        #first 3 elements: name of THIS file, timeout in seconds, number of test classes
        #rest: lists, each one containing: [test class index,, reference output test input]
        return retVal

if __name__ == "__main__":
    print f.refFuncWrapper()
    print "|"
    print f.inputFunc()    
