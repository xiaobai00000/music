import os
import requests
from bs4 import BeautifulSoup
import time
import re


# 这个是网易云缓存文件目录，一般不需要改
directory = '/storage/emulated/0/Android/data/com.netease.cloudmusic/cache/Cache/Lyric/'

# 这个是下载后的目录，可自定义
path = '/storage/emulated/0/0网易云音乐/'




headers = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; SM-N9600 Build/M1AJQ) AppleWebKit/537.36 ('
    'KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/12.0 Mobile Safari/537.36'
    ' COVC/045816'}


def rename(s): # 这个函数是合法化文件名称，作者太懒了，直接复制于 百度旗下的AI语言模型，文心一言
    # 替换非法字符
    s = re.sub(r'[\\/*?:"<>|]', '_', s)
    # 删除前导的点（在某些操作系统中，这可能会导致问题）
    s = re.sub(r'^\.', '', s)
    # 删除尾随的点
    s = re.sub(r'\.$', '', s)
    return s

def info_list(): #返回文件列表
    # 指定目录

    # 获取目录中的文件列表
    files = os.listdir(directory)
    
    # 使用sorted函数和os.path.getmtime函数获取文件的修改时间，然后排序
    sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    
    try:
        sorted_files.remove('Images')
    except:
        pass
    # 打印排序后的文件列表
    return sorted_files


def process(file_name): # 参数文件名file_name，返回[id，文件名song_name，歌词]
    a = open(directory + file_name, 'r').read()
    b = eval(a.replace('true','True').replace('false', 'False'))
    c = b['lrc']
    e = c.split('\n')[0] # '{"t":0,"c":[{"tx":"作词: "},{"tx":"张和平"}]}'
    f = c.split('\n')[1] # '{"t":1000,"c":[{"tx":"作曲: "},{"tx":"舒楠","li":"http://p1.music.126.net/RBIBtW1TbJf34G3F3NLi1g==/109951165857275040.jpg","or":"orpheus://nm/artist/home?id=5033&type=artist"}]}' 里面有封面的地址
    url = 'https://music.163.com/song?id=' + file_name
    respond = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(respond.text, 'html.parser')    
    song_name = soup.title.getText()[:-13]
    song_name = rename(song_name) # 合法化文件名
    
    lrc = c.replace(e, '').replace(f, '') # 歌词
    
    id = file_name
    return [id, song_name, lrc]


def download(id,name):
    url = 'https://music.163.com/song/media/outer/url?id=' + id
    responds = requests.get(url=url, headers=headers)
    name =rename(name) + '.m4a'
    with open(path+name, 'wb') as FP:
        FP.write(responds.content)
    print('\n下载成功，',name, '已保存到', path, '\n')


def process_without_get(file_name):
    a = open(directory + file_name, 'r').read()
    b = eval(a.replace('true','True').replace('false', 'False'))
    c = b['lrc']
    e = c.split('\n')[0] # '{"t":0,"c":[{"tx":"作词: "},{"tx":"张和平"}]}'
    f = c.split('\n')[2] 
    return f

def main():
    id_list = info_list()
    id_list.reverse()
    print('以下是歌曲歌词的一句，不是音乐名称')
    print('\n')
    i = 0
    for id in id_list:
        i = i +1
        if i <= 10:
            print(str(i), process_without_get(id_list[i-1]))

    try:
        choice1 = int(input('请选择音乐：'))
        info = process(id_list[choice1-1])
        print('\n', info[1], '\n')
        choice2 = input('（输入任意内容表示取消，直接回车表示）请确认：')
        if choice2 == '':
            print('正在下载', info[1])
            download(info[0], info[1])
            with open(path + info[1] + '.lrc', 'w') as fp:
                fp.write(info[2])
        else:
            print('您已取消')
    except:
        print('您未选择，请重新选择')
main()
