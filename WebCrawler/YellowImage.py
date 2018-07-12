#!/usr/local/bin/python3
#coding=utf-8

import os
import requests
from lxml import etree


def downloadImages(url):
    data = requests.get(page).text
    dom = etree.HTML(data)

    title_path = '//*[@id="photos"]/h1/text()'
    totalpage_path = '//*[@id="picnum"]/span[2]/text()'
    image_path = '//*[@id="big-pic"]/p/a/img'

    title = dom.xpath(title_path)[0]
    total = dom.xpath(totalpage_path)[0]
    image_url = dom.xpath(image_path)[0]

    img_src = image_url.xpath('./@src')[0]
    img_alt = image_url.xpath('./@alt')[0]

    print(title, total, img_src, img_alt)

    cwd = os.getcwd()
    save_path = os.path.join(cwd, 'images/' + title)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    print(u'保存图片的路径：', save_path)

    img_path = os.path.dirname(img_src)
    img_name = os.path.basename(img_src)
    img_format = img_name.split('.')[1]
    print(img_path, img_name)

    for i in range(1, int(total) + 1):
        new_img_url = '%s/%02d.%s' % (img_path, i, img_format)
        save_img_path = '%s/%02d.%s' % (save_path, i, img_format)
        # 下载图片
        image = requests.get(new_img_url)
        # 命名并保存图片
        with open(save_img_path, 'wb') as f:
            f.write(image.content)




if __name__ == '__main__':

    url = 'https://www.aitaotu.com/'

    # download list
    list = ['guonei/36350.html', 'guonei/36352.html', 'guonei/36351.html', 'guonei/36357.html', 'guonei/36250.html',
            'guonei/36341.html', 'guonei/36334.html', 'guonei/36306.html', 'guonei/35969.html', 'guonei/35219.html',
            'guonei/36290.html', 'guonei/36277.html', 'guonei/36263.html', 'gangtai/36303.html', 'gangtai/36226.html',
            'guonei/35260.html', 'guonei/35247.html', 'guonei/36257.html', 'guonei/36221.html', 'guonei/21647.html',
            'guonei/21499.html', 'guonei/36319.html', 'guonei/34903.html', 'guonei/14148.html', 'guonei/33780.html',
            'guonei/14338.html', 'guonei/14550.html', 'guonei/14818.html', 'guonei/16820.html', 'guonei/18388.html',
            'guonei/13447.html', 'guonei/25912.html', 'guonei/13991.html', 'guonei/8246.html', 'guonei/36171.html'
            ]

    print(u'准备下载：%d套图', len(list))

    for type in list:
        page = url + type
        downloadImages(page)


    print(u'下载完成啦！')
