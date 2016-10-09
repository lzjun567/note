#Linux替换目录下多个文件中的字符串
在Linux中，替换多个文件中的某个字符串可以使用`grep`和`sed`的组合来实现这个功能。
###基本格式
	
	grep -rl matchstring somedir/ | xargs sed -i 's/string1/string2/g'

`matchstring`是你将要被替换的字符串，它与`string1`是同样的字符串，`string2`是用来替换`string1`的字符串。`somdir`表示在指定目录下。

###例子
	
	grep -rl 'windows' ./ | xargs sed -i 's/windows/linux/g'
这个命令表示在当前目录下所有文件中搜索字符串“windows”，并用“linux”替换之。
