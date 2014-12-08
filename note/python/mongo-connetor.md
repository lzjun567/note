mongo-connector原理及改造
======================
这段时间因为项目的某个需求需要改造mongo-connector，改造开源产品首先要读懂别人的代码，于是总结记录一下自己的分析过程。这里假设你对Solr有一定的了解。   
 
mongo-connctor是一款用于同步MongoDB数据到其他系统组件，比如它能同步数据到Solr、ElasticSearch或者其他MongoDB集群中去。它的实现原理是依据MongoDB的Replica Set复制模式，通过分析oplog日志文件达到最终的同步目的。安装配置启动过程可参考[官方文档](https://github.com/10gen-labs/mongo-connector)。这篇文章具体来分析一下mongo-connetor的执行过程是怎样的。
####oplog
首先需要了解oplog的格式，它的格式在不同版本的mongodb上有所区别，大致是：  
    
    PRIMARY> db.version()
    2.2.2
    PRIMARY> db.oplog.rs.findOne()
    {
        "ts" : Timestamp(1364186197000, 58),
        "h" : NumberLong("-7878220425718087654"),
        "v" : 2,
        "op" : "u",
        "ns" : "exaitem_gmsbatchtask.jdgmsbatchtask",
        "o2" : {
            "_id" : "83f09a98-6a41-497b-a988-99ba5399d296"
        },
        "o" : {
            "_id" : "83f09a98-6a41-497b-a988-99ba5399d296",
            "status" : 2,
            "content" : "",
            "type" : 17,
            "business" : "832722",
            "optype" : 2,
            "addDate" : ISODate("2013-03-25T04:36:38.511Z"),
            "modifyDate" : ISODate("2013-03-25T04:36:39.131Z"),
            "source" : 5
        }

* ts 由4个字节的timestamp 和 4字节的自增计数器表示。
* op：
    
        "i"： insert
        "u"： update
        "d"： delete
        "c"： db cmd
        "db"：声明当前数据库 (其中ns 被设置成为=>数据库名称+ '.')
        "n":  no op,即空操作，其会定期执行以确保时效性 。
* ns：操作的namespace
* o：操作对应的document，即当前操作的内容（比如更新操作时要更新的的字段和值，那些没有被更新的字段及对应的值也会在这里面）
* o2：执行更新操作的条件，只有update才有该属性。}

####mongo-connector
mongo-connetor的核心目录结构是：  

    ├── mongo_connector
    │   ├── __init__.py
    │   ├── compat.py
    │   ├── config.txt
    │   ├── connector.py
    │   ├── constants.py
    │   ├── doc_managers
    │   │   ├── __init__.py
    │   │   ├── config.txt
    │   │   ├── doc_manager_simulator.py
    │   │   ├── elastic_doc_manager.py
    │   │   ├── formatters.py
    │   │   ├── mongo_doc_manager.py
    │   │   ├── schema.xml
    │   │   ├── solr_doc_manager.py
    │   │   └── solr_doc_manager.pyc
    │   ├── errors.py
    │   ├── locking_dict.py
    │   ├── oplog_manager.py
    │   └── util.py
    
程序的入口就是connector.py，main方法通过从命令行中接收参数信息，参数信息可以用`mongo-conntor --help`查看，根据参数信息构建connector对象，connetor继承Thread，具体的执行流程如下：  
![mongo-connetor](http://foofish.qiniudn.com/mongo-connetor.001.jpg)

基本的执行流程理解之后，我有这个一个需求，同mongodb同步到solr中的document中的部分field是手动加上去的，比如：用户的粉丝数量在mongodb中没有存储，而是放在redis中，此时有会通过其他方式把粉丝数同步到solr中去，同步之后，就会遇到一个问题，如果mongodb中的那条记录有更新操作，比如：该纪录修改了usename字段，但是他用的是mongodb中的赋值操作，而不是修改器`$set`，此时mongo-conntor会把这条记录的所有字段更新过去，相当于把对应solr中的那个document删除，重新索引，这是粉丝数就没有了。具体的细节可以通过查看solr_doc_manager.py文件来验证。也可以看看我从官方fork的一份代码中查看，这份[代码](https://github.com/lzjun567/mongo-connector)做了些注视。

通过在apply_update方法中添加逻辑：  
    
     #solr中有的字段但mongodb中没有的字段，继续保留在solr中
     for key in doc:
         if key not in update_spec:
             update_spec[key] = doc[key]
就可以解决该问题了。  
