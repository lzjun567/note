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

你可能认为它执行的过程先是：`1 < x`，返回`True`，然后再比较`True < 10`,当然这么做也是返回`True`,因为比较表达式`True < 10`,解释器会把`True`转换成`1`，`False`转换成`0`。但是解释器内部并不是这样干，它会把这种链式的比较操作转换成：`1 < x and x < 10`，不信你可以看看最后一个例子。它本可以值得所有编程语言拥有，但是很遗憾  

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
callable函数会一直被调用，直到它返回sentinel，例如：  

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
