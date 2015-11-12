ImportNew Android App 从0到1
==============================
[ImportNew](http://www.importnew.com)是一个专注于 Java 相关技术分享的博客，平常自己关注ImportNew比较多，曾经有想过自己开发一个客户端出来，可以随时随地方便在移动设备上阅读，不过很多时候仅仅想想就过去了，但这次是玩真的，从零开始写ImportNew客户端，前后断断续续用业余时间花了两周多时间把Demo做了出来，实践证明实现一个想法并没有想象中的那么难，主要问题还是太懒。  

####为什么要做ImportNew Android客户端  
最早接触Android还是在10年的时候，当时Nokia还是市场主流，周围同学几乎人手一台Nokia，不过隔壁宿舍有个土豪买了个Android 系统的SumSang手机，那是第一次体验到Android，那界面在当时绝对算得上惊艳，尽管那时还没见过iPhone长啥样。于是回宿舍后手痒痒地开始按照官方文档把开发环境搭建好开启人生中第0个Android App------那个人尽皆知的Hello World，那时的开发工具和现在根本没法比，开个模拟器比蜗牛还慢，此后就再也没去折腾了。今天又重新拾起来，主要是因为我终于有了自己的第一台Android手机（这样装逼或许会被打的），其实真正的初衷源于自己想做一款专属健康管理App，因为大部分码农从来都不在乎自己的身体健康。那么问题来了，你的第1个App为什么是ImportNew客户端？其实ImportNew的前身就是前面提到的那个健康管理App。最开始画了一个ListView出来，接着了解到Fragments的用法，看到Fragments的一个例子是左侧列表Items，右侧是某个Item的详情，这让我想到可以先做个ImportNew客户端出来，于是就开干了。
![fragments](http://7i7hhc.com1.z0.glb.clouddn.com/fragments.png)
####ImportNew技术细节
前后端分离，做各自擅长的事是一个应用程序延续生命力基本要素。客户端所展示的数据均源自ImportNew网站，后端有专门的爬虫，不定时爬取最新文章，通过提供Restful风格接口返回结构化文档给客户端展示。
####后端技术
爬虫使用`tornado.queues`模块用协程的方式实现异步的生产者/消费者模型，并发地爬取页面。在单机环境下爬完整站所有文章在1分多钟的时间，如果用普通[Requests](http://docs.python-requests.org/en/latest/)库单线程模式则会花费30多分钟。  
![crawler](http://7i7hhc.com1.z0.glb.clouddn.com/crawler.jpg)

后端接口使用Python/Tornado实现，数据库直接使用Redis，这种比较简单的客户端用Redis简直是绝配，文章列表用了SortedSet，文章详情用Hash结构来表示，完全没必要用MySQL。
####前端技术
最开始做Demo的时候用ListView组件展示文章列表，自定义ViewHolder来保存试图引用提高ListView的滑动流畅度，后来发现有一个更高级的控件RecycleView用来替换ListView，RecyclerView是谷歌V7包下新增的控件，该控件默认实现了ViewHold模式。此外文章的详细页面用过好几种方法，最开始直接传递一个url给Webview加载文章的详细页面，但这样的实现方式显然与直接用浏览器没什么区别。因此，后来接着把文章的详细页面数据也一同爬取到，此时Webview加载的一个文本。文章的样式依然通过css控制，只不过Css是放在本地加载，而无需再通过WebView去远程服务器加载样式文件，这样的方案可以提高页面的响应速度。所有的网络请求用异步加载库Volley。
![importnew](http://7i7hhc.com1.z0.glb.clouddn.com/ImportNew_1.jpg)

所有代码已开源：[ImportNewApp](https://github.com/lzjun567/ImportNewApp)，[ImportNewAPI](https://github.com/lzjun567/ImportNewAPI)。App下载地址：  
![download](http://7i7hhc.com1.z0.glb.clouddn.com/importnew_download.png)  

最后，感谢这个伟大的开源时代，让学习变得更简单。


