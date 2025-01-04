from DrissionPage import SessionPage

# 创建页面对象
page = SessionPage()

# 爬取三页
for i in range(1,4):
    # 访问某一页
    page.get(f'https://gitee.com/explore/all?order=starred&page={i}')
    # 获取所有标题的<a>元素列表
    links = page.eles('.title project-namespace-path')
    for link in links:
        print(link.text,link.link)
        # .text获取元素的文本，.link获取元素的href或src属性
