redis简介
==========
很喜欢redis作者[antirez](http://antirez.com/latest/0)里面的几句话：  
> **代码就像一首诗**, **设计就是与复杂性做斗争**, **coding是一件很辛苦的事, 唯一的办法是享受它, 如果它不能带来快乐就停止它**.  

Redis是数据库，性能俱佳的非关系性数据库，提供了5种不同的数据类型，分别是：字符串（Strings）、列表（Lists）、集合（Sets）、有序集合（Sorted sets） 、哈希（Hashes）。它能把数据持久化到磁盘，通过复制（replication）提高读性能，通过客户端共享提高写性能。  

###下载安装
Redis安装路径/usr/local/redis，源码保存路径：/usr/local/src，[redis官方站点](http://redis.io/download)下载:  
    
    $  cd /usr/local/src/
    $ wget http://download.redis.io/releases/redis-3.2.3.tar.gz
    $ tar xzf redis-3.2.3.tar.gz
    $ cd redis-3.2.3/src

    $ make all
        Hint: It's a good idea to run 'make test' ;)
    $ make test
        \o/ All tests passed without errors!
        Cleanup: may take some time... OK
    $ make PREFIX=/usr/local/redis-3.2.3 install

    $ mkdir /usr/local/redis-3.2.3/{conf,logs,data}
    $ ln -s /usr/local/redis-3.2.3 /usr/local/redis

    $ tree /usr/local/redis
        /usr/local/redis
        ├── bin
        │   ├── redis-benchmark
        │   ├── redis-check-aof
        │   ├── redis-check-rdb
        │   ├── redis-cli
        │   ├── redis-sentinel -> redis-server
        │   └── redis-server
        ├── conf
        ├── data
        └── logs

###修改配置
redis配置生成可以通过utils/uinstall_server.sh文件交互式生成，也可以直接拷贝模版redis.conf进行修改：  
    
    cp redis.conf /usr/local/redis/conf/6379.conf
主要需改的地方有两处，分别是logfile：redis日志存放位置，dir:redis持久化保存数据的目录
    
    logfile "/usr/local/redis/logs/6379.log"
    dir /usr/local/redis/data
其他可以都可以选择默认配置项。查看配置项可以使用：
    
    grep -Ev '^$|#' /usr/local/redis/conf/6379.conf

###启动

    $ /usr/local/redis/bin/redis-server /usr/local/redis/conf/6379.conf

### 测试
连接redis
    
    $ /usr/local/redis/bin/redis-cli -p 6379

    127.0.0.1:6379> keys *
    1) "_kombu.binding.celeryev"
    127.0.0.1:6379> set name sentry
    OK
    127.0.0.1:6379> keys *
    1) "name"
    2) "_kombu.binding.celeryev"
    127.0.0.1:6379> get name
    "sentry"
    127.0.0.1
    
