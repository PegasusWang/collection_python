# Python 没白学，抓取大佬博客制作电子书

利用 calibre 提供的工具抓取感兴趣的网页导出电子书
最近发现了一位大佬的技术博客感觉非常不错，不过吧文章有点多，长时间盯着屏幕眼睛也受不了。
如果博客使用的是 gitbook、mkdocs 或者 sphinx 之类的文档工具生成的倒还是方便，工具提供了网页导出电子书pdf/epub/mobi 等格式的方式。
不过吧如果没有开放下载，想要看一些博客就比较麻烦了。平常使用电子书居多，就想着要是能把文章合成一本电子书然后放到电子书阅读器上阅读就好了，
于是就开始搜索解决方式看看有没有现成的工具，其实自己写爬虫然后转换也可以，不过稍微麻烦一点。

搜了一下还真让我发现了一种方便的方式，利用 calibre 这个电子书管理工具提供的命令行工具配合简单的 python 脚本就可以实现。

参考：

- https://bookfere.com/tools#calibre
- https://www.jianshu.com/p/0bcb92509309
- https://snowdreams1006.github.io/myGitbook/advance/export.html

# 安装 calibre

在calibre官网下载插件，下载链接：https://calibre-ebook.com/download 下载适合自己系统的版本：

然后在命令行链接环境变量：

`sudo ln -s /Applications/calibre.app/Contents/MacOS/ebook-convert /usr/local/bin`
