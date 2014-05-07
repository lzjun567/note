Action Bar 是几乎每个App都有东西，大概样子就是：  
![action_bar](http://foofish.qiniudn.com/actionbar-actions.png)

这个ActionBar仅支持Android3.0(API level11)以上的版本。因此你设置`AndroidManifest.xml`：  
    
    <manifest ... >
        <uses-sdk android:minSdkVersion="11" ... />
        ...
    </manifest>

所有action按钮和items定义在res/menu目录下面， 

