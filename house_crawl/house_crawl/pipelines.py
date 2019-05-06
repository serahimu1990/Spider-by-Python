# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class HouseCrawlPipeline(object):
    def __init__(self):
        # 设置本机数据库的参数，并进行连接
        dbparams={'host':'127.0.0.1','port':3306,'user':'root','password':'','database':'fang','charset':'utf8'}
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        # 执行sql语句，将爬取的数据存入数据库中
        self.cursor.execute(self.sql,(item['province'],item['city'],item['address'],item['name'],item['area'],item['price'],
                                      item['unit'],item['rooms'],item['floor'],item['year'],item['toward'],item['house_url']))
        self.conn.commit()

        return item
    @property
    def sql(self):
        if not self._sql:
            self._sql = """insert into secondhouse(id,省份,城市,位置,小区,面积,总价,单价,房型,所在层,年限,
            朝向,链接) values(Null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            return self._sql
        return self._sql



