#! https://zhuanlan.zhihu.com/p/565994247
# Python 学习笔记之路线图

在这个系列笔记中，我将陆续整理自己在学习 Python 编程语言及其框架的过程中留下的笔记和代码，目的是掌握如何在生产环境中利用各种领域的第三方框架来快速开发应用程序。和大多数学习过程一样，我需要在第一部分笔记中花费一点篇幅来鸟瞰一下 Python 语言所涉及的领域，以便从全局视野来规划接下来的学习路线图，为此，我会在`https://github.com/owlman/study_note`项目的`Programming/LanguageStudy/Python`目录下创建一个名为的`RouteMap`目录，用于存放并维护接下来的这一部分笔记。

## 程序库与框架概览

诚如大家所知，Python 是当前在程序设计领域中最为热门的、解释型的高级编程语言之一。它支持函数式、指令式、结构化和面向对象编程等多种编程范型，且拥有强大的动态类型系统和垃圾回收功能，能够自动管理内存使用，并且其本身拥有一个巨大而广泛的标准库。这些特性可以帮助使用这门编程语言的程序员在参与各种规模的项目时编写出思路清晰的、合乎逻辑的代码。在使用 Python 编写代码时，开发者们通常会遵循“优雅、明确、简单”的核心准则，具体来说就是：

    优美优于丑陋。明了优于隐晦。
    简单优于复杂。复杂优于凌乱。
    扁平优于嵌套。稀疏优于稠密。
    可读性很重要。

上述准则确保了开发者们在使用 Python 语言时一般会拒绝花俏的语法，而选择明确且尽可能没有歧义的语法。当然了，对于这些准则的坚守也导致了 Python 社区对于牺牲了优雅特性的优化策略持有了较为谨慎的态度，一些对非重要部分进行性能优化的补丁通常很难被获准合并到 Python 的官方实现 CPython 项目中，这也限制 Python 在某些对执行速度有较高要求领域的使用。到目前为止，人们主要将 Python 应用于以下领域，并开发了相应的程序库与框架：

- **科学计算**：在这一领域，我们可以选择使用 Numpy、Scipy、pandas、matplotlib 等框架进行各种科学数值计算，并生成相关的数据报告或图表；
- **网络爬虫**：在这一领域，我们可以选择使用 Scrapy 这个轻量级的框架来从指定的网站中收集有用的数据；
- **Web 开发**：在这一领域，我们可以选择使用 Django、Web2py、Bottle、Tornado、Flask 等框架来开发个人博客、线上论坛等 Web 应用程序以及基于 HTTP 协议的应用程序服务端；
- **游戏开发**：在这一领域，我们可以选择使用 PyGame、PyOgre、Obespoir 等框架来开发俄罗斯方块、贪吃蛇这样的二维或三维的游戏。
- **图形化界面开发**：在这一领域，我们可以选择使用 PyQT、WxPython 等框架来实现带有图形界面的应用程序。
- **网络编程**：在这一领域，我们可以选择使用 Twisted 框架来开发基于多种网络协议的应用程序，该框架支持的协议既包括 UDP、TCP、TLS 等传输层协议，也包括 HTTP、FTP 等应用层协议；
- **人工智能**：在这一领域，我们可以选择使用Dpark、NLTK、tensorflow等框架来数据挖掘、自然语言处理、机器学习等方向上的工作；
- **自动化运维**：在这一领域，我们可以选择使用 Buildbot 框架来实现自动化软件构建、测试和发布等过程。每当代码有改变，服务器要求不同平台上的客户端立即进行代码构建和测试，收集并报告不同平台的构建和测试结果；
- **自动化测试**：在这一领域，我们可以选择使用 Selenium、Robot framework 等框架来实现自动化的图形界面测试、接口测试、兼容性测试等；

基本上，除了基本语法之外，一个 Python 开发者的能力实际上就取决于如何根据自己面对的问题找到适用的框架，并在合理的时间内掌握该框架的使用方法，并用它快速地构建自己的项目。在后续笔记中，我们将会利用具体的项目实践来介绍如何构建这种“在做中学，在学中做”的能力。

## 规划路线图

在了解以上基本概念之后，接下来就可以来具体规划一下要学习如何使用Python语言进行框架开发的学习路线图了。大致上，我们可以将路线图划分为以下三个里程碑。

### 掌握 Python 语言的基础

要想学习接下来要介绍的内容，掌握 Python 语言的基本语法及其标准库的使用方法无疑是先决条件。虽然在这个系列笔记中，我们会设定自己已经掌握了这门语言的基本使用，但对于“掌握”程度，我们还是希望先和读者约定以下标准。首先，自然是要能正确地安装 Python 语言运行环境，掌握这一能力的标准是读者能在自己的计算机环境中顺利地执行以下 Hello World 程序：

```python
#! /usr/bin/env python

def main():
    print("hello world!")

if __name__ == '__main__':
    main()
```

接下来，读者需要掌握的是 Python 语言的标准语法，包括灵活运用各种表达式语句、条件语句、循环语句，以及会使用标准库提供的各种数据类型和数据结构，掌握这一能力的标准是能理解下面代码中实现的各种排序算法，并能正确地调用它们：

