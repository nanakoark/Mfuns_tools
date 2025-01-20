import os
from asyncio import as_completed
from datetime import datetime as dt
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import json
import filetype

# 错误回复
def errfeedback(r):
    try:
        jsdata = json.loads(r.content)
        if jsdata['code'] == 40044 or jsdata['code'] == 403:
            return '外链文件不存在','早期使用Mfvideo的外链视频已丢失＞﹏＜，肥肠抱歉 ≧ ﹏ ≦'
    except json.decoder.JSONDecodeError:
        return '外链文件不存在', '早期使用Mfvideo的外链视频已丢失＞﹏＜，肥肠抱歉 ≧ ﹏ ≦'
    except Exception:
        return '出错了'



# 定义函数对文件进行分块
def byte_range(url,chunk=10):
    header = {
        'mftools': 'letmepass!'
    }
    proxie = {
        # 'http': 'http://127.0.0.1:22334',
        # 'https': 'http://127.0.0.1:22334'
    }
    try:
        r = requests.get(url,headers=header,stream=True,timeout=10,allow_redirects=True,proxies=proxie)
        accept_range = r.headers.get('Accept-Ranges',None)
        filesize = r.headers.get('content-length',None)
        result = []
        # 若服务器支持分块下载
        if accept_range and filesize:
            filesize = int(filesize)
            step_length = int(filesize/chunk)
            a = 0
            b = step_length-1
            for i in range(chunk):
                result.append([a,b])
                a,b = b+1,b+step_length
            result[-1][-1] = filesize
            return result,filesize
        elif accept_range == None and filesize:
            print('服务器不支持分块下载')
            result.append([0, filesize])
            return result, filesize
        # 考虑文件丢失的情况
        elif accept_range == None and filesize == None:
            print('外链文件不存在', '早期使用Mfvideo的外链视频已丢失＞﹏＜，肥肠抱歉 ≧ ﹏ ≦')


    except Exception as e:
        r = requests.get(url,headers=header,stream=True,timeout=10,allow_redirects=True)
        print(f'发生错误:\n{e}')
        for i in errfeedback(r):
            print(i,sep='\n')



# 定义函数下载分块文件
def dlpatch(temp_path,url,start,end,pbar):
        header = {
            'mftools':'letmepass!',
            'Range':f'bytes={start}-{end}'
        }
        proxie = {
            # 'http':'http://127.0.0.1:22334',
            # 'https':'http://127.0.0.1:22334'
        }
        try:
            r = requests.get(url,headers=header,stream=True,timeout=10,allow_redirects=True,proxies=proxie)
            with open(temp_path,'rb+') as f:
                rec = 0
                for chunk in r.iter_content(chunk_size=1024*64):
                    if chunk:
                        f.write(chunk)
                    rec += 1
                    if rec%16 == 0:
                        pbar.update(1)

        # 考虑网络问题导致的错误
        except Exception as e:
            print(f'发生错误:\n{e}')
            print('可能是网络问题导致下载超时，重试中~')


# 定义组合分块文件的函数
def assemble(path,filesize_ls,tp_ls):
    dic = {}
    for item in range(len(tp_ls)):
        dic[tp_ls[item]] = filesize_ls[item]

    for tpn,se in dic.items():
        start = se[0]
        with open(tpn,'rb') as tpf:
            content = tpf.read()
            with open(path, 'rb+') as f:
                f.seek(start)
                f.write(content)


# 定义删除分块文件的函数
def deltempfile(tp_ls):
    try:
        for path in tp_ls:
            if os.path.exists(path):
                os.remove(path)
    except Exception as e:
        print(f'清理临时文件时发生错误:\n{e}')


# 定义函数自动为文件补全后缀
def rename(path):
    file_type = filetype.guess(path)
    # 从mime推断扩展名
    ext = file_type.extension

    # 重命名文件
    new_path = f'{path}.{ext}'
    os.rename(path, new_path)
    return new_path


