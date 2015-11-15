可能会不常用到的Git命令
 ==================
 
1. 统计代码行数

        git ls-files | xargs wc -l
2. 统计python代码行数

        git ls-files | grep .py | xargs wc -l
        
3. 更新fork项目
如果你fork了别人的项目，过段时间突然发现该项目更新了很多内容，于是你想同步更新到自己的仓库中，可以按如下步骤：  
    
    1. 添加一个remote指向上游仓库
            
            git remote add upstream https://github.com/keleshev/schema.git
    2. 获取上游远程分支更新内容
            
            git fetch upstream
    3. 合并到本地分支
            
            git checkout master
            git merge upstream/master
            
4. 删除远程分支
    
        git push origin --delete branch-a   # 删除远程分支branch-a
    * 错误处理：删除远程分支的时候报错
    
        error: unable to delete 'lzjun': remote ref does not exist
        error: failed to push some refs to 'git@bitbucket.org:sponialtd/openplay_pylibs.git'
    我本地显示的分支（远程仓库中已经没有了该分支）：  
        
        remotes/origin/lzjun
    解决办法是：  
        
        git fetch -p origin   #http://stackoverflow.com/questions/10292480/when-deleting-remote-git-branch-error-unable-to-push-to-unqualified-destinatio 
            
5. 不再同步某些已经加入仓库的文件

    有时候忘记添加.gitignore文件，而误把一些pyc文件同步到了仓库中，此时你希望不再同步这些文件，使用： 
        
        git update-index --assume-unchanged path/to/file
    如果现在你又想把它加入到仓库中，怎么办？使用：    
    
        git update-index --no-assume-unchanged path/to/file

6. 删除一次commit
    
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
        

