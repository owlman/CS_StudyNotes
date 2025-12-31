# Python 3.x 速查手册（活页本）

以下是模拟Python速查手册的文字稿，我初步设计将该手册划分为十二个活页，每页都设置有一个独立的主题，各个活页之间用分隔线（`---`）隔开。

---

## 基础语法速览

* 缩进规则
* 注释方式
* 代码块结构
* **【新增】Python 语言结构概览（脚本 / 模块 / 包）**
* **【新增】Python 保留关键字速览（表格）**

---

## 变量与命名规则

* 命名规范（PEP 8）
* 作用域（LEGB）
* 常见命名错误
* **【新增】变量绑定与动态类型要点**

---

## 内置数据类型速查

* int / float / bool
* str
* None
* **【新增】bool 与 int 的关系提示**

---

## 核心数据结构对照表

* list / tuple / set / dict
* 可变性对比
* 常用方法速查
* **【新增】类型注解中常见容器写法（list[int] / dict[str, int]）**

---

## 条件与循环模板

* if / elif / else
* for / while
* break / continue / pass
* **【新增】for–else 使用提示（冷知识）**

---

## 函数与参数机制

* def 语法
* 默认参数
* *args / **kwargs
* 返回值模式
* **【新增】类型提示（Python 3.5+）**

  * 参数与返回值注解
  * typing 与内置泛型
* **【新增】联合类型（Union）**

  * Union[T1, T2]
  * T1 | T2（3.10+）

---

## 模块、包与导入规则

* import / from … import
* **name** == "**main**"
* 包结构示意
* **【新增】模块导入顺序与常见误区**

---

## 异常处理速查

* try / except / else / finally
* 常见异常类型
* raise 用法
* **【新增】异常链与自定义异常提示**

---

## 文件与上下文管理器

* open 模式对照
* with 语法
* 编码问题提示
* **【新增】文本 / 二进制模式区分**

---

## 常用内置函数与 I/O 速查

* len / range / enumerate
* zip / map / filter
* sorted / any / all
* **【新增】控制台输入与输出**

  * input()
  * print()（sep / end / file）
* **【新增】输出显示与转换**

  * str / repr / format
  * f-string 速览

---

## 推导式与生成器

* 列表 / 字典推导式
* generator 表达式
* yield 语义
* **【新增】推导式 vs 生成器使用场景对比**

---

## 装饰器与常见高级语法

* 装饰器结构图
* functools.wraps
* 常见使用场景
* **【新增】装饰器执行顺序提示**

---


以下为参考资料：

https://www.amazon.com/Python-Programming-Language-QuickStudy-Laminated/dp/1423251652

Python Programming Language: a QuickStudy Laminated Reference Guide

为各个技能水平的开发者打造，汇集常见操作的核心要点，并提供编写代码时最快捷的参考指南。这本实用的 **6 页覆膜速查卡** 是一份简明的桌面参考资料，涵盖 Python 逻辑、语法和操作背后的关键概念。内容由专家精心编写，重点讲解使用 Python 进行程序规划、变量的初始赋值、导入其他库、格式化输出字符串以及创建类等内容。无论是初学者还是经验丰富的程序员，都会发现它是查阅核心概念的理想工具。超高的性价比，让你可以轻松将这份参考指南加入程序员的工具箱。

**6 页覆膜速查指南包含：**

* 历史与关键特性
* 语言结构
* 命名规范
* 变量与数据类型
* 常见数据类型
* 类型提示与静态类型（Python 3.5+）
* 联合类型（Unions）
* 保留关键字
* 模块导入
* 控制台输入与输出
* 输出显示
* 输出转换


以下是模拟Python速查表的模板（结合OCR核心信息+原图视觉逻辑重构），兼顾“快速查阅性”与“知识完整性”：

Python Programming Language

Python 3.x

─────────────────────────────────────

📚 Working with Python（Python 核心特性）

Interpreted & Portable：解释型语言，无需编译；跨 Windows/macOS/Linux 运行。

Object-Oriented & Functional：支持面向对象（类、继承）与函数式编程（lambda/map/filter）。

Dynamic Typing：变量类型运行时确定（无需提前声明，如 x = 5 → x = "text" 合法）。

Batteries-Included：内置丰富标准库（math/os/sys 等）；第三方库通过 pip 扩展。

─────────────────────────────────────

📝 Naming Conventions（命名规范）

变量名：全小写 + 下划线分隔（snake_case），例：user_name = "Alice"。

常量：全大写（社区约定），例：MAX_RETRY = 3。

类名：驼峰式（CamelCase），例：class UserProfile:。

避坑：禁止用 Python 保留关键字（见下文「Reserved Keywords」）作为标识符。

─────────────────────────────────────

🛠 Writing Code Basics（代码编写基础）

变量与赋值：动态类型，直接赋值生效（无需声明类型）。

age = 25 # int price = 9.9 # float name = "Bob" # str is_student = True # bool 

复合赋值运算符：+=/-=/*=//= 简化操作（如 count += 1 等价 count = count + 1）。

类型转换：显式转换避免隐式错误，例：int("123")/str(3.14)/list("abc")。

打印输出：print() 输出到控制台（支持字符串格式化，如 f"{name} is {age} years old"）。

─────────────────────────────────────

🎯 Scope & Indentation（作用域与缩进）

缩进即语法：Python 用缩进划分代码块（替代大括号 {}），建议用 4 个空格（勿混合 Tab/空格）。

def greet(): # 函数定义（缩进块开始） print("Hello!") # 函数内代码（同层级缩进） 

局部 vs 全局作用域：

函数内变量是局部变量（仅函数内可见）。

修改全局变量需用 global 声明：

global_var = 10 def modify_global(): global global_var global_var = 20 # 修改全局变量 

─────────────────────────────────────

🔑 Reserved Keywords（保留关键字）

以下单词为 Python 语法保留，禁止用作变量/函数/类名：

and, as, assert, break, class, continue, def, del, elif, else, except, False, finally, for, from, global, if, import, in, is, lambda, None, nonlocal, not, or, pass, raise, return, True, try, while, with, yield

─────────────────────────────────────

💬 Comments（注释）

单行注释：行首加 #，例：# 计算用户年龄。

多行注释：用三引号包裹（也可作文档字符串），例：

""" 这是多行注释， 用于解释复杂逻辑～ """ 

文档字符串（Docstring）：函数/类开头的字符串（可通过 help() 查看），例：

def add(a, b): """返回两个数的和""" return a + b 

─────────────────────────────────────

📊 Data Types & Variables（数据类型与变量）

类型说明示例int整数（无大小限制）42, -7float浮点数3.14, -0.5str字符串（不可变序列）"Hello", 'Python'bool布尔（True/False）is_valid = Truelist可变有序列表[1, "a", True]tuple不可变有序元组(1, 2, 3)dict键值对映射（可变）{"name": "Alice", "age": 25}set无序不重复集合{1, 2, 3}（重复元素自动去重） 

设计说明（视觉&结构）

分层逻辑：从“语言特性”到“编码细节”，符合学习路径；

排版强化：用分隔线（─）划分板块，标题分级加粗，代码块用等宽字体+语法高亮；

信息密度：核心知识点配示例（如数据类型、作用域），减少记忆负担。

此模板既保留原图“快速查阅、重点突出”的风格，又补充 OCR 中“动态类型”“保留关键字”等关键信息，适合新手/复习时快速定位知识点～ 🐍， 