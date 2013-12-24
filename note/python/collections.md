collections 学习笔记
==========================
collections模块集结了Python中的高性能的容器数据类型，这些数据类型主要包括：namedtuple()、deque、Counter、OrderedDiect、defaultdict。他们作为替换内建（built-in）容器数据类型dict、list、set、tuple的可选方案。  

####namedtuple()  
namedtuple()是一个工厂函数,他是tuple的子类,用于创建一个轻量级的对象类型,它的作用就是将tuple封装成类(class)类型.它扩展了常规的元组,这样就可以通过名字来代替索引来访问field.它不需要更多的内存,,因为常规的tuple需要一个预实例字典.  

语法是这样的:  

    collections.namedtuple(typename, filed_names[, verbose])
地一个参数指定新类型的名字,第二个参数是字符串(用空格隔开)它构成了这个类型的域. 如果verbose等于True.那么就会打印出类生成信息.  

    >>> People = namedtuple("People",'age name', True)
    class People(tuple):
        'People(age, name)'
    
        __slots__ = ()
    
        _fields = ('age', 'name')
    
        def __new__(_cls, age, name):
            'Create new instance of People(age, name)'
            return _tuple.__new__(_cls, (age, name))
    
        @classmethod
        def _make(cls, iterable, new=tuple.__new__, len=len):
            'Make a new People object from a sequence or iterable'
            result = new(cls, iterable)
            if len(result) != 2:
                raise TypeError('Expected 2 arguments, got %d' % len(result))
            return result
    
        def __repr__(self):
            'Return a nicely formatted representation string'
            return 'People(age=%r, name=%r)' % self
    
        def _asdict(self):
            'Return a new OrderedDict which maps field names to their values'
            return OrderedDict(zip(self._fields, self))
    
        def _replace(_self, **kwds):
            'Return a new People object replacing specified fields with new values'
            result = _self._make(map(kwds.pop, ('age', 'name'), _self))
            if kwds:
                raise ValueError('Got unexpected field names: %r' % kwds.keys())
            return result
    
        def __getnewargs__(self):
            'Return self as a plain tuple.  Used by copy and pickle.'
            return tuple(self)
    
        __dict__ = _property(_asdict)
    
        def __getstate__(self):
            'Exclude the OrderedDict from pickling'
            pass
    
        age = _property(_itemgetter(0), doc='Alias for field number 0')
    
        name = _property(_itemgetter(1), doc='Alias for field number 1')
    
    
    >>> 
    >>> 
    >>> 
    >>> p = People(22,'zhsan')
    >>> p[0]
    22
    >>> p.age
    22
    >>> 
http://stackoverflow.com/questions/2970608/what-are-named-tuples-in-python
http://docs.python.org/2/library/collections.html?highlight=collections#collections.namedtuple

