Solr(10)：相关性[FAQ](http://wiki.apache.org/solr/SolrRelevancyFAQ)
========
* 从Solr3.1开始，推荐使用edismax查询解析器，即defType=edismax
* 如何在字段title和subject中搜索superman
    * 标准查询解析器使用：
            
            q = title:superman subject:superman
    * dismax中使用：
            
            q= superman&qf=title subject
* 搜索superman时，title字段权重高于subject
    * 标准查询解析器：
            
            q = title:superman^2 subject:superman
    * dismax中使用：
            
            q = superman&qf=title^2 subject
*如何查询诸如： 
    * "Wi-Fi" -> "Wi", "Fi" 

