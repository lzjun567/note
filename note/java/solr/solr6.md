Solr(6)整合MySQL、Mongodb
=======
MySQL
----------------------
1. 拷贝mysql-connector-java-5.1.25-bin.jar到E:\solr-4.8.0\example\solr-webapp\webapp\WEB-INF\lib目录下面
2. 配置E:\solr-4.8.0\example\solr\collection1\conf\solrconfig.xml  

        <requestHandler name="/dataimport" 
             class="org.apache.solr.handler.dataimport.DataImportHandler"> 
               <lst name="defaults"> 
                  <str name="config">data-config.xml</str> 
               </lst> 
        </requestHandler> 
3. 导入依赖库文件：  

          <lib dir="../../../dist/" regex="solr-dataimporthandler-\d.*\.jar"/>
    加在 

          <lib dir="../../../dist/" regex="solr-cell-\d.*\.jar" />
    前面。

4. 创建E:\solr-4.8.0\example\solr\collection1\conf\data-config.xml，指定MySQL数据库地址，用户名、密码以及建立索引的数据表 
        
        <?xml version="1.0" encoding="UTF-8" ?>
            <dataConfig>  
                    <dataSource type="JdbcDataSource" 
                                driver="com.mysql.jdbc.Driver" 
                                url="jdbc:mysql://localhost:3306/django_blog" 
                                user="root" 
                                password=""/>  
                        <document name="blog">  
                                <entity name="blog_blog" pk="id" 
                                        query="select id,title,content from blog_blog"
                                        deltaImportQuery="select id,title,content from blog_blog where ID='${dataimporter.delta.id}'"  
                                        deltaQuery="select id  from blog_blog where add_time > '${dataimporter.last_index_time}'"  
                                        deletedPkQuery="select id  from blog_blog where id=0">  
                                     <field column="id" name="id" />  
                                     <field column="title" name="title" />  
                                     <field column="content" name="content"/>  
                                </entity>  
                       </document> 
            </dataConfig>


   * query 用于初次导入到索引的sql语句。
   * deltaImportQuery 根据ID取得需要进入的索引的单条数据。
   * deltaQuery 用于增量索引的sql语句，用于取得需要增量索引的ID。
   * deletedPkQuery 用于取出需要从索引中删除文档的的ID

5. 为数据库表字段建立域（field），编辑E:\solr-4.8.0\example\solr\collection1\conf\schema.xml:  
    
        <!-- mysql -->
           <field name="id" type="string" indexed="true" stored="true" required="true" /> 
           <field name="title" type="text_cn" indexed="true" stored="true" termVectors="true" termPositions="true" termOffsets="true"/> 
           <field name="content" type="text_cn" indexed="true" stored="true" termVectors="true" termPositions="true" termOffsets="true"/> 
        <!-- mysql -->

6. 配置增量索引更新文件

参考：[http://josh-persistence.iteye.com/blog/2017155](http://josh-persistence.iteye.com/blog/2017155)  
Mongodb
=======
1. 安装[mongo-connector](https://github.com/10gen-labs/mongo-connector/wiki)，最好使用手动安装方式：  

        git clone https://github.com/10gen-labs/mongo-connector.git
        cd mongo-connector
        #安装前修改mongo_connector/constants.py的变量：设置DEFAULT_COMMIT_INTERVAL = 0
        python setup.py install
    默认是不会自动提交了，这里设置成自动提交，否则mongodb数据库更新，索引这边没法同时更新，或者在命令行中可以指定是否自动提交，不过我现在还没发现。

2. 配置schema.xml，把mongodb中需要加上索引的字段配置到schema.xml文件中：  

        <?xml version="1.0" encoding="UTF-8" ?>
        <schema name="example" version="1.5">
            <field name="_version_" type="long" indexed="true" stored="true"/>
            <field name="_id" type="string" indexed="true" stored="true" required="true" multiValued="false" /> 
            <field name="body" type="string" indexed="true" stored="true"/>
            <field name="title" type="string" indexed="true" stored="true" multiValued="true"/>
            <field name="text" type="text_general" indexed="true" stored="false" multiValued="true"/>   
            <uniqueKey>_id</uniqueKey>
            <defaultSearchField>title</defaultSearchField>
            <solrQueryParser defaultOperator="OR"/> 
            <fieldType name="string" class="solr.StrField" sortMissingLast="true" />
            <fieldType name="long" class="solr.TrieLongField" precisionStep="0" positionIncrementGap="0"/>
            <fieldType name="text_general" class="solr.TextField" positionIncrementGap="100">
              <analyzer type="index">
                <tokenizer class="solr.StandardTokenizerFactory"/>
                <filter class="solr.StopFilterFactory" ignoreCase="true" words="stopwords.txt" />
                <filter class="solr.LowerCaseFilterFactory"/>
              </analyzer>
              <analyzer type="query">
                <tokenizer class="solr.StandardTokenizerFactory"/>
                <filter class="solr.StopFilterFactory" ignoreCase="true" words="stopwords.txt" />
                <filter class="solr.SynonymFilterFactory" synonyms="synonyms.txt" ignoreCase="true" expand="true"/>
                <filter class="solr.LowerCaseFilterFactory"/>
              </analyzer>
            </fieldType>
        </schema>

3. 启动Mongod：  

        mongod --replSet myDevReplSet --smallfiles  
    初始化:rs.initiate()

4. 启动mongo-connector:
    
        E:\Users\liuzhijun\workspace\mongo-connector\mongo_connector\doc_managers>mongo-connector -m localhost:27017 -t http://localhost:8983/solr/collection2 -n s_soccer.person -u id -d ./solr_doc_manager.py
    * -m：mongod服务
    * -t：solr服务
    * -n：mongodb命名空间，监听database.collection，多个命名空间逗号分隔
    * -u：uniquekey
    * -d：处理文档的manager文件

    **注意**：mongodb通常使用`_id`作为uniquekey，而Solrmore使用`id`作为uniquekey，如果不做处理，索引文件时将会失败，有两种方式来处理这个问题：  
    1. 指定参数`--unique-key=id`到mongo-connector，Mongo Connector 就可以翻译把`_id`转换到`id`。
    2. 把schema.xml文件中的:
            
            <uniqueKey>id<uniqueKey>
        替换成
            
            <uniqueKey>_id</uniqueKey>
        同时还要定义一个`_id`的字段：
            
            <field name="_id" type="string" indexed="true" stored="true" />
    3. 启动时如果报错：  
            
            2014-06-18 12:30:36,648 - ERROR - OplogThread: Last entry no longer in oplog cannot recover! Collection(Database(MongoClient('localhost', 27017), u'local'), u'oplog.rs')
        清空E:\Users\liuzhijun\workspace\mongo-connector\mongo_connector\doc_managers\config.txt中的内容，需要删除索引目录下的文件重新启动

5. 测试
mongodb中的数据变化都会同步到solr中去。



