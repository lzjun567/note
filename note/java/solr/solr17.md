http://jacoxu.com/?p=509

 PERFORMANCE NOTE: this schema includes many optional features and should not
 be used for benchmarking.  To improve performance one could
  - set stored="false" for all fields possible (esp large fields) when you
    only need to search on the field but don't need to return the original
    value.
  - set indexed="false" if you don't need to search on the field, but only
    return the field as a result of searching on other indexed fields.
  - remove all unneeded copyField statements
  - for best index size and searching performance, set "index" to false
    for all general text fields, use copyField to copy them to the
    catchall "text" field, and use that for searching.
  - For maximum indexing performance, use the StreamingUpdateSolrServer
    java client.
  - Remember to run the JVM in server mode, and use a higher logging level
    that avoids logging every request
-->

* Master专做索引（Indexing），Slave用于查询（querying）根据不同的应用场景使用多个slave。
* schema的字段定义： 
    * 当你搜索的字段不需要返回原始的值得时候，该字段尽量设置stored="false"（特别是对于大字段）。  
    * 对于不需要索引而仅仅是需要搜索的结果的字段设置indexed="false"。
* 根据需要使用copyField
* 根据需要使用dynamicField
* 使用"server"模式启动Solr，在64位系统中会默认选择java HotSpot Server VM
* 把日志级别尽可能调高，在example/resource/log4j.properties下面。


