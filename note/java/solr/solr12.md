solr(12)：源码分析之HTMLStripCharFilterFactory
==============
HTMLStripCharFilter工厂类，用于过滤HTML，必须用<charFilter>标签指定，而且要在<tokenizer>之前，例如：  

    <fieldType name="text_html" class="solr.TextField" positionIncrementGap="100">
       <analyzer>
         <charFilter class="solr.HTMLStripCharFilterFactory" escapedTags="a, title" />
         <tokenizer class="solr.WhitespaceTokenizerFactory"/>
       </analyzer>
     </fieldType>


http://copious.me/posts/lucene-code-samples-htmlstripcharfilter/
