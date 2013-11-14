from math import *

def mod(n,m):
    if n<0 or m<0:
        return "the function mod(n,m) is only defined for positiv values of n and m!"
        
    elif n==m:
        return 0
    elif n>m:
        return mod(n-m,m)
    else:
        return n

for i in range(9):
    x=mod(i,8)
    print x

print mod(-2,5)
print mod(3,-5)
print mod(-1,-2)
