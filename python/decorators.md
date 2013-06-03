####Python's functions are objects
####Python函数是对象  
To understand decorators, you must first understand that functions are objects in Python. This has important consequences. Let's see why with a simple example :  
为了理解装饰器，首先需要明白函数在Python中也是对象，理解这一点很重要，下面用一个例子来说明：  

    def shout(word="yes"):
        return word.capitalize()+"!"
    
    print shout()
    # 输出 : 'Yes!'
    
    # As an object, you can assign the function to a variable like any
    # other object 
    #函数作为对象，你可以象其他对象一样赋值给变量 
    scream = shout
    
    # Notice we don't use parentheses: we are not calling the function, we are
    # putting the function "shout" into the variable "scream". 
    # It means you can then call "shout" from "scream":
    # 注意：这里我们没有使用圆括号去调用函数，仅仅是把函数"shout"赋值给变量"scream"
    #也就是说你可以通过"scream"来调用"shout"
    print scream()
    # 输出 : 'Yes!'
    
    # More than that, it means you can remove the old name 'shout', and
    # the function will still be accessible from 'scream'
    # 不仅如此，你还可以删除'shout'，该函数仍然可以通过'scream'来访问。
    
    del shout
    try:
        print shout()
    except NameError, e:
        print e
        #输出: "name 'shout' is not defined"
    
    print scream()
    # 输出: 'Yes!'
OK, keep that in mind, we are going back to it soon. Another interesting property of Python functions is they can be defined... inside another function!  
好了，先记住上面规则，稍后再回到这里来，Python另一个有意思的特点是函数可以定义在另一个函数里面。  

    def talk():
    
        # You can define a function on the fly in "talk" ...
        # 你可以直接在"talk"中定义函数
        def whisper(word="yes"):
            return word.lower()+"..."
    
        # ... and use it right away!
        # ... 立马就可以在这里使用 
        print whisper()
    
    # You call "talk", that defines "whisper" EVERY TIME you call it, then
    # "whisper" is called in "talk". 
    # 每次调用"talk"时，"whipser"将被"talk"调用
    talk()
    # 输出: 
    # "yes..."
    
    # But "whisper" DOES NOT EXIST outside "talk":
    # 注意："whisper"在函数"talk"外面是不可见的 
    try:
        print whisper()
    except NameError, e:
        print e
        #输出 : "name 'whisper' is not defined"*

####Functions references
OK, still here? Now the fun part, you've seen that functions are objects and therefore:  
OK，你已经知道函数是对象了：  

+ can be assigned to a variable;  
+ 它可以赋值给变量   
+ can be defined in another function.  
+ 可以定义在另外的函数中  

Well, that means that a function can return another function :-) Have a look:  

也就是意味着一个函数可以返回另一个函数:-)，请看下面：  

    def getTalk(type="shout"):
    
        # We define functions on the fly
        # 直接在函数中定义函数
        def shout(word="yes"):
            return word.capitalize()+"!"
    
        def whisper(word="yes") :
            return word.lower()+"...";
    
        # Then we return one of them
        # 返回其中的一个函数
        if type == "shout":
            # We don't use "()", we are not calling the function,
            # 这里没有使用"()"，我们不是调用这个函数，而是返回这个函数对象
            # we are returning the function object
            return shout  
        else:
            return whisper
    
    # How do you use this strange beast?
    # 怎么使用这个奇怪的东东呢？
    # Get the function and assign it to a variable
    # 获取函数并赋值给变量
    talk = getTalk()      
    
    # You can see that "talk" is here a function object:
      "talk"在这儿就是一个函数对象
    print talk
    #输出: <function shout at 0xb7ea817c>
    
    # The object is the one returned by the function:
      这个对象就是由一个函数返回的 
    print talk()
    #输出 : Yes!
    
    # And you can even use it directly if you feel wild:
    你甚至能直接使用它
    print getTalk("whisper")()
    #输出 : yes...

