#Sentry
软件界有这么一条定论：不管多么优秀的软件一定会有Bug，只是Bug的多少和严重性不一样而已。如果有一款软件能帮助你，当应用系统出现Bug时，或者有异常信息时，主动告知开发者，及时处理掉这些问题，毫无疑问地会给开发者带来极大的便利。而Sentry就是这样一款系统，她能实时收集业务系统的错误日志，并以邮件或者其他方式通知用户。

Sentry基于Python语言开发，它可以集成在大部分语言编写的系统中，不论是Python、Ruby、GO还是Java、抑或者PHP。Sentry也是在站在巨人的肩膀上诞生的，它使用的WEB框架是Django，依赖MySQL/PostgreSQL、Redis、Celery。

###安装
Sentry的安装可以基于Python的[Virtualenv](http://foofish.net/blog/88/virtualenv)来，也可以直接安装在系统中，不过还是推荐用Virtualenv的方式来安装，因为Sentry依赖的Python包非常多，避免跟其它应用发生冲突。
	

	pip install sentry
	pip install sentry[mysql]  # sentry默认使用postresql作为存储，如果要使用MySQL的话，要使用：  

###初始化
sentry初始化前确保所有依赖包已经安装成功。
	
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
Sentry服务启动后，就可以把服务正式接入到我们的应用系统了，如果你的系统是基于Python的应用，那么Sentry提供了`reven`包，可以无缝地接入到业务系统中：  
	
	pip install raven --upgrade
如果是于Tornado集成的话可以按照步骤：  
	
	# setup:

	application = tornado.web.Application(handlers)
	application.sentry_client = AsyncSentryClient(
	    'https://<key>:<secret>@app.getsentry.com/<project>'
	)

	这里的https就是在sentry的web管理后台创建project后生成的

	# useage

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

### Supervisor进程管理
Sentry和Celery都不是作为后台进程启动的，管理起来不方便，这时可以用Supervisor来管理，优雅地实现进程的管理。
	
	[program:sentry]
	command=sentry --config=/root/.sentry/sentry.conf.py run web
	process_name=sentry_server
	numprocs=1
	redirect_stderr = true
	environment=C_FORCE_ROOT="true"
	stdout_logfile = /data/server/log/sentry.log


	[program:celery]
	command=sentry --config=/root/.sentry/sentry.conf.py run worker
	process_name=celery_server
	numprocs=1
	environment=C_FORCE_ROOT="true"
	redirect_stderr = true
	stdout_logfile = /data/server/log/celery.log

###后续

	export C_FORCE_ROOT="true"

	supervisor

	nginx

默认启动的时候加载配置文件  ~/.sentry/sentry.conf.py 文件，但是如果显示指定配置文件启动的时候报错：  

	sentry --config=/root/.sentry/sentry.conf.py run web
错误信息：
>sentry.runner.importer.ConfigurationError: `system.secret-key` MUST be set. Use 'sentry config generate-secret-key' to get one.

可以修改配置文件：
	
	system.secret-key='you key'
