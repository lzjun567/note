MySQL启动报错：InnoDB: Unable to lock ./ibdata1 error
========
在OS X环境下MySQL启动时报错：  
	
	016-03-03T00:02:30.483037Z 0 [ERROR] InnoDB: Unable to lock ./ibdata1 error: 35
	2016-03-03T00:02:30.483100Z 0 [Note] InnoDB: Check that you do not already have another mysqld process using the same InnoDB data or log files.

终端不断地重复打印上面的错误日志，从错误日志看起来似乎有另外一个mysqld进程占用了./ibdata1文件，于是使用ps命令查看是否有mysqld进程在运行：
	
	ps -ef |grep mysqld
   	74  7711     1   0  8:04上午 ??         0:00.34 /usr/local/mysql/bin/mysqld --user=_mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data --plugin-dir=/usr/local/mysql/lib/plugin --log-error=/usr/local/mysql/data/mysqld.local.err --pid-file=/usr/local/mysql/data/mysqld.local.pid

发现有一个7711的进程在运行，于是强制kill掉：  
	
	sudo kill -9 7711
再次ps查询：
	
	ps -ef |grep mysqld
	74  7759     1   0  8:10上午 ??         0:00.29 /usr/local/mysql/bin/mysqld --user=_mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data --plugin-dir=/usr/local/mysql/lib/plugin --log-error=/usr/local/mysql/data/mysqld.local.err --pid-file=/usr/local/mysql/data/mysqld.local.pid

发现还在，只不过pid由原来的7711变成了现在的7759，那么看看mysqld进程打开了哪些文件：
	
	lsof -c mysqld
该进程没有打开任何文件，这就见鬼了。

>Mac OS X, lsof only shows your own processes unless running as root with sudo

于是再次运行：

	sudo lsof -c mysqld
	COMMAND  PID   USER   FD     TYPE             DEVICE  SIZE/OFF    NODE NAME
	mysqld  8655 _mysql  cwd      DIR                1,4       544 3090250 /usr/local/mysql/data
	mysqld  8655 _mysql  txt      REG                1,4  31130736 3089789 /usr/local/mysql/bin/mysqld

的确发现有一个实实在在的mysqld进程在运行，也占用的这些mysql文件，经过一番Google大法，发现在OS X中启动MySQL跟在Linux中启动方式完全是牛马不相及，在OS X中启动/重启MySQL的正确姿势是：

	sudo launchctl unload -w /Library/LaunchDaemons/com.oracle.oss.mysql.mysqld.plist
此时再来看看是否还有mysqld进程：
	
	ps -ef |grep mysqld
嗯，发现确实没有了，再来启动MySQL：
	
	sudo launchctl load -w /Library/LaunchDaemons/com.oracle.oss.mysql.mysqld.plist
问题总算解决，但还没完，总得把原理搞清楚才行。  

####launchd是什么？
launchd是Mac OS X从10.4开始引入，用于用于初始化系统环境的关键进程，它是内核装载成功之后在OS环境下启动的第一个进程。传统的Linux会使用/etc/rc.*或者/etc/init来管理开机要启动的服务，而在OS X中就是使用launchd来管理。采用这种方式来配置启动项很简单，只需要一个plist文件。/Library/LaunchDaemons目录下的plist文件都是系统启动后立即启动进程。使用launchctl命令加载/卸载plist文件，加载配置文件后，程序启动，卸载配置文件后程序关闭。

卸载配置文件后又尝试直接用mysqld命令来启动mysql进程试试：
	
	/usr/local/mysql/bin/mysqld
	2016-03-03T01:35:50.359258Z 0 [ERROR] InnoDB: ./ib_logfile0 can't be opened in read-write mode.
	2016-03-03T01:35:50.359283Z 0 [ERROR] InnoDB: Plugin initialization aborted with error Generic error
	2016-03-03T01:35:50.670517Z 0 [ERROR] Plugin 'InnoDB' init function returned error.
	2016-03-03T01:35:50.670555Z 0 [ERROR] Plugin 'InnoDB' registration as a STORAGE ENGINE failed.
	2016-03-03T01:35:50.670568Z 0 [ERROR] Failed to initialize plugins.
	2016-03-03T01:35:50.670574Z 0 [ERROR] Aborting
ib_logfile0不能被打开，猜测是用户权限文件，不能用当前系统用户启动mysql。那么加上sudo看看，用root来启动：
	
	2016-03-03T01:38:10.977313Z 0 [ERROR] Fatal error: Please read "Security" section of the manual to find out how to run mysqld as root!

	2016-03-03T01:38:10.977339Z 0 [ERROR] Aborting

	2016-03-03T01:38:10.977350Z 0 [Note] Binlog end
	2016-03-03T01:38:10.977410Z 0 [Note] /usr/local/mysql/bin/mysqld: Shutdown complete

叫我去读MySQL的安全手册，还是用launchd的方式启动吧。