But wait, there is more. If you can return a function, then you can pass one as a parameter:  
等等，还有呢，如果能返回一个函数，那么这个函数还可以作为参数传递    

    def doSomethingBefore(func): 
        print "I do something before then I call the function you gave me"
        print func()
    
    doSomethingBefore(scream)
    #输出: 
    #I do something before then I call the function you gave me
    #Yes!

Well, you just have everything needed to understand decorators. You see, decorators are wrappers which means that they let you execute code before and after the function they decorate without the need to modify the function itself.  
好啦，终于可以开始理解装饰器了，你瞧，装饰器就是对函数进行一层包裹，能在函数运行前或运行后执行额外的代码，而不需要修改函数本身。  

####Handcrafted decorators
####纯手工装饰器
How you would do it manually:
你可以用手工方式如下实现：  

# A decorator is a function that expects ANOTHER function as parameter  
# 装饰器是一个接受另一个函数作为参数的函数

    def my_shiny_new_decorator(a_function_to_decorate):
    
        # Inside, the decorator defines a function on the fly: the wrapper.
        # This function is going to be wrapped around the original function
        # so it can execute code before and after it.
        # 
        # 装饰器内定义了一个函数，该函数包裹原始函数，可以在原始函数前后执行代码
        def the_wrapper_around_the_original_function():
    
            # Put here the code you want to be executed BEFORE the original 
            # function is called
            #在原始函数调用前执行代码
            print "Before the function runs"
    
            # Call the function here (using parentheses)
            #调用函数（注意这里带括号）
            a_function_to_decorate()
    
            # Put here the code you want to be executed AFTER the original 
            # function is called
            #调用完原始函数后执行代码
            print "After the function runs"
    
        # At this point, "a_function_to_decorate" HAS NEVER BEEN EXECUTED.
        # We return the wrapper function we have just created.
        # The wrapper contains the function and the code to execute before
        # and after. It's ready to use!
        # 在这个地方，" a_function_to_decorate"函数从来没有被执行
        #而是返回这个刚刚创建的包裹函数，该函数包含了函数的代码及前后代码段，这样准备使用了
        return the_wrapper_around_the_original_function
    
    # Now imagine you create a function you don't want to ever touch again.
    # 现在假设你创建一个函数，而且又不想做任何修改了
    def a_stand_alone_function():
        print "I am a stand alone function, don't you dare modify me"
    
    a_stand_alone_function() 
    #outputs: I am a stand alone function, don't you dare modify me
    #输出：I am a stand alone function, don't you dare modify me
    
    # Well, you can decorate it to extend its behavior.
    # Just pass it to the decorator, it will wrap it dynamically in 
    # any code you want and return you a new function ready to be used:

    #嗯，你可以装饰这个函数扩展其行为
    
    a_stand_alone_function_decorated = my_shiny_new_decorator(a_stand_alone_function)
    a_stand_alone_function_decorated()
    #outputs:
    #输出：
    #Before the function runs
    #I am a stand alone function, don't you dare modify me
    #After the function runs

Now, you probably want that every time you call a_stand_alone_function, a_stand_alone_function_decorated is called instead. That's easy, just overwrite a_stand_alone_function with the function returned by my_shiny_new_decorator:  

现在，你可能每次想每次调用*a_stand_alone_function*的时候，*a_stand_alone_function_decorated*就被调用，这很简单，只需重写*a_stand_alone_function*函数，通过*my_shiny_new_decorator*  

    a_stand_alone_function = my_shiny_new_decorator(a_stand_alone_function)
    a_stand_alone_function()
    #输出:
    #Before the function runs
    #I am a stand alone function, don't you dare modify me
    #After the function runs
    
    # And guess what? That's EXACTLY what decorators do!

####Decorators demystified
####装饰器揭秘

