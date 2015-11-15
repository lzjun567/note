RQ（Rdis Queue）
=============
一个任务（Job）就是一个普通的Python对象，其具体表现形式就是一个函数，比如下面的`count_words_at_url`函数。该任务会在worker（后台）进程中被异步调用，任何Python函数都可以被异步调用，只需把该函数的引用以及它所必须的参数推送到到队列里面即可，这个过程叫入队（enquueing）。  
###任务入队（Enqueueing jobs）
把任务放入队列中时，首先声明一个函数：  
    
    #somewhere.py

    import requests

    def count_words_at_url(uri):
        resp = requests.get(url)
        return len(resp.text.split())

注意到没有？这个函数没有任何特别的地方，任何可被调用的Python函数都可以放入到RQ队列中。接下来把这个耗时的统计操作放到后台去做，可以简单的这样做：  
    
    #rqtest.py

    from rq import Queue
    from redis import Redis
    from somewhere import count_words_at_url

    #告诉RQ连接哪个Redis
    redis_conn = Redis() # 默认连接localhost:8986
    q = Queue(connection = redis_conn)  #默认队列没有使用其他参数
    
    #延迟执行count_words_at_url函数
    job =  q.enqueue(count_words_at_url, “http://foofish.net”)

    print job.result  # => None
        
    # 现在，等待一会儿，直到worker完成
    time.sleep(2)
    print job.result

**注意**：这里的`somewhere`是该统计任务的模块名称，不要把上面这段代码放在同一个模块中，`__main__`模块中的函数（任务）不能被worker（后台进程）处理。否者会报错：  
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
其实队列默认是有个名字的，其默认名称为“default”，你也可以很简单地通过手动的方式为其指定：  
    
    q = Queue(‘low’, connection=redis_conn)
    q = enqueue(count_words_at_url, “http://nvie.com”)
正如上面代码那样，你可以给队列取任意的名字，按照你自己的想法灵活处理不同的队列任务，不过一种通用的命名规则是根据优先级、重要程度来处理的方式来命名（比如：high, medium, low）。  
####任务入队列时指定额外参数
如果你想给enqueue函数本身传递参数，比如超时处理的timeout，那么这时候你需要使用enqueue_call函数：  

    q = Queue(‘low’, connection=redis_conn)
    q.enqueue_call(func=count_words_at_url, args=(‘http://nvie.com’), timeout=30)
本质上，从RQ的源码来看enqueue函数最终还是会把参数封装好传递给enqueue_call去执行。

####equeue的第一个参数可接收的数据类型
* 函数的引用，比如上例中的`cont_words_at_uri`
* 某对象的实例方法的引用
* 字符串，这个字符串是某个函数所在的路径的字符串格式，比如：获取队列中任务的个数  

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
此外，你还可以获取任务列表的ID集合，任务对象集合，或者是根据某个任务id获取该任务对象：  
    
    queued_job_ids = q.job_ids  # 从队列中获取所有任务的id集合
    queued_jobs = q.jobs        # 获取队列中的任务实例集合
    job =  q.fetch_job(“my_id”) # 根据任务id获取任务实例
其中id一般使用uuid.uuid4函数生成，Job实例保存了任务的id、入队的时间等信息   
>>Job(‘1eb1e613-5c35-4701-a62f-9047986591d5’, enqueued_at=datetime.datetime(2014, 12, 8, 14, 56, 1))

###RQ设计哲学
RQ以极简设计原则实现任务队列，你不需要设置任何前置条件，不需要指定任何频道（channels）、exchanges、路由规则（routing rules）等等，你唯一要做的就是把任务放入到队列中。RQ没有使用多先进的broker（中间人）去做消息路由，你可能认为这是一个很好的特性或者是一个障碍，这主要取决于你要解决的问题。  

最后，它不需要任何协议，因为他依赖的是(pickle)[https://docs.python.org/2/library/pickle.html]去序列化任务，因为他仅仅是一个支持Python的系统。  

###有延迟的result
当任务进入队列后，`queue.enqueue()`方法会返回一个`Job`实例，这只不是一个代理对象而已，它可用于检查真实任务对象的返回结果。就因为这个目的，它有一个很便利的属性`reuslt`，当任务还没完成时，会返回`None`，或者是非None值（假如任务有返回值的话）。  

###`job`装饰器
如果你要是熟悉Celery，那么你应该使用过他的`@task`装饰器，从RQ的0.3版本开始也有个类似的装饰器：  
    
    from rq.decorators import job
    @job(‘low’, connection=my_redis_conn, timeout=5)
    def add(x, y):
        return x + y

    job = add.delay(3, 4)
    time.sleep(1)
    print job.result

**注意：**，如果打印结果是None，那么你应该要开启名为`low`的后台进程（rqworker low）去执行该队列中的任务才能看到预期的结果。  

###忽略worker进程
有时为了测试目的，你并不需要把任务委托给worker进程异步处理，实现此功能只需在构建队列的构造器里传递`async=False`即可（0.3.1以上版本才支持）  
    
    from rq import Queue
    from redis import Redis
    from somewhere import count_words_at_url

    q = Queue(‘low’, async=False, connection=Redis())
    job = q.enqueue(count_words_at_url, “http://foofish.net”)
    print job.result
以上代码就是在一个进程中同步执行任务了，worker不再去处理该任务。此行为类似与Celery的中`ALWARYS_EAGER`  
###任务依赖
RQ0.4.0中的新特性支持多个任务的链式执行，因为一个任务有可能依赖于另一个任务，使用`depends_on`参数即可：  
    
    q = Queue(‘low’, async=False)
    report_job = q.enqueue(generate_report)
    q.enqueue(send_report, depends_on=report_job)
它能把一个很大的任务切分成多个更小的任务来处理，一个任务依赖于另外一个任务其实就是只有等到它所依赖的任务处理完成后才进入队列中去，如果所依赖的任务处理失败了，那么该任务也不会被处理了。  

    # rqtest_utils.py
    import requests
    
    def count_words_at_url(url):
        resp = requests.get(url)
        raise ValueError(“for test”) # 模拟异常发生
        return len(resp.text.split())
    
    
    def count_all_words(*args):
        return sum(args)

    #rqtest.py
    from rq import Queue
    from redis import Redis
    
    from rqtest3_utils import count_words_at_url
    from rqtest3_utils import count_all_words
    
    
    q = Queue(‘low’, connection=Redis())
    job0 = q.enqueue(count_words_at_url, “http://foofish.net”)
    job2 = q.enqueue(count_all_words, depends_on=job0)
    
执行rqtest.py时，从worker进程中看到结果：  

    20:32:42 low: rqtest3_utils.count_words_at_url('http://foofish.net') (3acfc6f5-3845-4241-bc36-c58abb79604a)
    20:32:42 Starting new HTTP connection (1): foofish.net
    20:32:43 ValueError: for test
    Traceback (most recent call last):
      File "/Library/Python/2.7/site-packages/rq/worker.py", line 479, in perform_job
        rv = job.perform()
      File "/Library/Python/2.7/site-packages/rq/job.py", line 466, in perform
        self._result = self.func(*self.args, **self.kwargs)
      File "/Users/lzjun/Workspace/my/toolkit/rqtest3_utils.py", line 11, in count_words_at_url
        raise ValueError("for test")
    ValueError: for test
    
    20:32:43 Moving job to failed queue.
job2并没有继续处理下去了，如果job2没有依赖job0的话，那么即使Job0执行失败了，Job2也会继续执行。  

参考：    
[http://python-rq.org/docs/](http://python-rq.org/docs/)  
[RQ项目分析](https://github.com/redisbook/book/blob/master/usage/rq_project/rq_project_analysis.md)