```python
#! /usr/bin/env python

import random

def selectionSort(coll):
    if(coll == []): return []
    for i in range(len(coll)-1,0,-1):
        max_j = i
        for j in range(i):
            if coll[j] > coll[max_j]: max_j = j
        coll[i], coll[max_j] = coll[max_j], coll[i]

    return coll

def countingSort(coll):
    if(coll == []): return []
    endl = len(coll)
    minv = min(coll)
    maxv = max(coll)
    temp = [0 for i in range(maxv - minv + 1)]

    for i in range(endl):
        temp[coll[i] - minv] += 1
    index = 0
    for i in range(minv, maxv + 1):
        for j in range(temp[i - minv]):
            coll[index] = i
            index += 1
    return coll

def radixSort(coll, length):
    if(coll == []): return []
    
    for d in xrange(length):
        LSD = [[] for _ in xrange(10)]
        for n in coll:
            LSD[n / (10 ** d) % 10].append(n)
        coll = [tmp_a for tmp_b in LSD for tmp_a in tmp_b]
    
    return coll

def bucketSort(coll):
    if(coll == []): return []
    
    length = len(coll)
    buckets = [[] for _ in xrange(length)] 
    for tmp_a in coll:
        buckets[int(length * tmp_a)].append(tmp_a)
    tmp_coll = []
    for tmp_b in buckets:
        tmp_coll.extend(insertSort(tmp_b))

    return tmp_coll

def insertSort(coll):
    if(coll == []): return []
    for i in range(1,len(coll)):
        j = i
        while j > 0 and coll[j-1] > coll[j]:
             coll[j-1], coll[j] = coll[j], coll[j-1]  
             j -= 1
              
    return coll 

def shellSort(coll):
    if(coll == []): return []
    size = len(coll)
    step = size / 2
    while(step >= 1):
        for i in range(step, size):
            tmp = coll[i]
            ins = i
            while(ins >= step and tmp < coll[ins - step]):
                coll[ins] = coll[ins - step]
                ins -= step
            coll[ins] = tmp
        step = step / 2
    
    return coll

def bubbleSort(coll):
    if(coll == []): return []
    endl = len(coll)
    for i in range(endl, 0, -1):
        for j in range(0, i - 1):
            if(coll[j] > coll[j + 1]):
                coll[j], coll[j + 1] = coll[j + 1], coll[j]

def quickSort(coll):
    if(coll == []): return []
    return quickSort([x for x in coll[1:] if x < coll[0]]) + \
                         coll[0:1] + \
                         quickSort([x for x in coll[1:] if x >= coll[0]])
```

最后，在最理想的情况下，读者还应该具备一些针对某一特定任务来编写自动化脚本的能力，例如能理解并复述下面这段实现 Git 提交操作的自动化脚本。

```python
#! /usr/bin/env python

import os
import sys
import time

if not len(sys.argv) in range(2, 4):
    print("Usage: git_commit.py <git_dir> [commit_message]") 
    exit(1)

title = "=    Starting " + sys.argv[0] + "......    ="
n = len(title)
print(n*'=')
print(title)
print(n*'=')

os.chdir(sys.argv[1])
print("work_dir: " + sys.argv[1])
if len(sys.argv) == 3 and sys.argv[2] != "":
    commit_message = sys.argv[2]
else:
    commit_message = "committed at " + time.strftime("%Y-%m-%d",time.localtime(time.time()))

os.system("git add .")
os.system("git commit -m '"+ commit_message + "'")

print("Commit is complete!")

print(n*'=')    
print("=     Done!" + (n-len("=     Done!")-1)*' ' + "=")
print(n*'=')
```

如果读者在基于以上标准的自我检验中遇到了一些不可回避的问题，我们会强烈建议先回过头去补习一下 Python 语言的基础知识，例如去阅读一下《Python 基础教程》或者其他介绍了上述基础的书籍，等达到了我们在这里约定的对基础知识的“掌握”标准，再继续学习后面的内容，以便实现最好的学习效果。

### 掌握快速上手框架的能力

这一里程碑主要聚焦的是*可持续之学习能力*。众所周知，在如今的软件开发活动中，我们可以选择的开发框架不仅琳琅满目，选择众多，而且新陈代谢极为快速。这意味着，即使某一本书介绍了当前最为流行的框架及其具体使用方法，很有可能等到它最终出版之时，开发者们已经有了更好的选择。所以授之以鱼不如授之以渔，真正的目的是要掌握“快速学习新框架”的能力，这需要我们掌握如何阅读这些框架本身提供的官方文档，以便自行去了解这些框架的设计思路，并理解为什么决定开放那些接口给用户，为什么对用户隐藏那些实现。这就需要读者自己具备开发框架的能力。换句话说，虽然不必重复发明轮子，但一个优秀的工程师或设计师应该了解轮子是如何被发明的，这样才能清楚在怎么样的轮子上构建怎么样的车。

总而言之，对于如今的项软件工程师来说，在一个月内快速掌握某个新框架的能力远比之前已经掌握了多少个框架重要得多，例如当开发团队的管理员在面试新成员时，如果这位面试者有五年 A 框架的使用经验，那固然是很好，但团队中很多人都有，未必需要再多一个同类型的人才、但如果该面试者能在一个礼拜快速上手基于 Python 的任意一种框架，那么这位人才的重要性就会被凸显出来。毕竟如果我是一个开发团队的管理者，肯定不会喜欢团队的成员告诉我这个不会，那个不会。
