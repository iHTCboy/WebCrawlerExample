#!/usr/bin/env python
#coding=utf-8
'''
163_NeteaseMusic.py
WebCrawlerExample

Created by HTC at 2018/9/9
Copyright © 2018 iHTCboy. All rights reserved.
'''

import os
import re
import json
import requests
from lxml import etree


def download_songs(url=None):
    if url is None:
        url = 'https://music.163.com/#/playlist?id=2384642500'

    url = url.replace('/#', '').replace('https', 'http')  # 对字符串进行去空格和转协议处理
    # 网易云音乐外链url接口：http://music.163.com/song/media/outer/url?id=xxxx
    out_link = 'http://music.163.com/song/media/outer/url?id='
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'https://music.163.com/',
        'Host': 'music.163.com'
    }
    # 请求页面的源码
    res = requests.get(url=url, headers=headers).text

    tree = etree.HTML(res)
    # 音乐列表
    song_list = tree.xpath('//ul[@class="f-hide"]/li/a')
    # 如果是歌手页面
    artist_name_tree = tree.xpath('//h2[@id="artist-name"]/text()')
    artist_name = str(artist_name_tree[0]) if artist_name_tree else None

    # 如果是歌单页面：
    #song_list_tree = tree.xpath('//*[@id="m-playlist"]/div[1]/div/div/div[2]/div[2]/div/div[1]/table/tbody')
    song_list_name_tree = tree.xpath('//h2[contains(@class,"f-ff2")]/text()')
    song_list_name = str(song_list_name_tree[0]) if song_list_name_tree else None

    # 设置音乐下载的文件夹为歌手名字或歌单名
    folder = './' + artist_name if artist_name else './' + song_list_name

    if not os.path.exists(folder):
        os.mkdir(folder)

    for i, s in enumerate(song_list):
        href = str(s.xpath('./@href')[0])
        song_id = href.split('=')[-1]
        src = out_link + song_id  # 拼接获取音乐真实的src资源值
        title = str(s.xpath('./text()')[0])  # 音乐的名字
        filename = title + '.mp3'
        filepath = folder + '/' + filename
        print('开始下载第{}首音乐：{}\n'.format(i + 1, filename))

        try:  # 下载音乐
            #下载歌词
            #download_lyric(title, song_id)

            data = requests.get(src).content  # 音乐的二进制数据

            with open(filepath, 'wb') as f:
                f.write(data)
        except Exception as e:
            print(e)

    print('{}首全部歌曲已经下载完毕！'.format(len(song_list)))


def download_lyric(song_name, song_id):
    url = 'http://music.163.com/api/song/lyric?id={}&lv=-1&kv=-1&tv=-1'.format(song_id)
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'https://music.163.com/',
        'Host': 'music.163.com'
        # 'Origin': 'https://music.163.com'
    }
    # 请求页面的源码
    res = requests.get(url=url, headers=headers).text
    json_obj = json.loads(res)
    lyric = json_obj['lrc']['lyric']
    reg = re.compile(r'\[.*\]')
    lrc_text = re.sub(reg, '', lyric).strip()

    print(song_name, lrc_text)




if __name__ == '__main__':
    #music_list = 'https://music.163.com/#/playlist?id=2384642500' #歌曲清单
    music_list = 'https://music.163.com/#/artist?id=8325' #歌手排行榜
    # music_list = 'https://music.163.com/#/search/m/?order=hot&cat=全部&limit=435&offset=435&s=梁静茹' #搜索列表
    download_songs(music_list)
