Mako 模板语言
-------------------
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
输出 `this+is+some+text`,`u`代表url转义,而`h`代表html转义,`x`代表xml转义,`trim`代表trim函数,用于去掉字符串两边的空格.  

#####控制结构