The previous example, using the decorator syntax:  
前面的例子，使用装饰器语法如下：  

    @my_shiny_new_decorator
    def another_stand_alone_function():
        print "Leave me alone"
    
    another_stand_alone_function()  
    #输出:  
    #Before the function runs
    #Leave me alone
    #After the function runs

Yes, that's all, it's that simple. @decorator is just a shortcut to:  
没错，就这么简单，@装饰器 是下面代码的快捷方式：  

    another_stand_alone_function = my_shiny_new_decorator(another_stand_alone_function)

Decorators are just a pythonic variant of the decorator design pattern. There are several classic design patterns embedded in Python to ease development, like iterators.  

装饰器是装饰器模式的一种pythonic方式，还有很多经典设计模式嵌在Python中简化开发，比如迭代器  

Of course, you can cumulate decorators:  
当然，你也可以累积装饰器  

    def bread(func):
        def wrapper():
            print "</''''''\>"
            func()
            print "<\______/>"
        return wrapper
    
    def ingredients(func):
        def wrapper():
            print "#tomatoes#"
            func()
            print "~salad~"
        return wrapper
    
    def sandwich(food="--ham--"):
        print food
    
    sandwich()
    #outputs: --ham--
    sandwich = bread(ingredients(sandwich))
    sandwich()
    #outputs:
    #</''''''\>
    # #tomatoes#
    # --ham--
    # ~salad~
    #<\______/>
Using the Python decorator syntax:

@bread
@ingredients
def sandwich(food="--ham--"):
    print food

sandwich()
#outputs:
#</''''''\>
# #tomatoes#
# --ham--
# ~salad~
#<\______/>
The order you set the decorators MATTERS:

@ingredients
@bread
def strange_sandwich(food="--ham--"):
    print food

strange_sandwich()
#outputs:
##tomatoes#
#</''''''\>
# --ham--
#<\______/>
# ~salad~
Eventually answering the question
As a conclusion, you can easily see how to answer the question:

# The decorator to make it bold
def makebold(fn):
    # The new function the decorator returns
    def wrapper():
        # Insertion of some code before and after
        return "<b>" + fn() + "</b>"
    return wrapper

# The decorator to make it italic
def makeitalic(fn):
    # The new function the decorator returns
    def wrapper():
        # Insertion of some code before and after
        return "<i>" + fn() + "</i>"
    return wrapper

@makebold
@makeitalic
def say():
    return "hello"

print say() 
#outputs: <b><i>hello</i></b>

# This is the exact equivalent to 
def say():
    return "hello"
say = makebold(makeitalic(say))

print say() 
#outputs: <b><i>hello</i></b>
You can now just leave happy, or burn your brain a little bit more and see advanced uses of decorators.

Passing arguments to the decorated function
# It's not black magic, you just have to let the wrapper 
# pass the argument:

def a_decorator_passing_arguments(function_to_decorate):
    def a_wrapper_accepting_arguments(arg1, arg2):
        print "I got args! Look:", arg1, arg2
        function_to_decorate(arg1, arg2)
    return a_wrapper_accepting_arguments

# Since when you are calling the function returned by the decorator, you are
# calling the wrapper, passing arguments to the wrapper will let it pass them to 
# the decorated function

@a_decorator_passing_arguments
def print_full_name(first_name, last_name):
    print "My name is", first_name, last_name

print_full_name("Peter", "Venkman")
# outputs:
#I got args! Look: Peter Venkman
#My name is Peter Venkman
Decorating methods
What's great with Python is that methods and functions are really the same, except methods expect their first parameter to be a reference to the current object (self). It means you can build a decorator for methods the same way, just remember to take self in consideration:

def method_friendly_decorator(method_to_decorate):
    def wrapper(self, lie):
        lie = lie - 3 # very friendly, decrease age even more :-)
        return method_to_decorate(self, lie)
    return wrapper


