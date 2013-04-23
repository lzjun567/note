yield：生成器
----------------
任何使用yield的函数都称之为生成器，如：  

    def count(n):
        while n > 0:
            yield n   #生成值：n
            n -= 1
另外一种说法：生成器就是一个返回迭代器的函数，与普通函数的区别是生成器包含yield语句，更简单点理解生成器就是一个迭代器。   

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

在调用count函数时：c=count(5)，并不会打印"counting"只有等到调用c.next()时才真正执行里面的语句。每次调用next()方法时，count函数会运行到语句` yield n`处为止，next()的返回值就是生成值`n`，再次调用next()方法时，函数继续执行yield之后的语句（熟悉Java的朋友肯定知道Thread.yield()方法，作用是暂停当前线程的运行，让其他线程执行），如：

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
            line = f.readline()  #读取文件中新的文本行
            if not line:
                time.sleep(0.1)
                continue
            yield line
    
    def grep(lines,searchtext):
        for line in lines:
            if searchtext in line:
                yield line


调用：  

    flog = tail(open('warn.log'))
    pylines = grep(flog,'python')
    for line in pylines:
        print line,

用yield实现斐波那契数列：  

    def fibonacci():
        a=b=1
        yield a
        yield b
        while True:
            a,b = b,a+b
            yield b

调用：  

    for num in fibonacci():
        if num > 100:
            break
        print num,

yield中return的作用：  
作为生成器，因为每次迭代就会返回一个值，所以不能显示的在生成器函数中return 某个值，包括None值也不行，否则会抛出“SyntaxError”的异常，但是在函数中可以出现单独的return，表示结束该语句。  
通过固定长度的缓冲区不断读文件，防止一次性读取出现内存溢出的例子：  

    def read_file(path):
        size = 1024
        with open(path,'r') as f:
            while True:
                block = f.read(SIZE)
                if block:
                    yield block
                else:
                    return

如果是在函数中return 具体某个值，就直接抛异常了  

    >>> def test_return():
    ...      yield 4
    ...      return 0
    ...
      File "<stdin>", line 3
    SyntaxError: 'return' with argument inside generator


与yield有关的一个很重要的概念叫**协程**，下次好好研究研究。  

参考：
http://www.cnblogs.com/huxi/archive/2011/07/14/2106863.html  
http://www.ibm.com/developerworks/cn/opensource/os-cn-python-yield/
《Python 参考手册》

