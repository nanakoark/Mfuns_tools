import time
from tqdm import tqdm
import src.createTab
from DrissionPage import SessionPage
from src.cookies import getCookies,getAccessToken
from src.file_store import getPath
from mf_print import mfprint


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

def upload(f_path):
    create = src.createTab.CreateTab(None)
    tab = create.create()
    tab.ele('.__button-1cvdmx0-almmd n-button n-button--default-type n-button--medium-type n-button--block n-button--dashed').click()
    upload_button = tab.ele('.m-upload-video dragger')
    upload_button.click.to_upload(f_path)
    tab.listen.start(targets='https://api.mfuns.net/v1/contribute/video/upload_complete')
    mfprint('正在上传')
    with tqdm(total=100, ncols=75, colour='#a78bfa') as pbar:
      #  pbar.set_description('【Mftools】Processing')
        now = tab.ele('.__progress-1cvdmx0-d n-progress n-progress--line n-progress--default',timeout=10).attr('aria-valuenow')
        try:
            while bool(now) == True:
                now = tab.ele('.__progress-1cvdmx0-d n-progress n-progress--line n-progress--default', timeout=2).attr(
                    'aria-valuenow')
                pbar.n = int(now)
                pbar.refresh()

        except Exception:
            pbar.n = 100
            pbar.refresh()
        mfprint('请稍等片刻，正在确认是否已经上传完成~')
        tab.listen.wait(3)
    mfprint('上传成功')



# 获取access_token
def getAccess_token():
    tab.get('https://www.mfuns.net')
    access_token = getAccessToken(tab)
    return access_token

# 获得稿件号与视频对象对应的字典
def getUploaddict(mvid_dict):
    header = {
        'authorization' : getAccess_token(),
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    # 获取投稿视频列表
    ls = get_Contribute_list(header)
    # 获取投稿视频id与mv号关联的字典
    re_di = getRe_di(ls)
    conid_dict = dict()
    for mvid in mvid_dict:
        mvid_dict[mvid].conid = re_di[int(mvid)]
        conid_dict[re_di[int(mvid)]] = mvid_dict[mvid]
    return conid_dict

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
def main(video,retain_external_link = True):
    conid = video.conid
    mfprint(f'开始上传 mv{video.mvid} {video.title}')
    tab.get(f'https://www.mfuns.net/create/video?type=edit&contributeId={conid}')
    if video.hasmultiP == True:
        k =0 #统计p数
        for f_path in video.f_path:
            k +=1
            print(f'开始上传P{k}')
            if f_path == 0:
                print(f'P{k}使用直链，不再上传')
            else:
                upload(f_path[1])
            time.sleep(1)
    else:
        upload(video.f_path)

    # 是否保留外链视频
    if retain_external_link == True:
        pass
        update_button = tab.ele('.__button-1cvdmx0-dllmp n-button n-button--primary-type n-button--large-type')
        update_button.click()
    elif retain_external_link == False:
        ps = tab.eles('.m-video__part-item')
        for pt in range(len(ps)):
            p = tab.ele('.m-video__part-item')
            isPan_url = p.child('.info').child('.type').text
            if isPan_url == '外链':
                delateP(p)

# 定义仅删除外链分P函数
def onlydelete(video):
    conid = video.conid
    mfprint(f'删除外链分P mv{video.mvid} {video.title}')
    tab.get(f'https://www.mfuns.net/create/video?type=edit&contributeId={conid}')
    ps = tab.eles('.m-video__part-item')
    for pt in range(len(ps)):
        p = tab.ele('.m-video__part-item')
        isPan_url = p.child('.info').child('.type').text
        if isPan_url == '外链':
            delateP(p)





