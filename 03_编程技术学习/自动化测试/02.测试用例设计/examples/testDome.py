import pytest

# 演示单元测试    
def test_UnitTestingDome() :
    # 导入要测试的目标模块
    import testfunc
    # 基于判定/条件覆盖策略的测试用例：
    testCases = [
        {"x" : 2, "y" : 0, "z" : 4},
        {"x" : 2, "y" : 1, "z" : 1},
        {"x" : 1, "y" : 0, "z" : 1},
        {"x" : 1, "y" : 1, "z" : 1}
    ]
    
    # 执行测试用例：
    for index, case in enumerate(testCases) :
        print("\n正在执行第 %s 个测试用例：" % str(index+1))
        testfunc.afunc(case["x"], case["y"], case["z"])

# 演示接口测试    
def test_InterfaceTestingDome() :
    # 导入之前封装的请求操作类
    import json
    from requestsHandler import RequestsHandler
    # 创建请求操作类的对象
    req = RequestsHandler()
    login_url = 'http://localhost:3001/users/session'
    # 基于边界值分析策略的测试用例：
    testCases = [
        {   # 已注册用户正常登录的情况
            "username": "lingjie", 
            "password": "12345678" 
        },
        {   # 已注册用户非正常登录的情况
            "username": "lingjie", 
            "password": "12x45678"
        }, 
        {    # 未注册用户登录的情况
            "username": "batman", 
            "password": "12345678" 
        },
        {   # 没填写用户名的情况
            "username": "", 
            "password": "12345678"
        },
        {   # 没有填写密码的情况
            "username": "lingjie", 
            "password": ""
        } 
    ]    
    # 执行测试用例：
    for index, case in enumerate(testCases) :
        print("\n正在执行第 %s 个测试用例：" % str(index+1))
        # 获取响应数据
        res = req.visit('post', login_url, json=case)
        if(res != "not json") :
            # 查看 HTTP API 返回的数据
            print(res["message"])
        else :
            print("没有返回 JSON 格式的数据！")
    # 关闭请求会话
    req.close_session()

# 演示功能测试    
def test_FunctionalityTestingDome():
    # 导入之前之前修改的自定义类型
    from testLogin import TestLogin
    
    # 基于边界值分析策略的测试用例：
    testCases = [
        {   # 已注册用户正常登录的情况
            "username": "lingjie", 
            "password": "12345678" 
        },
        {   # 已注册用户非正常登录的情况
            "username": "lingjie", 
            "password": "12x45678"
        }, 
        {    # 未注册用户登录的情况
            "username": "batman", 
            "password": "12345678" 
        },
        {   # 没填写用户名的情况
            "username": "", 
            "password": "12345678"
        },
        {   # 没有填写密码的情况
            "username": "lingjie", 
            "password": ""
        } 
    ]

    # 执行测试用例：
    for index, case in enumerate(testCases) :
        print("\n正在执行第 %s 个测试用例：" % str(index+1))
        # 创建一个 TestLogin 类的实例
        tester = TestLogin()
        tester.test_testLogin(case)
        del tester

def test_PerformanceTestingDome():
    # 引入需要的标准模块
    import random, sys
    # 引入自定义模块
    import sorting
    # 为快速排序算法放宽递归限制
    sys.setrecursionlimit(2000)

    # 定义一个用于获取排序用时的内部函数
    def runSort(func, case) :
        import time
        start = time.process_time()
        func(case)
        end = time.process_time()
        return end - start 
    
    bubbleCounter = 0 # 用于累计冒泡排序胜出的次数
    quickCounter = 0 # 用于累计快速排序胜出的次数
    # 在这里，我们设置执行 1000 次测试
    for i in range(1000) :
        # 生成一个拥有 1000 个随机数的数组，以充当测试用例
        testCase = [random.uniform(0, 1) for _ in range(1000)]
        bUsetime = runSort(sorting.bubbleSort, testCase)
        qUsetime = runSort(sorting.quickSort, testCase)
        # 累计两种算法胜出的次数，平局则忽略不计
        if(bUsetime > qUsetime):
            quickCounter = quickCounter+1 # 快速排序胜出
        elif(bUsetime < qUsetime):
            bubbleCounter = bubbleCounter+1 # 冒泡排序胜出
        
    print("'\n冒泡排序胜出 %s 次，快速排序胜出 %s 次" \
            % (bubbleCounter, quickCounter))
