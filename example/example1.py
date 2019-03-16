from xxx import x

@x.pattern
def length(lst):
    return (lst and True) or False

@length.match(False)
def _(lst): 
    """
    lst is []
    """
    return 0

@length.match(True)
def _(lst):
    return 1 + length(lst[1:])

m = 1000000
r = range(m)
import time
t1 = time.clock()
v = length(r)
t2 = time.clock()
x.debug(f"length( range({m}) )", v, t2 - t1)
