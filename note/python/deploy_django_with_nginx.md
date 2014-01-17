Django应用部署(nginx,gunicorn,virtualenv,supervisor)
====================================================
Django在python语言中最受欢迎的全栈式web框架,过去部署Django应用一般采用Apache+mod_wsgi,但是随着Nginx出色的性能表现,Django也有了更先进的部署方式,比较常用的一种部署方案是Nginx+Gunicorn. 接下来我会详细讲解一个完整的符合生产条件的部署过程及所用的组件.它们有一个特点是:全部属于开源实现.  
####前提条件
我假设你对Linux有基本的了解,而且拥有一台root权限的主机.我使用的服务器是Ubuntu12.04.你也可以选择其他Linux发行版(如:CentOS,Fedora),相应的安装包管理方式是`apt-get`和`yum`.如果你手头没有服务器,那么我推荐你使用非常便宜的由[DigitalOcean](https://www.digitalocean.com/?refcode=af4cff8f42bc)VPS服务器.最低$0.05/小时的费用  
####系统更新

    $ sudo apt-get update
    $ sudo apt-get upgrade
####安装MySQL

    $ sudo apt-get install mysql-server
安装过程中会提示输入数据库密码,安装成功后创建一个MySQL新用户,并赋予权限  

    #以管理员身份登录
    mysql -uroot -p         

    #选择mysql
    use mysql               

    #创建用户名和设定密码
    create user 'test_user'@'localhost' identified by 'password' 

    #创建数据库
    create database test_db 

    #授予test_user操作test_db的所有权限
    grant all privileges on test_db.* to test_user@localhost identified by 'password'

    #使所有操作生效
    flush privileges
####安装virtualenv,为app创建一个独立的python环境
[Virtualenv](http://virtualenv.org)可以在系统中创建一个独立的python环境,多个应用彼此不受影响,这样不同的应用使用的依赖库就不会相互冲突(比如一个应用是基于Django1.5,另一个应用可以用virtualenv创建新的python环境来使用Django1.6).当然它的安装也很简单  
    
    sudo apt-get install python-virtualenv
#####为app创建并且激活一个python环境
我们把应用创建在/var/www目录下面,  

    $ cd /var/www/
    $ virtualenv hello_django

    New python executable in hello_django/bin/python
    Installing Setuptools....................................done.
    Installing Pip...........................................done.

    $ cd hello_django
    $ source bin/activate
    (hello_django) $                #注意`$`符号前的hello_django, 此时表明你已经在这个新的python执行环境中

现在python环境激活了,你就可以在这个环境中安装django等其他库  

    (hello_django) $ pip install django

    Downloading/unpacking django
      Downloading Django-1.6.1.tar.gz (6.6MB): 6.6MB downloaded
      Running setup.py egg_info for package django
        
        warning: no previously-included files matching '__pycache__' found under directory '*'
        warning: no previously-included files matching '*.py[co]' found under directory '*'
    Installing collected packages: django
      Running setup.py install for django
        changing mode of build/scripts-2.7/django-admin.py from 644 to 755
        
        warning: no previously-included files matching '__pycache__' found under directory '*'
        warning: no previously-included files matching '*.py[co]' found under directory '*'
        changing mode of /usr/local/bin/django-admin.py to 755
    Successfully installed django
    Cleaning up...
    
接下来就创建一个空的django项目  
    
    (hello_django) $ django-admin.py startproject hello

用开发模式测试一下项目是否可以正常运行

    (hello_django) $ cd hello
    (hello_django) $ python manage.py runserver localhost:80

    Validating models...
    
    0 errors found
    January 17, 2014 - 10:34:13
    Django version 1.6.1, using settings 'hello.settings'
    Starting development server at http://localhost:80/
    Quit the server with CONTROL-C.
此时你应该可以正常访问:http://localhost了.     
####配置MySQL配合Django工作
