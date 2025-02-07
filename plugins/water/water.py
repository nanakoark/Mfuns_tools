import time
import sys
sys.path.append('.\\') # 设置sys.path
sys.path.append(r'.\site-packages')
from src.createTab import CreateTab
from src.login import login

# 创建页面
ini_path = None
createtab = CreateTab(ini_path)
createtab.headless(False)
tab = createtab.create()

# 登录
login(tab)

# 定义签到函数
def signin(tab):
    tab.get('https://www.mfuns.net/member/sign')
    if bool(tab.ele('今日已签到', timeout=3.0)) == True:
        print('今日已签到 ♪(^∇^*)')
    elif bool(tab.ele('立即签到', timeout=3.0)) == True:
        print('签到中~')
        tab.ele('.__button-1cvdmx0-llmp n-button n-button--primary-type n-button--large-type').click()
        if bool(tab.ele('今日已签到', timeout=3.0)) == True:
            print('签到成功 ♪(^∇^*)')
    else:
        pass

time.sleep(1)
# 签到
signin(tab)


