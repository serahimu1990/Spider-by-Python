# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu.items  import JianshuItem
import re



class JshuSpider(CrawlSpider):
    name = 'jshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['http://jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        # item=JianshuItem()
        title = response.xpath("//h1[@class='title']/text()").get()
        author = response.xpath("//span[@class='name']/a/text()").get()
        pub_time=response.xpath("//span[@class='publish-time']/text()").get().replace("*","")
        url=response.url
        url1=url.split("?")[0]
        article_id = url1.split("/")[-1]
        content = response.xpath("//div[@class='show-content']//text()").getall()
        content =list(map(lambda x: re.sub(r"\s","",x),content))
        content =list(filter(lambda x:x!='',content))
        content =",".join(content)
        word_count=response.xpath("//span[@class='wordage']/text()").get()
        word_count = word_count.split(" ")[-1]
        comment_count = response.xpath("//span[@class='comments-count']/text()").get()
        comment_count=str(comment_count.split(" ")[-1])
        read_count = response.xpath("//div[@class='meta']/span[@class='views-count']/text()").get()
        # read_count = re.search(r'.*(\d+).*', read_count).group(1)
        read_count=read_count.split(" ")[-1]
        like_count = response.xpath("//span[@class='likes-count']/text()").get()
        like_count = like_count.split(" ")[-1]
        subjects = ",".join(response.xpath("//span[@class='include-collection']/a/div/text()").getall())

        item=JianshuItem(title=title,author=author,pub_time=pub_time,url=response.url,article_id=article_id
                         ,content=content,word_count=word_count,comment_count=comment_count,read_count=read_count,
                         like_count=like_count,subjects=subjects)
        # print(item)
        yield item
