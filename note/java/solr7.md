CopyField
================
copyfield可以实现一个字段的多次使用

比如：

说的简单一点，比如现在你要查询有"Java"的博客， 那么你肯定要查内容，标题是否包含Java，但是solr不能像SQL那样，where tittle like '%Java%'  or  content like '%Java%'.   这个时候copyField就派上用场了， 定义一个新字段，将title和content 复制到这个新字段，索引的时候，直接从这个新字段查询，这样就达到目地了。  这便是copyField的典型应用场景 。注意：如果dest由多个source构成，就需要将其指定为multiValued
    
    <field name="title"/>
    <field name="content"/>
    <field name="tc" multiValued="true"/>
    <copyFeild source="title" dest="tc" maxChars="3000"/>
    <copyFeild source="content" dest="tc" maxChars="3000"/>

现在就可以通过指定tc来搜索包括title、content在内的关键字了。

####multiValued
当某个文档内容一个字段多个值，比如：  

    <add>  
      <doc>  
        <field name="id">2</field>  
        ...  
        <field name="link">http://manning.com/</field>               
        <field name="link">http://lucene.apache.org/solr/</field>   
        ...  
         </doc> 
    </add>

那么在solr中可以配置一个字段的属性为multiValued="true"

    <field name="link"  
           type= "string"  
           indexed= "true"  
           stored="true"  
           multiValued="true"/> 

这样搜索`link:" http://manning.com/"`时，Solr会在
