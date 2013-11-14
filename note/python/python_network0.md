###《Python网络编程》学习笔记一
学习新知识最好的方式就是一边记笔记，一边写代码，为了更深入地了解网络编程、异步通信、事件驱动编程等领域知识，开始系统学习相关知识，主要参考书目包括《Python网络编程》、《Twisted Network Progamming Essentials》，gevent、celey、rabbitmq等官方文档。  

网络编程离不开TCP/IP，因此想写好一个网络相关的程序，那么理解TCP/IP原理是最基本的要求。你能想象如果不理解TCP/IP，能写出一个goagent出来吗？  

TCP/IP是一些协议的合集，每个TCP连接有一个IP地址和一个端口号来唯一标识。TCP是一个可靠的连接，为了实现其可靠性，每个信息包都包含一个**校验码**，它用来保证信息在传输过程中没有被更改的代码。信息包到达目的地后，接收方会对比校验码和数据，如果校验码不对，那么该包就丢弃。  

为了防止信息包的丢失，TCP要求接收方每收到一个信息包都反馈一下，如果没有提供反馈，那么就自动重新发送，直到接受者收到为止。  

为了防止信息包重复或顺序错误，TCP每传送一个信息包都会传送一个序号，接受方会检查这个序号，确保收到该信息包，并把全部信息包按顺序重新合并。如果接收方看到一个已经存在的序号，那么该信息包就会被丢弃。  

####建立socket
对于客户端程序来说，建立socket需要两个步骤，第一：建立一个socket对象，第二：把他连接到远程服务器。建立socket对象时，需要告诉系统两个事情：**通信类型和协议家族**。通信类型指明用什么协议来传输数据，协议包括IPv4(当前Internet标准）、IPv6（将来的Internet标准）等，协议家族定义了数据如何被传输。  

对于Internet通信类型基本上都是AF_INET（对应IPv4），协议家族一般是表示TCP通信的SOCK_STREAM或表示UDP通信的SOCK_DGRAM。对于TCP通信，建立socket的代码一般是：  

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
连接socket，需要一个元组参数，包含远程主机名和端口：  

    socket.connect(('www.google.com', 80))

建立连接后，可以获取连接信息：  

    s.getsocketname()  #返回本身IP和端口号，每次运行时段口号不尽相同
    s.getpeername()    #返回远程机器的IP地址和端口号

####用socket通信
用socket接收和发送数据有两种方式，分别是socket对象和文件类对象，其中socket对象提供了send()、sendto()、recv()、recvfrom()接口，文件类对象提供了read()、write()、readline()接口。socket对象能精确控制数据的读写。而类文件对象是面向线性的对象，不适用于UDP  

    import socket, sys
    
    port = 80
    host = 'localhost'
    filename = '/subject/2412'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    #socket对象 
    s.sendall(filename + "/r/n")
    buf = s.recv(2048)
    while len(buf):
        sys.stdout.write(buf)
        buf = s.recv(2048)

    #类文件对象
    fd = s.makefile("rw", 0)
    fd.write(filename+"\r\n")
    for line in fd.readlines():
        sys.stdout.write(line)

####socket异常
* 与一般I/O和通信问题有关的异常是：socket.error  
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            pass

        try:
            port = socket.getservbyname(textport, 'tcp')
        except socket.error:
            pass

        try:
            s.sendall("GET / HTTP/1.1\r\n\r\n")
        except socket.error:
            pass

        try:
            s.recv(2048)
        except socket.error:
            pass:

* 与查询地址信息有关的异常：socket.gaierror  

        try:
            s.connect((host, port))
        except socket.gaierror:
            pass
* 与其他地址错误有关的异常：socket.herror  

