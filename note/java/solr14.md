solr.EdgeNGramFilterFactory
================
http://wiki.apache.org/solr/AnalyzersTokenizersTokenFilters#solr.EdgeNGramFilterFactory
对于词元Nigerain，  

    Nigerian => "ni", "nig", "nige", "niger", "nigeri", "nigeria", "nigeria", "nigerian"
默认minGramSize=1，maxGramSize=1，从左边开始，比如：对于单词Apache，如果minGramSize=4，那么就会得到 "Apac", "Apach", "Apache"3个词元(token)  
这个过滤器在前缀匹配的时候非常实用，

    <fieldType name="text_general_edge_ngram" class="solr.TextField" positionIncrementGap="100">
       <analyzer type="index">
          <tokenizer class="solr.LowerCaseTokenizerFactory"/>
          <filter class="solr.EdgeNGramFilterFactory" minGramSize="2" maxGramSize="15" side="front"/>
       </analyzer>
       <analyzer type="query">
          <tokenizer class="solr.LowerCaseTokenizerFactory"/>
       </analyzer>
    </fieldType>

minGramSize：
