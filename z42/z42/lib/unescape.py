# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, Tag, NavigableString
import htmlentitydefs
import re
from urlparse import urlparse

BLOD_LINE = re.compile(r"^\s*\*\*[\r\n]+", re.M)

_char = re.compile(r'&(\w+?);')
_dec = re.compile(r'&#(\d{2,4});')
_hex = re.compile(r'&#x(\d{2,4});')


def _char_unescape(m, defs=htmlentitydefs.entitydefs):
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0)


import re
import htmlentitydefs


def unescape(s):
    # First convert alpha entities (such as &eacute;)
    # (Inspired from http://mail.python.org/pipermail/python-list/2007-June/443813.html)
    def entity2char(m):
        entity = m.group(1)
        if entity in htmlentitydefs.name2codepoint:
            return unichr(htmlentitydefs.name2codepoint[entity])
        return u" "  # Unknown entity: We replace with a space.
    t = re.sub(
        u'&(%s);' % u'|'.join(htmlentitydefs.name2codepoint), entity2char, s)

    # Then convert numerical entities (such as &#233;)
    t = re.sub(u'&#(\d+);', lambda x: unichr(int(x.group(1))), t)

    # Then convert hexa entities (such as &#x00E9;)
    return re.sub(u'&#x(\w+);', lambda x: unichr(int(x.group(1), 16)), t)


H_BOLD = (
    'h1',
    'h2',
    'h3',
)
B_BOLD = (
    'h4',
    'h5',
    'h6',
)

BLOCK = set([
    'form',
    'hr',
    'div',
    'table',
    'tr',
    'li',
    'pre',
    'p',
])

BOLD = set([
    'b',
    'strong',
    'i',
    'em',
])

PASS = set([
    'span',
    'font',
])


