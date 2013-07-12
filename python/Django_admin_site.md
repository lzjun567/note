###使用Django admin模块，必须：  
1. 添加`django.contrib.admin` 到`INSTALLED_APPS`中  
2. admin依赖的app包括：`django.contrib.auth`,`django.contrib.contenttypes`,`django.contrib.messages`和`django.contrib.sessions`
3. 添加`django.contrib.messages.context_processors.messsags`到`TEMPLATE_CONTEXT_PROCESSORS`
4. 添加`django.contrib.auth.middleware.AuthenticateionMiddleware`和`django.contrib.messages.middleware.MessageMiddleware`,`到MIDDLEWARE_CLASS`

###ModelAdmin.actions

自定义action函数和普通函数没啥区别，需要是三个参数：当前的 ModelAdmin，当前的HttpRequest，用户说选中的QuerySet  

    def make_publiced(modleadmin,request,queryset):
        queryset.update(public=False)

直接调用queryset的update比逐个迭代entity更高效。默认action的下拉列表显示的名字就是函数名`make_publiced`,但是你可以起一个更优雅的名字：

    make_publiced.short_description = u"标记为公开"

最后一步就是告诉modelaction

    actions = ['make_publiced']

以上就是你需要做的全部
https://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/
