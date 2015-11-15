这个我的vim的配置，我主要用来做Python开发  

    "vim用双引号表示注释
    "默认文件编码
    set fileencodings=ucs-bom,utf-8,cp936,gb18030,big5,euc-jp,euc-kr,latin1
    set fileencoding=utf-8
    set encoding=utf-8   "设置vim内部编码格式
    
    colorscheme desert   "编辑器背景颜色
    
    syntax on   "语法
    
    " 解决windows下如果encoding设置utf-8，菜单会乱码问题
     set langmenu=zh_CN.UTF-8
     language message zh_CN.UTF-8
     source $VIMRUNTIME/delmenu.vim
     source $VIMRUNTIME/menu.vim
    
    
    "  以下命令代码缩进相关
    "set autoindent  "继承前一行的缩进
    set smartindent
    set smarttab
    set expandtab   "tab都用空格代替
    set softtabstop=4  "tab=四个空格
    set tabstop=4
    set shiftwidth=4
    "set textwidth=79
    
    set nocompatible "不兼容vi的键盘模式
    set ruler  "在状态行显示光标所在位置的行号和列号
    set nu
    set mouse=a
    
    "不生成临时文件
    set noswapfile
    set nobackup
    set backspace=2  "允许退格键删除字符
    set ignorecase  "搜索忽略大小写
    
    "禁掉箭头移动功能，勤用hjkl
    nnoremap <up> <nop>
    nnoremap <down> <nop>
    nnoremap <left> <nop>
    nnoremap <right> <nop>
    
    "markdown 语法，在浏览器查看效果，自动刷新
    function! ViewAtChrome(name)
        let file = expand("%:p")
        exec ":update " . file
        let l:browser = {
            "cr":"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"   
            }
        exec ":silent !start".l:browsers[a:name]."file://".file
    endfunction 
    
    "快捷键  调出浏览器
    nmap <f4>cr :call ViewAtChrome("cr")<cr>
    
    "快捷键
    ab reprint 转载请注明出处，谢谢合作！作者---[zhijun](http://weibo.com/527355345)
    
    "缩写时提示
    function! s:forxAsk(forx,expansion)
        let answer = confirm("使用缩写'" . a:forx ."'?","&Yes\n&No",1)
        return answer == 1 ? a:expansion :a:forx
    endfunction
    :iabbrev <expr> forx <SID>forxAsk('forx','for(x=0;x<100;x++){<CR><CR>}<Esc>gi<Tab>')
    
    
    "自动补全
    filetype plugin indent on
    set completeopt=longest,menu
    "自动补全命令时使用菜单式匹配列表
    set wildmenu
    " 在windows下Vim7的omni-completion功能不支持64位的python，所以按Ctrl-x
    " Ctrl-O无效，必须换成32位的
    autocmd FileType python set omnifunc=pythoncomplete#Complete
    autocmd FileType html set omnifunc=htmlcomplete#COmpleteTags
    "Pydiction
    let g:pydiction_location='E:\Vim\vim73\complete-dict'
    
    "TagList
    let Tlist_Show_One_File=1
    let Tlist_Exit_OnlyWindow=1
    
    "===========  F5 run python ====================
    autocmd BufRead *.py set makeprg=python\ -c\ \"import\ py_compile,sys;\ sys.stderr=sys.stdout;\ py_compile.compile(r'%')\"
    autocmd BufRead *.py set efm=%C\ %.%#,%A\ \ File\ \"%f\"\\,\ line\ %l%.%#,%Z%[%^\ ]%\\@=%m
    autocmd BufRead *.py nmap <F5> :!python %<CR>
    
    autocmd BufRead *.py set tabstop=4
    autocmd BufRead *.py set nowrap
    autocmd BufRead *.py set go+=b
    
    "F8切换到taglist窗口
    nnoremap <silent><F8> :TlistToggle<CR>
    
    ""http://www.cnblogs.com/renrenqq/archive/2010/09/09/1813669.html
    ""https://github.com/rkulla/pydiction
    
    "常用的折叠方式就两种，indent和marker
    "indent方式会利用缩进自动进行折叠
    set foldmethod=indent

" 无论是normal模式还是插入模式还是visual模式，按crtl+s 保存文件
nmap <c-s> :w<CR>
vmap <c-s> <Esc><c-s>gv
imap <c-s> <Esc><c-s>
