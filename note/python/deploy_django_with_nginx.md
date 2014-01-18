Django应用部署(nginx,gunicorn,virtualenv,supervisor)
====================================================
[Django](http://djangoproject.org)在python语言中是最受欢迎的全栈式web框架，过去部署Django应用一般采用Apache+mod_wsgi，但是随着Nginx出色的性能表现，Django也有了更先进的部署方式，比较常用的一种部署方案是Nginx+Gunicorn。 接下来我会详细介绍一个完整的符合生产条件的部署过程及组件，这些组件全部属于开源实现。  
####前提条件
我假设你对Linux有基本的了解,而且拥有一台root权限的主机.我使用的服务器是Ubuntu12.04.你也可以选择其他Linux发行版(如:CentOS、Fedora)，相应的安装包管理方式分是`apt-get`和`yum`.如果你手头没有服务器,那么我推荐使用非常便宜的VPS服务器[DigitalOcean](https://www.digitalocean.com/?refcode=af4cff8f42bc)。最低$0.05/小时的费用。  
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
我们把应用创建在/webapps目录下面,  

    $ cd /webapps/
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
虽然DJango有完善的安全追踪记录，但是如果应用对服务器资源的访问限制在自己的范围内，可以避免无谓的入侵危害，因此我们的web应用应该使用有限制权限的用户来运行这个web应用。  

为应用创建一个用户，名字叫做`hello`，附给系统组叫`webapps`。  

    $ sudo groupadd --system webapps
    $ sudo useradd --system --gid webapps --home /webapps/hello_django hello 
####Gunicorn
在生产环境下我们就不应该使用Django自带的单线程的开发服务器，[Gunicorn](http://gunicorn.org)就是很好的选择。  

    (hello_django) $ pip install gunicorn

    Downloading/unpacking gunicorn
      Downloading gunicorn-0.17.4.tar.gz (372Kb): 372Kb downloaded
      Running setup.py egg_info for package gunicorn
    
    Installing collected packages: gunicorn
      Running setup.py install for gunicorn
    
        Installing gunicorn_paster script to /webapps/hello_django/bin
        Installing gunicorn script to /webapps/hello_django/bin
        Installing gunicorn_django script to /webapps/hello_django/bin
    Successfully installed gunicorn
    Cleaning up...
安装成功后，现在你可以通过一下命令测试下你的django应用能否运行在gunicorn上面。  

    (hello_django) $ gunicron hello.wsgi:application --bind 0.0.0.0:8001
现在你应该可以访问Gunicron服务器从http://localhost:8001 , Gunicron安装好后，接下来再写一个bash脚本做一些配置使之用起来更方便。 文件保存为`bin/gunicorn_start.sh`

    #!/bin/bash
    NAME='hello_app'                                   #应用的名称
    DJANGODIR=/webapps/hello_django/hello              #django项目的目录
    SOCKFILE=/webapps/hello_django/run/gunicorn.sock   #使用这个sock来通信
    USER=hello                                         #运行此应用的用户
    GROUP=webapps                                      #运行此应用的组
    NUM_WORKERS=3                                      #gunicron使用的工作进程数
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
    
    ^C (CONTROL-C to kill Gunicorn)
    
    2014-01-17 15:59:28 [10736] [INFO] Worker exiting (pid: 10736)
    2014-01-17 15:59:28 [10735] [INFO] Worker exiting (pid: 10735)
    2014-01-17 15:59:28 [10724] [INFO] Handling signal: int
    2014-01-17 15:59:28 [10737] [INFO] Worker exiting (pid: 10737)
    2014-01-17 15:59:28 [10724] [INFO] Shutting down: Master
    $ exit

--workers 设置的个数规则是：2*CPUs+1。因此单核CPU机器的进程数设置为3个。  
--name 默认是`gunicorn`，置顶后，可以通过`top`或`ps`查看到，唯一标识其进程。  
####s使用Supervisor启动、监控
`gunicorn_start`脚本现在准备就绪，我们需要确保系统能够自动启动或者重启，因为系统可能会由于某些原因导致异常终止，这个任务就交给supervisor，它的安装也非常简单：  

    $ sudo apt-get insatll supervisor
安装后，在`/etc/supervisor/conf.d/`目录下创建配置文件`/etc/supervisor/conf.d/hello.conf`，用来启动监视应用程序。  

    [program:hello]
    command = /webapps/hello_django/bin/gunicorn_start.sh                 ; Command to start app
    user = hello                                                          ; User to run as
    stdout_logfile = /webapps/hello_django/logs/gunicorn_supervisor.log   ; Where to write log messages
    redirect_stderr = true  

创建文件存储日子：  

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

####Nginx
配置Nginx  

    $ sudo apt-get install nginx
    $ sudo /etc/init.d/nginx start
#####创建一个Nginx虚拟服务器服务于Django
每个Nginx虚拟服务器应该是通过一个在`/etc/nginx/sites-available`目录下的文件描述的，为了使之生效需要在`/etc/nginx/sites-enbled`做一个符号连接  
创建配置文件`/etc/nginx/sites-available/hello`，内容如下：  

    upstream hello_app_server {
      # fail_timeout=0 means we always retry an upstream even if it failed
      # to return a good HTTP response (in case the Unicorn master nukes a
      # single worker for timing out).
     
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
            # an HTTP header important enough to have its own Wikipedia entry:
            #   http://en.wikipedia.org/wiki/X-Forwarded-For
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     
            # enable this if and only if you use HTTPS, this helps Rack
            # set the proper protocol for doing redirects:
            # proxy_set_header X-Forwarded-Proto https;
     
            # pass the Host: header from the client right along so redirects
            # can be set properly within the Rack application
            proxy_set_header Host $http_host;
     
            # we don't want nginx trying to do something clever with
            # redirects, we set the Host: header above already.
            proxy_redirect off;
     
            # set "proxy_buffering off" *only* for Rainbows! when doing
            # Comet/long-poll stuff.  It's also safe to set if you're
            # using only serving fast clients with Unicorn + nginx.
            # Otherwise you _want_ nginx to buffer responses to slow
            # clients, really.
            # proxy_buffering off;
     
            # Try to serve static files from nginx, no point in making an
            # *application* server like Unicorn/Rainbows! serve static files.
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







