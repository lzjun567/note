solr自定义分词器：PunctuationTokenizerFactory
=================
有这么一个需求，像外国人的名字翻译成中文后，firstname和lastname中间会有个"·"或者是"-"这样的字符来分隔，通常姓名是作为完整的词保存到索引的，比如："贝拉克·奥巴马"希望分词的结果是"贝拉克|奥巴马"，但是IK默认的分词结果是："贝拉|克|奥|巴马"。怎么办呢？首先想到的是lucene自带有一个分词器叫[WhitespaceTokenizerFactory](https://wiki.apache.org/solr/AnalyzersTokenizersTokenFilters#solr.WhitespaceTokenizerFactory)。他会把字符按照空格来切分，比如："贝拉克 奥巴马"就能分成"贝拉克|奥巴马"两个词。因此我们可以仿照WhitespaceTokenizerFactory写一个类似的分词器。  

####第一步创建Tokenizer

    package com.sponia.lucene.analysis;
    
    import org.apache.lucene.analysis.util.CharTokenizer;
    import org.apache.lucene.util.Version;
    import org.apache.lucene.util.AttributeSource.AttributeFactory;
    
    import java.io.Reader;
    
    /**
     * Created by liuzhijun on 2014/7/18.
     */
    public class PunctuationTokenizer extends CharTokenizer {
    
        public PunctuationTokenizer(Version matchVersion, Reader in) {
            super(matchVersion, in);
        }
    
        public PunctuationTokenizer(Version matchVersion, AttributeFactory factory, Reader in) {
            super(matchVersion, factory, in);
        }
    
        @Override
        protected boolean isTokenChar(int c) {
            //这行就是关键代码，凡是遇到下面任意字符，都将作为切分词的依据 
            return c != ' ' && c != ',' && c != '.' && c != '·';
            
        }
    
    }
####第二步创建与之对应的工厂类PunctuationTokenizerFactory
    
    package com.sponia.lucene.analysis;
    
    import org.apache.lucene.analysis.Tokenizer;
    import org.apache.lucene.analysis.util.TokenizerFactory;
    import org.apache.lucene.util.AttributeSource;
    import org.apache.lucene.util.Version;
    
    import java.io.Reader;
    import java.util.Map;
    
    /**
     * Created by liuzhijun on 2014/7/18.
     */
    public class PunctuationTokenizerFactory extends TokenizerFactory {
    
        public PunctuationTokenizerFactory(Map<String,String> args) {
            super(args);
            assureMatchVersion();
            if (!args.isEmpty()) {
                throw new IllegalArgumentException("Unknown parameters: " + args);
            }
        }
    
        @Override
        public Tokenizer create(AttributeSource.AttributeFactory factory, Reader input) {
            return new PunctuationTokenizer(Version.LUCENE_47, factory, input);
        }
    }

####第三部配置到schema.xml中

     <fieldType name="text_punctuation" class="solr.TextField">
        <analyzer type="index"> 
            <tokenizer class="com.sponia.lucene.analysis.PunctuationTokenizerFactory"/>
        </analyzer>
        <analyzer type="query"> 
            <tokenizer class="org.wltea.analyzer.lucene.IKAnalyzerSolrFactory" useSmart="true"/>
            <filter class="solr.SynonymFilterFactory" synonyms="synonyms.txt" ignoreCase="true" expand="false"/>
        </analyzer>
    </fieldType> 

一个完整的分词器就完成了，步骤非常简单，现在来看看分词效果：  

![punctition.png](http://foofish.qiniudn.com/punctition.png)