class Lucy(object):

    def __init__(self):
        self.age = 32

    @method_friendly_decorator
    def sayYourAge(self, lie):
        print "I am %s, what did you think?" % (self.age + lie)

l = Lucy()
l.sayYourAge(-3)
#outputs: I am 26, what did you think?
Of course, if you make a very general decorator and want to apply it to any function or method, no matter its arguments, then just use *args, **kwargs:

def a_decorator_passing_arbitrary_arguments(function_to_decorate):
    # The wrapper accepts any arguments
    def a_wrapper_accepting_arbitrary_arguments(*args, **kwargs):
        print "Do I have args?:"
        print args
        print kwargs
        # Then you unpack the arguments, here *args, **kwargs
        # If you are not familiar with unpacking, check:
        # http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/
        function_to_decorate(*args, **kwargs)
    return a_wrapper_accepting_arbitrary_arguments

@a_decorator_passing_arbitrary_arguments
def function_with_no_argument():
    print "Python is cool, no argument here."

function_with_no_argument()
#outputs
#Do I have args?:
#()
#{}
#Python is cool, no argument here.

@a_decorator_passing_arbitrary_arguments
def function_with_arguments(a, b, c):
    print a, b, c

function_with_arguments(1,2,3)
#outputs
#Do I have args?:
#(1, 2, 3)
#{}
#1 2 3 

@a_decorator_passing_arbitrary_arguments
def function_with_named_arguments(a, b, c, platypus="Why not ?"):
    print "Do %s, %s and %s like platypus? %s" %\
    (a, b, c, platypus)

function_with_named_arguments("Bill", "Linus", "Steve", platypus="Indeed!")
#outputs
#Do I have args ? :
#('Bill', 'Linus', 'Steve')
#{'platypus': 'Indeed!'}
#Do Bill, Linus and Steve like platypus? Indeed!

class Mary(object):

    def __init__(self):
        self.age = 31

    @a_decorator_passing_arbitrary_arguments
    def sayYourAge(self, lie=-3): # You can now add a default value
        print "I am %s, what did you think ?" % (self.age + lie)

m = Mary()
m.sayYourAge()
#outputs
# Do I have args?:
#(<__main__.Mary object at 0xb7d303ac>,)
#{}
#I am 28, what did you think?
Passing arguments to the decorator
Great, now what would you say about passing arguments to the decorator itself? Well this is a bit twisted because a decorator must accept a function as an argument and therefore, you cannot pass the decorated function arguments directly to the decorator.

Before rushing to the solution, let's write a little reminder:

# Decorators are ORDINARY functions
def my_decorator(func):
    print "I am a ordinary function"
    def wrapper():
        print "I am function returned by the decorator"
        func()
    return wrapper

# Therefore, you can call it without any "@"

def lazy_function():
    print "zzzzzzzz"

decorated_function = my_decorator(lazy_function)
#outputs: I am a ordinary function

# It outputs "I am a ordinary function", because that's just what you do:
# calling a function. Nothing magic.

@my_decorator
def lazy_function():
    print "zzzzzzzz"

#outputs: I am a ordinary function
It's exactly the same. "my_decorator" is called. So when you @my_decorator, you are telling Python to call the function 'labeled by the variable "my_decorator"'. It's important, because the label you give can point directly to the decorator... or not! Let's start to be evil!

def decorator_maker():

    print "I make decorators! I am executed only once: "+\
          "when you make me create a decorator."

    def my_decorator(func):

        print "I am a decorator! I am executed only when you decorate a function."

        def wrapped():
            print ("I am the wrapper around the decorated function. "
                  "I am called when you call the decorated function. "
                  "As the wrapper, I return the RESULT of the decorated function.")
            return func()

        print "As the decorator, I return the wrapped function."

        return wrapped

    print "As a decorator maker, I return a decorator"
    return my_decorator

# Let's create a decorator. It's just a new function after all.
new_decorator = decorator_maker()       
#outputs:
#I make decorators! I am executed only once: when you make me create a decorator.
#As a decorator maker, I return a decorator

