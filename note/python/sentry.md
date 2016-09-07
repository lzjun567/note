#Sentry
软件界有这么一条定论：不管多么优秀的软件一定会有Bug，只是Bug的多少和严重性不一样而已。有些Bug是在用户使用你的系统过程中发现的，热心的网友会把Bug触发的场景耐心地汇报给软件提供者，不那么热心的网友一言不合就卸载你们的产品了，而你还不知道问题出在哪里，你只能去无穷无尽的日志中去查找问题。如果有一款软件能帮助你，当应用系统出现Bug时，或者有异常信息时，主动告知开发者，及时处理掉这些问题，毫无疑问地会给开发者带来极大的便利。而Sentry就是这样一款系统，她能实时收集业务系统的错误日志，并以邮件或者其他方式通知用户。

Sentry基于Python语言开发，它可以集成在大部分语言编写的系统中，不论是Python、Ruby、GO还是Java、抑或者PHP。Sentry也是在站在巨人的肩膀上诞生的，它使用的WEB框架是Django，依赖MySQL/PostgreSQL、Redis、Celery。

###安装
Sentry的安装可以基于Python的[VirtualENV](http://foofish.net/blog/88/virtualenv)来，也可以直接安装在系统中，不过还是推荐用VirtualENV的方式来安装，因为Sentry依赖的Python包非常多，避免跟其他包发生冲突。
	

	pip install sentry
	# sentry默认使用postresql作为存储，如果要使用MySQL的话，要使用：  
	pip install sentry[mysql]

###初始化
sentry初始化前确保所有依赖包已经安装成功、有一个Redis2.8以上版本的服务可用。
	
	sentry init
初始化之后，会在当前用户目录下生成配置文件。
	
	.sentry/
	├── config.yml
	└── sentry.conf.py



修改配置文件
	
	vim ~/.sentry/sentry.conf.py  主要是数据库的配置

	DATABASES = {
	    'default': {
	        # You can swap out the engine for MySQL easily by changing this value
	        # to ``django.db.backends.mysql`` or to PostgreSQL with
	        # ``django.db.backends.postgresql_psycopg2``
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': 'sentry_server',
	        'USER': 'sentry',
	        'PASSWORD': '****',
	        'HOST': '',
	        'PORT': '',
	        'OPTIONS': {
	            'init_command': 'SET storage_engine=INNODB',
	        }
	    }
	}

初始化数据库

	sentry upgrade
创建用户
	
	sentry createuser

###启动服务

首先确保MySQL，Redis服务已经开启，启动senry服务和任务队列服务：
	
	sentry run web  # 运行web服务
	sentry  run worker # 队列服务

###客户端接入
Sentry服务启动后，就可以把服务正式接入到我们的系统了，如果你的系统的Python应用，那么Sentry提供了`reven`包，可以无缝地接入到业务系统中：  
	
	pip install raven --upgrade
如果是于Tornado集成的话可以按照步骤：  
	
	setup:

	application = tornado.web.Application(handlers)
	application.sentry_client = AsyncSentryClient(
	    'https://<key>:<secret>@app.getsentry.com/<project>'
	)
	
	这里的https就是在sentry的web管理后台创建project后生成的

	useage

	class AsyncExceptionHandler(SentryMixin, tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        try:
            raise ValueError()
        except Exception as e:
            response = yield tornado.gen.Task(
                self.captureException, exc_info=True
            )
        self.finish()
