python单元测试：Fudge
=====================
在单元测试过程中，如果代码中多处有数据库访问（读/写）、第三方请求，或者代码中包含一些复杂的对象，真实环境中难以被触发的对象的时候，该如何写单元测试呢？

使用模拟对象机制测试python代码，模拟对象（mock object）可以取代真实对象的位置，用于测试一些与真实对象进行交互或依赖真实对象的功能，模拟对象的目的就是创建一个轻量级的，可控制的对象来代替测试中需要的真实对象，模拟真实对象的行为和功能，方便测试。

###Stub、Mock、Fake区别
> Stub:
> For replacing a method with code that returns a specified result

简单来说就是可以用stub去fake（伪造）一个方法，阻断原来方法的调用
> Mock:
> A stub with an expectations that the method gets called

简单来说mock就是stub + expectation, 说它是stub是因为它也可以像stub一样伪造方法,阻断对原来方法的调用, expectation是说它不仅伪造了这个方法,还期望你(必须)调用这个方法,如果没有被调用到,这个test就fail了

> Fake:
> objects actually have working implementations, but usually take some shortcut which makes them not suitable for production

简单来说就是一个真实对象的一个轻量级的完整实现


mock对象的使用范畴：
真实对象具有不可确定的行为，产生不可预测的结果（如：天气预报）
真实对象很难被创建
真实对象的某些行为很难被触发


###(Fudge)[http://farmdev.com/projects/fudge/]
Fudge是一个类似于Java中的JMock的纯python的mock测试模块，主要功能就是可以伪造对象，替换代码中真实的对象，来完成测试。fudge主要用来模拟那些在应用中不容易构造或者比较复杂的对象（如项目中涉及mongodb或者redis模块，使用fudge后在测试的时候可以不需要真正的redis环境就能测试代码），从而使测试顺利进行。  

