####什么是描述符（descriptor）
简单来讲，描述符是一个Python对象，这个对象比较特殊，特殊性在于其**属性**的访问方式不再像普通对象那样访问，它通过一种叫描述符协议的方法来访问。这些方法是`__get__`、`__set__`、`__delete__`。定义了其中任意一个方法的对象都叫描述符。举个例子：  
**普通对象**  

    class Parent(object):
        name = 'p'
    
    class Person(Parent):
        name = "zs"
    
    zhangsan = Person()
    zhangsan.name = "zhangsan"
    print zhangsan.name
    #>> zhangsan
    
普通的Python对象操作（get，set，delete）属性时都是在这个对象的`__dict__`基础之上操作的。比如上例中它在访问属性`name`的方式是通过如下顺序去查找，直到找到该属性位置，如果在父类中还没找到那么就抛异常了。  

1. `zhangsan.__dict__['name']`
2. `type(zhangsan).__dict__['name'] 等价于 Person.__dict__['name']`
3. `zhangsan.__class__.__base__.__dict__['name']  等价于  Parent.__dict__['name']`

通过dict的方式修改属性name的值：  
    
    zhangsan.__dict__['name'] = 'lisi'
    print zhangsan.name
    #>> lisi


**描述符**  

    class DescriptorName(object):
        def __init__(self, name):
            self.name = name
    
        def __get__(self, instance, owner):
            print '__get__', instance, owner
            return self.name
    
        def __set__(self, instance, value):
            print '__set__', instance, value
            self.name = value
    
    
    class Person(object):
        name = DescriptorName('zhangsan')
    
    
    zhangsan = Person()
    print zhangsan.name
    #>>__get__ <__main__.Person object at 0x10bc59d50> <class '__main__.Person'>
    #>>zhangsan

这里的DescriptorName就是一个描述符，访问Person对象的name属性时不再是通过`__dict__`属性来访问的，而是通过调用DescriptorName的`__get__`方法获取的，同样的道理，给name赋值的时候是通过调用`__set__`方法实现而不是通过`__dict__`属性。  

    zhangsan.__dict__['name'] = 'lisi'
    print zhangsan.name
    #>>__get__ <__main__.Person object at 0x10bc59d50> <class '__main__.Person'>
    #>>zhangsan
    
    zhangsan.name = "lisi"
    print zhangsan.name
    #>>__set__ <__main__.Person object at 0x108b35d50> lisi
    #>>__get__ <__main__.Person object at 0x108b35d50> <class '__main__.Person'>
    #>>lisi

类似地，删除属性的值也是通过调用`__delete__`方法完成的。此时，你有没有发现描述符似曾相识，没错，用过Django就知道在定义model的时候，就用到了描述符。
    
    from django.db import models
    
    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published') 



那描述符协议是什么呢?这个协议指的就是这三个方法。  

    descr.__get__(self, obj, type=None) --> value
    
    descr.__set__(self, obj, value) --> None
    
    descr.__delete__(self, obj) --> None

那么描述符有什么牛逼的？ 通常来说Python对象的属性控制默认是这样的：从对象的字典(`__dict__`)中获取（get），设置（set）,删除（delete），比如：对于实例`a`，`a.x`的查找顺序为`a.__dict__['x']`,然后是`type(a).__dict__['x']`.如果还是没找到就往上级(父类)中查找。描述符就好比是破坏小子，他会改变这种默认的控制行为。究竟是怎么改变的呢？  

想必会你已经猜到了，如果属性`x`是一个描述符，那么访问`a.x`时不再从字典`__dict__`中读取，而是调用描述符的`__get__()`方法，对于设置和删除也是同样的原理。  

既然知道他有化腐朽为神奇的这种特点，聪明的你一定能想到的能用在什么场景下，我用邮件地址的验证这个简单的例子来演示他是如何运作的。  

    class Person(object):
        def __init__(self, email):
            self.email = email

