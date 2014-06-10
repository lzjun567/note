Query Elevation 组件
=====================
Elevation的意思是指“提升”，把某个文档提到前面，尽管这个组件能在任何的QueryParser下使用，不过最明智的选择还是用DisMax或者eDisMax。另外这个组件同时支持分布式搜索。  

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

配置文件如果放在conf目录下，那么自在solr启动的时候加载一次，如果是放在data目录，那么会被每一个IndexReader重新加载。

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

请求参数中添加exclude=true，那么返回结果只就只包括elevate文件中指定的结果  

    http://localhost:8983/solr/collection1/elevate?q=python&wt=json&indent=true&df=content&exclusive=true

请求参数中指定excludeIds和elevatedIds，后配置文件不再生效  

    http://localhost:8983/solr/collection1/elevate?q=python&wt=json&indent=true&df=content&elevateIds=10,17&excludeIds=57
