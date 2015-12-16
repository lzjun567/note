Python列表对象实现原理
===================
Python中的列表基于PyListObject实现，列表支持元素的插入、删除、更新操作，因此PyListObject是一个变长对象（列表的长度随着元素的增加和删除而变长和变短），同时它还是一个可变对象（列表中的元素根据列表的操作而发生变化，内存大小动态的变化），PyListObject的定义：  
```python
typedef struct {
	# 列表对象引用计数
    int ob_refcnt;  
    # 列表类型对象      
	struct _typeobject *ob_type;
	# 列表元素的长度
    int ob_size; /* Number of items in variable part */
    # 真正存放列表元素容器的指针，list[0] 就是 ob_item[0]
    PyObject **ob_item;
    # 当前列表可容纳的元素大小
    Py_ssize_t allocated;
} PyListObject;
```
	
咋一看PyListObject对象的定义非常简单，除了通用对象都有的引用计数（ob\_refcnt）、类型信息（ob\_type），以及变长对象的长度（ob\_size）之外，剩下的只有ob\_item，和allocated，ob\_item是真正存放列表元素容器的指针，专门有一块内存用来存储列表元素，这块内存的大小就是allocated所能容纳的空间。alloocated是列表所能容纳的元素大小，而且满足条件： 

- 0 <= ob_size <= allocated
- len(list) == ob_size
- ob\_item == NULL 时 ob_size == allocated == 0  

