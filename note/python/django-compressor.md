#Django Compressor压缩静态文件(js/css)
原文发表于：http://foofish.net/blog/63/django-compressor  

网站开发阶段静态资源文件一般都是未经过压缩合并处理的，这对于访问量巨大的网站来说不仅浪费带宽，而且也会影响网站的访问速度。django-compressor的作用就是在项目部署的时候对静态文件压缩合并成一个文件。

下面先对settings配置文件的相关参数简要介绍再讨论Compressor的如何使用。如果你对setting文件非常了解不妨直接从第二部分开始阅读。 

###setting文件配置
早期的django处理静态资源要比较啰嗦，还要配置urlpatterns，不过自从django1.6开始加入了`django.contrib.staticfiles`这个内置app后，开发环境下处理静态资源就方便很多。

1. `django.contrib.staticfiles`是django的内置(build-in)app，用于处理js，css，images等静态资源。首先确保这个app已经包含在`INSTALLED_APPS`中，django1.6默认是包含在其中的。  
2. 指定`STATIC_URL`，比如：  
    
    	STATIC_URL = '/static/'
    
	STATIC_URL是客户端访问静态资源的根路径，比如：模版中定义的资源路径是：  
    
    	{% load staticfiles %}
    	<script src="{% static "js/blog.js" %}"></script>

	渲染后的效果是：    

    	<script src="/static/js/blog.js"></script>

3. 默认django会从app下的static子目录下查找静态文件，因此通常情况下你都是将相关静态文件放在各自的app/static目录下。为什么是这样的呢？django有个默认的配置项`STATICFILES_FINDERS`，默认值是：  

        ("django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder")

	从上面我们看到有个叫AppDirectoriesFinder的模块，就是负责在app/static目录下找静态文件的。至于FileSystemFinder我们稍后介绍。      
4. 像jquery，bootstrap等这样公用的资源文件都是在多个不同的app中共用的，如果是放在某个app中显得不符python哲学，因此django希望提供了公有的目录来放这些文件，需要用的一个配置参数是：`STATICFILES_DIRS`，比如：  

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
        '/var/www/static/',
    )

也就是静态文件可以放在磁盘的任何一个位置都可以（只要有权限访问）现在应该明白FileSystemFinder的作用了吧。就是用来查找定义在STATICFILES_DIRS中的静态文件的。  

###部署
以上是我们在开发环境下对静态资源的处理过程，那么在生产环境下是怎么处理的呢？如果还是这样由django自己来处理，那么累死django了，对于静态资源直接由Nginx这样的代理去处理好了。`django.contrib.staticfiles`提供非常方便的管理命令用来收集不同目录下的静态资源到一个统一的目录中去。 

1. 设置`STATIC_ROOT`，这个目录就是存放所有静态资源的地方.   

        STATIC_ROOT="/var/www/foofish.net/static/"

2. 运行collectstatic管理命令  

        python manage.py collectstatic

   这个命令会拷贝所有静态资源到STATIC_ROOT目录。      
3. 配置一下nginx，让访问/static/路径的请求直接访问STATIC_ROOT就可以了。  

         location /static {
            alias /var/www/foofish.net/static/; # your Django project's static files -       amend as required
        }

###第二部分：compressor
django compressor 的安装配置非常简单，主要步骤：  

安装:  

    pip install django_compressor

配置:  

    COMPRESS_ENABLED = True

    INSTALLED_APPS = (
        # other apps
        "compressor",
    )

    STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',)

默认Compress开启与否取决对于DEBUG，默认是COMPRESS_ENABLED与DEBUG的值相反。因为compress的功能本身是用在生产环境下项目发布前对静态文件压缩处理的。因此想在开发阶段(DEBUG=True)的时候做测试使用，需要手动设置COMPRESS_ENABLED=True    

使用:  

    {% load compress %}
    #处理css
    {% compress css %}
    <link href="{% static "css/bootstrap.min.css" %}" rel="stylesheet">
    <link href="{% static "css/blog-home.css" %}" rel="stylesheet">
    <link href="{% static "css/github.css" %}" rel="stylesheet">
    {% endcompress %}
    
    #处理js
    {% compress js %}
    <script src="{% static "js/jquery-1.10.2.js" %}"></script>
    <script src="{% static "js/bootstrap.js" %}"></script>
    <script src="{% static "js/blog.js" %}"></script>
    {% endcompress %}

执行命令：`python manage.py compress` ,最终文件将合并成:  

    <link rel="stylesheet" href="/static/CACHE/css/f18b10165eed.css" type="text/css">
    <script type="text/javascript" src="/static/CACHE/js/9d1f64ba50fc.js"></script>
这两文件在STATIC_ROOT目录下面。  