# Then we decorate the function

def decorated_function():
    print "I am the decorated function."

decorated_function = new_decorator(decorated_function)
#outputs:
#I am a decorator! I am executed only when you decorate a function.
#As the decorator, I return the wrapped function

# Let's call the function:
decorated_function()
#outputs:
#I am the wrapper around the decorated function. I am called when you call the decorated function.
#As the wrapper, I return the RESULT of the decorated function.
#I am the decorated function.
No surprise here. Let's do EXACTLY the same thing, but skipping intermediate variables:

def decorated_function():
    print "I am the decorated function."
decorated_function = decorator_maker()(decorated_function)
#outputs:
#I make decorators! I am executed only once: when you make me create a decorator.
#As a decorator maker, I return a decorator
#I am a decorator! I am executed only when you decorate a function.
#As the decorator, I return the wrapped function.

# Finally:
decorated_function()    
#outputs:
#I am the wrapper around the decorated function. I am called when you call the decorated function.
#As the wrapper, I return the RESULT of the decorated function.
#I am the decorated function.
Let's make it AGAIN, even shorter:

@decorator_maker()
def decorated_function():
    print "I am the decorated function."
#outputs:
#I make decorators! I am executed only once: when you make me create a decorator.
#As a decorator maker, I return a decorator
#I am a decorator! I am executed only when you decorate a function.
#As the decorator, I return the wrapped function.

#Eventually: 
decorated_function()    
#outputs:
#I am the wrapper around the decorated function. I am called when you call the decorated function.
#As the wrapper, I return the RESULT of the decorated function.
#I am the decorated function.
Hey, did you see that? We used a function call with the "@" syntax :-)

So back to decorators with arguments. If we can use functions to generate the decorator on the fly, we can pass arguments to that function, right?

def decorator_maker_with_arguments(decorator_arg1, decorator_arg2):

    print "I make decorators! And I accept arguments:", decorator_arg1, decorator_arg2

    def my_decorator(func):
        # The ability to pass arguments here is a gift from closures.
        # If you are not comfortable with closures, you can assume it's ok,
        # or read: http://stackoverflow.com/questions/13857/can-you-explain-closures-as-they-relate-to-python
        print "I am the decorator. Somehow you passed me arguments:", decorator_arg1, decorator_arg2

        # Don't confuse decorator arguments and function arguments!
        def wrapped(function_arg1, function_arg2) :
            print ("I am the wrapper around the decorated function.\n"
                  "I can access all the variables\n"
                  "\t- from the decorator: {0} {1}\n"
                  "\t- from the function call: {2} {3}\n"
                  "Then I can pass them to the decorated function"
                  .format(decorator_arg1, decorator_arg2,
                          function_arg1, function_arg2))
            return func(function_arg1, function_arg2)

        return wrapped

    return my_decorator

@decorator_maker_with_arguments("Leonard", "Sheldon")
def decorated_function_with_arguments(function_arg1, function_arg2):
    print ("I am the decorated function and only knows about my arguments: {0}"
           " {1}".format(function_arg1, function_arg2))

decorated_function_with_arguments("Rajesh", "Howard")
#outputs:
#I make decorators! And I accept arguments: Leonard Sheldon
#I am the decorator. Somehow you passed me arguments: Leonard Sheldon
#I am the wrapper around the decorated function. 
#I can access all the variables 
#   - from the decorator: Leonard Sheldon 
#   - from the function call: Rajesh Howard 
#Then I can pass them to the decorated function
#I am the decorated function and only knows about my arguments: Rajesh Howard
Here it is, a decorator with arguments. Arguments can be set as variable:

c1 = "Penny"
c2 = "Leslie"

@decorator_maker_with_arguments("Leonard", c1)
def decorated_function_with_arguments(function_arg1, function_arg2):
    print ("I am the decorated function and only knows about my arguments:"
           " {0} {1}".format(function_arg1, function_arg2))

