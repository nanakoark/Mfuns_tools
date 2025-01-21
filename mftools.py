import os
import subprocess
import sys
import time
from src.mf_print import mfprint

# 启动画面
print(
r'''
 _      _____ _____  ____  ____  _     ____
/ \__/|/    //__ __\/  _ \/  _ \/ \   / ___\
| |\/|||  __\  / \  | / \|| / \|| |   |    \
| |  ||| |     | |  | \_/|| \_/|| |_/\\___ |
\_/  \|\_/     \_/  \____/\____/\____/\____/
'''
)

print('Checking~')
time.sleep(1)
print('Version:0.1.0')

# 设置工作目录为当前py文件所在目录
currentdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(currentdir)

# 检查是否正在使用虚拟环境
venv_python = os.path.join(currentdir, ".venv", "Scripts", "python.exe")
if venv_python not in sys.executable:
    print(r"请使用以下命令激活虚拟环境: .venv\Scripts\activate")
    had_activated = False
else:
    print(f"虚拟环境已激活，当前使用: {sys.executable}")
    had_activated = True

time.sleep(1)

# 主代码块
print()
if had_activated:
    continue_ = True
    while continue_:
        mfprint('功能列表如下：')
        print('1.网盘外链转直链')
        print('...(没有更多了)...')
        print()
        time.sleep(0.7)
        userinput = input('【Mftools】请选择功能:')
        if userinput == '1':
            subprocess.run([venv_python, 'plugins/pan_transfer/pan_transfer.py'])

        userinput = input('【Mftools】请问还需要进行其它操作吗？[Y/N]: ')
        continue_ = True if  userinput in ('Y','y') else False

mfprint('再见喵~')

