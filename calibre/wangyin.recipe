#!/usr/bin/python
# encoding: utf-8

from calibre.web.feeds.recipes import BasicNewsRecipe # 引入 Recipe 基础类

class Wang_Yin_Blog(BasicNewsRecipe): # 继承 BasicNewsRecipe 类的新类名

    #///////////////////
    # 设置电子书元数据
    #///////////////////
    title = '当然我在扯淡' # 电子书名
    description = u'王垠的博客' # 电子书简介
    #cover_url = '' # 电子书封面
    #masthead_url = '' # 页头图片
    __author__ = '王垠' # 作者
    language = 'zh' # 语言
    encoding = 'utf-8' # 编码

    #///////////////////
    # 抓取页面内容设置
    #///////////////////
    #keep_only_tags = [{ 'class': 'example' }] # 仅保留指定选择器包含的内容
    no_stylesheets = True # 去除 CSS 样式
    remove_javascript = True # 去除 JavaScript 脚本
    auto_cleanup = True # 自动清理 HTML 代码
    delay = 5 # 抓取页面间隔秒数
    max_articles_per_feed = 999 # 抓取文章数量

    #///////////////////
    # 页面内容解析方法
    #///////////////////
    def parse_index(self):
        site = 'http://www.yinwang.org' # 页面列表页
        soup = self.index_to_soup(site) # 解析列表页返回 BeautifulSoup 对象
        links = soup.findAll("li",{"class":"list-group-item title"}) # 获取所有文章链接
        articles = [] # 定义空文章资源数组
        for link in links: # 循环处理所有文章链接
            title = link.a.contents[0].strip() # 提取文章标题
            url = site + link.a.get("href") # 提取文章链接
            a = {'title': title , 'url':url} # 组合标题和链接
            articles.append(a) # 累加到数组中
        ans = [(self.title, articles)] # 组成最终的数据结构
        return ans # 返回可供 Calibre 转换的数据结构
