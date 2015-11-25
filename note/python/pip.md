修改pip安装源
============
用pip安装依赖包时默认访问`https://pypi.python.org/simple/`，但是经常出现不稳定以及访问速度非常慢的情况，国内厂商提供的pipy镜像目前可用的有：        

* http://pypi.douban.com/ 豆瓣 
* http://pypi.mirrors.ustc.edu.cn/simple/ 中国科学技术大学 

有两种方式使用我们自己指定的镜像源，第一种是手动指定：

	pip -i http://pypi.douban.com/simple install Flask -- trusted-host pypi.douban.com

不过这种方式在每次安装时都要手动指定，因此你可以把它写在配置文件中，这就是第二种方法，在当前用户目录下创建.pip文件夹

	mkdir ~/.pip

然后在该目录下创建pip.conf文件填写：

	[global]
	trusted-host =  pypi.douban.com
	index-url = http://pypi.douban.com/simple

上面配置是针对OSX／Linux系统，如果是Windows，那么创建%HOMEPATH%\pip\pip.ini文件来配置。
