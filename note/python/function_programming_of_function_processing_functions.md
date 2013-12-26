函数式编程-----序列处理函数:map(),filter(),reduce()
----------------------------
####map(function, sequence[, ...]) → list  

创建一个新的列表,函数作用于原来列表中的每个元素  

    >>> map( int, [ "10", "12", "14", 3.1415926, 5L ] )
    [10, 12, 14, 3, 5]
这个函数等效下面这个定义:  
    
    def map(function, sequence):
        return [function(v) for v in sequence]
map函数可以接收多个序列,如果是这种情况的话,function必须接收多个参数,参数的个数必须和序列的个数保持一致.如果function=None, 那么返回的列表是有tuple构成的列表  

    >>>map(None, range(3), range(3))
    [(0, 0), (1, 1), (2, 2)]

####filter(function, sequence) → list 
返回列表对象,它的sequence元素中作用在function函数中返回True的元素,如果function是None,那么就是sequence中元素等于True的元素.它的行为定义类似于:  

    def filter( aFunction, aSequence ):
        return [ v for v in aSequence if aFunction(v) ]
例子:  

    >>> import random
    >>> rolls = list( (random.randint(1,6),random.randint(1,6)) for u in range(100) )
    >>> def hardways( pair ):
    ...     d1, d2 = pair
    ...     return d1 == d2 and d1+d2 in ( 4, 6, 8, 10 )
    >>> filter( hardways, rolls )
    [(4, 4), (5, 5), (2, 2), (5, 5), (4, 4), (5, 5), (5, 5), (3, 3), (2, 2), (2, 2), (5, 5), (4, 4)]
    >>> len(_)
    12
####reduce(function, sequence[, initial=0]) → value
function必须接收两个参数, function在内部累加sequence中的每个元素,到最后变成一个单一的value.  

    def reduce( aFunction, aSequence, init= 0 ):
        r= init
        for s in aSequence:
            r= aFunction( r, s )
        return r
例子:  

    >>> def plus( a, b ):
    ...     return a+b
    >>> reduce( plus, [1, 3, 5, 7, 9] )
    25
python的built-in函数中如:sum(),any(),all()都是类似的reduce函数.  

####zip(sequence[, sequence...]) → sequence
zip接收的参数都是序列,他把多个序列便成一个序列,新序列是tuple的集合.如果其中一个序列太长那就就会被截取.  
例子:  

    >>> zip( range(5), range(1,12,2) )
    [(0, 1), (1, 3), (2, 5), (3, 7), (4, 9)]
这个例子中,前面序列range(5)的长度是5, 后面序列的长度是6,最终长的序列会被截取掉.  当map的地一个参数function是None时,其功能与zip类似,但是map不是截取,而是对较短的序列用None填充.  

    >>> map(None, range(5), range(1,12,2))
    [(0, 1), (1, 3), (2, 5), (3, 7), (4, 9), (None, 11)]

http://www.itmaybeahack.com/book/python-2.6/html/p02/p02c10_adv_seq.html

