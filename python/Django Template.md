###一、变量

1. 变量的形式是：{{variable}}， 当模板引擎碰到变量的时候，引擎使用变量的值代替变量。
2. 使用dot(.)能够访问变量的属性
3. 当模板引擎碰到dot的时候，查找的顺序是什么样子呢？模版系统会按照如下顺序查找：

 - a.字典查找，例如：foo["var1"]
 - b.属性查找，例如：foo.bar
 - c.方法查找，例如：foo.bar()
 - d.list-index查找，例如foo[bar]
 
**注意**：方法查找比一般的查找要复杂一些  

- 如果调用方法期间，方法抛出一个异常，那么异常将会产生，除非异常对象带有一个属性silent_variable_failure，如果这个值是True，那么将会返回一个空字串。
- 方法调用仅仅对那些没有参数的方法才会生效
- 一些方法会产生副作用，所以系统允许方法设置一个属性alters_data，如果值为True，那么将不能够调用，其设置方法是：

        def sensitive_function(self):
            #函数内容
            sensitive_function.alters_data = True
- 如果模板中使用的某个变量不存在，那么模板系统将使用setting.py中 变量TEMPLATE_STRING_IF_INVALID的值进行替代，在默认情况下，该变量的值是''(空字符）。

###二、过滤器

1. 可以通过过滤器来修改变量的显示，过滤器的形式是：{{ variable | filter }}，管道符号'|'代表使用过滤器
2. 过滤器能够采用链式的方式使用，例如：{{ text | escape | linebreaks }}
3. 过滤器还可以带参数，例如： {{ bio|truncatewords:30 }}
4. 过滤器的参数中如果带有空格，那么需要用引号引起来，例如：{{ list | join : ", "}}
5. django中30个内建的过滤器

    1. add
            使用形式为：{{ value | add: "2"}}
            意义：将value的值增加2
            例如：value的值为4，那么输出结构为6
            **注意**：add首先尝试将两个值当作整数相加，如果失败就尝试把两个值组合在一起（比如遇到字符串或者list的时候），其他失败的情况最后返回一个空字符串，例如：表达式`{{first|add:second}}`，first=[1,2,3],second=[4,5,6]，那么输出结果为[1，2，3，4，5，6]

    2. addslashes
            使用形式为：{{ value | addslashes }}
            意义：在value中的引号（单引号和双引号）前增加反斜线
            例如：{{value|addslashes}}，`value=I' using Django`，输出结果是：`I\'m using Django`.  
            
    3. capfirst
            使用形式为：{{ value | capfirst }}
            意义：value的第一个字符转化成大写形式
    4. cut
             使用形式为：{{ value | cut:arg}}
             意义：移除value中包含arg的字符串
             例如，如果value是“String with spaces” arg是" "那么输出是"Stringwithspaces"
             
    5. date
             使用形式为：：
                 (a) {{ value | date:"D d M Y" }}，例如，如果value是一个datetime对象(datetime.datetime.now())那么输出将是字符串"Wed 09 Jan 2008"
                 (b) {{ value | date }}，这种形式没有格式化字符串，这时候，格式化字符串会自动采用DATE_FORMAT所设置的形式。
             意义：将日期格式数据按照给定的格式输出
    6. default
             使用形式：{{ value | default: "nothing" }}，例如，如果value是“”，那么输出将是nothing
             意义：如果value的意义是False，那么输出使用缺省值
             
    7. default_if_none
             使用形式：{{ value | default_if_none:"nothing" }}，例如，如果value是None，那么输出将是nothing
             意义：如果value是None，那么输出将使用缺省值
             
    8. dictsort
             意义：如果value的值是一个字典，那么返回值是按照关键字排序的结果
             使用形式：{{ value | dictsort:"name"}}，例如，
             如果value是：
       [
           {'name': 'zed', 'age': 19},
           {'name': 'amy', 'age': 22},
           {'name': 'joe', 'age': 31},
       ]
       那么，输出是：
       [
           {'name': 'amy', 'age': 22},
           {'name': 'joe', 'age': 31},
           {'name': 'zed', 'age': 19},
       ]

    9. dictsortreversed
       意义：如果value的值是一个字典，那么返回值是按照关键字排序的结果的反序
       使用形式：与上述(8)完全相同。
       
    10. divisibleby
       使用形式：{{ value | divisibleby:arg}}，如果value是21，arg是3，那么输出将是True
       意义：如果value能够被arg整除，那么返回值将是True
       
    11. escape
       使用形式：{{ value | escape}}
       意义：替换value中的某些字符，以适应HTML格式，包括：
       
            < is converted to &lt;
            > is converted to &gt;
            ' (single quote) is converted to &#39;
            " (double quote) is converted to &quot;
            & is converted to &amp;
        
       escape仅仅在输出的时候才起作用，所以escape不能够用在链式过滤器的中间，
他应该总是最后一个过滤器，如果想在链式过滤器的中间使用，那么可以使用force_escape

    12. escapejs
       使用形式：{{ value | escapejs }}
       意义：替换value中的某些字符，以适应JAVASCRIPT和JSON格式。
       例如：如果value的值是： `testing\r\njavascript \'string" <b>escaping</b>`, 那么输出：`testing\\u000D\\u000Ajavascript \\u0027string\\u0022 \\u003Cb\\u003Eescaping\\u003C/b\\u003E`
       
    13. filesizeformat
       使用形式：{{ value | filesizeformat }}
       意义：格式化value，使其成为易读的文件大小，例如：13KB，4.1MB等。
       
   14. first
       使用形式：{{ value | first }}
       意义：返回列表中的第一个Item，例如，如果value是列表['a','b','c']，那么输出将是'a'。

    15. floatformat
       使用形式：{{ value | floatformat}}或者{{value|floatformat:arg}}，
                 arg可以是正数也可以是负数。没有参数的floatformat相当于floatformat:-1
       (1)如果不带arg，那么引擎会四舍五入，同时最多只保留一位小数
       
            34.23234    {{ value|floatformat }}  34.2
            34.00000	{{ value|floatformat }}	34
            34.26000	{{ value|floatformat }}	34.3
        (2)如果arg是正数，那么引擎会四舍五入，同时保留arg位的小数。

            34.23234	{{ value|floatformat:3 }}	34.232
            34.00000	{{ value|floatformat:3 }}	34.000
            34.26000	{{ value|floatformat:3 }}	34.260
        (3)如果arg是负数，那么引擎会四舍五入，如果有小数部分，那么保留arg位小数；否则，则没有任何小数部分。

            34.23234	{{ value|floatformat:"-3" }}	34.232
            34.00000	{{ value|floatformat:"-3" }}	34
            34.26000	{{ value|floatformat:"-3" }}	34.26
            
    16. get_digit
       使用形式：{{ value | get_digit:"arg"}}，例如，如果value是123456789，arg是2，那么输出是8
       意义：给定一个数字，返回，请求的数字，记住：1代表最右边的数字，如果value不是合法输入，那么会返回所有原有值。
       
    17. iriencode
       使用形式：{{value | iriencode}}
       意义：如果value中有非ASCII字符，那么将其进行转化成URL中适合的编码，如果value已经进行过URLENCODE，该操作就不会再起作用。
       
    18. join
       使用形式：{{ value | join:"arg"}}，如果value是['a','b','c']，arg是'//'那么输出是a//b//c
       意义：使用指定的字符串连接一个list，作用如同python的str.join(list)
       
    19. last
       使用形式：{{ value | last }}
       意义：返回列表中的最后一个Item
       
    20. length
       使用形式：{{ value | length }}
       意义：返回value的长度。
       
    21. length_is
       使用形式：{{ value | length_is:"arg"}}
       意义：返回True，如果value的长度等于arg的时候，例如：如果value是['a','b','c']，arg是3，那么返回True
       
    22. linebreaks
       使用形式：{{value|linebreaks}}
       意义：value中的"\n"将被<br/>替代，并且整个value使用</p>包围起来，从而适和HTML的格式
       
    23. linebreaksbr
       使用形式：{{value |linebreaksbr}}
       意义：value中的"\n"将被`<br/>`替代
       
    24. linenumbers
       使用形式：{{value | linenumbers}}
       意义：显示的文本，带有行数。
       
    25. ljust
       使用形式：{{value | ljust}}
       意义：在一个给定宽度的字段中，左对齐显示value
       
    26. center
       使用形式：{{value | center}}
       意义：在一个给定宽度的字段中，中心对齐显示value
       
    27. rjust
       使用形式：{{value | rjust}}
       意义：在一个给定宽度的字段中，右对齐显示value
       
    28. lower
       使用形式：{{value | lower}}
       意义：将一个字符串转换成小写形式
       
    29. make_list
       使用形式：{{value | make_list}}
       意义：将value转换成一个list，对于字符串，转换成字符list；对于整数，转换成整数list
       例如value是Joel，那么输出将是[u'J',u'o',u'e',u'l']；value是123，那么输出将是[1,2,3]
       
    30. pluralize
       使用形式：{{value | pluralize}}，或者{{value | pluralize:"es"}}，或者{{value | pluralize:"y,ies"}}
       意义：如果value不是1，则返回一个复数后缀，缺省的后缀是's'
    31. random
       使用形式：{{value | random}}
       意义：从给定的list中返回一个任意的Item
       
    32. removetags
       使用形式：{{value | removetags:"tag1 tag2 tag3..."}}
       意义：删除value中tag1,tag2....的标签。例如，如果value是`<b>Joel</b> <button>is</button> a <span>slug</span>`
             tags是"b span"，那么输出将是：`Joel <button>is</button> a slug`
             
    33. safe
       使用形式：{{value | safe}}
       意义：当系统设置autoescaping打开的时候，该过滤器使得输出不进行escape转换
       
    34. safeseq
       与上述safe基本相同，但有一点不同的就是：safe是针对字符串，而safeseq是针对多个字符串组成的sequence
       
    35. slice
       使用形式：{{some_list | slice:":2"}}
       意义：与python语法中的slice相同，:2表示第一的第二个元素
       
    36. slugify
        使用形式：{{value | slugify}}
        意义：将value转换成小写形式，同事删除所有分单词字符，并将空格变成横线
              例如：如果value是Joel is a slug，那么输出将是joel-is-a-slug
    37. stringformat
        这个不经常用，先不说
        简单举个例子：如果value是 10，那么输出 1.000000E+01
        
    38. striptags
        使用形式：{{value | striptags}}
        意义：删除value中的所有HTML标签
        
    39. time
        使用形式：{{value | time:"H:i"}}或者{{value | time}}
        意义：格式化时间输出，如果time后面没有格式化参数，那么输出按照TIME_FORMAT中设置的进行。
        
    40. title
        转换一个字符串成为title格式。
        如： value是 "my first post",输出： "My First Post"
        
    41. truncatewords
        使用形式：{{value | truncatewords:2}}
        意义：将value切成truncatewords指定的单词数目
        例如，如果value是Joel is a slug 那么输出将是：Joel is ...
        
    42. truncatewords_html
        使用形式同(39)
        意义：truncation点之前如果某个标签打开了，但是没有关闭，那么在truncation点会立即关闭。
              因为这个操作的效率比truncatewords低，所有只有在value是html格式时，才考虑使用。
              
    43. upper
        转换一个字符串为大写形式
        
    44. urlencode
        将一个字符串进行URLEncode
        
    45. urlize
        意义：将一个字符串中的URL转化成可点击的形式。
        使用形式：{{ value | urlize }}
        例如，如果value是Check out www.djangoproject.com，那么输出将是：
              Check out <a href="http://www.djangoproject.com">www.djangoproject.com</a>
              
    46. urlizetrunc
        使用形式：{{ value | urlizetrunc:15}}
        意义：与(43)相同，但是有一点不同就是现实的链接字符会被truncate成特定的长度，后面以...现实。
        
    47. wordcount
        返回字符串中单词的数目
        
    48. wordwrap
        使用形式：{{value | wordwrap:5}}
        意义：按照指定的长度包装字符串
        例如，如果value是Joel is a slug，那么输出将会是：
        Joel
        is a
        slug
    49. timesince
        使用形式：{{value | timesince:arg}}
        意义：返回参数arg到value的天数和小时数
        例如，如果 blog_date 是一个日期实例表示 2006-06-01 午夜， 而 comment_date 是一个日期实例表示 2006-06-01 早上8点，
              那么 {{ comment_date|timesince:blog_date }} 将返回 "8 hours".
              
    50. timeuntil
        使用形式：{{value | timeuntil}}
        意义：与(47)基本相同，一个不同点就是，返回的是value距离当前日期的天数和小时数。

###三、标签  
1. 标签的形式是：{% tag %}，标签要比变量复杂
2. 标签的作用  
      (1)在输出时创建一些文本  
      (2)通过执行循环和一些逻辑来实现控制流  
      (3)装载一些外部信息进入模板
3. 内建标签
      (1)autoescape

        使用形式：
             {% autoescape off %}
                 (内容)
             {% endautoescape %}
         意义：当某块内容不需要自动转义的时候，这样写就可以了。当然如果块内某些地方需要转义的话，调用filter也可以。
      (2)block
      
         使用形式：
             {% block %}
                 (定义块内容)
             {% endblock %}
         意义：定义一个块，该块能够被继承他的子孙模板重写
      (3)comment
      
         使用形式：
             {% comment %}
                  (内容)
             {% endcomment %}
         意义：模板系统会忽略该标签内部的所有内容。
      (4)cycle
      
         使用形式：
         例如:
             <tr class="{% cycle list%}">
              ...
             </tr>
         意义：在循环时轮流使用给定的字符串列表中的值。
         
      (5)extends
      
         使用形式：{% extends "base.html" %}或者{% extends variable %}变量可以是一个字符串，也可以是一个模板对象。
         意义：表示本模板要对指定的父模板进行扩展。
      (6)filter
      
         使用形式：
             {%filter force_escape|lower%}
                 (内容)
             {%endfilter%}
         意义：将filter 标签圈定的内容执行过滤器操作。
      (7)firstof
      
         使用形式：{%firstof var1 var2 var3%}
         意义：输出第一个值不等于False的变量
         等价于：               
         {% if var1 %}
             {{ var1 }}
         {% else %}
             {% if var2 %}
                 {{ var2 }}
             {% else %}
                 {% if var3 %}
                     {{ var3 }}
                 {% endif %}
             {% endif %}
         {% endif %}
      (8)for
      
         使用形式：
             {% for variable in list/dict %}
                   (使用variable)
             {% endfor%}
         意义：循环list中的每个值，进行相应的输出
         注意：(a)也可以反向遍历{% for variable in list/dict reversed %}
               (b)也可以{% for x, y in points %} points中的每个元素为 (x,y)
               (c)也可以{% for key,value in data.items %}   data是一个dictionary 
         for loop中定义的一些内建变量
         forloop.counter         当前的迭代器数目(从1开始)
         forloop.counter0        当前的迭代器数目(从0开始)
         forloop.revcounter      当前的反向迭代器数目(从1开始)
         forloop.revcounter0     当前的反向迭代器数目(从0开始)
         forloop.first           值为True，如果是第一次通过迭代器
         forloop.last            值为True，如果是最后一次通过迭代器
         forloop.parentloop      对于嵌套循环，这是当前循环的上一层循环
      (9)for ... empty
      
         使用形式如下：
             {% for varibale in list %}
                  (内容1)
             {% empty %}
                  (内容2)
             {% endfor %}
         意义：当list是空的时候，能够执行内容2，其形式等同于，先if判断list是否存在，然后在根据情况做什么操作。
      (10)if
      
         使用形式如下 ：
             {% if variable %}
                 (内容1)
             {% else %}
                 (内容2)
             {% endif %}
         注意：variable中可以使用and or 或者not，但是有一条必须记住，就是不允许and 和 or一起使用
       (11)ifchanged
       
          使用形式：
          (a)如果直接检测循环变量是否变化，那么使用：
              {% ifchanged %}  
                  (内容)
              {% endifchanged %}
          (b)如果检测循环变量的某个dot变量，例如循环变量是date，那么检测date.hour，那么使用：
              {% ifchanged date.hour%}  
                  (内容)
              {% endifchanged %}    
          (c)ifchanged也可以加上一个{% else %}语句
          意义：检测本次循环的值和上一次循环的值一样不一样，只能用在循环里面。 
       (12)ifequal
       
          使用形式：
              {% ifequal variable1 variable2 %}
                  ...
              {% endifequal %}
          意义：判断两个变量是否相等。
       (13)ifnotequal
       
          使用与(12)相同
       (14)include
       
          使用形式：{% include "foo/bar.html" %}或者{% include template_name %}
          意义：将另外一个模板文件中的内容添加到该文件中。注意区别extend是继承。
       (15)now
       
          使用形式：{% now "jS F Y H:i "%}，注意存在需要转义的情况例如{% now "jS o\f F" %}，因为f是格式化字符串
          
具体的格式化字符串如下所示：
a
'a.m.' or 'p.m.' (Note that this is slightly different than PHP's output, because this includes periods to match Associated Press style.)	'a.m.'  
A
'AM' or 'PM'.	'AM'

b
Month, textual, 3 letters, lowercase.	'jan'

B
Not implemented.

d
Day of the month, 2 digits with leading zeros.	'01' to '31'

D
Day of the week, textual, 3 letters.	'Fri'

f
Time, in 12-hour hours and minutes, with minutes left off if they're zero. Proprietary extension.	'1', '1:30'

F
Month, textual, long.	'January'

g
Hour, 12-hour format without leading zeros.	'1' to '12'

G
Hour, 24-hour format without leading zeros.	'0' to '23'

h
Hour, 12-hour format.	'01' to '12'

H
Hour, 24-hour format.	'00' to '23'

i
Minutes.	'00' to '59'

I
Not implemented.	 

j
Day of the month without leading zeros.	'1' to '31'

l
Day of the week, textual, long.	'Friday'

L
Boolean for whether it's a leap year.	True or False

m
Month, 2 digits with leading zeros.	'01' to '12'

M
Month, textual, 3 letters.	'Jan'

n
Month without leading zeros.	'1' to '12'

N
Month abbreviation in Associated Press style. Proprietary 
extension.	'Jan.', 'Feb.', 'March', 'May'

O
Difference to Greenwich time in hours.	'+0200'

P
Time, in 12-hour hours, minutes and 'a.m.'/'p.m.', with minutes left off if they're zero and the special-case strings 'midnight' and 'noon' if appropriate. Proprietary extension.	'1 a.m.', '1:30 p.m.', 'midnight','noon', '12:30 p.m.'

r
RFC 2822 formatted date.	'Thu, 21 Dec 2000 16:01:07+0200'

s
Seconds, 2 digits with leading zeros.	'00' to '59'

S
English ordinal suffix for day of the month, 2 characters.	'st', 'nd', 'rd' or 'th'

t
Number of days in the given month.	28 to 31

T
Time zone of this machine.	'EST', 'MDT'

U
Not implemented.	 

w
Day of the week, digits without leading zeros.	'0' (Sunday) to '6' (Saturday)

W
ISO-8601 week number of year, with weeks starting on Monday.	1, 53

y
Year, 2 digits.	'99'

Y
Year, 4 digits.	'1999'

z
Day of the year.	0 to 365

Z
Time zone offset in seconds. The offset for timezones west of UTC is always negative, and for those east of UTC is always positive.

(16)spaceless
         使用形式：{% spaceless %}
                        (内容)
                   {% endspaceless %}
         意义：删除包围内容中的所有tab或者回车字符。
         
(17)template
          使用形式：{% templatetag %}
          意义：模板系统本身没有转义的概念，因此如果要输出一个像“{%”这样的东东，就需要采用这种方式，否则就会语法错误
其参数有：

    openblock	{%
    closeblock	%}
    openvariable	{{
    closevariable	}}
    openbrace	{
    closebrace	}
    opencomment	{#
    closecomment	#}
    
(18)with

使用形式：
     {% with  "expensive var1" as var2 %}
     {% endwith %}
 意义：当一个变量的访问消耗很大的模板解析时，可以用另外一个变量替换它，这种替换只有在with内部有效。
 
(19)url
 使用形式：{% url path.to.some_view arg1,arg2 %}
 意义：给定某个module中函数的名字，给定参数，那么模板引擎给你一个URL，从而避免硬编码URL到代码中
 
 注意：前提是URLconf中存在相应的映射,如果URLconf中没有该映射，那么会抛出异常，
       这是可以选择使用
       {% url path.to.view arg1 ,arg2 as the url %}
       <a href="{{ the_url }}">Link to optional stuff</a>
       其实这相当于
       {% url path.to.view as the_url %}
       {% if the_url %}
           <a href="{{ the_url }}">Link to optional stuff</a>
       {% endif %}
             
参考：
https://docs.djangoproject.com/en/dev/ref/templates/builtins/
http://lishiguang.iteye.com/blog/1332529
