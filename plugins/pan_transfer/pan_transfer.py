import time
from src.createTab import CreateTab
from src.login import login
from src.cookies import getUserinfo
from src.file_store import getPath
from DrissionPage import SessionPage
from tqdm import tqdm
from src.mf_print import mfprint
import json
import plugins.pan_transfer.downloader as downloader


# 获取全局目录
path = getPath(['data','pan_transfer','download'],2)
temp_path = getPath(['data','pan_transfer','temp'],2)

# 创建标签页
ini_path = None
createtab = CreateTab(ini_path)
#createtab.headless()
tab = createtab.create()

# 登录
login(tab)

# 获取uid
def getUID(tab):
    #try:
    userinfo=getUserinfo(tab,getPath(['data','userinfo','userinfo.json'],2))
    uid = userinfo['user']['id']
    print(f'你的UID为{uid}，看看有没有登录错了喵~')
    return uid
 #   except:
  #      print('获取UID失败，可能是网络问题，请尝试重新运行程序 ＞︿＜')

# 该函数用于判断是否以及到底了~
def end():
    if bool(tab.ele('没有更多了',timeout=2.5)) == True:
        return False
    else:
        return True


# 定义外链视频类
class panVideo():
    __slots__ = ['mvid','title','pan_url','hasmultiP','f_path']
    def __init__(self,mvid,title):
        self.mvid = mvid
        self.title = title
    def getPan_url(self):
        page = SessionPage()   # 在sessionpage中获取视频链接
        page.get(f'https://www.mfuns.net/video/{self.mvid}')
        temp_url = page.ele('@property=og:video').attr('content')
        if bool(page.ele('播放列表')) == True:    # 分开处理单P视频和多P视频
            self.hasmultiP = True
            self.pan_url=getMultiP(self.mvid)
        else:
            self.pan_url = temp_url
            self.hasmultiP = False
    def download(self):
        try:
            mfprint(f'开始下载: mv{self.mvid}  {self.title}')
            if self.hasmultiP == False:
                file_path = f'{path}/mv{self.mvid}'
                self.f_path = downloader.main(self.pan_url,file_path,temp_path)

            elif self.hasmultiP == True:
                for pid in self.pan_url:
                    file_path = f'{path}/mv{self.mvid}/{pid}'
                    self.f_path = downloader.main(self.pan_url,file_path,temp_path)
            mfprint(f'mv{self.mvid}  {self.title} 下载完成~')
        except:
            mfprint(f'mv{self.mvid}  {self.title}下载失败')

    def upload(self):
        pass


# 定义函数获取多P视频的视频源url列表
def getMultiP(mvid):
    page = SessionPage()
    page.get(f'https://www.mfuns.net/video/{mvid}')
    p_dic = {}
    # 获取标题列表
    k = 0 # 用于记录p数
    temp_list = page.ele('.m-video__playlist').texts()
    for i in temp_list:
        k +=1
        weishu = len(str(k)) # 根据p数进行索引
        p_num = i[1:weishu+1]
        p_title = i[weishu+1:]
        p_dic[(p_num,p_title)] = None
    info_json = json.loads(page.ele('@id=__NUXT_DATA__').text)
    for j in p_dic:
        place = 0  # 查找标题附近10行内是否有url
        title_index = info_json.index(j[1])
        while place <= 10:
            item = info_json[title_index-5+place]
            place += 1
            if type(item) == str and ispan(item) == True:
                p_dic[j] = item
    return p_dic


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
    if type(pan_url) == str:
        if pan_url[8:21] == 'pan.nyaku.moe' or pan_url[8:24] == 'nyapan.mouup.top':
            return True
        else:
            return False
    elif type(pan_url) == dict:
        for k in pan_url:
            if pan_url[k][8:21] == 'pan.nyaku.moe' or pan_url[k][8:24] == 'nyapan.mouup.top':
                return True
        return False
    else:
        return False

