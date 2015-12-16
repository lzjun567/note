Python 整数对象实现原理
==================
整数对象在Python内部用`PyIntObject`结构体表示：  
```c
typedef struct {
    PyObject_HEAD
    long ob_ival;
} PyIntObject;
```
PyObject_HEAD宏中定义的两个属性分别是：  
```c
int ob_refcnt;        
struct _typeobject *ob_type;
 ```

 这两个属性是所有Python对象固有的：  

 * ob_refcnt：对象的引用计数，与Python的内存管理机制有关，它实现了基于引用计数的垃圾收集机制
 * ob_type：用于描述Python对象的类型信息。  

由此看来PyIntObject就是一个对C语言中long类型的数值的扩展，出于性能考虑,对于小整数，Python使用小整数对象池`small_ints`缓存了[-5，257）之间的整数，该范围内的整数在Python系统中是共享的。  
```c
#define NSMALLPOSINTS           257
#define NSMALLNEGINTS           5
static PyIntObject *small_ints[NSMALLNEGINTS + NSMALLPOSINTS];
```
![pythonblock_small_int](http://7lryy3.com1.z0.glb.clouddn.com/pythonblock_small_int.png)  

而超过该范围的整数即使值相同，但对象不一定是同一个，如下所示：当a与b的值都是10000，但并不是同一个对象，而值为1的时候，a和b属于同一个对象。
```python
>>> a = 10000
>>> b = 10000
>>> print a is b
False
>>> a = 1
>>> b = 1
>>> print a is b
True
```

对于超出了[-5, 257)之间的其他整数，Python同样提供了专门的缓冲池，供这些所谓的大整数使用，避免每次使用的时候都要不断的malloc分配内存带来的效率损耗。这块内存空间就是`PyIntBlock`。  
```c
struct _intblock {

    struct _intblock *next;
    PyIntObject objects[N_INTOBJECTS];
};
typedef struct _intblock PyIntBlock;

static PyIntBlock *block_list = NULL;
static PyIntObject *free_list = NULL;
```
这些内存块（blocks）由一个单向链表表示，表头是`block_list`，`block_list`始终指向最新创建的PyIntBlock对象。next指针指向下一个PyIntBlock对象，objects是一个PyIntObject数组（最终会转变成单向链表），它是真正用于存储被缓存的PyIntObjet对象的内存空间。 
`free_list`单向链表是所有block的objects中空闲的内存。所有空闲内存通过一个链表组织起来的好处就是在Python需要新的内存来存储新的PyIntObject对象时，能够通过`free_list`快速获得所需的内存。

![python int blcik](http://7lryy3.com1.z0.glb.clouddn.com/python_int_block.jpg)


创建一个整数对象时，如果它在小整数范围内，就直接从小整数缓冲池中直接返回，如果不在该范围内，就开辟一个大整数缓冲池内存空间：  
```c
[intobject.c]
PyObject* PyInt_FromLong(long ival)
{
     register PyIntObject *v; 
#if NSMALLNEGINTS + NSMALLPOSINTS > 0
     //[1] ：尝试使用小整数对象池
     if (-NSMALLNEGINTS <= ival && ival < NSMALLPOSINTS) {
        v = small_ints[ival + NSMALLNEGINTS];
        Py_INCREF(v);
        return (PyObject *) v;
    }
#endif
    //[2] ：为通用整数对象池申请新的内存空间
    if (free_list == NULL) {
        if ((free_list = fill_free_list()) == NULL)
            return NULL;
    }
    //[3] : (inline)内联PyObject_New的行为
    v = free_list;
    free_list = (PyIntObject *)v->ob_type;
    PyObject_INIT(v, &PyInt_Type);
    v->ob_ival = ival;
    return (PyObject *) v;
}
```
`fill_free_list`就是创建大整数缓冲池内存空间的逻辑，该函数返回一个`free_list`链表，当整数对象ival创建成功后，`free_list`表头就指向了`v->ob_type`，`ob_type`不是所有Python对象中表示类型信息的字段吗？怎么在这里作为一个连接指针呢？这是Python在性能与代码优雅之间取中庸之道，对名称的滥用，放弃了对类型安全的坚持。把它理解成指向下一个PyIntObject的指针即可。  
```c
[intobject.c]
static PyIntObject* fill_free_list(void)
{
    PyIntObject *p, *q;
    // 申请大小为sizeof(PyIntBlock)的内存空间
    // block list始终指向最新创建的PyIntBlock
    p = (PyIntObject *) PyMem_MALLOC(sizeof(PyIntBlock));
    ((PyIntBlock *)p)->next = block_list;
    block_list = (PyIntBlock *)p;

    //：将PyIntBlock中的PyIntObject数组(objects)转变成单向链表
    p = &((PyIntBlock *)p)->objects[0];
    q = p + N_INTOBJECTS;
    while (--q > p)
    	// ob_type指向下一个未被使用的PyIntObject。
        q->ob_type = (struct _typeobject *)(q-1);
    q->ob_type = NULL;
    return p + N_INTOBJECTS - 1;
}
```
不同的PyIntBlock里面的空闲的内存是怎样连接起来构成`free_list`的呢？这个秘密放在了整数对象垃圾回收的时候，在PyIntObject对象的tp_dealloc操作中可以看到：  
```c	
[intobject.c]
static void int_dealloc(PyIntObject *v)
{
    if (PyInt_CheckExact(v)) {
        v->ob_type = (struct _typeobject *)free_list;
        free_list = v;
    }
    else
        v->ob_type->tp_free((PyObject *)v);
}
```
原来PyIntObject对象销毁时，它所占用的内存并不会释放，而是继续被Python使用，进而将`free_list`表头指向了这个要被销毁的对象上。   

####总结
* Python中的int对象就是c语言中long类型数值的扩展  
* 小整数对象[-5, 257]在python中是共享的
* 整数对象都是从缓冲池中获取的。
* 整数对象回收时，内存并不会归还给系统，而是将其对象的ob_type指向free_list，供新创建的整数对象使用

参考：[intobject.c](https://github.com/lzjun567/python2.7/blob/master/Objects/intobject.c)