[Django](http://djangoproject.org)是Python语言中最受欢迎的全栈式Web框架之一，过去部署Django应用一般采用Apache+mod_wsgi，但是由于有了Nginx出色的性能表现，Django也有了更先进的部署方式，比较常用的一种部署方案是Nginx+Gunicorn。 接下来我会详细完整地介绍一个符合生产条件标准的部署过程。  
####前提条件
假设你对Linux有基本的了解，而且拥有一台root权限的主机。我使用的服务器是Ubuntu12.04。你也可以选择其他Linux发行版(如:CentOS、Fedora)，如果你手头没有服务器，那么我推荐使用非常便宜的VPS服务器[DigitalOcean](https://www.digitalocean.com/?refcode=af4cff8f42bc)，最低$0.05/小时的费用，使用我的[Refer](https://www.digitalocean.com/?refcode=af4cff8f42bc)注册，即可获得$10免费使用低配服务器两个月。
####更新系统

    $ sudo apt-get update
    $ sudo apt-get upgrade
    $ sudo apt-get install python-dev
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
####安装Virtualenv
[Virtualenv](http://foofish.net/blog/88/virtualenv)可以在系统中创建一个独立的Python环境，多个应用之间彼此不受影响，这样不同的应用使用的依赖库就不会相互冲突(比如一个应用是基于Django1.5，另一个应用可以用Django1.6)。  
    
    $ pip install virtualenv
我们把应用虚拟环境创建在/webapps目录下面,  

    $ cd /webapps/
    $ virtualenv hello_django

    New python executable in hello_django/bin/python
    Installing Setuptools....................................done.
    Installing Pip...........................................done.

    $ cd hello_django
    $ source bin/activate    # 激活
    (hello_django) $         # 注意`$`符号前的hello_django表明你已经在这个新的python虚拟环境中
    (hello_django) $ pip install django  # 安装django
    (hello_django) $ django-admin.py startproject hello # 创建一个空的django项目hello  

用开发模式测试一下项目是否可以正常运行

    (hello_django) $ cd hello
    (hello_django) $ python manage.py runserver localhost:80

    Validating models...
    
    0 errors found
    January 17, 2014 - 10:34:13
    Django version 1.6.1, using settings 'hello.settings'
    Starting development server at http://localhost:80/
    Quit the server with CONTROL-C.
此时你应该可以正常访问:http://localhost了。

####更新settings文件

Django 使用MySQL作为后端存储需要使用`MySQL-python`数据库适配器，但是它需要依赖本地扩展库`python-dev`，`libmysqlclient-dev`，所以先安装依赖库  

    $ sudo apt-get install python-dev libmysqlclient-dev
安装 `MySQL-python`  

    (hello_django) $pip install mysql-python
在settings.py中配置数据库信息  

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'test_db',
            'USER': 'test_user',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '',                      # Set to empty string for default.
        }
    }
django初始化数据库，默认Django会创建一些数据表  
    
    (hello_dango) $ python manage.py syncdb

####为应用创建系统用户
虽然Django有完善的安全追踪记录，但是如果应用对服务器资源的访问限制在自己的范围内，可以避免无谓的入侵危害，因此我们的web应用应该使用有限制权限的用户来运行这个web应用。  

为应用创建一个用户，名字叫做`hello`，附给系统组叫`webapps`。  

    $ sudo groupadd --system webapps
    $ sudo useradd --system --gid webapps --home /webapps/hello_django hello 
####安装Gunicorn
在生产环境下我们就不应该使用Django自带的单线程的开发服务器，[Gunicorn](http://gunicorn.org)就是很好的选择。  

    (hello_django) $ pip install gunicorn

安装成功后，现在你可以通过一下命令测试下你的django应用能否运行在gunicorn上面。  

    (hello_django) $ gunicorn hello.wsgi:application --bind 0.0.0.0:8001
现在你应该可以从http://localhost:8001 访问Gunicorn服务器。Gunicorn安装好后，接下来再写一个bash脚本做一些配置使之用起来更方便。 文件保存为`bin/gunicorn_start.sh`

    #!/bin/bash
    NAME='hello_app'                                   #应用的名称
    DJANGODIR=/webapps/hello_django/hello              #django项目的目录
    SOCKFILE=/webapps/hello_django/run/gunicorn.sock   #使用这个sock来通信
    USER=hello                                         #运行此应用的用户
    GROUP=webapps                                      #运行此应用的组
    NUM_WORKERS=3                                      #gunicorn使用的工作进程数
    DJANGO_SETTINGS_MODULE=hello.settings              #django的配置文件
    DJANGO_WSGI_MODULE=hello.wsgi                      #wsgi模块
    
    echo "starting $NAME as `whoami`"
    
    #激活python虚拟运行环境
    cd $DJANGODIR
    source ../bin/activate
    export  DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
    export PYTHONPATH=$DJANGODIR:$PYTHONPATH
    
    #如果gunicorn.sock所在目录不存在则创建
    RUNDIR=$(dirname $SOCKFILE)
    test -d $RUNDIR || mkdir -p $RUNDIR
    
    #启动Django
    
    exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
        --name $NAME \
        --workers $NUM_WORKERS \
        --user=$USER --GROUP=$GROUP \
        --log-level=debug \
        --bind=unix:$SOCKFILE

用户`hello`将运新这个应用，那么要把这个应用的目录的权限交给`hello`  

    $ sudo chown -R hello:users /webapps/hello_django
    $ sudo chmod -R g+w /webapps/hello_django
    $ sudo chmod u+x bin/gunicorn_start.sh
如果你还不是组`users`的成员，使用下面命令：  

    $ sudo usermod -a -G users `whoami`

现在就可以切换到用户`hello`来执行这段脚本：  

    $sudo su - hello
    $bin/gunicorn_start.sh

    Starting hello_app as hello
    2014-01-17 15:59:25 [10724] [INFO] Starting gunicorn 18.0
    2014-01-17 15:59:25 [10724] [DEBUG] Arbiter booted
    2014-01-17 15:59:25 [10724] [INFO] Listening at: unix:/webapps/hello_django/run/gunicorn.sock (10724)
    2014-01-17 15:59:25 [10724] [INFO] Using worker: sync
    2014-01-17 15:59:25 [10735] [INFO] Booting worker with pid: 10735
    2014-01-17 15:59:25 [10736] [INFO] Booting worker with pid: 10736
    2014-01-17 15:59:25 [10737] [INFO] Booting worker with pid: 10737
    
* --workers 设置的个数规则是：2*CPUs+1。因此单核CPU机器的进程数设置为3个。  
* --name 默认是`gunicorn`，置顶后，可以通过`top`或`ps`查看到，唯一标识其进程。  

####使用Supervisor启动、监控应用
脚本现在准备就绪，我们需要确保系统能够自动启动或者重启，因为系统可能会由于某些原因导致异常终止，这个任务就交给supervisor，它的安装也非常简单：  

    $ sudo apt-get insatll supervisor
安装后，在`/etc/supervisor/conf.d/`目录下创建配置文件`/etc/supervisor/conf.d/hello.conf`，用来启动、监视应用程序。  

    [program:hello]
    command = /webapps/hello_django/bin/gunicorn_start.sh                 ; Command to start app
    user = hello                                                          ; User to run as
    stdout_logfile = /webapps/hello_django/logs/gunicorn_supervisor.log   ; Where to write log messages
    redirect_stderr = true  

创建文件存储日志：  

    $ mkdir -p /webapps/hello/logs
    $ touch /webapps/hello_django/logs/gunicorn_supervisor.log

配置好了之后，supervisor重新加载配置文件  

    $ sudo supervisorctl reread
    hello: available
    $ sudo supervisorctl update
    hello: added process group
同时你还可以检查app的状态、启动、停止、重启  

    $ sudo aupervisorctl status hello
    hello                RUNNING
    $ sudo supervisorctl stop hello 
    hello: stopped
    $ sudo supervisorctl start hello 
    hello: started
    $sudo supervisorctl restart hello 
    hello:stoped
    hello:started
现在应用可以在系统重启或者某些原因崩溃后自动重启了。  

####配置Nginx  
Nginx作为反向代理程序

    $ sudo apt-get install nginx
    $ sudo /etc/init.d/nginx start
每个Nginx虚拟服务器应该是通过一个在`/etc/nginx/sites-available`目录下的文件描述的，为了使之生效需要在`/etc/nginx/sites-enbled`做一个符号连接。创建配置文件`/etc/nginx/sites-available/hello`，内容如下：  

    upstream hello_app_server {
      server unix:/webapps/hello_django/run/gunicorn.sock fail_timeout=0;
    }
     
    server {
     
        listen   80;
        server_name localhost;
     
        client_max_body_size 4G;
     
        access_log /webapps/hello_django/logs/nginx-access.log;
        error_log /webapps/hello_django/logs/nginx-error.log;
     
        location /static/ {
            alias   /webapps/hello_django/static/;
        }
        
        location /media/ {
            alias   /webapps/hello_django/media/;
        }
     
        location / {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     
            proxy_set_header Host $http_host;
     
            proxy_redirect off;
     
            if (!-f $request_filename) {
                proxy_pass http://hello_app_server;
                break;
            }
        }
     
        # Error pages
        error_page 500 502 503 504 /500.html;
        location = /500.html {
            root /webapps/hello_django/static/;
        }
    }
创建符号链接：  

    $ sudo ln -s /etc/nginx/sites-available/hello /etc/nginx/sites-enabled/hello
重启Nginx：  

    $ sudo /etc/init.d/nginx restart

所有配置基本完成了，现在你就可以看到django的欢迎界面了。  

####卸载Django应用
如果你需要卸载这个项目，那么可以按照如下步骤彻底清除  

移除虚拟服务器从Nginx的`sites-enabled`目录：  

    $ sudo rm /etc/nginx/sites-enabled/hello_django
重启Nginx：  
    
    $ sudo /etc/init.d/nginx restart
如果以后都不打算使用这个项目了，那么可以从`site-available`目录删除配置文件  
    
    $ sudo rm /etc/nginx/sites-available/hello_django

用Supervisor停掉应用：  
    
    $ sudo supervisorctl stop hello 

从supervisor的控制脚本目录中移除配置：  

    $ sudo rm /etc/supervisor/conf.d/hello.conf

最后可以把整个应用的目录删除：  
    
    $ sudo rm -r  /webapps/hello_django

####总结
如果你是一步一步根据这个教程来操作的话，那么整个目录结构应该是如下：  

    /webapps/hello_django/
    ├── bin                          <= virtualenv创建的目录
    │   ├── activate                 <= Environment activation script
    │   ├── django-admin.py
    │   ├── gunicorn
    │   ├── gunicorn_django
    │   ├── gunicorn_start.sh           <= 用Gunicorn启动应用的脚本
    │   └── python
    ├── hello                        <= 项目的根目录,把他添加到 PYTHONPATH
    │   ├── manage.py
    │   ├── project_application_1
    │   ├── project_application_2
    │   └── hello                    <= 项目的配置目录
    │       ├── __init__.py
    │       ├── settings.py          <= hello.settings - settings模块， Gunicorn需要使用
    │       ├── urls.py
    │       └── wsgi.py              <= hello.wsgi - WSGI module，Gunicorn使用
    ├── include
    │   └── python2.7 -> /usr/include/python2.7
    ├── lib
    │   └── python2.7
    ├── lib64 -> /webapps/hello_django/lib
    ├── logs                         <= 项目的日子目录
    │   ├── gunicorn_supervisor.log
    │   ├── nginx-access.log
    │   └── nginx-error.log
    ├── media                        <= 用户文件上传目录
    ├── run
    │   └── gunicorn.sock 
    └── static                       <= 项目的静态资源目录

所有步骤经过自己操作验证通过，如果你在配置过程中有任何疑问，毫不犹豫给我留言。

