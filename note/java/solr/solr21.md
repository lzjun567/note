生产环境部署Solr
===============
solr安装包自带有Jetty服务器，如果是运行单实例Solr的话，使用内置的Jetty没有问题，如果需要运行多个实例，就必须下载完整的Jetty包，否则会出现不可预知的错误，[Solr官方文档](http://wiki.apache.org/solr/SolrJetty)有说明。  
>  For non-trivial installations (multi-instances) with Jetty 6, you need to download full Jetty package because it contains additional modules (JettyPlus)  
>Running multiple instances： we recommend you to use Tomcat as servlet container because it is more trivial way to add solr instance even without rebooting tomcat. See SolrTomcat article


我就遇到过这样的问题，系统运行了两个Solr实例，其中有一个实例大概运行一周左右就不接收任何请求了，后台日子也没有任务错误消息。这里介绍的是Tomcat的部署方式。  
部署在Tomcat，Tomcat7在解析URL的末尾的“/”时有bug，但在Tomcat7.0.5+已经被修复。 Tomcat[下载地址](http://tomcat.apache.org/download-70.cgi#7.0.55)  

如果你下载的是官方发行版的话，$SOLR_INSTALL/dist/目录下有一个solr-*.war文件，把名字改成solr.war，此外，$SOLR_INSTALL/example/solr目录的文件也是必须的，都应该部署到servlet 容器中（tomcat、jetty）  

如果Solr索引大小超过服务器的物理内存，那就意味着在查询请求时为了加载文件到内存中磁盘扫描是必须的，这会非常影响查询的速度。有些用户寄希于SSD上，虽然它能加快磁盘的扫描速度，如果你有足够的内存确保整个索引一直处于内存之中而不是在磁盘雨内存中来回的切换，这样才能真正达到最好的搜索性能。

如果是为了提高索引的吞吐量，SSD就能带来很大的好处，因为索引是一个I/O频繁的操作。  

####JVM设置
预先分配好堆空间大小，如果在在需要的时候再去扩展影响性能。  
    
    java -Xms2048m -Xmx2048m -jar start.jar
把堆空间的最大值和最小值设置成相同大小是确保Solr不会因为JVM进程因堆空间不足来扩展空间影响Solr的性能。同时分配更多的内存给Solr的JVM并不是好建议，因为内存大了，gc的时间也会相应的增加，因此，在确保Solr的关键数据(caches, solr cores等其他常驻内存的数据）执行查询操作。




###Jetty部署多个Solr实例
####安装Jetty
jetty，solr放在/root/projects-v1.2，下载Jetty9：  
    
    cd /root/project-v1.2
    wget http://ftp.yz.yamagata-u.ac.jp/pub/eclipse//jetty/stable-9/dist/jetty-distribution-9.2.2.v20140723.zip
解压：  

    unzip jetty-distribution-9.2.2.v20140723.zip
    mv jetty-distribution-9.2.2.v20140723.zip jetty
创建jetty用户：    

    useradd jetty -U -s /bin/false
    chown -R jetty:jetty /root/projects-v1.2/jetty

拷贝Jetty启动脚本作为系统服务：
    
    cp /root/projects-v1.2/jetty/bin/jetty.sh /etc/init.d/sponia-context-search
Jetty启动时需要配置参数，创建相应配置文件：  

    vim /etc/default/sponia-context-search
    #添加如下内容
    NO_START=0
    JETTY_HOME=/root/projects-v1.2/jetty
    JETTY_HOST=0.0.0.0
    JETTY_ARGS="jetty.port=8986 /root/projects-v1.2/jetty/etc/jetty-deploy.xml"
    #JETTY_USER=jetty # Run as this user
    JETTY_LOGS=/root/projects-v1.2/sponia-global-search/log
    JETTY_PID=/var/run/sponia-global-search.pid
    JAVA=/usr/bin/java # Path to Java
    # Extra options to pass to the JVM
    JAVA_OPTIONS="-XX:+UseConcMarkSweepGC -XX:+UseParNewGC"

此时jetty正常启动的话，访问：http://192.168.200.2:8985/    

####安装Solr
下载solr4.9：    

    wget http://ftp.jaist.ac.jp/pub/apache/lucene/solr/4.9.0/solr-4.9.0.zip
    unzip solr-4.9.0.zip
    cp solr-4.9.0/dist/solr-4.9.0.war /root/projects-v1.2/jetty/webapps/solr.war
    cp -R solr-4.9.0/example/solr /root/projects-v1.2/sponia-context-search

拷贝dist和contrib用于数据导入：  

    cp -r solr-4.9.0/dist /root/projects-v1.2/sponia-context-search
    cp -r solr-4.9.0/contrib /root/projects-v1.2/sponia-context-search

指定solr home 目录：
添加下面这行到/etc/default/sponia-context-search  
    
    JAVA_OPTIONS="-Dsolr.solr.home=/root/projects-v1.2/sponia-context-search $JAVA_OPTIONS"

修改配置：/root/projects-v1.2/sponia-context-search/collection1/conf/solrconfig.xml：    
    
    #更新路径
    <lib dir="../../contrib/extraction/lib" regex=".*\.jar" />
    <lib dir="../../dist/" regex="solr-cell-\d.*\.jar" />

    <lib dir="../../contrib/clustering/lib/" regex=".*\.jar" />
    <lib dir="../../dist/" regex="solr-clustering-\d.*\.jar" />

    <lib dir="../../contrib/langid/lib/" regex=".*\.jar" />
    <lib dir="../../dist/" regex="solr-langid-\d.*\.jar" />

    <lib dir="../../contrib/velocity/lib" regex=".*\.jar" />
    <lib dir="../../dist/" regex="solr-velocity-\d.*\.jar" />
    #新增下面两行用户数据导入 
    <lib dir="../../contrib/dataimporthandler/lib" regex=".*\.jar" />
    <lib dir="../../dist/" regex="apache-solr-dataimporthandler-.*\.jar" />

此时solr还没法访问，需要指定solr依赖的log相关的jar文件：   
    cp /root/projects-v1.2/solr-4.9.0/example/lib/ext/* /root/projects-v1.2/jetty/lib/ext/

另还要mysql_jdbc.jar包：  
    
    cp /root/projects/solr/dist/com.mysql.jdbc_5.1.5.jar /root/projects-v1.2/jetty/lib/ext/

重启jetty，访问：http://192.168.200.2:8985/solr/#/





