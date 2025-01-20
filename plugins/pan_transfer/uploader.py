import src.createTab
from DrissionPage import SessionPage
from src.cookies import getCookies,getAccessToken
from src.file_store import getPath

create = src.createTab.CreateTab(None)
tab = create.create()

def get_Contribute_list(header):
    page = SessionPage()
    page.get('https://api.mfuns.net/v1/contribute/list?type=1&page=1&size=10', headers=header, timeout=3)
    di = page.json
    total = di['data']['total']
    page_num = total//10 +1
    for i in range(2,page_num+1):
        page.get(f'https://api.mfuns.net/v1/contribute/list?type=1&page={i}&size=10', headers=header, timeout=3)
        di['data']['list'].extend(page.json['data']['list'])
    return di['data']['list']

tab.get('https://www.mfuns.net')
access_token = getAccessToken(tab)
header = {
    'authorization' : access_token,
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

ls = get_Contribute_list(header)



# tab.change_mode()
# print(tab.get('https://api.mfuns.net/v1/contribute/list?type=1&page=1&size=10'))
#print(type(tab.get('https://api.mfuns.net/v1/contribute/list?type=1&page=10&size=10')))
