Django Signals
===========================
当某个事件发生的时候，signal(信号)允许senders(发送者)用来通知receivers(接收者)，通知receivers干嘛？你想要recivers干嘛就可以干嘛。这在多处代码对同一个事件感兴趣的时候就有用武之地了。 比如：Django提供了一个built-in signal，叫`django.core.signals.request_finished`，这个signal会在一个HTTP请求完成后发送。下面就用一个简单的实例说明：在每个请求完成后打印"request finished"    
####编写receiver
reciver是一个普通的callable对象，简单来说就是一个可被调用的函数，但是需要注意的是它需要接收一个参数`sender`和一个关键字参数`**kwargs`

    def my_callback(sender, **kwargs):
        '''
        这是个receiver函数
        你可以在这里做爱做的的事情
        '''
        print sender
        print kwargs
        print("Request finished!")

这里我们先撇开sender和kwargs后面再分析，reciver函数写好之后，就需要把`request_finished`信号连接(注册)到`my_callback`。  

    from django.core.signals import request_finished
    request_finished.connect(my_callback)

现在请求一个URL路径`/hello`，后台打印的结果：  

    [31/Mar/2014 21:52:33] "GET /hello/ HTTP/1.1" 200 263
    <class 'django.core.handlers.wsgi.WSGIHandler'>
    {'signal': <django.dispatch.dispatcher.Signal object at 0x0262E510>}
    Request finished!

以上就是一个signal的执行流程，那么django内部是怎么实现的呢？为什么调用了reciver.connect后，my_callback就能得到执行了呢？且看源代码分析：  

request_finished定义在文件django.core.signals.py里面：  

    from django.dispatch import Signal

    request_started = Signal()
    request_finished = Signal()
    got_request_exception = Signal(providing_args=["request"])

`request_finished`就是Signal的实例。GET请求完成后会执行`my_callback`方法，为什么这么神奇，我们顺着request_finished的思路来猜想，既然是请求完成了，那么此时response对象也生成了，那么神奇的事情一定是在response里面发生的。去response.py文件里面看看：django.http.response.py  

    def close(self):
        for closable in self._closable_objects:
            try:
                closable.close()
            except Exception:
                pass
        signals.request_finished.send(sender=self._handler_class)
看到在response的close方法里面有send方法，而且这个sender就是我们在前面看到的`django.core.handlers.wsgi.WSGIHandler'`，这个send方法会发送信号给所有的receivers。  

    #Signal.send方法的源代码：

    responses = []
    if not self.receivers or self.sender_receivers_cache.get(sender) is NO_RECEIVERS:
        return responses

    for receiver in self._live_receivers(sender):
        response = receiver(signal=self, sender=sender, **named)
        responses.append((receiver, response))
    return responses

注意：你可以看到在for循环里面迭代的调用的receiver方法。以上就是django内部的执行原理。思考下send方式是signal的而不是sender的呢？从面向对象的角度来说，**谁是对象的拥有者，谁就提供相应的方法**。比如汽车的drive方法肯定是由汽车提供而不是由人。


####小结
我们需要做的只是编写receiver，然后调用signal.connect方法，相当于把receiver注册到signal上去。当事件触发时，相应的signal就会通知所有注册的receivers得到调用。尼玛，这是传说中的观察者模式。  

连接receiver函数还有另外一个方法，用装饰器：  

    @receiver(request_finished):
    def my_handler(sender, **kwages):
        '''
django还提供了很多内置的signals，比如：

1. django.db.models.signals.pre_save & django.db.models.signals.post_save

    Sent before or after a model’s save() method is called.

2. django.db.models.signals.pre_delete & django.db.models.signals.post_delete

    Sent before or after a model’s delete() method or queryset’s delete() method is called.

3. django.db.models.signals.m2m_changed

    Sent when a ManyToManyField on a model is changed.

signal还可以指定具体的senders，比如pre_save这个signal是在Model对象保存在被发送，但是我希望只有某一类Model保存的时候才发送，你就可以指定：  

    @receiver(pre_save, MyModel):
    def my_handle(sender, **kwargs):
        pass
这样每次只有保存MyModel实例后才会发送，其他的XXModel就会忽略掉。  

完！

