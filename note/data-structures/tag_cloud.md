标签云算法Python实现
========
标签云（Tag Cloud）常见于各种博客站点中，标签有利于网站内容分类，还可以用于相关性内容推荐。近日笔者有空把个人的开源博客[Django_blog](https://github.com/lzjun567/django_blog)添加了一个新功能--标签云。最终效果请访问：[http://foofish.net/blog/tags](http://foofish.net/blog/tags)
![tagcloud](http://7d9py7.com1.z0.glb.clouddn.com/tag-cloud.jpg)

####实现原理

标签云最终展现出来的效果其实是由两个HTML参数来控制的，分别是：font-size和color，如：
	
	<a href="http://foofish.net/blog/tag/django" style="font-size:24px; color:#4f4f4f">django</a>
标签关联的文章越多，表示这个标签被引用的次数越大，font-size的值也越大，color的颜色越深。考虑到体验效果，font-size不能随着的标签的引用次数的增大而无限增大，否则页面显得非常丑陋。因此会把font-size控制在某个区间，同理color也是在一个区间中。

这里我把font-size设置在12到33之间数组FONT\_SIZES，标签的font-size属性只能是里面的一个值，COLORS是与FONT\_SIZES对应的一个数组，12对应#ccc，15对应#adadad，以此类推。
	
	MIN_FONT_SIZE = 12     # 最小尺寸
    MAX_FONT_SIZE = 33     # 最大尺寸
    FONT_SIZES = [MIN_FONT_SIZE, 15, 18, 21, 24, 27, 30, MAX_FONT_SIZE]   
    COLORS = ['#ccc', "#adadad", '#8e8e8e', '#6f6f6f', '#4f4f4f', '#303030', '#111', '#000']

现在关键问题就是如何根据标签的引用次数(tag\_ref\_count)来确定它的font-size。一旦font-size了，color也随之确定。要想标签的font-size能够均匀分布在数组FONT\_SIZES中，那么要遵循的一个原则就是，随着次数的增加其font-size的取值也增加，而且引用次数最少的标签使用MIN\_FONT\_SIZE，引用次数最多的标签使用MAX\_FONT\_SIZE。

因此有一个公式，`MIN_FONT_SIZE + n*step = MAX_FONT_SIZE`，step是步长，n是指引用次数最多的标签减去引用次数最少的标签，表示两者之间总共有多少步step，根据此根式可以算出每一步的step值是多少，知道了步长后，就可以计算出任意一个标签的font-size了，任何一个标签到最小标签的步数是两者之差，因此每一个标签的font-size为 `MIN_FONT_SIZE + (tag_ref_count-min_ref_count)*step`

![tag-step](http://7d9py7.com1.z0.glb.clouddn.com/tag-step.jpg)


源代码：

	# encoding: utf-8
	__author__ = 'liuzhijun'


	class TagCloud(object):
	    MIN_FONT_SIZE = 12
	    MAX_FONT_SIZE = 33
	    FONT_SIZES = [MIN_FONT_SIZE, 15, 18, 21, 24, 27, 30, MAX_FONT_SIZE]
	    COLORS = ['#ccc', "#adadad", '#8e8e8e', '#6f6f6f', '#4f4f4f', '#303030', '#111', '#000']

	    def __init__(self, min_ref_count, max_ref_count):
	        TagCloud.min_ref_count = min_ref_count
	        # 如果最大标签和最小标签相等,那么认为两者的步长为0,所有标签取同样的font-size.
	        if max_ref_count == min_ref_count:
	            TagCloud.step = 0
	        else:
	            TagCloud.step = (TagCloud.MAX_FONT_SIZE - TagCloud.MIN_FONT_SIZE) / (max_ref_count - min_ref_count)

	    def get_tag_font_size(self, tag_ref_count):
	        font_size = TagCloud.MIN_FONT_SIZE + (tag_ref_count - TagCloud.min_ref_count) * TagCloud.step
	        # 上面计算出来的font_size并不一定刚好是FONT_SIZES中的某个元素, 可以能某两个元素之间的某个值
	        # 因此要取最接近FONT_SIZES中某个元素
	        font_size = min(TagCloud.FONT_SIZES, key=lambda x: abs(font_size - x))
	        return font_size

	    def get_tag_color(self, tag_ref_count):
	        return TagCloud.COLORS[(TagCloud.FONT_SIZES.index(self.get_tag_font_size(tag_ref_count)))]

输出结果：
	
	12,12,12,18,24,18,21,27,33,








