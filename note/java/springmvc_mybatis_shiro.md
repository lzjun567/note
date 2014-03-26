####安装配置Maven
添加M2_HOME环境变量  
windows平台：   

    M2_HOME ---> C:\Program Files\Apache Software Foundation\apache-maven-3.2.1
    PATH  ---> PATH+%M2_HOME%\bin
Linux平台：

    export M2_HOME=/usr/local/apache-maven/apache-maven-3.2.1
    export M2=$M2_HOME/bin
    export PATH=$M2:$PATH

试运行`mvn  --version`：   

    C:\Users\liuzhijun>mvn --version
    Apache Maven 3.2.1 (ea8b2b07643dbb1b84b6d16e1f08391b666bc1e9; 2014-02-15T01:37:52+08:00)
    Maven home: E:\Java\apache-maven-3.2.1
    Java version: 1.6.0_41, vendor: Sun Microsystems Inc.
    Java home: E:\Java\jdk1.6.0_41\jre
    Default locale: zh_CN, platform encoding: GBK
    OS name: "windows 7", version: "6.2", arch: "amd64", family: "windows"

[安装m2e](http://download.eclipse.org/technology/m2e/releases)  
安装个m2e真是折腾人，直接安装发现eclipse需要访问sourceforge，下载相关东西，你知道的，这网站是需要番羽墙的。因此我在Eclipse上使用代理安装。  

安装失败:  
    Cannot complete the install because one or more required items could not be found.
      Software being installed: m2e - slf4j over logback logging (Optional) 1.4.0.20130601-0317 (org.eclipse.m2e.logback.feature.feature.group 1.4.0.20130601-0317)
        Missing requirement: m2e logback configuration 1.4.0.20130601-0317 (org.eclipse.m2e.logback.configuration 1.4.0.20130601-0317) requires 'bundle org.slf4j.api 1.6.2' but it could not be found
          Cannot satisfy dependency:
              From: m2e - slf4j over logback logging (Optional) 1.4.0.20130601-0317 (org.eclipse.m2e.logback.feature.feature.group 1.4.0.20130601-0317)
                  To: org.eclipse.m2e.logback.configuration [1.4.0.20130601-0317]



需要下载slf4j.jar包，于是[下载](http://www.slf4j.org/download.html)解压把该jar包放入eclipse的plugin目录下，继续上面的安装，等待若干分钟后安装完成。


