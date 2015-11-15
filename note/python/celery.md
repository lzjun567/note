Celery-----分布式任务队列
=======================
高可用：任务失败或者连接断了自动重试  
快：一个celery进程可以处理上10万的任务每分钟  
灵活：可以自定义实现每一个模块  
 


如果你是windows用户，首先现在安装[redis](https://github.com/MSOpenTech/redis/blob/2.6/bin/release/redisbin64.zip)，

安装celery  

    pip install celery
    pip install redis
默认会安装好celery最新版本

创建Celery实例

    app = Celery('tasks', broker='redis://localhost')

创建任务(tasks.py)：  
    
    from celery import Celery

    app = Celery('tasks', broker='redis://localhost')
    
    @app.task
    def add(x, y):
        return x + y
        
启动worker进程：  
    
    celery -A tasks worker --loglevel=info
    

在代码中调用task:  
    
    >>> from tasks import add
    >>> add.delay(4, 4)
    
执行过程：先会把任务放入队列（默认名字就叫celery）中，如果worker进程启动了，就会从队列中取出来，消费掉它。


AMQP 术语
MESSAGE
        
     {'task': 'myapp.tasks.add',
     'id': '54086c5e-6193-4575-8308-dbab76798756',
     'args': [4, 4],
     'kwargs': {}}
    



发送消息的客户端是生产者
接受消息的是消费者
broker:消息服务器，路由消息从生产者到消费者



 交换机（exchange）: 接收消息，转发消息到绑定的队列,有好几种类型
 
 正常发送消息和接受消息的步骤：  
    1. 创建exchange
    2. 创建队列
    3. 绑定队列到exchange上
    
  
 把Celery应用到Application中去：  
 










Highly Available

Workers and clients will automatically retry in the event of connection loss or failure, and some brokers support HA in way of Master/Master or Master/Slave replication.


