def html2txt(htm):
    htm = htm.replace(u'*', u'﹡').replace('\r\n', '\n').replace('\r', '\n')

    soup = BeautifulSoup(htm)

    def soup2txt_rtursion(soup):
        li = []
        for i in soup:

            if isinstance(i, NavigableString):

                li.append(i.string)

            else:

                name = i.name
                if name == 'a':
                    s = soup2txt_rtursion(i)
                    ss = s.rstrip()

                    href = i.get('href') or ''
                    href = href.strip().replace(' ', '+')
                    if href not in ss and '\n' not in ss:
                        if href and href.startswith('http') and href != ss:
                            if ss:
                                ss = ss.replace("[", "［").replace("]", "］")
                                href_name = ss
                            else:
                                href_name = urlparse(href).netloc
                            li.append('%s' % ( href_name))
                            #li.append('[[%s %s]]' % (href, href_name))
                        li.append(s[len(ss):])
                    else:
                        li.append(s)
                elif name == 'img':
                    src = i.get('src')
                    if src:
                        # img_url = upyun_fetch_pic(src)
                        li.append(u'\n图:%s\n' % src)
                elif name in ('style', 'script'):
                    pass
                elif name == 'pre':
                    s = soup2txt_rtursion(i)
                    if s:
                        if '\n' in s.strip('\n') and (len(s.encode('utf-8', 'ignore')) / len(s)) < 2:
                            s = '\n{{{\r%s\r}}}\n' % s.replace(
                                '\n', '\r').strip('\r')
                        li.append(s)
                elif name == 'br':
                    li.append("\n")
                else:
                    s = soup2txt_rtursion(i)

                    if name in H_BOLD:
                        if '\n' not in s and '**' not in s:
                            li.append(u'\n== %s ==\n' % s)
                        else:
                            li.append(s)
                    elif name in BLOCK:
                        li.append(u'\n%s\n' % s)
                    elif (name in BOLD or name in B_BOLD) and '**' not in s and '\n' not in s:
                        if s.strip():
                            li.append(u'**%s**' % s)
                    else:
                        li.append(s)

        return u''.join(li)

    s = soup2txt_rtursion(soup)
    s = unescape(s.strip())
    txt = s
    txt = '\n\n'.join(filter(bool, [i.strip() for i in s.split('\n')]))
    txt = txt.replace('\r', '\n')
    txt = BLOD_LINE.sub('**', txt)
    return txt

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print html2txt("""
以下内容按照时间倒叙排列，方便各位阅读，以后不定期更新：<br>(之前发布的内容，不保证符合现状)<br><br>2012.12 <br>豆瓣首席科学家、算法组leader在程序员杂志上发文《下一代个性化推荐系统》<br><a rel="nofollow" href="http://www.programmer.com.cn/14366/" target="_blank">http://www.programmer.com.cn/14366/</a><br><br>2012.12<br>豆瓣高级工程总监段念在letagilefly会议上讲豆瓣的技术团队敏捷实践<br><a rel="nofollow" href="http://letagilefly.com/post/2012/12/douban-agile-practice-8872.html">http://letagilefly.com/post/2012/12/douban-agile-practice-8872.html</a><br><br>2012.10<br>豆瓣设计师在极客公园讲豆瓣FM的设计<br><a rel="nofollow" href="http://www.geekpark.net/cast/view/165236" target="_blank">http://www.geekpark.net/cast/view/165236</a><br>既qcon和openparty之后，极客公园成为下一个豆瓣人爱显摆的地方<br><br>2012.4 QCon Beijing上分享的豆瓣阅读前端技术的slide: <a rel="nofollow" href="https://docs.google.com/presentation/d/1oJud9pei_mm75GG_Rcb2-0ksWtl1hmtYaAt20DSrzV0/present?pli=1#slide=id.p" target="_blank">Web Apps and more</a><br><br>2012.4 QCon Beijing, hongqn分享豆瓣在技术架构上分分合合的经验<br><a rel="nofollow" href="http://www.slideshare.net/hongqn/ss-12662476" target="_blank">分久必合，合久必分</a>, 讲讲豆瓣自己的DAE(douban app engine)的由来和未来<br><br>2012.4 Dpark入驻github，<a rel="nofollow" href="https://github.com/douban/dpark">a Python clone of Spark</a><br><br>2012.2:<br>豆瓣开始用github做开源了，欢迎<a rel="nofollow" href="http://github.com/douban">关注</a><br><br>2012.1 年会上展示的豆瓣代码仓库提交历史的视频  <a rel="nofollow" href="http://site.douban.com/widget/videos/5194602/video/125168/">代码大爆炸</a>，年会播放视频过程中群情激奋，大家齐声高呼“NB”，某些人热泪盈眶<br><br>2011.12 在velocity大会上第一次公开讲豆瓣的DPark系统: <br><a rel="nofollow" href="http://velocity.oreilly.com.cn/2011/index.php?func=session&amp;name=%E6%94%AF%E6%8C%81%E8%BF%AD%E4%BB%A3%E8%AE%A1%E7%AE%97%E7%9A%84MapReduce%E6%A1%86%E6%9E%B6" target="_blank">支持迭代计算的MapReduce框架</a><br><br>2011.12 上海python大会上hongqn的演讲: <a rel="nofollow" href="http://www.slideshare.net/hongqn/python-10461681" target="_blank">python在豆瓣的应用</a><br><br>2011.7  前端工程师在D2大会上讲 <a rel="nofollow" href="http://www.slideshare.net/dexter_yy/mvc-8554206" target="_blank">新版阿尔法城背后的前端MVC实践</a><br><br>2010.12<br>BeansDB大规模重构，底层存储完全自己实现的版本发布<br><a rel="nofollow" href="http://www.douban.com/note/122507891/">beansdb卷土重来</a><br><br>2010.11 前端leader讲<a rel="nofollow" href="http://www.slideshare.net/kejun/f2e-douban">豆瓣前端团队的工作方式</a><br><br>2010.9 前端组leader在webrebuild大会上讲豆瓣的前端架构<br><a rel="nofollow" href="http://hikejun.com/sharing/2010webrebuild/?file=fe-infrastructure.html" target="_blank">关于前端架构，我说的其实是...</a><br><br>2010.9<br>豆瓣想做一个用web技术开发桌面应用的框架，欢迎参与：<a rel="nofollow" href="http://code.google.com/p/onering-desktop/" target="_blank">OneRing Desktop</a><br><br>2010.8<br>豆瓣前端工程师在Open Party讲<a rel="nofollow" href="http://www.slideshare.net/openparty/douban-pulse">HTML5实战</a><br><br>2010.4 hongqn第二次在QCon Beijing讲豆瓣是如何用Python的<br><a rel="nofollow" href="http://www.slideshare.net/hongqn/qcon2010-3881323" target="_blank">Python在Web2.0网站的应用</a><br><br>2010.4 百度技术大会上，<br><a rel="nofollow" href="http://wenku.baidu.com/view/86a70f37f111f18583d05a1b.html" target="_blank">豆瓣数据存储实践</a><br><br>2009.12<br>豆瓣算法组leader在resys技术沙龙上的演讲<br><a rel="nofollow" href="http://www.slideshare.net/clickstone/ss-2756065" target="_blank">豆瓣在推荐领域里的实践和思考</a>  <br><br>2009.12<br>豆瓣开源了自己的KeyValue存储系统，<br><a rel="nofollow" href="http://code.google.com/p/beansdb/" target="_blank">BeansDB</a><br><br>2009.4<br>hongqn第一次在QCon上的演讲，关于豆瓣技术架构变迁的历史  <a rel="nofollow" href="http://www.slideshare.net/hongqn/qcon-beijing-2009" target="_blank">豆瓣网技术架构的发展历程</a> <br><br>2007.12<br><a rel="nofollow" href="http://blog.douban.com/douban/2007/12/17/105/">豆瓣技术团队的指环王文化</a> <br><br><br>one more thing:<br><br><a rel="nofollow" href="http://www.douban.com/photos/album/36150897/">我们不定期举行的happy day</a><br><br><a rel="nofollow" href="http://site.douban.com/110275/">豆瓣招聘小站</a>, 内有软文和照片若干<br><br><a rel="nofollow" href="http://www.douban.com/note/149378596/">豆瓣这些Geeks</a></div></div>
""")
    print unescape("""<option value='&#20013;&#22269;&#35821;&#35328;&#25991;&#23398;&#31995;'>&#20013;&#22269;&#35821;&#35328;&#25991;&#23398;&#31995;</option>""")


