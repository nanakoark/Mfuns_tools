from src.createTab import CreateTab
from src.login import login
from src.cookies import getCookies, getUserinfo
from src.file_store import getPath
from DrissionPage import SessionPage

# 创建标签页
ini_path = None
createtab = CreateTab(ini_path)
#createtab.headless()
tab = createtab.create()

# 登录
login(tab)

# 获取uid
def getUID(tab):
    try:
        userinfo=getUserinfo(tab,getPath(['data','userinfo','userinfo.json'],2))
        uid = userinfo['user']['id']
        print(f'你的UID为{uid}，看看有没有登录错了喵~')
        return uid
    except:
        print('获取UID失败，可能是网络问题，请尝试重新运行程序 ＞︿＜')

# 该函数用于判断是否以及到底了~
def end():
    if bool(tab.ele('没有更多了',timeout=2.5)) == True:
        return False
    else:
        return True


# 定义外链视频类
class panVideo():
    __slots__ = ['mvid','title','pan_url']
    def __init__(self,mvid,title):
        self.mvid = mvid
        self.title = title
    def getPan_url(self):
        page = SessionPage()   # 在sessionpage中获取视频链接
        page.get(f'https://www.mfuns.net/video/{self.mvid}')
        self.pan_url = page.ele('@property=og:video').attr('content')
    def download(self):
        pass
    def upload(self):
        pass

# 定义函数查找mvid
def find_mvid(url):
    try:
        for i in range(len(url)):

            if url[i:i+5] == 'video':

                return url[i+6:]

        return False
    except TypeError:
        return False

# 定义函数判断是否为网盘外链
def ispan(pan_url):
    if pan_url[8:21] == 'pan.nyaku.moe' or pan_url[8:24] == 'nyapan.mouup.top':
        return True
    else:
        return False

# 定义获取视频列表的函数，需要传入已经完成加载的个人中心-视频页(tab)，返回视频对象组成的列表mfv_list
def mv_list(tab):
    video_list = tab.eles('.m-link notlink')
    mfv_list= []
    for i in video_list:
        title = i.attr('title')
        mvurl = i.link
        if bool(find_mvid(mvurl)) == True:
            mvid = find_mvid(mvurl)
            mfvideo = panVideo(mvid,title)
            mfvideo.getPan_url()
            mfv_list.append(mfvideo)
    print('总共检索到{}个视频'.format(len(mfv_list)))
    return mfv_list


# 定义从视频列表筛选出使用nya盘外链的视频的函数，需要传入用户视频对象列表，返回筛选完成的视频对象列表
def pv_list(mfv_list):
    panv_list = []
    for mfvideo in mfv_list:
        if ispan(mfvideo.pan_url) == True:
            panv_list.append(mfvideo)
    print('其中有{}个使用Nya盘的视频'.format(len(panv_list)))
    return panv_list


# 加载视频下载页
uid = getUID(tab)
tab.get(f'https://www.mfuns.net/member/{uid}/videoList')
while end():
    tab.actions.scroll(delta_y=23333)

# 获取视频列表
mfv_list = mv_list(tab)
# 筛选出使用nya盘的视频
panv_list = pv_list(mfv_list)









