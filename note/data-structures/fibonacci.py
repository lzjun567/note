import cProfile, pstats, StringIO

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
    import time 
    start = time.time()
    f0(1000000)
    end = time.time()
    print end-start
    start = time.time()
    f(1000000)
    print time.time()-start



if __name__ == '__main__':
    perfromce_profile()
