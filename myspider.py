"""Description
- 实现抓取水质信息
- python 版本：Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12)
Info
- author : "leeyoung"
- email : "reusleeyoung@163.com"
- date   : "2017.11.10"
"""

#coding=utf-8

import re
import urllib.request
from time import ctime,sleep
from bs4 import BeautifulSoup

import proxy
from datastore import DataStore


class HtmlParser(object):
    def __init__(self):
        self.storage = DataStore()
        #self._start()

    #def _start(self):
        #self.storage.csv_store('水质自动监测站','断面属性','测量时间$pH$溶解氧$氨氮$高锰酸盐指数$总有机碳','data.csv')

    def get_info(self, start_url):
        try:
            data = proxy.proxy_request(start_url)
            soup = BeautifulSoup(data, 'lxml')
            total_data = soup.find_all(type="hidden")
            temp_num = 1
            for data in total_data:
                temp_data = data.get('value')
                if temp_num == 2:
                    data_list = temp_data.split('!!')
                if temp_num == 3:
                    station_list = temp_data.split('!!')
                if temp_num == 4:
                    attr_list = temp_data.split('!!')
                if temp_num >= 5:
                    break
                else:
                    temp_num += 1

        except Exception as e:
            print("exception:" + str(e))
            sleep(1)

        return data_list, station_list, attr_list

    #数据拆分
    def split_data(self, data_list, station_list, attr_list):
        station_dict = {}
        attr_dict = {}
        data_dict = {}
        #去除列表中的空值
        while '' in data_list:
            data_list.remove('')
        while '' in station_list:
            station_list.remove('')
        while '' in attr_list:
            attr_list.remove('')
        try:
            for i in data_list:
                Data = i.split('$')
                data_num = i.split('$')[0]
                data_dict[data_num] = Data

            for j in station_list:
                station_num = j.split('$')[0]
                station_name = j.split('$')[1]
                station_dict[station_num] = station_name

            for k in attr_list:
                attr_num = k.split('$')[0]
                attr_name = k.split('$')[1]
                attr_dict[attr_num] = attr_name

        except Exception as e:
            print("exception:" + str(e))
            sleep(1)
        return data_dict, station_dict, attr_dict

    #保存到本地CSV文件
    def data_store(self, data_dict, station_dict, attr_dict):
        try:
            for key in station_dict:
                self.storage.csv_store(station_dict[key], attr_dict[key], data_dict[key], 'data.csv')

        except Exception as e:
            print("exception:" + str(e))
            sleep(1)

    #保存到数据库
    def insert_mysql(self, data_dict, station_dict, attr_dict):
        try:
            for key in station_dict:
                self.storage.insert_database(station_dict[key], attr_dict[key], data_dict[key])

        except Exception as e:
            print("exception:" + str(e))
            sleep(1)


if __name__ == "__main__":
    print("start at: ", ctime())
    start_url = "http://online.watertest.com.cn/#"
    html_par = HtmlParser()
    #数据信息列表
    data_list, station_list, attr_list = html_par.get_info(start_url)
    data_dict, station_dict, attr_dict = html_par.split_data(data_list, station_list, attr_list)
    #html_par.data_store(data_dict, station_dict, attr_dict)
    html_par.insert_mysql(data_dict, station_dict, attr_dict)
    print("end at：", ctime())







