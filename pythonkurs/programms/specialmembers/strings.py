# zk = zeichenkette
zk = 'string'
# b = buchstabe
for i in range(len(zk)):
    b= zk[i]
    print "index: " + str(i) + " , ist der " + str(i+1) + ".te Buchstabe von dem Wort " + zk + ": "  + b

# explaination:
# * i is called an index
# * len(string) is a build-in-function returns the number of characters in a string.
# compere the output of the following printstatement:

print "\n das Wort \"" + zk + "\" besteht aus " + str(len(zk)) + " Buchstaben."

# what happens by using negative integers as index?
# compere with the following print-statement:

print "\n"
i=-1
while i >= -len(zk):
    print zk[i]
    i -= 1
