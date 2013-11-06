迭代器(Iterator)与生成器(Generator)的区别
=========================
迭代器是一个更抽象的概念，任何对象，如果它的类有next方法（__next__ python3)和__iter__方法返回自己本身。  

每个生成器都是一个迭代器，但是反过来不行。通常生成器是通过调用一个或多个yield表达式构成的函数s生成的。同时满足迭代器的定义。  

当你需要一个类除了有生成器的特性之外还要有一些自定义的方法时，可以使用自定义的迭代器，一般来说生成器更方便，更简单。  

    def squares(start, stop):
        for i in xrange(start, stop):
            yield i*i
等同于生成器表达式：  

    （i*i for i in xrange(start, stop))
列表推倒式是：  
    
    [i*i for i in xrange(start, stop)]

如果是构建一个自定义的迭代器：  

    class Squares(object):
        def __init__(self, start, stop):
            self.start = start
            self.stop = stop
        def __iter__(self):
            return self
        def next(self):
            if self.start >= self.stop:
                raise StopIteration
            current = self.start * self.start
            self.start += 1
            return current
此时，你还可以定义自己的方法如：  

    def current(self):
        return self.start

两者的相同点：对象迭代完后就不能重写迭代了。  

Iterables, Iterators, Genrators
==============================
热身一下
--------------
如果你是来自其它语言比如c，很自然想到的方式是创建一个计数器，然后以自增的方式迭代list。  

    my_list = [17  23  47  51  101  173  999  1001]
    
    i = 0
    while i < len(my_list):
        v = my_list[i]
        print v,
        i += 1
输出：  

    17 23 47 51 101 173 999 1001

也有可能会借用range，写一个类C语言的风格的for循环：  

    for i in range(len(my_list)):
        v = my_list[i]
        print v,
输出：  

    17 23 47 51 101 173 999 1001

上面两种方法都不是Pythonic方式，取而代之的是：  

    for v in my_list:
        print v,
输出：   

    17 23 47 51 101 173 999 1001

很多类型的对象都能通过这种方式来迭代，迭代字符串会生成单个字符：  

    for v in "Hello":
        print v,
输出：  

    H e l l o
迭代字典，生成字典的key（以无序的方式）：  

    d = {
        'a': 1,
        'b': 2,
        'c': 3,
        }
    
    for v in d:
        print v,
    # 注意这里是无序的

输出：  

    a c b

迭代文件对象，产生字符串行，包括换行符：  

    f = open("suzuki.txt")
    for line in f:
        print ">", line
输出：  

    > On education
    
    > "Education has failed in a very serious way to convey the most important lesson science can teach: skepticism."
    
    > "An educational system isn't worth a great deal if it teaches young people how to make a living but doesn't teach them how to make a life."

以上可以看出列表、元祖、字符串、字典、文件都可以迭代，能被迭代的对象都称为可迭代对象（Iteratbles)，for循环不是唯一接收Iteratbles的东东，还有：  

list构造器接收任何类型的Iteratbles，可以使用list()接收字典对象返回只有key的列表：  

    list(d)
输出：  

    ['a', 'c', 'b']
还可以：  

    list("Hello")
输出：  

    ['H', 'e', 'l', 'l', 'o']

还可以用在列表推倒式中：  

    ascii = [ord(x) for x in "Hello"]
    ascii
输出：  
    
    [72, 101, 108, 108, 111]

sum()函数接收任何数字类型的可迭代对象:  

    sum(ascii)

输出：  
    
    500

str.join()方法接收任何字符类型的可迭代对象 （这里的说法不严谨，总之原则是迭代的元素必须是str类型的)：  

    "-".join(d)
输出：  

    ‘a-c-b'






 http://stackoverflow.com/questions/2776829/difference-between-python-generators-vs-iterators
http://excess.org/article/2013/02/itergen1/