decorated_function_with_arguments(c2, "Howard")
#outputs:
#I make decorators! And I accept arguments: Leonard Penny
#I am the decorator. Somehow you passed me arguments: Leonard Penny
#I am the wrapper around the decorated function. 
#I can access all the variables 
#   - from the decorator: Leonard Penny 
#   - from the function call: Leslie Howard 
#Then I can pass them to the decorated function
#I am the decorated function and only knows about my arguments: Leslie Howard
As you can see, you can pass arguments to the decorator like any function using this trick. You can even use *args, **kwargs if you wish. But remember decorators are called only once. Just when Python imports the script. You can't dynamically set the arguments afterwards. When you do "import x", the function is already decorated, so you can't change anything.

Let's practice: a decorator to decorate a decorator
OK, as a bonus, I'll give you a snippet to make any decorator accept generically any argument. After all, in order to accept arguments, we created our decorator using another function. We wrapped the decorator. Anything else we saw recently that wrapped function? Oh yes, decorators! Let's have some fun and write a decorator for the decorators:

def decorator_with_args(decorator_to_enhance):
    """ 
    This function is supposed to be used as a decorator.
    It must decorate an other function, that is intended to be used as a decorator.
    Take a cup of coffee.
    It will allow any decorator to accept an arbitrary number of arguments,
    saving you the headache to remember how to do that every time.
    """

    # We use the same trick we did to pass arguments
    def decorator_maker(*args, **kwargs):

        # We create on the fly a decorator that accepts only a function
        # but keeps the passed arguments from the maker.
        def decorator_wrapper(func):

            # We return the result of the original decorator, which, after all, 
            # IS JUST AN ORDINARY FUNCTION (which returns a function).
            # Only pitfall: the decorator must have this specific signature or it won't work:
            return decorator_to_enhance(func, *args, **kwargs)

        return decorator_wrapper

    return decorator_maker
It can be used as follows:

# You create the function you will use as a decorator. And stick a decorator on it :-)
# Don't forget, the signature is "decorator(func, *args, **kwargs)"
@decorator_with_args 
def decorated_decorator(func, *args, **kwargs): 
    def wrapper(function_arg1, function_arg2):
        print "Decorated with", args, kwargs
        return func(function_arg1, function_arg2)
    return wrapper

# Then you decorate the functions you wish with your brand new decorated decorator.

@decorated_decorator(42, 404, 1024)
def decorated_function(function_arg1, function_arg2):
    print "Hello", function_arg1, function_arg2

decorated_function("Universe and", "everything")
#outputs:
#Decorated with (42, 404, 1024) {}
#Hello Universe and everything

# Whoooot!
I know, the last time you had this feeling, it was after listening a guy saying: "before understanding recursion, you must first understand recursion". But now, don't you feel good about mastering this?

Best practices while using decorators
They are new as of Python 2.4, so be sure that's what your code is running on.
Decorators slow down the function call. Keep that in mind.
You can not un-decorate a function. There are hacks to create decorators that can be removed but nobody uses them. So once a function is decorated, it's done. For all the code.
Decorators wrap functions, which can make them hard to debug.
Python 2.5 solves this last issue by providing the functools module including functools.wraps that copies the name, module and docstring of any wrapped function to it's wrapper. Fun fact, functools.wraps is a decorator :-)

# For debugging, the stacktrace prints you the function __name__
def foo():
    print "foo"

print foo.__name__
#outputs: foo

# With a decorator, it gets messy    
def bar(func):
    def wrapper():
        print "bar"
        return func()
    return wrapper

@bar
def foo():
    print "foo"

print foo.__name__
#outputs: wrapper

# "functools" can help for that

import functools

def bar(func):
    # We say that "wrapper", is wrapping "func"
    # and the magic begins
    @functools.wraps(func)
    def wrapper():
        print "bar"
        return func()
    return wrapper

