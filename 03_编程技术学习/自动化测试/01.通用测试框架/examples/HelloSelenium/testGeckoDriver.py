from time import sleep
# 导入框架中的 WebDriver 组件
from selenium import webdriver
# 创建操作 Web 浏览器的驱动器对象

def TestGeckodriver(Url):
    driver = webdriver.Firefox()
    # 使用驱动器对象打开浏览器并访问指定的 URL
    driver.get(Url)
    # 设置浏览器的窗口宽 800，高400
    driver.set_window_size(800, 400)
    # 等待 3 秒再继续
    sleep(3)
    # 使用驱动器对象刷新当前页面
    driver.refresh()
    # 等待 3 秒再继续
    sleep(3)
    # 使用驱动器对象最大化浏览器窗口
    driver.maximize_window()
    # 等待 3 秒再继续
    sleep(3)
    # 使用驱动器对象关闭浏览器窗口
    driver.close()
    # 使用驱动器对象退出浏览器程序
    driver.quit()

# 调用测试方法
if (__name__ == "__main__") :
    TestGeckodriver("https://www.baidu.com")