# 定义获取视频列表的函数，需要传入已经完成加载的个人中心-视频页(tab)，返回视频对象组成的列表mfv_list
def mv_list(tab):
    video_list = tab.eles('.m-link notlink')
    mfv_list= []

    # 进度条
    mfprint('开始检索你上传的视频（￣︶￣）↗')
    with tqdm(total=len(video_list),ncols=75,colour='#a78bfa') as pbar:
        pbar.set_description('【Mftools】Processing')
        # 主代码
        for i in video_list:
            title = i.attr('title')
            mvurl = i.link
            if bool(find_mvid(mvurl)) == True:
                mvid = find_mvid(mvurl)
                mfvideo = panVideo(mvid,title)
                mfvideo.getPan_url()
                mfv_list.append(mfvideo)
            time.sleep(0.1)
            pbar.update(1)

    mfprint('总共检索到{}个视频'.format(len(mfv_list)))
    return mfv_list


# 定义从视频列表筛选出使用nya盘外链的视频的函数，需要传入用户视频对象列表，返回筛选完成的视频对象列表
def pv_list(mfv_list):
    panv_list = []
    # 进度条
    mfprint('开始查找使用nya盘外链的视频~')
    with tqdm(total=len(mfv_list),ncols=75,colour='#a78bfa') as pbar:
        pbar.set_description('【Mftools】Processing')

        for mfvideo in mfv_list:
            if type(mfvideo.pan_url) == str and ispan(mfvideo.pan_url) == True:
                panv_list.append(mfvideo)
            elif type(mfvideo.pan_url) == dict and ispan(mfvideo.pan_url) == True:
                panv_list.append(mfvideo)

            time.sleep(0.1)
            pbar.update(1)
    mfprint('其中有{}个使用Nya盘的视频'.format(len(panv_list)))
    return panv_list


# 定义根据p_list下载视频的函数
def getVideo(p_list,panv_list):
    for i in p_list:
        v = panv_list[i]
        v.download()



# 加载视频下载页
uid = getUID(tab)
tab.get(f'https://www.mfuns.net/member/{uid}/videoList')
while end():
    tab.actions.scroll(delta_y=23333)

# 获取视频列表
mfv_list = mv_list(tab)
# 筛选出使用nya盘的视频
panv_list = pv_list(mfv_list)


# 展示筛选出的视频 | 序号 | mv号 | 标题 |
mfprint('应该都在下面了喵~')
mfprint('|{:^3}|{:^8}| 标题'.format('序号','mv号'))
k = 0
idandmv = {} # 使用列表存储序号和mv号的对应关系
for video in panv_list:
    k += 1
    mfprint('{:^7}{:<10}{}'.format(k,f'mv{video.mvid}',video.title))
    idandmv[f'mv{video.mvid}'] = k

# 输出输入提示
print('-'*50)
mfprint('请输入你希望重新上传以转为直链的视频的【序号】或【mv号】')
mfprint('你可以：')
mfprint('（1）直接回车或输入0，所有视频都会被尝试转直链')
mfprint('或者：')
mfprint('（2）输入单个序号或mv号[例如：1 或 mv35124]，只有指定的视频会被转为直链')
mfprint('（3）输入多个序号或mv号，用英文逗号分隔[例如：1,2,3,]')
mfprint('注意：序号和mv号可以混用；逗号必须是英文逗号!')

# 用户输入需要转直链的视频，得到索引的列表p_list
p_range = input('【Mftools】请输入需要转直链的视频: ')
p_range = p_range.split(',')

p_list = []
for item in p_range:
    if item == '0' or item == '':
        p_list.append(range(len(panv_list)))
    elif item[0:2] == 'mv':
        index = idandmv[item] - 1
        p_list.append(index)
    else:
        index = int(item) -1
        p_list.append(index)


# 下载视频
getVideo(p_list,panv_list)








