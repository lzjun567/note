class Test(object):
    def __init__(self, a):
        print 'init'
        print a
    def __call__(self, a,b):
        print 'call'
        print a,b


t = Test(3)
print (Test)
print type(t)

print(t(4,5))

