###Android应用的组成部分
**Activities**：应用的展示层，应用的UI由一个或多个Activity类构建而成，Activities使用Fragements和Views来布局和显示信息，响应用户的动作，和桌面应用开发对比，Activities等效于窗体。  
**Services**：应用中不可见的worker，这个组件不需要UI就能运行，用于更新数据源和Activities，触发通知和广播Intents。通常用在执行长期运行的任务场景中。  
**Content Providers**：这是一个可共享的持久化数据存储，它管理和持久化应用的数据，通常是与SQL数据库交互。  
**Intents**：一个强大的消息传递框架，可以使用Intents开启或者停止Acitivities和Services，或者是请求一个动作。  
**Broadcast Receivers**：Intent监听器。  
**Widgets**：可视化的应用组件，通常是放在设备的主屏幕上。  
**Notification**：Notification可以在不打断当前Activity的同时提醒用户。 
###Android应用的生命周期
默认情况下，Android应用运行在自己的进程中，每个进程是一个独立的Dalvik实例。
 