@bar
def foo():
    print "foo"

print foo.__name__
#outputs: foo
How can the decorators be useful?
Now the big question: what can I use decorators for? Seem cool and powerful, but a practical example would be great. Well, there are 1000 possibilities. Classic uses are extending a function behavior from an external lib (you can't modify it) or for a debug purpose (you don't want to modify it because it's temporary). You can use them to extends several functions with the same code without rewriting it every time, for DRY's sake. E.g.:

def benchmark(func):
    """
    A decorator that prints the time a function takes
    to execute.
    """
    import time
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print func.__name__, time.clock()-t
        return res
    return wrapper


def logging(func):
    """
    A decorator that logs the activity of the script.
    (it actually just prints it, but it could be logging!)
    """
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print func.__name__, args, kwargs
        return res
    return wrapper


def counter(func):
    """
    A decorator that counts and prints the number of times a function has been executed
    """
    def wrapper(*args, **kwargs):
        wrapper.count = wrapper.count + 1
        res = func(*args, **kwargs)
        print "{0} has been used: {1}x".format(func.__name__, wrapper.count)
        return res
    wrapper.count = 0
    return wrapper

@counter
@benchmark
@logging
def reverse_string(string):
    return str(reversed(string))

print reverse_string("Able was I ere I saw Elba")
print reverse_string("A man, a plan, a canoe, pasta, heros, rajahs, a coloratura, maps, snipe, percale, macaroni, a gag, a banana bag, a tan, a tag, a banana bag again (or a camel), a crepe, pins, Spam, a rut, a Rolo, cash, a jar, sore hats, a peon, a canal: Panama!")

#outputs:
#reverse_string ('Able was I ere I saw Elba',) {}
#wrapper 0.0
#wrapper has been used: 1x 
#ablE was I ere I saw elbA
#reverse_string ('A man, a plan, a canoe, pasta, heros, rajahs, a coloratura, maps, snipe, percale, macaroni, a gag, a banana bag, a tan, a tag, a banana bag again (or a camel), a crepe, pins, Spam, a rut, a Rolo, cash, a jar, sore hats, a peon, a canal: Panama!',) {}
#wrapper 0.0
#wrapper has been used: 2x
#!amanaP :lanac a ,noep a ,stah eros ,raj a ,hsac ,oloR a ,tur a ,mapS ,snip ,eperc a ,)lemac a ro( niaga gab ananab a ,gat a ,nat a ,gab ananab a ,gag a ,inoracam ,elacrep ,epins ,spam ,arutaroloc a ,shajar ,soreh ,atsap ,eonac a ,nalp a ,nam A
Of course the good thing with decorators is that you can use them right away on almost anything without rewriting. DRY, I said:

@counter
@benchmark
@logging
def get_random_futurama_quote():
    import httplib
    conn = httplib.HTTPConnection("slashdot.org:80")
    conn.request("HEAD", "/index.html")
    for key, value in conn.getresponse().getheaders():
        if key.startswith("x-b") or key.startswith("x-f"):
            return value
    return "No, I'm ... doesn't!"

print get_random_futurama_quote()
print get_random_futurama_quote()

#outputs:
#get_random_futurama_quote () {}
#wrapper 0.02
#wrapper has been used: 1x
#The laws of science be a harsh mistress.
#get_random_futurama_quote () {}
#wrapper 0.01
#wrapper has been used: 2x
#Curse you, merciful Poseidon!
Python itself provides several decorators: property, staticmethod, etc. Django use decorators to manage caching and view permissions. Twisted to fake inlining asynchronous functions calls. This really is a large playground.

EDIT: given the success of this answer, and people asking me to do the same with metaclasses, I did.

[decorators](http://stackoverflow.com/questions/739654/how-can-i-make-a-chain-of-function-decorators-in-python)
