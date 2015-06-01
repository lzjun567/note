Python如何使用static、class、abstract方法
==================
####方法在Python中是如何工作的
方法就是一个函数，它作为一个类属性而存在，你可以如下方式来声明、访问一个函数：  
    
    >>> class Pizza(object):
    ...     def __init__(self, size):
    ...         self.size = size
    ...     def get_size(self):
    ...         return self.size
    ...
    >>> Pizza.get_size
    <unbound method Pizza.get_size>
Python在告诉你，属性*get_size*是类*Pizza*的一个**未绑定**方法。这是什么意思呢？很快我们就知道答案：  
    
    >>> Pizza.get_size()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unbound method get_size() must be called with Pizza instance as first argument (got nothing instead)
我们不能这么调用，因为它还没有绑定到*Pizza*的任何实例上，需要一个实例作为它的第一个参数传递进去（Python2必须是该类的实例，Python中可以是任何东西），尝试一下：  
    
    >>> Pizza.get_size(Pizza(42))
    42
太棒了，现在用一个实例作为它的的第一个参数来调用，整个世界都清静了，如果我说这种调用方式还不是最方便的，你也会这么认为的；没错，每次想调用这个方法的时候我们都不得不引用这个类，如果不知道哪个类是我们的对象，长期来看这种方式是行不通的。  
那么Python为我们做了什么呢，它绑定了所有来自类*Pizza*的方法以及该类的任何一个实例的方法。也就意味着现在属性*get_size*是*Pizza*的一个实例的绑定方法，这个方法的第一个参数就是该实例本身。  
    
    >>> Pizza(42).get_size
    <bound method Pizza.get_size of <__main__.Pizza object at 0x7f3138827910>>
    >>> Pizza(42).get_size()
    42
和我们预期的一样，现在不再需要提供任何参数给*get_size*，因为它已经是绑定的，它的*self*参数会自动地设置给*Pizza*实例，下面代码是最好的证明：  
    
    >>> m = Pizza(42).get_size
    >>> m()
    42
更有甚者，你都没必要使用持有*Pizza*对象的引用了，因为该方法已经绑定到了这个对象，所以这个方法对它自己来说是已经足够了。  

也许，如果你想知道这个绑定的方法是绑定在哪个对象上，用下面这种手段就能得知：  
    
    >>> m = Pizza(42).get_size
    >>> m.__self__
    <__main__.Pizza object at 0x7f3138827910>
    >>> # You could guess, look at this:
    ...
    >>> m == m.__self__.get_size
    True
显然，该对象仍然有一个引用存在，只要你愿意你还是可以把它找回来。  

在Python3中，类所依附的函数不再当作是**未绑定**的方法，而是把它当作一个简单地函数，如果有必要它会绑定到一个对象身上去，原则依然和Python2保持一致，但是模块更简洁：  
    
    >>> class Pizza(object):
    ...     def __init__(self, size):
    ...         self.size = size
    ...     def get_size(self):
    ...         return self.size
    ...
    >>> Pizza.get_size
    <function Pizza.get_size at 0x7f307f984dd0>

####静态方法
静态方法是一类特殊的方法，有时你可能需要写一个属于这个类的方法，但是这些代码完全不会使用到实例对象本身，例如：  
    
    class Pizza(object):
        @staticmethod
        def mix_ingredients(x, y):
            return x + y
     
        def cook(self):
            return self.mix_ingredients(self.cheese, self.vegetables)
这个例子中，如果把*mix_ingredients*作为非静态方法同样可以运行，但是它要提供*self*参数，而这个参数根本不会被使用到。这里的*@staticmethod*装饰器可以给我们带来一些好处：  
* Python不再需要为*Pizza*对象初始化一个绑定方法，绑定方法同样是对象，但是创建他们需要成本，静态方法就可以避免这些：  
    
        >>> Pizza().cook is Pizza().cook
        False
        >>> Pizza().mix_ingredients is Pizza.mix_ingredients
        True
        >>> Pizza().mix_ingredients is Pizza().mix_ingredients
        True
* 可读性更好的代码，看到*@staticmethod*我们就知道这个方法并不需要依赖对象本身的状态。
* 可以在子类中被覆盖，如果是把*mix_ingredients*作为模块的最顶层函数，那么继承自*Pizza*的子类就没法改变pizza的*mix_ingredients*了如果不覆盖cook的话。  

