Python 奇技淫巧
-----------------
本文整理自SO上的热门问答[hidden features of python](http://stackoverflow.com/questions/101268/hidden-features-of-python?rq=1)，早期有人做过类似的整理，但是内容比较旧而且比较粗糙，因此笔者在原文基础上加入自己的一些理解，另外那些高质量的评论也引入进来了。总之，这是一篇用心之作，希望你可以喜欢。
####链式比较操作

    >>> x = 5
    >>> 1 < x < 10
    True
    >>> 10 < x < 20 
    False
    >>> x < 10 < x*10 < 100
    True
    >>> 10 > x <= 9
    True
    >>> 5 == x > 4
    True

你可能认为它执行的过程先是：`1 < x`，返回`True`，然后再比较`True < 10`,当然这么做也是返回`True`,比较表达式`True < 10`,因为解释器会把`True`转换成`1`，`False`转换成`0`。但这里的链式比较解释器在内部并不是这样干的，它会把这种链式的比较操作转换成：`1 < x and x < 10`，不信你可以看看最后一个例子。这样的链式操作本可以值得所有编程语言拥有，但是很遗憾  

####枚举

    >>> a = ['a', 'b', 'c', 'd', 'e']
    >>> for index, item in enumerate(a): print index, item
    ...
    0 a
    1 b
    2 c
    3 d
    4 e
    >>>
用enumerate包装一个可迭代对象,可以同时使用迭代项和索引，如果你不这么干的话，下面有一种比较麻烦的方法：  

    for i in range(len(a)):
        print i, a[i]

enumerate 还可以接收一个可选参数start，默认start等于0。`enumerate(list, start=1)`，这样index的起始值就是1  

####生成器对象

    x=(n for n in foo if bar(n))  #foo是可迭代对象
    >>> type(x)
    <type 'generator'>
你可以把生成器对象赋值给x，意味着可以对x进行迭代操作：  

    for n in x:
        pass
它的好处就是不需要存储中间结果，也许你会使用（列表推倒式）：  

    x = [n for n in foo if bar(n)]
    >>> type(x)
    <type 'list'>
它比生成器对象能带来更快的速度。相对地，生成器更能节省内存开销，它的值是按需生成，不需要像列表推倒式一样把整个结果保存在内存中，同时它不能重新迭代，列表推倒式则不然。  

####iter()可接收callable参数
iter()内建函数接收的参数分为两种，第一种是：  
    
    iter(collection)---> iterator
参数collection必须是可迭代对象或者是序列 ，第二种是：  

    iter（callable， sentinel) --> iterator
callable函数会一直被调用，直到它的返回结果等于sentinel，例如：  

    def seek_next_line(f):
        #每次读一个字符，直到出现换行符就返回
        for c in iter(lambda: f.read(1),'\n'):  
            pass

####小心可变的默认参数

    >>> def foo(x=[]):
    ...     x.append(1)
    ...     print x
    ... 
    >>> foo()
    [1]
    >>> foo()
    [1, 1]
    >>> foo()
    [1, 1, 1]

取而代之的是你应该使用一个标记值表示“没有指定”来替换可变值,如：  

    >>> def foo(x=None):
    ...     if x is None:
    ...         x = []
    ...     x.append(1)
    ...     print x
    >>> foo()
    [1]
    >>> foo()
    [1]

####发送值到生成器函数在中

    def mygen():
        """Yield 5 until something else is passed back via send()"""
        a = 5
        while True:
            f = (yield a) #yield a and possibly get f in return
            if f is not None: 
                a = f  #store the new value
你可以：  

    >>> g = mygen()
    >>> g.next()
    5
    >>> g.next()
    5
    >>> g.send(7)  #we send this back to the generator
    7
    >>> g.next() #now it will yield 7 until we send something else
    7

如果你不喜欢使用空格缩进，那么可以使用C语言花括号{}定义函数：  

    >>> from __future__ import braces   #这里的braces 指的是：curly braces（花括号）
      File "<stdin>", line 1
    SyntaxError: not a chance

当然这仅仅是一个玩笑，想用花括号定义函数？没门。感兴趣的还可以了解下：  

    from __future__ import barry_as_FLUFL

不过这是python3里面的特性，http://www.python.org/dev/peps/pep-0401/  

####切片操作中的步长参数

    a = [1,2,3,4,5]
    >>> a[::2]  # iterate over the whole list in 2-increments
    [1,3,5]
还有一个特例：`x[::-1]`，反转列表：  

    >>> a[::-1]
    [5,4,3,2,1]
有关反转，还有两个函数reverse、reversed，reverse是list对象的方法，没有返回值，而reversed是内建方法，可接收的参数包括tuple、string、list、unicode，以及用户自定义的类型，返回一个迭代器。  

    >>> l = range(5)
    >>> l
    [0, 1, 2, 3, 4]
    >>> l.reverse()
    >>> l
    [4, 3, 2, 1, 0]
    >>> l2 = reversed(l)
    >>> l2
    <listreverseiterator object at 0x99faeec>
####装饰器
装饰器使一个函数或方法包装在另一个函数里头，可以在被包装的函数添加一些额外的功能，比如日志，还可以对参数、返回结果进行修改。装饰器有点类似Java中的AOP。下面这个例子是打印被装饰的函数里面的参数的装饰器，  

    >>> def print_args(function):
    >>>     def wrapper(*args, **kwargs):
    >>>         print 'Arguments:', args, kwargs
    >>>         return function(*args, **kwargs)
    >>>     return wrapper
    
    >>> @print_args
    >>> def write(text):
    >>>     print text
    
    >>> write('foo')
    Arguments: ('foo',) {}
    foo

@是语法糖，它等价于：  

    >>> write = print_args(write)
    >>> write('foo')
    arguments: ('foo',) {}
    foo

####for ... else语法

    for i in foo:
        if i == 0:
            break
    else:
        print("i was never 0")
else代码块只有在for循环结束后或者break语句后执行，等价于下面：  

    found = False
    for i in foo:
        if i == 0:
            found = True
            break
    if not found: 
        print("i was never 0")
不过这种语法看起来怪怪地，让人感觉是else块是在for语句块没有执行的时候执行的，很容易让人去类比 if else 的语法，如果是把else换成finally或许更容易理解    

####python2.5有个`__missing__`方法
dict的子类如果定义了方法`__missing__(self, key)`，如果key不再dict中，那么d[key]就会调用`__missing__`方法，而且d[key]的返回值就是`__missing__`的返回值。  

    >>> class MyDict(dict):
    ...  def __missing__(self, key):
    ...   self[key] = rv = []
    ...   return rv
    ... 
    >>> m = MyDict()
    >>> m["foo"].append(1)
    >>> m["foo"].append(2)
    >>> dict(m)
    {'foo': [1, 2]}

在collections模块下有一个叫defaultdict的dict子类，它与missing非常类似，但是对于不存在的项不需要传递参数。  

    >>> from collections import defaultdict
    >>> m = defaultdict(list)
    >>> m["foo"].append(1)
    >>> m["foo"].append(2)
    >>> dict(m)
    {'foo': [1, 2]}

####交换值

    >>> a = 10
    >>> b = 5
    >>> a, b
    (10, 5)
    
    >>> a, b = b, a
    >>> a, b
    (5, 10)
    

