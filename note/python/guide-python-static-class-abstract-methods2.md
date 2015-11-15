如何正确使用static、class、abstract方法
==================
####How methods work in Python
A method is a function that is stored as a class attribute. You can declare and access such a function this way:  
####方法在Python中是如何工作的
方法就是一个函数，它作为一个类属性而存在，你可以用如下方式来声明、访问一个函数：
    
    >>> class Pizza(object):
    ...     def __init__(self, size):
    ...         self.size = size
    ...     def get_size(self):
    ...         return self.size
    ...
    >>> Pizza.get_size
    <unbound method Pizza.get_size>
What Python tells you here, is that the attribute get_size of the class Pizza is a method that is unbound. What does this mean? We'll know as soon as we'll try to call it:  
Python在告诉你，属性*get_size*是类*Pizza*的一个**未绑定**方法。这是什么意思呢？很快我们就会知道答案：  
    
    >>> Pizza.get_size()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unbound method get_size() must be called with Pizza instance as first argument (got nothing instead)
We can't call it because it's not bound to any instance of Pizza. And a method wants an instance as its first argument (in Python 2 it must be an instance of that class; in Python 3 it could be anything). Let's try to do that then:  
我们不能这么调用，因为它还没有绑定到*Pizza*类的任何实例上，它需要一个实例作为第一个参数传递进去（Python2必须是该类的实例，Python中可以是任何东西），尝试一下：  
    
    >>> Pizza.get_size(Pizza(42))
    42
It worked! We called the method with an instance as its first argument, so everything's fine. But you will agree with me if I say this is not a very handy way to call methods; we have to refer to the class each time we want to call a method. And if we don't know what class is our object, this is not going to work for very long.  
太棒了，现在用一个实例作为它的的第一个参数来调用，整个世界都清静了，如果我说这种调用方式还不是最方便的，你也会这么认为的；没错，现在每次调用这个方法的时候我们都不得不引用这个类，如果不知道哪个类是我们的对象，长期看来这种方式是行不通的。  

So what Python does for us, is that it binds all the methods from the class Pizza to any instance of this class. This means that the attribute get_size of an instance of Pizza is a bound method: a method for which the first argument will be the instance itself.  
那么Python为我们做了什么呢，它绑定了所有来自类*Pizza*的方法以及该类的任何一个实例的方法。也就意味着现在属性*get_size*是*Pizza*的一个实例对象的绑定方法，这个方法的第一个参数就是该实例本身。  
    
    >>> Pizza(42).get_size
    <bound method Pizza.get_size of <__main__.Pizza object at 0x7f3138827910>>
    >>> Pizza(42).get_size()
    42
As expected, we don't have to provide any argument to get_size, since it's bound, its self argument is automatically set to our Pizza instance. Here's a even better proof of that:  
和我们预期的一样，现在不再需要提供任何参数给*get_size*，因为它已经是绑定的，它的*self*参数会自动地设置给*Pizza*实例，下面代码是最好的证明：  
    
    >>> m = Pizza(42).get_size
    >>> m()
    42
Indeed, you don't even have to keep a reference to your Pizza object. Its method is bound to the object, so the method is sufficient to itself.  
更有甚者，你都没必要使用持有*Pizza*对象的引用了，因为该方法已经绑定到了这个对象，所以这个方法对它自己来说是已经足够了。  

But what if you wanted to know which object this bound method is bound to? Here's a little trick:  
也许，如果你想知道这个绑定的方法是绑定在哪个对象上，下面这种手段就能得知：  
    
    >>> m = Pizza(42).get_size
    >>> m.__self__
    <__main__.Pizza object at 0x7f3138827910>
    >>> # You could guess, look at this:
    ...
    >>> m == m.__self__.get_size
    True

Obviously, we still have a reference to our object, and we can find it back if we want.  

In Python 3, the functions attached to a class are not considered as unbound method anymore, but as simple functions, that are bound to an object if required. So the principle stays the same, the model is just simplified.  

显然，该对象仍然有一个引用存在，只要你愿意你还是可以把它找回来。  

在Python3中，依附在类上的函数不再当作是**未绑定**的方法，而是把它当作一个简单地函数，如果有必要它会绑定到一个对象身上去，原则依然和Python2保持一致，但是模块更简洁：  
    
    >>> class Pizza(object):
    ...     def __init__(self, size):
    ...         self.size = size
    ...     def get_size(self):
    ...         return self.size
    ...
    >>> Pizza.get_size
    <function Pizza.get_size at 0x7f307f984dd0>

