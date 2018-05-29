# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.exceptions import NotConfigured

class LianjiaPipeline(object):
    table_name = 'renting_information'

    def __init__(self, db_config):
        self.db = pymysql.connect(**db_config)
        self.cursor = self.db.cursor()
    
    def process_item(self, item, spider):
        insert_fields = list()
        for field,value in item.items():        
            value = value.replace("'","\\\'")
            value = value.replace('"','\\\"')
            insert_fields.append("`{field}`='{value}'".format(field=field, value=value))        
        
        sql = "insert into {table} set {insert_fields}".format(table=self.table_name, insert_fields=','.join(insert_fields))
        offect_row = self.cursor.execute(sql)
        self.db.commit()
         
        if offect_row != 1:
            print("insert error!", "sql:",sql)        

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()
 
    @classmethod
    def from_crawler(cls, crawler):
        renting_db_config = crawler.settings.get('DB_RENTING')
        if renting_db_config is None:
            raise NotConfigured
        return cls(renting_db_config)
          
