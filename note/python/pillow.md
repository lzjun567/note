Pillow
=================
Pillow 是从PIL上面fork下来的，因为PIL自从2009年就再没有更新过了，Pillow由作者Alex Clark和其他一些contributors一起维护，算是一个更好用的PIL，它能对图片文件进行各种操作。本文不再介绍如何安装了，本博客之前曾写过一篇文章《[使用django-simple-captcha遇到的坑](http://foofish.net/index.php/%E4%BD%BF%E7%94%A8django-simple-captcha%E9%81%87%E5%88%B0%E7%9A%84%E5%9D%91/)》，这篇主要介绍如何使用Pillow。  

####理解Image类
Pillow库中最重要的类就是Image类，Image类定义在pil模块下，有多种方式来创建一个Image实例，比如：通过加载图片文件生成或者通过处理其他image返回Image实例，还可以通过屏幕抓取的方式获取Image实例。  

使用open()函数从文件中加载返回一个image  

    from PIL import Image
    im = Image.open('Lenna.jpg')
    print im
    print(im.format, im.size, im.mode)

输出：  

    <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=400x400 at 0x26247B0>
    ('JPEG', (400, 400), 'RGB')
创建了Image实例后你就可以通过某些方法操作图片了，例如im.show()可以显示图片。  

####读写图片文件
读文件时，直接调用open()从磁盘中读取，你并不需要知道文件的格式，Pillow会基于文件的内容判断文件的格式，保存文件时直接调用save()方法，pillow直接根据文件名的扩展名作为文件的格式，除非你明确指定其格式。  
#####格式转换

    import os.path
    infile = "/Lenna.jpg"
    f, e = os.path.silitext(infile)
    outfile = f + ".png"
    try:
        Image.open(infile).save(outfile)
    except IOError:
        print("cannot convert"+infile)

如果你的扩展名是非标准的，那么你就需要明确指定其格式。  

#####创建缩略图

    import os.path
    infile = "/Lenna.jpg"
    outfile = os.path.splitext(infile)[0]+".thumbnail"  #这个就是一个非标准的文件格式
    size = (128,128)
    
    try:
        im = Image.open(infile)
        im.thumbnail(size)
        im.save(outfile, "JPEG")  #因为oufile不是标准的文件格式，那么这里明确指定其格式
    excep IOError:
        print("cannot create thumbnail for",infile)



