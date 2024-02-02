#! https://zhuanlan.zhihu.com/p/670453410

# 前端编程接口：DOM与BOM

> 本文部分内容节选自笔者于 2021 年出版的[《JavaScript 全栈开发》](https://book.douban.com/subject/35493728/)一书。

众所周知，网页浏览器是 JavaScript 最初的宿主环境，基于浏览器端的编程（即前端编程）也是这门脚本语言应用得最为成熟的领域。而这一领域编程也是时下最热门的技术议题之一，能否充分发挥 JavaScript 语言在浏览器端强大处理能力直接关系到我们所构建的 Web 应用程序的核心竞争力。在这篇笔记中，我们将具体为读者介绍如何使用这门语言处理浏览器端的工作。

## 前端编程概述

在基于网页浏览器的编程环境中，我们所使用的 JavaScript 语言其实是由三部分组成的。首先是语言的核心部分：ECMAScript，再来就是用于操作 HTML 文档的文档对象模型（DOM）和用于操作浏览器部分功能的浏览器对象模型（BOM）。换而言之，我们在前端编程中主要面对的是以下两个对象模型：

- **文档对象模型**： 即 Document Object Model，简称 DOM，它是一组按照 W3C 组织的标准定义的、用于操作 HTML 及 XML 文档的应用程序接口，JavaScript 是通过这些接口来操作 Web 页面中的各种元素的。简而言之，就是 DOM 会在内存中将读取到的 HTML 或 XML 文档解释成一个树状的数据结构，然后让 JavaScript 以增、删、改、查该树形结构上节点并为其注册事件响应函数的形式来完成对 Web 页面的处理。

- **浏览器对象模型**： 即 Browser Object Model，简称 BOM，该对象模型中包含了`windows`、`navigator`、`screen`、`history`、`location`等一系列与浏览器功能相关的对象组件，JavaScript 是通过它们来实现窗口的弹出与平移、获取浏览器名称、版本号、用户的操作系统、用户机器的屏幕分辨率以及用户之前的访问记录等超出 HTML 文档范围的、Web 应用的客户端功能。当然了，由于 BOM 长期以来并没有统一的标准，每个浏览器都有自己的 BOM 实现，所以我们在使用 BOM 时经常会遇到各种兼容性问题，但读者也不必太过担心，在 HTML5 标准发布并被广泛采用之后，这个问题已经得到了很大程度的解决，如今的主流浏览器几乎都采用了相同的对象实现，这些对象的方法和属性被约定俗成地统称为 BOM 的方法和属性。

除此之外，由于前端编程面对的环境是 Web 应用程序的用户界面，界面的装饰美化也是我们需要关注的任务。因此，以 CSS 为代表的 Web 美工技术也是我们学习前端编程必须要具备的基础知识。况且，如今在 JavaScript 的具体使用中，我们在选取页面元素时也会用到不少 CSS 选择器的使用思维。当然了。本书预设读者已经掌握了从 HTML5 到 CSS3 的所有相关基础技术，这里只是强调一下它们在前端开发中的重要性，具体就不做专门的介绍了，读者如果有需要的话，请自行阅读相关资料，补足相关的基础再继续后面的学习。

> 关联笔记：[[HTML 学习笔记]] [[CSS 学习笔记]]

当然了，除了与 HTML 和 CSS 相关的基础知识之外，初学者在具体学习如何在前端环境中使用 JavaScript 之前，还需要先对网页浏览器在前端编程中所扮演的角色要有一个基本的了解。下面，我们就来简单介绍一下这部分的基础知识。

### 浏览器的角色

正如我们之前所说，要学习 Web 应用程序的开发就必须要先分清楚浏览器和服务器在 B/S 架构下各自所扮演的角色，它们的分工具体如下：

- Web 服务器在 B/S 架构下所承担的角色通常被称之为 Web 应用程序的“后端”，主要负责存储并处理用户提交的请求数据，然后把响应数据返回给用户所在的 Web 浏览器。它一般用于处理较为复杂的业务逻辑，包括执行大型计算、存储海量数据等，开发与维护的成本都比较高。

- Web 浏览器在 B/S 架构下所承担的角色通常被称之为 Web 应用程序的“前端”，主要负责提供应用程序的用户操作界面，以及向 Web 服务器提交请求数据并接收来自服务器的响应数据。它一般用于处理与用户交互相关的业务逻辑，包括呈现数据、响应用户操作等。这部分的开发与维护成本主要受到浏览器的影响较大。

从上述分工可以看出，如果我们要想进行 Web 应用程序的前端开发，首先必须要熟悉应用程序主要面向的执行环境 —— 网页浏览器。就目前来说，浏览器之间差异主要来自于它们采用的渲染引擎。下面，让我们来对如今市面上主流的浏览器渲染引擎做个简单的介绍：

- **Trident**：Internet Explorer 浏览器采用的渲染引擎，除此之外，采用该渲染引擎的浏览器还有：Avant、Sleipnir、GOSURF、GreenBrowser 和 KKman 等。由于 Internet Explorer 浏览器是市占率最高的桌面操作系统 —— Windows 系统的内置浏览器，所以除非我们想开发一个小众的应用程序，否则就不能忽视采用这一引擎的浏览器。而且直到目前为止，国内主要的网上银行还都只支持 Internet Explorer 浏览器。
  
  由于 Internet Explorer 浏览器曾经长期处于垄断地位（从 Windows 95 的年代一直到 Windows XP 初期），一家独大的心态使得微软在很长一段时间内都惰于更新浏览器引擎，这让 Trident 引擎一度与 W3C 标准近乎脱节，并且累积了大量的安全性漏洞。也正因为如此，许多开发者和学者对采用这一引擎的浏览器一直都颇有微词，这客观上也促使了很多用户转向了采用其他引擎的浏览器。

- **Gecko**：最初是 Netscape 浏览器采用的渲染引擎，后来的 FireFox 浏览器也采用了这一引擎。由于 Gecko 是一款完全开源的浏览器渲染引擎，全世界的开发者都可以为其编写代码，因此受到许多人的青睐，采用 Gecko 引擎的浏览器也很多，除了被使用最多的 Firefox 浏览器，还包括 Mozilla SeaMonkey、waterfox、Iceweasel、K-Meleon 等。

- **Webkit**：最初是 Safari 浏览器采用的渲染引擎，后来的 Chrome 浏览器也采用了这一引擎 。在很长的一段时间里，该渲染引擎都只是 macOS 系统上 Safari 浏览器的专用引擎，非常小众。但随着 Safari 浏览器推出了 Windows 版，和 Chrome 浏览器的加入，以及这两款浏览器在分别在 iOS 和 Android 等移动端操作系统上所占据的主导地位，该浏览器引擎安全、稳定、快速的优势得到了极大的发挥。目前，Chrome 浏览器的市占率已经超越了 Internet Explorer，成为了浏览器领域新的领头羊。

在了解了主流浏览器采用的渲染引擎之后，我们就可以来介绍一下浏览器的工作原理了。正如我们之前所说，浏览器的主要功能就是向 Web 应用程序所在的服务器发出请求，然后在浏览器窗口中展示服务器返回来的响应数据。这里所说的响应数据一般是包括 HTML 文档、PDF 文档、图片、视频等不同类型的资源。具体来说，浏览器按照分工可以分成以下几个组成部分：

- **用户界面**：用户所请求的资源位置通常要通过 URI（统一资源标示符）的形式在浏览器的地址栏中或者用之前保存在浏览器中的书签来指定。除此之外，Web 页面的导航通常也需要通过浏览器显示区中的页面元素，或工具栏中的前进/后退按钮以及菜单栏中的历史列表来完成。这些功能都是浏览器的用户界面来提供的，它会负责将用户的请求数据交付给浏览器引擎，由后者将其发送给服务器。

- **浏览器引擎**：这一部分主要负责在用户界面和渲染引擎之间传送数据与操作指令，以及向服务器发送请求并接收响应，它是整个浏览器的调度中心。

- **页面渲染引擎**：这一部分主要负责显示响应数据的内容。具体来说，就是浏览器在收到服务器返回的响应数据之后，就会将其交给渲染引擎。如果返回的响应数据是 HTML 文档。它就负责解析 HTML 和 CSS 内容，并将解析结果排版后显示在屏幕上。如果返回的响应数据是 JavaScript 脚本代码，它就负责去调用 JavaScript 解释器，以便解释执行这些脚本代码。

- **前端数据存取**： Web 应用程序在某些情况下也会需要在客户端保存一些数据，例如用户允许浏览器记住的用户名和密码等，这时候就需要用到 Cookie 以及 HTML5 新定义的“网络数据库”这一类浏览器端的数据存储功能。

### 前端编程任务

由浏览器在 B/S 架构中扮演的角色可以看出，所谓 Web 应用程序的前端开发，应该主要包含以下任务：

- 第一： **设计 Web 应用的用户界面**：这部分的任务包括用 HTML 来定义的网页结构，和用 CSS 来设计的网页样式。在这部分工作中，我们会决定 Web 应用要在浏览器中呈现的标题、段落、列表、表格、图片以及音乐、视频等多媒体页面元素，这是基本的，也是我们后续工作的基础所在。

- 第二： **赋予 Web 应用的用户界面与用户交互的能力**：这部分的任务包括响应网页上所有被注册了相关事件的元素，以及部分用户对浏览器本身所做的操作，譬如前进/后退的导航按钮、将某些数据存储到 Cookie 中等。这部分工作我们就主要是通过 JavaScript 这一类浏览器脚本语言来实现的。

在明确了前端开发中要完成的具体任务之后，接下来，我们就可以来具体研究如何使用 JavaScript 语言来完成这些任务了。下面，让我们先从用于操作 HTML/XML 元素的、最基础的 DOM 接口开始。

## 文档对象模型

在这一节中，我们将详细为读者介绍文档对象模型（即 DOM）。首先，我们会简略地回顾一下 DOM 的发展历程。以便读者能更全面地理解 DOM 标准规范的来龙去脉，发展现况以及使用思路。然后，我们会借助大量示例来演示如何在 JavaScript 中用 DOM 处理 HTML 文档中的各种页面元素。

### 起源与标准化历程

正如我们之前所说，DOM 是 由 W3C 组织负责标准化的一套最初只针对 XML 文档，后来逐步扩展到 HTML 文档的应用程序接口。和 JavaScript 一样，在标准化的文档对象模型出现之前，由于微软和网景这两家公司在浏览器市场上的恶性竞争，Web 应用的开发者们经历过一段较为黑暗的时代。在那个混沌的年代里，Internet Explorer 4 和 Netscape Navigator 4 各自实现的是不同的 DHTML（即 Dynamic HTML）接口，彼此在很多地方都互不兼容，这让 HTML 面临着失去跨平台的先天性优势的危机，而开发者们为了扩展 Web 应用的市场。又必须要尽可能地维持程序在双方浏览器上的兼容性，这往往需要付出非常大的精力来构建一些看起来极不优雅并且后期难以维护的解决方案。时至今日，笔者每每回忆起那些岁月所做的 Web 开发，其过程真是让人苦不堪言。

于是，为了响应广大开发者的呼声，对软件寡头们之间的恶性竞争行为进行约束，负责制定 Web 通信标准的 W3C 组织制定出了一套统一面向 XML 和 HTML 文档的应用程序接口规范，即 DOM 标准。这套标准按照其制定进展，各大浏览器对 DOM 的支持通常被分为以下几个级别：

- **DOM 0**：该级别在标准化的意义上其实是不存在的，因为它实际上是标准化初级阶段的 DOM，大部分实现还停留在实验阶段，但如今开发者们习惯上将其称之为 DOM 0。在实现了这一级别的浏览器中，具有代表性的就是分别在 1997 年的 6 月和 10 月发布的 Internet Explorer 4 和 Netscape Navigator 4、这两款浏览器都各行其是地定义了一组用于操作 HTML 文档的应用程序接口，从而使 JavaScript 的功能得到了大大地扩展，如今我们更习惯将这些扩展称之为 DHTML。需要说明的是，DHTML 并不是一项新技术，而是将 HTML、CSS、JavaScript 技术组合的一种描述。即：

    – 利用 HTML 标签将 Web 页面划分为各种页面元素。
    – 利用 CSS 样式来设置这些页面元素的外观及位置。
    – 利用 JavaScript 脚本来操控页面元素及其外观样式。

    但正如之前所说，由于没有统一的规范和标准，这两款浏览器对相同功能的实现确完全不一样。为了保持程序的兼容性，Web 开发者们必须先写一些探测性的代码来检测一下自己编写的 JavaScript 脚本到底运行于哪一款浏览器之下，然后再切换至与之对应的脚本片段。但这就让 Web 应用程序的代码变得前所未有的臃肿，且难以维护，DHTML 也因此在人们心中留下了非常糟糕的印象。

- **DOM 1**：W3C 组织在结合了各方浏览器实现的优点之后。于 1998 年的 10 月完成了第 1 级的 DOM，我们习惯上称之为：DOM 1。DOM 1 主要定义了 XML 和 HTML 文档的底层结构，它主要由 DOM Core 和 DOM HTML 两个部分组成。其中，DOM Core 规定的是 XML 文档的结构标准，该标准简化了我们对文档中页面元素的操作。而 DOM HTML 则是在 DOM Core 的基础上做了进一步的扩展，添加了许多面向 HTML 文档的对象和方法，譬如用于表示整个文档的document对象及其方法。

- **DOM 2**：DOM 2 引入了更多的交互能力，也支持了更高级的 XML 特性。DOM 2 在原来 DOM 1 的基础上又扩充了鼠标、键盘等用户界面事件，并通过对象接口增加了对 CSS 的支持。DOM 2 中的 DOM Core 也经过扩展开始支持 XML 命名空间。具体来说就是，DOM 2 在 DOM 标准中引入了下列模块：

    – DOM Views：该模块定义了跟踪不同文档视图的接口。
    – DOM Events：该模块定义了事件和事件处理的接口。
    – DOM Style：该模块定义了基于 CSS 样式为页面元素设置外观的接口。
    – DOM Traversal & Range：该模块定义了遍历和操作文档树的接口。

- **DOM 3**：DOM 3 在 DOM 2 的基础上进一步扩展了 DOM，它继续在 DOM 标准中引入了以下模块：
    – DOM Load & Save：该模块定义以统一方式加载和保存文档的接口。
    – DOM Validation：该模块定义了验证文档的接口。
    – DOM Core 的扩展：增加了对 XML 1.0 规范的支持，包含了 XML Infoset、XPath 和 XML Base 等组件。

除此之外，W3C 组织也制定了一系列专用标记语言的 DOM 扩展标准。例如：用于制作矢量图的 SVG，用于编写数学公式的 MathML，用于描述多媒体的 SMIL 等，这些都是基于 XML 扩展而来的标记语言，DOM 标准也为它们定义了专用的应用程序接口。

当然，W3C 组织只负责制定标准，浏览器对标准的实现完成度才是我们在编程过程中所要面对的实际问题。幸运的是，经过多年的努力，如今的 Chrome 和 Firefox 等主流浏览器都基本实现了 DOM 标准制定的接口，但由于一些历史遗留问题，Internet Explorer 浏览器在实现 DOM 标准的同时，依然保留了大量标准化之前的 OnlyIE 的接口。这样做主要是为了确保大量旧时代的代码依然能正确运行，作为标准化之后的开发者，我们在编写新的代码时就不宜再使用这些接口了。关于这一点，我们稍后在具体介绍 DOM 接口的调用时会特别举例说明。

### DOM 的树状结构

在具体使用 DOM 之前，我们首先要明确一个概念，即 DOM 只是一套用于处理 XML 和 HTML 文档的应用程序接口，它并不是 JavaScript 专有的，VBScript、Python 等脚本语言也一样可以调用这套接口。所以换句话说，DOM 本质上是一套以 XML 这类结构化标记语言为中心的编程工具，它的设计目的是为 XML 和 HTML 这类文档提供一种映射在内存中的数据结构，以便其他编程语言可以在程序运行时通过该数据结构来操作文档，从而改变文档的结构，样式和内容。具体来说就是，DOM 会将其读取到的 XML 和 HTML 文档映射到在内存中一个树状的数据结构上，文档界面中的每个页面元素都会被解析成该树状结构上的节点，然后其他脚本语言就可以通过增、删、改。查这些节点来完成对这些文档的处理。举个例子，对于下面这个 HTML 文档：

```html
<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>浏览器标题栏文字</title>
    </head>
    <body>
        <h1>网页一级标题</h1>
        <div>
            <p>网页正文内容</p>
        </div>
    </body>
</html>
```

如果我们想要在程序中直接对上述文本进行解析，那就得从上到下逐行读取，然后用词法分析算法处理每一行中的语法标记，整个过程是非常复杂的，基本上是在亲手实现一个网页浏览器，这完全不符合编程方法中“不重复发明轮子”的原则，现在有了 DOM 标准接口，浏览器就会自行根据其读取到的文档在内存中创建一个与之相对应的树状数据结构，该数据结构其大致如下图所示：

![DOM 树状结构示意图](img/1.png)

然后，我们就只需要直接在 JavaScript 或 VBScript 脚本中对该树状结构进行操作即可。换句话说，开发人员现在不必再去亲自解析 XML 和 HTML 文档的具体文本了，DOM 已经将目标文档转换成了内存中一个可直接操作的树状结构，并且其接口设计完全适用于面向对象编程，这显然就大大简化了 Web 应用程序开发的复杂度。

### 节点类型及其接口

如果我们之前学过数据结构的基础理论，就该知道“树（Tree）”是一种以开枝展叶的形式将多个节点链接起来的多层结构体。其             节点之间的关系非常类似于传统家庭里的父系族谱，从被称为“根”的单一节点往下，每一个节点都与其上下一层的节点之间是父子辈关系，与同一层节点之间是兄弟关系。例如在上面的 DOM 结构示意图中，`html`节点是整个树状结构的根节点，`head`和`body`则是它的两个子节点，而`h1`和`div`这两个节点则又是`body`节点的子节点。与此同时，由于`h1`和`div`来自同一个父节点，所以它们彼此是兄弟节点的关系。

所以在 DOM 标准所定义的接口中，节点（Node）是我们可操作的最基本类型。其树状数据结构中的每一个节点都对应着 HTML 文档中的一个标签元素。为了便于对所有的节点进行统一处理，DOM 标准定义了一套适用于所有 DOM 节点对象的接口，下面我们来介绍其中比较常用的一些属性和方法：

- **`nodeType`属性**：该属性值是一个从 1 到 12 的整数常量，每个常量都代表着一种类型的 DOM 节点对象，具体如下：

    | 常量标识符                  | 常量值 | 相关说明                                                         |
    | --------------------------- | ------ | ---------------------------------------------------------------- |
    | Node.ELEMENT_NODE           | 1      | 代表 XML 或 HTML 文档中的页面元素，通常对应着一个具体的页面标记。   |
    | Node.ATTRIBUTE_NODE         | 2      | 代表页面元素的某一个属性，譬如div元素的id属性。                    |
    | Node.TEXT_NODE              | 3      | 代表页面元素或其属性中的文本内容，譬如p元素中的文本。               |
    | Node.CDATASECTIONNODE       | 4      | 代表文档中用<![CDATA[]]>表示声明的不需要解析的文本。               |
    | Node.ENTITYREFERENCENODE    | 5      | 代表实体引用，常见于 XML 文档中。                                 |
    | Node.ENTITY_NODE            | 6      | 代表实体，常见于 XML 文档中。                                     |
    | Node.PROCESSINGINSTRUCTIONNODE | 7      | 代表ProcessingInstruction对象，常见于 XML 文档。                  |
    | Node.COMMENT_NODE           | 8      | 代表文档中的注释节点，即<!--注释内容--->标签的内容。               |
    | Node.DOCUMENT_NODE          | 9      | 代表整个文档，即DOM 树的根节点：document对象。                     |
    | Node.DOCUMENTTYPENODE       | 10     | 代表文档采用的接口版本，譬如<!DOCTYPE html>代表的是 HTML5。        |
    | Node.DOCUMENTFRAGMENTNODE   | 11     | 代表 HTML 文档的某个部分，但它没有对应的元素标签，也不直接显示在浏览器中。 |
    | Node.NOTATION_NODE          | 12     | 代表 DTD 中声明的符号。                                           |

    但在通常情况下，我们只需要记住以下几种常用的节点类型即可：

    | nodeType值 | 对应的节点类型 |
    | ---------- | -------------- |
    | 1          | 元素节点       |
    | 2          | 属性节点       |
    | 3          | 文本节点       |
    | 8          | 注释节点       |
    | 9          | 文档节点       |

    当然了，我们在之前的那一张表中也看到了，DOM 标准事实上是为这些常量定义了相应的常量标识符的，譬如元素节点是`node.ELEMENT_NODE`、属性节点是`node.ATTRIBUTE_NODE`、文本节点是`node.TEXT_NODE`、注释节点是`node.COMMENT_NODE`、文档节点是`node.DOCUMENT_NODE`等。奈何并不是所有的浏览器都支持了这些标识符（譬如微软的 IE8 及其更早的版本就不支持它们），所以我们通常还是直接使用数字来判断节点类型。

- **`nodeName`属性**：该属性的值取决于节点的具体类型，常见情况如下：

  - 元素节点的`nodeName`属性值是其对应的 HTML 标签名。
  - 属性节点的`nodeName`属性值与其对应 HTML 标签的属性名相同。
  - 文本节点的`nodeName`属性值始终为`#text`。
  - 注释节点的`nodeName`属性值始终为`#comment`。
  - 文档节点的`nodeName`属性值始终为`#document`，

- **`nodeValue`属性**：该属性的值也取决于节点的具体类型，常见情况如下：

  - 元素节点的`nodeValue`属性值是`undefined`或`null`。
  - 属性节点的`nodeValue`属性值是其对应 HTML 标签属性的值。
  - 文本节点的`nodeValue`属性值是其对应 HTML 标签中的文本本身。

  请注意：如果希望返回指定元素节点中的文本，请务必要记住文本始终位于文本节点中，我们必须先获取该元素节点下面的文本节点，才能读取到这段文本。例如，假设我们要获取`element`这个元素节点下的文本，就应该这样写：

    ```javascript
    const someText = element.childNodes[0].nodeValue;
    ```

- **`childNodees`属性**：事实上，我们在上面的代码中已经迫不及待地使用该属性了，这也间接说明了它是节点接口中最常用的属性之一。该属性中存储的是当前节点的所有子节点，这是一个实现了迭代器接口的`NodeList`对象，我们可以将其作为一个数组对象来使用，譬如对其进行如下遍历：

    ```javascript
    for(let i = 0; i < element.childNodes.length; ++i) {
        console.log(element.childNodes[i].nodeName);
    }
    ```

    或者直接通过`for-of`循环，利用迭代器接口来完成遍历：

    ```javascript
    for(let aNode of element.childNodes) {
        console.log(aNode.nodeName);
    }
    ```

- **`firstChild`属性**：该属性引用的是当前节点的第一个子节点，即`aNode.childNodes[0]`的值。

- **`lastChild`属性**：该属性引用的是当前节点的最后一个子节点，即`aNode.childNodes[aNode.childNodes.length-1]`的值，而当某个节点只有一个子节点时，其`firstChild`属性和`lastChild`属性指向的是同一个节点。

- **`parentNode`属性**：该属性引用的是当前节点的父节点，当且仅当当前节点为根节点时，该属性值为`null`。

- **`previousSibling`属性**：该属性引用的是当前节点的前一个兄弟节点，即该节点在其共同父节点的`childNodes`属性中的索引位置是当前节点的前一个，当且仅当当前节点为其父节点的第一个节点时，该属性值为`null`。

- **`nextSibling`属性**：该属性引用的是当前节点的后一个兄弟节点，即该节点在其共同父节点的`childNodes`属性中的索引位置是当前节点的后一个，当且仅当当前节点为其父节点的最后一个节点时，该属性值为`null`。

- **`appendChild()`方法**：该方法的作用是在当前节点的`childNodes`属性的最后一个索引位置后面再继续添加一个子节点，它只接收一个节点类型的实参，用于传递要添加的节点。例如：

    ```javascript
    aNode.appendChild(newNode);
    console.log(aNode.lastChild == newNode); // 输出：true
    ```

- **`insertChild()`方法**：该方法的作用是在当前节点的`childNodes`属性中指定位置的前面再继续添加一个子节点，它接收两个节点类型的实参，第一个实参用于传递要添加的节点，第二个实参用于指示节点的添加位置，通常是`childNodes`属性中的某个现有节点，新节点会被添加在该节点之前，而当该实参值为`null`时，就相当于调用了`appendChild()`方法，新节点会被添加到`childNodes`列表的末尾。与此同时，该方法也会返回这个新添加的节点。下面来看几个示例：

    ```javascript
    // 将新节点添加到第一个子节点前面
    const returnNode = aNode.insertChild(newNode, aNode.firstChild);
    console.log(aNode.firstChild == newNode);  // 输出：true
    console.log(returnNode == newNode);        // 输出：true

    // 将新节点添加到最后一个子节点前面
    aNode.insertChild(newNode, aNode.lastChild);
    console.log(aNode.lastChild.previousSibling == newNode);  // 输出：true

    // 将新节点添加为最后一个子节点
    aNode.insertChild(newNode, null);
    console.log(aNode.lastChild == newNode);  // 输出：true
    ```

- **`replaceChild()`方法**：该方法的作用是用一个新节点去替换当前节点的某一个被指定的子节点，它接收两个节点类型的实参，第一个实参传递的是将被用于替换的新节点，第二个实参指向的是当前节点的某个子节点，它是我们的替换目标，并且将作为方法的返回值被返回。下面来看几个示例：

    ```javascript
    // 替换当前节点的第一个子节点
    const oldNode = aNode.firstChild;
    const returnNode = replaceChild(newNode, aNode.firstChild);
    console.log(aNode.firstChild == newNode); // 输出：true
    console.log(returnNode == oldNode);       // 输出：true

    // 替换当前节点的最后一个子节点
    const oldNode = aNode.lastChild;
    const returnNode = replaceChild(newNode, aNode.lastChild);
    console.log(aNode.lastChild == newNode); // 输出：true
    console.log(returnNode == oldNode);       // 输出：true
    ```

- **removeChild()`方法**：该方法的作用是移除一个指定的当前节点的子节点，它只接收一个节点类型的实参，用于指定需要被移除的节点，并将其作为返回值返回。下面来看几个示例：

    ```javascript
    // 移除当前节点的第一个子节点
    const oldNode = aNode.firstChild;
    const newFirstChild = aNode.firstChild.nextSibling;
    const returnNode = removeChild(aNode.firstChild);
    console.log(aNode.firstChild == newFirstNode); // 输出：true
    console.log(returnNode == oldNode);            // 输出：true

    // 移除当前节点的第一个子节点
    const oldNode = aNode.lastChild;
    const newLastChild = aNode.lastChild.previousSibling;
    const returnNode = removeChild(aNode.lastChild);
    console.log(aNode.lastChild == newLastNode);   // 输出：true
    console.log(returnNode == oldNode);            // 输出：true
    ```

- **`cloneNode()`方法**：该方法的作用是复制当前节点，它只接收一个布尔类型的实参。当实参值为`false`时，该方法执行的是浅拷贝，它返回的是当前节点的引用。当实参值为`true`时，该方法执行的是深拷贝，它会将当前节点及其所有子节点全部重新复制一份，并该副本的引用返回。下面来看个示例，假设`aNode`节点的内容如下：

    ```html
    <div id="targetID">
        <p>这是一个 div 区域。</p>
    </div>
    ```

    我们就可以对它编写如下代码：

    ```javascript
    // 浅拷贝
    const shallowCopy = aNode.cloneNode(false);
    console.log(shallowCopy.childNodes.length);  // 输出：0

    // 深拷贝
    const deepCopy = aNode.cloneNode(true);
    console.log(deepCopy.childNodes.length);    // 输出：3
    ```

细心的读者可能已经发现了，上面这些的代码大多数都无法直接执行，因为我们既没有介绍当前节点`aNode`如何获取，也没有介绍新节点`newNode`如何创建，代码根本就是无的放矢，没有具体操作对象。这是因为这两个操作都要取决于节点的具体类型，接下来就让我们来补上这一课吧。

正如我们之前所说，DOM 节点的类型实际上有 12 种，但其中的绝大部分不是在 HTML 文档中不太常用，就是因在各大浏览器中的行为尚不一致而不被推荐，所以我们实际需要熟悉并时常用到的节点类型只有之前在第二张表中列出的元素节点、属性节点、文本节点、注释节点以及文档节点。下面，我们就逐一来介绍一下这些节点类型以及它们所提供的接口。

- **文档节点**：文档节点通常用于代表一整个 XML 或 HTML 文档，换句话说，一个文档的 DOM 树状结构中往往有且只能有一个文档节点。文档节点的`nodeType`的值为 9、`nodeName`的值为`#document`、`nodeValue`的值为 null。而在浏览器环境下，文档节点事实上是一个名为`document`的全局对象，我们通常都是通过这个对象来获取当前 HTML 页面中的信息，并对页面中的元素执行各种操作的。下面，我们就来了解一下 DOM 标准为文档节点定义的专用接口（文档节点自然也继承了上一节中介绍的所有统一节点接口，这里就不重复介绍了）：

  - `documentElement`属性： 在 HTML 文档中，这个属性代表的是当前页面的`<html>`标签，它在 DOM 树状结构中对应着一个元素类型的节点。在某些浏览器的实现中，该节点有时也是文档节点的的第一个子节点。对此，我们可以用下面的代码来验证一下：

    ```javascript
    const htmlNode = document.documentElement;
    console.log(htmlNode == document.firstChild);
    // 某些浏览器会输出 false，而另一些则输出 true。
    ```

  - `body`属性： 在 HTML 文档中，这个属性代表的是当前页面的`<body>`标签，它在 DOM 树状结构中也对应着一个元素类型的节点。由于在 Web 开发中，我们要执行绝大部分操作针对的都是该节点的子节点，所以该属性应该是`document`对象使用率最高的属性之一了。与此同时，它在通常情况下还应该是上述`htmlNode`节点的最后一个子节点，我们可以接着上面的代码继续来验证一下：

    ```javascript
    const bodyNode = document.body;
    console.log(bodyNode == htmlNode.lastChild);
    ```

  - `title`属性： 该属性中存储的是`<title>`标签中的文本，该文本会通常出现在浏览器窗口的标题栏和标签页中。我们也可以用该属性来修改当前页面的标题，例如：

    ```javascript
    console.log(document.title); // 输出现有标题
    document.title = 'new title';
    console.log(document.title); // 输出：new title
    ```

  - `URL`属性： 该属性中存储的是当前页面在浏览器地址栏中显示的 URL，我们是通过该 URL 来向服务器发送访问当前页面的请求的。

  - `domain`属性： 该属性中存储的是当前页面的 URL 所属的域名，譬如，假设当前页面的 URL 是`http://owlman.org/index.htm`，该属性值就是`owlman.org`。

  - `referrer`属性： 该属性中存储的是链接到当前页面的那个页面的 URL。譬如，假设我们是通过`http://owlman.org/index.htm`这个页面访问到`http://owlman.org/readme.htm`的，那么，后者的该属性值就是`http://owlman.org/index.htm`。当然了，如果当前页面不来自任何页面，我们是亲自输入 URL 来访问它的，那该属性值就为`null`。

  - `anchors`属性： 该属性是一个类数组对象，其中存储的是当前页面中所有设置了`name`属性的`<a>`元素。

  - `forms`属性： 该属性也是一个类数组对象，其中存储的是当前页面中所有的`<form>`元素。

  - `images`属性： 该属性也是一个类数组对象，其中存储的是当前页面中所有的`<img>`元素。

  - `links`属性： 该属性也是一个类数组对象，其中存储的是当前页面中所有设置了`href`属性的`<a>`元素。

  - `getElementById()`方法： 该方法的作用是获取当前页面中指定`id`值的页面元素，如果当前页面中有`id`值相同的元素，就选取其中的第一个元素。在上一节中频繁出现的`aNode`节点通常就是用该方法来获取的。例如对于下面的 HTML 文档：

    ```html
    <!DOCTYPE html>
    <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>浏览器端JS代码测试</title>
            <link rel="stylesheet" type="text/css" href="style.css" />
            <script type="module" src="test.js"></script>
        </head>
        <body>
            <noscript>
                <p>本页面需要浏览器支持或启用JavaScript。</p>
            </noscript>
            <h1>浏览器端的JavaScript</h1>
            <div class="box" id="box_1">
                <p>这是一个 div 区域。</p>
            </div>
            <div class="box" id="box_2">
                <p>这是另一个 div 区域。</p>
            </div>
            </body>
    </html>
    ```

    如果我们想获取`id`值为`box_1`的`<div>`元素，就可以在其外链的`test.js`文件中编写如下代码：

    ```javascript
    const aNode = document.getElementById('box_1');

    // 浅拷贝
    const shallowCopy = aNode.cloneNode(false);
    console.log(shallowCopy.childNodes.length);  // 输出：0

    // 深拷贝
    const deepCopy = aNode.cloneNode(true);
    console.log(deepCopy.childNodes.length);    // 输出：3
    ```

    请注意：这里的`id`值在大部分浏览器中是严格区分大小写的，或许只有 IE7 及其早期版本例外。

    - `getElementsByName()`方法： 该方法的作用是返回一个类数组对象，其中包含了当前页面中所有设置了相同`name`值的元素。我们经常会在处理表单中的单选框时用到它，毕竟为了让浏览器知道哪一些单选框属于同一组互斥性选项，我们会将同一组单选框赋予相同的`name`值。

    - `getElementsByTagName()`方法： 该方法的作用是返回一个类数组对象，其中包含了当前页面中所有使用了相同标签的元素，例如，我们上面介绍某些类数组功能的属性也可以使用该方法来实现：

    ```javascript
    console.log(document.forms == document.getElementsByTagName('form'));
    console.log(document.images == document.getElementsByTagName('img'));
    ```

    - `getElementsByClassName()`方法： 该方法的作用是返回一个类数组对象，其中包含了当前页面中设置了相同`class`属性的元素。众所周知，在 HTML 文档中，元素的`class`属性主要是提供给 CSS 设计样式的，而有时候样式的设置需要 JavaScript 脚本的配合。例如，如果我们想为之前那个 HTML 文档中所有设置了`box`样式的元素注册一个鼠标单击事件，就可以在其外链的`test.js`文件中这样写：

    ```javascript
    const aClassNodes = document.getElementsByClassName('box');
    for(const tmpNode of aClassNodes) {
        tmpNode.onClick = function() {
            tmpNode.className = 'newStyle';
        }
    }
    ```

    当然，读者在这里暂时不必理会事件的概念，我们将会在之后的笔记中具体介绍这部分的内容。

    - `write()`方法： 该方法的作用是将其接收到的字符串类型的实参原样输出到`document`对象所代表的 HTML 文档中。

    - `writeln()`方法： 该方法的作用与`write()`方法基本相同，唯一的区别是该方法会在输出实参字符串的同时加上一个换行符。例如，我们可以在之前使用的 HTML 文档中`id`值为`box_2`的`div`元素后面再添加一个`<script>`标签，具体如下：

    ```html
    <!DOCTYPE html>
    <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>浏览器端JS代码测试</title>
            <link rel="stylesheet" type="text/css" href="style.css" />
            <script type="module" src="test.js"></script>
        </head>
        <body>
            <noscript>
                <p>本页面需要浏览器支持或启用JavaScript。</p>
            </noscript>
            <h1>浏览器端的JavaScript</h1>
            <div class="box" id="box_1">
                <p>这是一个 div 区域。</p>
            </div>
            <div class="box" id="box_2">
                <p>这是另一个 div 区域。</p>
            </div>
            <script>
                document.write('当前时间是：');
                const now = new Date();
                document.writeln(now.toLocaleDateString());
            </script>
        </body>
    </html>
    ```

    - `createElement()`方法： 该方法的作用是创建一个新的元素节点。例如，对于之前示例中没有详细说明来历的、代表新节点的`newNode`对象，我们可以这样创建：

    ```javascript
    const newNode = document.createElement('div');
    document.body.appendChild(newNode);
    ```

    如你所见，`createElement()`方法只接收一个代表新建元素标签名的字符串为实参，并且对于 HTML 标签来说，该实参值是不区分大小写的。关于元素节点本身的具体操作，我们稍后会详细介绍。

    - `createAttribute()`方法： 该方法的作用是创建一个新的属性节点。例如，我们可以这样为上面的`newNode`节点添加一个属性节点：

    ```javascript
    const attrNode = document.createAttribute('class');
    attrNode.value = 'box';
    newNode.setAttributeNode(attrNode);
    ```

    如你所见，`createAttribute()`方法也只接收一个字符串类型的实参，用来指明新建属性节点的名称。关于属性节点本身的操作，我们稍后会做详细介绍。

    - `createTextNode()`方法： 该方法的作用是创建一个新的文本节点，它也只接收一个字符串类型的实参，用来指定其创建节点所要容纳的文本。例如，我们可以这样为上面的`newNode`节点所代表的`<div>`标签中添加一段文本：

    ```javascript
    const textNode = document.createTextNode('这是box_4中的文本。');
    newNode.appendChild(textNode);
    ```

    关于文本节点本身的操作，我们稍后会做详细介绍。

    - `createComment()`方法： 该方法的作用是创建一个新的注释节点，它同样只接收一个字符串类型的实参，用来指定注释的内容。例如，如果我们想在上述`newNode`节点所代表的`<div>`标签中添加一段注释，可以这样做：

    ```javascript
    const myComment = document.createComment('这是一个用脚本添加的div元素。');
    newNode.appendChild(myComment);
    console.log(newNode.lastChild.data); // 输出：这是一个用脚本添加的div元素。
    ```

    我们稍后也会具体介绍注释节点本身的属性和方法。在这里需要注意的是，`document`对象虽然可以往 HTML 文档中写入字符串，或对文档中的特定元素执行各种增、删、改、查操作，但作为文档节点本身，它是只读的。换句话说，我们直接在`document`对象上调用`appendChild()`、`removeChild()`这一类增删直系子节点的方法是无效的。

- **元素节点**：在 DOM 的定义中，元素节点代表的是 XML 或 HTML 文档中的各种页面元素，其`nodeType`的值为 1、`nodeName`的值为它们各自对应的页面标签、`nodeValue`的值为 null。在 Web 前端开发的语境下，元素节点通常对应着一个具体的 HTML 标签。例如，之前调用的`document.body`属性返回的就是一个 HTML 标签为`<body>`的元素节点。严格来说，HTML 的每一种标签都对应着一种类型的元素节点，但在通常情况下，我们在处理元素节点时不需要进行如此细致的分类，只需要熟练掌握一部分通用的属性和方法就足以解决绝大部分问题了。下面就来介绍一下这些属性和方法，首先是任意一种元素节点都有的通用属性：

  - `tagName`属性： 该属性的作用是返回当前元素节点所对应的 HTML 标签，事实上可以认为这是`nodeName`属性的一个别名。但该属性专属于元素节点，无论从接口语义上，还是在名称上都显得要更直观一些，例如对于之前所用的 HTML 文档中的第一个`<div>`元素，我们可以这样查看它的标签名：

    ```javascript
    const aNode = document.getElementById('box_1');
    console.log(aNode.tagName);   // 输出：DIV
    ```

    需要注意的是，`tagName`属性返回的 HTML 标签名都是用大写字母来表示的，而对于 XML 标签，它返回的则是文档中实际使用的标签字符。所以，如果我们不清楚自己编写的脚本是用于处理 HTML 还是 XML，就必须要对`tagName`属性返回的字符串进行统一的大小写转换。

  - `id`属性： 该属性的作用是返回当前元素节点所对应 HTML 标签的id属性。例如对于上面的`aNode`节点，我们可以这样查看它的id属性：

    ```javascript
    console.log(aNode.id);  // 输出：box_1
    ```

  - `className`属性： 该属性的作用是返回当前元素节点所对应 HTML 标签的`class`属性，但由于`class`在 JavaScript 中属于语言本身的关键字，所以只能将其对应属性命名为`className`。例如我们可以这样查看`aNode`节点的`className`属性：

    ```javascript
    console.log(aNode.className); // 输出：box
    ```

  - `title`属性： 该属性的作用是返回当前元素节点所对应 HTML 标签的`title`属性，该属性主要用于对相关的页面元素进行说明，当鼠标悬停在该元素上时就会显示。例如我们可以这样查看`aNode`节点的`title`属性：

    ```javascript
    console.log(aNode.title);
    ```

  - `lang`属性： 该属性的作用是返回当前元素节点所对应 HTML 标签的`lang`属性，该属性主要用于声明相关页面元素及其子元素所采用语言的编码。例如在编写中文网页时，我们通常会这样编写`<html>`标签：`<html lang="zh-CN">`。当然，在一般元素节点中很少需要设置该属性。到了JavaScript 中，我们可以这样查看`aNode`节点的lang属性：

    ```javascript
    console.log(aNode.lang);
    ```

  - `dir`属性： 该属性的作用是返回当前元素节点所对应 HTML 标签的`dir`属性，该属性主要用于说明当前页面中文字的走向，它只有两个值，分别是代表从左向右的`ltr`和代表从右向左的`rtl`，当然了，这一属性在实际开发中也很少被用到，相关的工作一般会交由 CSS 来完成。例如我们可以这样查看`aNode`节点的`dir`属性：

    ```javascript
    console.log(aNode.dir);
    ```

    到目前为止，我们所介绍的这些属性反映的都是一个元素节点的基本信息。这些信息不仅可以读取。也可以在 JavaScript 中修改它们。例如，我们可以这样修改`aNode`节点的基本信息：

    ```javascript
    aNode.id = 'box_3';
    aNode.className = 'newBox';
    aNode.title = '第三段测试文本';
    aNode.lang= 'en';
    aNode.dir = 'rtl';
    ```

    当然，上面这些属性对应的都是每个 HTML 标签都有的通用属性，它们自然可以通过 DOM 节点对象的属性方式来操作。除此之外，还会有一些特定标签的专用属性，例如`<a>`标签的`href`属性、`<img>`标签的`src`属性等。基本上，对于 HTML 规范所定义的标签属性，DOM 中与之对应的元素节点对象都是有相应的属性的。例如，对于下面这个设置了`onclick`事件的`<a>`元素：

    ```html
    <a id="sayhello" href="#" onclick="alert('hello')">打个招呼</a>
    ```

    我们仍然可以通过 DOM 对象属性的方式来对其进行操作，像这样：

    ```javascript
    const sayhello = document.getElementById('sayhello');
    console.log(typeof sayhello.onclick);                  // 输出：function
    sayhello = function() {};
    ```

    除此之外，我们还可以选择调用 DOM 提供的三个属性方法：

  - `getAttribute()`方法： 该方法的作用是读取当前元素的指定属性，它会接收一个字符串类型的实参，用于指定要读取的属性名。需要注意的是，这里的属性名是要与当前元素对应的 HTML 标签的属性名相同。譬如对于`<div>`标签的`class`属性，我们传递给该方法的实参值就应该是`class`，而不是`className`了。下面，我们来具体演示一下该方法的使用：

    ```javascript
    // 获取当前页面中所有<img>标签的src属性
    for(const image of document.images) {
        console.log(image.getAttribute('src'));
    }

    // 获取当前页面中所有<a>标签的href属性
    for(const link of document.links) {
        console.log(link.getAttribute('href'));
    }
    ```

    另外，需要注意的是，`getAttribute()`方法的实参值并不区分大小写，换句话说，`SRC`和`src`指定的是相同的属性名，如果该方法没有找到指定的属性名，就会返回 null。

  - `setAttribute()`方法： 该方法的作用是设置当前元素节点所对应 HTML 标签中指定属性的值，如果指定的属性不存在，那就创建该属性。它接收两个实参，第一个实参是一个用于指定目标属性名的字符串，该实参的用法规则与`getAttribute()`方法的实参完全相同。第二个实参则是目标属性的值。下面，我们来具体演示一下该方法的使用：

    ```javascript
    // 为当前页面中所有<img>标签设置src属性
    for(let i = 0; i < document.images.length; ++i) {
        document.images[i].setAttribute('src', i+'.png');
    }
    ```

  - `removeAttribute()`方法： 该方法的作用是删除当前元素节点对应 HTML 标签中的指定属性，这一方法在实际开发中并不常用。

  但这三个方法存在着一个明显的问题，即它们都是以字符串的形式来增、删、改、查相应 HTML 标签中的属性的。换句话说，它们读取到的`onclick`属性是一段内容是 JavaScript 代码的字符串，而不是一个`function`类型的对象。我们可以用`typeof`操作符来验证一下使用 DOM 元素对象的属性与调用`getAttribute()`方法的区别：

    ```javascript
    console.log(typeof sayhello.onclick);                 // 输出：function
    console.log(typeof sayhello.getAttribute('onclick'));  // 输出：string
    ```
  
  正是出于这样的原因，在实际开发中，我们对于 HTML 规范定义的标签属性，基本都会采用 DOM 对象属性的方式来操作。但我们有时候也会为某些标签添加一些自定义属性，譬如在 HTML5 规范中，我们通常会定义一些名称以data-为前缀的可被验证的自定义属性，用来传递某些特定的数据，这些属性在对应的 DOM 对象中是没有相应属性的。通常只有对于这样的自定义属性，我们才会使用到`getAttribute()`方法。例如，对于下面这个带有自定义属性的`<div>`标签：

    ```html
    <div id="box_4" data-sayhello="hello"></div>
    ```

  我们可以分别用对象属性和调用`getAttribute()`方法这两种方式分别来访问一下上述`<div>`标签中的自定义属性`data-sayhello`的值，看看各自是什么结果：

    ```javascript
    const otherNode = document.getElementById('box_4');
    console.log(otherNode.data-sayhello);                  // 输出：NaN 或 undefined
    console.log(otherNode.getAttribute('data-sayhello'));  // 输出：hello
    ```

  如你所见，用对象属性方式访问标签自定义属性的结果是因浏览器而异的，有些浏览器会返回 NaN，有些浏览器则会返回 undefined。所以在实际开发中，我们通常会用`getAttribute()`方法来访问 HTML 标签的自定义属性。最后，如果我们在某些情况下需要以 DOM 节点对象的形式操作相关元素的属性的话，也可以选择调用以下三个方法：

  - `getAttributeNode()`方法： 该方法的作用是以 DOM 节点对象的形式读取当前元素中的指定属性，它接收一个字符串类型的实参，用于指定要读取的属性，并以节点对象的形式将其返回。
  - `setAttributeNode()`方法： 该方法的作用是以 DOM 对象节点的形式设置当前元素中的指定属性，它接收一个属性节点类型的实参，用于指定要设置的属性。如果指定属性不存在，就将该属性节点添加为当前元素的新属性。
  - `removeAttributeNode()`方法： 该方法的作用是以 DOM 对象节点的形式删除当前元素中的指定属性，它接收一个属性节点类型的实参，用于指定要删除的属性。

  关于以上三个方法的具体使用，我们将会留待详细介绍书信节点的时候再加以演示。

- **属性节点**：在 DOM 的定义中，属性节点代表的是 XML 或 HTML 文档中各种页面元素的属性，其`nodeType`的值为 2、`nodeName`的值为节点所代表的标签属性的名称、`nodeValue`的值为节点所代表的标签属性中存取的数据。在 Web 前端开发的语境下，属性节点通常对应着一个 HTML 标签的属性。例如，之前调用的`sayhello.onclick`属性返回的就是代表`<a>`标签元素的`onclick`属性的节点。属性节点对象主要提供了以下三个接口：

  - `name`属性：`nodeName`属性的别名，用于存取节点所代表标签属性的名称。
  - `value`属性： `nodeValue`属性的别名，用于存取节点所代表标签属性中的数据。
  - `specified`属性：该属性是一个布尔类型的值，用来表示该属性是用脚本代码设置的（值为`true`），还是原本就设置在 HTML 文档中的（值为`false`）。

  下面，我们可以用脚本创建一个 HTML 标签为`<div>`的元素节点，并在其中演示一下属性节点的使用：

    ```javascript
    // 用脚本创建新节点
    const newNode = document.createElement('div');
    document.body.appendChild(newNode);
    // 新建属性节点
    let attrNode = document.createAttribute('class');
    attrNode.value = 'box';
    // 为当前元素添加属性
    newNode.setAttributeNode(attrNode);
    // 重新获取属性节点
    attrNode = newNode.getAttributeNode(attrNode.name);
    // 以节点对象的形式修改当前元素的属性
    attrNode.value = 'newbox';
    newNode.setAttributeNode(attrNode);
    // 以节点对象的形式删除当前元素的属性
    newNode.removeAttributeNode(attrNode);
    console.log(attrNode.specified);  // 输出：true
    ```

    严格来说，属性节点通常并不被视为是 HTML 文档所对应 DOM 模型的一部分，它很少被当做独立的节点来使用。

- **文本节点**：在 DOM 的定义中，文本节点代表的是 XML 或 HTML 文档中各种页面元素中显示的文本，其`nodeType`的值为 3、`nodeName`的值为`#text`、`nodeValue`的值为节点所代表的那段文本。通常情况下，文本节点都位于 DOM 树状结构的末端，被认为是叶子节点，不再有子节点了。因此，文本节点上的操作基本是一些字符串处理，为此，DOM 为文本节点定义了以下接口：

  - `data`属性：`nodeValue`属性的别名，用于存取注释节点中的文本。
  - `appendData()`方法： 该方法的作用是将指定的文本加入到当前节点的现有文本的后面，它接收一个字符串类型的实参，用于指定要插入的文本。
  - `deleteData()`方法： 该方法的作用是将指定的文本从当前节点的现有文本中删除，它接收两个实参，第一个实参用于指定要删除文本的始起位置，第二个实参用于指定要删除文本的字符数。
  - `insertData()`方法： 该方法的作用是将指定的文本插入到当前节点的现有文本中，它接收两个实参，第一个实参用于指定要插入文本在现有文本中的始起位置，第二个实参用于指定要插入的文本。
  - `replaceData()`方法： 该方法的作用是用指定文本替换掉当前节点的现有文本中的某段文本，它接收三个实参，第一个实参用于要替换文本在现有文本中的始起位置，第二个实参用于指定现有文本中要被替换文本的字符数，第三个实参用于指定要替换的文本。
  - `splitText()`方法： 该方法的作用是按照指定位置分割当前节点中的现有文本，它接收一个用于指定分割位置的实参。
  - `subSrtingData()`方法： 该方法的作用是从当前节点的现有文本中读取某一段指定的文本，它接收两个实参，第一个实参用于指定要读取文本在现有文本中的始起位置，第二个实参用于指定要读取文本的字符数。

  下面，我们可以用脚本创建一个 HTML 标签为`<div>`的元素节点，并在其中演示一下上述接口的使用：

    ```javascript
    // 用脚本创建新节点
    const newNode = document.createElement('div');
    newNode.id = 'box_4';
    document.body.appendChild(newNode);
    // 创建文本节点
    const textNode = document.createTextNode('这是box_4中的文本。');
    newNode.appendChild(textNode);
    console.log(newNode.lastChild.data); // 输出：这是box_4中的文本。
    // 在现有文本后面添加文本
    textNode.appendData('你好！');
    console.log(newNode.lastChild.data); // 输出：这是box_4中的文本。你好！
    // 在指定位置添加文本
    textNode.insertData(0, 'test: ');
    console.log(newNode.lastChild.data); // 输出：test: 这是box_4中的文本。你好！
    // 读取指定文本
    console.log(textNode.substringData(0, 'test: '.length)); // 输出：test:
    // 替换指定文本
    textNode.replaceData(0,'test: '.length, '测试：');
    console.log(newNode.lastChild.data); 
                                    // 输出：测试：这是box_4中的文本。你好！
    // 删除指定文本
    textNode.deleteData(0, '测试：'.length);
    console.log(newNode.lastChild.data); // 输出：这是box_4中的文本。你好！
    ```

- **注释节点**：在 DOM 的定义中，注释节点代表的是 XML 或 HTML 文档中的注释标签。其`nodeType`的值为 8、`nodeName`的值为`#comment`、`nodeValue`的值为节点所代表注释标签中的文本。注释节点对象的接口与文本节点对象基本相同，它可以执行文本节点除`splitText()`方法之外的所有操作，例如对于下面这个带有注释标签的`<div>`标签：

    ```html
    <div id="box_5"><!--这是一个注释。---></div>
    ```

    注释标签应该是该`<div>`标签的第一个子节点，我们可以通过该子节点的`data`属性来读取其中的注释文本，并用`appentData()`方法添加内容，像这样：

    ```javascript
    const box_5 = document.getElementById('box_5');
    console.log(box_5.firstChild.data);          // 输出：这是一个注释。
    box_5.firstChild.appendData('测试。');
    console.log(box_5.firstChild.data);          // 输出：这是一个注释。测试。
    ```

### 常用的 DOM 接口

凭心而论，就一般性的 Web 前端开发任务来说，DOM 1 中定义的接口就基本上已经可以满足大部分需要了。但程序开发的工作从来就不只是让代码按照我们的设计意图运行起来这么简单，它同时还必须要兼顾程序的运行效率、程序员编程的效率以及程序后期的维护效率等一系列会影响程序开发、部署与使用成本的问题。这就要求我们在程序开发过程中，对于一些具有重大影响的核心任务采用一些经过针对性优化的、并且调用起来也更方便的、让代码可读性更高更易于维护的接口。有意思的是，这些扩展接口最初基本都来自于开发者社区，并且在社区中获得广泛认可之后，用市场需求倒逼浏览器厂商对其提供支持，从而成为了事实上的标准。然后在经过一段时间，才会最终被 W3C 这样的组织纳入正式的标准规范。所以，接下来要介绍的这些 DOM 接口虽然未必都已经被纳入正式标准，但基本已得到了主流 Web 浏览器的支持，读者大可放心使用。下面，让我们按照不同的任务来介绍一下这些 DOM 接口。

#### 文本处理

在 DOM 标准定义中，HTML 文档中所有元素中的文本都是一个独立的 DOM 节点对象，并且通常以最终子节点的形式存在于 DOM 树结构中。这意味着，我们每当要添加、删除或修改某个指定元素中的文本，就必须按照创建节点或获取节点的步骤走一遍，例如我们要这样为指定元素添加仅有几个字的文本：

```JavaScript
const otherNode = document.getElementById('box_4');
const textNode = document.createTextNode('这是box_4中的文本。');
textNode.insertData(0, 'test: ');
textNode.replaceData(0,'test: '.length, '测试：');
otherNode.appendChild(textNode);
```

先姑且不论调用那么多方法给程序运行效率带来的影响，就说为了添加这样区区几个字的文本，要程序员编写那么一大段代码，程序的开发效率也令人担忧。况且这样写代码，显然也不够简洁直观，代码写得不仔细就极容易遗漏某个细节，阅读代码不仔细就很难在成百上千行代码中分辨出这段代码在干什么，并在维护时准确定位它们，所以这段代码的可维护性也不怎么样。

更糟糕的是，一些浏览器会将 HTML 标签中所有的换行符视为一个独立的文本节点，也就是说，对于下面两个拥有相同文本的`div`元素：

```HTML
<div id="box_6">一段文本</div>
<div id="box_7">
    一段文本
</div>
```

在某些浏览器中，它们子节点的数量是不一样的，我们可以来验证一下：

```JavaScript
const box_6 = document.getElementById('box_6');
console.log(box_6.childNodes.length);   // 在所有浏览器中都输出 1 。
const box_7 = document.getElementById('box_7');
console.log(box_7.childNodes.length);  // 由于标签中存在换行符，某些浏览器会输出 3 。
```

这意味着我们在一些浏览器中无法用`box_7`节点的`firstChild`属性访问到其下面的文本。当然，我们也可以先调用`normalize()`方法再使用该属性读取文本，像这样：

```JavaScript
const box_7 = document.getElementById('box_7');
box_7.normalize();
console.log(box_7.firstChild);
```

但这样做依然不够直观，而事实上，开发者们更多时候会选择用`innerText`和`outerText`这两个属性来读写节点中文本信息。这两个属性最初是 IE 浏览器特有的接口，后来得到了开发者们的广泛使用，虽然至今都尚未被纳入正式标准，但它们在大多数浏览器中都得到了支持。下面，我们来具体介绍一下这两个属性的用法：

- **`innerText`属性**：在使用该属性读取节点中的文本时，它会将该节点下所有的文本拼接成一整个字符串并返回，例如对于下面这个`div`元素：

    ```HTML
    <div id="box_8">
        <p>这是一段文本。</p>
        <p>这是另外一段文本。</p>
    </div>
    ```

    我们可以用如下代码来看看其`innerText`属性返回的内容：

    ```JavaScript
    const box_8 = document.getElementById('box_8');
    console.log(box_8.innerText);
    // 以上脚本输出：
    //   这是一段文本。
    //   这是另外一段文本。
    ```

    而当我们使用该属性为指定节点设置文本时，必须要记得它会用单一的文本节点覆盖掉该节点下的所有子节点。例如，如果我们对上面的`box_8`对象执行下面的代码：

    ```JavaScript
    const box_8 = document.getElementById('box_8');
    box_8.innerText = '这是一段测试文本';
    ```

    之前那个`id`值等于`box_8`的`div`元素实际上就变成了这样：

    ```HTML
    <div id="box_8">这是一段测试文本</div>
    ```

- **`outerText`属性**：该属性在执行读取操作时行为与`innerText`属性完全一致，但在写入操作时，它覆盖掉的就不是指定节点下面的子节点了，它会连同被指定的节点本身及其子节点一同覆盖掉。例如，对于下面这个`div`元素：

    ```HTML
    <div id="box_8">
        <div id="box_9">这是一段文本</div>
    </div>
    ```

    如果我们对上面的`box_9`对象执行下面的代码：

    ```JavaScript
    const box_9 = document.getElementById('box_9');
    box_9.outerText = '这是一段测试文本';
    ```

    之前那个`id`值等于`box_8`的`div`元素实际上就变成了这样：

    ```HTML
    <div id="box_8">这是一段测试文本</div>
    ```

除此之外，需要注意的是，`innerText`和`outerText`这两个属性会将接收到的 HTML 代码中的特殊字符进行转义，换而言之，它们会将 HTML 代码原样呈现。而不会交由浏览器来解析。如果我们想设置浏览器可解析的 HTML 代码，应该改用`innerHTML`和`outerHTML`这两个属性，它们在使用方式上与`innerText`和`outerText`是相同的，只不过作用从设置文本变成了设置 DOM 子树结构。

#### 元素遍历

部分浏览器会因换行符而生成文本节点的问题也会给我们的元素遍历操作带来麻烦，为了避免在遍历 DOM 树结构上的元素节点时读取到没有意义的文本节点，我们通常需要在遍历循环中加上节点类型的判断，就像这样：

```JavaScript
// 老方法：
function forEachElement(element) {
    let nodePtr = element.firstChild;
    while(nodePtr !== element.lastChild) {
        if(nodePtr.nodeType === 1) { // 检查是否为元素节点
            console.log(nodePtr.tagName);
            forEachElement(nodePtr);   // 递归调用
        }
        nodePtr = nodePtr.nextSibling;
    }
}
forEachElement(document.body);
```

但这样做显然不够简洁明了，尤其在只能用数字来表示节点类型的情况下，采用这种方法是不利于代码的可读性和开发者的编程效率的。为了解决这个问题，DOM 为我们提供了以下这些专用于遍历元素节点的接口：

- **`childElementCount`属性**：该属性用于返回当前节点的子节点中元素节点的个数，即不包含文本节点和注释节点。
- **`firstElementChild`属性**：该属性用于返回当前节点的子节点中的第一个元素节点。
- **`lastElementChild`属性**：该属性用于返回当前节点的子节点中的最后一个元素节点。
- **`previousElementSibling`属性**：该属性返回当前节点的前一个同辈元素节点。
- **`nextElementSibling`属性**：该属性返回当前节点的后一个同辈元素节点。

有了这些接口，我们就可以像下面这样遍历 DOM 树结构中的元素了：

```JavaScript
// 新方法：
function forEachElement_new(element){
    let elemPtr = element.firstElementChild;
    while(elemPtr != element.lastElementChild) {
        console.log(elemPtr.tagName);
        forEachElement_new(elemPtr);
        elemPtr = elemPtr.nextElementSibling;
    }
}
forEachElement_new(document.body);
```

#### 元素选择

在实际开发过程中，比起元素节点的遍历，我们更常需要执行的操作是要从一堆层层嵌套的 DOM 元素中快速获取到要操作的元素对象。而在相当长的一段时间里，我们只能通过以下四个接口来执行这类操作：

- `getElementById()`方法
- `getElementsByName()`方法
- `getElementsByTagName()`方法
- `getElementsByClassName()`方法

但这些接口有两个明显的问题：首先，它们的名称各不相同而且都相当长，在没有自动补齐的编程环境中是极易出错的，尤其是除了第一个接口外，其他三个接口的`Element`单词后面都有一个`s`。其次，它们的行为也并不一致，第一个接口返回的是单一元素，即使目标 HTML 文档中有多个匹配元素，它也只返回第一个匹配的元素。而其他三个接口返回的都是一个元素数组[^1]，即使目标 HTML 文档中只有一个匹配元素，它们返回的也是一个包含单元素的数组，这意味着我们还是要用读取数据的方式来获取元素对象。在过去，为了避免上述问题，开发者们只能选择使用 JQuery 这样的第三方库提供的接口。而如今为了响应市场需求，W3C 组织也参考了 CSS 选择器的用法，为我们重新提供了以下两个选取页面元素的接口：

- **`querySelector()`方法**：该方法的作用是返回目标对象中第一个符合条件的元素对象，它接收一个字符串类型的实参，该实参是一个 CSS 选择器，即我们用`#id`、`.className`、`tagName`等 CSS 选择器模式来指定要匹配的元素。例如下面这个调用与`document.getElementById('box_1')`是等价的：

    ```JavaScript
    const box_1 = document.querySelector('#box_1');
    ```

    但除此之外，我们还可以这样使用该接口：

    ```JavaScript
    // 返回 document 对象中第一个 class 值等于 box 的元素：
    const boxObj_1 = document.querySelector('.box');
    // 返回 document 对象中第一个标签为 div 的元素：
    const div_1 = document.querySelector('div');
    // 返回 document 对象中第一个 class 值等于 box 的 div 元素：
    const divBox_1 = document.querySelector('div.box');
    ```

- **`querySelectorAll()`方法**：该方法的作用是返回目标对象中所有符合条件的元素对象[^2]，它接收一个字符串类型的实参，该实参的用法与`querySelector()`方法相同，也就是说，我们可以这样使用该接口：

    ```JavaScript
    // 返回 document 对象中所有 ID 值等于 box_1 的元素：
    const boxes = document.querySelectorAll('#box_1');
    // 返回 document 对象中所有 class 值等于 box 的元素：
    // 等价于调用 document.getElementsByClassName('box')
    const boxObjs = document.querySelectorAll('.box');
    // 返回 document 对象中所有标签为 div 的元素：
    // 等价于调用 document.getElementsByTagName('div')
    const divAll = document.querySelectorAll('div');
    ```

需要注意的是，这两个元素选择器接口不仅可以用`document`来调用，我们也可以在具体的 DOM 元素节点上调用它们，在这种情况下元素选择去将在调用它的这个节点对象的子节点中选取匹配元素。所以，如你所见，这两个新的元素选择器接口不仅可以实现之前四个老选择器接口的全部功能，还能指定更复杂的匹配条件。例如，如果我们想获取某个指定`class`值的`div`元素，就可以这样做：

```JavaScript
// 返回 document 对象中所有 class 值等于 box 的 div 元素：
const divBoxes = document.querySelectorAll('div.box');
```

并且，新的元素选择器在使用方式上也更为灵活，无论哪一种匹配条件，都可以选择是要获取第一个匹配元素，还是所有匹配元素。这显然有助于提高我们的开发效率，并改善代码本身的可读性。在之后的代码示例中，我们也会尽可能地改用这两个元素选择器来执行获取页面元素的任务。

#### 创建表格

在设计 Web 应用程序界面的过程中，表格一直是我们使用得非常频繁的 HTML 页面元素之一。但我们会发现，由于表格元素涉及到一系列子元素，如果用一般创建元素节点的那些接口来创建表格，将是一个非常繁琐的过程。例如，我们现在用一般创建元素节点的老方法来创建一个 2x2 的简单表格：

```JavaScript
// 老方法：
const table = document.createElement('table');
// 表体：
const tbody = document.createElement('tbody');
// 第一行：
const row_1 = document.createElement('tr');
const cell_1 = document.createElement('td');
cell_1.innerText = '张三';
row_1.appendChild(cell_1);
const cell_2 = document.createElement('td');
cell_2.innerText = '1000';
row_1.appendChild(cell_2);
tbody.appendChild(row_1);
// 第二行：
const row_2 = document.createElement('tr');
const cell_3 = document.createElement('td');
cell_3.innerText = '李四';
row_2.appendChild(cell_3);
const cell_4 = document.createElement('td');
cell_4.innerText = '1001';
row_2.appendChild(cell_4);
tbody.appendChild(row_2);
table.appendChild(tbody);
document.body.appendChild(table);
```

显然，这种创建表格的方法所需要的代码量绝对不会让人觉得这是在创建一个“简单的”表格，而我们在实际开发中要创建的表格通常都要比这个例子复杂得多，读者可以自行想象届时要付出开发成本。而且在这种情况下，代码的可读性通常都不会好到哪儿去，因此维护成本自然也低不了。为了解决这一问题，DOM 为我们提供了一系列专用于处理表格的接口，首先是由`<table>`元素对象调用的属性和方法：

- **`caption`属性**：该属性对应的是`<table>`元素下面的`<caption>`元素，我们可以通过该属性来设置调用该方法的`<table>`元素对象的标题。
- **`tHead`属性**：该属性对应的是`<table>`元素下面的`<thead>`元素，我们可以通过该属性来设置调用该方法的`<table>`元素对象的页眉。
- **`tFoot`属性**：该属性对应的是`<table>`元素下面的`<tfoot>`元素，我们可以通过该属性来设置调用该方法的`<table>`元素对象的页脚。
- **`rows`属性**：该属性是调用该方法的`<table>`元素对象中用于存储`<tr>`元素的类数组对象，我们可以通过该属性来管理其中的`<tr>`元素。
- **`createCaption()`方法**：该方法用于创建一个`<caption>`元素，并在返回该元素对象引用的同时，将其加入到调用该方法的`<table>`元素对象中。
- **`createTHead()`方法**：该方法用于创建一个`<thead>`元素，并在返回该元素对象引用的同时，将其加入到调用该方法的`<table>`元素对象中。
- **`createTFoot()`方法**：该方法用于创建一个`<tfoot>`元素，并在返回该元素对象引用的同时，将其加入到调用该方法的`<table>`元素对象中。
- **`deleteCaption()`方法**：该方法用于删除调用该方法的`<table>`元素对象中的`<caption>`元素。
- **`deleteTHead()`方法**：该方法用于删除调用该方法的`<table>`元素对象中的`<thead>`元素。
- **`deleteTFoot()`方法**：该方法用于删除调用该方法的`<table>`元素对象中的`<tfoot>`元素。
- **`deleteRow()`方法**：该方法用于删除调用该方法的`<table>`元素对象中的`<tr>`元素，它接收一个数字类型的实参，用于指定被删除元素在`rows`属性中的索引值。
- **`insertRow()`方法**：该方法用于在调用该方法的`<table>`元素对象中插入一个`<tr>`元素，它接收一个数字类型的实参，用于指定被插入元素在`rows`属性中的索引值。
  
再来是由`<tbody>`元素对象调用的属性和方法：

- **`rows`属性**：该属性是调用该方法的`<tbody>`元素对象中用于存储`<tr>`元素的类数组对象，我们可以通过该属性来管理其中的`<tr>`元素。
- **`deleteRow()`方法**：该方法用于删除调用该方法的`<tbody>`元素对象中的`<tr>`元素，它接收一个数字类型的实参，用于指定被删除元素在`rows`属性中的索引值。
- **`insertRow()`方法**：该方法用于在调用该方法的`<tbody>`元素对象中插入一个`<tr>`元素，它接收一个数字类型的实参，用于指定被插入元素在`rows`属性中的索引值。

最后是`<tr>`元素对象调用的属性和方法：

- **`cells`属性**：该属性是调用该方法的`<tr>`元素对象中用于存储`<td>`元素的类数组对象，我们可以通过该属性来管理其中的`<td>`元素。
- **`deleteCell()`方法**：该方法用于删除调用该方法的`<tr>`元素对象中的`<td>`元素，它接收一个数字类型的实参，用于指定被删除元素在`cells`属性中的索引值。
- **`insertCell()`方法**：该方法用于在调用该方法的`<tr>`元素对象中插入一个`<td>`元素，它接收一个数字类型的实参，用于指定被插入元素在`cells`属性中的索引值。

下面，我们用这些专用接口来创建一个 2x2 的简单表格，读者可以自行对比一下这个创建表格的新方法与之前老方法的区别：

```JavaScript
// 新方法：
const newTable = document.createElement('table');
// 表体：
const newTboby = document.createElement('tbody');
// 第一行
newTboby.insertRow(0);
newTboby.rows[0].insertCell(0);
newTboby.rows[0].cells[0].innerText = '王五';
newTboby.rows[0].insertCell(1);
newTboby.rows[0].cells[1].innerText = '1002';
// 第二行
newTboby.insertRow(1);
newTboby.rows[1].insertCell(0);
newTboby.rows[1].cells[0].innerText = '赵六';
newTboby.rows[1].insertCell(1);
newTboby.rows[1].cells[1].innerText = '1003';
newTable.appendChild(newTboby);
document.body.appendChild(newTable);
```

很显然，现在我们创建表格的行元素和单元格元素时需要写的代码量也相对少了许多，而且代码本身也更简洁明了，简单易懂了，这对降低开发成本和维护成本都有好处。

#### 样式变换

让 Web 页面中的各元素能随程序运行时的实际情况来变换外观（譬如背景色、字体及其大小等），是其作为应用程序用户界面的基本功能之一。实现这一功能需要我们在 JavaScript 脚本中为 HTML 页面元素赋予 CSS 样式值，而这些元素中与 CSS 相关的主要是`style`和`class`这两个属性，所以我们在 JavaScript 中执行样式变换任务将围绕着它们来展开。为此，DOM 标准也提供了专用的扩展接口，下面我们就来分别介绍一下这些接口。

**`style`属性**

在编写 HTML 文档时，我们有时会将一些简单的 CSS 样式直接写在相关元素标签的`style`属性中。例如，如果我们只想为一个`div`元素设置一个背景色，其实可以这样做：

```HTML
<div id="box_10" style="background-color:red">
  这是一个用于测试样式变换的 div 元素。
</div>
```

这种做法是 CSS 样式设置中优先级最高的方式，因为在 CSS 样式的计算规则中，`style`属性是最后被读取的样式，这意味着我们在该属性中设置的样式会覆盖掉用其他方式设置的样式。但是，这种方式不仅不利于设置较为复杂的样式，它也违反了将呈现样式与文档结构分离，以降低耦合度的设计原则。但如果我们是在 JavaScript 脚本中设置元素的`style`属性，就不存在这样的问题了。为此，DOM 2 引入了相应的样式模块，所以对于 HTML 文档中每一个可设置`style`属性的标签，其对应的 DOM 对象中也有一个与之相应的`style`属性。

在 DOM 2 的定义中，元素节点对象的`style`属性本身也是一个对象，它也以属性的形式存储了当前元素所有可设置的 CSS 条目。当然了，这些属性在命名上与其实际对应的 CSS 条目存在着些许的不同，譬如对于像`font-size`、`background-color`这样带连接符的 CSS 条目，它在`style`属性对象中就会采用`fontSize`、`backgroundColor`这样的驼峰命名法。再譬如对于`float`这样的，在 JavaScript 中属于保留字的 CSS 条目名称，在`style`属性对象中就改用`cssFloat`这样的命名。例如，对于上面这个`div`元素，我们可以这样读取并修改它的`style`属性：

```JavaScript
const box_10 = document.querySelector('#box_10');
console.log(box_10.style.backgroundColor);
box_10.style.backgroundColor = 'blue';
console.log(box_10.style.backgroundColor);
```

当然，我们也可以继续接着为该`div`元素设置高度、宽度、字体大小等样式，例如像这样：

```JavaScript
box_10.style.width = '50%';
box_10.style.height = '250px';
box_10.style.fontSize = '18px';
```

除了这些与 CSS 样式条目一一对应的属性，元素节点的`style`属性对象还为我们提供以下接口：

- **`cssText`属性**：该属性的主要作用是以字符串的形式返回当前元素节点的`style`属性，例如，如果想查看我们之前为`id`值为`box_10`的`div`元素设置的所有 CSS 样式，就可以接着上面的代码这样写：

    ```JavaScript
    console.log(box_10.style.cssText);
    // 输出：background-color: blue; width: 50%; height: 250px; font-size: 18px;
    ```

    当然，该属性也可以用于以字符串的形式一次性地设置多个 CSS 样式，只不过这样的设置需要小心，因为无论我们赋予它什么值，之前在`style`属性中设置的所有样式都会被抹除。下面，我们可以来验证一下，请接着上面的代码这样写：

    ```JavaScript
    box_10.style.cssText = 'font-size: 20px; background-color: red';
    console.log(box_10.style.cssText);
    // 输出：font-size: 20px; background-color: red;
    ```

- **`length`属性**：该属性的作用是返回当前元素节点的`style`属性中设置的 CSS 条目数量。例如，我们可以这样查看`box_10`元素的`style`属性中设置了多少 CSS 样式：

    ```JavaScript
    const box_10 = document.querySelector('#box_10');
    console.log(box_10.style.backgroundColor);
    box_10.style.backgroundColor = 'blue';
    box_10.style.width = '50%';
    box_10.style.height = '250px';
    box_10.style.fontSize = '14px';
    console.log(box_10.style.length); // 输出 4
    ```

- **`item()`方法**：该方法的作用是按指定的索引值返回当前元素节点的`style`属性中 CSS 样式的条目名称，它接收一个数字类型的实参，用于指定相关 CSS 条目的索引值。因此，该方法通常需搭配`length`属性来使用。例如，如果想查看`style`属性中设置了哪些 CSS 条目，我们可以接着上面的代码这样写：

    ```JavaScript
    for(let i = 0; i < box_10.style.length; ++i) {
        console.log(box_10.style.item(i));
    }
    ```

- **`getPropertyValue()`方法**：该方法的作用是按照指定的 CSS 条目名称返回在当前元素的`style`属性中设置的样式值，它接收一个字符串类型的实参，用于指定相关的 CSS 条目名称。例如，如果想要完整地遍历当前元素在`style`属性中设置的 CSS 样式，我们可以将上面的循环修改如下：

    ```JavaScript
    for(let i = 0; i < box_10.style.length; ++i) {
        const cssItem = box_10.style.item(i);
        const cssValue = box_10.style.getPropertyValue(cssItem);
        console.log((cssItem + ' : ' + cssValue);
    }
    ```

- **`setProperty()`方法**：该方法的作用是在当前元素的`style`属性中设置或添加指定的 CSS 样式条目，它接收两个字符串类型的实参，第一个实参用于指定要设置的 CSS 条目名称，如果该条目目前不存在于当前元素的`style`属性中，就将它添加进去。第二个实参用于指定要设置的样式值。当然，这个方法并不常用，我们更倾向于用之前那种属性的方式来设置样式，也就是说：

    ```JavaScript
    box_10.style.setProperty('width','50%');
    // 等价于：box_10.style.width = '50%';
    ```

- **`removeProperty()`方法**：该方法的作用是在当前元素的`style`属性中移除指定 CSS 条目中的样式值，它接收一个字符串类型的实参，用于指定要移除样式值的 CSS 条目名称。需要注意的是，该方法只能用于移除我们在`style`属性中设置的样式值，用其他方式设置的样式，并由`style`属性继承为默认值的样式是不受影响的。也就是说，这里所谓的“移除”实际上的效果是恢复指定 CSS 条目在`style`属性中默认值，所以该方法并不常用。

**`classList`属性**

在编写 HTML 文档时，对于那些需要多个 CSS 条目联动的更为复杂的样式变换操作，我们通常会选择先在外链的 CSS 文件或者`<style>`标签中定义相应的 CSS 类，然后通过目标元素的`class`属性来实现。正如上一章中所说，HTML 页面元素的`class`属性对应的是 DOM 中元素对象的`className`属性，这意味着，我们也可以在 JavaScript 中执行同样的样式变换操作。

但`className`属性在执行样式变换任务时并不是一个太好用的接口。因为在实际的 Web 开发中，针对页面元素的样式变换通常是几个不同的 CSS 类的搭配组合。例如，在某个 Web 页面中，我们通常会先为所有的`<div>`元素设置一些宽度、高度、边框等基本样式，并将这些样式定义在名为`box`的 CSS 类中。然后分别为显示错误信息的`<div>`元素定义一个名为`bug`的 CSS 类、为显示提示信息的`<div>`元素定义一个名为`tip`的 CSS 类，以便它们呈现出不同的字体和背景色。这样一来，当一个`<div>`元素显示提示信息时，它的`class`属性值应该是“box tip”，当它要显示错误信息时，`class`值就要被修改成“box bug”。这显然是一个用空格分隔的 CSS 类名列表，而按照 DOM 标准的定义，元素节点的`className`属性只是一个字符串类型的对象，这意味着，我们只能使用字符串分隔、查找以及替换的方式来实现样式变换任务，像这样：

```JavaScript
const box_11 = document.createElement('div');
box_11.id = 'box_11';
box_11.className = 'box tip';
document.body.appendChild(box_11);
setTimeout(function() {
    let pos = -1;
    const CSSClasses = box_11.className.split(/\s+/);
    for(let i = 0; i < CSSClasses.length; ++i) {
        if(CSSClasses[i] == 'tip') {
            pos = i;
            break;
        }
    }
    CSSClasses[pos] = 'bug';
    box_11.className = CSSClasses.join(' ');
}, 3000);
```

在上面的代码中。我们首先创建了一个`id`值为`box_11`的`<div>`元素节点，它初始状态下的`className`属性值为“box tip”，然后在三秒之后将该值变换成了“box bug”。诚如各位所见，上述代码的整个编写过程不仅太过繁琐，而且极易出错，这很显然是不利于降低开发成本和维护成本的。为了解决这个问题，DOM 为元素节点另外定义了一组增加、删除及修改 CSS 类名的接口，即`classList`属性，它会将根据我们在元素节点的`className`中设置的 CSS 类名自动构建出一个相应的类数组对象。下面，我们就来介绍一下该对象提供的接口：

- **`add()`方法**：该方法的作用是将指定的 CSS 类名添加到当前元素节点的`classList`属性中，它接收一个字符串类型的实参，用于指定要添加的 CSS 类名。例如，如果我们需要为上面的`box_11`元素节点再添加一个名为`message`的 CSS 类，就可以这样写：

    ```JavaScript
    box_11.classList.add('message');
    ```

- **`remove()`方法**：该方法的作用是将指定的 CSS 类名从当前元素节点的`classList`属性中移除，它接收一个字符串类型的实参，用于指定要移除的 CSS 类名。例如，如果我们需要移除上面为`box_11`元素节点添加的 CSS 类名，就可以这样写：

    ```JavaScript
    box_11.classList.remove('message');
    ```

- **`contains()`方法**：该方法的作用是判断指定的 CSS 类名是否存在于当前元素节点的`classList`属性中，如果存在返回 true，否则就返回 false、它接收一个字符串类型的实参，用于指定要查看的 CSS 类名。例如，如果我们想要在移除指定的 CSS 类名，先判断一下它是否存在于`box_11`元素节点的`classList`属性中，就可以这样写：

    ```JavaScript
    if(box_11.classList.contains('message')) {
        box_11.classList.remove('message');
    }
    ```

- **`toggle()`方法**：该方法的作用是在指定 CSS 类名不存在于当前节点的`classList`属性中时添加它。反之，如果指定的 CSS 类名已经存在于其中了，则删除它。例如，如果我们想为`box_11`元素节点反复添加或删除一个 CSS 类，可以这样写：

    ```JavaScript
    for(let i = 0; i < 10; ++i){
        setTimeout(function(){
            box_11.classList.toggle('message');
        }, i*3000);
    }
    ```

下面，我们可以再创建一个`id`值为`box_12`的`<div>`元素节点，并用`classList`属性提供的接口在节点上实现与`box_11`元素节点相同的显示效果，以便读者可以对比两者的区别：

```JavaScript
const box_12 = document.createElement('div');
box_12.id = 'box_12';
box_12.classList.add('box');
box_12.classList.add('tip');
document.body.appendChild(box_12);
setTimeout(function(){
    if(box_12.classList.contains('tip')) {
        box_12.classList.remove('tip');
    }
    box_12.classList.add('bug');
}, 3000);
```

很显然，与之前在`box_11`元素节点上的实现相比，上面的代码显得更为简单明了、清晰易懂，更有助于降低开发和维护的成本。

### 浏览器对象模型

到目前为止，我们所做的前端编程任务面向的都是 DOM 所对应的 HTML 文档。但在实际前端开发中，有些任务是要面向 Web 浏览器来执行的，这时候就需要用到另一套专门面向浏览器的应用程序接口：**浏览器对象模型（即 Browser Object Model，以下简称 BOM）**了。与 DOM 不同的是，BOM 没有复杂的数据结构，它本质上只是一个由多个不同功能的对象组成的聚合体，其中的每一个对象都独立负责处理一种专门的浏览器任务，事实上，我们之前一直在使用的`document`对象也是其中之一。当然了，由于在相当长的一段历史时期里，BOM 并没有被制定出一致的标准，市场上各种浏览器提供商在 BOM 中聚合的对象都不尽相同，某对象在某一浏览器中被支持，在另一浏览器却不被支持的情况比比皆是。幸好，在 HTML 5 发布之后，W3C 组织为了规范化 JavaScript 的相关操作，根据目前各大主流浏览器之间共同实现的那些对象，对 BOM 的最基本组成进行了一定程度的标准化。下面，我们就来介绍一下这部分被标准化了的内容。

首先，BOM 中所有对象组成的聚合体被命名为`window`对象。该对象在 BOM 中处于核心地位，它实际上是浏览器本身在 JavaScript 脚本程序中的一个引用句柄。也就是说，`window`对象是我们在 JavaScript 代码中操作浏览器窗口的一个接口，我们可以用它来执行获取窗口大小与位置、弹出系统对话框等直接面向浏览器窗口的操作。当然了，如今大部分浏览器都带有标签页的功能，在这些浏览器中，每个标签页都拥有独立的`window`对象，同一个窗口的标签页之间并不共享一个`window`对象，所以该对象的一部分接口所要面向的目标已经由浏览器窗口转向了浏览器的标签页，这点我们在使用`window`对象接口时务必要有一个清晰的概念。另外，`window`对象除了是我们操作浏览器的接口对象之外，同时还是 JavaScript 在前端编程环境中的全局对象，它所在的作用域就是前端编程环境中的全局作用域，因此它的属性和方法都可以被当做全局变量和方法来调用。也就是说，在前端编程环境中，`document`和`window.document`这两个标识符引用的是同一个对象，因而通常情况下是不需要加`window.`这个前缀的，对此，我们可以来验证一下：

```JavaScript
console.log(document === window.document);  // 输出 true
```

当然了，由于`window`对象中提供的对象和方法非常多，且其中许多接口在各浏览器中的表现都不太一致，而笔者也并不打算将本书写成一部面面俱到的参考手册，所以接下来，我们还是会按照前端开发中常见的编程任务来介绍 BOM 中一些常用接口的使用方式。

#### 识别显示环境

在 Web 应用程序的开发中，有时候需要根据脚本运行时所处的显示环境来编写相应的代码。例如，面向移动端设备的代码通常会与 PC 端有所不同，这种情况下就需要在 JavaScript 脚本运行时获取浏览器窗口或当前设备屏幕的大小，以判断脚本当前是否运行在移动端设备上。虽然很多浏览器都在`window`对象中提供了类似像`innerHeight`（显示区高度）、`innerWidth`（显示区宽度）、`outerHeight`（窗口高度）、`outerWidth`（窗口宽度）、`screenX`（窗口位置的横向坐标）、`screenY`（窗口位置的纵向坐标）这样的全局属性以便我们获取浏览器在运行时的大小及其位置信息（这里所谓的“显示区”指的是浏览器窗口中真正用于显示网页内容的区域，不包含标题栏、菜单栏、工具栏、标签栏以及状态栏所占的区域，而所谓的“窗口位置”则指的是窗口左上角那个点在整个显示屏中的位置坐标），例如：

```JavaScript
console.log('浏览器窗口大小：', outerHeight+','+outerWidth);
console.log('浏览器窗口位置：', screenX+','+ screenY);
console.log('浏览器显示区大小：', innerHeight+','+innerWidth);
```

但以上这些属性在各浏览器中的表现不太一致，而且有些浏览器会用`screenLeft`和`screenTop`这两个属性来实现与`screenX`、`screenY`相同的功能，所以笔者还是推荐使用`window`对象的专职成员，`screen`对象来获取设备方面的信息，下面我们就来介绍一下该对象提供的常用接口（如果读者希望希望了解该对象的全部接口，还请查阅相关的参考手册）：

- **`height`属性**：该属性表示的是浏览器所在设备屏幕的高度。
- **`width`属性**：该属性表示的是浏览器所在设备屏幕的宽度。
- **`availHeight`属性**：该属性表示的是当前程序可使用的屏幕区域的高度。
- **`availWidth`属性**：该属性表示的是当前程序可使用的屏幕区域的宽度。
- **`availLeft`属性**：该属性表示的是当前程序可使用的屏幕区域的横向坐标。
- **`availTop`属性**：该属性表示的是当前程序可使用的屏幕区域的纵向坐标。
- **`colorDepth`属性**：该属性表示的是当前程序可以的系统颜色值的位数，目前大多数系统是 24 位。

这里需要特别说明的是，`screen`对象的这些属性都是只读的，它们不可在脚本运行过程中被修改，这也正是笔者推荐使用该对象的另一个原因。毕竟，在实际 Web 应用程序开发中，我们并不鼓励在运行时调整浏览器的大小或位置。想必读者应该也有所耳闻，JavaScript 脚本在早期某一段时间基本上是恶作剧的代名词，其中的原因之一，就是因为那时有太多脚本通过在运行时调整浏览器窗口的位置和大小搞出了许多华而不实的效果。这些脚本轻则只是一个恶趣味的炫技或无聊的玩笑，重则甚至会导致用户的操作系统崩溃死机或数据丢失（尤其在 Windows 98 的年代），无论哪一种情况都给用户带来不少困扰，而使用`screen`对象的只读属性就可以从根本是杜绝这种可能性。下面，我们就来演示一下如何用`screen`对象来获取 JavaScript 脚本所运行的显示环境：

```JavaScript
console.log('当前设备屏幕大小：', screen.height+','+screen.width);
console.log('程序可用区域大小：', screen.availHeight+','+screen.availWidth);
console.log('程序可用区域位置：', screen.availLeft+','+screen.availTop);
console.log('系统颜色的位数：', screen.colorDepth);
```

这样一来，我们就可以对当前脚本是否运行在怎样的显示环境中做一个基本的判断了。例如在通常情况下。如果得知设备屏幕的高度小于 900 且宽度小于 420，脚本就基本可以判断自己是运行在手机这样的设备上，因此，我们可以在代码中这样写：

```JavaScript
if(screen.height<900 && screen.width<420) {
    console.log('你的脚本运行在屏幕大小与手机相似的设备上。');
} else {
    console.log('你的脚本运行在手机以外的大屏设备上。');
}
```

下面，我们可以用 Google Chrome 浏览器来模拟一下手机屏幕，并查看结果：

![识别显示环境](./img/2.png)

当然了，如果我们的目标只是根据 Web 应用程序在运行时的显示环境来调整字体、图片等元素的大小和排列效果，通常只需要使用 CSS 的响应式布局功能就可以了。除非涉及更为复杂的程序业务逻辑，我们没有必要使用 JavaScript 来处理这方面的事务。

#### 定位与导航

在 JavaScript 中，网页的定位与导航，包括浏览器访问记录的回溯等功能都是靠`window`对象中`location`和`history`这两个专职成员来实现的。其中，`location`对象负责的是存储并解析浏览器当前载入页面的 URL 信息，而`history`对象负责的则是浏览器的访问记录。下面，我们先来介绍一下`location`对象提供的常用接口：

- **`href`属性**：该属性返回的是浏览器当前载入页面的完整 URL，例如`https://www.google.com`。
- **`protocol`属性**：该属性返回的是浏览器当前载入页面 URL中的协议部分，例如`https`或`ftp`。
- **`host`属性**：该属性返回的是浏览器当前载入页面 URL中的主机名及端口号，例如`www.google.com:80`。
- **`hostname`属性**：该属性返回的是浏览器当前载入页面 URL中的主机名，例如`www.google.com`。
- **`port`属性**：该属性返回的是浏览器当前载入页面 URL中的主机端口号，例如`8080`或`7575`。
- **`hash`属性**：该属性返回的是浏览器当前载入页面 URL中`#`标识的内容（即当前页面中的锚链接），如果不存在相关标识，就返回空字符串。例如：如果当前页面的 URL 是`http://myweb.com/test.htm#location`，该属性返回的就是`#location`。
- **`search`属性**：该属性返回的是浏览器当前载入页面 URL中`?`标识的内容（也叫查询字符串），如果不存在相关标识，就返回空字符串。例如：如果当前页面的 URL 是`http://myweb.com/test.htm?script=js`，该属性返回的就是`?script=js`。
- **`assign()`方法**：该方法的作用是在当前浏览器窗口（或标签页）中打开指定的页面，它只接收一个字符串类型的实参，用于指定要载入页面的 URL。
- **`replace()`方法**：该方法的作用和使用方式与`assign()`方法基本相同，唯一的区别是它不会在浏览器的访问历史中留下记录。

下面，让我们来演示一下对指定的具体解析，当然了，在开始具体解析操作之前，让我们先用`assign()`方法打开`http://127.0.0.1:5500/src/code/03_web/03-test.htm?script=js#location`这个 URL：

```JavaScript
const testUrl = 'http://127.0.0.1:5500/src/code/03_web/03-test.htm?script=js#location';
location.assign(testUrl);
console.log('当前页面的完整 URL：', location.href);
console.log('当前页面使用的网络协议：', location.protocol);
console.log('当前页面所在的主机信息：', location.host);
console.log('当前页面所在的主机名称：', location.hostname);
console.log('当前页面所在的主机端口：', location.port);
console.log('当前页面 URL的 hash 部分：', location.hash);
console.log('当前页面 URL 的 search 部分：', location.search);
```

下面让我们在 Google Chrome 浏览器中执行该脚本，并打开 JavaScript 控制台查看结果：

![URL的解析](img/3.png)

当然了，读者在自己的学习环境中测试以上代码时，要根据自己的 Web 服务器设置来调整`testUrl`的具体内容。只不过，为了能让测试覆盖到`location`对象的每一个常用属性，我们建议要在 URL 中加上`search`和`hash`部分。除此之外，与`screen`对象不同的是，`location`对象的这些属性是可在运行时被修改的，就该之后就会改变浏览器当前载入的内容。例如，如果我们想修改当前页面 URL 中的 search 部分，就可以这样做：

```JavaScript
location.search = '?script=vbs';
```

这样一来，当前页面的 URL 就自动变成了`http://127.0.0.1:5500/src/code/03_web/03-test.htm?script=vbs`，并重新让浏览器重新载入。下面，让我们继续来介绍用于回溯浏览器访问历史的`history`对象，该对象提供的常用接口如下：

- **`length`属性**：该属性返回的是浏览器访问历史中记录的数量。
- **`back()`方法**：该方法的作用就相当于执行一次浏览器上的“后退”功能。
- **`forward()`方法**：该方法的作用就相当于执行一次浏览器上的“前进”功能。
- **`go()`方法**：该方法可以直接指定浏览器执行“后退”或“前进”功能的次数。
  
  通常情况下，该方法只需接收一个数字类型的实参，负数代表执行“后退”功能的次数，正数则代表执行“前进”功能的次数。也就是说：

  ```JavaScript
  history.go(-2); // 就相当于执行两次 history.back() 调用。
  history.go(3);  // 就相当于执行三次 history.forward() 调用。
  ```

  但在某些情况下，`go()`方法也可以接收一个字符串类型的实参，用于以关键字的形式查找相关的历史记录，并重新载入其找到的第一个页面，例如：

  ```JavaScript
  history.go('google.com');
  history.go('127.0.0.1:5500');
  history.go('test.htm?script=js');
  ```

当然，在使用`history`对象时务必要清楚一个概念，那就是开发者在编写脚本时是不可能知道浏览器的访问历史中有多少记录的。而且，出于安全方面的考虑，在服务器端也不应该读取浏览器端的访问历史，所以 JavaScript 脚本对于浏览器访问历史的操作，只能交由具体执行该脚本代码的浏览器来“见机行事”。

#### 浏览器识别

虽说脚本的具体执行要交由浏览器“见机行事”，但就像是软件公司派出去给客户的技术支持人员，他们虽然无法预知客户那里具体发生的状况，但到了现场就必须要有迅速掌握客户环境的能耐，脚本至少也应该要具备识别自身所在浏览器的能力。这部分的功能就要依靠`window`对象中的另一个专职成员：`navigator`对象。该对象之所以叫这个名字是因为最初引入这个组件的是 Netscape Navigator 浏览器，但如今它已经成为了所有浏览器都支持的组件，我们可以通过它来获取脚本所在浏览器的相关信息，让脚本能自己识别自身所在的执行环境。下面，我们就来具体介绍一下`navigator`对象所提供的常用接口：

- **`appName`属性**：该属性返回脚本所在浏览器的完整名称，由于历史原因该属性很多时候都返回 Netscape。
- **`appVersion`属性**：该属性返回脚本所在浏览器的版本信息。  
- **`language`属性**：该属性返回脚本所在浏览器的默认语言。
- **`userAgent`属性**：该属性返回脚本所在浏览器将在其 HTTP 头信息的`user-agent`项中要发送的内容。
- **`cookieEnabled`属性**：该属性返回一个布尔类型的值，用于表示脚本所在的浏览器是否启用了 cookie。
- **`plugins`属性**：该属性返回一个用于存储插件信息的数组，用于表示脚本所在的浏览器中安装的插件。该数组中的每一项又都提供了以下接口：
  - **`name`属性**：该属性返回的是插件的名称。
  - **`description`属性**：该属性返回的是插件的说明性文本。
  - **`filename`属性**：该属性返回的是插件所对应的文件的名称。
  - **`length`属性**：该属性返回的是插件可处理的 MIME 类型的数量。
- **`platform`属性**：该属性返回脚本所在客户设备的名称。
- **`javaEnabled()`方法**：该方法返回一个布尔类型的值，用于表示脚本所在的浏览器是否启用了 Java。

当然，必须要强调的是，以上这些接口只是`navigator`对象众多属性和方法中被笔者认为较为常用的一部分，如果读者希望了解该对象的所有属性和方法，还请查阅相关的参考手册。下面，我们用以上属性编写一个脚本，并用它了解一些自己使用的浏览器：

```JavaScript
console.log('你所使用的浏览器是：', navigator.appName);
console.log('浏览器的发行版信息：', navigator.appVersion);
console.log('浏览器使用的默认语言：', navigator.language);
console.log('浏览器的user-agent信息：', navigator.userAgent);
console.log('浏览器是否启用了cookie：', navigator.cookieEnabled? '是':'否');
console.log('浏览器是否启用了java：', navigator.javaEnabled()? '是':'否');
console.log('浏览器所在的设备环境：', navigator.platform);
console.log('你的浏览器中按照了以下插件：');
for(const plugin of navigator.plugins) {
    console.log('-插件名称：', plugin.name);
    console.log('--插件描述：', plugin.description);
    console.log('--插件所在文件：', plugin.filename);
    console.log('--插件支持的MIME类型数量：', plugin.length);
}
```

读者可在自己使用的浏览器中执行上述脚本，并查看输出结果，譬如在笔者使用的 Google Chrome 浏览器中，其输出结果如下：

![查看浏览器信息](img/4.png)

#### 弹出对话框

在 Web 应用程序的运行过程中，有时候也需要像 PC 端桌面应用一样，以弹出对话框的方式来提示用户或让用户确认、提供某些信息。为此，`window`对象提供了以下三弹出基本系统对话框的方法，下面我们依次来介绍一下它们：

- **`alert()`方法**：该方法弹出的对话框中只有一条提示信息和一个确认按钮，该对话框通常用于提示或警告某一条消息，用户只需读取消息并单击按钮即可。该方法接收一个字符串类型的实参，用于设置需要提示的信息，例如：

    ```JavaScript
    alert('这是一条提示信息！');
    ```

    以上代码弹出的对话框如下图所示：

    ![消息提示对话框](img/5.png)

- **`confirm()`方法**：该方法弹出的对话框中包含一条待确认的消息，一个取消按钮和一个确认按钮。该对话框通常用于让用户确认某一条消息（通常是某个操作），我们可以根据当下看到的消息来决定点击取消按钮还是确认按钮。该方法接收一个字符串类型的实参，用于设置需要用户确认的信息，并且在用户单击确认按钮时返回 true，单击取消按钮或窗口的关闭按钮时返回 false。所以，`confirm()`方法的使用方式通常是这样的：

    ```JavaScript
    if(confirm('确定要执行这个操作吗？')) {
        console.log('确认！');
    } else {
        console.log('确认！');
    }
    ```

    以上代码弹出的对话框如下图所示：

    ![消息提示对话框](img/6.png)

- **`prompt()`方法**：该方法弹出的对话框中包含一个文本输入区域，一个取消按钮和一个确认按钮。该对话框通常用于让用户提供某一信息（譬如电子邮件地址），我们只需根据自己的需要选择是在输入相关信息之后单击确认按钮，还是直接单击取消按钮拒绝输入即可。该方法可接两个字符串类型的实参，第一个实参用于设置提示用户输入什么内容的文本，第二个实参用于设置默认的输入信息（该参数是可选的），并且在用户单击确认按钮时返回输入的内容，单击取消按钮或窗口的关闭按钮时返回 null。所以，`prompt()`方法的使用方式通常是这样的：

    ```JavaScript
    const email = prompt('请输入你的电子邮件地址：');
    if(email != null) {
        console.log(email);
    }
    ```

    以上代码弹出的对话框如下图所示：

    ![信息输入对话框](img/7.png)

需要特别强调的是，以上三种方法弹出的是系统对话框，它们不是 HTML 与 CSS 所描述的内容，其外观取决于用户所使用的 Web 浏览器与操作系统，并且，这三种对话框采用的都是同步执行的方式，这意味着，当以上任何一种对话框弹出时，JavaScript 脚本就会停止执行，直至对话框关闭之后才会继续执行。也正因为如此，我们并不建议读者在实际 Web 开发中过于频繁地使用这三种对话框，它们会破坏 Web 应用程序异步执行的优势。

## 综合练习

现在，让我们按照本书的惯例来对这篇笔记所介绍的知识点做一些具有实用性的使用示范，以便巩固学习成果。正如我们在开头所说，这里介绍的部分接口是一些可能尚未完全被纳入标准的 DOM 和 BOM 接口。况且，即使这些接口都已经被纳入了标准，各大浏览器对标准的实现完成度也不一样，甚至相同浏览器的不同版本之间对特定接口的支持也有差异（例如IE 8 和 9 这两个版本对标准接口的实现差异简直可以用“变异”来形容）。而 Web 应用程序开发的最大特点之一就是，开发者永远无法预知用户会使用什么浏览器来访问自己编写的程序。于是，让程序在运行时检测脚本所在的浏览器，以确定它是否支持我们在开发中使用到接口，并在这些接口不被支持时设置好备用方案或程序报错机制，就成为了 Web 开发着们在某些情况下不得不做的一件事。下面，我们以元素选择器的接口为例来示范一下这件事的具体处理方式。

正如之前所说的，在选取某个具体的页面元素时，选择`querySelector()`方法是一个更好的选择。但问题就在于，`querySelector()`方法是一个近些年才出现的 DOM 扩展接口。虽然目前各大主流浏览器的最新版本都支持了这一扩展接口，但我们依然无法确定该接口在所有用户使用的浏览器中都能正常运作，毕竟还有大量用户至今仍在在使用 IE 8 以及更早版本的 IE 浏览器呢。在这种情况下，我们就需要用回`getElementById()`系列的方法了，其具体处理过程如下：

```JavaScript
function getElement(query) {
    if(typeof document.querySelector == 'function') {
        return document.querySelector(query);
    } else {
        switch(query[0]) {
            case '#':
                return document.getElementById(query.substring(1));
            case '.':
                return document.getElementsByClassName(query.substring(1))[0];
            default:
                return document.getElementsByTagName(query)[0];
        }
    }
}
```

如你所见，我们在这里自己封装了一个元素选择器，并将其命名为`getElement()`函数，这个函数的实参与`document.querySelector()`方法的实参相同。在该函数中，我们首先会用`typeof`操作符来判断`document`对象中是否存在一个名为`querySelector`的成员，只有该成员存在并且是该对象的一个方法时，`typeof`操作符才会返回“function”这个字符串。在这种情况下，我们只需直接调用`document.querySelector()`方法即可。但是，如果该方法不存在，那么我们就需要对函数的实参进行分析，如果实参以`#`字符开头，就按元素的`id`属性来选取，如果实参以`.`字符开头，那就按元素的`class`属性值来选取，其他情况则按元素的标签名选取。

以上解决方案也可以运用到其他我们不确定是否被所有浏览器支持的 DOM 扩展接口，它的作用就像是许多电子产品的接口转换器，一旦发现新的接口规格不被支持，就自动转换到旧有规格的接口上去，以确保产品的基本功能可以正常运作。下面我们可以将这个自定义的元素选择器更新到之前的“电话交换机测试”程序的源码中，以作为常备工具来使用：

```JavaScript
import { TelephoneExchange } from './TelephoneExchange.js';

// 自定义元素选择器
function getElement(query) {
    if(typeof document.querySelector == 'function') {
        return document.querySelector(query);
    } else {
        switch(query[0]) {
        case '#':
            return document.getElementById(query.substring(1));
        case '.':
            return document.getElementsByClassName(query.substring(1))[0];
        default:
            return document.getElementsByTagName(query)[0];
        }
    }
}

const phoneExch = new TelephoneExchange(['张三', '李四', '王五', '赵六']);
const callList = getElement('#callList');  // 使用自定义选择器

for(const [key, name] of phoneExch.map.entries()) {
    const item = document.createElement('li');
    const btn = document.createElement('input');
    btn.type = 'button';
    btn.className = 'callme';
    btn.id = key;
    btn.value = name;
    item.appendChild(btn);
    callList.appendChild(item);
}
```

除了在运行时检测脚本所在浏览器对某一特定接口的支持情况，我们也可以通过读取`navigator`对象提供的各种信息来判断浏览器的状况，例如利用`navigator.cookieEnabled`来判断浏览器是否启用了 Cookie 功能，利用`navigator.javaEnabled()`来判断浏览器是否开启了对 Java 小程序的支持。除此之外，在实际开发中，我们通常还会通过解析`navigator.userAgent`返回的信息来完成识别浏览器的任务，例如可以编写这样一个返回浏览器名称的函数：

```JavaScript
function getdBrowserName() {
    const user_agent = navigator.userAgent;
    if(user_agent.indexOf('Firefox')>-1) {
        return 'Firefox';
    } else if(user_agent.indexOf('Chrome')>-1) {
        return 'Chrome';
    } else if(user_agent.indexOf('Trident')>-1
        && user_agent.indexOf('rv:11')>-1) {
        return 'IE11';
    } else if(user_agent.indexOf('MSIE')>-1
        && u_agent.indexOf('Trident')>-1) {
        return 'IE(8-10)';
    } else if(user_agent.indexOf('MSIE')>-1) {
        return 'IE(6-7)';
    } else if(user_agent.indexOf('Opera')>-1) {
        return 'Opera';
    } else {
        return '不知名的浏览器，其user-agent信息为：'+user_agent;
    }
}
```

然后，我们就可以根据`getdBrowserName()`函数返回的字符串来执行一些针对性的任务，例如 Google Chrome 与 Mozilla Firefox 这两款浏览器支持的插件各不相同，我们通常要先判断是什么浏览器，才能进一步确认它是否安装了某一插件，例如，如果我们想要在运行时确认 Google Chrome 浏览器是否安装了 PDF 插件，就可以编写这样一个函数：

```JavaScript
function hasPDFPlugin() {
    const browser_name = getdBrowserName();
    if(browser_name == 'Chrome') {
        for(const plugin of navigator.plugins) {
            if(plugin.name == 'Chrome PDF Plugin') {
                return true;
            }
        }
    }
    return false;
}
```

当然了，我们也可以用同样的方式识别浏览器所在的操作系统等信息，以便脚本可以在运行时针对特定的用户环境做出反应。但需要提醒读者的是，由于市场存在着恶性竞争的因素，浏览器提供商经常会在其`user-agent`信息中加入某些虚假信息，以便对脚本进行电子奇葩，例如，微软当初为了与网景竞争，在很长一段时间内都在其`user-agent`信息中声称自己是“Mozilla”浏览器。所以，我们并不鼓励过于依赖特定的浏览器来开发应用程序，在大部分时候应该尽量采用具有通用性的解决方案。
