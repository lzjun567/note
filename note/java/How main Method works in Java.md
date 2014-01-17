如何生成一个合适的hashcode方法
------------------------------
Hashcode在基于key-value的集合如：HashMap、LinkedHashMap中扮演很重要的角色。此外在HashSet集合中也会运用到，使用合适的hashcode方法在检索操作时的时间复杂度最好的是 O(1).  

一个差劲的hashcode算法不仅会降低基于哈希集合的性能，而且会导致异常结果。Java应用中有多种不同的方式来生成hashcode。  

####Effective Java
Josh Bloch在他的书籍《Effective Java》告诉我们重写hashcode方法的最佳实践方式。  

一个好的hashcode方法通常最好是不相等的对象产生不相等的hash值，理想情况下，hashcode方法应该把集合中不相等的实例均匀分布到所有可能的hash值上面。  

1. 把某个非0的常数值，比如17，保存在一个名为result的int类型的变量中。
2. 对于对象中的每个域，做如下操作：  

    * 为该域计算int类型的哈希值c：  
            
        *  如果该域是boolean类型，则计算(f?1:0)
        *  如果该域是byte、char、short或者int类型，则计算(int)f
        *  如果该域是long类型，则计算(int)(f^(f>>>32))
        *  如果该域是float类型，则计算Float.floatToIntBits(f)
        *  如果该域是double类型，则计算Double.doubleToLongBits(f)，然后重复第三个步骤。
        *  如果该域是一个对象引用，并且该类的equals方法通过递归调用equals方法来比较这个域，同样为这个域递归的调用hashCode，如果这个域为null，则返回0。
        *  如果该域是数组，则要把每一个元素当作单独的域来处理，递归的运用上述规则，如果数组域中的每个元素都很重要，那么可以使用Arrays.hashCode方法。

把上面计算得到的hash值c合并到result中  

    result = 31*result + c 

####String中的Hashcode方法
String的hashcode的算法就充分利用了字符串内部字符数组的所有字符。生成hash码的算法的在string类中看起来像如下所示，注意“s“是那个字符数组，n是字符串的长度。  

    s[0]*31^(n-1) + s[1]*31^(n-2) + ... + s[n-1]

####Hashcode使用Eclipse IDE
现代IDE通过点击右键上下文菜单可以自动生成hashcode方法，通过Eclipse IDE 生成的hashcode像：  

    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + a;
        return result;
    }

但是并不推荐如上代码使用在企业级代码中，最好使用第三方库如Apache commons来生成hashocde方法。  

####Apache commons HashcodeBuilder
我们可以用Apache Commons hashcode builder来生成代码，使用这样一个第三方库的优势是可以反复验证尝试代码。下面代码显示了如何使用Apache Commons hash code 为一个自定义类构建生成hash code 。  

    public int hashCode(){
           HashCodeBuilder builder = new HashCodeBuilder();
           builder.append(mostSignificantMemberVariable);
       ........................
       builder.append(leastSignificantMemberVariable);
           return builder.toHashCode();
       }

如上面代码显示的，最重要的签名成员变量应该首先传递然后跟随的是没那么重要的成员变量。  

Apache Commons库同样为自定义的类提供了构建生成equals的方法，使用equals构建器的代码看起来非常像上面的代码。事实上传递给成员变量从最重要的签名到最不重要的签名一样的规则，同样应用于equals构建器中。  

