# -*- coding: utf-8 -*-
import scrapy
import json
import re
from house_crawl.items import SecondHouseItem

class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs =response.xpath("//div[@class='outCont']//tr")
        procince=None
        for tr in trs:
            tds = tr.xpath(".//td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub(r"\s","",province_text)
            if province_text:
                province=province_text
                if province=='其它':
                    continue
            city_td=tds[1]
            city_links=city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url=city_link.xpath(".//@href").get()
                url_split = city_url.split("//")
                scheme = url_split[0]
                domain = url_split[1]
                # newhouse_url = scheme +"//"+ "newhouse." + domain + "house/s/"
                second_url = scheme +"//"+ "esf." + domain
                # print(city)
                # yield scrapy.Request(url=newhouse_url,callback=self.parse_newhouse,meta={"meta":(province,city)})
                yield scrapy.Request(url=second_url, callback=self.parse_second, meta={"meta": (province, city)})

    # def parse_newhouse(self,response): 新房页面解析，暂时不用
    #     province,city = response.meta.get("meta")
    #     lis = response.xpath("//div[contains(@class,'nl_con')]/ul/li")
    #     for li in lis:
    #         name = li.xpath(".//div[@class='nlcd_name']/a/text()").get().strip()
    #         house_type_list = li.xpath(".//div[contains(@class,'house_type')]/a/text()").getall()
    #         house_type_list=list(map(lambda x:re.sub(r"\s","",x),house_type_list))
    #         rooms= list(filter(lambda x: x.endswith('居'),house_type_list))
    #         area = "".join(li.xpath(".//div[contains(@class,'house_type')]/text()").getall())
    #         area = re.sub(r"\s|/","",area)
    #         address = li.xpath(".//div[@class='address']/a/@title").get()
    #         district_text = "".join(li.xpath(".//div[@class='address']/a//text()").getall())
    #         district = re.search(r".*\[(.+)\].*",district_text).group()
    #         sale = li.xpath(".//div[contains(@class,'fangyuan')]/span/text()").get()
    #         price = "".join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
    #         price = re.sub(r"\s|广告","",price)
    #         origin_url = li.xpath(".//div[@class='nlcd_name']/a/@href").get()
    #         item = NewHouseItem(name=name,rooms=rooms,area=area,address=address,district=district,sale=sale,price=price,
    #                             house_url=origin_url,province=province,city=city)
    #         yield item
    #     next_url = response.xpath("//div[class='page']//a[@class='next']/@href").get()
    #     if next_url:
    #         yield scrapy.Request(url=response.urljion(next_url),callback=self.parse_newhouse,meta={"meta":(province,city)})
    def parse_second(self,response):
        province,city = response.meta.get("meta")
        dls = response.xpath("//div[@class='shop_list shop_list_4']/dl")
        for dl in dls:
            item = SecondHouseItem(province=province,city=city)
            item['name']=dl.xpath(".//p[@class='add_shop']/a/@title").get()
            infos = dl.xpath(".//p[@class='tel_shop']/text()").getall()
            infos = list(map(lambda x: re.sub(r"\s","",x),infos))
            item['floor']=None
            item['toward'] = None
            item['year'] = None
            item['area'] = None
            item['rooms'] = None
            # print(infos)
            for info in infos:
                if '室' in info:
                    item['rooms']=info
                elif '层' in info:
                    item['floor']=info
                elif '向' in info:
                    item['toward']=info
                elif '㎡' in info:
                    item['area']=info
                elif '年' in info:
                    item['year'] = info
            #
            item['address']=dl.xpath(".//p[@class='add_shop']/span/text()").get()
            price=dl.xpath(".//dd[@class='price_right']/span//text()").getall()
            if len(price)>0:
                item['price']=price[0]+price[1]
                item['unit']=price[2]
            else:
                item['price'] = None
                item['unit'] = None
            detail_url = dl.xpath(".//h4[@class='clearfix']/a/@href").get()
            item['house_url'] =response.urljoin(detail_url)


            yield item
        next_url = response.xpath("//div[@class='page_al']/p/a/@href").get()

        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_second,meta={"meta":(province,city)})

        # print(next_url)
