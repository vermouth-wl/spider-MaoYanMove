import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import random

# 初始化浏览器对象
browser = webdriver.Edge(r'D:\software\edgeDriver\msedgedriver.exe')
# 设置延时
wait = WebDriverWait(browser, 10)

# 使用浏览器打开Url
browser.get('https://www.huya.com/22076283')

# 发送弹幕需要登录, 先获取登录按钮, 使用css选择器, 然后自动点击登录按钮
loginBtn = browser.find_element_by_css_selector('#nav-login')
loginBtn.click()

# 登录方法一，如果方法一登录需要输入验证码, 请注释方法一
# 获取用户账号密码输入框
# 虎牙加载用户名密码框是试用iframe，所以此处需要切换到iframe框架中
# browser.switch_to_frame('UDBSdkLgn_iframe')
# username_input = browser.find_element_by_css_selector('#account-login-form > div:nth-child(1) > input')
# password_input = browser.find_element_by_css_selector('#account-login-form > div:nth-child(2) > input')
# print(username_input)
# print(password_input)
# # 清除用户密码并填充内容
# username_input.clear()
# password_input.clear()
# username_input.send_keys(config.USERNAME)
# password_input.send_keys(config.PASSWORD)
# time.sleep(3)
# # 获取登录按钮并点击
# try:
#     submit = wait.until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, '#login-btn'))
#     )
#     submit.click()
#
# except:
#     pass
# 登录方法二，如果方法一失效，请取消该方法注释，在弹出输入框后采用手工输入
# 延迟20秒的原因是要进行登录, 如果不手工登录, 则需要搞定图像识别的反爬虫, 此处为了简单直接等待20手工登录
time.sleep(30)
# browser.switch_to_default_content()
sum = 780
while True:

    # 获取弹幕输入框, 使用css选择器
    barrage_input = browser.find_element_by_css_selector('#pub_msg_input')

    # 发送弹幕内容
    # content_arr = [
    #     '欢迎新进来的宝宝，喜欢凌之轩的萌新点点订阅哟~',
    #     '送礼物参与点歌，凌芝会的都会给你唱的~',
    #     '一块钱的礼物就可以拥有凌芝的牌子啦，出门也有牌面~',
    #     '主播是二次元古风唱见，唱歌可好听了呢~',
    #     '仙之巅，傲世间，有了凌芝便有天~',
    #     '东篱把酒黄昏后，有凌轩盈袖~',
    #     '红藕香残玉簟秋，卡个牌子，凌踏九州~',
    #     '常记凌轩日暮，沉醉不知归路~',
    #     '试问凌之轩，却道花灯共旧~',
    #     '玉枕纱厨，半夜轩总颂~'
    # ]

    # random_index = random.randint(0, len(content_arr) - 1)
    sum = sum + 1

    # 将弹幕内容填充进文本输入框
    send_content = '轩轩不在的第 ' + str(sum) + ' 分钟，轩轩啥时候回来啊[大哭]'
    # send_content = content_arr[random_index]
    # barrage_input.send_keys(time.strftime('%H:%M:%S', time.localtime(time.time())) + '--' + send_content)
    barrage_input.send_keys(send_content)
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ' ', '发送弹幕: {}'.format(send_content))
    time.sleep(3)

    # 获取发送按钮
    send_btn = browser.find_element_by_css_selector('#msg_send_bt')
    send_btn.click()
    time.sleep(57)
