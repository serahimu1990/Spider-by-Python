# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
# from scrapy.exporters import JsonLinesItemExporter
class JianshuPipeline(object):
    # def __init__(self):
    #     self.fp=open('article.json','wb')
    #     self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False)
    # def process_item(self,item,spider):
    #     self.exporter.export_item(item)
    #     print('finish one')
    #     return item
    # def close_spider(self,spider):
    #     self.fp.close()



    def __init__(self):
        dbparams={'host':'127.0.0.1','port':3306,'user':'root','password': '', 'database':'jianshu2'\
            ,'charset':'utf8'}
        self.conn=pymysql.connect(**dbparams)
        self.cursor=self.conn.cursor()
        self._sql=None
    def process_item(self, item, spider):
        self.cursor.execute(self.sql,(item['title'],item['author'],item['pub_time'],item['article_id'],item['content'],
                                     item['url'],item['word_count'],item['comment_count'],item['read_count'],
                                      item['like_count'],item['subjects']))
        self.conn.commit()
        print("finish one")

        return item
    @property
    def sql(self):
        if not self._sql:
            self._sql="""insert into article(id,title,author,pub_time,article_id,content,url,word_count,
            comment_count,read_count,like_count,subjects) values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql
