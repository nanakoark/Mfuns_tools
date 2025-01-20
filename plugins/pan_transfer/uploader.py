from tqdm import tqdm
import src.createTab
from DrissionPage import SessionPage
from src.cookies import getCookies,getAccessToken
from src.file_store import getPath
from src.mf_print import mfprint


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

def getRe_di(Contribute_list):
    re_di = {}
    for i in Contribute_list:
        re_di[i['resource_id']] = i['id']
    return re_di

def upload(conid):
    create = src.createTab.CreateTab(None)
    tab = create.create()
    tab.get(f'https://www.mfuns.net/create/video?type=edit&contributeId={conid}')
    tab.ele('.__button-1cvdmx0-almmd n-button n-button--default-type n-button--medium-type n-button--block n-button--dashed').click()
    upload_button = tab.ele('.m-upload-video dragger')
    upload_button.click.to_upload(r"C:\Users\31087\Downloads\ia6oqjQK_動いてないのに暑いよ (quilt heron remix) _ 찌그러진 수시노 리믹스.mp4")
    tab.listen.start(targets='https://api.mfuns.net/v1/contribute/video/upload_complete')
    mfprint('正在上传')
    with tqdm(total=100, ncols=75, colour='#a78bfa') as pbar:
        now = tab.ele('.__progress-1cvdmx0-d n-progress n-progress--line n-progress--default',timeout=2).attr('aria-valuenow')
        while bool(now) == True:
            pbar.n = int(now)
            pbar.refresh()
        pbar.n(100)
        pbar.refresh()
    tab.listen.wait(3)
    mfprint('上传成功')



# 获取access_token
def getAccess_token():
    tab.get('https://www.mfuns.net')
    access_token = getAccessToken(tab)
    return access_token

# 获得mv号和稿件号对应的字典
def getUploaddict(mvid_list):
    header = {
        'authorization' : getAccess_token(),
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    # 获取投稿视频列表
    ls = get_Contribute_list(header)
    # 获取投稿视频id与mv号关联的字典
    re_di = getRe_di(ls)
    mvid_conid = dict()
    for mvid in mvid_list:
        mvid_conid[mvid] = re_di[mvid]
    return mvid_conid

# 删除外链视频
def delateP(p):
    action = p.child(locator='.actions')
    delate_button = action.child(locator='.__button-1cvdmx0-ehlmmd n-button n-button--default-type n-button--medium-type')
    delate_button.click()
    confirm_button = tab.ele('.__button-1cvdmx0-lsmw n-button n-button--warning-type n-button--small-type')
    confirm_button.click()
    update_button = tab.ele('.__button-1cvdmx0-dllmp n-button n-button--primary-type n-button--large-type')
    update_button.click()


# 主代码
def main(mvid_list,retain_external_link = True):
    mvid_conid = getUploaddict(mvid_list)
    for mvid in mvid_conid:
        conid = mvid_conid[mvid]
        upload(conid)

    # 是否保留外链视频
    if retain_external_link == True:
        return None
    elif retain_external_link == False:
        p_list = tab.eles('.m-video__part-item')
        for p in p_list:
            isPan_url = p.child('.info').child('.type').text
            if isPan_url == '外链':
                delateP(p)








