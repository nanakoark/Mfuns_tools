import os

# 此函数用于获取不同级目录下的路径
## 传入以目录名称字符串为元素的列表，以及向前回溯的目录层级数
## 返回路径字符串
def getPath(subpath,dir_num = 1):
    if dir_num == 1:
        current_Path = os.getcwd()
        parent_Dir = os.path.dirname(current_Path)
        targer_Path = os.path.join(parent_Dir,*subpath)
    elif dir_num == 0:
        return os.path.join(*subpath)
    else:
        current_Path = os.getcwd()
        parent_Dir = os.path.dirname(current_Path)
        for i in range(dir_num-1):
            parent_Dir = os.path.dirname(parent_Dir)
        targer_Path = os.path.join(parent_Dir, *subpath)
    return targer_Path







