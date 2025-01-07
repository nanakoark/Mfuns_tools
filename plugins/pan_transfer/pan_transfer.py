from src.createTab import CreateTab
from src.login import login
from src.cookies import getCookies, getUserinfo
from src.file_store import getPath

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

uid = getUID(tab)
tab.get(f'https://www.mfuns.net/member/{uid}/videoList')



