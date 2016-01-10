Python创建单例模式的三种方式
===========================
####方法一：使用装饰器
装饰器维护一个字典对象instances，缓存了所有单例类，只要单例不存在则创建，已经存在直接返回该实例对象。
	
	def singleton(cls):
	    instances = {}

	    def wrapper(*args, **kwargs):
	        if cls not in instances:
	            instances[cls] = cls(*args, **kwargs)
	        return instances[cls]

	    return wrapper


	@singleton
	class Foo(object):
	    pass

	foo1 = Foo()
	foo2 = Foo()

	print foo1 is foo2

####方法二：使用基类
`__new__`是真正创建实例对象的方法，所以重写基类的`__new__`方法，以此来保证创建对象的时候只生成一个实例
	
	class Singleton(object):
	    def __new__(cls, *args, **kwargs):
	        if not hasattr(cls, '_instance'):
	            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
	        return cls._instance


	class Foo(Singleton):
	    pass

	foo1 = Foo()
	foo2 = Foo()

	print foo1 is foo2  # True

####方法三：使用元类
元类（参考：[深刻理解Python中的元类](http://blog.jobbole.com/21351/)）是用于创建类对象的类，类对象创建实例对象时一定会调用`__call__`方法，因此在调用`__call__`时候保证始终只创建一个实例即可，`type`是python中的一个元类。

	class Singleton(type):
	    def __call__(cls, *args, **kwargs):
	        if not hasattr(cls, '_instance'):
	            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
	        return cls._instance


	class Foo(object):
	    __metaclass__ = Singleton


	foo1 = Foo()
	foo2 = Foo()

	print foo1 is foo2  # True

http://foofish.net/blog/93/python_singleton
