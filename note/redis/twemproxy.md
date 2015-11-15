####twemproxy能做什么？
Twemproxy是twitter开发的Redis代理服务，有了Twemproxy，不管服务端部署了多少个Redis实例，对客户端来说就是一个单实例的Redis，开发者通过tweproxy访问Redis的实例时不需要关心去哪台Redis读取key-value数据，也不需要关心key-value写到了哪台Redis。 

Twemproxy可以避免单点故障问题，因为Twemproxy背后使用多台服务器水平扩张Redis实例，Twemproxy可以把数据分片（sharding）到多台服务器上，每台服务器存储整个数据集的一部分，因此，如果某个Reids服务宕机了，那么该部分数据也就丢失了，此时需要借助Reids的master-slave 复制模式（replication）保证数据有备份。  

####安装
本测试使用源码安装方式（OSX环境）：

	#预安装automake、libtool:  
	$ brew install automake
	$ brew install libtool
	
	$ git clone git@github.com:twitter/twemproxy.git
	$ cd twemproxy
	$ autoreconf -fvi
	$ ./configure --enable-debug=full
	$ make
	$ src/nutcracker -h
安装成功后可以执行命令查看twemproxy的使用方式：  
	
	src/nutcracker -h
	
    -h, --help             : this help
    -V, --version          : show version and exit
    -t, --test-conf        : 检查配置文件是否正确
    -d, --daemonize        : run as a daemon
    -D, --describe-stats   : print stats description and exit
    -v, --verbose=N        : set logging level (default: 5, min: 0, max: 11)
    -o, --output=S         : set logging file (default: stderr)
    -c, --conf-file=S      : set configuration file (default: conf/nutcracker.yml)
    -s, --stats-port=N     : set stats monitoring port (default: 22222)
    -a, --stats-addr=S     : set stats monitoring ip (default: 0.0.0.0)
    -i, --stats-interval=N : set stats aggregation interval in msec (default: 30000 msec)
    -p, --pid-file=S       : set pid file (default: off)
    -m, --mbuf-size=N      : set size of mbuf chunk in bytes (default: 16384 bytes)
	
	
	
	
1. 在客户端和多个Redis实例间做代理
2. 多个Redis实例之间进行自动数据分片
3. 支持一致性哈希

支持Linux， BSD，OSX，等:wq

