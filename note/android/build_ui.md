Android：构建一个简单的UI
===========
Android的GUI由View和ViewGroup对象构成，View指的就是那些Button，Textfield等等。ViewGroup就是指view容器。  

Android可以直接通过XML配置文件来定义UI。  

![viewgroup](http://foofish.qiniudn.com/viewgroup.png)

####创建一个Linear布局
打开res/layout/framgment_main.xml，删掉`<RelativeLayout>`换成`<LinearLayout>`：  

    <LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
        xmlns:tools="http://schemas.android.com/tools"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="horizontal" >
    </LinearLayout>

LinearLayout 就是一个view group，在<LinearLayout>添加一个View：  

    <EditText android:id="@+id/edit_message"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:hint="@string/edit_message" />

android:id 是这个view的唯一标识符，可以在代码中通过这个id来操作这个对象。  

`wrap_content` 就是指view的宽度和高度根据view的内容填充大小。 如果是用"match_parent"就是跟父对象的大小一样。  

android:hint 指view的内容为空的时候的指，此时你的edit_message还没定义，因此会报错   

####添加String Resources
String resources可以在一个单独的地方管理所有UI文本，这样更易查找和更新文本。默认情况下project的string resource文件在res/values/strings.xml下面。现在添加一个新的字符串"edit_message"设置为"输入消息".  

    <?xml version="1.0" encoding="utf-8"?>
    <resources>
    
        <string name="app_name">defish</string>
        <string name="dummy_button">Dummy Button</string>
        <string name="dummy_content">DUMMY\nCONTENT</string>
        <string name="edit_message">输入消息</string>
    
    </resources>
    

格式更好的布局  

    <EditText
        android:id="@+id/edit_message"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_weight="1"
        android:hint="@string/edit_message" />
    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/button_send" />

    
