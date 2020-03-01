"""
    @author: chen
    @date: 2020/2/22
    @description: 此文件是同目录下 main.py 的配置文件，可以通过修改相关变量来进行来自定义程序。更多描述请参见 main.py
"""
# 导入第三方库
import wx

# settings.py 此处定义音乐下载相关参数

# 下载位置 Todo 通过对话框形式设置下载路径
down_path = "e:/music/"
# 窗口标题
title = u"网易云歌单/排行榜下载"

# 窗口大小
size = wx.Size(610,402)

# 窗口样式
style = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL

# 链接提示
url_tip = u"网易云歌单/排行榜链接"

# 下载按钮
down_tip = u"下载歌单"

# 大文本框中初始内容
status_init = u'''
    网易云音乐歌单下载，网页中复制URL,格式如下：
    https://music.163.com/#/playlist?id=xxxxxxxxxx
    或者：
    https://music.163.com/#/discover/toplist?id=xxxxxxx
    下载目标目录：{}
    因为目前技术原因，程序线程还不能反复启动，所以请在下载完成之后重
    启一下程序，再进行下一个歌单/排行榜的下载。
    可以多开下载不同的歌单/排行榜。
    --------------------------------------------------------------------------------
    支持歌单和排名榜 - chen
    --------------------------------------------------------------------------------
'''.format(down_path)

# 爬取网易云时的User-Agent
user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'

# 下载时的headers
down_headers = {'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Upgrade-Insecure-Requests': '1'
}