####类方法
话虽如此，什么是类方法呢？类方法不是绑定到对象上，而是绑定在类上的方法。  
    
    >>> class Pizza(object):
    ...     radius = 42
    ...     @classmethod
    ...     def get_radius(cls):
    ...         return cls.radius
    ... 
    >>> 
    >>> Pizza.get_radius
    <bound method type.get_radius of <class '__main__.Pizza'>>
    >>> Pizza().get_radius
    <bound method type.get_radius of <class '__main__.Pizza'>>
    >>> Pizza.get_radius is Pizza().get_radius
    True
    >>> Pizza.get_radius()
    42
无论你用哪种方式访问这个方法，它总是绑定到了这个类身上，它的第一个参数是这个类本身（记住：类也是对象）。  

什么时候使用这种方法呢？类方法通常在以下两种方法是非常有用：  
* 工厂方法：它用于创建实例，例如一些预处理，如果使用*@staticmethod*代替，那我们不得不硬编码*Pizza*类名在函数中，这使得任何继承*Pizza*的类不能使用这是我们这个工厂方法给它自己用。
    
        class Pizza(object):
            def __init__(self, ingredients):
                self.ingredients = ingredients
         
            @classmethod
            def from_fridge(cls, fridge):
                return cls(fridge.get_cheese() + fridge.get_vegetables())
* 调用静态类：如果你把一个静态方法拆分成多个静态方法，使用类方法可以不需要硬编码类名，使用这种方式声明方法，*Pizza*明永远都不会在直接被引用，继承和方法覆盖都可以完美的工作。  
    
        class Pizza(object):
            def __init__(self, radius, height):
                self.radius = radius
                self.height = height
         
            @staticmethod
            def compute_area(radius):
                 return math.pi * (radius ** 2)
         
            @classmethod
            def compute_volume(cls, height, radius):
                 return height * cls.compute_area(radius)
         
            def get_volume(self):
                return self.compute_volume(self.height, self.radius)

####抽象方法
抽象方法是定义在基类中的一类方法，它没有提供任何实现，它类似于Java中一个接口的方法。  

在Python中实现抽象方法最简单地方式是：  
    
    class Pizza(object):
        def get_radius(self):
            raise NotImplementedError
任何继承自*Pizza*的类必须覆盖实现方法*get_radius*，否则会抛出异常。  

这种抽象方法的实现有它的弊端，如果你写一个类继承*Pizza*，但是忘记实现*get_radius*，异常只有在你真正尝试使用的时候才会抛出来。  

    >>> Pizza()
    <__main__.Pizza object at 0x7fb747353d90>
    >>> Pizza().get_radius()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 3, in get_radius
    NotImplementedError

还有一种方式可以让错误更早的触发，当对象被初始化之后，使用Python提供的**abc**模块：  
    
    import abc
 
    class BasePizza(object):
        __metaclass__  = abc.ABCMeta
     
        @abc.abstractmethod
        def get_radius(self):
             """Method that should do something."""
使用*abc*以及指定类，在你尝试初始化*BasePizza*或者任何子类的时候立马就会得到一个*TypeError*，而无需等到真正调用*get_radius*的时候才发现异常。 
    
    >>> BasePizza()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: Can't instantiate abstract class BasePizza with abstract methods get_radius

####混合静态方法、类方法、抽象方法
当构建类和继承的时候，时间在流逝当你不得不混合所有装饰器的时候，所以这里有些tips。  

记住声明一个抽象的方法，不要凝固方法的原型，也就意味着必须实现，但是我可以用任何的参数列表作为参数：  
    
    import abc
 
    class BasePizza(object):
        __metaclass__  = abc.ABCMeta
     
        @abc.abstractmethod
        def get_ingredients(self):
             """Returns the ingredient list."""
     
    class Calzone(BasePizza):
        def get_ingredients(self, with_egg=False):
            egg = Egg() if with_egg else None
            return self.ingredients + egg

这是有效的，因为*Calzone*完成了我们给*BasePizza*对象所需要的接口需求。意味着我们同样可以实现作为一个类方法或者静态方法：  
    
    import abc
 
    class BasePizza(object):
        __metaclass__  = abc.ABCMeta
     
        @abc.abstractmethod
        def get_ingredients(self):
             """Returns the ingredient list."""
     
    class DietPizza(BasePizza):
        @staticmethod
        def get_ingredients():
            return None
    
https://julien.danjou.info/blog/2013/guide-python-static-class-abstract-methods    