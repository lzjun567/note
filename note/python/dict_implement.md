Python 字典数据类型（dict）源码分析
================================
字典类型是Python中最常用的数据类型之一，它是一个键值对的集合，字典通过键来索引，关联到相对的值，理论上它的查询复杂度是 O(1) ：   
    
    >>> d = {'a': 1, 'b': 2}
    >>> d['c'] = 3
    >>> d
    {'a': 1, 'b': 2, 'c': 3}

通过key来访问value：  
    
    >>> d['a']
    1
    >>> d['b']
    2
    >>> d['c']
    3
    >>> d['d']
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    KeyError: 'd'

遇到不存在的key就会出现异常KeyError，当然也可以使用`d.get('d')`的方式默认返回`None`值。 那么字典的内部结构是怎样的呢？  

####哈希表 (hash tables)
哈希表（也叫散列表），根据关键值对(Key value)而直接进行访问的数据结构。它通过把key和value映射到表中一个位置来访问记录，这种查询速度非常快，更新也快。这个映射函数叫做哈希函数，存放值的数组叫做哈希表。  

1. 数据添加过程：把key通过哈希函数转换成一个整型数字，然后就将该数字对数组长度进行取余，取余结果就当作数组的下标，将value存储在以该数字为下标的数组空间里。  
2. 数据查询过程：再次使用哈希函数将key转换为对应的数组下标，并定位到数组的位置获取value。

但是，对key进行hash的时候，不同的key可能hash出来的结果是一样的，那么就使用链表的数组法来表示。  

Python 的字典结构就是使用哈希表结构来实现的。一个好的hash函数应最小化冲突的数量，

解决哈希表发生碰撞的方法：开放寻址法，链接法。  

####开放寻址法(open addressing)


















http://www.cnblogs.com/michaelyin/archive/2011/02/14/1954724.html
http://www.laurentluce.com/posts/python-dictionary-implementation/

http://stackoverflow.com/questions/327311/how-are-pythons-built-in-dictionaries-implemented








