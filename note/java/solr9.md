Query Elevation 组件
=====================
Elevation的意思是指“提升”，把某个文档提到前面，它能实现“竞价排名”的功能。尽管这个组件能在任何的QueryParser下使用，不过最明智的选择还是用DisMax或者eDisMax。另外这个组件同时支持分布式搜索。  

####配置

    <searchComponent name="elevator" class="solr.QueryElevationComponent" >
      <!-- pick a fieldType to analyze queries -->
      <str name="queryFieldType">string</str>
      <str name="config-file">elevate.xml</str>
    </searchComponent>
    <requestHandler name="/elevate" class="solr.SearchHandler" startup="lazy">
      <lst name="defaults">
        <str name="echoParams">explicit</str>
      </lst>
      <arr name="last-components">
        <str>elevator</str>
      </arr>
    </requestHandler>

配置文件如果放在conf目录下，那么自在solr启动的时候加载一次，如果是放在data目录，那么会在IndexReader初始化的时候重新加载，也就是在每次commit发生的时候会重新加载elevate.xml文件，这样就可以实现动态加载Elevation信息。

elevate.xml配置文件看起来应该是：  

    <elevate>
     <query text="AAA">
      <doc id="A" />
      <doc id="B" />
     </query>
     <query text="ipod">
      <doc id="A" />
      <!-- you can optionally exclude documents from a query result -->
      <doc id="B" exclude="true" />
     </query>
    </elevate>
是的，也可以指定某个文档不出现在搜索结果中，只需要属性exclude="true"    

请求参数中添加exclude=true，那么返回结果只就只包括elevate文件中指定的结果:    
[http://localhost:8983/solr/collection1/elevate?q=python&wt=json&indent=true&df=content&exclusive=true](http://localhost:8983/solr/collection1/elevate?q=python&wt=json&indent=true&df=content&exclusive=true)

请求参数中指定excludeIds和elevatedIds，后配置文件不再生效  
[http://localhost:8983/solr/collection1/elevate?q=python&wt=json&indent=true&df=content&elevateIds=10,17&excludeIds=57](http://localhost:8983/solr/collection1/elevate?q=python&wt=json&indent=true&df=content&elevateIds=10,17&excludeIds=57)

Optional attributes on "doc"

boost = <float> — default is 1.0
This is a convinience mechanism equivilent to specifying a boost attribute on each of the individual fields that support norms (see below)
Optional attributes for "field"

update = "add" | "set" | "inc" — for atomic updating and adding of fields <!> Solr4.0
boost = <float> — default is 1.0 (See SolrRelevancyFAQ)
NOTE: make sure norms are enabled (omitNorms="false" in the schema.xml) for any fields where the index-time boost should be stored.

<add>
  <doc boost="2.5">
    <field name="employeeId">05991</field>
    <field name="office" boost="2.0">Bridgewater</field>
  </doc>
</add>


http://wiki.apache.org/solr/UpdateXmlMessages#Optional_attributes_on_.22doc.22

http://java.dzone.com/articles/options-tune-document%E2%80%99s
