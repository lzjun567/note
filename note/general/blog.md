#博客优化
最近对我的博客[http://foofish.net](http://foofish.net/)进行了一次性能优化，主要是针对前端部分，从如下几个方面进行，基本原则参照《构建高性能Web站点》这本书。

####使用CDN
对于公有的静态资源，比如jquery.min.js、highlight.min.js等文件全部使用CDN，提高网站的访问速度。

####合并静态文件

整个网站的css和js文件总共超过10个，如果等浏览器全部加载完这些文件大概需要3秒以上，如果是比较的网络环境体验可能更糟糕。因此在部署的时候把多个CSS文件合并成一个，JS合并的一个文件，使用的工具是[Django-Compressor](http://foofish.net/blog/63/django-compressor)。合并后用Google的PageSpeed工具体检网站得分是83。


####压缩静态文件
文件合并后，总大小没变化，因此还有优化的空间，因为像这种字符构成的静态文件压缩的比例是非常高的，通常可以压缩到原来的三分之一。压缩这块使用Nginx的gizp功能
	
	http {
		
		gzip on;
	    gzip_disable "msie6";

		gzip_vary on;
		gzip_proxied any;
		gzip_comp_level 6;
		gzip_buffers 4 8k;
		gzip_http_version 1.1;
		gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
	    
	    ..... 其他配置
	}

压缩后PageSpeed得分飙到了95分。

####使用浏览器缓存
如果服务端没有给静态资源指定过期时间，那么浏览器每次都要发送请求给服务器询问这些静态资源有没有更新，如果有更新就会返回完整的内容给浏览器，如果没有更新就告诉浏览器直接返回304，叫浏览器直接使用本地缓存。这里有一步骤显得多余，如果没有更新可以叫浏览器不发送请求，关于HTTP缓存可参考[HTTP缓存](http://foofish.net/blog/95/http-cache-policy)，直接读取浏览器本地的缓存副本就得了，这样一来又可以节省一次请求。配置nginx：

	location ~* ^.+\.(css|js|txt|xml|swf|wav)$ {
	    access_log   off;
	    expires      7d;
	    add_header Cache-Control private;
	}
