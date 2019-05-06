# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http.response.html import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class JianshuDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.chrome_options=Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')

        self.driver = webdriver.Chrome(executable_path=r"C:\Users\zhuxi\Documents\chromedriver_win32\chromedriver.exe",
                                       chrome_options=self.chrome_options)

    def process_request(self,request,spider):
        self.driver.get(request.url)
        time.sleep(1)
        try:
            while True:
                ShowMore = self.driver.find_element_by_class_name('show-more')
                ShowMore.click()
                time.sleep(0.3)
                if not ShowMore:
                    break
        except:
            pass
        source =self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url,body=source,request=request,encoding='utf-8')
        return response