现在如果有不安分的小子总想着搞破坏，传递一个无效的email过来，如果你不使用描述符你是没辙的，你别告诉我说你可以在init方法里面做验证嘛？老兄，python是一门动态语言，也没有像我大java一样拥有私有变量。用一个例子来粉碎你的猜想。  

    import re
    class Person(object):
        def __init__(self, email):
            m = re.match('\w+@\w+\.\w+', email)
            if not m:
                raise Exception('email not valid')
            self.email = email

上面这个初始化方法看似完美有缺，如果客户端能安分的按规则行房，错了，是行事。就不会出什么大问题。传入的无效值也能优雅的以异常的形式警告。  

    >>> p = test.Person('lzjun567@gmail.com')
    >>> p.email
    'lzjun567@gmail.com'
    >>> p2 = test.Person('dfsdfsdf')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "test.py", line 38, in __init__
        raise Exception('email not valid')
    Exception: email not valid
    >>> 

但是，捣蛋小子来了，他要这样给p对象赋值email：  
    
    >>> p.email = 'sdfsdfsdf'
    >>> p.email
    'sdfsdfsdf'
    >>> p.__dict__
    {'email': 'sdfsdfsdf'}
    >>> 

这时的`p.email`默认从`__dict__`读取值。你看给`p`传个火星来的email地址也能接受。这下只有上帝能救你于水火之中，其实上帝就是那个描述符啦。那怎么把email变成一个描述符啊?当然方式有好几种：  

#####基于类创建描述符

    import re

    class Email(object):
    
        def __init__(self):
            self._name = ''
    
        def __get__(self, obj, type=None):
            return self._name
    
        def __set__(self, obj, value):
            m = re.match('\w+@\w+\.\w+', value)
            if not m:
                raise Exception('email not valid')
            self._name = value
    
        def __delete__(self, obj):
            del self._name
        
    class Person(object):
        email = Email()

这下你给他赋值一个火星文看看:  

    >>> p = Person()
    >>> p.email = 'ではないああを行う'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "test.py", line 46, in __set__
        raise Exception('email not valid')
    Exception: email not valid
    >>> 

    >>> p.email = 'lzjun@gmail.com'
    >>> p.email
    'lzjun@gmail.com'
    
现在总算是能抵挡住大和民族的`呀咩嗲`了,再来看看`__dict__`中有哪些东西：  

    >>> Person.__dict__
    dict_proxy({'__dict__': <attribute '__dict__' of 'Person' objects>, '__module__': 'test', '__weakref__': <attribute '__weakref__' of 'Person' objects>, 'email': <test.Email object at 0x8842fcc>, '__doc__': None})
    >>> p.__dict__
    {}

嗯，纵使email赫然在列dict中，拥有了描述符后，解释器对其视而不见，转而去调用描述符中对应的方法。即使是下面的操作方式也是徒劳而已：

    >>> p.__dict__['email'] = 'xxxxxx'
    >>> p.email
    'lzjun@gmail.com'
    >>> 

#####使用property()函数创建描述符

    class Person(object):
    
        def __init__(self):
            self._email = None
    
        def get_email(self):
            return self._email
    
        def set_email(self, value):
             m = re.match('\w+@\w+\.\w+', value)
             if not m:
                 raise Exception('email not valid')
             self._email = value
    
        def del_email(self):
            del self._email
    
        email = property(get_email, set_email, del_email, 'this is email property')
            

    >>> p = Person()
    >>> p.email
    >>> p.email = 'dsfsfsd'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "test.py", line 71, in set_email
        raise Exception('email not valid')
    Exception: email not valid
    >>> p.email = 'lzjun567@gmail.com'
    >>> p.email
    'lzjun567@gmail.com'
    >>> 

property()函数返回的是一个描述符对象，它可接收四个参数：`property(fget=None, fset=None, fdel=None, doc=None)`  

