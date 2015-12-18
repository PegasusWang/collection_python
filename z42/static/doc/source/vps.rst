
.. _vps_tutorial: 

==================================================
VPS 开发服务器初始配置
==================================================

:作者: 王然 kxxoling@gmail.com


将域名配置到 DNSPOD
-----------------------

首先需要注册一个 DNSPOD 账号，并拥有一个未使用的一级域名，没有的话需要在域名提供商
（比如 `GoDaddy <http://godaddy.com>`_ ）那里购买。

* 在 DNSPOD 中添加你已注册的域名信息
* 添加一级域名记录以及泛域名记录，并指向你的 VPS IP
* 在域名购买商那里将域名解析服务器修改为 DNSPOD 提供的域名解析服务器

.. raw:: html

    <script type="text/javascript">
      document.createElement('video');document.createElement('audio');document.createElement('track');
    </script>
    <link href="//vjs.zencdn.net/4.6/video-js.css" rel="stylesheet">
    <script src="//vjs.zencdn.net/4.6/video.js"></script>
    <video id="example_video_1" class="video-js vjs-default-skin"
      controls preload="auto" width="640" height="264"
      data-setup='{"example_option":true}'>
      <source src="//dn-pevc.qbox.me/DNSPOD.mp4" type='video/mp4' />
    </video>


配置 VPS
-----------------------

根据邮件提示以 root 用户登录 VPS（ssh root@your.domain），系统已为你创建了一个叫做 zz 的用户，现在为他创建密码：::

	passwd zz

根据提示完成后退出 ssh。

接下来配置无密码登录 VPS。首次使用 ssh 密钥登录需要在本地创建 ssh 密钥：

Mac & Linux: `ssh-keygen` ，该命令会在 home 目录 .ssh 文件夹中创建两个文件：
id_rsa 和 id_rsa.pub。形式如下：

将密钥拷贝到服务器：

Linux ::

    `ssh-copy-id zz@your.domain`

Mac 下等价命令 ::

    `cat ~/.ssh/id_rsa.pub | ssh zz@your.domain "mkdir ~/.ssh; cat - >> authorized_keys"`


windows用户可以参考 :ref:`xshell` 配置xshell


配置开发环境
------------------------

使用 zz 用户登录 VPS，并在本地生成密钥 `ssh-keygen`

将 `~/.ssh/id_rsa.pub` 中全部内容（公钥）复制到 `BitBucket`。 https://bitbucket.org/account/user/youritbucket-b-id/ssh-keys/。

fork `42web 源代码 <https://bitbucket.org/zuroc/42web>`_

修改 ~/.hgrc 文件，在此设置全局用户名&邮箱

修改 ~/42web/.hg/hgrc 文件，修改修改为如下::

	[paths]
	default = ssh://hg@bitbucket.org/your-bitbucket-id/42web
	zsp = ssh://hg@bitbucket.org/zuroc/42web

接下来将代码更新到最新（要求当前目录在 hg 版本控制的目录）::
    hg fetch zsp

如何 pull request


运行初始化脚本
-------------------------

在 ~/42web/zapp/SITE/misc/once 目录中运行脚本 ./init.sh
（~/42web/zapp/SITE/misc/once/init.sh ）

修改 ~/42web/zapp/SITE/misc/config/nginx/vps1884/zz.conf 内容如下::

    upstream hi-acg_com{
          server 127.0.0.1:4222  max_fails=3  fail_timeout=10s;
    }
    server {
        server_name doc.hi-acg.com;
        location /{
            root /home/zz/42web/static/doc/build/html;
        }
    }
    server {
        server_name hi-acg.com *.hi-acg.com;
    
        location ~ ^/(favicon\.ico|crossdomain\.xml|robots.txt) {
            expires max;
            root /home/zz/42web/static/SITE;
        }
    
        location /{
            expires -1;
            proxy_set_header Host $host;
            proxy_pass http://hi-acg_com;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            access_log /var/log/nginx/hi-acg.com.access_log main;
            error_log /var/log/nginx/hi-acg.com.error_log info;
        }
        location /css{
            expires -1;
            root /home/zz/42web;
        }
        location /js{
            expires -1;
            root /home/zz/42web;
        }
    }


在 ~/42web/zapp/SITE/misc/config/_host/主机名.py 文件修改为如下内容，并注意将 HOST 修改为自己的域名::

    import _env
    from z42 import config
    
    def prepare(o):
        config.SMTP.SENDER = config.SMTP.USERNAME = 'postmaster@42.sendcloud.org'
        config.SMTP.PASSWORD = '密码见Google Docs'
        config.SMTP.HOST = 'smtpcloud.sohu.com'
        config.HOST = "hi-acg.com"
        config.MYSQL_PASSWORD = "密码见Google Docs"
        config.MYSQL_HOST = "127.0.0.1"
        config.MYSQL_USER = "zz"   

 
    def finish(o):
        pass


因为用户配置的优先级 > 主机配置 > 全局

启动开发脚本，首次运行会比较缓慢。运行完成后请勿关闭此脚本::

    ~/42web/zapp/SITE/dev.sh

如开发过程中涉及到邮件功能，需要启另外一个脚本::
    
    python ~/42web/zapp/SITE/model/gearman/server/run.py

（如需要启动 Gearman 请输入 `sudo service gearmand restart` ）


配置数据库
---------------------------

在 `42web/zapp/SITE/misc/backup/mysql/` 目录下运行以下语句修改数据库::

    mysql -h127.0.0.1 -uzz -prstfsgbcedh zz_42web < zz_42web.sql


配置 SMTP
-------------------------

修改配置文件中的邮件服务器配置。

全局配置：42web/z42/config/default.py
个人配置：42web/zapp/SITE/misc/config/_host/主机名.py

如个人配置与全局配置冲突，个人配置将覆盖全局配置。可以在 42web 目录下运行 `ipython` ，并输入
`from z42.config import SMTP; print SMTP.HOST; print SMTP.PASSWD` 测试是否覆盖配置成功。

最后，修改 42web/z42/web/smtp.py 中的邮箱并运行，测试是否配置成功。


配置 phpMyAdmin 访问域名
-----------------------------------------------

修改文件 `/etc/nginx/config/phpmyadmin.conf` ，将其中 server_name 修改为自己想用的二级域名，比如 admin.hi-acg.com。


安装 RockMongo
---------------------------------------------

下载 RockMongo 源代码::

    sudo git clone https://github.com/iwind/rockmongo.git /var/www/rockmongo

会将源代码下载在 /var/www 目录。

下载依赖::

    sudo emerge =dev-php/pecl-mongo-1.5.1 --autounmask-write
    sudo etc-update
    -3
    y
    sudo emerge =dev-php/pecl-mongo-1.5.1

添加配置文件： `sudo vi /etc/nginx/conf/rockmongo.conf` 并添加以下内容::

    server{
        listen       80;
        server_name  mongo.kanrss.com;       #这里修改为自己的域名
        index  index.php;
        root  /var/www/rockmongo;
    
        location ~ \.php$ {
            root  /var/www/rockmongo;
    
            fastcgi_pass  127.0.0.1:9000;
            fastcgi_index index.php;
            include /etc/nginx/fastcgi.conf;
            include        fastcgi_params;
        }
    }

再修改 rockmongo 配置文件 /var/www/rockmongo/config.php 中变量 $MONGO["servers"][$i]["mongo_auth"] 和 $MONGO["servers"][$i]["control_auth"] 为 false，以配置 rockmongo 无密码登录。

重新启动 php-fpm ：`sudo service php-fpm restart`

Nginx 重新加载文件：`sudo service nginx reload`

