from DrissionPage import Chromium

# 创建mixtab对象
tab = Chromium().latest_tab
# 访问网址
tab.get('https://gitee.com/explore')
# 搜索
tab.ele('@name=q').input('drissionpage')
tab.ele('.ui orange button').click()

# 转换为收发数据包模式
tab.change_mode()

tab.get(f'https://gitee.com/explore/all')
# 获取所有标题的<a>元素列表
links = tab.eles('.title project-namespace-path')
for link in links:
    print(link.text,link.link)
    # .text获取元素的文本，.link获取元素的href或src属性
