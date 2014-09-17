拼写检查
===========
拼写检查又可以称作为**纠错**，有四种情景需要去考虑的：  

1. 查询时有一个或多个错误拼写的词汇单元导致不能命中相关文档，如果**搜索建议**功能可用，那么自动自动建议词汇单元，同时提示用户：“atmosphere 代替 atmosphear 搜索”。![suggestion](http://github-note.qiniudn.com/solr_suggest2.png)
2. 查询时是稀有的词汇单元，导致只命中少量文档，如果搜索建议开启了同时有更多的命中文档，那么可以提示：“你是否要搜索....”。![suggestion](http://github-note.qiniudn.com/solr_suggest1.png)。
3. 查询时又正确的拼写词汇单元，搜索建议功能开启，但是都只包含少量的命中文档或者有相同的命中，那么这种情况下不应该有任何提示。  
4. 查询时的词汇单元不存在索引中，搜索建议没开启。  

首先需要有一种方法为每一个查询的词汇单元标识建议词汇单元，也就是从有序的字典中查找与用户相似的词汇单元。
**拼写检查**能够帮助用户提供更精确的查询上节约不少时间，尤其是在移动互联网的大环境之下。  
**Autosuggest**：能帮助用户从索引中提供即时的搜索建议。  

Solr的Spell checker真正意义上还不算是一个checker，而是一个spell suggester。如果你的查询关键字拼写错误，它会提供一个建议：“你查找是XXX或者YYY吗。”  
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

