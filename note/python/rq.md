RQ
=============
RQ（Rdis Queue）

一个任务（Job）就是一个普通的Python对象，其具体表现形式就是一个函数，比如下面的`count_words_at_url`函数。该任务会在worker（后台）进程中被异步调用，任何Python函数都可以异步调用，只需简单通过推送该函数的引用以及它要接收的参数到队列里面即可，整个过程叫入队（enquueing）。  

###任务入队（Enqueueing jobs）
把任务放入队列中，首先声明一个函数：  
    
    #somewhere.py

    import requests

    def count_words_at_url(uri):
        resp = requests.get(url)
        return len(resp.text.split())

注意到没有？这个函数没有任何特别的地方，任何可被调用的Python函数都可以放入到RQ队列中。  

接下来把这个费时的统计操作放到后台去做，可以简单的这样做：  
    
    #rqtest.py

    from rq import Queue
    from redis import Redis
    from somewhere import count_words_at_url

    #告诉RQ连接哪个Redis
    redis_conn = Redis() # 默认连接localhost:8986
    q = Queue(connection = redis_conn)  #默认队列不使用任何参数
    
    #延迟执行count_words_at_url函数
    job =  q.enqueue(count_words_at_url, “http://foofish.net”)

    print job.result  # => None
        
    # 现在，等待一会儿，直到worker完成
    time.sleep(2)
    print job.result

**注意**：这里的`somewhere`是该统计任务的模块名称，不要把上面这段代码放在同一个模块中，否者会报错：  
>>Functions from the __main__ module cannot be processed by workers.

在somewhere.py所在目录运行命令“rqworker”可以看到队列处理任务的过程：  
    
    18:37:43 RQ worker started, version 0.4.6
    18:37:43
    18:37:43 *** Listening on default...
    18:38:05 default: somewhere.count_words_at_url(‘http://www.baidu.com’) (a6cc042b-e5d1-44b7-b5fa-a07abcb0c5c0)
    18:38:05 Starting new HTTP connection (1): www.baidu.com
    18:38:06 Job OK, result = 2173
    18:38:06 Result is kept for 500 seconds.

####给队列指定名字
其实队列默认是有个名字的，其默认名称为“default”，你也可以很简单的通过手动的方式为其指定：  
    
    q = Queue(‘low’, connection=redis_conn)
    q = enqueue(count_words_at_url, “http://nvie.com”)
正如上面代码那样，你可以给队列取任意的名字，按照你自己的想法灵活处理不同的队列任务，一种通用的命名规则是根据优先级，重要程度来处理（比如：high, medium, low）。  
####任务入队列时指定额外参数
如果你想给enqueue函数本身传递参数，比如超时处理的timeout，那么这时候你需要使用enqueue_call函数：  

    q = Queue(‘low’, connection=redis_conn)
    q.enqueue_call(func=count_words_at_url, args=(‘http://nvie.com’), timeout=30)
本质上，从RQ的源码来看enqueue函数最终还是会把参数封装好传递给enqueue_call去执行。

####equeue的第一个参数可接收的数据类型
* 函数的引用，比如上例中的`cont_words_at_uri`
* 某对象的实例方法的引用
* 字符串，这个字符串是某个函数所在的路径的字符串格式，比如：  

        q = Queue(‘low’, connection=redis_conn)
        q.enqueue(‘my_package.my_module.my_func’, 3, 4)

###队列（Queue）的其他操作
除了任务入队之外，Queue还有很多实用的方法，比如：  
    
    from rq import Queue
    from redis import Redis

    redis_conn = Redis()
    q = Qeueue(connection=redis_conn)

    #获取队列中任务的个数
    print len(q)
**注意：**len方法是在[这个commit](https://github.com/nvie/rq/commit/c1dc30eae30aefe9ab501012a3cd9c5e2aac0c58)才加入的，先前的版本要调用`q.count`查看队列中的任务个数。有时任务执行的速度非常快，还没来得及打印任务就执行完了，看不出效果，因此可以一次往队列中多加些任务，比如：  
    
    queue = Queue(connection=redis_conn)
    for i in range(10):
        queue.enqueue(count_words_at_url, “http://www.baidu.com”)

    print ‘count:’, queue.count
除此之外，你还可以获取任务列表的ID集合，任务对象集合，或者是根据某个任务id获取该任务对象：  
    
    queued_job_ids = q.job_ids  # 从队列中获取所有任务的id集合
    queued_jobs = q.jobs # 获取队列中的任务实例集合
    job =  q.fetch_joB(“my_id”) # 根据任务id获取任务实例
其中id一般使用uuid.uuid4函数生成，Job实例保存了任务的id、入队的时间等信息   
>>Job(‘1eb1e613-5c35-4701-a62f-9047986591d5’, enqueued_at=datetime.datetime(2014, 12, 8, 14, 56, 1))

###RQ的设计哲学
RQ以极简的设计原则实现队列，你不需要设置任何前置条件，不需要指定任何频道（channels）、exchanges、路由规则（routing rules）等等，你唯一要做的就是把任务放入到队列中。  
RQ不需要使用高级的broker去做消息路由，你可能认为这是一个很好的特性或者是一个障碍，但这取决于你要解决的问题。  
最后，它不需要任何协议，因为他依赖的是pickle去序列化任务，因为他仅仅是一个支持Python的系统。  

###有延迟的result
当任务进入队列后，`queue.enqueue()`方法会返回一个`Job`实例，这只不是一个代理对象而已，它可用于检查真是任务对象的结果。就因为这个目的，它有一个很便利的属性`reuslt`，当任务还没完成时，会返回`None`，或者是非None值（假如任务在第一步有返回值）。  

###`job`装饰器
如果你要是熟悉Celery，那么你应该使用过他的`@task`装饰器，从RQ>=0.3开始，也有个类似的装饰器：  
    
    from rq.decorators import job
    @job(‘low’, connection=my_redis_conn, timeout=5)
    def add(x, y):
        return x + y

    job = add.delay(3, 4)
    time.sleep(1)
    print job.result

**注意：**，如果打印结果是None，那么你应该要开启名为`low`的后台进程（rqworker low）去执行该队列中的任务才能看到预期的结果。  






参考：    
[http://python-rq.org/docs/](http://python-rq.org/docs/)  
[RQ项目分析](https://github.com/redisbook/book/blob/master/usage/rq_project/rq_project_analysis.md)