* fget：属性获取方法
* fset：属性设置方法
* fdel：属性删除方法
* doc： docstring

采用property实现描述符与使用类实现描述符的作用是一样的，只是实现方式不一样。property的一种纯python的实现方式如下：  

    class Property(object):
        "Emulate PyProperty_Type() in Objects/descrobject.c"
    
        def __init__(self, fget=None, fset=None, fdel=None, doc=None):
            self.fget = fget
            self.fset = fset
            self.fdel = fdel
            if doc is None and fget is not None:
                doc = fget.__doc__
            self.__doc__ = doc
    
        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("unreadable attribute")
            return self.fget(obj)
    
        def __set__(self, obj, value):
            if self.fset is None:
                raise AttributeError("can't set attribute")
            self.fset(obj, value)
    
        def __delete__(self, obj):
            if self.fdel is None:
                raise AttributeError("can't delete attribute")
            self.fdel(obj)
    
        def getter(self, fget):
            return type(self)(fget, self.fset, self.fdel, self.__doc__)
    
        def setter(self, fset):
            return type(self)(self.fget, fset, self.fdel, self.__doc__)
    
        def deleter(self, fdel):
            return type(self)(self.fget, self.fset, fdel, self.__doc__)

留心的你发现property里面还有getter，setter，deleter方法，那他们是做什么用的呢？来看看第三种创建描述符的方法。  

#####使用@property装饰器

    class Person(object):
    
        def __init__(self):
            self._email = None
    
        @property
        def email(self):
            return self._email
    
        @email.setter
        def email(self, value):
             m = re.match('\w+@\w+\.\w+', value)
             if not m:
                 raise Exception('email not valid')
             self._email = value
    
        @email.deleter
        def email(self):
            del self._email
    
    >>>
    >>> Person.email
    <property object at 0x02214930>
    >>> p.email = 'lzjun'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "test.py", line 93, in email
        raise Exception('email not valid')
    Exception: email not valid
    >>> p.email = 'lzjun@gmail.com'
    >>> p.email
    'lzjun@gmail.com'
    >>>

发现没有，其实装饰器property只是property函数的一种语法糖而已，setter和deleter作用在函数上面作为装饰器使用。  

####哪些场景用到了描述符

其实python的实例方法就是一个描述符，来看下面代码块：  

    >>> class Foo(object):
    ...     def my_function(self):
    ...        pass
    ...
    >>> Foo.my_function
    <unbound method Foo.my_function>
    >>> Foo.__dict__['my_function']
    <function my_function at 0x02217830>
    >>> Foo.__dict__['my_function'].__get__(None, Foo)
    <unbound method Foo.my_function>
    >>> Foo().my_function
    <bound method Foo.my_function of <__main__.Foo object at 0x0221FFD0>>
    >>> Foo.__dict__['my_function'].__get__(Foo(), Foo)
    <bound method Foo.my_function of <__main__.Foo object at 0x02226350>>

my_function函数实现了`__get__`方法。描述符也被大量用在各种框架中，比如：django的[paginator.py](https://github.com/django/django/blob/master/django/core/paginator.py)模块，django的model其实也使用了描述符。  







python 函数默认是一个描述符.调用 my_instance.my_method会重载为Myclass.__dict__['my_method'].__get__(myinstance, MyClass).


http://docs.python.org/2/howto/descriptor.html#properties
http://stackoverflow.com/questions/17330160/python-how-does-decorator-property-work
https://pyzh.readthedocs.org/en/latest/Descriptor-HOW-TO-Guide.html
http://www.ibm.com/developerworks/cn/opensource/os-pythondescriptors/
https://blog.tonyseek.com/post/notes-about-python-descriptor/
https://speakerdeck.com/mitsuhiko/basket-of-random-python-snippets
http://docs.python.org/2/howto/descriptor.html
http://utcc.utoronto.ca/~cks/space/blog/python/AttributeLookupOrder
