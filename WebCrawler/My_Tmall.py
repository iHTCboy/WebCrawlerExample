#!/usr/bin/env python
# coding=utf-8
'''
My_Tmall.py
WebCrawlerExample

Created by HTC at 2018/8/23
Copyright © 2018 iHTCboy. All rights reserved.
'''

import os
import requests
import json
import csv
import random
import re
from datetime import datetime
from urllib import request
import time


class TM_producs(object):
    def __init__(self, storename):
        self.storename = storename
        self.url = 'https://{}.m.tmall.com'.format(storename)
        self.headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 "
                          "(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
        }
        datenum = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.filename = '{}_{}.csv'.format(self.storename, datenum)
        self.get_file()

    def get_file(self):
        '''创建一个含有标题的表格'''
        title = ['item_id', 'product_id', 'price', 'quantity', 'sold', 'title', 'totalSoldQuantity', 'url', 'img']
        with open(self.filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=title)
            writer.writeheader()
        return

    def get_totalpage(self):
        '''提取总页码数'''
        num = random.randint(83739921, 87739530)
        endurl = '/shop/shop_auction_search.do?sort=s&p=1&page_size=12&from=h5&ajson=1&_tm_source=tmallsearch&callback=jsonp_{}'
        url = self.url + endurl.format(num)
        html = requests.get(url, headers=self.headers).text
        infos = re.findall('\(({.*})\)', html)[0]
        infos = json.loads(infos)
        totalpage = infos.get('total_page')
        return int(totalpage)

    def get_products(self, page):
        '''提取单页商品列表'''
        num = random.randint(83739921, 87739530)
        endurl = '/shop/shop_auction_search.do?sort=s&p={}&page_size=12&from=h5&ajson=1&_tm_source=tmallsearch&callback=jsonp_{}'
        url = self.url + endurl.format(page, num)
        html = requests.get(url, headers=self.headers).text
        infos = re.findall('\(({.*})\)', html)[0]
        infos = json.loads(infos)
        products = infos.get('items')
        for product in products:
            del product['titleUnderIconList']
            item_id = product['item_id']
            product_id = self.get_product_spm(item_id)
            product['product_id'] = product_id
            imgUrl = 'https:' + product['img']
            self.save_img(imgUrl, product_id)
            item_id = product['item_id']

        # print(products)
        title = ['item_id', 'product_id', 'price', 'quantity', 'sold', 'title', 'totalSoldQuantity', 'url', 'img']
        with open(self.filename, 'a', encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=title)
            writer.writerows(products)

    def get_product_spm(self, item_id):
        url = 'https://detail.m.tmall.com/item.htm?id={}'.format(item_id)
        html = requests.get(url, headers=self.headers).text
        # {"货号":"07300318000 "}
        product_id = re.findall(r'"货号":"(.+?)"}', html)[0].strip()
        print(product_id)
        return product_id

    def save_img(self, img_url, file_name):
        try:
            # 获得图片后缀
            file_suffix = os.path.splitext(img_url)[1]
            cwd = os.getcwd()
            save_path = os.path.join(cwd, 'images/')
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            image_path = os.path.join(save_path, file_name + file_suffix)
            # 下载图片
            image = requests.get(img_url, headers=self.headers)
            # 命名并保存图片
            with open(image_path, 'wb') as f:
                f.write(image.content)

        except Exception as e:
            print('图片下载错误 ：', file_name, e)

    def main(self):
        '''循环爬取所有页面宝贝'''
        total_page = self.get_totalpage()
        for i in range(1, total_page + 1):
            self.get_products(i)
            print('总计{}页商品，已经提取第{}页'.format(total_page, i))
            time.sleep(1 + random.random())


if __name__ == '__main__':
    storename = 'mgssp'
    tm = TM_producs(storename)
    tm.main()
