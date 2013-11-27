WSGI规范定义request/response循环,每次请求到达,调用一次应用中的callable,返回 zhuti 主体iterator.接着服务器遍历主体,分块写入socket.遍历完整个主体,就关闭客户端的连接.  这个流程是线程同步的,如果遇到等待数据(IO/socket/数据库),那么该线程就只能阻塞,而每个线程只能处理一个请求,但是服务器的线程池中的线程总数是有限的,如果请求数量一多的话,用户只能处于当代状态.性能很差劲.


而greenlet类似于传统线程,创建时只需消耗很少的资源.这样服务器可以生成无数greenlet而无需担心其资源会耗尽,为每个连接分配一个greenlet也毫无压力.让他们不阻塞当前线程,将cpu让给下一个greenlet.实际上是用基于gevent的伪线程替换了python的线程.

gevent.monkey.patch_all()的作用是将常见的阻塞如:socket, select等阻塞的地方使用协程跳转,而不是在那一直等待,

    gevent.joinall([
        gevent.spawn(task1),
        gevent.spawn(task2),
    ])


gevent.socket
gevent.sleep
