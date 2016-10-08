#分析urllib.unquote乱码的原因
Python中的urllib模块用来处理url相关的操作，`unquote`方法对应javascript中的urldecode方法，它对url进行解码，把类似"%xx"的字符替换成单个字符，例如：“%E6%B3%95%E5%9B%BD%E7%BA%A2%E9%85%92”解码后会转换成“法国红酒”，但是使用过程中，如果姿势不对，最终转换出来的字符会是乱码“æ³å½çº¢é”。

笔者在一个真实的Tornado应用中就遇到了这样的问题，浏览器通过请求传递到后台后，获取参数的值后：  
	
	name = self.get_argument("name", "")
	name = urllib.unquote(name)
	# save to db

name的值打印出来的显示的是：**“%E6%B3%95%E5%9B%BD%E7%BA%A2%E9%85%92”**，看起来没什么问题，但结果最终保存到数据库中的时候就成了一串乱码**“æ³å½çº¢é”**，这个问题实在是让人百思不得其解。
###原因分析
于是想用直接编码的字符来处理看看是否会出现乱码：  

	name = '%E6%B3%95%E5%9B%BD%E7%BA%A2%E9%85%92'
	name = urllib.unquote(name)
	# save to db


发现这种方式处理没有任何问题，name的值解码之后就是“法国红酒”，经过一番思考，原因只可能是出在`self.get_argument("name")`这处代码段了。原来，get_argument默认返回的是值的类型是unicode，而`unquote`方法处理unicode类型的字符时，直接返回的就是：  
	
	u'\xe6\xb3\x95\xe5\x9b\xbd\xe7\xba\xa2\xe9\x85\x92'
注意这里返回的值类型是unicode，也就是说unquote方法接收参数类型是unidoe，返回的值类型也是unicode，只不过是把"%"替换成了'\x'，最终由：  
	
	u"%E6%B3%95%E5%9B%BD%E7%BA%A2%E9%85%92"
替换为了：
	
	u"\xe6\xb3\x95\xe5\x9b\xbd\xe7\xba\xa2\xe9\x85\x92"
而**u"\xe6\xb3\x95\xe5\x9b\xbd\xe7\xba\xa2\xe9\x85\x92"**完全就是一个ascii码字符串，只不过是用16进制表示的，我们再来看看'e6','b3'....分别对应ascii中的什么字符。你可以参考网址：[http://www.ascii-code.com](http://www.ascii-code.com/)，'e6'是一个扩展的ascii字符，在128-255区间范围内，他对应的符号就是'æ'
	

	DEC	OCT	HEX	BIN		   Symbol	
	230	346	E6	11100110	æ

现在你应该明白为什么会生成乱码字符：
	
	æ³å½çº¢é

###解决办法
在调用`self.get_argument('name')`方法之后，把返回的值转换成str类型：	
	
	name = self.get_argument("name", "")
	name = str(name)
	name = urllib.unquote(name)
	# save to db

转换称str类型的字符串之后，相当于调用：
	
	'\xe6\xb3\x95\xe5\x9b\xbd\xe7\xba\xa2\xe9\x85\x92'.decode("utf-8")

	>>> u'\u6cd5\u56fd\u7ea2\u9152'