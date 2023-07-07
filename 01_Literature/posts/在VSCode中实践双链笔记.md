# 在 VSCode 中实现双链笔记

---
 **文献说明：**

- 原文出处：`https://client.sspai.com/post/70956`；
- 二次加工：改善文章结构、标注文章要点；
- 关联文献：[[卡片盒笔记法介绍]]；

---

近年来，随着「卡片盒笔记系统」及其相关方法论的兴起，人们对更有效地记录笔记的需求的高涨，笔记软件的市场呈现出推陈出新和自我革新的局面。不仅有 Roam Research 和 Obsidian 等后起之秀凭借对这两种笔记法的率先支持获得广泛欢迎，一些传统笔记软件，例如 Notion，也在逐步加入相应的功能支持。在这些丰富的笔记软件选择之外，还有另一个值得关注的软件，也通过特殊的方式实现了这些功能需求，那就是微软出品的文本编辑器 VSCode。==VSCode 最为强大之处，就在于它可以通过丰富的扩展，将其定制成为自己专属且特化的应用==。这篇文章要介绍的，便是在 VSCode 上实现「卡片盒笔记系统」功能的扩展：Foam。

在 [Foam 插件的官方主页](https://client.sspai.com/link?target=https%3A%2F%2Ffoambubble.github.io%2Ffoam%2F) 上，==Foam 被定义为「**受 Roam Research 启发**的、依托于 VSCode 和 GitHub 的、**管理和分享**个人知识的系统」==。你可以用它来组织研究、记录笔记或者在网络上发布内容。这篇文章中我们将主要把 Foam 作为构建卡片盒笔记系统的工具。

## 基础配置与上手

### 使用 VSCode

Foam 作为 [VSCode](https://client.sspai.com/link?target=https%3A%2F%2Fcode.visualstudio.com%2F) 的扩展，必须依托其上才能运行。而 VSCode 作为一个代码编辑器，主要还是面向前端工程师等群体，对于一些文字工作者可能有使用门槛，这里简单介绍一些在 VSCode 上使用 Foam 需要注意的点。

一个标准的 VSCode 项目（对于我们就是 Foam 笔记库），其配置文件位于项目文件夹（笔记库的根目录）下的 `.vscode` 文件夹下。在这篇文章中我们主要需要使用两个文件：`settings.json`（项目的配置文件）和 `foam-snippets.code-snippets` 文件（用户代码片段）。

需要注意的是，如果将笔记库保存为 VSCode 工作区，即后缀为 `.code-space` 的文件，那该文件本身就是工作区的配置文件。对该文件的更改会覆盖 `.vscode` 目录下 `settings.json` 文件中的配置。

在 VSCode 中执行一个命令（内建的或者来自扩展的），需要通过命令面板（command palette，快捷键 `Ctrl + Shift + P`）。这篇文章中主要使用的一些命令如下：

- `Foam: Create New Note`：在当前目录下创建新的笔记条目。
- `Foam: Show Graph`：打开知识图谱页面。
- `Foam: Open Daily Note`：创建 Daily Note。
- `Foam: Create New Note From Template`：从模板创建新笔记。

在 VSCode 中搜索文件可以使用快捷键 `Ctrl + P` 弹出对应面板，通过文件名进行搜索。打开侧边栏的搜索面板（快捷键 `Ctrl + Shift + F`），可以对整个笔记库的内容进行检索。

### 配置笔记库

下面开始建立 Foam 笔记库。根据是否使用 GitHub 进行版本控制，分为两种方案。

#### 在 GitHub 上建立笔记库

使用官方提供的 [foam-template](https://client.sspai.com/link?target=https%3A%2F%2Fgithub.com%2Ffoambubble%2Ffoam-template) 在自己的 GitHub 上建立仓库，可以选择是否将仓库设为私有库。仓库建立后，将其 clone 到本地并在 VSCode 中打开。这样以后就可以通过 GitHub 对你的笔记库进行版本控制，也可以通过 Github Pages 或其他静态网页服务发布笔记。

#### 在本地使用 Foam

鉴于国内的网络环境和学习 git 操作的学习成本，也可以选择在本地建立 Foam 笔记库。下载[官方模板](https://client.sspai.com/link?target=https%3A%2F%2Fgithub.com%2Ffoambubble%2Ffoam-template%2Farchive%2Fmaster.zip)到本地解压后便可以作为笔记库的根目录。

通过以上两种方式建立 Foam 笔记库，并在 VSCode 中打开笔记库根目录后，软件会自动提示安装 Foam 和其他推荐的扩展（包括：Markdown All in One、Markdown Emoji、Paste Image、Todo Tree 和 Spell Right 等），可以选择全部或按需安装。

### 初步上手

基础配置完成后，让我们开始了解 Foam 的基本功能和操作。Foam 具备一般卡片盒笔记软件的常用功能，如 Markdown 支持、双向链接、知识图谱、标签、Daily Note 等，且使用体验比较良好。

#### 创建新的笔记

要在 Foam 中创建新的笔记，可以使用快捷键 `Ctrl + Shift + P` 打开命令面板，输入并执行 `Foam: Create New Note` 命令，即可在当前文件夹下创建新的笔记文件（`.md` 格式）。当然也可以在侧边栏「资源管理器」面板或者通过快捷键 `Ctrl + N` 实现相应的功能。需要注意的是，因为 Foam 本地化程度有限，个人不推荐使用中文的文件名。官方用例中使用的文件名有两种：`title-case-name` 或 `Title Case Name`。

#### 创建双向链接

在 Foam 中创建一个双向链接与在其他软件中无异，即使用 `[[]]` 符号。如果被 `[[]]` 包括的文本有对应的笔记，就会成为一个双向链接。当将鼠标移动并悬浮在文本上时，会显示这一条目的预览，可以按下 `Ctrl + 单击` 或鼠标右键选择「转到定义」来打开这条笔记；如果没有对应的笔记，则会创建一个占位符，按下`Ctrl + Click` 创建可以对应的条目。

![](https://cdn.sspai.com/2022/01/14/3cf4c34d2df8a7a22dab9bb4f37e02a9.jpg?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1)

创建双向链接或占位符

Foam 并不支持 Roam Research 式的块引用，但支持标题引用，使用方式为：`[[wikilink#heading]]`，这样便能引用对应条目中该标题下的内容。

![](https://cdn.sspai.com/2022/01/14/c5dbc866108c6fbbf1571d730342519b.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1)

使用标题引用

#### 笔记元数据

使用 Markdown 文档时，在笔记头部使用 YAML 语言格式的字段来定义这个文档的元数据是一个良好的习惯，Foam 也支持这一功能（note property）。其格式如下：

```yaml
---
title: Title Case Name
date: yyyy-mm-dd
type: feature
tags: tag1, tag2, tag3
---
```

`title` 属性定义了这条笔记的标题和在知识图谱（Foam Graph）上的名称（标识笔记时，优先级为： `title` 属性 > 正文的一级标题 > 笔记的文件名）。

`tags` 属性定义这条笔记的标签。多个标签之间用空格或半角逗号分隔。另外也可以通过在笔记正文中使用 `#tag` 来添加标签。Foam 支持多级标签即 `#tag/sub-tag`，但笔者并不使用，个人认为这还是在按树状结构来组织笔记。

`type` 属性可以用于在知识图谱中区分笔记的类型，可以将不同 `type` 属性的笔记用不同颜色表示。

也可以自定义其他的属性，如：日期（`date`）、作者（`author`）、来源（`source`）等。

![](https://cdn.sspai.com/2022/01/14/a032170d973e9793d88c3601b5bea487.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1)

使用颜色区分不同 type 的笔记

#### 知识图谱

在命令面板执行 `Foam: Show Graph` 命令来打开 Foam 的知识图谱，还可以通过页面右上角的过滤控件进行图谱中显示的节点进行控制。同样支持缩放和拖拽等操作。

![](https://cdn.sspai.com/2022/01/14/da0d81a9b81f2fb5825b3a5a360d5ab3.jpg?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1)

Foam 中的知识图谱

#### Daily Note

与 Roam Research 类似，Foam 也支持快速记录 Daily Note。在命令面板执行 `Foam: Open Daily Note` 命令或按下快捷键 `Alt + D`，即可创建或打开今日的 Daily Note。在此处可以记录今天的任务、灵感或其他想要记录的内容。Daily Note 格式可以通过模板功能自定义（下文会介绍如何在 Foam 中自定义模板）。

在 Daily Note 笔记中，键入 `/` 会显示一些日期建议，通过这种方法可以快速插入指向指定日期的双向链接。

![](https://cdn.sspai.com/2022/01/14/cc2c50280e30638f25e679b85a5e9345.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1)

键入 / 来快速插入指向对应日期的链接

#### 侧边栏面板

Foam 的侧边栏面板包含这几项功能：文件管理、大纲、时间线、标签管理（Tag Explorer）、占位符（Placeholders）、孤立笔记（Orphans）和反向链接（Backlinks）。

大纲面板用于查看笔记的目录结构。时间线记录了文件修改和 git 操作的历史。标签管理面板中可以查看笔记库中的所有标签并进行检索。占位符面板显示了所有被 `[[]]` 标记但没有创建对应笔记的项目。孤立笔记指没有引用也没有被引用的笔记条目。而在反向链接面板，会列出全部引用了此条目的笔记。

这些功能面板可以通过拖动自行排序或隐藏，也可以拖动到底部面板（按下`Ctrl + J` 弹出）。个人习惯将反向链接面板和标签管理面板放到底部，方便查看。

![](https://cdn.sspai.com/2022/01/14/657a8fc52a3454515aa2bda1cc2c487a.jpg?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1)

Foam 的侧边栏面板

## 生产力从美化开始

正如前面所说，赏心悦目的界面也会对情绪和效率产生积极影响，因此对 Foam 的编辑器和笔记预览界面进行美化也是非常重要的一环。

Foam 使用 Markdown 作为笔记的文件格式，一方面其通用性便利了跨平台使用，另一方面也可以利用 `CSS` 文件对其进行美化（如果你想定制自己的 Markdown 的预览样式，可以参考 [Typora 的指南](https://client.sspai.com/link?target=https%3A%2F%2Ftheme.typora.io%2Fdoc%2FWrite-Custom-Theme%2F)）。

Foam 的项目配置文件是位于笔记库根目录下的 `.vscode/settings.json` 文件，Markdown 预览样式则由笔记库根目录下 `assets/css/style.scss` 文件控制。然而经过测试，直接修改该样式表文件并没有生效。这里我选择复制该文件并将后缀改为 `.css`，然后在配置文件中新增一行代码 `"markdown.styles": ["assets\\css\\style.css"],`，配置生效。

个人并没有进行太多的样式调整，主要是将英文字体改为 `Cascadia Code` 来实现对连写符号的支持：

![](https://cdn.sspai.com/2022/01/14/1dd648d69a06e81950919c851cb87be0.jpg?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1)

Cascadia Code 字体支持连写字符

## 使用代码片段和模板来提高效率

### 代码片段的配置介绍

VSCode 内建对代码片段（snippets）的支持，并且支持用户自定义代码片段，因此这一功能也可以在 Foam 中使用。在 Foam 笔记库根目录下 `.vscode` 路径创建 `foam-snippets.code-snippets` 文件以创建用户片段（该文件本质上是一个 json 文件）。

一条代码片段通常包含这些字段：

- `"scope"`，编辑这些格式的文件时，该代码片段生效；
- `"prefix"`，键入该字段时会显示该代码片段的建议；
- `"body"`，该代码片段的内容；
- `"description"`，对该代码片段的描述。

个人的两个用例是为笔记创建元数据和在笔记中插入时间戳，仅供参考。

### 创建笔记元数据

个人的笔记元数据中的属性一般包括：`title`，`date`，`type` 和 `tags`。

```json
"Metadata": {
    "scope": "markdown",
    "prefix": "/meta",
    "description": "创建这条笔记的元数据",
    "body": [
        "---",
        "title: $1",
        "date: $CURRENT_YEAR 年$CURRENT_MONTH_NAME $CURRENT_DATE 日",
        "type: ${2|生活,TODO,思考,知识|}",
        "tags: $3",
        "---"
    ]
}
```

在 VSCode 的代码片段中，类似 `$1` 这样的格式化文本称为 tabstop。在键入 `/meta` 并在建议中选择上述代码片段后，光标会首先停留在 `$1` 处，我们可以在此处输入文本，键入完成后按 `tab` 会跳转到下一个 tabstop `${2|type1,type2,type3|}`，这是一个需要选择而非键入的格式，完成选择后再次按 `tab`跳转到 `$3` 处，在此可以输入这条笔记的标签，全部完成后按 `tab` 跳出代码片段。

像 `date` 属性中的 `$CURRENT_YEAR` 和类似的格式化文本则是由 VSCode 预定义的变量，它的值和格式取决于系统的日期时间，因此在输入这条代码片段后，就会自动完成 `date` 属性，而不需要自行添加。

### 插入时间戳

由于笔记系统经常需要更新，个人偏好在内容更新处添加一条时间戳作为记录。

```json
"Time Stamp": {
    "scope": "markdown",
    "prefix": "/stamp",
    "description": "在此处插入一条时间戳",
    "body": [
        "这条笔记${1|创建,更新|}于: $CURRENT_YEAR 年$CURRENT_MONTH_NAME $CURRENT_DATE 日，$CURRENT_DAY_NAME，$CURRENT_HOUR: $CURRENT_MINUTE."
    ],
}
```

在 `$1` 处可以选择是创建还是更新了这个条目。

如果想要了解更多创建用户代码片段的方法，可以参考[微软的官方文档](https://client.sspai.com/link?target=https%3A%2F%2Fcode.visualstudio.com%2Fdocs%2Feditor%2Fuserdefinedsnippets)。

### 创建和使用模板

和 Roam Research 与 Obsidian 一样，在 Foam 中也可以创建和使用模板。在命令面板执行 `Foam: Create New Note From template` 命令即可从现有的模板创建笔记。Foam 的模板文件位于笔记库根目录的 `.foam/templates` 路径下。Foam 的模板同样支持 VSCode 代码片段中预定义的变量。

以 Daily Note 为例，在模板文件夹路径下创建 `daily-note.md` 文件，便可以开始自定义这一模板。我的 Daily Note 模板定义如下：

![](https://cdn.sspai.com/2022/01/14/0a829d4a7c2c4bbdb53b8b8e5c4a1c1b.png?imageView2/2/w/1120/q/40/interlace/1/ignore-error/1)

我的 Daily Note 模板

除此之外，Daily Note 的一些属性也可以在项目的配置文件中修改，如 Daily Note 的存放位置和文件名格式：

```yaml
"foam.openDailyNote.directory": "journal", // 默认存放在 journal 文件夹
"foam.openDailyNote.fileNameFormat": "'DailyNote'-yyyy-mm-dd" // Eg.: DailyNote-2022-01-13.md
"foam.openDailyNote.onStartup": true // 启动项目时自动打开 Daily Note
```

也可以在 Foam 中定义其他模板，如 Todo List、Weekly Note 等1，都会极大地便利个人的日常学习和各项工作。

### 使用 note-macros 扩展（不推荐）

除了使用 Foam 模板，官方也提供了从 note-macros 扩展快速创建新笔记的选择。note-macros 并不是配置 Foam 时就安装的扩展，因此需要自行安装。要创建由 note-macros 宏定义的笔记，只需在命令面板执行 `Note Macros: Run A Macro` 命令，然后选择自定义的宏即可。也可以为特定的宏绑定快捷键，像使用 `Alt + D` 创建 Daily Note 一样快速创建新笔记。

要创建自定义的宏，需要在配置文件中添加相应的字段。官方提供了从 note-macros 创建 Weekly Note 的用例：

```
"note-macros": {
    "Weekly": [
        {
            "type": "note",
            "directory": "Weekly",
            "extension": ".md",
            "name": "weekly-note",
            "date": "yyyy-W"
        }
    ]
}
```

不过需要注意的是，这种方式无法在创建笔记的同时创建笔记的元数据（note-macro 扩展的开发者虽然规划了这一功能，但实际上该扩展项目已经 17 个月没有更新了），需要自己定义相应的代码片段来实现快捷输入，而且无法自定义文件名的格式。总而言之，目前并不推荐使用这种方法来创建笔记模板。

## 从其它源获取内容

虽然我并不建议将来自外界的信息不经消化吸收直接保存在笔记库中，但 Foam 毕竟提供了这个选择并且确实存在这种需求，因此还是稍作提及。

### 从网页捕获内容

像其他笔记软件大多提供了剪辑网页内容的功能一样，Foam 也可以保存来自网页的内容：通过 [MarkDownload](https://client.sspai.com/link?target=https%3A%2F%2Fgithub.com%2Fdeathau%2Fmarkdownload) 这一浏览器扩展。MarkDownload 可以获取整个网页的主体文本、或只截取想要保存的文本为 Markdown 文件，并为其添加元数据。在扩展选项中可以调整元数据的格式为与 Foam 一致，从而无缝衔接 Foam 笔记库。

### 从 iOS 端输入内容

如果将 Foam 笔记库托管在 GitHub 上，我们就可以从 iOS 端输入内容并将其推送到库中。Foam 官方给出了 [通过 Shortcuts](https://client.sspai.com/link?target=https%3A%2F%2Ffoambubble.github.io%2Ffoam%2Frecipes%2Fcapture-notes-with-shortcuts-and-github-actions) 和 [通过 Drafts Pro](https://client.sspai.com/link?target=https%3A%2F%2Ffoambubble.github.io%2Ffoam%2Frecipes%2Fcapture-notes-with-drafts-pro) 输入内容两种解决方案。我目前手边并没有可用的 iOS 设备，因此就不再展开。

## 并不完美但未来可期

与 Roam Research 和 Obsidian 等专业笔记软件相比，Foam 或许没有独特优势，甚至在某些方面支持并不完善。但好在作为一个开源项目，它能够深植良好的社区环境，吸收用户的建议与反馈，让每个人都成为项目的贡献者。

目前国内介绍和分享 Foam 使用经验的内容比较少，本文仅作为抛砖引玉，让更多人能认识到这款工具。毕竟对用户来说，多一种选择本身就是一件好事，而对于开源项目的开发者而言，更多人参与其中本身就是开源理念的价值所在。如果你也想推动 Foam 项目的进展，可以关注他们的 [开发路线图](https://client.sspai.com/link?target=https%3A%2F%2Ffoambubble.github.io%2Ffoam%2Fdev%2Froadmap)，或者加入他们的 [Discord Server](https://client.sspai.com/link?target=https%3A%2F%2Ffoambubble.github.io%2Fjoin-discord%2Fw)。
