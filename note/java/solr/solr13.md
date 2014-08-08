solr(14)：solr.SynonymFilterFactory
=============================
https://wiki.apache.org/solr/AnalyzersTokenizersTokenFilters  

使用方式：  

      <fieldtype name="syn" class="solr.TextField">
          <analyzer>
              <tokenizer class="solr.WhitespaceTokenizerFactory"/>
              <filter class="solr.SynonymFilterFactory" synonyms="syn.txt" ignoreCase="true" expand="false"/>
          </analyzer>
      </fieldtype>

配置文件syn.txt格式：  
    
    # blank lines and lines starting with pound are comments.

    #Explicit mappings match any token sequence on the LHS of "=>"
    #and replace with all alternatives on the RHS.  These types of mappings
    #ignore the expand parameter in the schema.
    #Examples:
    i-pod, i pod => ipod,
    sea biscuit, sea biscit => seabiscuit
    
    #Equivalent synonyms may be separated with commas and give
    #no explicit mapping.  In this case the mapping behavior will
    #be taken from the expand parameter in the schema.  This allows
    #the same synonym file to be used in different synonym handling strategies.
    #Examples:
    ipod, i-pod, i pod
    foozball , foosball
    universe , cosmos
    
    # If expand==true, "ipod, i-pod, i pod" is equivalent to the explicit mapping:
    ipod, i-pod, i pod => ipod, i-pod, i pod
    # If expand==false, "ipod, i-pod, i pod" is equivalent to the explicit mapping:
    ipod, i-pod, i pod => ipod
    
    #multiple synonym mapping entries are merged.
    foo => foo bar
    foo => baz
    #is equivalent to
    foo => foo bar, baz

配置文件按行处理，空行和"#"开头的行都是注释，同义词有两种配置方式：  

1. 对于使用等式"=>"的行，expand参数会忽略掉，"=>"左边的词元将会被右边的词替换。如：  
    
        i-pod, i pod => ipod,
        sea biscuit, sea biscit => seabiscuit 
    也就是说在搜索或者索引时，遇到i-pod或i pod时都将用ipod代替。  
2. 同义词用逗号分隔，它没有显示的映射关系，它的映射策略取决于expand参数。例如：  
    
        ipod, i-pod, i pod
        foozball , foosball
        universe , cosmos
    * 如果expand==true，那么它等效于：  

            ipod, i-pod, i pod => ipod, i-pod, i pod
        也就是说当你搜i-pod的时候，可以同时匹配ipod,i-pod,i pod，搜ipod的时候也是同理。
    * 如果expand==false， 那么它等效于：  
            ipod, i-pod, i pod => ipod
        也即是说他只匹配改行的第一个词元。
另外多个同义词映射实体会被合并，如：  
    foo => foo bar
    foo => baz
    foo => foo bar, baz

3. ingoreCase:为true时忽略大小写，处理时都转换为小写  
