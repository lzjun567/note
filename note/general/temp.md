#免费HTTPS证书Let's Encrypt安装教程
HTTPS在各大互联网站已经成为标配，很多小网站有配置了HTTPS，这是未来的一种趋势。HTTPS的好处多多，可以防止各种攻击劫持，运营商广告植入，客户传输信息泄露等问题。为了让HTTPS能够全面普及，Let's Encrypt项目应运而生，它由互联网安全研究小组ISRG（Internet Security Research Group）提供服务，而 ISRG 是来自美国加利福尼亚州的一个公益组织。Let's Encrypt 得到了 Mozilla、Cisco和 Chrome 等众多公司和机构的支持，发展十分迅猛。

申请 Let's Encrypt 证书免费、简单，不过每次申请只有90 天的有效期，但可以通过脚本定期更新，配置好之后一劳永逸。本站的HTTPS证书就是根据本教程一步一步搭建出来的，希望对正在寻找免费HTTPS方案的你有一定的帮助。

按照Let's Encrypt 官方提供的工具安装HTTPS的话与过于复杂，于是有好心人提供了更为轻巧的工具安装， [acme-tiny](https://github.com/diafygi/acme-tiny)应运而生，它的代码量在200行内，只需依赖Python和OpenSSL。

####第一步：创建 Let's Encrypt 账号（如何你还没有的话）

Let's Encrypt使用一个私钥来进行账号的创建与登陆，因此我们需要使用openssl创建一个account.key。  
    
    openssl genrsa 4096 > account.key

如果你已经有一个Let's Encrypt key的话，那么只需要做一次转换，因为Let's Encrpt 的客户端生成的key时JWK格式，而acm-tiny使用的是PEM格式。转换key需要使用一个[脚本](https://gist.github.com/JonLundy/f25c99ee0770e19dc595)  
    
    # 下载脚本
    wget -O - "https://gist.githubusercontent.com/JonLundy/f25c99ee0770e19dc595/raw/6035c1c8938fae85810de6aad1ecf6e2db663e26/conv.py" > conv.py
    
    # 把private key 拷贝到你的工作目录
    cp /etc/letsencrypt/accounts/acme-v01.api.letsencrypt.org/directory/<id>/private_key.json private_key.json
    
    # 创建一个DER编码的private key
    openssl asn1parse -noout -out private_key.der -genconf <(python conv.py private_key.json)
    
    # 转换成PEM格式
    openssl rsa -in private_key.der -inform der > account.key

####创建域名的CSR（certificate signing request）
Let's Encrypt 使用的ACME协议需要一个CSR文件，可以使用它来重新申请HTTPS证书，接下来我们就可以创建域名CSR，在创建CSR之前，我们需要给我们的域名创建一个私钥（这个和上面的账户私钥无关）。

    #创建普通域名私钥
    openssl genrsa 4096 > domain.key
接下来，使用你的域名私钥创建CSR文件，这一步里面是可以增加最多100个需要加密的域名的，替换下面的foofish.net即可（注意，稍后会说到，每个域名都会涉及到验证）
    
    #单个域名
    openssl req -new -sha256 -key domain.key -subj "/CN=foofish.net" > domain.csr

    #多个域名(如果你有多个域名，比如：www.foofish.net和foofish.net，使用这种方式)
    openssl req -new -sha256 -key domain.key -subj "/" -reqexts SAN -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:foofish.net,DNS:www.foofish.net")) > domain.csr

执行这一步时，需要指定 openssl.cnf 文件，一般这个文件在你的 openssl 安装目录底下。

####配置域名验证

CA 在签发 DV（Domain Validation）证书时，需要验证域名所有权。传统 CA 的验证方式一般是往 admin@foofish.net 发验证邮件，而 Let's Encrypt 是在你的服务器上生成一个随机验证文件，再通过创建 CSR 时指定的域名访问，如果可以访问则表明你对这个域名有控制权。 首先创建用于存放验证文件的目录，例如：

    mkdir -p var/www/challenges
然后配置一个 HTTP 服务，以 Nginx 为例：(注意：这里的端口是80，不是443）

    server {
        listen 80;
        server_name www.foofish.net foofish.net;
    
        location ^~ /.well-known/acme-challenge/ {
            alias /var/www/challenges/;
            try_files $uri =404;
        }

       ...the rest of your config
    }
    
这个验证服务以后更新证书还要用到，需要一直保留。

####获取网站证书

先把 acme-tiny 脚本保存到之前的 ssl 目录：

    wget https://raw.githubusercontent.com/diafygi/acme-tiny/master/acme_tiny.py
指定账户私钥、CSR 以及验证目录，执行脚本：

    python acme_tiny.py --account-key ./account.key --csr ./domain.csr --acme-dir /var/www/challenges/ > ./signed.crt
如果一切正常，当前目录下就会生成一个 signed.crt，这就是申请好的证书文件。

####安装证书
证书生成后，就可以把它配置在web 服务器上了，需要注意的是，Nginx需要追加一个Let's Encrypt的中间证书，在 Nginx 配置中，需要把中间证书和网站证书合在一起：

    wget -O - https://letsencrypt.org/certs/lets-encrypt-x1-cross-signed.pem > intermediate.pem
    cat signed.crt intermediate.pem > chained.pem
最终，修改 Nginx 中有关证书的配置并 reload 服务即可：

    server {
        listen 443;
        server_name foofish.net, www.foofish.net;
    
        ssl on;
        ssl_certificate /path/to/chained.pem;
        ssl_certificate_key /path/to/domain.key;
        ssl_session_timeout 5m;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA:ECDHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA;
        ssl_session_cache shared:SSL:50m;
        ssl_prefer_server_ciphers on;
    
        ...the rest of your config
    }
    
    server {
        listen 80;
        server_name foofish.net, www.foofish.net;
    
        location /.well-known/acme-challenge/ {
            alias /var/www/challenges/;
            try_files $uri =404;
        }
    
        ...the rest of your config
    }
    
ssl_certificate     ~/www/ssl/chained.pem;
ssl_certificate_key ~/www/ssl/domain.key;
####配置自动更新

Let’s Encrypt 签发的证书只有 90 天有效期，但可以通过脚本定期更新。例如我创建了一个 renew_cert.sh，内容如下：

    #!/bin/bash
    
    cd /home/xxx/www/ssl/
    python acme_tiny.py --account-key account.key --csr domain.csr --acme-dir /home/xxx/www/challenges/ > signed.crt || exit
    wget -O - https://letsencrypt.org/certs/lets-encrypt-x1-cross-signed.pem > intermediate.pem
    cat signed.crt intermediate.pem > chained.pem
    /usr/local/nginx/sbin/nginx -s reload
这个脚本需要以 root 帐号运行，使用绝对路径比较保险。最后，修改 root 帐号的 crontab 配置，加入以下内容：

    0 0 1 * * /home/xxx/root_shell/renew_cert.sh >/dev/null 2>&1
这样以后证书每个月都会自动更新，一劳永逸。实际上，Let’s Encrypt 官方将证书有效期定为 90 天一方面是为了更安全，更重要的是鼓励用户采用自动部署方案。)

kjMixed Content: The page at 'https://foofish.net/' was loaded over HTTPS, but requested an insecure script 'http://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js'. This request has been blocked; the content must be served over HTTPS.


Mixed Content: The page at 'https://foofish.net/' was loaded over HTTPS, but requested an insecure script 'http://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js'. This request has been blocked; the content must be served over HTTPS.
