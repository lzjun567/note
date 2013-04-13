生成器
----------------
任何使用yield的函数都称之为生成器，如：  

    def count(n):
        while n > 0:
            yield n   #生成值：n
            n -= 1
使用yield，可以让函数生成一个序列，该函数返回的对象类型是"generator"，通过该对象连续调用next()方法返回序列值。  

    c = count(5)
    c.next()
    >>> 5
    c.next()
    >>>4

生成器函数只有在调用next()方法的时候才开始执行函数里面的语句，比如：  

    def count(n):
        print "cunting"
        while n > 0:
            yield n   #生成值：n
            n -= 1

在调用count函数时：c=count(5)，并不会打印"counting"只有等到调用c.next()时才真正执行里面的语句。每次调用next()方法时，count函数会运行到语句` yield n`处为止，next()的返回值就是生成值`n`，再次调用next()方法时，函数继续执行yield之后的语句，如：

    def count(n):
        print "cunting"
        while n > 0:
            print 'before yield'
            yield n   #生成值：n
            n -= 1
            print 'after yield'
上述代码在第一次调用next方法时，并不会打印"after yield"。如果一直调用next方法，当执行到没有可迭代的值后，程序就会报错：  
>>> Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  StopIteration

所以一般不会手动的调用next方法，而使用for循环：  

    for i in count(5):
        print i,


实例：  用yield生成器模拟Linux中命令：`tail -f | grep python` 用于查找监控日志文件中出现有python字样的行。  

import time
def tail(f):
    f.seek(0,2)#移动到文件EOF，参考：[seek](http://docs.python.org/2/library/stdtypes.html?highlight=file#file.seek)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def grep(lines,searchtext):
    for line in lines:
        if searchtext in line:
            yield line

