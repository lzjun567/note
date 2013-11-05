####Python 常见异常

+ NameError：访问未申明的变量  
+ ZeroDevisionError：除数为零  
+ SyntaxError：解释器语法错误，该错误不是在运行时发生的  
+ IndexError：索引超出序列范围  
+ KeyError：访问字典中不存在的Key
+ IOError：任何与IO相关的操作  
+ AttributeError：访问对象中不存在的属性
+ ValueError：任何数值操作，如int('zzz')
+ TypeError：期待的类型与实际的类型不一致时，如float(('hello',))，float只能接收字符串或者数字  

+ KeyboardInterupt，SystemExit：人为引发的错误，用户想终止程序运行  

####异常结构图：

    --BaseException
        |- KeyboarInterrupt
        |- SystemExit
        |- Exception
            |-(built-in exception)

####异常写法：

    try:
        #业务代码块
    except Exception1 [,reason]:   #异常原因是可选参数
        #异常处理代码块


    try:
        #业务代码块
    except (Exception1,Exception2) [,reason]:   #异常原因是可选参数，可以接收多个异常
        #异常处理代码块


    try:
        #业务代码块
    except Exception1 [,reason]:   #异常原因是可选参数
        #异常处理代码块
    except Exception2 [,reason]:   #异常原因是可选参数
        #异常处理代码块            #可以分别处理多个异常


    try:
        #业务代码块
    except Exception1 [,reason]:   #异常原因是可选参数
        #异常处理代码块
    else:
        #else字句，没有发生异常时，执行此处的代码
        
    try:
        #业务代码块
    except Exception1 [,reason]:   #异常原因是可选参数
        #异常处理代码块
    else:
        #else字句，没有发生异常时，执行此处的代码
    finally:
        #最终程序都会执行到这里来，无论异常发生与否

