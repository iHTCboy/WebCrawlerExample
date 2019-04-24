#!/usr/bin/env python
#coding=utf-8
'''
ObjC.io.py

Created by HTC at 2019-04-24
Copyright © 2019 iHTCboy. All rights reserved.
'''

import os
import json
import requests
from bs4 import BeautifulSoup


def downloadObjC():
    url = 'https://www.objc.io/issues/'
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    sidebar = soup.select(".c-issue-unit")
    dict_divs = {}
    for div in sidebar:
        index = div.attrs['id']
        issue_content_title = div.select('.c-issue-unit__header__name')[0].text
        issue_header_meta = div.select('.c-issue-unit__header__meta')[0].text
        issue_content_list = div.select('.c-issue-unit__toc__item')

        list_array = []
        for item in issue_content_list:
            title = item.select('.c-issue-unit__toc__item__name')[0].text
            url = 'https://www.objc.io' + item.find('a')['href']
            author = item.select('.c-issue-unit__toc__item__author')
            author = author[0].text if author else ''
            list_array.append({'title': title, 'url' : url, 'author': author})

        dict_divs[str(index)] = {
            'index' : str(index),
            'issue_title' : issue_content_title,
            'issue_date_meta' : issue_header_meta,
            'issue_list' : list_array
        }

    return dict_divs



def downloadObjC_cn():
    url = 'https://objccn.io/issues/'
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    sidebar = soup.select(".col-md-4")
    array_divs = []
    index = 1
    for div in sidebar:
        issue_content_title = div.select('.issue_content_title')[0].text
        issue_header_meta = div.select('.issue_header_meta')[0].text
        issue_content_list = div.select('.issue_content_item')

        list_array = []
        for item in issue_content_list:
            title = item.text
            url = 'https://objccn.io' + item.find('a')['href']
            list_array.append({'title': title, 'url' : url, 'author': ''})

        array_divs.append({
            'index' : str(index),
            'issue_title_cn' : issue_content_title,
            'issue_date_meta_cn' : issue_header_meta,
            'issue_list_cn' : list_array
        })

        index += 1


    dict_objc = downloadObjC()
    for issue in array_divs:
        index = issue['index']
        dict = dict_objc[index]
        issue['issue_title'] = dict['issue_title']
        issue['issue_date_meta'] = dict['issue_date_meta']
        issue['issue_list'] = dict['issue_list']

    print(array_divs)
    saveJson(array_divs, 'Objc.io.json')



# 保存内容
def saveJson(content, save_name):
    save_path = os.path.join(os.getcwd(), save_name)
    save_path = save_path.replace('\\', '/')
    # 保存
    with open(save_path, "wb") as f:
        f.write(json.dumps(content).encode("utf-8"))

def downloadNSHipster():
    url = 'https://nshipster.com'
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    sidebar = soup.select(".archive dl")#.select('dl')
    dict_dls = {}
    for dl in sidebar:
        content_title = dl.select('dt')[0].text
        content_list = dl.select('dd')
        list_array = []
        for item in content_list:
            title = item.text.replace('\u200b', '') #无字符？
            title = title.replace('&nbsp;', ' ') #空格
            title = title.replace('\u00a0', ' ') #空格
            title = title.replace('\n', ' ') #回车
            #title = title.replace('&amp;', ' ') # &
            title = title.replace('                  ', '')
            url = 'https://nshipster.com' + item.find('a')['href']
            list_array.append({'title': title, 'url' : url})

        dict_dls[content_title] = {
            'content_title' : content_title,
            'content_list' : list_array
        }

    return dict_dls


def downloadNSHipster_cn():
    url = 'https://nshipster.cn'
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    sidebar = soup.select(".archive dl")  # .select('dl')
    dict_dls = {}
    for dl in sidebar:
        content_title = dl.select('dt')[0].text
        content_list = dl.select('dd')
        list_array = []
        for item in content_list:
            title = item.text.replace('\u200b', '')  # 无字符？
            title = title.replace('&nbsp;', ' ')  # 空格
            title = title.replace('\u00a0', ' ')  # 空格
            title = title.replace('\n', ' ')  # 回车
            # title = title.replace('&amp;', ' ') # &
            title = title.replace('                  ', '')
            url = 'https://nshipster.cn' + item.find('a')['href']
            list_array.append({'title': title, 'url': url})

        dict_dls[content_title] = {
            'content_title_cn': content_title,
            'content_list_cn': list_array
        }

    dict_objc = downloadNSHipster()
    for key, value in dict_dls.items():
        dict = dict_objc[key]
        dict['content_title_cn'] = value['content_title_cn']
        dict['content_list_cn'] = value['content_list_cn']

    print(dict_objc)
    saveJson(dict_objc, 'NSHipster.json')



if __name__ == '__main__':
    #downloadObjC()
    #downloadObjC_cn()
    # downloadNSHipster()
    downloadNSHipster_cn()

'''
https://www.objc.io
https://www.objccn.io

var ulElement = document.getElementsByClassName("c-issue__articles")[0];
var liElemnts = ulElement.getElementsByClassName('c-issue__article');
var abc = [];
for(let liElement of liElemnts) {
 	let aElements = liElement.getElementsByTagName("a");
 	let href = aElements[0].getAttribute("href");
 	let url = 'https://www.objc.io/' + href.slice(0, href.length - 1);
	abc.push(url);
}

var s = abc.join("\n");
'''



'''
http://nshipster.com
http://nshipster.cn

var ulElements = document.getElementsByClassName("archive");
var abc = [];
for(let dlElement of ulElements) {
 	let ddElements = dlElement.getElementsByTagName("dd");
 	for(let ddElement of ddElements) {
 		let aElement = ddElement.getElementsByTagName("a")[0];
 		let text = aElement.innerText;
 		let href = aElement.getAttribute("href");
 		let url = text + ' (' + 'https://nshipster.cn' + href.slice(0, href.length - 1) + ')';
 		abc.push(url);
 	}
}
'''
