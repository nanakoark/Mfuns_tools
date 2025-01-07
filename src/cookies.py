from urllib.parse import unquote
import json

def getCookies(tab,path):
    '''
    该函数用于下载Cookies并保存到data/userinfo/cookies.json内

    :param tab: 传入浏览器标签页对象
    :param path: 传入文件保存地址
    :return: None
    '''
    cookies_ls = tab.cookies()
    with open(path, 'w', encoding='UTF8') as cookies_json:
        json.dump(cookies_ls, cookies_json, ensure_ascii=False, indent=4)


def getUserinfo(tab,path):
    '''
    该函数用于下载&保存Cookies中的userinfo并返回userinfo的字典

    :param tab: 传入浏览器标签页对象
    :param path: 传入文件保存地址
    :return: userinfo的字典
    '''
    cookies_ls = tab.cookies()
    for i in cookies_ls:
        if i['name'] == 'userInfo':
            value = unquote(i['value'])
            json_value = json.loads(value)
            print(type(json_value))
            with open(path,'w',encoding='UTF8') as userinfo:
                json.dump(json_value,userinfo,ensure_ascii=False,indent=4)
            return json_value





