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
    ckls = []
    for cookie_dic in cookies_ls:
        for key in cookie_dic:
            cookie_dic[key] = unquote(cookie_dic[key])
        ckls.append(cookie_dic)

    with open(path, 'w', encoding='UTF8') as cookies_json:
        json.dump(ckls, cookies_json, ensure_ascii=False, indent=4)


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
            with open(path,'w',encoding='UTF8') as userinfo:
                json.dump(json_value,userinfo,ensure_ascii=False,indent=4)
            return json_value


def getAccessToken(tab):
    cookie = list(tab.cookies())
    for item in cookie:
        if item['name'] == 'access_token':
            access_token = unquote(item['value'])
    access_token = access_token.strip('\"')
    return access_token


