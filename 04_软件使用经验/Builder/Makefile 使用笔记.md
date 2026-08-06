---
title: Makefile 使用笔记
author: 凌杰
date: 2018-04-16
updated: 2026-08-06
tags: 自动化构建
categories: 软件使用经验
---

> [!NOTE] 笔记说明
>
> 这篇笔记将用于记录本人在使用 make 这款项目构建工具过程中所记录的心得体会，它将会被存储在本人的[计算机专业笔记库](https://github.com/owlman/CS_Studynotes) 中，并予以长期维护。

## Makefile 简介

在软件开发中，make 通常被视为一种项目构建工具。该工具主要经由读取一种名为`makefile`或`Makefile`的文件来实现软件项目的自动化构建。它会通过一种被称之为“target”概念来检查项目文件之间的依赖关系，这种依赖关系的检查系统非常简单，主要通过对比文件的修改时间来实现。在大多数情况下，我们主要用它来编译源代码，生成结果代码，然后把结果代码连接起来生成可执行文件或者库文件。

## 优点与缺点

与大多数古老的 UNIX 工具一样，make 也分别有着人数众多的拥护者和反对者。它在适应现代大型软件项目方面有着许许多多的问题。但是，依然有很多人坚定地认为（包括我）它能应付绝大多数常见的情况，而且使用非常的简单，功能强大，表达清楚。无论如何，make 如今仍然被用来编译很多完整的操作系统，而且它的那些“更为现代”的替代品们在基本操作上与它没有太大差别。

当然，随着现代的集成开发环境（IDE）的诞生，特别是非 UNIX 的平台上，很多程序员不再手动管理依赖关系检查，甚至不用去管哪些文件是这个项目的一部分，而是把这些任务交给了他们的开发环境去做。类似的，很多现代的项目也发展出了自己专属的、能高效管理依赖关系的构建工具（例如 Java 生态中的 Apache Ant）。

## 主要版本

make 程序经历过各方多次的改写与重写，各方都依据自己的需要做了一些特定的改良。目前市面上主要流行有以下几种版本：

- GNU make：GNU make 对 make 的标准功能进行了重新改写，并加入作者自认为值得加入的新功能，常和 GNU 编译系统一起被使用，是大多数 GNU Linux 默认安装的工具。
- BSD make：该版本是从 Adam de Boor 制作的版本上发展起来的。它在编译目标的时候有并发计算的能力。主要应用于FreeBSD，NetBSD 和 OpenBSD这些系统。
- Microsoft nmake：该版本主要用于微软的 Windows 系统中，多见于 Visual Studio 项目的构建场景。需要特别留意的是，微软的 nmake 与 BSD 系的 `bmake`（也叫 BSD make）是两种完全不同的工具，名字相近但功能定位截然不同；千万不要把这两者混淆。

## 从一个简单的例子开始

我们可以用《K&R》中 4.5 那个例子来做个说明。在这个例子中，我们会看到一份主程序代码(`main.c`)、三份函数代码(`getop.c`、`stack.c`、`getch.c`)以及一个头文件(`calc.h`)。通常情况下，我们会将这个项目的目录结构安排如下：

```bash
example
├── calc
│   ├── calc.h 
│   ├── getch.c
│   ├── getop.c
│   ├── stack.c
│   └── main.c
├── out
│   └── calc
├── test
│   └── run_calc.py
└── makefile
```

在不使用 make 的情况下，如果我们想要对该项目进行编译，就需要先进入到`calc`目录下，然后再执行如下命令：

```bash
gcc main.c getch.c getop.c stack.c -o ../out/calc 
```

并且，之后在开发+调试这个项目的过程中，我们需要不断地重复输入上面这条编译命令，或者通过终端的历史功能不停地按上下键来寻找最近执行过的命令。这样做两个缺陷：

1. 一旦终端历史记录被丢失，就不得不从头开始输入命令。大家都知道，手工输入命令往往是错误的根源，因此，我们会希望有一个更智能的编译命令。

2. 任何时候，只要我们修改了项目中任何一个文件，上述编译命令就会重新编译所有的文件，当文件足够多时这样的编译会非常耗时。

那么 make 又能做什么呢？让我们打开项目根目录下的`makefile`文件，先输入一条最简单的编译规则：

```makefile
out/calc: calc/main.c calc/getch.c calc/getop.c calc/stack.c
    mkdir -p out
    gcc calc/main.c calc/getch.c calc/getop.c calc/stack.c -o out/calc
```

在这里，读者看到的就是一条最基本的 Makefile 语句，它主要分成了三个部分，第一行冒号之前的`out/calc`，我们称之为目标（target），被认为是这条语句所要处理的对象，具体到这里就是我们所要编译的这个程序`calc`和它所在的目录`out`。冒号后面的部分（`calc/main.c calc/getch.c calc/getop.c calc/stack.c`），我们称之为依赖关系表，也就是编译`calc`程序所需要的源码文件，这些文件只要有一个发生了变化，就会触发该语句的第三部分，我们称其为命令部分，相信读者也看得出这就是我们之前输入的那条编译命令。现在我们只需要直接在项目根目录下打开终端并输入`make`命令，就会看到它按照我们的设定去编译程序了。

不过，这里有一点需要特别留意：无论是 make 还是 gcc，都不会自动创建目标文件所在的目录，因此在第一次编译之前，我们必须先手动执行`mkdir -p out`来创建好`out`目录（上面命令部分的第一行已经替你写好了这一步），否则 gcc 会因为找不到输出目录而报错。后面几个版本的 Makefile 同样依赖`out`目录，为简洁起见不再重复写出这一步，使用时请记得先创建它。

> 请注意，在第二行的 gcc 命令之前必须要有一个 tab 缩进。语法规定 Makefile 中的任何命令之前都必须要有一个 tab 缩进，否则就会报错。

当然了，上面这个`makefile`文件中的代码显然有很明显的冗余问题，让我们来试着解决一下这方面的问题，先初步修改一下上面的代码：

```makefile
cc = gcc
prom = out/calc
src = calc/main.c calc/getch.c calc/getop.c calc/stack.c

$(prom): $(src)
    $(cc) $(src) -o $(prom)
```

如读者所见，我们在上述代码中定义了`cc`、`prom`以及`src`这三个变量。它们分别用于告诉 make 我们要使用的编译器、要编译的目标以及源文件。这样一来，今后我们要修改这三者中的任何一项，只需要修改变量的定义即可，而不用再去管后面的代码部分了。

但我们现在依然还是没能解决”只修改一个文件，整个项目就要全部重新编译”的问题。而且 make 是基于文件修改时间（mtime）来判断依赖关系是否发生变化的，如果我们只是修改了`calc.h`而没有将其显式列入目标的依赖关系表，make 就不会察觉到它的变化（所以下面有必要再为头文件专门设置一个变量，并将其加入到依赖关系表中）。下面，我们来想一想如何解决这个问题。考虑到在标准的编译过程中，源文件往往是先被编译成目标文件，然后再由目标文件连接成可执行文件的。我们可以利用这一点来调整一下这些文件之间的依赖关系：

```makefile
cc = gcc
prom = out/calc
deps = calc/calc.h
obj = out/main.o out/getch.o out/getop.o out/stack.o

$(prom): $(obj)
    $(cc) $(obj) -o $(prom)

out/main.o: calc/main.c $(deps)
    $(cc) -c calc/main.c -o out/main.o

out/getch.o: calc/getch.c $(deps)
    $(cc) -c calc/getch.c -o out/getch.o

out/getop.o: calc/getop.c $(deps)
    $(cc) -c calc/getop.c -o out/getop.o

out/stack.o: calc/stack.c $(deps)
    $(cc) -c calc/stack.c -o out/stack.o
```

这样一来，上面的问题显然是解决了，但同时我们又让代码变得非常啰嗦；过多重复的内容既不利于阅读，也不利于后期维护。经过再度观察，我们发现所有`.c`都会被编译成相同名称的`.o`文件。我们可以根据该特点再对其做进一步的简化：

```makefile
cc = gcc
prom = out/calc
deps = calc/calc.h
obj = out/main.o out/getch.o out/getop.o out/stack.o

$(prom): $(obj)
    $(cc) -o $(prom) $(obj)

out/%.o: calc/%.c $(deps)
    $(cc) -c $< -o $@
```

在这里，我们用到了几个特殊的宏。首先是`%.o`和`%.c`，这表示所有的`.o`目标都依赖于与它同名的`.c`文件（当然还有`deps`中列出的头文件）。再来就是命令部分的`$<`和`$@`，`$<`代表的是依赖关系表中的第一项（如果我们想引用的是整个关系表，那么就应该使用`$^`），具体到这里就是`calc/%.c`。而`$@`代表的是当前语句的目标，即`out/%.o`。这样一来，make 就会自动将`calc`目录下所有的`.c`源文件编译成`out`目录下同名的`.o`文件。不用我们一项一项去指定了。整个代码自然简洁了许多。

到目前为止，我们已经有了一个不错的`makefile`文件，至少用来维护这个小型工程是没有什么问题了。当然，如果要进一步增加上面这个项目的可扩展性，我们就会需要用到一些 Makefile 语法中的伪目标和函数规则了。例如，如果我们想增加自动清理编译结果的功能就可以为其定义一个带伪目标的规则；

```makefile
cc = gcc
prom = out/calc
deps = calc/calc.h
obj = out/main.o out/getch.o out/getop.o out/stack.o

$(prom): $(obj)
    $(cc) -o $(prom) $(obj)

out/%.o: calc/%.c $(deps)
    $(cc) -c $< -o $@

.PHONY: clean
clean:
    rm -rf $(obj) $(prom)
```

有了上面最后两行代码，当我们在终端中执行`make clean`命令时，它就会去删除该工程生成的所有编译文件。注意这里把`clean`声明成了伪目标（`.PHONY`）：伪目标不代表真实文件，声明之后即使项目目录下恰好存在一个名为`clean`的文件，`make clean` 也不会被误判为“无需执行”。

另外，如果我们需要往工程中添加一个`.c`或`.h`，可能同时就要再手动为`obj`变量再添加第一个`.o`文件，如果这列表很长，代码会非常难看，为此，我们需要用到 Makefile 语法中的函数功能，这里演示其中的两个：

```makefile
# 这个版本不适用于 Windows 系统
cc = gcc
prom = out/calc
deps = $(shell find calc/ -name "*.h")
src = $(shell find calc/ -name "*.c")
obj = $(src:calc/%.c=out/%.o) 

$(prom): $(obj)
    $(cc) -o $(prom) $(obj)

out/%.o: calc/%.c $(deps)
    $(cc) -c $< -o $@

.PHONY: clean
clean:
    -rm -f $(obj) $(prom)
```

上面示例中，`clean` 这条 recipe 之前的 `-rm -f` 写法有两层意思：一是 `-` 前缀告诉 make 即便命令返回非零也继续往下走；二是把原来的 `-rf` 改成 `-f`，避免 `rm` 把整个 `out` 目录都连带删除掉。

其中，`shell`函数主要用于执行`shell`命令，具体到这里就是找出`calc`目录下所有的`.c`和`.h`文件。而`$(src:calc/%.c=out/%.o)`则是一个字符替换函数，它会将`src`中所有的`calc/*.c`字串替换成`out/*.o`，实际上就等于列出了所有`.c`文件要编译的结果。有了这两个设定，无论我们今后在该工程加入多少`.c`和`.h`文件，`makefile`文件都能自动将其纳入到工程中来。

需要特别留意的是，`find`是类 UNIX 系统上的命令，在 Windows 的 cmd / PowerShell 上默认并不存在，所以上面这段 makefile 直接拷贝到 Windows 上是会报错的。如果希望让该 makefile 跨平台运行，常见的替代方案有以下几种：

- **使用 Git Bash / WSL / MSYS 等终端**：这些终端自带 GNU 工具链，`find`命令可以直接使用，makefile 无需任何修改。
- **使用 make 内建的`wildcard`函数**：它可以达到与`$(shell find ...)`相同的效果，而且本身就是跨平台的：

  ```makefile
  deps = $(wildcard calc/*.h)
  src  = $(wildcard calc/*.c)
  ```

- **PowerShell 替代**：如果环境只能是原生 PowerShell，则需要把`find`替换为`Get-ChildItem -Recurse`等价的命令；不过由于这个改写成本较高，更推荐直接换用上述两种方案之一。

## 小结

本文从 make 的基本概念出发，借助《K&R》中那个名为`calc`的经典小例子，逐步演示了如何由最简单的编译规则演化到支持模式匹配、伪目标和函数的高级写法。尽管如今 cmake、ninja 等更现代的元构建系统已经能够处理大型项目的复杂依赖关系（可参阅同目录下的 [[Ninja 使用笔记]]），但 make 凭借其语法简洁、上手成本低、对系统依赖少等特点，依然是小型项目、嵌入式工程以及日常脚本化构建任务的首选工具。掌握好本文介绍的这些基础语法，便足以应付绝大多数常见的编译场景。

## 常见陷阱

最后再补充几个使用 make 时最容易踩到的坑，供初学者参考：

- **`.PHONY`一定要显式声明**：凡是“目标不是真实文件”的规则（如`clean`、`install`、`all`），都应当显式列入 `.PHONY`。否则一旦项目目录下真的出现了一个同名的文件，make 就会被误判为“目标已是最新，无需执行”，导致相应的命令无法触发。
- **命令前必须用 tab 缩进，不能用空格**：Makefile 语法规定每个 recipe 行之前必须是单个 tab 字符；任何缩进改用空格的情况都会被 make 直接报错。这一条用编辑器（如 VS Code）装上 Makefile 插件后会自动高亮提示。
- **并行编译`-j`的副作用**：使用 `make -jN` 多线程编译时，各条 recipe 是并发执行的。如果多条命令会写同一个临时文件、或者读取同一份“正在写”的文件，就可能出现竞争问题。常见的规避方式包括：把每个中间产物放到独立的 target 文件名下（`$@`已经替我们做了这件事），以及避免在 recipe 里直接`cd`后再`make`子目录。
- **变量赋值用`=`还是`:=`**：本文中使用的`=`是递归展开，变量被引用时才去解析右侧的表达式；而`:=`是立即展开，定义时就一次性求值。对于包含`$(shell ...)`的变量，更推荐用 `:=`，以防止每次引用时都重新执行一次 shell 命令。

## 参考资料

- [中文维基百科](https://zh.wikipedia.org/wiki/Make)。
- [一个简单的 Makefile 教程](http://blog.163.com/weidao_xue/blog/static/2045410462012102222755897/)。
- [GNU Make Manual](http://www.cs.utexas.edu/~cannata/cs345/GNU%20Make%20Manual.pdf)
