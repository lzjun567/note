轻松理解Python装饰器
==================
或许你已经用过装饰器，它的使用方式非常简单但理解起来困难（其实真正理解的也很简单），想要理解装饰器，你需要懂点函数式编程的概念，python函数的定义以及函数调用的语法规则等，虽然我没法把装饰器变得简单，但是我希望可以通过下面的步骤让你由浅入深明白装饰器是什么。假定你拥有最基本的Python知识，本文阐述的东西可能对那些在工作中经常接触Python的人有很大的帮助。

###1、函数（Functions）
在Python里，函数是用def关键字后跟一个函数名称和一个可选的参数表列来创建的，可以用关键字return指定返回值。下面让我们创建和调用一个最简单的函数：

	>>> def foo():
	...     return 1
	>>> foo()
	1
该函数的函数体（在Python里将就是多行语句）是强制性的并且通过缩进来表明。我们可以通过在函数名后面添加双括号来调用函数。

###2、作用域（Scope）
在Python中，每个函数都会创建一个作用域。Pythonistas也可能称函数拥有它们自己的命名空间（namespace）。这意味着当在函数体里遇到变量名时，Python首先在该函数的命名空间中查找，Python包含了一些让我们查看命名空间的函数。让我们写一个简单的函数来探查一下local和global作用域的区别。

	>>> a_string = "This is a global variable"
	>>> def foo():
	...     print locals()
	>>> print globals() # doctest: +ELLIPSIS
	{..., 'a_strin': 'This ia a global variable'}
	>>> foo() # 2
	{}
内建的globals函数返回一个字典对象，它包含所有Python知道的变量名(为了清楚明了起见，我已经忽略了一些Python自动创建的变量)。在#2处我调用了函数foo，它将函数内部的local namespace里的内容打印了出来。正如我们看到的foo函数拥有自己的独立namespace，现在它还是空的。

###3、变量解析规则（variable resolution rules）
当然，这并不意味着在函数内部我们不能访问全局变量。Python的作用域规则是，变量的创建总会创建一个新的local变量，但是变量的访问（包括修改）会先查找local作用域然后顺着最邻近的作用域去寻找匹配。因此，如果我们修改foo函数来让它打印global变量，结果就会像我们希望的那样：

	>>> a_string = "This is global variable"
	>>> def foo():
	...     print a_string # 1
	>>> foo()
	This is a global variable
在#1处，Python在函数中寻找一个local变量，但是没有找到，然后在global变量中找到了一个同名的变量。

另一方面，如果我们尝试在函数里给global变量赋值，结果将不如我们所愿：

	>>> a_string = 'This is a global variable"
	>>> def foo():
	...     a_string = "test" # 1
	...        print locals()
	>>> foo()
	{'a_string': 'test'}
	>>> a_string # 2
	'This is a global variable'
正如我们所见，全局变量可以被访问到（如果是可变类型，其甚至可以被改变），但是（默认情况下）不能被赋值。在函数内部的#1处我们实际上创建了一个新的local变量，它和全局变量拥有相同的名字，它将全局变量给覆盖了。我们可以通过在foo函数内部打印local namespace来发现到它已经有了一个条目，通过对函数外部的#2处的输出结果我们可以看到，变量a_string的值根本就没有被改变。

###4、变量的生命周期（Variable lifetime）
也要注意到，变量不仅“生活在”一个命名空间里，它们还有生命周期。考虑下面的代码：

	>>> def foo():
	...     x = 1
	>>> foo()
	>>> print x # 1
	Traceback (most recent call last):
	...
	NameError: name 'x' is not defined
在#1处不仅因为作用域规则引发了问题（尽管这是出现了NameError的原因），而且也出于在Python和许多其它语言里的函数调用实现的原因。此处，我们没有任何可用的语法来获取变量x的值——字面上是不存在的。每次当调用foo函数时，它的namespace被重新构建，并且当函数结束时被销毁。

