#Django1.5自定义User模型
Django1.5自定义用户profile可谓简单很多，编写自己的model类MyUser，MyUser至少要满足如下要求：

 1. 必须有一个整型的主键
 2. 有一个唯一性约束字段，比如username或者email，用来做用户认证
 3. 提供一种方法以“short”和“long"的形式显示user，换种说法就是要实现
    get\_full\_name和get\_short\_name方法。

###一：在project中创建一个account app

    django-admin startapp account

###二：自定义MyUser

实现自定义User模型最简单的方式就是继承AbstractBaseUser，AbstractBaseUser实现了User的核心功能，你只需对一些额外的细节进行实现就可以了。可以看看AbstractBaseUser的源码：

    @python_2_unicode_compatible
    class AbstractBaseUser(models.Model):
        password = models.CharField(_('password'), max_length=128)
        last_login = models.DateTimeField(_('last login'), default=timezone.now)
    
        is_active = True
    
        REQUIRED_FIELDS = []
    
        class Meta:
            abstract = True
    
        def get_username(self):
            "Return the identifying username for this User"
            return getattr(self, self.USERNAME_FIELD)
    
        def __str__(self):
            return self.get_username()
    
        def natural_key(self):
            return (self.get_username(),)
    
        def is_anonymous(self):
            """
            Always returns False. This is a way of comparing User objects to
            anonymous users.
            """
            return False
    
        def is_authenticated(self):
            """
            Always return True. This is a way to tell if the user has been
            authenticated in templates.
            """
            return True
    
        def set_password(self, raw_password):
            self.password = make_password(raw_password)
    
        def check_password(self, raw_password):
            """
            Returns a boolean of whether the raw_password was correct. Handles
            hashing formats behind the scenes.
            """
            def setter(raw_password):
                self.set_password(raw_password)
                self.save(update_fields=["password"])
            return check_password(raw_password, self.password, setter)
    
        def set_unusable_password(self):
            # Sets a value that will never be a valid hash
            self.password = make_password(None)
    
        def has_usable_password(self):
            return is_password_usable(self.password)
    
        def get_full_name(self):
            raise NotImplementedError()
    
        def get_short_name(self):
            raise NotImplementedError()

AbstractBaseUser只有get\_full\_name和get\_short\_name方法没有实现了。接下来我们就通过继承AbstractBaseUser来自定义User模型叫MyUser：

    class MyUser(AbstractBaseUser, PermissionsMixin):
        username = models.CharField('username', max_length=30, unique=True,
                                    db_index=True)
        email = models.EmailField('email address',max_length=254, unique=True)
        date_of_birth = models.DateField('date of birth', blank=True, null=True)
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['username']
    
        is_staff = models.BooleanField('staff status', default=False,
            help_text='Designates whether the user can log into this admin '
                  'site.')
        is_active = models.BooleanField('active', default=True,
            help_text='Designates whether this user should be treated as '
                   'active. Unselect this instead of deleting accounts.')
    
        def get_full_name(self):
            full_name = '%s %s' % (self.first_name, self.last_name)
            return full_name.strip()
    
        def get_short_name(self):
            return self.first_name
    
        objects = MyUserManager()

* USERNAME_FIELD ：作为用户登录认证用的字段，可以usename，或者email等，但必须是唯一的。
* REQUIRED_FIELDS ：使用createsuperuser命令创建超级用户时提示操作者输入的字段
* is_staff ：判断用户是否可以登录管理后台
* is_active ：判断用户是否可以正常登录
    
###三：自定义MyUserManager
同时要为MyUser自定义个一个manager，通过继承BaseUserManager，提供creat_user和create_superuser方法。

    class MyUserManager(BaseUserManager):
        def create_user(self, username, email=None, password=None, **extra_fields):
            now = timezone.now()
            if not email:
                raise ValueError('The given email must be set')
            email = UserManager.normalize_email(email)
            user = self.model(username=username, email=email,
                               is_staff=False, is_active=True, is_superuser=False,
                               last_login=now, **extra_fields)
    
            user.set_password(password)
            user.save(using=self._db)
            return user
    
        def create_superuser(self, username, email, password, **extra_fields):
            u = self.create_user(username, email, password, **extra_fields)
            u.is_staff = True
            u.is_active = True
            u.is_superuser = True
            u.save(using=self._db)
            return u

###四：指定AUTH\_USER\_MODEL

覆盖默认的AUTH\_USER\_MODEL，在settings.py文件中增加：
  
	AUTH_USER_MODEL = 'user.MyUser'

###五：注册MyUser

在account模块下创建admin.py，添加如下代码把MyUser模型注册到admin中：

    from django.contrib import admin
    from user.models import MyUser
    admin.site.register(MyUser)

总结：实现自定义的User模型在Django1.5足够简单方便，根据自己需求继承AbstractBaseUser就可以了。当然如果你想了解更多关于Django 自定义用户模型相关内容，官方文档告诉你更多更好的完好

如果你有什么建议和问题欢迎留言。