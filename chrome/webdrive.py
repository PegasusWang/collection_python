#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver  # 从selenium导入webdriver
import time

"""
常用查找元素方法：

find_element_by_id # ID
find_elements_by_class_name # class
find_elements_by_tag_name # 标签名
find_elements_by_name # name
find_elements_by_link_text # a标签中的text查找（精确匹配）
find_elements_by_partial_link_text #a标签中的text查找（部分匹配即可）
find_elements_by_css_selector # css选择器查找
find_elements_by_xpath # find_elements_by_xpath("//input")，请翻阅文档
"""
driver = webdriver.Chrome('driver/chromedriver.exe')

driver.get('https://www.baidu.com')

input = driver.find_element_by_id('kw')
searchButton = driver.find_element_by_id('su')  # 获取搜索按钮
input.send_keys('python')
searchButton.click()
time.sleep(10)
driver.close()
