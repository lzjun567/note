StringIO---像文件一样读写字符串
===============================
有些API仅接受文件对象，但是你只有一个字符串，比如使用gzip模块压缩字符串的时候，StringIO就可以派上用场了 

    import gzip
    import StringIO

    stringio = StringIO.StringIO()
    gzip_file = gzip.GzipFile(fileobj=stringio, mode='w')
    gzip_file.write('hello world')
    gzip_file.close()

    print stringio.getvalue()  #此方法必须是在stringio.close()调用前，否则ValueError

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
        cs.size = 10   #此处会报错，因为cStringIO.StringI没有属性size
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
