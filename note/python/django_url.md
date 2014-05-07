Django url()函数详解
======================
url()函数看起来的格式象：`url(r^/account/$', views.index, name=index)`，它可以接收四个参数，分别是两个必选参数：`regex`、`view`和两个可选参数：`kwargs`、`name`，接下来详细介绍这四个参数。  
#####regex
regex代表一个正则表达式，凡是与regex匹配的URL请求都会执行到url()函数中对应的第二个参数`view`代表的视图函数中。需要注意的是：正则表达式不会匹配URL中的域名和查询参数，如：http://www.foofish.net/article/?page=3, Django只找`article/`。正则表达式在URLconf模块加载时就编译好了，所以在匹配的时候速度是很快的。  

#####view
Django匹配正则表达式成功后，就会找到相应的视图函数，Django始终用HttpRequest对象作为第一个参数传递给视图函数，此外使用regex参数中携带的参数作为可选参数传递给视图函数。如：`url(r'^(?P<article_id>\d+)/$', views.detail, name='detail')`,，括号对`(?P<article_id>\d+)`里面的参数将作为第二个参数传递给视图函数`detail(request, article_id)`，这里参数的名字必须一模一样。因为你在url函数中显示的指定了该参数的名字，当然你也可以不显示的指定，如：`url(r'^(\d+)/$', views.detail, name='detail')`，这样在视图函数里，第二个参数的名称就随便命名了。它根据位置参数的位置来匹配。  

#####name
讲name之前，先说说Django template的内建标签url，`{% url path.to.some_view%}`可以返回视图函数对应的URL（相对域名的绝对路径），比如`url(r^/account/$', views.index, name=index)`，使用`{% url view.index %}`将返回`/accout/`，这样做可以提高模版的灵活性，如果是使用硬编码的方式，模版难以维护。  

使用标签url的时候可能会遇到一个问题就是：对于：  

    urlpatterns = patterns('',
        url(r'^archive/(\d{4})/$', archive, name="full-archive"),
        url(r'^archive-summary/(\d{4})/$', archive, {'summary': True}, "arch-summary"),
    )
同一个视图函数有多个urlconf，此时模版系统想通过视图名`archive`获取URL时，就不知所措了，name参数就是用来解决此问题的。name用来唯一区一个视图对应多个urlconf的场景。通过name来反向获取URL。  
如：

    urlpatterns = patterns('',
        url(r'^archive/(\d{4})/$', archive, name="full-archive"),
        url(r'^archive-summary/(\d{4})/$', archive, {'summary': True}, "arch-summary"),
    )

在模版中可以使用：  

    {% url "arch-summary" 1945 %}
    {% url "full-archive" 2007 %}

#####kwargs
kwargs就是一个字典类型的参数，它的使用方式如：  

        url(r'^archive-summary/(\d{4})/$', archive, {'summary': True}, "arch-summary"),

这里的kwargs 就是 `{'summary': True}`  

视图函数中就是这样使用：  

    def archive(request, archive_id, summary):


注意：  

1. 如果在url.py中有`url(r'^comment/(\d{1,9})/delete/$','delete_comment'),`的配置，如果不存在`delete_comment`这样一个函数视图，如果在模版中使用了`{% url path.to.some_view %}`这个标签，那么抛出 ViewDoesNotExit错误。仔细想想很有道理，如果视图不存在，即使匹配到了URL，当访问这个URL的时候，还是会抛ViewDoesNotExit的异常，这里Django只是在加载解析URLConf的时候就做了检查。
2. 如果在根url.py文件中使用了`url(r'^people/', include('people.urls', namespace='people'))`，这里people是一个app，那么在people这个app中的url.py中`url(r'^(\d{1,9})/$','index', name='index')`必须指定了name=index才能正常使用{% url 'people:index'%}，否则：  

        NoReverseMatch at /
        Reverse for 'subjects' with arguments '()' and keyword arguments '{}' not found

当然如果你确定不是上述问题抛出的此异常，那么可以看下这两个答案：  
http://stackoverflow.com/questions/9649587/reverse-for-with-arguments-and-keyword-arguments-not-found  
http://stackoverflow.com/questions/14882491/django-release-1-5-url-requires-a-non-empty-first-argument-the-syntax-change  
本文参考  
https://docs.djangoproject.com/en/1.1/topics/http/urls/#id2  
https://docs.djangoproject.com/en/1.1/ref/templates/builtins/#std:templatetag-url