![pylistobject](http://7lryy3.com1.z0.glb.clouddn.com/pylistobject.jpg)

####列表对象的创建
PylistObject对象的是通过函数PyList\_New创建而成，接收参数**size**，该参数用于指定列表对象所能容纳的最大元素个数。  
```python
// 列表缓冲池, PyList_MAXFREELIST为80
static PyListObject *free_list[PyList_MAXFREELIST];
//缓冲池当前大小
static int numfree = 0;

PyObject *PyList_New(Py_ssize_t size)
{
    PyListObject *op; //列表对象
    size_t nbytes;    //创建列表对象需要分配的内存大小

    if (size < 0) {
        PyErr_BadInternalCall();
        return NULL;
    }
    /* Check for overflow without an actual overflow,
     *  which can cause compiler to optimise out */
    if ((size_t)size > PY_SIZE_MAX / sizeof(PyObject *))
        return PyErr_NoMemory();
    nbytes = size * sizeof(PyObject *);
    if (numfree) {
        numfree--;
        op = free_list[numfree];
        _Py_NewReference((PyObject *)op);

    } else {
        op = PyObject_GC_New(PyListObject, &PyList_Type);
        if (op == NULL)
            return NULL;

    }
    if (size <= 0)
        op->ob_item = NULL;
    else {
        op->ob_item = (PyObject **) PyMem_MALLOC(nbytes);
        if (op->ob_item == NULL) {
            Py_DECREF(op);
            return PyErr_NoMemory();
        }
        memset(op->ob_item, 0, nbytes);
    }
    # 设置ob_size
    Py_SIZE(op) = size;
    op->allocated = size;
    _PyObject_GC_TRACK(op);
    return (PyObject *) op;
}
```
创建过程大致是：  

1. 检查size参数是否有效，如果小于0，直接返回NULL，创建失败
2. 检查size参数是否超出Python所能接受的大小，如果大于PY\_SIZE\_MAX（64位机器为8字节，在32位机器为4字节），内存溢出。
3. 检查缓冲池free\_list是否有可用的对象，有则直接从缓冲池中使用，没有则创建新的PyListObject，分配内存。
4. 初始化ob\_item中的元素的值为Null
5. 设置PyListObject的allocated和ob\_size。

####PyListObject对象的缓冲池
free\_list是PyListObject对象的缓冲池，其大小为80，那么PyListObject对象是什么时候加入到缓冲池free\_list的呢？答案在list\_dealloc方法中：  
```python
static void
list_dealloc(PyListObject *op)
{
    Py_ssize_t i;
    PyObject_GC_UnTrack(op);
    Py_TRASHCAN_SAFE_BEGIN(op)
    if (
        i = Py_SIZE(op);
        while (--i >= 0) {
            Py_XDECREF(op->ob_item[i]);
        }
        PyMem_FREE(op->ob_item);
    }
    if (numfree < PyList_MAXFREELIST && PyList_CheckExact(op))
        free_list[numfree++] = op;
    else
        Py_TYPE(op)->tp_free((PyObject *)op);
    Py_TRASHCAN_SAFE_END(op)
}
```
当PyListObject对象被销毁的时候，首先将列表中所有元素的引用计数减一，然后释放ob\_item占用的内存，只要缓冲池空间还没满，那么就把该PyListObject加入到缓冲池中（此时PyListObject占用的内存并不会正真正回收给系统，下次创建PyListObject优先从缓冲池中获取PyListObject），否则释放PyListObject对象的内存空间。

####列表元素插入
设置列表某个位置的值时，如“list[1]=0”，列表的内存结构并不会发生变化，而往列表中插入元素时会改变列表的内存结构：   
```python
static int
ins1(PyListObject *self, Py_ssize_t where, PyObject *v)
{
	// n是列表元素长度
    Py_ssize_t i, n = Py_SIZE(self);
    PyObject **items;
    if (v == NULL) {
        PyErr_BadInternalCall();
        return -1;
    }
    if (n == PY_SSIZE_T_MAX) {
        PyErr_SetString(PyExc_OverflowError,
            "cannot add more objects to list");
        return -1;
    }

    if (list_resize(self, n+1) == -1)
        return -1;

    if (where < 0) {
        where += n;
        if (where < 0)
            where = 0;
    }
    if (where > n)
        where = n;
    items = self->ob_item;
    for (i = n; --i >= where; )
        items[i+1] = items[i];
    Py_INCREF(v);
    items[where] = v;
    return 0;
}
```

相比设置某个列表位置的值来说，插入操作要多一次PyListObject容量大小的调整，逻辑是list\_resize，其次是挪动where之后的元素位置。  
```python
// newsize： 列表新的长度
static int  
list_resize(PyListObject *self, Py_ssize_t newsize)
{
    PyObject **items;
    size_t new_allocated;
    Py_ssize_t allocated = self->allocated;

    
    if (allocated >= newsize && newsize >= (allocated >> 1)) {
        assert(self->ob_item != NULL || newsize == 0);
        Py_SIZE(self) = newsize;
        return 0;
    }

    new_allocated = (newsize >> 3) + (newsize < 9 ? 3 : 6);

    /* check for integer overflow */
    if (new_allocated > PY_SIZE_MAX - newsize) {
        PyErr_NoMemory();
        return -1;
    } else {
        new_allocated += newsize;
    }

    if (newsize == 0)
        new_allocated = 0;
    items = self->ob_item;
    if (new_allocated <= (PY_SIZE_MAX / sizeof(PyObject *)))
        PyMem_RESIZE(items, PyObject *, new_allocated);
    else
        items = NULL;
    if (items == NULL) {
        PyErr_NoMemory();
        return -1;
    }
    self->ob_item = items;
    Py_SIZE(self) = newsize;
    self->allocated = new_allocated;
    return 0;
}
```

满足 `allocated >= newsize && newsize >= (allocated /2)`时，简单改变list的元素长度，PyListObject对象不会重新分配内存空间，否则重新分配内存空间，如果`newsize<allocated/2`，那么会减缩内存空间，如果`newsize>allocated`，就会扩大内存空间。当`newsize==0`时内存空间将缩减为0。 

![!python_list_resize](http://7lryy3.com1.z0.glb.clouddn.com/python_list_resize.jpg)

####总结
* PyListObject缓冲池的创建发生在列表销毁的时候。
* PyListObject对象的创建分两步：先创建PyListObject对象，然后初始化元素列表为NULL。
* PyListObject对象的销毁分两步：先销毁PyListObject对象中的元素列表，然后销毁PyListObject本身。
* PyListObject对象内存的占用空间会根据列表长度的变化而调整。

参考：  

* [listobject.h](https://github.com/lzjun567/python2.7/blob/master/Include/listobject.h)
* [listobject.c](https://github.com/lzjun567/python2.7/blob/master/Objects/listobject.c)