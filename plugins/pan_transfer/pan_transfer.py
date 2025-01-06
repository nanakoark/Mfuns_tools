from src.createTab import CreateTab
from src.login import login

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
        tab.ele('.m-img m-avatar').click()
        ls = tab.eles('.myz-text myz-text--medium myz-text--sm')
        uid = ls[0].text[4:]
        print(f'你的UID为{uid}，看看有没有登录错了喵~')
        return uid
    except:
        print('获取UID失败，可能是网络问题，请尝试重新运行程序 ＞︿＜')

uid = getUID(tab)
print(tab.cookies())