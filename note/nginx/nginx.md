#Nginx配置文件结构详解
Nginx的配置文件的主体结构式下面这种形式，主要包括六大块：main、events、http、upstream、server、location。

    {
        main
        events : {}
        http   : {
                upstream {

                }
                server : {
                        main
                        location : {}
                    }
            }
    }

#####全局配置指令：main
    
    #定义 Nginx 运行的用户和用户组,默认由 nobody 账号运行, windows 下面可以注释掉。 
    user www www;

    # nginx 进程数，一般建议设置为1。起的太多了，可能会带来性能上的问题。但是如果是耗 CPU 的操作的话，建议等于 CPU 总核心数。
    # 这个还可以和 worker_cpu_affinity 配合
    worker_processes 1;

    # 全局错误日志定义类型，[ debug | info | notice | warn | error | crit ]
    error_log /var/log/nginx/error.log info;

    # 进程文件，windows 底下可以注释掉
    pid /var/run/nginx.pid;

    # 一个nginx进程打开的最多文件描述符(句柄)数目，理论值应该是最多打开文件数（系统的值ulimit -n）与nginx进程数相除，
    # 但是nginx分配请求并不均匀，所以建议与ulimit -n的值保持一致。
    worker_rlimit_nofile 65535;
  
这段配置代码应处于nginx.conf文件的最顶部。 

####events模块
工作模式及请求连接数上限，nginx的工作模式可选值有select、poll、epoll、kqueue，在Linux中使用epoll，可以提高nginx的性能。并发总数是 worker\_processes 和 worker\_connections 的乘积 ，即 max\_clients = worker\_processes * worker\_connections

    events {
        use   epoll; 
        #单个后台worker process进程的最大并发链接数    
        worker_connections  1024;
    }

####http模块
http模块的主要配置主要是通过HTTP协议请求时响应给浏览器的一些设置，主要包括：字符集、客户端上传文件的最大值、连接超时设置，访问日志格式设置，是否开启gzip压缩等。

    http {

        include       mime.types; //包含指定的文件（可以含路径）
        
        default_type  application/octet-stream; 
        
        #charset   utf-8;  //默认的字符编码集
        
        client_max_body_size  8m; //配置客户端能够上传的文件大小
        
        keepalive_timeout  65;  //连接超时时间
        
        #gzip  on; //是否开启gzip压缩（还需要和其它配置项共同起作用）
        
        //配置访问日志格式
        
        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
        
                                     '$status $body_bytes_sent "$http_referer" '
        
                                      '"$http_user_agent" "$http_x_forwarded_for"';
        
         access_log  /var/nginx/logs/host.access.log  main;  //启用访问日志，并且指定日志采用的格式
         ... 其他配置
    }

#####gzip
启用gzip可以提高网页的传输速度，页面经过gzip压缩后的大小通常要比原网页小30%甚至更多，不过gzip在服务端也是会销毁cpu资源的。因此不能压缩比例控制在合适的范围既能提高客户端的请求速度，也不会对服务端造成太大的压力。

    gzip on; //用于开启或关闭gzip模块(on/off)
    
    gzip_min_length 1k;  //设置允许压缩的页面最小字节数，页面字节数从header头得content-length中进行获取。默认值是0，不管页面多大都压缩。建议设置成大于1k的字节数，小于1k可能会越压越大。
    
    gzip_buffers 4 16k;  //设置系统获取几个单位的缓存用于存储gzip的压缩结果数据流。4 16k代表以16k为单位，原始数据大小以16k为单位的4倍申请内存。
    
    gzip_http_version 1.1;  //识别http的协议版本(1.0/1.1)
    
    gzip_comp_level 2;  //gzip压缩比，1压缩比最小处理速度最快，9压缩比最大但处理速度最慢(传输快但比较消耗cpu)
    
    gzip_types text/plain application/x-javascript text/css application/xml;   //匹配mime类型进行压缩，无论是否指定,”text/html”类型总是会被压缩的。

    gzip_vary on;  //和http头有关系，加个vary头，给代理服务器用的，有的浏览器支持压缩，有的不支持，所以避免浪费不支持的也压缩，所以根据客户端的HTTP头来判断，是否需要压缩

常见参考配置：

    gzip on;
    gzip_min_length 1k;
    gzip_buffers 16 64k;
    gzip_http_version 1.1;
    gzip_comp_level 6;
    gzip_types text/plain application/x-javascript text/css application/xml;
    gzip_vary on;
    
####虚拟主机server模块

server模块是嵌套在http模块里面的，是用户配置虚拟主机的地方，它可以作为单独的文件以include的形式包含到http模块中。最简单的server配置是这样的：
    
    server {
        listen       80;
        server_name  localhost;
        access_log  logs/localhost.access.log  main;
        error_log logs/localhost.error.log;
        
        root /data/static_site_dir;
        index index.html;
    }
listen指令告诉nginx监听80端口，server_name指令可以设置基于域名的虚拟主机，也可以是主机的名字。access\_log指令不尽可以放在http模块，也可以放在server模块中，这里的log是只会记录访问该虚拟主机下得日志。

####location模块

#####资源文件

####代理请求

#####静态站点



使用include指令

测试：
nginx -t -c <path-to-nginx.conf>
测试include的语法有没有错误

####HTTP server 块
这是最常用的模块,位于全部配置的下面

http://div.io/topic/1395

