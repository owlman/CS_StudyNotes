# Python 3.x 速查手册（活页本）

以下是模拟Python速查手册的文字稿，我初步设计将该手册划分为十二个活页，每页都设置有一个独立的主题，各个活页之间用分隔线（即`---`）隔开。

---

## 基础语法速览

### 缩进规则

> **Python 使用缩进表示代码块，而非花括号 `{}`**

#### 基本规则

* **推荐缩进：4 个空格**
* 同一代码块 **缩进必须一致**
* 不允许混用 Tab 与空格

#### 示例

```python
if x > 0:
    print("positive")
    if x > 10:
        print("large")
```

#### 常见错误

* ❌ 缩进层级不一致
* ❌ Tab 与空格混用
* ❌ 在不需要代码块的地方缩进

### 注释方式

#### 单行注释

```python
# 这是单行注释
```

#### 行内注释

```python
x = 10  # 初始化变量
```

#### 文档字符串

```python
def add(a, b):
    """返回 a 与 b 的和"""
    return a + b
```

> [!TIP] **请注意：**
>
> 📌 文档字符串（Docstring） 可被 `help()` 和 IDE 识别
> 📌 使用三引号 `""" """`

### 代码块结构

#### 常见代码块起始关键字

* `if / elif / else`
* `for / while`
* `def`
* `class`
* `try / except / finally`
* `with`

#### 统一结构

```python
关键字 条件:
    代码块
```

### Python 语言结构概览

```bash
脚本（script）
│
├─ 模块（module）  →  .py 文件
│
└─ 包（package）   →  用于组织模块的目录（__init__.py 可选）
```

**表1-1** 对照速览

| 结构 | 说明                        |
| ---- | --------------------------- |
| 脚本 | 直接运行的 Python 文件      |
| 模块 | 可被 import 的 .py 文件     |
| 包   | 组织模块的目录结构          |

### 保留字/关键字速览（按功能分类）

> **关键字不能作为变量名、函数名或类名**

#### 逻辑与控制

```python
if  elif  else  for  while  break  continue  pass
```

#### 函数与类

```python
def  return  lambda  class  yield
```

#### 异常与上下文

```python
try  except  finally  raise  with  as
```

#### 逻辑运算

```python
and  or  not  in  is
```

#### 作用域与导入

```python
import  from  global  nonlocal
```

#### 常量与特殊值

```python
True  False  None
```

### 速查提示

* ❗ 缩进错误是 **SyntaxError** 的常见来源
* ❗ 关键字大小写敏感（`True` ≠ `true`）
* ✔ 推荐使用编辑器自动缩进与语法高亮

---

## 变量与命名规则

### 命名规范（PEP 8）

> **命名的目标是“可读性优先”，而不是“省字符”**

#### 基本约定

| 对象类型    | 命名形式         | 示例              |
| ----------- | ---------------- | ----------------- |
| 变量 / 函数 | `snake_case`     | `total_count`     |
| 常量        | `UPPER_CASE`     | `MAX_SIZE`        |
| 类          | `PascalCase`     | `UserAccount`     |
| 模块        | `snake_case`     | `math_utils.py`   |
| 包          | 小写             | `utils`           |

#### 不推荐写法

* ❌ 使用拼音或无意义缩写
* ❌ 单字符变量名（循环计数器除外）
* ❌ 与内置名称冲突（如 `list`, `str`）

### 变量绑定与动态类型

> **Python 中变量是“名字”，不是“盒子”**

#### 变量绑定示意

```text
x  ──▶  对象（object）  ──▶  类型（type）
```

```python
x = 10        # x 绑定到 int 对象
x = "hello"   # x 重新绑定到 str 对象
```

* 变量本身 **不保存类型**
* 类型属于对象，而非变量名

### 作用域规则（LEGB）

> **查找变量名的顺序**

```text
Local  ──▶  Enclosing  ──▶  Global  ──▶  Built-in
```

#### 示例

```python
x = 1

def outer():
    x = 2
    def inner():
        print(x)
    inner()
```

输出：

```text
2
```

### global 与 nonlocal

#### global

```python
count = 0

def inc():
    global count
    count += 1
```

* 修改模块级变量
* 不影响内置作用域

#### nonlocal

```python
def outer():
    x = 0
    def inner():
        nonlocal x
        x += 1
```

* 修改外层函数变量
* 仅用于嵌套函数

### 常见命名错误

* ❌ 覆盖内置名称

  ```python
  list = [1, 2, 3]
  ```

* ❌ 在不同作用域中滥用同名变量
* ❌ 使用未定义变量（NameError）

### 速查提示

* ❗ 变量必须先绑定后使用
* ❗ `global` / `nonlocal` 是**作用域声明**，不是赋值
* ✔ 推荐使用 `isinstance()` 进行类型判断

---

## 内置数据类型速查

### 数值类型

#### `int`（整数）

```python
a = 10
b = -3
c = 0
```

* 任意精度（无溢出）
* 支持二进制 / 八进制 / 十六进制表示

```python
0b1010   # 10
0o12     # 10
0xA      # 10
```

#### `float`（浮点数）

```python
x = 3.14
y = 1e-3
```

* 基于 IEEE 754
* 存在精度误差

```python
0.1 + 0.2 == 0.3   # False
```

#### `complex`（复数）

```python
z = 1 + 2j
```

* `j` 表示虚部
* 常用于科学计算

### 布尔类型（Boolean）

#### `bool`

```python
True
False
```

* 仅有两个值
* 结果来自比较或逻辑运算

```python
x > 0
a == b
```

---

### ❗ bool 与 int 的关系（易错点）

> **`bool` 是 `int` 的子类**

```python
isinstance(True, int)   # True
```

```python
True == 1    # True
False == 0   # True
```

* 可参与算术运算
* 不推荐依赖该行为进行逻辑判断

### 文本类型（Text Type）

#### `str`

```python
s1 = "hello"
s2 = 'world'
s3 = """多行字符串"""
```

* 不可变（immutable）
* 基于 Unicode

```python
len("你好")   # 2
```

### 空值类型（Null Type）

#### `None`

```python
x = None
```

* 表示“无值”或“未设置”
* 唯一实例

```python
x is None    # 推荐
```

❌ 不推荐：

```python
x == None
```

### 类型检查与转换

#### 查看类型

```python
type(x)
isinstance(x, int)
```

---

#### 常见类型转换

```python
int("10")
float("3.14")
str(123)
bool(0)
```

⚠️ 转换失败会抛出 `ValueError`

### 真值判断（Truth Value Testing）

> **以下值在布尔上下文中为 False**

```text
False
None
0
0.0
0j
""  (空字符串)
[]  {}  set()
```

其余对象默认为 True

### 速查提示（Quick Tips）

* ❗ `None` 不是 `0`，也不是 `False`
* ❗ 浮点数比较应使用容差（如 `math.isclose`）
* ✔ 判断“是否为 None”使用 `is`

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
