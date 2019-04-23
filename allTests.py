"""
This file runs the autograders on all the functions in the file lab1
REQUIREMENTS:
This program assumes that the user has already run interface.py and
generated the corresponding test files.
The file which has the solutions (i.e. being graded) should be named
"lab1.py"
Modify and run the file function_generator.py before running this file
"""


import subprocess
import os.path
import struct
import signal
import json
import re
import threading
import compFuncs



class TestClass():
    def __init__(self):
        self.name = None
        self.fail = None
        self.success = None
        self.timeout = None
        self.compFunc = None
        self.testCases = None
        self.scorePerCase = None
    #for debugging purposes
    def __str__(self):
        s= "name:" + str(self.name) + "\nfail: " + str(self.fail) 
        + "\nsuccess: " + str(self.success) + "\ntimeout: " + str(self.timeout)
        + "\ntestCases: " 
        t =""
        for tc in self.testCases:
            t+= "\n" + str(tc)
        t+= "\ntotal " + str(self.scorePerCase)      
        return s + t
                
                
##a class for individual test cases        
class TestCase():
    def __init__(self):
        self.argList = None
        self.score = None
    #for debugging purposes
    def __str__(self):
        return "argList: " + str(self.argList) + "\nscore: " + str(self.score) 




meta = open("metadata.txt")
QUESTIONS = []
lines = meta.readlines()
for i in range(0,len(lines),2):
    QUESTIONS.append((lines[i].strip(),lines[i+1].strip()))

class Alarm(Exception):
        pass

def timeoutFunc ( p ):
        if p.poll() == None:
                try:
                        p.kill()
                        print "timed out"
                except:
                        pass
###CITATION: https://stackoverflow.com/questions/28401547/how-to-remove-comments-from-a-string        
def commentStrip(s):
    m = re.match(r'^([^#]*)#(.*)$', s)
    if m:  # The line contains a hash / comment
        s = m.group(1) 
    return s.strip()     

def ReadLine(f):
    line = f.readline()
    while line[0]=="#":
        line = f.readline()
    return line

def customSplit(arg):
    argList = []
    x = arg
    l = x.count(r'"')
    l = l/2
    for i in range(l):
        start = x.index(r'"')
        y = x[:start]
        if y!="":
            L = list(filter(lambda s: re.search("\s",s)==None 
                            and re.search(".",s)!=None
                            , re.split("\s",x[:start])))
            argList.extend(L)
        x = x[start+1:]
        end = x.index(r'"')
        argList.append(x[:end])
        x = x[end+1:]
    L = list(filter(lambda s: re.search("\s",s)==None 
                    and re.search(".",s)!=None
                    , re.split("\s",x)))
    argList.extend(L)    
    return argList
    

def runTest ( name, argList, timeout, compFunc,functionNum=0):
    #inpfile contains the input args for the test case
    #it writes it twice once for the ref and once for the test
    inpfile = open("input.txt","w") 
    for i in argList:
        inpfile.write(str(i)+"\n")
    for i in argList:
        inpfile.write(str(i)+"\n")        
    inpfile.close()
    
    #create a subprocess and run the function
    #run executable with a timeout managed by SIGALRM
    try:
        proc_id = subprocess.Popen("python "+name+".py",
                                   stderr=subprocess.PIPE,
                                   stdout=open("output.txt", "w"),
                                   stdin=open("input.txt","r"),
                                   shell=True)
        t = threading.Timer ( timeout,  timeoutFunc, [proc_id] )
        t.start ( )
        proc_id.wait()
        t.cancel ( )
        output = proc_id.returncode;
        
    #timeout error
    except Alarm:
        output = STATUS_TIMEOUT()
        proc_id.kill()

    #the return value of the function should be in output.txt
    out = open("output.txt","r")
    lines = map(lambda s: s.strip(), out.readlines())
    linesRef = lines[0:lines.index("|")+1] 
    linesTest = lines[lines.index("|")+1:] 
    lines = linesTest
    out.close ()
    
    #if the output was non-empty
    if (len ( lines ) > 0):
        #if there is a comp function then compare the output with the
        #reference output using comp, otherwise compare them using equality
        if compFunc != None:
            if compFunc ( str(lines[0]).rstrip('\n'), linesRef[0] ):
                return 1
        else:
            if str(lines[0]).rstrip('\n') == linesRef[0]:
                return 1
    return 0


#categories is a list of instances of the test category class
def runTestCases (categories):
    totalPts = 0
    for category in categories:
        name = category.name
        failMsg = category.fail
        successMsg = category.success
        timeout = category.timeout
        compFunc = category.compFunc
        cases = category.testCases
        scorePerCase = category.scorePerCase
        scores = []
        for case in cases:
            argList = case.argList
            if runTest(name, argList, timeout, compFunc) == 0:
                scores.append(0)
            else:
                scores.append(scorePerCase)
        totalPts += sum(scores)
        if sum(scores) < scorePerCase*len(cases):
            print failMsg
        else:
            print successMsg
    return totalPts

def testAll():
#    pointsEarned = [0] * len(QUESTIONS)
    result = dict ( )
    total = 0
    for qf in QUESTIONS:
        f = qf[1]
        q = qf[0]
        categories = []
        tests = open(q+".txt")
        name = q
        numClasses = int(commentStrip(ReadLine(tests)))
        for i in range(numClasses):
            cat = TestClass()
            cat.name = name
            cat.fail = commentStrip(ReadLine(tests))
            cat.success = commentStrip(ReadLine(tests))
            cat.timeout = int(commentStrip(ReadLine(tests)))
            cat.compFunc = compFuncs.COMPFUNCS[int(commentStrip(ReadLine(tests)))]
            cat.scorePerCase = float(commentStrip(ReadLine(tests)))
            cases = []
            numCases = int(commentStrip(ReadLine(tests)))
            for c in range(numCases):
                case = TestCase()
                case.argList = customSplit((ReadLine(tests)))
                cases.append(case)
            cat.testCases = cases
            categories.append(cat)

        print "Grading " + f
        print "\n"
        res = float(runTestCases(categories))     
        result[f] = res
        total += res
    
    print json.dumps({'scores': result,'scoreboard': [total,total]})
    
testAll()
        
                

            
      
            
            
        
    
    








