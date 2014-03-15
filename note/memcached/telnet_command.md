安装成功后, 确认一下memcached进程是否启动, 如下显示memecached进程已经存在.  

    lzjun@lzjun:~/workspace/note/note/memcached$ ps -eaf | grep memcached
    lzjun    10892  3749  0 11:48 ?        00:00:00 memcached -d

使用`telnet`连接Memcached, 格式:  

    telnet <hostname> <port>

默认端口是11211  

    telnet localhost 11211

####存储相关命令
**set/add/replace/append/prepend/cas**  

**set**

    set <key> <flags> <exptime> <bytes> \r\n <value> \r\n

* key:      key就是你要存储数据的键值, 数据通过key来获取
* flags:   无符号的32位整型,客户端提供的参数,用于标识数据格式,比如使用MEMCACHE_COMPRESSED表示数据压缩存储.还有json, xml等.对服务端而言,这个参数并不知道是做什么用的.
* exptime: 写入缓存失效的时间, 单位是秒, 0表示数据永久不过期, 除非当前内存不够用了使用LRU算法来回收该段内存.
* bytes:   用来缓存value的数据块的字节数, `<value>`的大小不能超过此`<bytes>` 
* \r\n:    表示回车换行
* value:   表示要缓存的数据


    set name 0 100 3
    liu
    STORED
    get name
    VALUE name 0 3
    liu
    END

如果bytes指定的值过小,而实际存储的值偏大的话,就会有Error,偏小也不行,必须相等,: 

    set name 0 100 3
    liuzhijun
    CLIENT_ERROR bad data chunk
    ERROR

**add** 只能添加不存在的key, 如果已经存在就不再存储  

    add length 0 0 4
    liuz
    STORED
    add length 0 0 4
    zjun
    NOT_STORED

**replace** 只能对已经存在的key进行替换  

    replace xxx 0 0 4
    junz
    NOT_STORED
    replace length 0 0 4
    junz
    STORED
    get length
    VALUE length 0 4
    junz
    END
**cas** : check and set , 只有版本号匹配的才能存储, 下面的6是版本号  

    cas length 0 0 4 6
    hell
    EXISTS
    gets length
    VALUE length 0 4 7
    lzju
    END
因为length的版本号是7, 而cas指定的是6,  直接返回了EXISTS    

    cas length 0 0 4 7
    hell
    STORED
    gets length
    VALUE length 0 4 8
    hell
    END
这样设计的目的是多个客户端修改同一个记录时, 防止使用改变过了key/value.  


####读取命令
**get/gets**  

    get/gets <key>

gets返回带版本信息的数据, 返回格式:  

    VALUE <key> <flags> <bytes> [versions] \r\n
    <datablock>\r\n
如:  

    gets length
    VALUE length 0 4 7
    lzju
    END
    get length name   #获取多个值 
    VALUE length 0 4
    lzju
    VALUE name 0 3
    liu
    END

####删除命令
格式:`delete <key>`  
####计数命令
格式: `incr/decr <key> <int>`, key必须存在, value必须是数字  

    set size 0 0 1
    1
    STORED
    incr size 10
    11
    decr size 5
    6

####统计命令
stats/settings/items/sizes/slabs
####工具
[memcached-tool](https://github.com/memcached/memcached/blob/master/scripts/memcached-tool) : a stats/management tool for memcached



