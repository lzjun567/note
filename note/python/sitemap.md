Django SiteMap
==================
首先`django.contrib.sitemaps`添加到`INSTALLED_APPS`，sitemaps会利用模版加载器`django.template.loaders.app_directories.Loader`加载的模版。默认情况下，这个加载器已经存在django的global_settings.py文件中的。  

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        #'django.template.loaders.eggs.Loader',
    )

以前介绍过一篇[文章](http://foofish.net/blog/63/django-compressor)有个参数叫STATICFILES_FINEDERS，也有类似的两个模块是：  

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
    )
接下来就是配置URL：  

    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})  

####Sitemap class
一个Sitemap类代表model里面一个实体类的部分，这部分最终会出现在sitemap.xml中的。下面就是一个简单的sitemap类，他会显示满足条件is_public=True和status=p的blog。  

    #!encoding=utf-8
    
    from django.contrib.sitemaps import Sitemap 
    from apps.blog.models import Blog 
    
    class BlogSitemap(Sitemap):
        changefreq = "weekly"
        priority = 0.5
    
        def items(self):
            return Blog.objects.filter(is_public=True).filter(status='p')
    
        def lastmod(self, obj):
            return obj.update_time

因为sitemap.xml显示的都是每个blog的url，因此BlogSitemap还有一个方法叫location()，用来定义blog的url的，默认这个方法会调用blog的get_absolute_url()方法，如果你的blog类没有实现这个方法那么在访问/sitemap.xml的就会出错了。  

    AttributeError at /sitemap.xml
    'Blog' object has no attribute 'get_absolute_url'
    Request Method:	GET
    Request URL:	http://localhost:8000/sitemap.xml

因此自己来实现location方法  

    def location(self, obj):
        return  r'/blog/%d/%s' % (obj.id, obj.link)
现在访问http://localhost:8000/sitemap.xml，你就能正常查看到sitemap了。  

    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
    <loc>
    http://localhost:8000/blog/1/personal-blog-based-django-and-bootstrap
    </loc>
    <lastmod>2014-03-20</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.5</priority>
    </url>
    </urlset>

 
