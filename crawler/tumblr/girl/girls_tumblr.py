#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..crawler import Spider
from ..tumblr_api import TumblrApi
from bs4 import BeautifulSoup
import lxml
import re
import requests
import time


# for recursive fetch
def fetch_html(url, retries=5):
    try:
        html = requests.get(url, timeout=20).text
    except:
        if retries > 0:
            print 'fetching...', retries, url
            time.sleep(3)
            return fetch_html(url, retries-1)
        else:
            print 'fetch failed', url
            return ''
    return html


def get_media_url_list(url):
    if not url:
        return []
    print 'fetch html...', url
    html = fetch_html(url)
    if not html:
        return []
    soup = BeautifulSoup(html, 'lxml')
    img_tag_list = soup.find_all('img')
    url_list = [i.get('src') for i in img_tag_list if i]
    return set(url_list)


class HotgirlsfcSpider(Spider):

    def get_img(self, url='http://hotgirlsfc.tumblr.com/'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        media_list = soup.find_all('div', class_='img')
        img_list = [i.find('img') for i in media_list if i]
        url_list = [i.get('src') for i in img_list if i]
        return set(url_list)


class MzituSpider(Spider):

    def get_img(self, url='http://www.mzitu.com/'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        img_list = soup.find_all('img', class_='lazy')
        url_list = [i.get('data-original') for i in img_list if i]
        return set(url_list)


class LovelyasiansSpider(Spider):
    def get_img(self, url='http://lovely-asians.tumblr.com'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        img_list = soup.find_all('img')
        url_list = [i.get('src') for i in img_list if i]
        url_list = [i for i in url_list if 'media.tumblr' in i]
        return set(url_list)


class KormodelsSpider(Spider):
    def get_post_img_list(self, url):
        """fetch http://kormodels.tumblr.com/post page"""
        print 'fetch...post', url
        html = fetch_html(url)
        soup = BeautifulSoup(html, 'lxml')
        img_tag_list = soup.find_all('meta', attrs={'property': 'og:image'})
        url_list = [i.get('content') for i in img_tag_list if i]
        return set(url_list)

    def get_gif(self, url='http://kormodels.tumblr.com/tagged/gifs/'):
        url_list = self.get_img(url)
        url_list = [i for i in url_list if 'gif' in i]
        return url_list

    def get_img(self, url='http://kormodels.tumblr.com/'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        a_tag_list = soup.find_all('a')
        href_list = [i.get('href') for i in a_tag_list if i]
        href_list = [i for i in href_list if 'kormodels.tumblr.com/post' in i]
        url_list = []
        for each in set(href_list):
            time.sleep(2)
            img_list = self.get_post_img_list(each)
            url_list.extend(list(img_list))
        return set(url_list)


class FerchoechoSpider(Spider):
    def get_img(self, url='http://ferchoecho.tumblr.com'):
        url_list = list(get_media_url_list(url))
        return [i for i in url_list if 'media.tumblr' in i]


class Girl2chickSpider(Spider):
    def get_img(self, url='http://girl2chick.tumblr.com/'):
        url_list = list(get_media_url_list(url))
        return [i for i in url_list if 'media.tumblr' in i]


class KoreangirlshdSpider(Spider):
    def get_img(self, url='http://koreangirlshd.com/'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        post_tag_list = soup.find_all('div', class_='entry-content')
        img_tag_list = [i.find('img') for i in post_tag_list if i]
        a_list = [i.find('a') for i in post_tag_list if i]
        url_list = [i.get('src') for i in img_tag_list if i]
        href_list = [i.get('href') for i in a_list if i]
        for each in set(href_list):
            time.sleep(2)
            url_list.extend(list(get_media_url_list(each)))

        return set(url_list)



class SnsdpicsSpider(Spider):
    def get_img(self, url='http://snsdpics.com'):    # /page/n
        s = KoreangirlshdSpider()
        return s.get_img(url)


class PassionNipponesSpider(Spider):
    def get_post_img_list(self, url):
        print 'fetch...passion', url
        html = fetch_html(url)
        soup = BeautifulSoup(html, 'lxml')
        img_tag_list = soup.find_all('img')
        href_list = [i.get('src') for i in img_tag_list if i]
        url_list = [i for i in href_list if 'ekladata' in i]
        return set(url_list)

    def get_img(self, url='http://passion-nippones.tumblr.com'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        a_tag_list = soup.find_all('a')
        href_list = []
        for each in a_tag_list:
            href = each.get('href', None)
            if href and 'eklablog' in href:
                href_list.append(href)
        url_list = []
        for each in set(href_list):
            time.sleep(2)
            img_list = self.get_post_img_list(each)
            url_list.extend(list(img_list))
        return set(url_list)


class Sossex1Spider(Spider):
    def get_img(self, url='http://sossex1.tumblr.com'):
        img_list = get_media_url_list(url)
        img_list = [i for i in img_list if i and 'media.tumblr' in i]
        return set([i for i in img_list if 'avatar' not in i])


class HotcosplaychicksSpider(Spider):
    """from 1 to 966"""
    def get_img(self, url='http://hotcosplaychicks.tumblr.com'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if i and 'media.tumblr' in i])


class ForchiSpider(Spider):
    def get_img(self, url='http://forchi.tumblr.com'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if i and 'media.tumblr' in i])


class ChinabeautiesSpider(Spider):
    """from 1 to 660"""
    def get_img(self, url='http://chinabeauties.tumblr.com'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if i and 'media.tumblr' in i])


class BestofasiangirlsSpider(Spider):
    def get_img(self, url='http://bestofasiangirls.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if i and 'media.tumblr' in i])


class TattoocnSpider(Spider):
    def get_img(self, url='http://tattoocn.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if i and 'media.tumblr' in i])


class HappylimSpider(Spider):
    def get_post_url_list(self, href_list):
        prefix = 'http://hello-happylim-blog.tumblr.com/post'
        href_list = [i for i in href_list if i and prefix in i]
        href_list = [i for i in href_list if 'embed' not in i and
                     'note' not in i]
        return href_list

    def get_post_img_list(self, url):
        """fetch http://kormodels.tumblr.com/post page"""
        print 'fetch...post', url
        html = fetch_html(url)
        soup = BeautifulSoup(html, 'lxml')
        img_tag_list = soup.find_all('meta', attrs={'property': 'og:image'})
        url_list = [i.get('content') for i in img_tag_list if i]
        return set(url_list)

    def get_img(self, url='http://hello-happylim-blog.tumblr.com/'):
        html = fetch_html(url)
        soup = BeautifulSoup(html, 'lxml')
        a_tag_list = soup.find_all('a')
        href_list = []
        for each in a_tag_list:
            href_list.append(each.get('href', None))
        href_list = self.get_post_url_list(href_list)

        img_list = []
        for each_url in set(href_list):
            time.sleep(2)
            img_list.extend(list(self.get_post_img_list(each_url)))
        return set(img_list)

class HonkawaSpider(Spider):
    def get_img(self, url='http://honkawa.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if 'media.tumblr' in i])


class Touch45Spider(Spider):
    def get_img(self, url='http://touch45.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if 'media.tumblr' in i])


class GigachaossSpider(Spider):
    def get_img(self, url='http://gigachaoss.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if 'media.tumblr' in i])


class JgiriSpider(Spider):
    def get_img(self, url='http://j-giri-gl.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if 'media.tumblr' in i])


class IdolmaniaxSpider(Spider):
    def get_img(self, url='http://idolmaniax.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if 'media.tumblr' in i])


class TokuninaidesuSpider(Spider):
    def get_img(self, url='http://tokuninaidesu.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if 'media.tumblr' in i])


class SilymarinSpider(Spider):
    def get_img(self, url='http://silymarin.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if 'media.tumblr' in i])


class ChioeveSpider(Spider):
    def get_img(self, url='http://chioeve.com/'):
        prefix = 'http://chioeve.com/'
        img_list = get_media_url_list(url)
        return set([prefix+i for i in img_list if 'uploads' in i])


class HotGirlsAsiaSpider(Spider):
    """
    def get_img(self, url='http://hot-girls-asia.tumblr.com/api/read/json?start=0'):
        #self.base_url = 'http://hot-girls-asia.tumblr.com/api/read/json?start=0'
        self.total_post_re = re.compile(r'"posts-total":(\d+),')
        self.img_re = re.compile(r'photo-url-1280":"(http.*?)",')
        html = fetch_html(url)
        imgs = self.img_re.findall(html)
        imgs = [img.replace('\\', '') for img in imgs if img]
        return set(imgs)
    """
    def get_img(self, url='http://hot-girls-asia.tumblr.com/api/read/json?start=1'):
        tumblr_api = TumblrApi(url)
        return tumblr_api.get_img_set()


class OshiriSpider(Spider):
    def get_img(self, url='http://honkawa-oshiri.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if 'media.tumblr' in i])


class VisualangelSpider(Spider):
    def get_img(self, url='http://visualangel.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if 'media.tumblr' in i and '500' in i])


class Blendy99Spider(Spider):
    def get_img(self, url='http://blendy99.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if 'media.tumblr' in i])


class AdnisSpider(Spider):
    def get_img(self, url='http://adnis.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i.replace('250', '1280') for i in img_list if 'media.tumblr' in i])


class JoanpeperoSpider(Spider):
    """not to add upload_all"""
    def get_img(self, url='http://joanpepero.tumblr.com/'):
        html = fetch_html(url)
        soup = BeautifulSoup(html, 'lxml')
        iframe_tag_list = soup.find_all('iframe', class_='photoset')
        url_list = []
        for i in iframe_tag_list:
            url_list.append(i.get('src'))
        img_url_list = []
        for each in url_list:
            img_url_list.extend(get_media_url_list(each))
        return set(img_url_list)


class AoababofanSpider(Spider):
    def get_img(self, url='http://aoababofan.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if 'media.tumblr' in i])


class LegloveworldSpider(Spider):
    """from 1 to 3628"""
    def get_img(self, url='http://legloveworld.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if 'media.tumblr' in i])


class KawaiilegSpider(Spider):
    def get_img(self, url='http://kawaiileg.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i.replace('250', '1280') for i in img_list if 'media.tumblr' in i])


class GanpukudouSpider(Spider):
    """from 1 to 8000"""
    def get_img(self, url='http://ganpukudou.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i.replace('250', '1280') for i in img_list if 'media.tumblr' in i])


class HeypantyhoseSpider(Spider):
    """from 1 to 170"""
    def get_img(self, url='http://heypantyhose.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i.replace('400', '1280') for i in img_list if 'media.tumblr' in i])


class SexyLadyJapanSpider(Spider):
    """from 1 to 350"""
    def get_img(self, url='http://sexy-lady-japan.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i.replace('400', '1280') for i in img_list if 'media.tumblr' in i])


class SekkusuSpider(Spider):
    """from 1 to 7800"""
    def get_img(self, url='http://sekkusu.tumblr.com/'):
        img_list = get_media_url_list(url)
        img_list = [i.replace('500', '1280') for i in img_list if 'media.tumblr' in i]
        return set([i for i in img_list if 'avatar' not in i])


class JacyliuSpider(JoanpeperoSpider):
    """not to add upload_all"""
    def get_img(self, url='http://jacyliu.tumblr.com/'):
        return super(JacyliuSpider, self).get_img(url)


class GirlFixSpider(Spider):
    def get_img(self, url='http://girl-fix.com/'):
        img_list = get_media_url_list(url)
        img_list = [i.replace('500', '1280') for i in img_list if 'media.tumblr' in i]
        return set([i for i in img_list if 'avatar' not in i])


class SmallPigSpider(Spider):
    def get_img(self, url='http://small-pig.tumblr.com/'):
        img_list = get_media_url_list(url)
        img_list = [i.replace('500', '1280') for i in img_list if 'media.tumblr' in i]
        return set([i for i in img_list if 'avatar' not in i])


class MoreangelsSpider(Spider):
    def get_img(self, url='http://moreangels.tumblr.com/'):
        img_list = get_media_url_list(url)
        img_list = [i.replace('500', '1280') for i in img_list if 'media.tumblr' in i]
        return set([i for i in img_list if 'avatar' not in i])


class DoumigirlsSpider(Spider):
    def get_img(self, url='http://www.doumigirls.com/'):
        img_list = get_media_url_list(url)
        img_list = [i.replace('500', '1280') for i in img_list if 'media.tumblr' in i]
        return set([i for i in img_list if 'avatar' not in i])


class IdoljpSpider(Spider):
    """from 1 to 2650"""
    def get_img(self, url='http://idoljp.tumblr.com/'):
        img_list = get_media_url_list(url)
        return set([i for i in img_list if i and 'media.tumblr' in i])


class TokujiroSpider(Spider):
    """from 1 to 2500"""
    def get_img(self, url='http://tokujiro.tumblr.com/'):
        img_list = get_media_url_list(url)
        img_list = [i.replace('250', '1280') for i in img_list if 'media.tumblr' in i]
        return set([i for i in img_list if 'avatar' not in i])
