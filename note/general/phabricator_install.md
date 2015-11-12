ubuntu 搭建 pharicator
======================
#### 安装Nginx, MySQL, PHP (LEMP) 

    sudo apt-get update
    sudo apt-get install mysql-server php5-mysql
    sudo apt-get install nginx
    sudo apt-get install php5-fpm
配置php  
    
    sudo vim /etc/php5/fpm/php.ini
找到cgi.fix_pathinfo=1所在的行，把1改为0
    
    cgi.fix_pathinfo=0
修改配置www.conf:   
    
    sudo vim /etc/php5/fpm/pool.d/www.conf
找到listen = 127.0.0.1:9000，替换成/var/run/php5-fpm.sock  
    
    listen = /var/run/php5-fpm.sock
重启php-fpm：
    
    sudo service php5-fpm restart

添加Phabricator 虚拟主机：  
    
    sudo vim /etc/nginx/sites-available/phabricator
配置文件内容：  
    
    server {
        listen 80 default_server;
        listen [::]:80 default_server ipv6only=on;
        
        root /home/ubuntu/phabricator/webroot;
        index index.html index.htm;
        
        server_name phabricator.example.com;  # 配置你自己的域名
        
        location / {
            index index.php;
            rewrite ^/(.*)$ /index.php?__path__=/$1 last;
        }
            
        error_page 404 /404.html;
        
        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
              root /usr/share/nginx/www;
        }

        location = /favicon.ico {
        try_files $uri =204;
        }
    
        location /index.php {
            try_files $uri =404;
            fastcgi_pass unix:/var/run/php5-fpm.sock;
            fastcgi_index index.php;
            include fastcgi_params;
         }
    }
        
需要注意的点：  
* 如果没有配置rewrite，则会显示错误：     
    
        Request parameter '__path__' is not set. Your rewrite rules are not configured correctly.

* 
        git clone git://github.com/facebook/libphutil.git
如果没有安装 libphutil.git会报错：  

    Unable to load libphutil. Put libphutil/ next to phabricator/, or update your PHP 'include_path' to include the parent directory of libphutil/.
 如果没有安装 arcanist
    
    git clone git://github.com/facebook/arcanist.git
报错 
    
    [Core Exception/PhutilBootloaderException] Include of 'arcanist/src/__phutil_library_init__.php' failed!

设置数据库：      
    
    ./bin/config set mysql.host localhost
    ./bin/config set mysql.user root
    ./bin/config set mysql.pass 123456
最后运行：       
    
    ./bin/storage upgrade
此时首页可以显示出来了。    
    
####Mail设置
1. 安装sendmail
    
        sudo apt-get install sendmail
2. mailer-adpter 修改成 PhabricatorMailImplementationPHPMailerLiteAdapter

3. 修改PHPMailer
    
    ./bin/config set phpmailer.smtp-host smtp.qq.com
    ./bin/config set phpmailer.smtp-port 465
    ./bin/config set phpmailer.smtp-protocol SSL
    ./bin/config set phpmailer.smtp-user xxxx@qq.com
    ./bin/config set phpmailer.smtp-password xxxx
    ./bin/phd restart
    
    
    
    
    
    