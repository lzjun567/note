####配置
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