# 定义函数自动创建文件夹
def create_folder(path,temp=True):
    if temp == True:
        if not os.path.exists(path):
            os.makedirs(path)
            return 'Created'
        else:
            return 'Existed'
    elif temp == False:
        parent_folder = os.path.dirname(path)
        if not os.path.exists(parent_folder):
            os.makedirs(parent_folder)
            return 'Created'
        else:
            return 'Existed'


def main(url_in,path,temp_path,chunk=10):
    '''
    这是下载脚本的主程序

    :param url_in: 传入下载地址
    :param path: 传入文件保存路径（含文件名）
    :param temp_path: 传入分块文件临时存放路径（文件夹）
    :param chunk: 分块数量
    :return: None
    '''
    temp_name = dt.now().strftime('%Y%m%d%H%M%S')
    url = url_in
    filesize_ls,filesize = byte_range(url,chunk)

    # 创建目录
    create_folder(path,temp=False)
    create_folder(temp_path)

    # 创建占位文件
    with open(path, 'wb') as f:
        f.close()
    # 新建临时文件
    k = 0
    tp_ls = []
    for i in range(chunk):
        tpname = f'{temp_name}_{k}'
        tep = '{}\\{}'.format(temp_path, tpname)
        tp_ls.append(tep)
        with open(tep, 'wb') as f:
            f.close()
        k += 1

    # print('分块文件创建完成')

    # 开始分块多线程下载
    with tqdm(total=(filesize//1048576),ncols=75,colour='#a78bfa',unit='MB') as pbar:
        pbar.set_description('【Mftools】Downloading')
        with ThreadPoolExecutor() as p:
            process = []
            j = 0
            for start, end in filesize_ls:
                tp = tp_ls[j]
                process.append(p.submit(dlpatch,tp,url,start,end,pbar))
                j += 1
        pbar.update(pbar.total - pbar.n)
        as_completed(process)
        # print('下载完成')

    # 组合分块文件
    assemble(path,filesize_ls, tp_ls)

    # 删除临时文件
    deltempfile(tp_ls)

    # 考虑不当文件名导致的错误
    if 0< os.path.getsize(path) <= 100:
        print('下载失败，可能是文件名问题，请在网盘中重命名文件，并删掉例如“#”此类特殊字符')
        return False

    # 根据文件类型重命名文件
    new_path = rename(path)
    return new_path

#下面是测试用代码块，引用该脚本时请删除或注释该内容 ~(￣▽￣)~*

# url1 = 'https://pan.nyaku.moe/api/v3/file/source/5334/1.mp4' # 不存在的url
url2 = 'https://pan.nyaku.moe/f/kx1HZ/%E5%8B%95%E3%81%84%E3%81%A6%E3%81%AA%E3%81%84%E3%81%AE%E3%81%AB%E6%9A%91%E3%81%84%E3%82%88%20%28quilt%20heron%20remix%29%20_%20%EC%B0%8C%EA%B7%B8%EB%9F%AC%EC%A7%84%20%EC%88%98%EC%8B%9C%EB%85%B8%20%EB%A6%AC%EB%AF%B9%EC%8A%A4.mp4'
url3 = 'http://39.103.142.157:22333/f/kx1HZ/%E5%8B%95%E3%81%84%E3%81%A6%E3%81%AA%E3%81%84%E3%81%AE%E3%81%AB%E6%9A%91%E3%81%84%E3%82%88%20%28quilt%20heron%20remix%29%20_%20%EC%B0%8C%EA%B7%B8%EB%9F%AC%EC%A7%84%20%EC%88%98%EC%8B%9C%EB%85%B8%20%EB%A6%AC%EB%AF%B9%EC%8A%A4.mp4'
main(url3,
     r'C:\Users\31087\Downloads\test',
     r'C:\Users\31087\Downloads\temp'
     )