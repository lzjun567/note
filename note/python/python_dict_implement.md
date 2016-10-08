Python 字典数据类型（dict）源码分析
================================
<<<<<<< HEAD
字典类型是Python中最常用的数据类型之一，它是一个键值对的集合，字典通过键来索引相应的值，理论上它的查询复杂度是 O(1) ：   
=======
字典类型是Python中最常用的数据类型之一，它是一个键值对的集合，字典通过键来索引，关联到相对的值，理论上它的查询复杂度是 O(1) ：   
>>>>>>> 8830afd4298ce03a3fec5980df8ffdcbd3665d2e
    
    >>> d = {'a': 1, 'b': 2}
    >>> d['c'] = 3
    >>> d
    {'a': 1, 'b': 2, 'c': 3}
在[字符串的实现原理](http://foofish.net/blog/91/python-str-implements)文章中，曾经出现过字典对象用于intern操作，那么字典的内部结构是怎样的呢？PyDictObject对象就是dict的内部实现。

####哈希表 (hash tables)
<<<<<<< HEAD
哈希表（也叫散列表），根据键值对(Key-value)而直接进行访问的数据结构。它通过把key和value映射到表中一个位置来访问记录，这种查询速度非常快，更新也快。而这个映射函数叫做哈希函数，存放值的数组叫做哈希表。 哈希函数的实现方式决定了哈希表的搜索效率。具体操作过程是：   
=======
哈希表（也叫散列表），根据关键值对(Key-value)而直接进行访问的数据结构。它通过把key和value映射到表中一个位置来访问记录，这种查询速度非常快，更新也快。而这个映射函数叫做哈希函数，存放值的数组叫做哈希表。 哈希函数的实现方式决定了哈希表的搜索效率。具体操作过程是：   
>>>>>>> 8830afd4298ce03a3fec5980df8ffdcbd3665d2e

1. 数据添加：把key通过哈希函数转换成一个整型数字，然后就将该数字对数组长度进行取余，取余结果就当作数组的下标，将value存储在以该数字为下标的数组空间里。  
2. 数据查询：再次使用哈希函数将key转换为对应的数组下标，并定位到数组的位置获取value。

但是，对key进行hash的时候，不同的key可能hash出来的结果是一样的，尤其是数据量增多的时候，这个问题叫做哈希冲突。如果解决这种冲突情况呢？通常的做法有两种，一种是链接法，另一种是开放寻址法，Python选择后者。

####开放寻址法（open addressing）
开放寻址法中，所有的元素都存放在散列表里，当产生哈希冲突时，通过一个探测函数计算出下一个候选位置，如果下一个获选位置还是有冲突，那么不断通过探测函数往下找，直到找个一个空槽来存放待插入元素。

####PyDictEntry
字典中的一个key\-value键值对元素称为entry（也叫做slots），对应到Python内部是PyDictEntry，PyDictObject就是PyDictEntry的集合。PyDictEntry的定义是：  
    
    typedef struct {
        /* Cached hash code of me_key.  Note that hash codes are C longs.
         * We have to use Py_ssize_t instead because dict_popitem() abuses
         * me_hash to hold a search finger.
         */
        Py_ssize_t me_hash;
        PyObject *me_key;
        PyObject *me_value;
    } PyDictEntry;
    
me\_hash用于缓存me\_key的哈希值，防止每次查询时都要计算哈希值，entry有三种状态。  

1. Unused：  me\_key == me\_value == NULL

    Unused是entry的初始状态，key和value都为NULL。插入元素时，Unused状态转换成Active状态。这是me\_key为NULL的唯一情况。
2. Active：  me\_key != NULL and me\_key != dummy 且 me\_value != NULL
    
    插入元素后，entry就成了Active状态，这是me\_value唯一不为NULL的情况，删除元素时Active状态刻转换成Dummy状态。
3. Dummy：  me\_key == dummy 且 me\_value == NULL
    
    此处的dummy对象实际上一个PyStringObject对象，仅作为指示标志。Dummy状态的元素可以在插入元素的时候将它变成Active状态，但它不可能再变成Unused状态。

为什么entry有Dummy状态呢？这是因为采用开放寻址法中，遇到哈希冲突时会找到下一个合适的位置，例如某元素经过哈希计算应该插入到A处，但是此时A处有元素的，通过探测函数计算得到下一个位置B，仍然有元素，直到找到位置C为止，此时ABC构成了探测链，查找元素时如果hash值相同，那么也是顺着这条探测链不断往后找，当删除探测链中的某个元素时，比如B，如果直接把B从哈希表中移除，即变成Unused状态，那么C就不可能再找到了，因为AC之间出现了断裂的现象，正是如此才出现了第三种状态---Dummy，Dummy是一种类似的伪删除方式，保证探测链的连续性。  
![python_entry_status](http://7lryy3.com1.z0.glb.clouddn.com/python_entry_status.jpg)

####PyDictObject
PyDictObject就是PyDictEntry对象的集合，PyDictObject的结构是：  
    
    typedef struct _dictobject PyDictObject;
    struct _dictobject {
        PyObject_HEAD
        Py_ssize_t ma_fill;  /* # Active + # Dummy */
        Py_ssize_t ma_used;  /* # Active */

        /* The table contains ma_mask + 1 slots, and that's a power of 2.
         * We store the mask instead of the size because the mask is more
         * frequently needed.
         */
        Py_ssize_t ma_mask;

        /* ma_table points to ma_smalltable for small tables, else to
         * additional malloc'ed memory.  ma_table is never NULL!  This rule
         * saves repeated runtime null-tests in the workhorse getitem and
         * setitem calls.
         */
        PyDictEntry *ma_table;
        PyDictEntry *(*ma_lookup)(PyDictObject *mp, PyObject *key, long hash);
        PyDictEntry ma_smalltable[PyDict_MINSIZE];
    };

* ma\_fill ：所有处于Active以及Dummy的元素个数
* ma\_used ：所有处于Active状态的元素个数
* ma\_mask ：所有entry的元素个数（Active+Dummy+Unused）
* ma\_smalltable：创建字典对象时，一定会创建一个大小为PyDict\_MINSIZE==8的PyDictEntry数组。
* ma\_table：当entry数量小于PyDict\_MINSIZE，ma\_table指向ma_smalltable的首地址，当entry数量大于8时，Python把它当做一个大字典来处理，此刻会申请额外的内存空间，同时将ma\_table指向这块空间。
* ma\_lookup：字典元素的搜索策略

PyDictObject使用PyObject\_HEAD而不是PyObject\_Var_HEAD，虽然字典也是变长对象，但此处并不是通过ob\_size来存储字典中元素的长度，而是通过ma\_used字段。

####PyDictObject的创建过程

    PyObject *
    PyDict_New(void)
    {
        register PyDictObject *mp;
        if (dummy == NULL) { /* Auto-initialize dummy */
            dummy = PyString_FromString("<dummy key>");
            if (dummy == NULL)
                return NULL;
        }
        if (numfree) {
            mp = free_list[--numfree];
            assert (mp != NULL);
            assert (Py_TYPE(mp) == &PyDict_Type);
            _Py_NewReference((PyObject *)mp);
            if (mp->ma_fill) {
                EMPTY_TO_MINSIZE(mp);
            } else {
                /* At least set ma_table and ma_mask; these are wrong
                   if an empty but presized dict is added to freelist */
                INIT_NONZERO_DICT_SLOTS(mp);
            }
            assert (mp->ma_used == 0);
            assert (mp->ma_table == mp->ma_smalltable);
            assert (mp->ma_mask == PyDict_MINSIZE - 1);
        } else {
            mp = PyObject_GC_New(PyDictObject, &PyDict_Type);
            if (mp == NULL)
                return NULL;
            EMPTY_TO_MINSIZE(mp);
        }
        mp->ma_lookup = lookdict_string;
        return (PyObject *)mp;
    }

1. 初始化dummy对象
2. 如果缓冲池还有可用的对象，则从缓冲池中读取，否则，执行步骤3
3. 分配内存空间，创建PyDictObject对象，初始化对象
4. 指定添加字典元素时的探测函数，元素的搜索策略

####字典搜索策略

    static PyDictEntry *
    lookdict(PyDictObject *mp, PyObject *key, register long hash)
    {
        register size_t i;
        register size_t perturb;
        register PyDictEntry *freeslot;
        register size_t mask = (size_t)mp->ma_mask;
        PyDictEntry *ep0 = mp->ma_table;
        register PyDictEntry *ep;
        register int cmp;
        PyObject *startkey;

        i = (size_t)hash & mask;
        ep = &ep0[i];
        if (ep->me_key == NULL || ep->me_key == key)
            return ep;

        if (ep->me_key == dummy)
            freeslot = ep;
        else {
            if (ep->me_hash == hash) {
                startkey = ep->me_key;
                Py_INCREF(startkey);
                cmp = PyObject_RichCompareBool(startkey, key, Py_EQ);
                Py_DECREF(startkey);
                if (cmp < 0)
                    return NULL;
                if (ep0 == mp->ma_table && ep->me_key == startkey) {
                    if (cmp > 0)
                        return ep;
                }
                else {
                    /* The compare did major nasty stuff to the
                     * dict:  start over.
                     * XXX A clever adversary could prevent this
                     * XXX from terminating.
                     */
                    return lookdict(mp, key, hash);
                }
            }
            freeslot = NULL;
        }

        /* In the loop, me_key == dummy is by far (factor of 100s) the
           least likely outcome, so test for that last. */
        for (perturb = hash; ; perturb >>= PERTURB_SHIFT) {
            i = (i << 2) + i + perturb + 1;
            ep = &ep0[i & mask];
            if (ep->me_key == NULL)
                return freeslot == NULL ? ep : freeslot;
            if (ep->me_key == key)
                return ep;
            if (ep->me_hash == hash && ep->me_key != dummy) {
                startkey = ep->me_key;
                Py_INCREF(startkey);
                cmp = PyObject_RichCompareBool(startkey, key, Py_EQ);
                Py_DECREF(startkey);
                if (cmp < 0)
                    return NULL;
                if (ep0 == mp->ma_table && ep->me_key == startkey) {
                    if (cmp > 0)
                        return ep;
                }
                else {
                    /* The compare did major nasty stuff to the
                     * dict:  start over.
                     * XXX A clever adversary could prevent this
                     * XXX from terminating.
                     */
                    return lookdict(mp, key, hash);
                }
            }
            else if (ep->me_key == dummy && freeslot == NULL)
                freeslot = ep;
        }
        assert(0);          /* NOT REACHED */
        return 0;
    }
字典在添加元素和查询元素时，都需要用到字典的搜索策略，搜索时，如果不存在该key，那么返回Unused状态的entry，如果存在该key，但是key是一个Dummy对象，那么返回Dummy状态的entry，其他情况就表示存在Active状态的entry，那么对于字典的插入操作，针对不同的情况进行操作也不一样。对于Active的entry，直接替换me\_value值即可；对于Unused或Dummy的entry，需要同时设置me\_key，me\_hash和me\_value

####PyDictObject对象缓冲池
PyDictObject对象缓冲池和PyListObject对象缓冲池的原理是类似的，都是在对象被销毁的时候把该对象添加到缓冲池中去，而且值保留PyDictObject对象本身，如果ma\_table维护的时从系统堆中申请的空间，那么Python会释放这块内存，如果ma\_table维护的是ma\_smalltable，那么只需把smalltable中的元素的引用计数减少即可。
    
    static void
    dict_dealloc(register PyDictObject *mp)
    {
        register PyDictEntry *ep;
        Py_ssize_t fill = mp->ma_fill;
        PyObject_GC_UnTrack(mp);
        Py_TRASHCAN_SAFE_BEGIN(mp)
        for (ep = mp->ma_table; fill > 0; ep++) {
            if (ep->me_key) {
                --fill;
                Py_DECREF(ep->me_key);
                Py_XDECREF(ep->me_value);
            }
        }
        if (mp->ma_table != mp->ma_smalltable)
            PyMem_DEL(mp->ma_table);
        if (numfree < PyDict_MAXFREELIST && Py_TYPE(mp) == &PyDict_Type)
            free_list[numfree++] = mp;
        else
            Py_TYPE(mp)->tp_free((PyObject *)mp);
        Py_TRASHCAN_SAFE_END(mp)
    }

<<<<<<< HEAD
参考：  
* [Python整数对象实现原理](http://foofish.net/blog/89/python_int_implement)
* [Python字符串实现原理](http://foofish.net/blog/90/python_str_inplements)
* [Python列表对象实现原理](http://foofish.net/blog/91/python-list-implements)
=======

>>>>>>> 8830afd4298ce03a3fec5980df8ffdcbd3665d2e
