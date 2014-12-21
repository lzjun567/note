RQ简介
==============
RQ(Redis Queue)是基于Redis的消息队列服务框架，任务进入队列后后台进程处理之，它能轻易集成到系统中，不过仅支持Python语言。RQ需要Redis>=2.6.0  
###安装
RQ的安装方法非常简单，直接命令：  

    pip install rq
或者如果你想尝新的话，从github安装开发版：  
    
    pip install -e git+git@github.com:nvie/rq.git@master#egg=rq

####开始
既然是基于Redis的服务，那么首先开启Redis是必须的，接着把任务放入队列中，任务就是你要处理某件的过程，就是一个普通的Python函数，通常来说，把任务放在后台进程来处理的都是一些耗时的、对即时性要求比较低的任务，比如：用户注册网站时一般的流程是填写基本信息后会即时返回注册成功的结果，接着才是收到邮件通知要求验证邮件的有效性，其中这个发邮件的任务就可以交给RQ来做。
    
    # my_module.py
    def send_mail(email):
        # 模拟发送邮件的过程
        time.sleep(2)
        return ‘ok’

然后创建一个RQ队列，把任务放入队列

    >>> from my_module import send_mail
    >>> from redis import Redis
    >>> from rq import Queue
    >>> q = Queue(connection=Redis())
    >>> result = q.enqueue(send_mail, ‘hello@qq.com’)

最后一步就是启动后台进程，后台进程会完成该任务的处理。在项目的目录下执行：  
    
    $ rqworker
    
    # 输出
    02:25:06 RQ worker started, version 0.4.6
    02:25:06
    02:25:06 *** Listening on default...
    02:25:06 default: my_module.send_mail(‘hello@qq.com’) (77778f9c-2947-4551-aa58-76a77c2c0d8e)
    02:25:07 Job OK, result = ok
    02:25:07 Result is kept for 500 seconds.
`default`是创建队列的时候默认的名字，`result＝ok`是任务的返回结果。你看，使用RQ就这么简单。  


