Python中的Enum
================
Enum（枚举）在很多应用场景中都会出现，因此绝大部分编程语言都实现了Enum类型，Python也不列外，但列外的是Enum在Python3.4中才被正式支持，我们先来看看Python3中的Enum是怎么使用的。  
枚举的创建方式很简单，就像创建一个类一样，只需继承Enum：   
    
    >>> from enum import Enum
    >>> class Role(Enum):
    ...     admin = 1
    ...     manager = 2
    ...     guest = 3

它的语法和定义`class`完全是一样的，但它并不是一个真正的class。这里的`Role`是Enum类型，里面的成员`admin`,`manager`都是它的实例对象，它们的类型是`Role`类型的：  
    
    >>> type(Role)
    <class 'enum.EnumMeta'>
    >>> type(Role.admin)
    <enum 'Role'>
    >>>

枚举的每一个实例对象都有自己的名字和值：  
    
    >>> Role.admin.name
    'admin'
    >>> Role.admin.value
    1

枚举内部更像是一个OrderedDict：  
    
    Role.__members__
    mappingproxy(OrderedDict([('admin', <Role.admin: 1>), ('manager', <Role.manager: 2>), ('guest', <Role.guest: 3>)]))
    >>>

Python2.x：  
    
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    
    __author__ = 'liuzhijun'
    
    def enum(name, *sequential, **named):
        values = dict(zip(sequential, range(len(sequential))), **named)
        values['values'] = values.values()
        # NOTE: Yes, we *really* want to cast using str() here.
        # On Python 2 type() requires a byte string (which is str() on Python 2).
        # On Python 3 it does not matter, so we'll use str(), which acts as
        # a no-op.
        # return type(str(name), (), values)
        import collections
        aa = collections.namedtuple(str(name), values.keys())
        return aa(**values)
    
    
    JobStatus = enum(
        'JobStatus',
        QUEUED='queued',
        FINISHED='finished',
        FAILED='failed',
        STARTED='started',
        DEFERRED='deferred'
    )
    
    print JobStatus.QUEUED
    print JobStatus.FAILED
    print JobStatus.STARTED
    print JobStatus._fields
    print JobStatus.values