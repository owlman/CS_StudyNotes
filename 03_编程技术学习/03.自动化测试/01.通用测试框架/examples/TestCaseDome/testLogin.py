from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# 将 TestLogin 类修改为普通的自定义类型
class TestLogin():
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.vars = {}

    def __del__(self):
        self.driver.quit()

    # 为 test_testLogin() 方法添加一个 user 参数
    # 用于执行不同的测试输入：
    def test_testLogin(self, user):
        self.driver.get("http://localhost:3001/")
        self.driver.set_window_size(880, 698)
        u_input = self.driver.find_element(By.CSS_SELECTOR, 
                                                        "tr:nth-child(1) input")
        u_input.send_keys(user["username"])
        p_input = self.driver.find_element(By.CSS_SELECTOR,
                                                        "tr:nth-child(2) input")
        p_input.send_keys(user["password"])
        login = self.driver.find_element(By.CSS_SELECTOR,
                                                        "td:nth-child(1) > input")
        login.click()
        self.driver.close()
