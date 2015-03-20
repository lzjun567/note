####RDB
Redis在重启时，RDB程序通过载入RDB文件还原数据库状态。  
rdbSave函数负责把数据保存到磁盘中，如果RDB文件已经存在，那么新的RDB文件将替换已有的RDB文件。
