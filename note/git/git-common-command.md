Git日常命令
=========
Git已经成为程序员日常工具之一，就像普通人每天要吃饭睡觉似的（说的好像程序员不需要睡觉似的）。那些Git基本的命令，每天都要用得命令你都记住了吗？如果还没的话，笔者已经帮你整理了一份清单，拿去吧，不用谢，我是雷锋。

工作区(Workspace)是电脑中实际的目录；暂存区(Index)像个缓存区域，临时保存你的改动；版本库(Repository)分为本地仓库（Local)和远程仓库(Remote)，一图胜千言。

![simple](http://www.ruanyifeng.com/blogimg/asset/2015/bg2015120901.png)

上图中的6个命令恐怕是使用频率最高的命令了，但只会使用以上命令是不够的，在这个复杂纷繁的程序世界，事情没你想的那么简单，不过有些事情想想就够了，不一定要去做，真要去做你也做不来，比如自己写个git来，但是，更多地的了解git是我们每个程序员都可以做得到的事。再看下图：  
![advance](http://ww4.sinaimg.cn/mw690/81b78497jw1eqnk1bkyaij20e40bpjsm.jpg)

####新建/克隆代码库

	
	$ git init                                          #当前目录新建一个Git代码库
	
	$ git init [project-name]						     #新建一个目录，将其初始化为Git代码库
	
	$ git clone [url]								     #下载一个项目和它的整个代码历史

####添加/删除文件
	
	# 添加指定文件到暂存区
	$ git add [file1] [file2] ...

	# 添加指定目录到暂存区，包括子目录
	$ git add [dir]

	# 添加当前目录的所有文件到暂存区
	$ git add .

	# 删除工作区文件，并且将这次删除放入暂存区
	$ git rm [file1] [file2] ...

	# 停止追踪指定文件，但该文件会保留在工作区
	$ git rm --cached [file]

	# 改名文件，并且将这个改名放入暂存区
	$ git mv [file-original] [file-renamed]

####代码提交
	
	# 提交暂存区所有文件到仓库区，并指定提交说明
	$ git commit -m [message]

	# 提交暂存区的指定文件到仓库区，并指定提交说明
	$ git commit [file1] [file2] ... -m [message]

	# 提交工作区自上次commit之后的变化，直接到仓库区
	$ git commit -a

	# 提交时显示所有diff信息
	$ git commit -v

	# 使用一次新的commit，替代上一次提交
	# 如果代码没有任何新变化，则用来改写上一次commit的提交信息
	$ git commit --amend -m [message]

	# 重做上一次commit，并包括指定文件的新变化
	$ git commit --amend [file1] [file2] ...

####分支
	
	# 列出所有本地分支
	$ git branch

	# 列出所有远程分支
	$ git branch -r

	# 列出所有本地分支和远程分支
	$ git branch -a

	# 新建一个分支，但依然停留在当前分支
	$ git branch [branch-name]

	# 新建一个分支，并切换到该分支
	$ git checkout -b [branch]

	# 新建一个分支，指向指定commit
	$ git branch [branch] [commit]

	# 新建一个分支，与指定的远程分支建立追踪关系
	$ git branch --track [branch] [remote-branch]

	# 切换到指定分支，并更新工作区
	$ git checkout [branch-name]

	# 建立追踪关系，在现有分支与指定的远程分支之间
	$ git branch --set-upstream [branch] [remote-branch]

	# 合并指定分支到当前分支
	$ git merge [branch]

	# 选择一个commit，合并进当前分支
	$ git cherry-pick [commit]

	# 删除分支
	$ git branch -d [branch-name]

	# 删除远程分支
	$ git push origin --delete [branch-name]
	$ git branch -dr [remote/branch]

####设置
git的配置文件是.gitconfig，支持全局配置和项目配置，全部配置对所有项目有效，用 `--global`选择指定。
	
	$ git config --list                                  #显示配置
	
	$ git config -e [--global]  						 #编辑(全局)配置文件
	
	$ git config [--global] user.name "xx"               #设置 commit 的用户
	
	$ git config [--global] user.email "xx@xx.com"       #设置 commit 的邮箱

