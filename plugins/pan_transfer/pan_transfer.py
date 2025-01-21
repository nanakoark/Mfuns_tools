import os
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
import plugins.pan_transfer.uploader as uploader


# 获取全局目录
path = getPath(['data','pan_transfer','download'],2)
temp_path = getPath(['data','pan_transfer','temp'],2)
log_path = getPath(['data','pan_transfer','log.json'],2)
# 读取配置文件
with open('config.json','r') as config_file:
    config = json.load(config_file)
    proxies = config['proxies']



# 定义获取uid的函数
def getUID(tab):
    #try:
    userinfo=getUserinfo(tab,getPath(['data','userinfo','userinfo.json'],2))
    uid = userinfo['user']['id']
    username = userinfo['user']['name']
    mfprint(f'你的UID为{uid}，看看有没有登录错了喵~')
    return uid,username
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
    __slots__ = ['mvid','title','pan_url','hasmultiP','f_path','downloadSuccessed','conid','uploaded']
    def __init__(self,mvid,title):
        self.mvid = mvid
        self.title = title
        self.uploaded = None
        self.downloadSuccessed = None
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
                self.f_path = downloader.main(self.pan_url,file_path,temp_path,proxie=proxies)

            elif self.hasmultiP == True:
                self.f_path = []
                for pid,title in self.pan_url:
                    if self.pan_url[(pid, title)] == None:
                        self.f_path.append(0)
                        continue
                    else:
                        file_path = f'{path}/mv{self.mvid}/{pid}'
                        self.f_path.append((pid,downloader.main(self.pan_url[(pid,title)],file_path,temp_path)))
            mfprint(f'mv{self.mvid}  {self.title} 下载完成~')
            self.downloadSuccessed = True
        except Exception as e:
            print(e)
            mfprint(f'mv{self.mvid}  {self.title}下载失败')
            self.downloadSuccessed = False

    def upload(self,rel):
        uploader.main(self,rel)

    def onlydelete(self):
        uploader.onlydelete(self)



# 定义函数获取多P视频的视频源url列表
def getMultiP(mvid):
    page = SessionPage()
    page.get(f'https://www.mfuns.net/video/{mvid}')
    author = username
    p_dic = {}
    key_ls = []
    # 获取标题列表
    k = 0 # 用于记录p数
    temp_list = page.ele('.m-video__playlist').texts()
    for i in temp_list:
        k +=1
        weishu = len(str(k)) # 根据p数进行索引
        p_num = i[1:weishu+1]
        p_title = i[weishu+1:]
        key_ls.append((p_num,p_title))
        p_dic[(p_num,p_title)] = None
    info_json = json.loads(page.ele('@id=__NUXT_DATA__').text)
    start_index = info_json.index('首页')
    end_index = info_json.index(author)
    key_ls_index = 0
    count = 0
    for ind in range(start_index,end_index+1):
        line = info_json[ind]
        if type(line) == str and line[0:5] == 'https':
            if ispan(line) == True:
                if count != 0:
                    key_ls_index += 1
                    p_dic[key_ls[key_ls_index]] = line
                    key_ls_index += 1
                else:
                    p_dic[key_ls[key_ls_index]] = line
                    key_ls_index += 1
            elif ispan(line) == False:
                p_dic[key_ls[key_ls_index]] = line
                count += 1


    for j in p_dic:
        if ispan(p_dic[j]) == False:
            p_dic[j] = None
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
            if pan_url[k] == None:
                continue
            elif pan_url[k][8:21] == 'pan.nyaku.moe' or pan_url[k][8:24] == 'nyapan.mouup.top':
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

# 定义书写log的函数，记录历史操作记录
def writelog(video,retain_ex_link,log_path):

    # 判断log文件是否存在
    if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
        with open(log_path, 'r', encoding='utf-8') as log:
            data = json.load(log)

    else:
        data = {}

        # 注意：mvid是字符串，conid是整数
    data[video.mvid] ={
            'mvid': video.mvid,
            'conid': video.conid,
            'title': video.title,
            'retain_ex_link': retain_ex_link
        }

    with open(log_path, 'w', encoding='utf-8') as log:
        json.dump(data, log, ensure_ascii=False, indent=4)


