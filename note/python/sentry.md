pip install -U virtualenv.

virtualenv ~/www/sentry/

source ~/www/sentry/bin/activate

pip install -U sentry

pip install -U sentry
Collecting sentry
  Downloading sentry-7.1.1.tar.gz (8.0MB)
      39% |############                    | 3.2MB 38kB/s eta 0:02:04
        Hash of the package https://pypi.python.org/packages/source/s/sentry/sentry-7.1.1.tar.gz#md5=998988cf3238bb1a9d0de1ef08cc107c (from https://pypi.python.org/simple/sentry/) (ba25618461a880bcd9b882237681cdf6) doesn’t match the expected hash 998988cf3238bb1a9d0de1ef08cc107c!
          Bad md5 hash for package https://pypi.python.org/packages/source/s/sentry/sentry-7.1.1.tar.gz#md5=998988cf3238bb1a9d0de1ef08cc107c (from https://pypi.python.org/simple/sentry/)

解决方法：
wget https://pypi.python.org/packages/source/s/sentry/sentry-7.1.1.tar.gz
pip install sentry-7.1.1.tar.gz

pip install -U sentry[mysql]
这个也不行，直接pip install -U MySQL-python替代上面这行命令

初始化
sentry init

修改配置文件
vim ~/.sentry/sentry.conf.py  主要是mysql的配置

初始化数据库
sentry upgrade
创建用户
sentry createuser

mysql，redis服务开启后，sentry可以使用了
sentry start
启动celery
新开一个窗口启动
sentry  celery worker -B


文档：http://raven.readthedocs.org/en/latest/integrations/tornado.html
      http://sentry.readthedocs.org/en/latest/quickstart/


