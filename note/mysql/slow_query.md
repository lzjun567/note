MySQL慢查询
==========
慢查询日志是由一些SQL语句构成的，当查询时间超过了`long_query_time`的值时会生成慢查询日志，long_query_time的最小值是1s，默认值是10s。  

检查MySQL慢查询是否开启：  

    mysql> show variables like '%slow%';
    +---------------------+----------------------------------------------------------+
    | Variable_name       | Value                                                    |
    +---------------------+----------------------------------------------------------+
    | slow_launch_time    | 2                                                        |
    | slow_query_log      | OFF                                                      |
    | slow_query_log_file | E:\Program Files\mysql-5.6.10-winx64\data\lzjun-slow.log |
    +---------------------+----------------------------------------------------------+
    3 rows in set (0.00 sec)

默认MySQL的slow_query_log是OFF，开启的方法有：  

 1. 启动MySQL的时候开启：

        mysqld  --slow_query_log=[{0|1}]   #MySQL5.5及以上版本
    不指定值或者1表示开启，0表示关闭
        mysqld --slow_query_log_file=file_name
    指定日志文件的保存的地方，如果指定，那么默认是保存在存放数据目录的`homename-slow.log`文件中。  

        mysqld  --log-slow-queries[=file_name]  #MySQL5.1及以下版本

 2. MySQL启动后设置

        set global slow_query_log=[1|0|ON|OFF]
        set global slow_query_log_file=[file_name]

 3. my.ini中配置

        slow_query_log=1
        slow_query_log_file=/var/log/mysql_slow.log

一般long_query_time的值不宜设置过大，默认值10秒就显得不合适，通常2-5秒是理想值。当然慢查询日志会对MySQL性能有影响。如果是主从结构打开一台专门用来监控慢查询好了。

