#python3
###特性一：高级拆箱
Python2 中可以以这样的方式进行拆箱操作：   
	
	>>> a, b = range(2)
	>>> a
	0
	>>> b
	1
你可以把序列中多个多个元素赋值给多个变量名，不过在 Python2 中必须满足变量名的个数与序列中的元素的个数是相等的，否则会报错。
然而，在 Python3 中你可以这样：  
	
	>>> a, b, *rest = range(10)
	>>> a
	0
	>>> b
	1
	>>> rest
	[2, 3, 4, 5, 6, 7, 8, 9]

拆箱时，可以仅仅指定有限个变量名，而剩下的元素可以放在一个列表中。 而且，`rest`变量可以放在任何位置：  
	
	>>> a, *rest, b = range(10)
	>>> a
	0
	>>> b
	9
	>>> rest
	[1, 2, 3, 4, 5, 6, 7, 8]

	>>> *rest, b = range(10)
	>>> rest
	[0, 1, 2, 3, 4, 5, 6, 7, 8]
	>>> b
	9

实用场景1：获取文件的首尾行：  
	
	>>> with open("using_python_to_profit") as f:
	...     first, *_, last = f.readlines()
	>>> first
	'Step 1: Use Python 3\n'
	>>> last
	'Step 10: Profit!\n'
实用场景2：重构函数：
	
	#重构前
	def f(a, b, *args):
    stuff
    # 重构后
	def f(*args):
	    a, b, *args = args
	    stuff