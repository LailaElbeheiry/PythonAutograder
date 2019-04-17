def CompFloats(a,b):
    try:
        a = float(a)
        b = float(b)
    except:
        return False
    return abs(a-b)<0.0005


COMPFUNCS = []
COMPFUNCS.append(lambda x,y: x==y)
COMPFUNCS.append(CompFloats)
