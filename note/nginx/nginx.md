<<<<<<< HEAD
# Nginx
Nignx是静态WEB服务器、反向代理服务器、邮件服务器。支持SSL、Virtual Host、URL Rewrite、HTTP Basic Auth、 Gzip功能。Nginx的负载均衡策略主要包括：轮询、加权轮询、和IP hash三种，还可以通过第三方模块实现，比如：url hash、fair。  

###准备工作

Nginx的一些模块需要依赖第三方库，pcre（支持rewrite模块用于正则表达式处理）、zlib（支持gzip模块，对HTTP的响应内容压缩）、openssl（支持ssl模块，HTTPS请求）  

    # CentOS 安装依赖库
    sudo yum -y install gcc gcc-c++ automake pcre pcre-devel zlib zlib-devel open openssl-devel

    # Ubuntu 安装依赖库
    sudo apt-get install libpcre3 libpcre3-dev libpcrecpp0 libssl-dev zlib1g-dev 


    wget http://nginx.org/download/nginx-1.10.0.tar.gz
    tar -zxvf nginx-1.10.0.tar.gz
    cd nginx-1.10.0
    .configure --prefix=your path  # 指定安装目录，默认安装目录为 /usr/local/nginx
    make
    make install

    ./configure --user=nginx --group=nginx --prefix=/usr/share/nginx --sbin-path=/usr/sbin/nginx --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --http-client-body-temp-path=/var/lib/nginx/tmp/client_body --http-proxy-temp-path=/var/lib/nginx/tmp/proxy --http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi --pid-path=/var/run/nginx.pid --lock-path=/var/lock/subsys/nginx --with-http_ssl_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_gzip_static_module --with-http_stub_status_module --with-http_perl_module --with-mail --with-mail_ssl_module --with-cc-opt='-m32 -march=i386' --with-openssl=/root/openssl-0.9.8o --with-pcre --with-pcre=/root/pcre-8.10 --with-zlib=/root/zlib-1.2.5 --with-http_geoip_module


    ./configure --user=nginx --group=nginx --prefix=/usr/local/nginx --sbin-path=/usr/local/sbin/nginx --conf-path=/usr/local/nginx/nginx.conf --error-log-path=/usr/local/nginx/logs/error.log --http-log-path=/usr/local/nginx/logs/access.log --pid-path=/usr/local/nginx/logs/nginx.pid --with-http_ssl_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_gzip_static_module --with-http_stub_status_module --with-http_perl_module --with-mail --with-mail_ssl_module --with-openssl=/home/liuzj/openssl-1.0.2f --with-pcre --with-pcre=/home/liuzj/pcre-8.39 --with-zlib=/home/liuzj/zlib-1.2.8 --with-http_geoip_module


    --prefix=/usr/local/nginx --pid-path=/usr/local/nginx/logs/nginx.pid --sbin-path=/usr/local/sbin/nginx --conf-path=/usr/local/nginx/nginx.conf --with-md5=/usr/lib64 --with-sha1=/usr/lib64 --with-http_ssl_module --with-http_dav_module --with-pcre=/home/liuzj/pcre-8.39 --with-zlib=/home/liuzj/zlib-1.2.8 --with-openssl=/home/liuzj/openssl-1.0.2f --without-mail_pop3_module --without-mail_imap_module --without-mail_smtp_module --without-select_module --without-poll_module --user=nginx --group=nginx

1.安装PCRE库

$ cd /usr/local/
$ wget http://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.38.tar.gz
$ tar -zxvf pcre-8.36.tar.gz
$ cd pcre-8.36
$ ./configure
$ make
$ make install

2.安装zlib库

$ cd /usr/local/ 
$ wget http://zlib.net/zlib-1.2.8.tar.gz
$ tar -zxvf zlib-1.2.8.tar.gz
$ cd zlib-1.2.8
$ ./configure
$ make
$ make install

3.安装ssl

$ cd /usr/local/
$ wget http://www.openssl.org/source/openssl-1.0.1j.tar.gz
$ tar -zxvf openssl-1.0.1j.tar.gz
$ ./config
$ make
$ make install


https://www.nginx.com/resources/admin-guide/installing-nginx-open-source/


http://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.38.tar.gz


###启停Nginx
Nginx默认安装在/usr/local/nginx目录，Nginx二进制执行文件路径为/usr/local/nginx/sbin/nginx
    
    /usr/local/nginx/sbin/nginx -h  #查看帮助文档
    
    /usr/local/nginx/sbin/nginx     # 启动nginx, -c 可以指定配置文件，默认读取/usr/local/nginx/conf/nginx.conf文件

    /usr/local/nginx/sbin/nginx -t  # 测试配置信息是否有误

    /usr/local/nginx/sbin/nginx -v  # 显示版本信息

    /usr/local/nginx/sbin/nginx -V  # 显示编译阶段的参数

    /usr/local/nginx/sbin/nginx -s stop # 强制停止nginx，与 kill 命令一样

    /usr/local/nginx/sbin/nginx -s quit # 首先关闭监听端口，停止接收新的请求，然后处理完当前所有请求在结束Nginx进程

    /usr/local/nginx/sbin/nginx -s reload  # 重新加载配置文件

###Nginx配置
Nginx通过一个master进程管理多个worker进程，worker进程数目与服务器的CPU核数对等，worker进程是真正处理HTTP服务的进程，而master负责监控管理worker进程。



Nginx配置
========
#####全局配置指令
user ：worker_processes 执行的用户，group忽略时，和user是一样的  
worker_processes：
error_log
pid:
==================
=======
>>>>>>> d9fba44c7ad9d4e980cc40d469c32ef2923100d1

./configure --prefix=/usr/local/nginx --sbin-path=/usr/local/sbin/nginx --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/run/nginx.pid --lock-path=/run/lock/subsys/nginx --user=nginx --group=nginx --with-file-aio --with-ipv6 --with-http_ssl_module  --with-http_realip_module --with-http_addition_module --with-http_xslt_module --with-http_image_filter_module --with-http_geoip_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_degradation_module --with-http_stub_status_module --with-http_perl_module --with-mail --with-mail_ssl_module --with-pcre 





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

