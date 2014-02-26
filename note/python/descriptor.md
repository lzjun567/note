####什么是描述符
只要是定义了`__get__()`,`__set()__`,`__delete()__`中任意一个方法的对象都叫描述符.  

那描述符协议是什么呢?这个协议指的就是这三个方法.  

    descr.__get__(self, obj, type=None) --> value
    
    descr.__set__(self, obj, value) --> None
    
    descr.__delete__(self, obj) --> None

那么描述符有什么牛逼的? 通常来说对象的属性的控制是这样的:默认从对象的字典(__dict__)中获取,设置,删除,比如:对于实例a,a.x的查找顺序为`a.__dict__['x']`,然后是`type(a).__dict__['x']`.如果还是没找到就往上级(父类)中查找.描述符就是破坏小子,他会改变这种默认的控制行为.  

想必会你已经猜到了,如果属性x是一个描述符,那么访问`a.x`时不再从字典`__dict__`中读取,而是调用`__get__()`方法,对于设置和删除也是同样的原理.  

既然知道他有化腐朽为神奇的特点,聪明的你一定能想到的能用在什么场景下,我举个例子就是邮件地址的验证. 

    class Person(object):
        def __init__(self, email):
            self.email = email
如果有不安分的小子总想着搞破坏,传递一个非法的email过来,如果你不使用描述符你是没辙的,你别告诉我说你可以在init方法里面做验证嘛?老兄,python是一门动态语言,也没有像我大java一样拥有私有变量.用一个例子来粉碎你的猜想.  

    import re
    class Person(object):
        def __init__(self, email):
            m = re.match('\w+@\w+\.\w+', email)
            if not m:
                raise Exception('email not valid')
            self.email = email

上面这个初始化方法看似完美有缺,如果客户端能安分的按规则行房,错了,是行事.就不会出什么大问题,如果传入的无效值能优雅的发布警告.

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

但是,捣蛋小子来了,他要这样给p对象赋值email:
    
    >>> p.email = 'sdfsdfsdf'
    >>> p.email
    'sdfsdfsdf'
    >>> p.__dict__
    {'email': 'sdfsdfsdf'}
    >>> 

p.email就是默认从__dict__读取的值.你看给p传个火星来的email地址也无事吧.这下只有上帝能救你于水火之中,其实上帝就是那个描述符啦.那怎么把email变成一个描述符啊?当然方式有好几种  

####基于类创建描述符

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
    
现在总算是能抵挡住大和民族的`yamiedie`了,在来看看`__dict__`中有那些东西:  

    >>> Person.__dict__
    dict_proxy({'__dict__': <attribute '__dict__' of 'Person' objects>, '__module__': 'test', '__weakref__': <attribute '__weakref__' of 'Person' objects>, 'email': <test.Email object at 0x8842fcc>, '__doc__': None})
    >>> p.__dict__
    {}

嗯,纵使email赫然在列,拥有了描述符后,解释器对其视而不见,转而去调用描述符中对应的方法.下面的操作也是徒劳而已:

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

property()函数返回的是一个描述符对象,它可介绍四个参数:`property(fget=None, fset=None, fdel=None, doc=None)`  

* fget：属性获取方法
* fset：属性设置方法
* fdel：属性删除方法
* doc： docstring

采用property实现描述符与使用类实现描述符的作用是一样的,只是实现方式不一样.  








python 函数默认是一个描述符.调用 my_instance.my_method会重载为Myclass.__dict__['my_method'].__get__(myinstance, MyClass).


http://docs.python.org/2/howto/descriptor.html#properties
http://stackoverflow.com/questions/17330160/python-how-does-decorator-property-work
https://pyzh.readthedocs.org/en/latest/Descriptor-HOW-TO-Guide.html
http://www.ibm.com/developerworks/cn/opensource/os-pythondescriptors/
https://blog.tonyseek.com/post/notes-about-python-descriptor/
https://speakerdeck.com/mitsuhiko/basket-of-random-python-snippets
http://docs.python.org/2/howto/descriptor.html
