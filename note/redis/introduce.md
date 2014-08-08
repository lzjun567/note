redis简介
==========
很喜欢redis作者[antirez](http://antirez.com/latest/0)里面的几句话, **代码就像一首诗**, **设计就是与复杂性做斗争**, **coding是一件很辛苦的事, 唯一的办法是享受它, 如果它不能带来快乐就停止它**.  

####下载安装
[redis官方站点](http://redis.io/download)下载:  

    $ wget http://download.redis.io/releases/redis-2.8.7.tar.gz
    $ tar xzf redis-2.8.7.tar.gz
    $ cd redis-2.8.7
    $ make

####运行连接

    $ src/redis-server
顺利的话, redis会正常启动, 启动信息  
redis 2.8.7 (00000000/0) 32 bit  
Running in stand alone mode  
Port: 6379  
PID: 11156  

使用内建的客户端连接:  

    $ src/redis-cli 
    127.0.0.1:6379> set foo bar
    OK
    127.0.0.1:6379> get foo
    "bar"
    127.0.0.1:6379> 



