django-simple-captcha遇到的坑
=============================
一Django站点[gongshare.com](http://gongshare.com)在做注册验证码时采用[django-simple-captcha](https://django-simple-captcha.readthedocs.org/en/latest/index.html)，因为笔者开发环境采用的Windows 64bit系统，结果安装的时候遇到各种坑。  

django-simple-captcha需要依赖django1.3+、PIL1.1.7+或者Pillow2.0+，根据[文档](https://django-simple-captcha.readthedocs.org/en/latest/usage.html)安装后开始使用时，最开始报如下错：  

    TypeError: function takes at most 4 arguments (6 given)

这个错误在stackoverlfow找到了[答案](http://stackoverflow.com/questions/16365462/when-i-run-django-simple-captcha-test-throw-2-errors)，把PIL替换成Pillow就行，Pillow是从PIL fork过来的一个版本，至于为什么会有Pillow这么个东西，[这里](https://github.com/python-imaging/Pillow)pillow的作者对它做了最好的解释，大概意思就是对PIL的安装及Bug修复太慢。  

窃以为替换了PIL后就没问题了，接着问题来了  

    IOError: encoder zip not available
还是在在stackoverflow找[答案](http://stackoverflow.com/questions/16990852/how-to-correctly-use-pil-with-python-under-windows)，目测还是PIL的问题，我很纳闷，PIL卸载了（使用命令`pip uninstall PIL`)，Pillow重新安装了，为啥还是不行，结果跑到控制面板安装的程序，发现还有个64位的PIL，因为笔者之前安装过一次二进制的PIL.exe，另外发现自己的Python版本也是64位的Python2.7.4，于是乎，手动卸载控制面板中出现的那个PIL，又重新安装了遍Pillow，未果，跑到[这个网站](http://www.lfd.uci.edu/~gohlke/pythonlibs/)下了个安装版的Pillow-2.1.0.win-amd64-py2.7.exe，新的错误出现了：  
    
    The _imaging C module is not installed
此时快要崩溃了，但还是不死心啊，于是把64位的python2.7.4也卸载掉，换成了32位的python2.7.5，此时此刻激动人心的一刻出现了。自己去感受一下吧。  

总结：  
+ 在进允许的情况下，尽可能在类Linux上做开发，这样遇到的坑比较少。  
+ 把Python换成32位的安装包，其他第三方的也跟着用32位  










