def efunc(x,n):
    """ 
    defined only for positive values of n
    calculate the function x^n recursivly 
    """

    if n>0:
        return efunc(x,n-1)*x
    elif n==0:
        return 1
    else:
        return "the function efunc(x,n) is only defined for posaitive values of n!"


# +++ Exercise: Refactor the following code
# $$$ for example write function(s) and general parameters

for i in range(4):
    print "2^" + str(i) + " = " + str(efunc(2,i))
print
for i in range(4):
    print str(i) + "^2" + " = " + str(efunc(i,2))
print
for i in range(4):
    print str(i) + "^" + str(i) + " = " + str(efunc(i,i))
print


print efunc(2,-1)
print efunc(-2,3)

# +++ Exercises for advanced programmers:
# +++ 1) write for the case n<0 an erroracception/errorhandling. 
# +++ 2) write a unittest testcase for the function efunc().
# +++ 3) improve efunc(x,n) so that negative n are also defined.

# lapstore.de
