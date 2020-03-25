# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import mysql.connector
import MySQLdb

class MysqlPipeline(object):
    def __init__(self):
        self.connection = MySQLdb.connect('localhost', 'root', 'parola123', 'resultsdb')
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        self.cursor.execute("""INSERT INTO tipico (country, league, cl, home, home_country, away, away_country, m_date, m_time, dt, ft1, ft2, ht1, ht2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
        (item['country'], item['league'], item['cl'], item['home'], item['home_country'], item['away'], item['away_country'], item['m_date'], item['m_time'], item['dt'], item['ft1'], item['ft2'], item['ht1'],item['ht2']))
        self.connection.commit()
        return item



