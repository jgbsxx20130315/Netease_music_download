#!/usr/bin/python3
# -*- coding: utf-8 -*
'''
    @author: chen
    @date: 2020/2/22
    @description: 这是一个以wxpython作GUI，
    @requirements: wxPython==4.0.7.post2
                   requests==2.22.0
                   lxml==4.5.0
                   beautifulsoup4==4.8.2
'''
# 导入第三方库
import requests
import threading
import os
import re
import wx
import wx.xrc
from bs4 import BeautifulSoup
import time
import sys

# 导入自定义设置
import settings

# 定义主窗口
class MusicDownloadFrame(threading.Thread, wx.Frame):
    musicData = []
    def __init__(self, threadID, name, counter):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title=settings.title, pos=wx.DefaultPosition,
                          size=settings.size, style=settings.style)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, settings.url_tip,
                                           wx.DefaultPosition, wx.DefaultSize, 0)

        self.m_staticText3.Wrap(-1)

        self.m_staticText3.SetFont(wx.Font(13, wx.FONTFAMILY_DECORATIVE,
                                           wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL,
                                           False, wx.EmptyString))

        bSizer5.Add(self.m_staticText3, 0, wx.ALL, 5)

        self.url_text = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                    wx.DefaultPosition, wx.Size(300, -1), 0)

        bSizer5.Add(self.url_text, 0, wx.ALL, 5)

        self.down_button = wx.Button(self, wx.ID_ANY, settings.down_tip,
                                     wx.DefaultPosition, wx.DefaultSize, 0)

        bSizer5.Add(self.down_button, 0, wx.ALL, 5)

        bSizer4.Add(bSizer5, 1, wx.EXPAND, 4)

        self.output_text = wx.TextCtrl(self, wx.ID_ANY, settings.status_init,
                                       wx.DefaultPosition, wx.Size(600, 320), wx.TE_MULTILINE)

        bSizer4.Add(self.output_text, 0, wx.ALL, 5)

        self.SetSizer(bSizer4)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.down_button.Bind(wx.EVT_BUTTON, self.main_button_click)

        # 多线程
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

        if not os.path.exists(settings.down_path):
            os.mkdir(settings.down_path)

    def __del__(self):
        pass

    def run(self):
        self.output_text.AppendText(u"歌单/排行榜中的歌曲已经获取成功，即将开始下载...\n")
        self.get(self.musicData)

    def main_button_click(self, event):
        self.musicData = []
        if self.getMusicData(self.url_text.GetValue().replace("#/","")) == None:
            time.sleep(5)
            sys.exit(requests.exceptions.ConnectionError)
        else:
            self.musicData = self.getMusicData(self.url_text.GetValue().replace("#/",""))

        print(self.musicData)
        if len(self.musicData) > 1:
            self.start()
        else:
            self.output_text.AppendText('这个歌单好像不存在呢，是不是网络有问题，或者链接写错了，没有下载到音乐。/(ㄒoㄒ)/~~')
            time.sleep(5)
            sys.exit("音乐下载失败")

    def get(self, values):
        print(len(values))     # Todo 这里打印歌单/排行榜条目时有点乱
        downNum = 0
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # 作为文件名时不可以使用的字符
        for x in values:       # Todo 这有个神仙变量
            x['name'] = re.sub(rstr, "_", x['name'])        # 将作为文件名时不可以使用的字符替换成下划线
            if not os.path.exists(settings.down_path + x['name'] + '.mp3'):
                self.output_text.AppendText('***** ' + x['name'] + '.mp3 ***** 下载中...\n')

                url = 'http://music.163.com/song/media/outer/url?id=' + x['id'] + '.mp3'
                try:
                    self.saveFile(url, settings.down_path + x['name'] + '.mp3')
                    downNum = downNum + 1
                except:
                    x = x - 1
                    self.output_text.AppendText(u'下载失败~\n')
        if downNum != 0:
            self.output_text.AppendText('下载完成' + str(downNum) + '个音乐，快去沉浸到音乐当中去吧！')
            time.sleep(5)
            sys.exit("音乐下载完成")
        elif downNum == 0:
            self.output_text.AppendText('这个歌单好像不存在呢，是不是网络有问题，或者链接写错了，没有下载到音乐。/(ㄒoㄒ)/~~')
            sys.exit("音乐下载失败")
        pass

    def getMusicData(self, url):

        headers = {'User-Agent': settings.user_agent}

        try:
            webData = requests.get(url, headers=headers).text
        except:
            self.output_text.AppendText('服务器好像跑到火星去了呢，连接中断,程序即将退出，/(ㄒoㄒ)/~~')
            return None
        soup = BeautifulSoup(webData, 'lxml')
        find_list = soup.find('ul', class_="f-hide").find_all('a')

        tempArr = []
        for a in find_list:
            music_id = a['href'].replace('/song?id=', '')
            music_name = a.text
            tempArr.append({'id': music_id, 'name': music_name})
        return tempArr

    def saveFile(self, url, path):
        headers = settings.down_headers
        response = requests.get(url, headers=headers)
        with open(path, 'wb') as f:
            f.write(response.content)
            f.flush()


def main():
    app = wx.App(False)
    frame = MusicDownloadFrame(1, "Thread-1", 1)
    frame.Show(True)
    # start the applications
    app.MainLoop()


if __name__ == '__main__':
    main()