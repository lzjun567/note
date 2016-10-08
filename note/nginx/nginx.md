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

    # we want nginx to run as user 'www'
    user www;

    # the load is CPU-bound and we have 12 cores
    worker_processes 12;

    # explicitly specifying the path to the mandatory error log
    error_log /var/log/nginx/error.log;

    # also explicitly specifying the path to the pid file
    pid   /var/run/nginx.pid;

    # sets up a new configuration context for the 'events' module
    events {

        # we're on a Solaris-based system and have determined that nginx
        # will stop responding to new requests over time with the default
        # connection-processing mechanism, so we switch to the second-best
        use /dev/poll;

        # the product of this number and the number of worker_processes
        # indicates how many simultaneous connections per IP:port pair are
        # accepted
        worker_connections 2048;
    }
    
这个配置文件应处于nginx.conf文件的最顶部.  

使用include指令

测试：
nginx -t -c <path-to-nginx.conf>
测试include的语法有没有错误

####HTTP server 块
这是最常用的模块,位于全部配置的下面