####Static methods
Static methods are a special case of methods. Sometimes, you'll write code that belongs to a class, but that doesn't use the object itself at all. For example:  
####静态方法
静态方法是一类特殊的方法，有时你可能需要写一个属于这个类的方法，但是这些代码完全不会使用到实例对象本身，例如：  
    
    class Pizza(object):
        @staticmethod
        def mix_ingredients(x, y):
            return x + y
     
        def cook(self):
            return self.mix_ingredients(self.cheese, self.vegetables)
In such a case, writing mix_ingredients as a non-static method would work too, but it would provide it a self argument that would not be used. Here, the decorator @staticmethod buys us several things:  
这个例子中，如果把*mix_ingredients*作为非静态方法同样可以运行，但是它要提供*self*参数，而这个参数在方法中根本不会被使用到。这里的*@staticmethod*装饰器可以给我们带来一些好处：  

* Python doesn't have to instantiate a bound-method for each Pizza object we instiantiate. Bound methods are objects too, and creating them has a cost. Having a static method avoids that:  
* Python不再需要为*Pizza*对象实例初始化一个绑定方法，绑定方法同样是对象，但是创建他们需要成本，而静态方法就可以避免这些。
    
        >>> Pizza().cook is Pizza().cook
        False
        >>> Pizza().mix_ingredients is Pizza.mix_ingredients
        True
        >>> Pizza().mix_ingredients is Pizza().mix_ingredients
        True

* It eases the readability of the code: seeing @staticmethod, we know that the method does not depend on the state of object itself;  
* 可读性更好的代码，看到*@staticmethod*我们就知道这个方法并不需要依赖对象本身的状态。
* It allows us to override the mix_ingredients method in a subclass. If we used a function mix_ingredients defined at the top-level of our module, a class inheriting from Pizza wouldn't be able to change the way we mix ingredients for our pizza without overriding cook itself.    
* 可以在子类中被覆盖，如果是把*mix_ingredients*作为模块的顶层函数，那么继承自*Pizza*的子类就没法改变pizza的*mix_ingredients*了如果不覆盖*cook*的话。  

####Class methods
Having said that, what are class methods? Class methods are methods that are not bound to an object, but to… a class!  
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

Whatever the way you use to access this method, it will be always bound to the class it is attached too, and its first argument will be the class itself (remember that classes are objects too).  
无论你用哪种方式访问这个方法，它总是绑定到了这个类身上，它的第一个参数是这个类本身（记住：类也是对象）。  

When to use this kind of methods? Well class methods are mostly useful for two types of methods:  
什么时候使用这种方法呢？类方法通常在以下两种场景是非常有用的：    

* Factory methods, that are used to create an instance for a class using for example some sort of pre-processing. If we use a @staticmethod instead, we would have to hardcode the Pizza class name in our function, making any class inheriting from Pizza unable to use our factory for its own use.  
* 工厂方法：它用于创建类的实例，例如一些预处理。如果使用*@staticmethod*代替，那我们不得不硬编码*Pizza*类名在函数中，这使得任何继承*Pizza*的类都不能使用我们这个工厂方法给它自己用。
    
        class Pizza(object):
            def __init__(self, ingredients):
                self.ingredients = ingredients
            @classmethod
            def from_fridge(cls, fridge):
                return cls(fridge.get_cheese() + fridge.get_vegetables())
* Static methods calling static methods: if you split a static methods in several static methods, you shouldn't hard-code the class name but use class methods. Using this way to declare ou method, the Pizza name is never directly referenced and inheritance and method overriding will work flawlessly  
* 调用静态类：如果你把一个静态方法拆分成多个静态方法，除非你使用类方法，否则你还是得硬编码类名。使用这种方式声明方法，*Pizza*类名明永远都不会在被直接引用，继承和方法覆盖都可以完美的工作。  
    
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
####Abstract methods
An abstract method is a method defined in a base class, but that may not provide any implementation. In Java, it would describe the methods of an interface.  
####抽象方法
抽象方法是定义在基类中的一种方法，它没有提供任何实现，类似于Java中接口(Interface)里面的方法。  

So the simplest way to write an abstract method in Python is:  
在Python中实现抽象方法最简单地方式是：  
    
    class Pizza(object):
        def get_radius(self):
            raise NotImplementedError

Any class inheriting from Pizza should implement and override the get_radius method, otherwise an exception would be raised.  

This particular way of implementing abstract method has a drawback. If you write a class that inherits from Pizza and forget to implement get_radius, the error will only be raised when you'll try to use that method.  
任何继承自*Pizza*的类必须覆盖实现方法*get_radius*，否则会抛出异常。  

这种抽象方法的实现有它的弊端，如果你写一个类继承*Pizza*，但是忘记实现*get_radius*，异常只有在你真正使用的时候才会抛出来。  

    >>> Pizza()
    <__main__.Pizza object at 0x7fb747353d90>
    >>> Pizza().get_radius()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 3, in get_radius
    NotImplementedError
