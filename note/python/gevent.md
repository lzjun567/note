####介绍
gevent 是一个python网络框架,对应Java的netty框架,使用greenlet提供异步API,基于libevent  
快速基于libevent的[event loop](http://www.ruanyifeng.com/blog/2013/10/event_loop.html)  
基于greenlet的轻量级执行单元  
重用python标准api(event,queue)  
协同的socket和ssl模块  
使用标准库和第三方模块写标准阻塞socket(gevent.monkey)  
dns查询执行通过libevent-dns  
基于libevent-http的快速WSGI服务器  
####安装
>=python2.4  
greenlet  
libevent1.4.x  

    from gevent import socket
说不能导入socket,参考http://stackoverflow.com/questions/6431096/gevent-does-not-install-properly-on-ubuntu
####例子

    import gevent
    from gevent import socket
    urls = ['www.google.com','www.python.org','www.foofish.net']
    jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
    gevent.joinall(jobs, timeout=2)
    print [job.value for job in jobs]
['74.125.128.147', '82.94.164.162', '106.186.27.60']

gevent.socket与python标准库的socket有相同的接口


http://sdiehl.github.io/gevent-tutorial/
