Git常用命令备忘
==============
Git已经成为程序员日常工具之一，那些Git基本的命令，每天都要用得命令你都记住了吗？如果还没的话，笔者整理了一份清单，以备不时之需所用。

####三个基本概念
1. 工作区(Workspace)是计算机中项目的根目录
2. 暂存区(Index)像个缓存区域，临时保存你的改动
3. 版本库(Repository)分为本地仓库（Local)和远程仓库(Remote)

几乎所有常用命令就是围绕这几个概念来操作的，一图胜千言，下面是一张比较简单的图，包括了最基本的命令

![simple](http://www.ruanyifeng.com/blogimg/asset/2015/bg2015120901.png)

但只会使用以上命令是不够的，在这个复杂纷繁的程序世界，事情没你想的那么简单，不过有些事情想想就够了，不一定要去做，真要去做你也做不来，比如自己写个git来，但是，更多地的了解git是我们每个程序员都可以做得到的事。再看下图：  
![advance](http://ww4.sinaimg.cn/mw690/81b78497jw1eqnk1bkyaij20e40bpjsm.jpg)

下面的命令结合上面两张图来理解、练习、记忆效果更加。暂时用不着的命令记不住，不理解也没关系，哪天遇到问题，再来找找有没有合适的方法也不迟。

####新建/克隆代码库

	
	$ git init                                          #当前目录新建一个Git代码库
	
	$ git init [project-name]						     #新建一个目录，将其初始化为Git代码库
	
	$ git clone [url]								     #下载一个项目和它的整个代码历史

	$ git fetch [url]									 #下载/同步项目到

####添加/删除文件
	
	
	$ git add [file1] [file2] ...   					# 添加指定文件到暂存区
	
	$ git add [dir] 									# 添加指定目录到暂存区，包括子目录

	$ git add .   										# 添加当前目录的所有文件到暂存区

	$ git rm [file1] [file2] ...   					# 删除工作区文件，并且将这次删除放入暂存区
	
	$ git rm --cached [file]   						# 停止追踪指定文件，但该文件会保留在工作区
	
	$ git mv [file-original] [file-renamed]  			# 改名文件，并且将这个改名放入暂存区

####代码提交
	
	$ git commit -m [message]  						# 提交暂存区所有文件到仓库区，并指定提交说明
	
	$ git commit [file1] [file2] ... -m [message]   	# 提交暂存区的指定文件到仓库区，并指定提交说明

	$ git commit -a   # 提交工作区自上次commit之后的变化，直接到仓库区。是git add 和 git commit的组合操作

	$ git commit -v  									# 提交时显示所有diff信息

	$ git commit --amend -m [message]   				# 使用一次新的commit，替代上一次提交


####分支
	
	$ git branch   									# 列出所有本地分支

	$ git branch -r									# 列出所有远程分支

	$ git branch -a 									# 列出所有本地分支和远程分支

	$ git branch [branch-name]  						# 新建一个分支，但依然停留在当前分支

	$ git checkout -b [branch]  						# 新建一个分支，并切换到该分支

	$ git branch [branch] [commit]  					# 新建一个分支，指向指定commit
	
	$ git checkout [branch-name]  						# 切换到指定分支

	$ git merge [branch]  								# 合并指定分支到当前分支

	$ git branch -d [branch-name]  					# 删除本地分支

	$ git push origin --delete [branch-name]  			# 方法一：删除远程分支
	$ git branch -dr [remote/branch]          			# 方法二：删除远程分支

####撤销
	
	$ git checkout [file]   							# 恢复暂存区的指定文件到工作区（注意区别分支操作中得checkout命令）

	$ git checkout [commit] [file]  					# 恢复某个commit的指定文件到暂存区和工作区

	$ git checkout .   								# 恢复暂存区的所有文件到工作区
	
	$ git reset [file]  								# 重置暂存区的指定文件，与最新的commit保持一致，但工作区不变
	
	$ git reset --hard    								# 重置暂存区与工作区，与最新的commit保持一致

	$ git reset [commit]   							# 重置当前分支的指针为指定commit，同时重置暂存区，但工作区不变
	
	$ git reset --hard [commit]  						# 重置当前分支的HEAD为指定commit，同时重置暂存区和工作区，与指定commit一致
	
	$ git reset --keep [commit]   						# 重置当前HEAD为指定commit，但保持暂存区和工作区不变

	$ git revert [commit]  							# 新建一个commit，用来撤销指定commit

####标签

	$ git tag  										# 列出所有tag
	
	$ git tag [tag] 									# 在当前commit新建一个tag

	$ git tag [tag] [commit] 							# 在指定commit新建一个tag

	$ git tag -d [tag]   								# 删除本地tag
	
	$ git push origin :refs/tags/[tagName]  			# 删除远程tag

	$ git show [tag]  									# 查看tag信息

	$ git push [remote] [tag]  						# 提交指定tag

	$ git push [remote] --tags  						# 提交所有tag

	$ git checkout -b [branch] [tag]   				# 新建一个分支，指向某个tag
####查看日志
	
	$ git status 									# 显示所有变更文件

	$ git log  										# 显示当前分支的版本历史

	$ git log --stat 								# 显示当前分支的版本历史，以及发生变更的文件

	$ git blame [file]								# 显示指定文件是什么人在什么时间修改过

	$ git log -p [file]								# 显示指定文件相关的每一次diff
	 
	$ git diff     									# 显示暂存区和工作区的差异

	$ git diff --cached [commit]					# 显示暂存区和某个commit的差异

	$ git diff HEAD 								# 显示工作区与当前分支最新commit之间的差异

	$ git show [commit]								# 显示某次提交的元数据和内容变化

	$ git show --name-only [commit]					# 显示某次提交发生变化的文件

	$ git show [commit]:[filename]					# 显示某次提交时，某个文件的内容
	
	$ git reflog									# 显示当前分支的最近几次提交

####远程同步

	$ git fetch [remote]							# 下载远程仓库的所有变动到暂存区

	$ git remote -v 								# 显示所有远程仓库
	
	$ git remote show [remote]						# 显示某个远程仓库的信息

	$ git remote add [shortname] [url]				# 增加一个新的远程仓库，并命名

	$ git pull [remote] [branch]					# 取回远程仓库的变化，并与本地分支合并

	$ git push [remote] [branch]					# 上传本地指定分支到远程仓库
	
	$ git push [remote] --force						# 即使有冲突，强行推送当前分支到远程仓库
	
	$ git push [remote] --all						# 推送所有分支到远程仓库
####设置
git的配置文件是.gitconfig，支持全局配置和项目配置，全部配置对所有项目有效，用 `--global`选择指定。
	
	$ git config --list                                  #显示配置
	
	$ git config -e [--global]  						 #编辑(全局)配置文件
	
	$ git config [--global] user.name "xx"               #设置 commit 的用户
	
	$ git config [--global] user.email "xx@xx.com"       #设置 commit 的邮箱

