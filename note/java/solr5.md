整合IK Analyzer
=====================
IK Analyzer是一款结合了词典和文法分析算法的中文分词组件，基于字符串匹配，支持用户词典扩展定义，支持细粒度和智能切分，比如：  

    张三说的确实在理

智能分词的结果是：  

    张三 |  说的 |  确实 |  在理 
最细粒度分词结果：  

    张三 |  三 |  说的 |  的确 |  的 |  确实 |  实在 |  在理

整合IK Analyzer比mmseg4j要简单很多，[下载](https://code.google.com/p/ik-analyzer/downloads/list)解压缩IKAnalyzer2012FF_u1.jar放到目录：E:\solr-4.8.0\example\solr-webapp\webapp\WEB-INF\lib，修改配置文件schema.xml，添加代码：  
   
      <field name="ik_analyzer_name" type="text_ik" indexed="true" stored="true"/> 

      <fieldType name="text_ik" class="solr.TextField">
            <analyzer type="index" isMaxWordLength="false" class="org.wltea.analyzer.lucene.IKAnalyzer"/>
    	    <analyzer type="query" isMaxWordLength="true" class="org.wltea.analyzer.lucene.IKAnalyzer"/>
      </fieldType>

    查询采用IK自己的最大分词法,索引则采用它的细粒度分词法

此时就算配置完成了，重启服务：java -jar start.jar，来看看IKAnalyzer的分词效果怎么样，打开Solr管理界面，点击左侧的Analysis页面  
![index4](http://blog-resource.qiniudn.com/index4.png)  
默认分词器进行最细粒度切分。IKAnalyzer支持通过配置IKAnalyzer.cfg.xml 文件来扩充您的与有词典以及停止词典（过滤词典），只需把IKAnalyzer.cfg.xml文件放入class目录下面，指定自己的词典mydic.dic  

    <?xml version="1.0" encoding="UTF-8"?> 
    <!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">   
    <properties>   
      <comment>IK Analyzer 扩展配置</comment> 
      <!--用户可以在这里配置自己的扩展字典  -->  
      <entry key="ext_dict">/mydict.dic; 
    /com/mycompany/dic/mydict2.dic;</entry>  
     
       <!--用户可以在这里配置自己的扩展停止词字典--> 
      <entry key="ext_stopwords">/ext_stopword.dic</entry>    
    </properties> 

