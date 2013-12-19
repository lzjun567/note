Mako 模板语言
-------------------
**Mako的哲学:Python is great scripting language ,don't reinvent the wheel, your template can handle it !**, api非常简单,
####入门
Template类是创建模板和渲染模板的核心类  

    from mako.template import Template
    mytemplate = Template("hello world")
    print mytemplate.render()

Template方法的参数会编译成一个Python模块来处理.这个模块包含一个函数`render_body()`,模块的输出结果就是这个方法返回的.下面就是"hello ${name}"编译后的module.

    # -*- encoding:ascii -*-
    from mako import runtime, filters, cache
    UNDEFINED = runtime.UNDEFINED
    __M_dict_builtin = dict
    __M_locals_builtin = locals
    _magic_number = 8
    _modified_time = 1385541516.897274
    _enable_loop = True
    _template_filename = 'hello.txt'
    _template_uri = 'hello.txt'
    _source_encoding = 'ascii'
    _exports = []
    
    
    def render_body(context,**pageargs):
        __M_caller = context.caller_stack._push_frame()
        try:
            __M_locals = __M_dict_builtin(pageargs=pageargs)
            name = context.get('name', UNDEFINED)
            __M_writer = context.writer()
            # SOURCE LINE 1
            __M_writer(u'hello ')
            __M_writer(unicode(name))
            __M_writer(u'\n')
            return ''
        finally:
            context.caller_stack._pop_frame()



调用render()方法时,mako会创建一个Context对象,context对象存储了模板中的变量名.此外还存储了一个缓冲buffer,用于捕获输出结果.如果你要自定义一个Context,那么就要调用render_context()方法渲染模板.  

    from mako.template import Template
    from mako.runtime import Context
    from StringIO import StringIO
    
    mytemplate = Template("hello, ${name}")
    buf = StringIO()
    ctx = Context(buf, name='jack')
    mytemplate.render_context(ctx)
    print buf.getvalue()

Template也可以加载文件模板,使用关键字参数`filename`  

    from mako.template import Template
    mytemplate = Template(filename='/docs/mytmpel.mako')
    print mytemplate.render()

为了提高性能,你还以添加参数module_directory='/tmp/moudle',指定生成的模块持久存储在文件系统中.  

    from mako.template import Template
    
    mytemplate = Template(filename='/docs/mytmpl.txt', module_directory='/tmp/mako_modules')
    print mytemplate.render()

####语法
mako模板可以从xml,html,email等任何类型的字符流文件.模板文件可以包含mako指定的指令,如:变量,表达式,控制结构体(条件控制/循环控制),服务端注释,python代码,还有各种标签.所有这些最终都会编译成python代码,  
#####表达式替换
最简单的表达式就是变量替换,语法是`${}`  

    this is x:${x}

#####表达式转义
mako拥有内建的转义机制,有针对html,url和xml的转义还有trim函数,这些转义符号可以用`|`操作符追加在替换表达式后面  

    ${"this is some text" | u}
输出 `this+is+some+text`,`u`代表url转义,而`h`代表html转义,`x`代表xml转义,`trim`代表trim函数,用于去掉字符串两边的空格,`n`表示不对html转义    

#####控制结构
控制结构的语法都是以`%<name>`开头,以`%end<name>`结尾
**if**  

    % if x==5:
        this is some output
    % endif
**for**  

    % for a in ['one', 'two', 'three', 'four', 'five']:
        % if a[0] == 't':
        its two or three
        % elif a[0] == 'f':
        four/five
        % else:
        one
        % endif
    % endfor
在for循环中有个`loop`上下文,它提供了很多额外的信息,比如:  

    <ul>
    % for a in ("one", "two", "three"):
        <li>Item ${loop.index}: ${a}</li>
    % endfor
    </ul>
loop.index显示当前的迭代的索引位置,index的起始为0  

#####注释
单行注释: mako 以两个`#`作为注释  

    ## this is a comment.
多行注释:  

    <%doc>
        these are comments
        more comments
    </%doc>
#####换行符
mako 和python 一样一反斜缸`\\`做为换行符     

    more and more people \
    go home 
    等价于:
    more and more people go home

#####python代码块
mako中嵌入python代码块时,使用标签`<%`和`%>`  

    <% 
    ##这里就是python代码块
    x = 10000
    y = x
    %>
    
    y = ${y}
这里的python代码块是位于模板中的渲染函数中的,如果是模块级别的代码,比如,函数,那就要用下面这个:  

#####模块级别代码快
模块级代码块用`<!%`和 `%>` 就多一个感叹号   

    <%!
        import mylib
        import re
    
        def filter(text):
            return re.sub(r'^@', '', text)
    %>
这里的filter函数就是与渲染函数是平级的了.模块级代码块可以存在mako中的任何位置,可以出现任意次数,最终渲染会按照声明的顺序合并在一块.  

####标签
mako提供了很多标签,如:include, def ,page等等,她的写法是:`<%name>`开头,结尾是`/>`或者`</%name>`,比如:  

    <%include file="foo.txt"/>
    <%def name="foo" buffered="True">
        this is a def
    </%def>

标签都有属性,有些属性是必须的,同时属性还支持赋值,所以你也可以使用表达式给属性赋值. 如:  

    <%include file="/foo/bar/${myfile}.txt"/>

#####<%include>
在mako文件中可以用include标签包含另外一个文件进来,比如所有页面都应该有header.html和footer.html,就可以把这两部分提取出来.  

    <%include file="header.html"/>
    
        hello world
    
    <%include file="footer.html"/>

`include`标签还有一个`args`的参数,用来传递值给被包含的文件中去.它与标签`<%page`相对应.  

    <%include file="toolbar.html" args="current_section='members', username='ed'"/>
#####<%page>

    <%page args="x, y, z='default'"/>
    <%page cached="True" cache_type="memory"/> 
目前,在一个模板中只能存在一个page标签,其他的会被忽略.且page标签不能放在其他标签里面,如放在block标签里面的,就读不到args设定的值.  
#####<%def>
def标签定义了一个python函数,它包含一些内容,可以在其他地方调用.  

    <%def name="myfunc(x)">
        this is myfunc, x is ${x}
    </%def>
    
    ${myfunc(19)}
#####<%block>
block 可以对这块区域代码执行制定的操作,比如:  

    <%block filter="h">
        some <html> stuff.
    </%block>
对文本`some <html> stuff`执行过滤操作.,block可以没有名字, 更常用的一种方式是用在继承上,比如定义个base.html:  

    ##base.html
    <html>
        <body>
        <%block name="header">
            <h2><%block name="title"/></h2>
        </%block>
        ${self.body()}
        </body>
    </html>

然后你就可以在其它页面继承base.html,block区别可以被继承者覆盖掉 如:  

    ## index.html
    <%inherit file="base.html"/>
    
    <%block name="header">
        this is some header content
    </%block>