# 定义读取log的函数
def readlog(log_path):
    with open(log_path, 'r', encoding='utf-8') as log:
        log_data = json.load(log)
        return log_data



## 主代码块

# 创建标签页
ini_path = None
createtab = CreateTab(ini_path)
#createtab.headless()
tab = createtab.create()

# 登录
times = 0
while times<=3:
    try:
        mfprint('正在登录~')
        login(tab)
        times = 233
    except Exception as e:
        print(e)
        mfprint('重试中~')
        times += 1

mfprint('\033[32m请不要关闭弹出的浏览器窗口!\033[0m')
mfprint('\033[31m脚本不稳定，请随时留意脚本在浏览器中的操作 ╰(￣ω￣ｏ)\033[0m')

# 加载视频下载页
uid,username = getUID(tab)
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
mfprint('注意：如果某个视频之前已经转过直链但是保留了外链，目前这个脚本还无法识别，非常抱歉 >_<')

# 用户输入需要转直链的视频，得到索引的列表p_list
p_range = input('【Mftools】请输入需要转直链的视频: ')
p_range = p_range.split(',')

p_list = []
for item in p_range:
    if item == '0' or item == '':
        p_list=list(range(len(panv_list)))
        mfprint('将尝试将所有外链视频转为直链')
    elif item[0:2] == 'mv':
        index = idandmv[item] - 1
        p_list.append(index)
    else:
        index = int(item) -1
        p_list.append(index)

# 询问是否需要保留外链视频
retain = input('【Mftools】请问是否需要保留外链视频（直链作为P2） [Y/N](默认保留): ')
retain_ex_link = True
if retain == 'Y' or retain == 'y' or retain == '' or retain == None:
    retain_ex_link = True
elif retain == 'N' or retain == 'n':
    retain_ex_link = False


# 遍历p_list，查找是否有之前已经操作过的视频
log_data = readlog(log_path)
refunc_di = {}
for index in p_list:
    video = panv_list[index]
    for mvid in log_data:
        if mvid == video.mvid:
            refunc_di[index] = video

mfprint('注意：以下视频已经转过直链啦，不过当时保留了外链作为分P：')
mfprint('|{:^3}|{:^8}| 标题'.format('序号','mv号'))
for index in refunc_di:
    video = refunc_di[index]
    mfprint('{:^7}{:<10}{}'.format(k, f'mv{video.mvid}', video.title))

if retain_ex_link == False:
    mfprint('请问您希望对它们执行什么操作：')
    mfprint('A 跳过，不再操作')
    mfprint('B 不再保留他们的外链')
    user_input = input('【Mftools】请输入字母A或B: ')
    if user_input == 'A':
        for index in refunc_di:
            p_list.remove(index)
    elif user_input == 'B':
        for index in refunc_di:
            panv_list[index].uploaded = True

elif retain_ex_link == True:
    mfprint('将不再对它们进行操作')
    for index in refunc_di:
        p_list.remove(index)


# 下载并上传视频
dl_list = p_list.copy()
for index in refunc_di:
    dl_list.remove(index)
if len(p_list) != 0:
    # 下载视频
    getVideo(dl_list,panv_list)
    print('-'*50)

    # 获取需要上传的视频的mv号和对应的视频元素的字典
    mvid_dict = {}
    for i in p_list:
        if panv_list[i].downloadSuccessed == True or panv_list[i].uploaded == True:
            mvid_dict[panv_list[i].mvid] = panv_list[i]


    if len(mvid_dict) != 0:
        # 上传视频/删除外链
        conid_dict = uploader.getUploaddict(mvid_dict)
        for i in conid_dict:
            video = conid_dict[i]
            if video.uploaded == True:
                video.onlydelete()
                writelog(video, retain_ex_link, log_path)
            else:
                writelog(video,retain_ex_link,log_path)
                video.upload(retain_ex_link)


mfprint('操作完成，请去检查一下有没有问题吧')






