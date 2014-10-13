拼写检查
===========
拼写检查又可以称作为**纠错**，在搜索程序中是一个很重要的特性，它能更正用户的误操作带来的错误搜索结果，这个特性在移动设备中显得尤为重要，因为键盘太小，误操作的概率也会增加。拼写检查有四种情景需要考虑：  

1. 查询时有一个或多个错误拼写的单词导致不能命中相关文档，如果**搜索建议**功能可用，那么搜索客户端应该自动用**建议词汇**搜索，同时给用户提示信息：“yyy 代替 xxx 搜索”。![suggestion](http://github-note.qiniudn.com/solr_suggest2.png)
2. 查询时是稀有的，偏门的，不常见的词语，导致只命中少量文档，如果**搜索建议**功能可用，同时"建议词汇"有更多的命中文档，那么可以提示：“你是否要搜索....”。![suggestion](http://github-note.qiniudn.com/solr_suggest1.png)
3. 查询时单词拼写正确，同时搜索建议功能开启，但是两者都只包含少量的命中文档或者有相同的命中，那么这种情况下不应该有任何提示。  
4. 查询时的词汇单元不存在索引中，同时也没有搜索建议词汇存在。  

根据上面的四中情形，可以从中提取出两个关键的“拼写检查”的需求。首先，需要有一种方法为每一个查询的词汇单元标识一个与之对应的“建议词汇”，也就是从有序的字典中查找与用户相似的词汇。第二，需要知道每个对应的“建议词汇”有多少匹配的文档，这个参数可以帮助用户决定是否给用户一个提示。  

####集成“拼写检查搜索组件”到/select请求处理器中
拼写组件可以轻松的集成到select请求处理器中，默认对所有的查询生效，此外客户端也可以控制组件是否生效，如果小禁用拼写检查，那么在url中指定查询参数spellcheck=false即可。  

    <requestHandler name="/select" class="solr.SearchHandler">
         <lst name="defaults">
           <str name="echoParams">explicit</str>
           <int name="rows">10</int>
           <str name="df">text</str>
           <!-- 添加spellcheck -->
           <str name="spellcheck">on</str>
           <str name="spellcheck.extendedResults">false</str>
           <str name="spellcheck.count">5</str>   <!-- 指定sugesstion的最大值 -->
           <str name="spellcheck.alternativeTermCount">2</str>
           <str name="spellcheck.maxResultsForSuggest">5</str>
           <str name="spellcheck.collate">true</str> <!-- 基于建议词语进行一次查询 -->
           <str name="spellcheck.collateExtendedResults">true</str>
           <str name="spellcheck.maxCollationTries">5</str>
           <str name="spellcheck.maxCollations">3</str>
         </lst>
        <!-- 拼写检查必须作为最后一个组件列出来 --> 
        <arr name="last-components">
            <str>spellcheck</str>
        </arr>
    </requestHandler>

#####实例：
索引中包含有“fk123,fk1234”等词汇的文档，现在用一个错误的词“fu123”去搜索：[http://localhost:8080/solr/collection1/select?q=fu123]( http://localhost:8080/solr/collection1/select?q=fu123) 

    <response>
        <lst name="responseHeader">
            <int name="status">0</int>
            <int name="QTime">22</int>
            <lst name="params">
                <str name="q">fu123</str>
            </lst>
        </lst>
        <result name="response" numFound="0" start="0"/>
        <lst name="spellcheck">
            <lst name="suggestions">
                <lst name="fu123">
                    <int name="numFound">2</int>
                    <int name="startOffset">0</int>
                    <int name="endOffset">5</int>
                    <arr name="suggestion">
                        <str>fk123</str>
                        <str>fk1234</str>
                    </arr>
                </lst>
                <lst name="collation">
                    <str name="collationQuery">fk123</str>
                    <int name="hits">1</int>
                    <lst name="misspellingsAndCorrections">
                        <str name="fu123">fk123</str>
                    </lst>
                </lst>
                <lst name="collation">
                    <str name="collationQuery">fk1234</str>
                    <int name="hits">1</int>
                    <lst name="misspellingsAndCorrections">
                        <str name="fu123">fk1234</str>
                    </lst>
                </lst>
            </lst>
        </lst>
    </response>  

没有发现任何"fu123"相关的记录，但是发现了两个建议词汇“fk123”和“fk1234”。

####配置独立的spellcheck搜索组件

    <SearchSpellrchComponent name="spellcheck" class="solr.SpellCheckComponent">
     <!--用text_general这个字段来分析查询关键字 -->
     <str name="queryAnalyzerFieldType">text_general</str>
     <!-- a spellchecker built from a field of the main index -->
     <lst name="spellchecker">
         <!-- 拼写检查器的名字 -->
       <str name="name">default</str>
         <!-- 用于suggestion的字段-->
       <str name="field">suggest</str>
       <str name="classname">solr.DirectSolrSpellChecker</str>
       <!-- the spellcheck distance measure used, the default is the internal levenshtein -->
       <str name="distanceMeasure">internal</str>
       <!-- minimum accuracy needed to be considered a valid spellcheck suggestion -->
       <float name="accuracy">0.5</float>
       <!-- the maximum #edits we consider when enumerating terms: can be 1 or 2 -->
       <int name="maxEdits">2</int>
       <!-- the minimum shared prefix when enumerating terms -->
       <int name="minPrefix">1</int>
       <!-- maximum number of inspections per result. -->
       <int name="maxInspections">5</int>
       <!-- minimum length of a query term to be considered for correction -->
       <int name="minQueryLength">4</int>
       <!-- maximum threshold of documents a query term can appear to be considered for correction -->
       <float name="maxQueryFrequency">0.01</float>
     </lst>
    </searchComponent>

####DirectSolrSpellChecker
Solr4中默认的拼写检查组件是DirectSolrSpellChecker，如其名字一样，直接通过main index提供“建议”，而不需要像早起版本的Solr一样首先要基于main index 构建一个“拼写检查”的index。它有三个关键参数：field，distaneMeasure，accuracy。    

field：用于标识用于suggestions的字段。使用copy field作为suggestion有利于应用不同的分析器。  
distanceMeasure：编辑距离，用于决定查询词汇的建议词汇  
accuracy：精确度。  


####N-gram
实现spellcheck，简单理解就是将用户输入的词组（英文为单词，中文为词组）和字典里面的“标准”词组进行“相似性”比较，并给出相似程度最高的词组。  



 checker真正意义上还不算是一个checker，而是一个spell suggester。如果你的查询关键字拼写错误，它会提供一个建议：“你查找是XXX或者YYY吗。”  
Solr4.0使用solr.DirectSolrSpellchecker实现spellchecker，它可以使用你自己的索引，每次commit不需要重建。  

1. 编辑solrconfig.xml，添加拼写组件：  
    
        <searchComponent name="spellcheck" class="solr.SpellCheckComponent">
            <str name="queryAnalyzerFieldType">text_general</str>
            <lst name="spellchecker">
                <str name="name">direct</str>
                <str name="field">title</str>
                <str name="classname">solr.DirectSolrSpellChecker</str>
                <str name="distanceMeasure">internal</str>
                <float name="accuracy">0.8</float>
                <int name="maxEdits">1</int>
                <int name="minPrefix">1</int>
                <int name="maxInspections">5</int>
                <int name="minQueryLength">3</int>
                <float name="maxQueryFrequency">0.01</float>
            </lst>
        </searchComponent>
2. 添加请求处理器：  
        
        <requestHandler name="/spell" class="solr.SearchHandler" startup="lazy">
            <lst name="defaults">
                <str name="df">title</str> <!-- 用于拼写检查的默认域 -->
                <str name="spellcheck.dictionary">direct</str>
                <str name="spellcheck">on</str>
                <str name="spellcheck.extendedResults">true</str> 
                <str name="spellcheck.count">5</str> 
                <str name="spellcheck.collate">true</str>
                <str name="spellcheck.collateExtendedResults">true</str> 
            </lst>
            <arr name="last-components">
                <str>spellcheck</str>
            </arr>
        </requestHandler>
3. 发送请求：/spell?q=discouna（假设索引中已经存在一个文档为：`{"id":"t0001","title":"discount"}`的数据）
4. 相应结果：  
        
        <response>
            <lst name="responseHeader">
                <int name="status">0</int>
                <int name="QTime">58</int>
            </lst>
            <result name="response" numFound="0" start="0"/>
            <lst name="spellcheck">
                <lst name="suggestions">
                    <lst name="discouna">
                        <int name="numFound">1</int>
                        <int name="startOffset">0</int>
                        <int name="endOffset">8</int>
                        <int name="origFreq">0</int>
                        <arr name="suggestion">
                            <lst>
                                <str name="word">discount</str>
                                <int name="freq">1</int>
                            </lst>
                        </arr>
                    </lst>
                    <bool name="correctlySpelled">false</bool>
                    <lst name="collation">
                        <str name="collationQuery">discount</str>
                        <int name="hits">0</int>
                        <lst name="misspellingsAndCorrections">
                            <str name="discouna">discount</str>
                        </lst>
                    </lst>
                </lst>
            </lst>
            </response>

