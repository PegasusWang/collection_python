# -*- coding: utf-8 -*-

import time
from urlparse import urljoin
import concurrent.futures
from lxml import etree
from crawler_utils import (logged_class, retry_get_html, retry_get,
                           proxy_get_html, lazy_property, ObjectDict)
try:
    from tornado.escape import utf8 as makes
except ImportError:
    from misc.util import makes

retry_get_html = proxy_get_html    # use proxy get html


class Site(object):
    """用来生成站点的商品列表页面"""
    """
    category_url_range = {
        'http://www.fantasyhairbuy.com/c/brazilian-hair_0371/%d.html': (1, 1),
    }
    """
    def __init__(self, category_url_range=None):
        if category_url_range is not None:
            self.category_url_range = category_url_range

    def generate_category_urls(self):
        """生成商品列表页面的url"""
        for url, page_range in self.category_url_range.items():
            for page_num in range(page_range[0], page_range[1]+1):
                yield url % page_num

    def generate_item_urls(self):
        """根据列表页拿到每个列表页面所有的商品url"""
        raise NotImplementedError()


@logged_class
class XpathCrawler(object):
    """用来抓取单个商品信息页面的爬虫"""
    xpath_dict = {}

    def __init__(self, url, xpath_dict=None):
        self.url = url    # 商品url
        if xpath_dict is not None:
            self.xpath_dict = xpath_dict

    @lazy_property
    def html(self):
        return retry_get_html(self.url)

    @lazy_property
    def parser(self):
        return etree.HTML(self.html)

    def get_field(self, field):
        """定义默认xpath解析方法，如果自定义方法，用get_作为开头覆盖默认get_field"""
        func_name = 'get_' + field
        xpath_str = self.xpath_dict.get(field)
        if hasattr(self, func_name):
            return getattr(self, func_name)(xpath_str)
        else:
            self.logger.debug(field, self.url)
            return self.parser.xpath(xpath_str)[0].strip() if xpath_str else ''

    def get_result(self):
        xpath_result = {}
        for field, xpath_string in self.xpath_dict.items():
            xpath_result[field] = makes(self.get_field(field))    # to utf8
        return xpath_result

    def get_link(self, xpath_str=None):
        return self.url


class FantasyhairbuySite(Site):
    domain = 'http://www.fantasyhairbuy.com/'
    category_url_range = {
        'http://www.fantasyhairbuy.com/c/brazilian-hair_0371/%d.html': (1, 1),
    }

    def generate_category_urls(self):
        html = retry_get_html(self.domain)
        parser = etree.HTML(html)
        category_xpath_str = '//*[@id="nav"]/div/div/ul//a/@href'
        category_hrefs = parser.xpath(category_xpath_str)
        category_urls = []
        for href in category_hrefs:
            category_urls.append(urljoin(self.domain, href))
        for url in category_urls:
            parser = etree.HTML(retry_get_html(url))
            try:
                page_str = parser.xpath('//div[@class="cur"]/text()')[0]
                num = int(page_str.split('/')[1])
            except Exception:
                num = 1
            for page_num in range(1, num+1):
                yield url + '/%d.html' % page_num

    def generate_item_urls(self):
        """遍历站点的目录页，返回所有目录页的商品url列表"""
        category_url_list = self.generate_category_urls()
        href_xpath = """//div[@id="prod_list"]//a[@class="pic_box"]/@href"""
        for category_url in category_url_list:
            html = retry_get_html(category_url)
            parser = etree.HTML(html)
            href_list = parser.xpath(href_xpath)
            for href in href_list:
                yield urljoin(self.domain, href)


class FantasyhairbuyCrawler(XpathCrawler):

    xpath_dict = {
        'availability': '//span[@class="prod_info_inventory"]/text()',
        'condition': '',
        'description': '//div[@class="widget prod_info_brief"]/text()',
        'image_link': '//meta[@property="og:image"]',
        'link': '',
        'title': '//div[@class="widget prod_info_title"]//text()',
        'price': '//div[@class="widget price_left price_0"]/del/text()',
        'brand': '',
        'sale_price': '//*[@id="cur_price"]/text()',
    }

    def get_price(self, xpath_str):
        price_str = self.parser.xpath(xpath_str)[0].strip()   # "USD $12.3"
        return price_str.split()[1]

    def get_condition(self, xpath_str):
        return 'new'

    def get_image_link(self, xpath_str):
        return urljoin(self.url, self.parser.xpath(xpath_str)[0].get('content'))

    def get_description(self, xpath_str):
        try:
            return self.parser.xpath(xpath_str)[0].strip() if xpath_str else ''
        except IndexError:    # 该网站一些商品没有简介
            return ''

    def get_result(self):
        xpath_result = super(FantasyhairbuyCrawler, self).get_result()
        # http://www.fantasyhairbuy.com/8-30-inch-whosale-price-full-cuticle-virgin-indian-straight-tangle-free-hair-weaves_p0050.html
        item_id = xpath_result['link'].rsplit('.', 1)[0].split('_')[1]    # extract id from url
        xpath_result['item_id'] = item_id
        return xpath_result


class FantasyhairbuyManager(object):
    domain = 'http://www.fantasyhairbuy.com/'

    def __init__(self, site_class=FantasyhairbuySite,
                 xpath_crawler_class=FantasyhairbuyCrawler):
        self.site = site_class()
        self.xpath_crawler = xpath_crawler_class
        self.results = []

    def sleep_run(self, seconds=3):
        item_urls = set(self.site.generate_item_urls())
        for url in item_urls:
            time.sleep(seconds)
            crawler = self.xpath_crawler(url)
            res_dict = crawler.get_result()
            self.results.append(res_dict)

    def run(self):
        item_urls = set(self.site.generate_item_urls())
        xpath_crawler_list = (self.xpath_crawler(url) for url in item_urls)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {
                executor.submit(c.get_result): c.url for c in xpath_crawler_list
            }
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    res_dict = future.result()
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                else:
                    self.results.append(res_dict)


URL_TO_MANAGER = {
    'http://www.fantasyhairbuy.com/': FantasyhairbuyManager
}


def main():
    from pprint import pprint
    f = FantasyhairbuyManager()
    f.run()
    for d in f.results:
        for k, v in d.items():
            print(k)
            pprint(v)

if __name__ == '__main__':
    main()

