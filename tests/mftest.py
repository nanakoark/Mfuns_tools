def login(tab,username,password):
    # 跳转到登录页面
    tab.get('https://mfuns.net')

    # 判断是否已经登录
    if bool(tab.ele('.m-img m-avatar',timeout=3.0)) == True:
        print('已经登录了喵~')
    else:

        # 点击“登录”按钮
        tab.ele('.__button-1cvdmx0-lsmp n-button n-button--primary-type n-button--small-type button signin').click()

        # 定位到账号文本框，获取文本框元素
        login = tab.ele('@autocomplete=username')
            # els用于查找元素，它返回一个ChromiumElement对象，用于操作元素
            # '#user_login'是定位符文本，#意思是按id属性查找元素

        login.input(str(username))

        # 同理输入密码
        passin = tab.ele('@autocomplete=current-password')
        passin.input(str(password))

        # 点击登录
        tab.ele('.__button-1cvdmx0-ilmmp n-button n-button--primary-type n-button--medium-type n-button--block').click()
            # 通过其value属性作为查找条件。@表示按属性名查找

    tab.change_mode()