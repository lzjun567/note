####介绍
gevent 是一个python网络框架,对应Java的netty框架,使用greenlet提供异步API,基于libevent ,它为各种并发和网络相关的任务提供了整洁的API.   

快速基于libevent的[event loop](http://www.ruanyifeng.com/blog/2013/10/event_loop.html)  
基于greenlet的轻量级执行单元  
重用python标准api(event,queue)  
协同的socket和ssl模块  
使用标准库和第三方模块写标准阻塞socket(gevent.monkey)  
dns查询执行通过libevent-dns  
基于libevent-http的快速WSGI服务器  
####安装
>=python2.4  
greenlet  
libevent1.4.x  

    from gevent import socket
说不能导入socket,参考http://stackoverflow.com/questions/6431096/gevent-does-not-install-properly-on-ubuntu
####例子

    import gevent
    from gevent import socket
    urls = ['www.google.com','www.python.org','www.foofish.net']
    jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
    gevent.joinall(jobs, timeout=2)
    print [job.value for job in jobs]
['74.125.128.147', '82.94.164.162', '106.186.27.60']

gevent.socket与python标准库的socket有相同的接口


http://sdiehl.github.io/gevent-tutorial/  
http://architects.dzone.com/articles/threads-versus-greenlets  
http://blog.pythonisito.com/2012/07/introduction-to-gevent.html  

###翻译
####Gevent简介
官方网站是这么介绍Gevent:  
>gevent is a coroutine-based Python networking library that uses greenlet to provide a high-level synchronous API on top of the libevent event loop.  

简单翻译过来就是：[gevent](http://www.gevent.org/)一个基于协程的Python网络库，依赖于[libevent](http://www.libevent.org/)的[event loop](http://www.ruanyifeng.com/blog/2013/10/event_loop.html)使用greenlet提供高级同步API。

这段话简单描述了gevent的架构实现和技术，不过初学者看了还是一脸茫然。我能想到的能最快让人理解的定义是:  
>gevent给了你线程,但是没有使用线程  

####为什么不使用线程
为什么不使用线程呢？线程最大的缺点对我来说就是相比较greenlets(使用在gevent中的类线程的抽象概念)来说它会占用大量资源。 例如：这个模拟helloworld webserver的小程序，下面是没有使用任何并发的代码：  
 
    import sys
    import socket
    import time
    
    def sequential(port):
        s = socket.socket()
        s.bind(('0.0.0.0', port))
        s.listen(500)
    
        while True:
            cli, addr = s.accept()
            handle_request(cli, time.sleep)
    
    def handle_request(s, sleep):
        try:
            s.recv(1024)
            sleep(0.1)
            s.send('''HTTP/1.0 200 Ok 
    
    HelloWorld''')
            s.shutdown(socket.SHUT_WR)
            print '.',
        except Exception, ex:
            print 'e', ex,
        finally:
            sys.stdout.flush()
            s.close()
    
    if __name__ == '__main__':
        sequential(int(sys.argv[1]))

这段代码使用sleep，目的是是减慢handle_request方法使它更真实。使用Apache的性能测试工具做大并发测试，然而我们得到很糟糕的结果。运行： `ab -r -n 200 -c 200 http://lcoalhost:1111/`  

结果:

    Benchmarking localhost (be patient)
    Completed 100 requests
    apr_pollset_poll: The timeout specified has expired (70007)
    Total of 196 requests Completed
到最后超时了。

也许用线程会更好，那么用threads函数替换sequential函数：

    import threading
    
    def thread(port):
        s = socket.socket()
        s.bind(('0.0.0.0', port))
        s.listen(500)
        while True:
            cli, addr = s.accept()
            t = threading.Thread(target=handle_request, args=(cli, time.sleep))
            t.daemon = True
        t.start()
结果:  

    Benchmarking localhost (be patient)
    Completed 100 requests
    Completed 200 requests
    Finished 200 requests
    
    
    Server Software:        
    Server Hostname:        localhost
    Server Port:            1115
    
    Document Path:          /
    Document Length:        10 bytes
    
    Concurrency Level:      200
    Time taken for tests:   0.229 seconds
    Complete requests:      200
    Failed requests:        0
    Write errors:           0
    Total transferred:      5600 bytes
    HTML transferred:       2000 bytes
    Requests per second:    874.02 [#/sec] (mean)
    Time per request:       228.827 [ms] (mean)
    Time per request:       1.144 [ms] (mean, across all concurrent requests)
    Transfer rate:          23.90 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    5   2.9      5      11
    Processing:   101  107   3.8    107     116
    Waiting:      101  107   3.9    106     115
    Total:        105  112   1.5    112     116
    
    Percentage of the requests served within a certain time (ms)
      50%    112
      66%    113
      75%    113
      80%    114
      90%    114
      95%    115
      98%    115
      99%    116
     100%    116 (longest request)

运行`ab -r -n 200 -c 200`，总共花时是0.229秒，现在我们用gevent做类线程的模拟操作:  

    import gevent
    def greenlet(port):
        from gevent import socket
        s = socket.socket()
        s.bind(('0.0.0.0', port))
        s.listen(500)
        while True:
            cli, addr = s.accept()
            gevent.spawn(handle_request, cli, gevent.sleep)    
结果:  

    Benchmarking localhost (be patient)
    Completed 100 requests
    Completed 200 requests
    Finished 200 requests
    
    
    Server Software:        
    Server Hostname:        localhost
    Server Port:            1115
    
    Document Path:          /
    Document Length:        0 bytes
    
    Concurrency Level:      200
    Time taken for tests:   0.012 seconds
    Complete requests:      200
    Failed requests:        597
       (Connect: 0, Receive: 398, Length: 0, Exceptions: 199)
    Write errors:           0
    Total transferred:      0 bytes
    HTML transferred:       0 bytes
    Requests per second:    16837.85 [#/sec] (mean)
    Time per request:       11.878 [ms] (mean)
    Time per request:       0.059 [ms] (mean, across all concurrent requests)
    Transfer rate:          0.00 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    0   0.0      0       0
    Processing:     0    2   2.2      4       5
    Waiting:        0    0   0.0      0       0
    Total:          0    2   2.2      4       5
    
    Percentage of the requests served within a certain time (ms)
      50%      4
      66%      4
      75%      4
      80%      4
      90%      5
      95%      5
      98%      5
      99%      5
     100%      5 (longest request)

我们看到总共花时不到0.012秒。

####为什么不要一直使用gevent/greenlets呢？
为什么不要一直在gevent中greenlet？主要是归结为抢占式问题，Greenlets使用协助式多任务，而线程使用抢占式多任务，意味着一个greenlet永远不会停止执行和'yield'让给另外的greenlet,除非它使用确定的'yielding'函数(像:gevent.socket.socket.recv或gevent.sleep)，而线程，另一方面，将yield到另一个线程(有时是不可遇见的)，具体基于操作系统什么时候切换它们。  

当然,如果你使用python一段时间了，你也已经听说过关于全局解释锁(GIL)，仅仅运行单个线程执行python字节码在同一时间。所以尽管你有线程在python中,他们给一些并发(依赖于是否指定扩展库你正在使用的GIL).线程提供更少的好处比你期待的来自于C或者Java.  

####那么Gevent中还有些啥
希望我能给你一些有兴趣在学习更多的有关gevent同时它的一些扩展,你因该发现的其它的好的东西在gevent中包括:  
* 函数to monkey_patch标准库,所以你可以使用socket.socket而不是gevent.socket.例如  
* 基本的服务器处理socket连接用自己的handlers  
* 更细粒度的控制在greenlet你的spawn.  
* 同步原生合适使用greenlets 
* greenlet pools
* greenlet-local对象(如:threadlocal, 但是greenlets)
* 两个基于greentlet的WSGI服务器

在之后的帖子中,我将更细致的介绍如何在生产环境下使用gevent.所以你想怎么样,gevent有时你已经在你的toolbox了, 他的并发处理能力激发了你?,任何项目已经使用gevent?我想听听你的评论,接下来.  


