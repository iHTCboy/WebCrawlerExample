#!/usr/bin/env python
#coding=utf-8
'''
Geeker.py

Created by HTC at 2019-04-24
Copyright © 2019 iHTCboy. All rights reserved.
'''

import re
import os
import json
import requests
from requests import session
from bs4 import BeautifulSoup


# 下载和解析html dom树
def downloadDomTree():
    path = '/Users/htc/Desktop/abc.html'
    htmlfile = open(path, 'r', encoding='utf-8')
    htmlhandle = htmlfile.read()
    soup = BeautifulSoup(htmlhandle, 'html.parser')
    # url = 'https://time.geekbang.org/column/intro/43'
    # html_doc = requests.get(url).text
    # soup = BeautifulSoup(html_doc, 'html.parser')
    sidebar = soup.select("._3c2pu66u_0")
    dict_divs = {}
    for div in sidebar:
        title = div.text
        title = title.replace('\n', '')
        title = title.replace(' 试读', '')
        title = title.strip()
        url = div.find('a')['href']
        content_id = url.replace('//time.geekbang.org/column/article/', '')
        origin = title
        title = content_id + ' - ' + title
        dict_divs[origin] = title

    # 获取该文件夹下的所以子文件
    files_path = '/Users/htc/Desktop/Go语言核心36讲/'
    temp_files = os.listdir(files_path)
    # 遍历子文件
    for temp_file in temp_files:
        # 拼接该文件绝对路径
        full_path = os.path.join(files_path, temp_file)
        full_path = full_path.replace('\\', '/')
        # 匹配.md文件
        if os.path.isfile(full_path) and os.path.splitext(full_path)[1] == ".txt":
            title = os.path.basename(full_path)
            title = title.replace('.txt', '')
            for key in dict_divs.keys():
                if title == key:
                    new_title = dict_divs[key]
                    dst = full_path.replace(key, new_title)
                    os.rename(full_path, dst)


# main
if __name__ == '__main__':
    downloadDomTree()