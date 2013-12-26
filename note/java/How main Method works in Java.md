如何生成一个合适的hashcode方法
---------------------
Hashcode在基于key-value的集合如HashMap、LinkedHashMap中扮演很重要的角色。除此之外hashcode的概念同样运用在HashSet中，最佳的部分使用合适的hashcode是获取操作是 O(1).  

一个差劲的hashcode算法不仅会降低一个基于哈希的集合性能，而且会导致异常结果。有多种不同的方式来生成hashcode。  

####Effective Java
Josh Bloch在他的书籍《Effective Java》告诉我们重写hashcode方法的最佳实践方式。  

一个好的hashcode方法通常是最好是不相等的对象产生不相等的hash值，理想情况下，hashcode方法应该把集合中不相等的实例均匀分布到所有可能的hash值上面。  

1. 把某个非0的常数值，比如17，保存在一个名为result的int类型的变量中。
2. 对于对象中的每个域，做如下操作：  

    * 为该域计算int类型的散列码c：  
            
            a. 如果该域是boolean类型，则计算(f?1:0)
            b. 如果该域是byte、char、short或者int类型，则计算(int)f
            c. 如果该域是long类型，则计算(int)(f^(f>>>32))
            d. 如果该域是float类型，则计算Float.floatToIntBits(f)
            e. 如果该域是double类型，则计算Double.doubleToLongBits(f)，然后重复c步骤。
            f. 如果该域是一个对象引用，并且该类的equals方法通过递归调用equals方法来比较这个域，同样为这个域递归的调用hashCode，如果这个域为null，则返回0。
            g. 如果该域是数组，则要把每一个元素当作单独的域来处理，递归的运用上述规则，如果数组域中的每个元素都很重要，那么可以使用Arrays.hashCode方法。

把上面计算得到的hash值c合并到result中  

    result = 31*result + c 
.
