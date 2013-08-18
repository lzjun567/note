wsgi:web服务器和应用程序app之间统一的接口，简单来说就是规范的接收web请求（request）


python paste 是一个WSGI工具包，在wsgi的基础上包装了几层。

    def app(environ, start_response):
        start_response('200 OK', [('content-type', 'text/html')])
        return ['Hello world!']

WSGI规范的参数. app需要完成的任务是响应envrion中的请求，准备好响应头和消息体，然后交给start_response处理，并返回响应消息体。

Paste 包含一个module，用来帮助实现WSGI中间件，它包含WSGI包装器，还包括了一个简单的webserver，用来处理WSGI请求。


WSGI middleware
WSGI标准是一个接口，它允许应用使用Python代码区处理HTTP请求。


egg包是目前最流行的python应用打包部署方式
