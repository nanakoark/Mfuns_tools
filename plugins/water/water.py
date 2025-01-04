import time
from src.createTab import CreateTab
from src.login import login

# 创建页面
ini_path = None
createtab = CreateTab(ini_path)
createtab.headless()
tab = createtab.create()

#获取用户名和密码
username = input('请输入你的mfuns账号：')
password = input("请输入你的密码(密码已隐藏~)：")
    #最后要记得换成getpass

# 登录
login(tab,username,password)

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