####如何使用fudge

    import twitter_oauth   #pip install twitter_oauth
    
    consumer_key = '***'
    consumer_secret = '***'
    oauth_token = "***"
    oauth_token_secret = '***'
    
    
    def post_msg_to_twitter(msg):
        # create GetOauth instance
        get_oauth_obj = twitter_oauth.GetOauth(consumer_key, consumer_secret)
        # create Api instance
        api = twitter_oauth.Api(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
        # post update
        api.post_update(u'Hello, Twitter:' + msg)
        print("send:%s" % msg)

因为`twitter_oauth`是独立的模块，因此只要调用了正确的方法，`post_msg_to_twitter`方法就一定能正确执行。Twitter在大陆没法直接请求访问，那怎么测试知道它没有问题呢? 使用fudge就能完成我们的任务，把twitter相关的对象伪造(fake)出来，只要我们自己的业务逻辑测试正确，那么测试就通过。    

    import fudge


    @fudge.patch('twitter_oauth.GetOauth', 'twitter_oauth.Api')
    def test_post_msg_to_twitter(msg, FakeGetOauth, FakeApi):
        FakeGetOauth.expects_call() \
            .with_args('***', '***')
    
        FakeApi.expects_call() \
            .with_args('***', '***', '***', '***') \
            .returns_fake() \
            .expects('post_update').with_args(u'Hello, Twitter:okey')
    
        post_msg_to_twitter(msg)
    
    
    if __name__ == '__main__':
        test_post_msg_to_twitter('okey')


* patch装饰器会在测试阶段根据装饰器里面的参数伪造对象，作为测试方法`test_post_to_twitter`的参数。这些伪造的对象就是stub或者mock或者是fake  
* Fudge可以根据你的需求严谨或随意的声明expectation。
    * 如果你不关心具体的参数，就可以调用`fudge.Fake.with_args()`不需要指定任何参数，如果要指定的话就必须是指定正确的参数（换句话说就是不能随意指定）
    * 如果你不关心方法调用与否，那么就可以用`fudge.Fake.provides()`代替`fudge.Fake.expects()`，这样即使代码中没有调用，测试用例也不会fail
    * 如果不关心方法的参数的具体值，那么可以用`fudge.Fake.with_arg_count()`来代替`fudge.Fake.with_args()`


###fudge模块
####fudge
* fudge.patch(*obj_paths)：测试装饰器，里面的参数都将作为fake对象将导出作为测试方法的参数使用。

        @fudge.patch('os.remove')
        def test(fake_remove):
            #do sutff
    patch方法会去调用fudge.clear\_calls()，fudge.verify()和fudge.clear\_expectations()，verify()方法才是真正验证所有方法是不是按照期待的那些调用了。
        
        def test():
            db = fudge.Fake('db').expects('connect')
            # fudge.verify()
    上面这个test函数如果没有用fudge.patch(), fudge.test() 或者 fudge.with_fakes()修饰，那么fudge就不会主动去验证方法是否得到执行，必须加上fudge.verify()方法才会触发调用。加上verify()就会提示你connect没有被调用：

        File "E:\Python27\lib\site-packages\fudge-1.0.3-py2.7.egg\fudge\__init__.py", line 453, in assert_called
            raise AssertionError("%s was not called" % (self))
        AssertionError: fake:db.connect() was not called
* fudge.test：装饰器，直接使用fake，而不是通过patch

        @fudge.test
        def test():
            db = fudge.Fake('db').expects('connect')
    不过绝大多数时候你都应该使用fudge.patch而不是fudge.test

* fudge.Fake：这个一个类，用来替换真实对象的fake对象，如上例

* fudge.calls(call)：重新定义一个call，相当于给call换一个名字

        def hello():
            print "hello there"
        
        def test_calls():
            f = fudge.Fake().provides("anthor_hello").calls(hello)
            f.anthor_hello()  #输出"hello there"

* expects(call_name)：表示期待调用call\_name方法
* expects_call()：表示该对像将得到调用
* provides(call_name)：这个方法与expects的区别是call\_name可以没有被调用

更多参考：[fudge](http://farmdev.com/projects/fudge/api/fudge.html)

####fudge.inspector
`fudge.inspector.ValueInspector`实例可以作为一种更具表现力的对象（Value inspector）传递给`fudge.Fake.with_args()`方法，为了更方便记忆ValueInspector实例简称为`arg`：  
    
    from fudge.inspector import arg
    image = fudge.Fake('image').expects('save').with_args(arg.endswith('.jpg'))
上面的测试代码就表示传递给save方法的参数必须是以`.jpg`结尾的值，否则测试没法通过

* arg.any()：表示没有任何约束
* contains(part)：必须包含指定的part参数
* has_attr(**attributes)：传递给方法的参数必须有属性在指定的attributes中
    
        class User:
            first_name="Bob"
            last_name = "James"
            job = "jazz musician"
        
        
        def test_has_attr():
            from fudge.inspector import arg
            db = fudge.Fake('db').expects("update").with_args(arg.has_attr(
                first_name="Bob",
                last_name="James"
            ))
            db.update(User())
* passes_test(test)：参数传递到test函数中必须返回True才能通过测试

        def is_valid(s):
            assert s in ['apple', 'ms', 'fb'], ('unexpected company %s' % s)
            return True
        
        def test_passes_test():
            system  = fudge.Fake('system').expects('set_company').with_args(arg.passes_test(is_valid))
            system.set_company('fb')
        
* startswith(part)：参数必须以part开头

更多参考：[fudge.inspector](http://farmdev.com/projects/fudge/api/fudge.inspector.html)

####fudge.patcher
* fudge.patcher.with\_patched\_object(obj, attr\_name, patched\_value)：装饰器，在被装饰的方法调用前给attr_name一个新的值patched\_value，方法执行完以后attr\_name再恢复成原来的值

        from fudge import with_patched_object
        
        class Session:
            state = 'clean'
            
        @with_patched_object(Session, "state", 'dirty')
        def test():
            print(Session.state)
        
        if __name__ == "__main__":
            test()
            print (Session.state)
    输出：

        dirty
        clean
    这样做的好处就是能独立于每个测试而不影响原来对象的完整性。

* fudge.pathcher.patched\_context(obj, attr\_name, patched\_value)：作用和上面的with\_patched\_object一样，只是用法上不一样而已，他的用法是：

        with patched_context(Session, 'state', 'dirty'):
            print Sessioin.state
就是[with语句](http://www.python.org/dev/peps/pep-0343/)的使用方式。

####tornado.test
由于python的单元测试模块式同步的，测试tornado中的异步代码有三种方式

1. 使用类似tornado.gen的yield生成器 tornado.testing.gen_test.

        class MyTestCase(AsyncTestCase):
        @tornado.testing.gen_test
        def test_http_fetch(self):
            client = AsyncHTTPClient(self.io_loop)
            response = yield client.fetch("http://www.tornadoweb.org")
            # Test contents of response
            self.assertIn("FriendFeed", response.body)
2. 手工方式调用self.stop，self.wait
        
        class MyTestCase2(AsyncTestCase):
            def test_http_fetch(self):
                client = AsyncHTTPClient(self.io_loop)
                client.fetch("http://www.tornadoweb.org/", self.stop)
                response = self.wait()
                # Test contents of response
                self.assertIn("FriendFeed", response.body)
3. 回调函数的方式：

        class MyTestCase3(AsyncTestCase):
            def test_http_fetch(self):
                client = AsyncHTTPClient(self.io_loop)
                client.fetch("http://www.tornadoweb.org/", self.handle_fetch)
                self.wait()
            def handle_fetch(self, response):
                #此处产生的异常会通过stack+context传播到self.wait方法中去
                self.assertIn("FriendFeed", response.body)
                self.stop()

后两者的原理是一样的，wait方法会一直运行IOLoop，直到stop方法调用或者超时（timeout默认是5's）2中的fetch的第二个参数self.stop相当于3中的self.handle_fetch，都是一个回调函数，区别就在于把sotp当成回调函数时，响应内容就会通过self.wait()函数返回，而像3中一样写一个自定义的回调函数，响应内容就会作为参数传递给该函数。可以详细查看下[tornado.testing.py](http://www.tornadoweb.org/en/stable/_modules/tornado/testing.html)这个文件中的stop和wait方法。

默认情况下，每个单元会构造一个新的IOLoop实例，这个IOLoop是在构造HTTP clients/servers的时候使用。如果测试需要一个全局的IOLoop，那么就需要重写get_new_ioloop方法。 源码：

    def setUp(self):
        super(AsyncTestCase, self).setUp()
        self.io_loop = self.get_new_ioloop()
        self.io_loop.make_current()

    def get_new_ioloop(self):
            """Creates a new `.IOLoop` for this test.  May be overridden in
            subclasses for tests that require a specific `.IOLoop` (usually
            the singleton `.IOLoop.instance()`).
            获取全局IOLoop时，调用IOLoop.instance()这个单例方法即可
            """
            return IOLoop()

* tornado.testing.AsyncHTTPTestCase  
这个类是AsyncTestCase的子类，一个测试用例会启动一个HTTP server，AsyncHTTPTestCase的子类必须重写`get_app()`方法，这个方法返回`tornado.web.Application`实例。application实例就是实际代码的application。  

        app = tornado.web.Application(handlers=[
               (r'/sleep', SleepHandler),
               (r'/now', JustNowHandler)
           ])
    返回这个app就好了。测试用例通常使用`self.http_client`来请求（fetch）这个server上的url。

        class MyHTTPTest(AsyncHTTPTestCase):
            def get_app(self):
                app = tornado.web.Application(handlers=[
                       (r'/sleep', SleepHandler),
                       (r'/now', JustNowHandler)
                ])
                return app
            def test_now(self):
                self.http_client.fetch(self.get_url('/'), self.stop)
                response = self.wait()
                self.assertIn('xx', response.body)  #判断返回的请求体中是否有字符串`xx`

    其实self.http_client就是一个AsyncHTTPClient实例，从源码中查看到：  

        def get_http_client(self):
            return AsyncHTTPClient(io_loop=self.io_loop)

####fakeredis
[fakeredis](https://github.com/jamesls/fakeredis)是[redis-py](https://github.com/andymccurdy/redis-py)的实现，模拟redis服务器通信的模块。应用场景只有一个：写单元测试。
