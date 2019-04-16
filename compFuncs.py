def CompFloats(a,b):
    try:
        a = float(a)
        b = float(b)
    except:
        return False
    return abs(a-b)<0.0005
#def compEqual(x,y):
#    print "x: ",x
#    print "y: ",y
#    return x==y

COMPFUNCS = []
COMPFUNCS.append(lambda x,y: x==y)
COMPFUNCS.append(CompFloats)

###COMPFUNCS = [equality, floats]
###INDICES =        0       1