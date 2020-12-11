"""
mac 搭建selenium与ChromeDriver环境
https://www.jianshu.com/p/39716ea15d99

1. 安装 chrome driver，找到你的浏览器对应版本。 http://chromedriver.chromium.org/downloads
2. 下载后放到 path 路径下，比如 mv 到 /usr/local/bin
"""


import datetime as dt
import random
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

MAX_SECONDS = 3600 * 5  # 最多 n 个小时


def main():
    url = "https://weread.qq.com/"
    url = "https://weread.qq.com/web/reader/b253292071697fe1b25cd24"

    c = webdriver.Chrome()
    c.get(url)
    time.sleep(10)  # 登陆一下

    beg = int(time.time())

    while True:
        actions = ActionChains(c)
        if random.choice([True, False]):
            actions.send_keys(Keys.ARROW_RIGHT)
        else:
            actions.send_keys(Keys.ARROW_LEFT)
        print(dt.datetime.now(), c.current_url)
        actions.perform()
        time.sleep(random.randint(15, 30))  # sleep 一下

        if int(time.time()) - beg > MAX_SECONDS:
            break

    c.close()


if __name__ == "__main__":
    main()