###5、函数的参数（Function parameters）
Python允许我们向函数传递参数。参数名成为了该函数的local变量。

	>>> def foo(x):
	...        print locals()
	>>> foo(1)
	{'x': 1}
Python有许多不同的定义和传递函数参数的方法。要想更详细深入地了解请参照[the Python documentation on defining functions](http://docs.python.org/tutorial/controlflow.html#more-on-defining-functions)。这里我展示一个简版：函数参数既可以是强制的位置参数(positional parameters)或者是命名参数，参数的默认值是可选的。

	>>> def foo(x, y=0): # 1
	...     return x - y
	>>> foo(3, 1) # 2
	2
	>>> foo(3) # 3
	3
	>>> foo() # 4
	Traceback (most recent call last):
	...
	TypeError: foo() takes at least 1 argument (0 given)
	>>> foo(y=1, x=3) # 5
	2
在#1处我们定义了一个带有一个位置参数x和一个命名参数y的函数。正如我们看到的，在#2处我们可以通过普通的值传递来调用函数，即使一个参数(译者注：这里指参数y）在函数定义里被定义为一个命名参数。在#3处我们可以看到，我们甚至可以不为命名参数传递任何值就可以调用函数——如果foo函数没有接收到传给命名参数y的值，Python将会用我们声明的默认值0来调用函数。当然，我们不能漏掉第一个（强制的，定好位置的）参数——#4以一个异常描述了这种错误。

都很清晰和直接，不是吗？下面变得有点儿让人疑惑——Python也支持函数调用时的命名参数而不只是在函数定义时。请看#5处，这里我们用两个命名参数调用函数，尽管这个函数是以一个命名和一个位置参数来定义的。因为我们的参数有名字，所以我们传递的参数的位置不会产生任何影响。 相反的情形当然也是正确的。我们的函数的一个参数被定义为一个命名参数但是我们通过位置传递参数—— #4处的调用foo(3, 1)将一个3作为第一个参数传递给我们排好序的参数x并将第二个参数（整数1）传递给第二个参数，尽管它被定义为一个命名参数。

Whoo!这就像用很多话来描述一个非常简单的概念：函数的参数可以有名称或者位置。

###6、内嵌函数（Nested functions）
Python允许创建嵌套函数，这意味着我们可以在函数内声明函数并且所有的作用域和声明周期规则也同样适用。

	>>> def outer():
	...     x = 1
	...     def inner():
	...         print x # 1
	...     inner() # 2
	...
	>>> outer()
	1
这看起来稍显复杂，但其行为仍相当直接，易于理解。考虑一下在#1处发生了什么——Python寻找一个名为x的local变量，失败了，然后在最邻近的外层作用域里搜寻，这个作用域是另一个函数！变量x是函数outer的local变量，但是和前文提到的一样，inner函数拥有对外层作用域的访问权限（最起码有读和修改的权限）。在#2处我们调用了inner函数。请记住inner也只是一个变量名，它也遵从Python的变量查找规则——Python首先在outer的作用域里查找之，找到了一个名为inner的local变量。

###7、函数是一等公民（Functions are first class objects in Python）
在Python中，这是一个常识，函数是和其它任何东西一样的对象。呃，函数包含变量，它不是那么的特殊！

	>>> issubclass(int, object) # all objects in Python inherit from a common baseclass
	True
	>>> def foo():
	...     pass
	>>> foo.__class__ # 1>>> issubclass(foo.__class__, object)
	True
你也许从没想到过函数也有属性，但是在Python中，和其它任何东西一样，函数是对象。（如果你发觉这令你感到困惑，请等一下，知道你了解到在Python中像其它任何东西一样，class也是对象！）也许正是因为这一点使Python多少有点“学术”的意味——在Python中像其它任何值一样只是常规的值而已。这意味着你可以将函数作为参数传递给函数或者在函数中将函数作为返回值返回！如果你从未考虑过这种事情请考虑下如下的合法Python代码：

	>>> def add(x, y):
	...     return x + y
	>>> def sub(x, y):
	...     return x - y
	>>> def apply(func, x, y): # 1
	...     return func(x, y) # 2
	>>> apply(add, 2, 1) # 3
	3
	>>> apply(sub, 2, 1)
	1
这个例子对你来说可能也不是太奇怪——add和sub是标准的Python函数，它们都接受两个值并返回一个计算了的结果。在#1处你可以看到变量接受一个函数就像其它任何普通的变量。在#2处我们调用传入apply的函数——在Python里双括号是调用操作符，并且调用变量名包含的值。在#3处你可以看出在Python中将函数当做值进行传递并没有任何特殊语法——函数名就像任何其它变量一样只是变量标签。

你之前可能见过这种行为——Python将函数作为参数经常见于像通过为key参数提供一个函数来自定义sorted内建函数等操作中。但是，将函数作为返回值返回会怎样呢？请考虑：

	>>> def outer():
	...     def inner():
	...         print "Inside inner"
	...     return inner # 1
	...
	>>> foo = outer() #2
	>>> foo # doctest:+ELLIPSIS
	<function inner at 0x...>
	>>> foo()
	Inside inner
这乍看起来有点奇怪。在#1处我返回了变量inner，它碰巧是一个函数标签。这里没有特殊语法——我们的函数返回了inner函数（调用outer()函数并不产生可见的执行）。还记得变量的生命周期吗？每当outer函数被调用时inner函数就会重新被定义一次，但是如果inner函数不被(outer)返回那么当超出outer的作用域后，inner将不复存在了。

在#2处我们可以获取到返回值，它是我们的inner函数，它被存储于一个新的变量foo。我们可以看到，如果我们计算foo，它真的包含inner函数，我们可以通过使用调用运算符（双括号，还记得吗？）来调用它。这看起来可能有点怪异，但是到目前为止没有什么难以理解，不是么？挺住，因为接下来的东西将会很怪异。

###8、闭包（Closures）
让我们不从定义而是从另一个代码示例开始。如果我们将上一个例子稍加修改会怎样呢？

	>>> def outer():
	...     x = 1
	...     def inner():
	...         print x # 1
	...     return inner
	>>> foo = outer()
	>>> foo.func_closure # doctest: +ELLIPSIS
	(<cell at 0x...: int object at 0x...>,)
从上一个例子中我们看到inner是一个由outer返回的函数，存储于一个名为foo的变量，我们可以通过foo()调用它。但是它能运行吗？让我们先来考虑一下作用域规则。

一切都依照Python的作用域规则而运行——x是outer函数了一个local变量。当inner在#1处打印x时，Python在inner中寻找一个local变量，没有找到；然后它在外层作用域即outer函数中寻找并找到了它。

但是自此处从变量生命周期的角度来看又会如何呢？变量x是函数outer的local变量，这意味着只有当outer函数运行时它才存在。只有当outer返回后我们才能调用inner，因此依照我们关于Python如何运作的模型来看，在我们调用inner的时候x已经不复存在了，那么某个运行时错误可能会出现。

事实与我们的预想并不一致，返回的inner函数的确正常运行。Python支持一种称为闭包(function closures)的特性，这意味着定义于非全局作用域的inner函数在定义时记得它们的外层作用域长什么样。这可以通过查看inner函数的func_closure属性来查看，它包含了外层作用域里的变量。

请记住，每次当outer函数被调用时inner函数都被重新定义一次。目前x的值没有改变，因此我们得到的每个inner函数和其它的inner函数拥有相同的行为，但是如果我们将它做出一点改变呢？

	>>> def outer(x):
	...     def inner():
	...         print x # 1
	...        return inner
	>>> print1 = outer(1)
	>>> print2 = outer(2)
	>>> print1()
	1
	>>> print2()
	2
从这个例子中你可以看到closures——函数记住他们的外层作用域的事实——可以用来构建本质上有一个硬编码参数的自定义函数。我们没有将数字1或者2传递给我们的inner函数但是构建了能"记住"其应该打印数字的自定义版本。

closures就是一个强有力的技术——你甚至想到在某些方面它有点类似于面向对象技术：outer是inner的构造函数，x扮演着一个类似私有成员变量的角色。它的作用有很多，如果你熟悉Python的sorted函数的key参数，你可能已经写过一个lambda函数通过第二项而不是第一项来排序一些列list。也许你现在可以写一个itemgetter函数，它接收一个用于检索的索引并返回一个函数，这个函数适合传递给key参数。

但是让我们不要用闭包做任何噩梦般的事情！相反，让我们重新从头开始来写一个decorator!

###9、装饰器（Decorators）
一个decorator只是一个带有一个函数作为参数并返回一个替换函数的闭包。我们将从简单的开始一直到写出有用的decorators。

	>>> def outer(some_func):
	...        def inner():
	...            print "before some_func"
	...            ret = some_func() # 1
	...            return ret + 1
	...        return inner
	>>> def foo():
	...        return 1
	>>> decorated = outer(foo) # 2
	>>> decorated()
	before some_func
	2
请仔细看我们的decorator实例。我们定义了一个接受单个参数some\_func的名为outer的函数。在outer内部我们定义了一个名为inner的嵌套函数。inner函数打印一个字符串然后调用some\_func，在#1处缓存它的返回值。some\_func的值可能在每次outer被调用时不同，但是无论它是什么我们都将调用它。最终，inner返回some_func的返回值加1，并且我们可以看到，当我们调用存储于#2处decorated里的返回函数时我们得到了输出的文本和一个返回值2而不是我们期望的调用foo产生的原始值1.

我们可以说decorated变量是foo的一个“装饰”版本——由foo加上一些东西构成。实际上，如果我们写了一个有用的decorator，我们可能想用装饰后的版本来替换foo，从而可以得到foo的“增添某些东西”的版本。我们可以不用学习任何新语法而做到这一点——重新将包含我们函数的变量进行赋值：

	>>> foo = outer(foo)
	>>> foo # doctest: +ELLIPSIS
	<function inner at 0x...>
现在任何对foo()的调用都不会得到原始的foo，而是会得到我们经过装饰的版本！领悟到了一些decorator的思想吗？

###10、装饰器的语法糖--@符号（The @ symbol applies a decorator to a function）
Python 2.4通过在函数定义前添加一个@符号实现对函数的包装。在上面的代码示例中，我们用一个包装了的函数来替换包含函数的变量来实现了包装。

	>>> add = wrapper(add)
这一模式任何时候都可以用来包装任何函数，但是如果们定义了一个函数，我们可以用@符号像下面示例那样包装它：

	>>> @wrapper
	... def add(a, b):
	...     return Coordinate(a.x + b.x, a.y + b.y)
请注意，这种方式和用wrapper函数的返回值来替换原始变量并没有任何不同，Python只是增添了一些语法糖(syntactic sugar)让它看起来更明显一点。

###11、\*args and \*\*kwargs
我们已经写了一个有用的decorator，但是它是硬编码的，它只适用于特定种类的函数——带有两个参数的函数。我们函数内部的checker函数接受了两个参数，然后继续将参数闭包里的函数。如果我们想要一个能包装任何类型函数的decorator呢？让我们实现一个在不改变被包装函数的前提下对每一次被包装函数的调用增添一次计数的包装器。这意味着这个decorator需要接受所有待包装的任何函数并将传递给它的任何参数传递给被包装的函数来调用它（被包装的函数）。

这种情况很常见，所以Python为这一特性提供了语法支持。请确保阅读[Python Tutorial](http://docs.python.org/tutorial/controlflow.html#arbitrary-argument-lists)以了解更多，但是在函数定义时使用\*运算符意味着任何传递给函数的额外位置参数最终以一个\*作为前导。因此：

	>>> def one(*args):
	...     print args # 1
	>>> one()
	()
	>>> one(1, 2, 3)
	(1, 2, 3)
	>>> def two(x, y, *args): # 2
	...     print x, y, args
	>>> two('a', 'b', 'c')
	a b ('c')
第一个函数one只是简单的将任何（如果有）传递给它的位置参数打印出来。正如你在#1处见到的，在函数内部我们只是引用了args变量——\*args只是表明在函数定义中位置参数应该保存在变量args中。Python也允许我们指定一些变量并捕获到任何在args变量里的其它参数，正如#2处所示。

\*运算符也可以用于函数调用中，这时它也有着类似的意义。在调用一个函数时带有一个以\*为前导的变量作为参数表示这个变量内容需要被解析然后用作位置参数。再一次以实例来说明：

	>>> def add(x, y):
	...     return x + y
	>>> lst = [1, 2]
	>>> add(lst[0], lst[1]) # 1
	3
	>>> add(*lst) # 2
	3
\#1处的代码抽取出了和#2处相同的参数——在#2处Python为我们自动解析了参数，我们也可以像在#1处一样自己解析出来。这看起来不错，\*args既表示当调用函数是从一个iterable抽取位置参数，也表示当定义一个函数是接受任何额外的位置变量。

当我们引入\*\*时，事情变得更加复杂点，与\*表示iterables和位置参数一样，\*\*表示dictionaries & key/value对。很简单，不是么？

	>>> def foo(**kwargs):
	...     print kwargs
	>>> foo()
	{}
	>>> foo(x=1, y=2)
	{'y': 2, 'x': 1}
当我们定义一个函数时我们可以用\*\*kwargs表明所有未捕获的keyword变量应该被存储在一个名为kwargs的字典中。前面的例子中的args和本例中的kwargs都不是Python语法的一部分，但是在函数定义时使用这两个作为变量名时一种惯例。就像*一样，我们可以在函数调用时使用\*\*。

	>>> dct = {'x': 1, 'y': 2}
	>>> def bar(x, y):
	...     rturn x + y
	>>> bar(**dct)
	3
###12、更通用的装饰器（More generic decorators）
用我们掌握的新“武器”我们可以写一个decorator用来“记录”函数的参数。为了简单起见，我们将其打印在stdout上：

	>>> def logger(func):
	...     def inner(*args, **kwargs): # 1
	...     print "Arguments were: %s, %s" % (args, kwargs)
	...     return func(*args, **kwargs) # 2
	... return inner
注意到在#1处inner函数带有任意数量的任何类型的参数，然后在#2处将它们传递到被包装的函数中。这允许我们包装或者装饰任何函数。

	>>> @logger
	... def foo1(x, y=1):
	...     return x * y
	>>> @logger
	... def foo2():
	...     return 2
	>>> foo1(5, 4)
	Arguments were: (5, 4), {}
	20
	>>> foo1(1)
	Arguments were: (1,), {}
	1
	>>> foo2()
	Arguments were: (),{}
	2
对函数的调用会产生一个"logging"输出行，也会输出一个如我们期望的函数返回值。

如果你一直跟到了最后一个实例，祝贺你，你已经理解了decorators了！你可以用你新掌握的“武器”做更好的事情了。你也可能考虑进一步学习，[Bruce Eckel有一篇关于decorators的优秀文章](http://www.artima.com/weblogs/viewpost.jsp?thread=240808)，他使用对象而不是函数实现了decorator。你可能会发现OOP代码比我们的纯函数版本更具可读性。Bruce还有一篇后续文，[providing parameters to decorators](http://www.artima.com/weblogs/viewpost.jsp?thread=240845)，用对象实现它可能也比函数实现更简单。最后，你也可能会去探查一下内建的[functools](http://docs.python.org/dev/library/functools.html)wraps函数，它是一个可以用在我们的装饰器中用来修改函数的签名的装饰器，修改之后d的函数更像被装饰的函数。

