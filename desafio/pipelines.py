# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import csv

import mysql.connector
from mysql.connector import errorcode
from scrapy.exceptions import DropItem

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ActivityPipeline:
    def process_item(self, item, spider):
        return item

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('relatorio.json', 'w')
        self.file.write('[')
        self.items_written = False  # Add this line

    def close_spider(self, spider):
        if self.items_written:
            self.remove_trailing_comma()
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.file.write(line)
        self.items_written = True  # Add this line
        return item

    def remove_trailing_comma(self):
        self.file.seek(self.file.tell() - 2)  # Move the cursor two positions back
        self.file.truncate()  # Remove the comma and newline


class CSVWriterPipeline:
    def open_spider(self, spider):
        self.file = open('relatorio.csv', 'w', newline='', encoding='utf8')
        writer = csv.writer(self.file)
        writer.writerow(['Porto', 'Mercadoria', 'Sentido', 'Volume Diário em Toneladas', 'Volume Diário em Movs'])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        writer = csv.writer(self.file)
        writer.writerow([item['harbor'], item['merchandise'], item['direction'], item['daily_volume_in_tons'], item['daily_volume_in_movs']]) # namedtuple breaks convention public fields have single underscore
        return item
    

class MySqlPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'mysqlroot',
            database = 'db_merchandise'
        )
    
        self.cur = self.conn.cursor()

        self.cur.execute("""DROP TABLE merchandise""")

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS merchandise(
                         id int NOT NULL auto_increment,
                         harbor text,
                         merchandise text,
                         direction text,
                         volume_tons VARCHAR(255),
                         volume_movs VARCHAR(255),
                         PRIMARY KEY (id)
        ) """)

    def process_item(self, item, spider):
        self.cur.execute(""" insert into merchandise(harbor, merchandise, direction, volume_tons, volume_movs) values (%s, %s, %s, %s, %s)""", (
            item['harbor'],
            item['merchandise'],
            item['direction'],
            item['daily_volume_in_tons'],
            item['daily_volume_in_movs']
        ))

        self.conn.commit()

    def close_spider(self, spider):

        self.cur.close()
        self.conn.close()
    
   