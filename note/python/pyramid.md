Pyramid学习笔记
========================
Static Assets：
------------------------------
static assets 指那些非Python原文件，如：图片、css、js、还有目录（没有__init__.py文件的目录）以及Mako或Chamelon模板文件。  
####理解asset规范：

    render_to_response('myapp:templates/some_template.pt', {}, request)
这里的字符串`myapp:templates/some_template.pt`就是一个**asset specification**它由两部分组成：  
1. package name （myapp）
2. asset name （templates/some_template.pt），相对于package目录

这两部分用一个冒号分隔开。pyramid使用pkg_resources API 解析 package name 和 asset name成相对于操作系统上的绝对路径。比如some_template.pt最后可能是解释成/home/workspace/project/templates/some_templates.pt。这样模板引擎就能正确加载、解析、执行模板文件了。  

####Serving Static Assets：
pyramid使得存放在文件系统目录里的assets文件通过用户游览器来查看成为可能。使用pyramid.config.Configurator.add_static_view()，例如：

    # config is an instance of pyramid.config.Configurator
    config.add_static_view(name='static', path='/var/www/static')

name参数代表URL的前缀，path参数代表文件系统中的路径，当用户访问URL:`/static/foo.css`时，返回文件/var/www/static/foo.css。  

    # config is an instance of pyramid.config.Configurator
    config.add_static_view(name='static', path='some_package:a/b/c/static')
这是使用assets specification 代替前面那种绝对路径的方式作为path参数的值，  
 
    add_static_view(name, path, **kw)
添加视图用来渲染静态资源（如：图片、js、css等）。当某个静态资源的URL被访问时，pyramid会添加一个视图来渲染该资源。它的可选参数cache_max_age，用来设置静态支援的过期时间。这个方法通常与pyramid.request.Request.static_url()结合使用。  

    request.static_url('mypackage:static/foo.css') =>

                        http://example.com/static/foo.css

    request.static_path('mypackage:static/foo.css') =>

                        /static/foo.css

add_static_view的name参数也可以是一个完全限定URL（full qualified URL) 如：  

    add_static_view('http://example.com/images', 'mypackage:images/')

那么static_url和static_path返回的都是：http://example.com/imgage/foo.css



Security
--------------------------------------------
authorization:授权，权限  
authentication:认证，登录验证  
pyramid 提供了一个可选的授权认证系统,在view被调用之前,认证系统可以根据request中的证书与上下文资源一道决定是否可以被访问.它的工作流程是这样的:  

* 当用户访问应用的时候生成request对象
* 基于request,context resource 通过 resource location定位到(traversal or URL dispatch)
* view callable 通过view lookup定位到 
* authentication policy 生效,传递给request,返回一些principal identifiers.
* 如果authorization policy 激活了,view configuration 关联了view callable,t它有关联的permission,那么authorization policy 会传递给context.permission关联view,允许或拒绝
* 如果authorization policy允许访问,视图就会被调用
* 如果authorization policy拒绝访问,视图就不会被调用,取而代之代之的是forbidden view

Security在Pyramid中，不想很多系统，清晰明确的分离的authorization和authentication。authorization仅仅是一种机制，通过request中的管理证书（credential）解析成一个或多个principal。

####使authorization生效
默认情况下，pyramid的authorization policy是不生效的。所有试图可以完全在匿名用户下能访问。为了保护试图基于安全设置防止被执行，你需要使authorization policy生效。  




 
