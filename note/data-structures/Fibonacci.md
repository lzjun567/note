斐波那契数列(Fibonacci)递归与非递归的性能对比
===============================================
费波那契数列由0和1开始，之后的数就由之前的两数相加 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584,……….  
####递归算法
用递归算法来求值,非常好理解.伪代码:  

    f(n) = 0                (n=0)
    f(n) = 1                (n=1)
    f(n) = f(n-1) + f(n-2)  (n>1)
实现:  

    def f(n):
        if n==0:
            return 0
        elif n==1:
            return 1
        elif n>1:
            return f(n-1) + f(n-2)

####非递归算法

    def f(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        if n>1:

            prev = 1    #第n-1项的值
            p_prev = 0  #第n-2项的值
            result = 1  #第n项的值

            for i in range(1,n):
               result = prev+p_prev 
               p_prev = prev
               prev = result
            return result

功能实现了,但是代码比较冗长,函数是要对前两项做特殊判断.现在优化一下,如何才能更通用,即使是第0个和第1个也能运用到for循环呢?假设在 0, 1, 1, 2, 3, 5, 8, 13... 之前还有两项, 是-1和1, 即: -1, 1, 0, 1, 1, 2, 3, 5, 8, 13, 21, 34,这样就通用了:  

    def f(n):
        prev = 1
        p_prev = -1
        result = 0
        for i in range(n+1):
            result = prev+p_prev
            p_prev = prev
            prev = result
        return result

现在评估一下他们的性能:  写一个性能装饰器.  

    def perfromce_profile(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            rtn = func(*args, **kwargs)
            end = time.time()
            print end-start
            return rtn
        return wrapper
他不能用在递归方法中. 所以最终还是写了这么个方法:  

    import time
    
    def f0(n):
        if n==0:
            return 0
        elif n==1:
            return 1
        elif n>1:
            return f(n-1) + f(n-2)
    
    def f(n):
          prev = 1
          p_prev = -1
          result = 0
          for i in range(n+1):
              result = prev+p_prev
              p_prev = prev
              prev = result
          return result   
    
    def perfromce_profile():
        start = time.time()
        f0(1000000)
        end = time.time()
        print end-start
        start = time.time()
        f(1000000)
        print time.time()-start
    
    
    
    if __name__ == '__main__':
        perfromce_profile() 

看出性能对比了吧:  

    54.2904469967
    27.7642970085

所以用递归弊端还是不少
