#coding=utf-8

import csv
import os
from time import ctime
from time import sleep

import pymysql

#存储数据
class DataStore(object):
    def csv_store(self, name, attr, data, path):
        if os.path.exists('data.csv'):
            with open(path, 'a+', newline='') as csv_file:
                csv_write = csv.writer(csv_file)
                first_item = data[12] + data[1]
                second_item = data[2]
                third_item = data[4]
                fourth_item = data[10]
                fifth_item = data[6]
                sixth_item = data[8]
                csv_write.writerow([name, attr, first_item, second_item, third_item, fourth_item, fifth_item, sixth_item])
                csv_file.close()
        else:
            data = str(data)
            with open(path, 'a+', newline='') as csv_file:
                csv_write = csv.writer(csv_file)
                first_item = data.split('$')[0]
                second_item = data.split('$')[1]
                third_item = data.split('$')[2]
                fourth_item = data.split('$')[3]
                fifth_item = data.split('$')[4]
                sixth_item = data.split('$')[5]

                csv_write.writerow([name, attr, first_item, second_item, third_item, fourth_item, fifth_item, sixth_item])
                csv_file.close()

        return
    #水质信息数据插入数据库
    def insert_database(self, name, attr, data):
        try:
            first_item = data[12] + data[1]
            second_item = data[2]
            third_item = data[4]
            fourth_item = data[10]
            fifth_item = data[6]
            sixth_item = data[8]
            conn = pymysql.connect(host="127.0.0.1", user="root", passwd="xy02012017", db="mypydb")
            cursor = conn.cursor()
            sql = """create table if not exists water_quality(
                                                           station_name varchar(100), 
                                                           attr_name varchar(50),
                                                           update_time varchar(20),
                                                           pH varchar(20),
                                                           O2 varchar(20),
                                                           NH varchar(20),
                                                           Mn varchar(20),
                                                           C varchar(20)
                                                           )engine=innodb char set utf8"""
            cursor.execute(sql)
            sql1 = "insert into comin_fo(station_name, attr_name, update_time, PH, O2, NH, Mn, C) VALUES( %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql1, (name, attr, first_item, second_item, third_item, fourth_item, fifth_item, sixth_item))
            conn.commit()

        except Exception as e:
            print("异常:" + e)

