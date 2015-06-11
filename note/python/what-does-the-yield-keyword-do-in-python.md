如何理解Python关键字yield
=======================
两年前开始接触Python，在[SO](http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python)上看到一篇关于`yield`的文章，讲解不错，于是尝试将其翻译成了中文，发布在[伯乐在线](http://python.jobbole.com/28506/#comment-93061)，后来译文收到了不少吐槽，于是两年后的今天对其文重新理解一篇，遂有了此文，译文加入了大量译注信息，帮助读者更好的理解。  
（译注：以下代码必须在Python3环境下运行）在理解*yield*之前，你需要明白生成器(generator)是什么？生成器又源自于迭代对象。  

####可迭代对象（Iterbles）
创建一个列表（list）时，你可以逐个地读取里面的每一项元素，这个过程称之为迭代（iteration）。  
    
    >>> mylist = [1, 2, 3]
    >>> for i in mylist:
    ...    print(i)
    1
    2
    3
*mylist*是一个可迭代对象。当使用列表推导式（list comprehension）创建了一个列表时，它就是一个可迭代对象：  
    
    >>> mylist = [x*x for x in range(3)]
    >>> for i in mylist:
    ...    print(i)
    0
    1
    4
任何可以使用在`for...in...`语句中的对象都可以叫做可迭代对象，例如：lists，strings，files等等。这些可迭代对象使用非常方便因为它能如你所愿的尽可能读取其中的元素，但是你不得不把所有的值存储在内存中，当它有大量元素的时候这并不一定总是你想要的。  

译者补充：dict对象以及任何实现了`__iter__()`或者`__getitem__()`方法的类都是可迭代对象，此外，可迭代对象还可以用在zip,map等函数中，当一个可迭代对象作为参数传递给内建函数`iter()`时，它会返回一个迭代器对象。通常没必要自己来处理迭代器本身或者手动调用`iter()`，`for`语句会自动调用`iter()`，它会创建一个临时的未命名的变量来持有这个迭代器用于循环期间。 为了更好的理解yield，译者引入了迭代器的介绍。  

####迭代器（iterator）
迭代器代表一个数据流对象，不断重复调用迭代器的`next()`方法可以逐次地返回数据流中的每一项，当没有更多数据可用时，`next()`方法会抛出异常**StopIteration**。此时迭代器对象已经枯竭了，之后调用`next()`方法都会抛出异常StopIteration.迭代器需要有一个`__iter()`方法用来返回迭代器本身。因此它也是一个可迭代的对象。



####生成器（Generators）
生成器也是一个迭代器，**但是你只可以迭代他们一次，不能重复迭代**，因为它并没有把所有值存储在内存中，而是实时地生成值：  
    
    >>> mygenerator = (x*x for x in range(3))
    >>> for i in mygenerator:
    ...    print(i)
    0
    1
    4
从结果上看用`()`代替`[]`效果是一样的，但是，你不可能第二次执行`for i in mygenerator`（译注：这里作者所表达的意思是第二次执行达不到期望的效果）因为生成器只能使用一次：首先计算出0，然后计算出1，最后计算出4。  

####Yield
**Yield**是关键字，它类似于**return**，只是函数会返回一个生成器。  
    
    >>> def createGenerator():
    ...    mylist = range(3)
    ...    for i in mylist:
    ...        yield i*i
    ...
    >>> mygenerator = createGenerator() # create a generator
    >>> print(mygenerator) # mygenerator is an object!
    <generator object createGenerator at 0xb7555c34>
    >>> for i in mygenerator:
    ...     print(i)
    0
    1
    4
    
这里的例子并没有什么实际用途，但是它很方便地让你知道当函数会返回一大批量数据时你只需要读取一次。为了完全弄懂**yield**，你必须清楚的是：**当函数被调用时，函数体中的代码是不会运行的**，函数仅仅是返回一个生成器对象。这里理解起来可能稍微有点复杂。函数中的代码每次会在`for`循环中被执行，接下来是最难的一部分：  
    
`for`第一次调用生成器对象时，代码将会从函数的开始处运行直到遇到`yield`为止，然后返回此次循环的第一个值，接着循环地执行函数体，返回下一个值，直到没有值返回为止。    
一旦函数运行再也没有遇到yield时，生成器就被认为是空的，有可能是因为循环终止，或者因为没有满足任何`if/else`。  

####控制生成器的穷举
    
    >>> class Bank(): # 创建银行，构建ATM机，只要没有危机，就可以不断地每次从中取100
    ...    crisis = False
    ...    def create_atm(self):
    ...        while not self.crisis:
    ...            yield "$100"
    >>> hsbc = Bank() # when everything's ok the ATM gives you as much as you want
    >>> corner_street_atm = hsbc.create_atm()
    >>> print(corner_street_atm.next())
    $100
    >>> print(corner_street_atm.next())
    $100
    >>> print([corner_street_atm.next() for cash in range(5)])
    ['$100', '$100', '$100', '$100', '$100']
    >>> hsbc.crisis = True # 危机来临，没有更多的钱了
    >>> print(corner_street_atm.next())
    <type 'exceptions.StopIteration'>
    >>> wall_street_atm = hsbc.create_atm() # 即使创建一个新的ATM，银行还是没钱
    >>> print(wall_street_atm.next())
    <type 'exceptions.StopIteration'>
    >>> hsbc.crisis = False # 危机过后，银行还是空的，因为该函数之前已经不满足while条件
    >>> print(corner_street_atm.next())
    <type 'exceptions.StopIteration'>
    >>> brand_new_atm = hsbc.create_atm() # 必须构建一个新的atm，恢复取钱业务
    >>> for cash in brand_new_atm:
    ...    print cash
    $100
    $100
    $100
    $100
    $100
    $100
    $100
    $100
    $100
    ...
对于类似资源的访问控制等场景，生成器显得很实用。  

####Itertools是你最好的朋友
itertools模块包含一些特殊的函数用来操作可迭代对象。曾经想复制一个生成器？两个生成器链接？在内嵌列表中一行代码处理分组？不会创建另外一个列表的Map/Zip函数？   
你要做的就是`import itertools`    
无例子无真相，我们来看看4匹马赛跑到达终点所有可能的顺序：    

    >>> horses = [1, 2, 3, 4]
    >>> races = itertools.permutations(horses)
    >>> print(races)
    <itertools.permutations object at 0xb754f1dc>
    >>> print(list(itertools.permutations(horses)))
    [(1, 2, 3, 4),
     (1, 2, 4, 3),
     (1, 3, 2, 4),
     (1, 3, 4, 2),
     (1, 4, 2, 3),
     (1, 4, 3, 2),
     (2, 1, 3, 4),
     (2, 1, 4, 3),
     (2, 3, 1, 4),
     (2, 3, 4, 1),
     (2, 4, 1, 3),
     (2, 4, 3, 1),
     (3, 1, 2, 4),
     (3, 1, 4, 2),
     (3, 2, 1, 4),
     (3, 2, 4, 1),
     (3, 4, 1, 2),
     (3, 4, 2, 1),
     (4, 1, 2, 3),
     (4, 1, 3, 2),
     (4, 2, 1, 3),
     (4, 2, 3, 1),
     (4, 3, 1, 2),
     (4, 3, 2, 1)]
####理解迭代的内部机制
迭代是操作可迭代对象（实现了`__iter__()`方法）和迭代器（实现了`__next__()`方法）的过程。可迭代对象是任何你可以从其得到一个迭代器对象的任意对象（译注：调用内建函数iter()），迭代器是能让你在可迭代对象上进行迭代的对象（译注：这里好绕，迭代器实现了`__iter__()`方法，因此它也是一个可迭代对象）。


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        