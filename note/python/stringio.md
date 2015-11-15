StringIO
===============================
StringIO是一个类文件（file-like）对象，真正的文件对象最终会映射到磁盘，而StringIO是一个和file对象有类似行为的内存文件对象。当有些操作要求是文件对象时，而你并不希望给出真实的文件对象时，此时你可以使用StringIO来替换。比如：GzipFile构造方法接收参数类型就是文件类型。StringIO就可以派上用场了 

    import gzip
    import StringIO

    file = StringIO.StringIO()
    gzip_file = gzip.GzipFile(fileobj=file, mode='w')
    gzip_file.write('hello world')
    gzip_file.close()

    print stringio.getvalue()  #此方法必须是在stringio.close()调用前，否则ValueError

再比如：  
    
    import StringIO
    MESSAGE =  “this is amazing game”
    file = StringIO.StringIO(MESSAGE)
    print file.read()

###cStringIO：性能更高的StringIO
cStringIO是一个速度更快的StringIO，其接口与StringIO基本类似，但是有以下区别：  
1. 不能构建任何版本的子类，因为它的构造方法返回的是一个built-in类型

        #coding:utf-8
        import StringIO
        
        stringio = StringIO.StringIO(u'helloworld我是')
        print type(stringio)    #<type 'instance'>
        stringio.size = 10      #可以给实例赋任何属性
        print stringio.getvalue()
        
        import cStringIO
        cs = cStringIO.StringIO(u'helloworld')
        print type(cs) #<type 'cStringIO.StringI'>
        cs.size = 10   #此处会报错，因为cStringIO.StringIO没有属性size
        print cs.getvalue()
2. cStringIO不接收中文unicode字符

        cs = cStringIO.StringIO(u'helloworldi我是')
        #异常
        Traceback (most recent call last):
          File "test.py", line 10, in <module>
            cs = cStringIO.StringIO(u'helloworldi鎴戞槸')
        UnicodeEncodeError: 'ascii' codec can't encode characters in position 11-12: ordinal not in range(128)

####python3 StringIO
python3去掉了StringIO和cStringIO模块，取而代之的是io.StringIO，要写出兼容py2和py3的代码的话，使用：

    try:
        from cStringIO import StringIO  # py2
    except ImportError:
        from io import StringIO  # py3
