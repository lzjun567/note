OS X El-Capitan 安装 virtualenvwrapper 遇到 Operation not permitted
=============================
事情是这样的，在安装完virtualenv后，想配合virtualenvwrapper使用，于是直接是pip安装：  
	
	$ pip install virtualenvwrapper

于是抱了一错误，说是没有权限，那么加上sudo后运行：  
	
	$ sudo pip install virtualenvwrapper

发现还是有问题，仔细一看堆栈信息：  

	
	Collecting six>=1.9.0 (from stevedore->virtualenvwrapper)
	  Downloading http://pypi.douban.com/packages/py2.py3/s/six/six-1.10.0-py2.py3-none-any.whl
	Installing collected packages: six, stevedore, virtualenvwrapper
	  Found existing installation: six 1.4.1
	    DEPRECATION: Uninstalling a distutils installed project (six) has been deprecated and will be removed in a future version. This is due to the fact that uninstalling a distutils project will only partially uninstall the project.
	    Uninstalling six-1.4.1:
	Exception:
	Traceback (most recent call last):
	  
	  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/shutil.py", line 103, in copystat
	    os.chflags(dst, st.st_flags)
	OSError: [Errno 1] Operation not permitted: '/tmp/pip-nGVqhl-uninstall/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/six-1.4.1-py2.7.egg-info'

virtualenvwrapper需要依赖six，在安装six的时候发现系统已经有一个six-1.4.1，但是virtualenvwrapper需要six-1.9.0，于是想先卸载老版本的six，此时问题来了，发现没有权限卸载，此时我就纳闷，加上sudo，还是没权限。于是Google之，最终还是在万能的GitHub找到答案。系统用的是**OS X El-Capitan**版本，six-1.4.1是系统内置的packages，因[系统集成保护](https://en.wikipedia.org/wiki/System_Integrity_Protection)你是没有权限去修改/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/six-1.4.1-py2.7.egg-info目录的。因此在安装virtualenvwrapper的时候需要选择忽略six的安装：    
	
	sudo pip install virtualenvwrapper --upgrade --ignore-installed six

最终问题迎刃而解。

参考：[https://github.com/pypa/pip/issues/3165](https://github.com/pypa/pip/issues/3165)
