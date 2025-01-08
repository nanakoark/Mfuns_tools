from DrissionPage.common import Settings
from DrissionPage import Chromium
from DrissionPage import ChromiumOptions
from src.file_store import getPath


class CreateTab():
    def __init__(self,ini_path):
        # 设置语言
        Settings.set_language('zh_cn')

        # 创建配置对象,设置隐藏浏览器界面
        self.co = ChromiumOptions(ini_path=ini_path).set_paths(local_port=9100,user_data_path='{}'.format(getPath(['data','userdata'],2)))

    def headless(self):
        self.co.headless()

    def create(self):
        # 启动或接管浏览器，并创建标签页对象
        tab = Chromium(addr_or_opts=self.co).latest_tab
        return tab

