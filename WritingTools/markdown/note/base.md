# 基本语法

## 标题

```markdown
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题
```

## 强调文本

```markdown
*斜体*
**粗体**
***斜体加粗体***
```

## 无序列表

```markdown
* 项目1
  * 子项目1
  * 子项目2
  * 子项目3
* 项目2
* 项目3
```

## 有序列表

```markdown
1. 项目1
   1. 子项目1
   2. 子项目2
   3. 子项目3
2. 项目2
3. 项目3
```

## 表格

```markdown
| Tables | Are | Cool |
|-------------|:-------------:|-----:|
| col 3 is | right-aligned | $1600 |
| col 2 is | centered | $12 |
| zebra stripes | are neat | $1 |
```

## 图片

```markdown
![me](img/me.png)
```

## 链接

```markdown
[owlman.org](http://owlman.org)
```

## 注释

```markdown
被注释文本A[^note1]
被注释文本B[^note2]
```

## 区块引用

```markdown
> This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
```

## 代码区块

```markdown
    ```C
    #include <stdio.h>
    #include "stack.h"

    int main(void)
    {
        printf("%s\n", "hello world!");
        return 0;
    }
    ```
```

## 分割线

*****

[^note1]: 注释内容A
[^note2]: 注释内容B