通过点击按钮进入到一个新的activity  

####添加按钮响应事件

`android:onClick`

    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/button_send"
        android:onClick="sendMessage" />
    
sendMessage是activity里面的方法名，当用户点击此按钮的时候系统会调用该方法。  
貌似在这个方法里面输出syso，没有任何消息输出。 更新：有输出， 在logcat里面可以看到   

####构建一个Intent
Intent的意思就是"intent to do something"，打算去做某事。通常用来启动另一个activity。  

现在在sendMessage方法中创建一个Intent来启动一个叫DisplayMessasgeActivity。  

    Intent intent = new Intent(this, DisplayMessageActivity.class);

this 是 Context对象，Activity是Context的一个子类。  
