#nginx故障分析
Nginx安装完成后，在公网上访问80端口的网址，结果没有任何响应。那么问题出现在哪里呢，一步步排查问题。

1. 首先确认nginx安装没有问题，查看nginx是否启动成功。  

	ps -ef |grep nginx
看看有没有nginx进程是否有在运行。
	
	root     16817     1  0 17:23 ?        00:00:00 nginx: master process /usr/local/nginx/sbin/nginx
	nobody   17029 16817  0 18:09 ?        00:00:00 nginx: worker process
这一步可以确定nginx服务是启动了的。

2. 查看端口占用情况，看nginx指定的端口是不是配置文件里面指定的80端口。
	
	lsof -i:80

	nginx     16817   root    6u  IPv4 1549186      0t0  TCP *:http (LISTEN)
	nginx     17029 nobody    6u  IPv4 1549186      0t0  TCP *:http (LISTEN)

	或者
	netstat -lanp|grep 80

	tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      16817/nginx: master 

端口确定是nginx占用之后，接着往下查

3. 本地网络是否可以访问该地址

	curl http://localhost
有内容返回：
	
	curl http://localhost
	<!DOCTYPE html>
	<html>
	<head>
	<title>Welcome to nginx!</title>
	.....
这里你可以确认问题出现在网络层，继续排查
4. 看看网络是否可以访问80端口，用telnet
	
	telnet xx.xx.xx.xx 80

	C:\Users\lzjun>telnet 123.57.218.39 80
	正在连接123.57.218.39...无法打开到主机的连接。 在端口 80: 连接失败
网络不通，那么说明网络不通。

来看看是不是防火墙问题。
。。。。。