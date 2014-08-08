gevent 入门篇
===========
并发编程模型主要有:  多进程,多线程,事件驱动, 协程. gevent 是基于协程的异步框架,它需要依赖于greenlet.gevent有什么样的优势? 先来通过一个简单的例子对比同步执行一个方法和使用gevent的异步方式.

普通的单线程同步执行任务

    import time

    def sync_task():
        #do something
        time.sleep(1)

    def sync_run():
        start = time.time()
        for i in range(10):
            sync_task()
        end = time.time()
    
    print("sync task executed in %f second"%(end-start))

打印结果: async task executed in 10.012671 second

如果换成多线程会是什么情况呢?  

    import threading

    def multi_thread_run():
        start = time.time()
        for i in range(10):
            t = threading.Thread(target=sync_task)
            t.start()
        end = time.time()
        print("multi thread task executed in %f second"%(end-start))

打印结果是:multi thread task executed in 0.002425 second, 呵呵,这个时间简直亮瞎了, 其实这段程序有问题,子线程还没执行完时,主线程就结束了,因此时间才那么短,其实要稍稍修改:  

    def multi_thread_run():
        start = time.time()
        threads = []
        for i in range(300):
            t = threading.Thread(target=sync_task)
            threads.append(t)
            t.start()
    
        for t in threads:
            t.join()
    
        end = time.time()
        print("multi thread task executed in %f second"%(end-start))
等所有子线程执行完之后再执行主线程,看看打印结果:  

    multi thread task executed in 1.002796 second
这是一个比较正常的结果.

换成gevent后会怎样呢?  

    import gevent
    def async_task():
        #do something
        gevent.sleep(1)
    
    def async_run():
        start = time.time()
        coroutins = []
    
        for i in range(10):
            coroutins.append(gevent.spawn(async_task))
        gevent.joinall(coroutins)
    
        end = time.time()
        print("async task executed in %f second"%(end-start))
打印输出:async task executed in 1.002012 second
gevent.spawn()方法会创建一个协程实例,gevent.joinall()是使所有的线程执行完了之后在运行主线程,这跟多线程编程是同样的概念. 发现gevent比多线程也没快多少,那gevent究竟有什么优势.现在假设把上面的10替换成1000,也就是1000线程与1000个coroutine之间的比较,会出现什么结果呢?如果是用线程的话直接报错了:`thread.error: can't start new thread`.而用协程就不会出现这种问题.  

coroutine相比thread的优势在于:  

* 创建threade的成本高,而创建coroutine的成本很低  
* thread的上下文切换成本高,而coroutin的切换速度很快  
* thread的上下文切换取决于cpu,而coroutine由自己控制  

先介绍到这里,下次接着聊  

参考[淺談coroutine與gevent](http://blog.ez2learn.com/2010/07/17/talk-about-coroutine-and-gevent/)
