#Django QA

* 如何在模板中获取网站的域名
	
		{{ request.META.HTTP_HOST }}

* model查询比较主键时，django提供了一个快捷方式`pk`，如果主键的名字是`id`

	等于操作，三种方式等同：
		
		>>> Blog.objects.get(id__exact=14) # Explicit form   
		>>> Blog.objects.get(id=14) # __exact is implied
		>>> Blog.objects.get(pk=14) # pk implies id__exact
	in 操作：

		>>> Blog.objects.filter(pk__in=[1,4,7])

	大于操作：

		>>> Blog.objects.filter(pk__gt=14)

	小于操作：

		>>> Blog.objects.filter(pk__lt=14)

* 模板中截取字符串可以用slice或者truncatechars或者truncatechars_html
		
		{{ value|truncatechars:9 }}
	效果：
		 "Joel is a slug" 变成 "Joel i...".