There's a way to triggers this way earlier, when the object is being instantiated, using the abc module that's provided with Python.  
还有一种方式可以让错误更早的触发，使用Python提供的**abc**模块，对象被初始化之后就可以抛出异常：  
    
    import abc
 
    class BasePizza(object):
        __metaclass__  = abc.ABCMeta
     
        @abc.abstractmethod
        def get_radius(self):
             """Method that should do something."""
Using abc and its special class, as soon as you'll try to instantiate BasePizza or any class inheriting from it, you'll get a TypeError.  
使用*abc*后，当你尝试初始化*BasePizza*或者任何子类的时候立马就会得到一个*TypeError*，而无需等到真正调用*get_radius*的时候才发现异常。 
    
    >>> BasePizza()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: Can't instantiate abstract class BasePizza with abstract methods get_radius

####Mixing static, class and abstract methods
When building classes and inheritances, the time will come where you will have to mix all these methods decorators. So here's some tips about it.  

Keep in mind that declaring a method as being abstract, doesn't freeze the prototype of that method. That means that it must be implemented, but i can be implemented with any argument list.
####混合静态方法、类方法、抽象方法
当你开始构建类和继承结构时，混合使用这些装饰器的时候到了，所以这里列出了一些技巧。  

记住，声明一个抽象的方法，不要凝固方法的原型，这就意味着你必须实现它，但是我可以用任何参数列表来实现：  
    
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

This is valid, since Calzone fulfil the interface requirement we defined for BasePizza objects. That means that we could also implement it as being a class or a static method, for example:  
这样是允许的，因为*Calzone*满足*BasePizza*对象所定义的接口需求。同样我们也可以用一个类方法或静态方法来实现：  
    
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
This is also correct and fulfil the contract we have with our abstract BasePizza class. The fact that the get_ingredients method don't need to know about the object to return result is an implementation detail, not a criteria to have our contract fulfilled.  

Therefore, you can't force an implementation of your abstract method to be a regular, class or static method, and arguably you shouldn't. Starting with Python 3 (this won't work as you would expect in Python 2, see issue5867), it's now possible to use the @staticmethod and @classmethod decorators on top of @abstractmethod:  
这同样是正确的,因为它遵循抽象类*BasePizza*设定的契约。事实上*get_ingredients*方法并不需要知道返回结果是什么，结果是实现细节，不是契约条件。  

因此，你不能强制抽象方法的实现是一个常规方法、或者是类方法还是静态方法，也没什么可争论的。从Python3开始（在Python2中不能如你期待的运行，见[issue5867](http://bugs.python.org/issue5867)），在*abstractmethod*方法上面使用*@staticmethod*和*@classmethod*装饰器成为可能。
    
    import abc
 
    class BasePizza(object):
        __metaclass__  = abc.ABCMeta
     
        ingredient = ['cheese']
     
        @classmethod
        @abc.abstractmethod
        def get_ingredients(cls):
             """Returns the ingredient list."""
             return cls.ingredients


Don't misread this: if you think this going to force your subclasses to implement get_ingredients as a class method, you are wrong. This simply implies that your implementation of get_ingredients in the BasePizza class is a class method.

An implementation in an abstract method? Yes! In Python, contrary to methods in Java interfaces, you can have code in your abstract methods and call it via super():  
别误会了，如果你认为它会强制子类作为一个类方法来实现*get_ingredients*那你就错了，它仅仅表示你实现的*get_ingredients*在*BasePizza*中是一个类方法。  

可以在抽象方法中做代码的实现？没错，Python与Java接口中的方法相反，你可以在抽象方法编写实现代码通过*super()*来调用它。（译注：在Java8中，接口也提供的默认方法，允许在接口中写方法的实现）

    import abc
     
    class BasePizza(object):
        __metaclass__  = abc.ABCMeta
     
        default_ingredients = ['cheese']
     
        @classmethod
        @abc.abstractmethod
        def get_ingredients(cls):
             """Returns the ingredient list."""
             return cls.default_ingredients
     
    class DietPizza(BasePizza):
        def get_ingredients(self):
            return ['egg'] + super(DietPizza, self).get_ingredients()

In such a case, every pizza you will build by inheriting from BasePizza will have to override the *get_ingredients* method, but will be able to use the default mechanism to get the ingredient list by using super().  
这个例子中，你构建的每个pizza都通过继承*BasePizza*的方式，你不得不覆盖*get_ingredients*方法，但是能够使用默认机制通过*super()*来获取*ingredient*列表。






















    
    
    
https://julien.danjou.info/blog/2013/guide-python-static-class-abstract-methods    