可能不常用到的Git命令
==================
 
####统计代码行数

    git ls-files | xargs wc -l
####统计python代码行数

    git ls-files | grep .py | xargs wc -l
        
####更新fork项目:
如果你fork了别人的项目，过段时间突然发现该项目更新了很多内容，于是你想同步更新到自己的仓库中，可以按如下步骤：  
    
    1. 添加一个remote指向上游仓库
            
            git remote add upstream https://github.com/keleshev/schema.git
    2. 获取上游远程分支更新内容
            
            git fetch upstream
    3. 合并到本地分支
            
            git checkout master
            git merge upstream/master
            
####删除远程分支
    
    git push origin --delete branch-a   # 删除远程分支branch-a
如果远程分支已经删除,但是本地还存在诸如:remotes/origin/[branch]这样的分支时，可能会引起错误:

>error: unable to delete 'lzjun': remote ref does not exist
error: failed to push some refs to 'git@bitbucket.org:sponialtd/openplay_pylibs.git'

解决办法是[参考地址](http://stackoverflow.com/questions/10292480/when-deleting-remote-git-branch-error-unable-to-push-to-unqualified-destination)：
        
    git fetch -p origin
####不再同步某些已经加入仓库的文件
有时候忘记添加.gitignore文件，而误把一些pyc文件同步到了仓库中，此时你希望不再同步这些文件，使用：
        
    git update-index --assume-unchanged path/to/file
如果现在你又想把它加入到仓库中，怎么办？使用：
    
    git update-index --no-assume-unchanged path/to/file

也可以使用命令：
    
    git reset --cached [file]

停止追踪文件，但不会删除，也就是说只从暂存区移除。

####删除一次commit
    
由于某些原因导致误操作增加了一次commit，现在想删除它，怎么办？
        
    git log

    commit 663019f323084a7ebdab0aa96223272816d64322
    Author: liuzhijun <lzjun567@gmail.com>
    Date:   Thu Aug 27 12:25:12 2015 +0800

        Remove TODO

    commit 0d6aa254961945372d3108ab053b51426194cbaf
    Author: liuzhijun <lzjun567@gmail.com>
    Date:   Thu Aug 27 12:22:59 2015 +0800

        Remove TODO
我要删除6630这个commit

    git reset --hard [commit]
    git push origin  HEAD --force
        

git push 到远程分支的时候报莫名其妙的错误：

    git push origin feature/3.1

    Counting objects: 8, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (7/7), done.
    Writing objects: 100% (8/8), 652 bytes | 0 bytes/s, done.
    Total 8 (delta 6), reused 3 (delta 1)
    remote: error: cannot lock ref 'refs/heads/feature/3.1': Unable to create '/ndiskd/repositories/li/liuzhijun/beiy           unbao.git/refs/heads/feature/3.1.lock': File exists.
    remote:
    remote: If no other git process is currently running, this probably means a
    remote: git process crashed in this repository earlier. Make sure no other git
    remote: process is running and remove the file manually to continue.
    To git@git.oschina.net:liuzhijun/xxx.git
     ! [remote rejected] feature/3.1 -> feature/3.1 (failed to update ref)

解决办法是把远程分支删除，再添加进来
    
    $ git remote -v
    origin  git@git.oschina.net:liuzhijun/xxx.git (fetch)
    origin  git@git.oschina.net:liuzhijun/xxx.git (push)

    $ git remote rm origin

    $ git remote add origin  git@git.oschina.net:liuzhijun/xxx.git
