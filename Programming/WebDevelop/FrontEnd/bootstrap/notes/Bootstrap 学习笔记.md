# Bootstrap 学习笔记

从方法论的角度来说，采用从零开始编写HTML+CSS代码的做法对于网页设计教学是非常有必要的，它能让初学者以“在做中学，学中做”的方式来实现快速入门，但在实际的生产环境中，继续这样做就不见得是最佳实践了，因为它不仅非常耗时费力，而且也极易出错，所以对网页设计师的要求也相对较高。如果我们平常只是一个前端程序员，并没有经历过专业的美术训练，那么大概率会在网页整体布局、图文信息排版、用户界面设计等问题上遇到较大的挑战。因此，在实际生产过程中，设计师们往往更倾向于使用成熟的第三方框架来辅助进行网页设计的工作。这篇笔记中，我们将致力于学习如何基于Bootstrap框架来快速完成网页的设计工作。

## 框架简介

Bootstrap框架是一款由Twitter公司推出、基于HTML+CSS+JavaScript技术实现的前端开发框架。它本质上是一个开源、免费的工具集，其中提供了一系列可重用的页面组件、样式类以及脚本代码，旨在帮助网页设计师快速构建出既充满专业感，又显得精致美观的网页（包括基于网页技术的Web应用程序界面）。目前，Bootstrap框架被广泛用于各种主流的Web应用中，例如Bing、LinkedIn、Instagram、Pinterest、Reddit、StackOverflow等，该框架在网页设计领域的最大竞争优势来自于以下几个方面：

- Bootstrap框架对响应式布局的强大支持。通过在项目中引入该框架，设计师们可以非常轻松地设计出能自动适应不同屏幕尺寸的网页，这将有助于提供更好的用户体验。在移动设备越来越普及的今天，响应式布局已经成为了Web开发的标配，Bootstrap框架的出现为开发者提供了一个快速实现响应式布局的工具。

- Bootstrap框架提供了丰富的用户界面组件和JavaScript插件（如导航栏、表格、表单、模态框等），这些组件和插件都经过了精心的设计和优化，能在不同的显示设备和浏览器上保持一致的显示效果，可以帮助设计师们轻松、快速地构建出各种常见的界面元素，这将大大提高他们的工作效率。除了现成的界面组件和JavaScript插件外，Bootstrap框架还支持自定义主题和样式，开发者可以根据自己的需求进行定制，从而实现更加个性化的界面设计。

- Bootstrap框架的开发者们还为初学者提供了详细的文档、丰富的示例代码以及完善的社区支持，这些资源都极大地平缓了该框架的学习曲线，使得人们快速掌握该框架的使用方法，这也是笔者在这里大力推荐读者基于 Bootstrap框架来学习网页设计的原因之一。

总而言之，Bootstrap框架是一款功能强大、易用性高、可扩展性强的前端开发框架，它为网页设计师们提供了快速构建响应式布局和常见Web界面元素的工具，极大地提高了开发效率和用户体验。如果读者想成为一名前端开发者，Bootstrap框架绝对是你应该要学习的工具之一。截止到本文撰写的时间为止（即2023年12月），Bootstrap框架已经迭代到了5.x版本系列，它相对于4.x和3.x最大的区别在于JavaScript脚本部分的实现，如今的Bootstrap框架在操作DOM时会直接使用ECMAScript 6的原生接口，不再需要额外引入jQuery库了。本文将基于5.x这一系列的版本来介绍如何使用Bootstrap框架来构建网页，接下来，我们将根据网页设计工作中不同的任务主题来介绍该框架的使用方法。

## 页面整体设计

正如上一节中所说，Bootstrap框架之所以如此受到欢迎，主要因为它提供了大量可重用的界面组件和CSS样式，这些组件和样式可以帮助设计师们快速有效地完成网页的整体设计任务。具体来说，Bootstrap框架在网页整体设计方面可以提供的便利主要如下：

- 它提供了大量的预定义样式，能够帮助网页设计师快速完成网页的整体布局。
- 它提供了大量的预定义模板，能够帮助网页设计师快速选择网页的配色方案。
- 它提供了大量的预定义组件，能够帮助网页设计师快速构建网页中要使用的界面元素。
- 它采用了基于移动设备优先的策略，能够帮助网页设计师快速实现网页的响应式布局。

### 完成整体布局

下面，让我们先从网页的整体布局任务开始。在考虑网页的整体布局时，Bootstrap框架为我们提供了以下几种常见的布局样式：

1. **固定宽度布局**：如果要采用这种布局样式，设计师需要使用`container`类来为网页内容提供了一个中心对齐且具有固定宽度的容器。这种容器会随着屏幕或视口尺寸的改变而调整其宽度。

2. **流体宽度布局**：如果要采用这种布局样式，设计师需要使用`container-fluid`类来为网页元素提供一个宽度为100%的容器，意味着它会占据其父元素或视口的整个宽度。

3. **响应式栅格布局**：如果要采用这种布局样式，设计师需要使用`container`和`row`这两个类来组织内容，然后在每个`row`类定义的页面元素中使用`col`类来安排更具体的网页内容。Bootstrap框架的栅格系统是一个强大的布局工具，它是响应式的，可以让网页自行适应不同视口尺寸。

4. **Flexbox布局**：Flexbox是一个独立的CSS布局模型，但Bootstrap框架已经整合了这种布局样式，提供了一系列与Flexbox相关的实用类（包括`d-flex`、 `justify-content-*`、 `align-items-*`等）。这种布局样式可以让设计师在一个容器内以更灵活的方式排列、对齐和分配子元素。与传统的浮动或定位方法相比，Flexbox提供了更多的控制和更简单的解决方案，特别是对于复杂的布局和对齐问题。

5. **组件布局**： Bootstrap框架还提供了许多组件，如导航栏、卡片、警报框等，读者可以使用这些组件来构建特定类型的布局。例如，你可以使用导航栏组件来创建一个具有导航功能的网站头部。

当然了，除了选择上面其中一种布局样式之外，读者还可以根据自己的具体需求灵活地混合使用这些样式，以便创建出更具复杂性的网页。Bootstrap框架的灵活性及其提供的丰富文档资源可以帮助我们轻松实现各种复杂的网页布局设计。接下来，让我们通过一个简单项目来为读者演示一下在项目中引入Bootstrap框架的具体步骤，以及如何基于该框架来完成网页的整体布局任务，项目的创建过程如下。

1. 在本地计算机中创建一个名为`HelloBootstrap`的文件夹（在这里，我将会将它创建在本笔记文件所在的目录下的`examples`目录中），并在其中创建一个名为`index.htm`的网页文件和两个分别名为`styles`和`scripts`的子目录。

2. 打开网页浏览器，使用搜索引擎找到Bootstrap框架的官网，然后进入到如下图所示的下载页面，并单击图中的「Download」按钮将编译好的CSS和JavaScript文件下载到本地计算机中。

    ![Bootstrap官方下载页面](./img/1.png)

3. 下载完成后，读者会得到一个名为`bootstrap-5.3.2-dist.zip`的压缩包文件，接下来的工作就是要该文件解压并将其中路径为`css/bootstrap.min.css`的文件复制到`HelloBootstrap`项目的`styles`目录下，而路径为`js/bootstrap.min.js`的文件则复制到该项目的`scripts`目录下。

4. 接下来，读者需要使用VS Code编辑器中打开`HelloBootstrap`项目，并在之前创建的`index.htm`文件的输入如下代码：

    ```html
    <!DOCTYPE html>
    <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="styles/bootstrap.min.css">
            <title>基于Bootstrap的网页布局</title>
        </head>
        <body>
            <nav class="p-3 navbar navbar-expand-lg bg-dark navbar-dark">  
                <div class="container">  
                <a class="navbar-brand" href="#">
                    <img src="./img/logo.jpg" class="rounded-pill" style="width: 3vw;" >
                    <span style="vertical-align: middle;" >导航栏区域</span>
                </a>  
                <button class="navbar-toggler" type="button"
                    data-bs-toggle="collapse" data-bs-target="#navbarNav"  
                    aria-controls="navbarNav" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>  
                </button>  
                <div class="collapse navbar-collapse" id="navbarNav">  
                    <ul class="navbar-nav ms-auto">  
                    <li class="nav-item">  
                        <a class="nav-link" href="#">链接1</a>  
                    </li>  
                    <li class="nav-item">  
                        <a class="nav-link" href="#">链接2</a>  
                    </li>  
                    <li class="nav-item">  
                        <a class="nav-link" href="#">链接3</a>  
                    </li>  
                    </ul>  
                </div>  
                </div>  
            </nav>
            <header class="p-4 bg-secondary text-light">
                <div class="container">
                    <h1>头部区域</h1>
                    <p>
                        header 标记用于定义网页的头部区域，
                        该区域通常用于放置网站的的标题。
                    </p>
                </div>
            </header>
            <main class="p-5">
                <section class="container">
                    <h2>章节区域</h2>
                    <p class="p-4">
                        section 标记用于定义网页中的章节区域，
                        根据要显示的内容类型，同一网页可被划分为多个章节区域。
                    </p> 
                    <div class="d-flex">
                        <aside class="p-3 bg-secondary text-light">
                            <h3>侧边栏区域</h3>
                            <p >aside 标记通常用于设置文章的内部导航。</p>
                            <nav class="navbar flex-column">
                                <a class="nav-link active" href="#">目录 1</a>
                                <a class="nav-link" href="#">目录 2</a>
                                <a class="nav-link" href="#">目录 3</a>
                                <a class="nav-link" href="#">目录 4</a>
                                <a class="nav-link" href="#">目录 5</a>
                                <a class="nav-link" href="#">目录 6</a>
                            </nav>
                        </aside>
                        <article class="p-3">
                            <h3>文章区域</h3>
                            <p class="mx-3">
                                article 标记通常用于定义一篇文章，
                                同一章节中可以有多篇文章。
                            </p>
                            <div class="p-3">
                                <h4>文章标题</h4>
                                <p class="mx-3">
                                    这是一个段落。这是一个段落。这是一个段落。
                                </p>
                                <h5>文章子标题</h5>
                                <p class="mx-3">
                                    这是另一个段落。这是另一个段落。这是另一个段落。
                                </p>
                            </div>
                        </article>        
                    </div>
                </section>
            </main>
            <footer class="p-3 bg-dark text-light  fixed-bottom">
                <div class="container">
                    <p>
                        footer 标记用于定义网页的页脚部分，
                        该区域通常用于放置与网站的合作方、版权相关的信息。
                    </p> 
                </div>
            </footer>
            <script src="./scripts/bootstrap.min.js"></script>
        </body>
    </html>
    ```

5. 在保存上述代码之后，读者就可以使用网页浏览器打开`index.htm`文件查看当前网页设计的结果，其外观样式在Google Chrome浏览器中的效果如下图所示。

    ![基于Bootstrap框架的网页布局示例](./img/2.png)

在上述示例中，我们首先在项目中引入了Bootstrap框架的CSS样式文件和JavaScript文件（以便能该框架提供的外观样式及其相关的功能），然后使用了该框架提供的样式类来完成网页的整体布局，并安排不同布局元素中的内容。关于页面内容的安排，我们会在后面的章节中做专门介绍，现在先来重点关注网页的整体布局。我们在这里主要采用了组件布局和Flexbox布局两大类布局样式。其中，组件布局类的样式主要运用于导航栏区域，而在作为网页主要区域的章节区域中采用的则是Flexbox布局，具体说明如下：

- 在导航栏区域，我们使用`navbar`和`navbar-expand-lg`这两个类创建了一个响应式的`<nav>`元素。在该元素内部，`navbar-brand`类用于定义当前网页的Logo元素（包括图片与文字）。`navbar-nav`类和`nav-item`类用于创建导航栏中的链接列表元素。另外在响应式布局方面，我们还利用`navbar-toggler`类创建了一个按钮元素，当网页在小屏幕设备上被访问时它就会被显示出来，而导航链接列表将会被收起，只有当用户点击该按钮时它才会重新被展开或收起。为此，我们需要将导航栏中的链接列表放在一个由`collapse`和`navbar-collapse`这两个类创建的`<div>`元素中。除此之外，我们还为导航链接列表本身添加了一个`ms-auto`类，这也是Bootstrap的响应式工具类之一，它会在小屏幕设备上自动将导航链接移到另一侧，以适应屏幕宽度。

- 在章节区域，我们首先使用`d-flex`类创建了一个以`<div>`标记来定义的弹性容器，然后用该容器来完成相关页面元素的排列和定位。这里的`d-flex`类也是Bootstrap框架提供的一个响应式工具类，下面是关于该类的使用说明：
  - **Flex容器**：`d-flex`类被应用于一个HTML元素（通常是`<div>`），将其定义为Flex容器。这意味着该元素的子元素将遵循Flexbox规则进行排列和布局。
  - **子元素排列**：一旦一个元素被定义为Flex容器，它的直接子元素成为Flex项，这些项会在容器内自动排列。你可以使用Bootstrap框架提供的其他类来控制子元素的排列方式，例如`justify-content-*`和`align-items-*`类，用于水平和垂直对齐。
  - **弹性布局**：Flexbox布局提供了一种强大的方式来管理和调整元素之间的空间分配。使用`d-flex`类，你可以轻松实现弹性的网页布局，以适应不同屏幕尺寸和内容需求。
  - **适应性和响应性**：Flexbox是响应式布局的理想选择，因为它可以在不同屏幕尺寸下自动调整元素的排列和大小，无需使用媒体查询。这使得你可以更容易地创建适应各种设备的网页布局。

### 制定配色方案

除了布局方面之外，网页的整体设计任务中还包含了配色方案的选择。由于网页的配色方案对于它所属的品牌标识，以及其用户的使用体验都具有着非常重要的影响，因此在启动一个网页设计项目时，设计师们首要任务之一就是要为网站设计一个符合其所属企业或个人的配色方案，以便增强用户对相关品牌标识的认知和记忆。例如，如今的人看到黄底黑字的配色很容易联想到美团外卖，看到红加白的配色可能就会联想到蜜雪冰城等。

正如你在上述示例中所见，设计师们在使用Bootstrap框架来进行网页整体设计的时候，通常会优先使用`bg-*`、`text-*`和`border-*`这三组样式类来制定一个初步的配色方案，然后再根据品牌的具体需求进行调整。Bootstrap框架中的这三组样式类提供了一系列具有预定含义的色彩，我们可以利用这些色彩快速有效地设计出具有通用性的网页配色方案。下面，让我们来详细介绍一下这三组样式类：

- `bg-*`样式类用于设置网页整体或者特定页面元素的背景颜色，它通常会为整个网页奠定基本的色彩基调。通过使用不同的背景颜色，设计师们可以清晰地划分出网页的不同区域，并给用户带来视觉上的层次感。这组样式类可能采用的颜色具体如下：
  - `bg-primary`类：效果为蓝色的背景；
  - `bg-success`类：效果为绿色的背景；
  - `bg-info`类：效果为浅蓝色的背景；
  - `bg-warning`类：效果为橙色的背景；
  - `bg-danger`类：效果为红色的背景；
  - `bg-secondary`类：效果为灰色的背景；
  - `bg-dark`类：效果为暗色系的背景；
  - `bg-light`类：效果为浅色系的背景；
  - `bg-transparent`类，效果透明的背景；

- `text-*`样式类用于设置网页中的文本颜色，它可以使得文本内容在网页中更加突出和易于阅读。设计师们通常根据文本的重要性来选择不同的文本颜色，例如主要文本、次要文本、成功信息、警告信息等。这组样式类可能采用的颜色具体如下：
  - `text-muted`类: 效果为浅灰色的文本，用于表示一些具有静默意义的文本；
  - `text-primary`类：效果为蓝色的文本，用于表示一些具有主要意义的文本；
  - `text-success`类：效果为绿色的文本，用于表示一些带有成功意义的文本；
  - `text-info`类：效果为浅蓝色的文本，用于表示一些带有信息意义的文本；
  - `text-warning`类：效果为橙色的文本，用于表示一些带有警告意义的文本；
  - `text-danger`类：效果为红色的文本，用于表示一些带有危险意义的文本；
  - `text-secondary`类：效果为灰色的文本，用于表示一些带有次要意义的文本；
  - `text-white`类：效果为白色的文本，主要用于搭配深色系背景色；
  - `text-light`类：效果为浅白色的文本，主要用于搭配深色系背景色；
  - `text-dark`类：效果为深黑色的文本，主要用于搭配浅色系背景色。
  - `text-body`类：效果为默认的黑色文本，主要用于搭配深色系背景色；

    除了上述单纯用于设置文本颜色的样式类之外，`text-*`样式类中还包含了一组以`text-bg-`为前缀的样式类，它们可以用于快速设置元素文本与其背景的搭配色，具体如下：
    - `text-bg-primary`类：效果通常为蓝色背景，白色字体的文本，主要用于显示主要信息的文本；
    - `text-bg-success`类：效果通常为绿色背景，白色字体的文本，主要用于显示带有成功意义的文本；
    - `text-bg-info`类：效果通常为浅蓝色背景，白色字体的文本，主要用于显示一些具有提示意义的文本；
    - `text-bg-warning`类：效果通常为橙色背景，白色字体的文本，主要用于显示带有警告信息的文本；
    - `text-bg-danger`类：效果通常为红色背景，白色字体的文本，主要用于显示带有危险提示信息的文本；
    - `text-bg-secondary`类：效果通常为灰色背景，白色字体的文本，主要用于显示次要信息的文本；
    - `text-bg-dark`类：效果通常为深灰色背景，白色字体的文本，主要用于设置深色系的文本元素；
    - `text-bg-light`类：效果通常为浅灰色背景，黑色字体的文本，主要用于设置浅色系的文本元素；

- `border-*`类用于设置网页中各页面元素的边框颜色，它可以让页面各元素之间更易于区分。设计师们可以利用边框颜色与背景颜色（或文本颜色）之间的相互配合来增强网页的视觉层次感。这组样式类可能采用的颜色具体如下：
  - `border-primary`类：采用与`bg-primary`相同的边框颜色；
  - `border-secondary`类：采用与`bg-secondary`相同的边框颜色；
  - `border-success`类：采用与`bg-success`相同的边框颜色；
  - `border-danger`类：采用与`bg-danger`相同的边框颜色；
  - `border-warning`类：采用与`bg-warning`相同的边框颜色；
  - `border-info`类：采用与`bg-info`相同的边框颜色；
  - `border-light`类：采用与`bg-light`相同的边框颜色；
  - `border-dark`类：采用与`bg-dark`相同的边框颜色；

当然了，我们在这里所做的只是一次关于如何使用Bootstrap框架的初体验，目的是让读者对该框架的使用方法能有一个大致的了解。接下来，我们还将结合网页设计工作中的其他任务做更多的演示。

## 图文信息排版

在完成了网页的整体设计工作之后，设计师们接下来的工作就是安排要如何显示网页中的具体内容了。而在网页可显示的诸多元素中，最基本的就是图文类元素了，这类元素主要包括标题、段落、强调、引用、链接、列表、表格、图片等。下面，让我们来继续介绍Bootstrap框架中可用于图文信息排版的样式类和界面组件。和之前一样，我们会先通过设计一个简单的示例来演示一下这些样式类和组件在图文排版任务中的应用，该示例的构建步骤如下：

1. 在本地计算机中创建一个名为`TextLayout`的项目（在这里，我将会将它创建在本笔记文件所在的目录下的`examples`目录中），并按照之前示例中演示的方法将Bootstrap框架引入到当前项目中。

2. 在VS Code这样的代码编辑器中打开刚刚创建项目，然后在该项目的根目录下创建一个`index.htm`文件，并在其中输入以下代码：

    ```html
    <!DOCTYPE html>
    <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="./styles/bootstrap.min.css">
            <script src="./scripts/bootstrap.min.js" defer></script>
            <title>网页文本排版示例</title>
        </head>
        <body class="p-4 container">
            <header class="p-3 text-center">
                <h1 class="p-3 m-3">图文报告标题</h1>
                <p class="m-0">报告人：owlman</p>
                <p class="m-0">发布日期：2023年12月</p>
            </header>
            <main class="row">
                <aside class="mt-3 p-3 col-3 text-bg-light">
                    <h2 class="p-2">目录：</h2>
                    <ul>
                        <li>第一部分：概述</li>
                        <li>第二部分：论述</li>
                        <li>第三部分：结论</li>
                        <li>第四部分：文献</li>
                <section class="p-2 col-9">
                    <article class="py-2 my-3 container">
                        <h2 class="mb-4 pb-2 border-bottom">第一部分：概述</h2>
                        <p>
                            在这里主要写一些报告的
                            <em class="mark">简单概要以及一些背景信息</em>。
                        </p>
                        <p>
                            要报告的问题包括：
                            Lorem ipsum dolor sit amet, consectetur adipisicing elit. 
                            Fuga facilis iure consequatur aspernatur! Libero, 
                        </p>
                        <p>
                            报告的相关背景：
                            Lorem ipsum dolor sit amet, consectetur adipisicing elit. 
                            Fuga facilis iure consequatur aspernatur! Libero, 
                        </p>
                    </article>
                    <article class="py-2 my-3">
                        <h2 class="mb-4 pb-2 border-bottom">第二部分：论述</h2>
                        <p>
                            在这里可以放置一些与报告内容相关的
                            <em class="mark">图片、表格以及引用文字</em>。
                        </p>
                        <div class="card m-2">
                            <div class="row  g-0">
                                <div class="card-body col-6">
                                    <h3 class="card-title mb-4">图文分析</h3>
                                    <p class="card-text">
                                        在这里可以用
                                        <em class="mark">无序列表和图片</em>
                                        元素来做一些分析说明。
                                    </p>
                                    <ul class="card-text">
                                        <li>第一项说明：Lorem sit amet。</li>
                                        <li>第二项说明：Lorem sit amet。</li>
                                        <li>第三项说明：Lorem sit amet。</li>
                                        <li>第四项说明：Lorem sit amet。</li>
                                        <li>第五项说明：Lorem sit amet。</li>
                                        <li>第六项说明：Lorem sit amet。</li>
                                        <li>第七项说明：Lorem sit amet。</li>
                                    </ul>
                                </div>
                                <img class="col-6 w-50 card-img"
                                    src="./img/pic.png" alt="示例图片">
                            </div> 
                        </div>
                        <div class="p-2 m-2">
                            <h3 class="mb-4">表格分析</h3>
                            <table class="table table-striped">
                                <thead class="table-dark">
                                    <tr>
                                        <th>项目名称</th>
                                        <th>报价数据</th>
                                        <th>相关说明</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>项目1</td>
                                        <td>￥30000</td>
                                        <td>在这里写一段说明文字。</td>
                                    </tr>
                                    <tr>
                                        <td>项目2</td>
                                        <td>￥25000</td>
                                        <td>在这里写一段说明文字。</td>
                                    </tr>
                                    <tr>
                                        <td>项目3</td>
                                        <td>￥50000</td>
                                        <td>在这里写一段说明文字。</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div class="p-2 m-2">
                            <h3 class="mb-4">引用文献</h3>
                            <blockquote class="p-3 blockquote text-bg-light">
                                <p>
                                    在这里可以使用
                                    <em class="mark">引用元素</em>
                                    援引一段现有文献中的文本段落。
                                </p>
                                <p class="blockquote-footer text-end">
                                    引用自《参考资料名称》
                                </p>
                            </blockquote>
                        </div>                
                    </article>
                    <article class="py-2 my-3 container">
                        <h2 class="mb-4 pb-2 border-bottom">第三部分：结论</h2>
                        <p>
                            在这里可以用
                            <em class="mark">无序列表</em>
                            元素来做一个总结。
                        </p>
                        <ul>
                            <li>
                                <strong class="p-1 text-bg-warning rounded ">
                                    结论一
                                </strong>：在这里写一段总结文字，
                                <span>
                                    ipsum dolor sit amet consectetur elit。
                                </span>  
                            </li>
                            <li>
                                <strong  class="p-1 text-bg-warning rounded">
                                    结论二
                                </strong>：在这里写一段总结文字，
                                <span>
                                    ipsum dolor sit amet consectetur elit。
                                </span>
                            </li>
                            <li>
                                <strong class="p-1 text-bg-warning rounded">
                                    结论三
                                </strong>：在这里写一段总结文字，
                                <span>
                                    ipsum dolor sit amet consectetur elit。
                                </span>
                            </li>
                        </ul>
                    </article>
                    <article class="py-2 mt-3 container">
                        <h2 class="mb-4 pb-2 border-bottom">第四部分：文献</h2>
                        <p>
                            在这里可以用
                            <em class="mark">有序列表+超链接元素</em>
                            来列举报告的参考文献。
                        </p>
                        <ol>
                            <li><a href="https://www.example.com">
                            【引用期刊格式】[序号]作者.篇名[J].刊名，出版年份，卷号（期号）：起止页码.
                            </a></li>
                            <li><a href="https://www.example.com">
                            【引用论文格式】[序号]作者.篇名[C].出版地：出版者，出版年份：起始页码. 
                            </a></li>
                            <li><a href="https://www.example.com">
                            【引用专着格式】[序号]作者.书名[M].出版地：出版社，出版年份：起止页码.
                            </a></li>
                        </ol> 
                    </article>
                </section>
            </main>
            <footer class="mt-4 p-2 border-top row text-center">
                <p class="text-muted">&copy; 2023 图文报告公司</p>
            </footer>        
        </body>
    </html>
    ```

3. 在保存上述代码之后，读者就可以使用网页浏览器打开`index.htm`文件查看当前网页设计的结果，其外观样式在Google Chrome浏览器中的效果如下图所示。

    ![基于Bootstrap框架的图文排版示例](./img/3.png)

正如读者所见，上述示例仅使用Bootstrap框架提供的一系列样式类就实现了《[[CSS 学习笔记]]》一文中用上百行CSS代码实现的类似效果，下面，就让我们从最基本的内外边距设置开始来逐一介绍这些样式类的使用方法。

### 元素基本设置

正如笔者曾经在《[[CSS 学习笔记]]》一文所介绍的，HTML/XML文档中的元素在CSS视角下是以“盒模型”的形式出现在显示设备中的，因此设置元素的尺寸大小，以及它们之间的间距是网页设计工作中最基本，最重要的任务之一。为了完成这一任务，设计师们通常会需要亲自编写相应的在CSS代码，先使用选择器匹配要设置样式的元素，然后利用`width`和`height`属性设置该元素的尺寸大小，用`margin`属性来设置该元素与相邻外界元素之间的距离（即外边距），而`padding`属性则用来设置该元素与其内部子元素之间的距离（即内边距）。但如果在项目中引入了Bootstrap框架，我们通常只需要直接在HTML/XML文档中使用`w-*`、`h-*`、`m-*`和`p-*`这两组预定义的样式类就可以快速完成这一任务。下面，我们就来详细介绍一下这两组样式类。

- `w-*`样式类：以`w-`为前缀的这组样式类主要用于设置元素的宽度尺寸，其可设定的值包括`25`、`50`、`75`、`100`和`auto`五种，其对应的CSS样式值如下表所示：

    | Bootstrap样式类 | CSS样式值 |
    | :--------------- | :--------- |
    | `w-25`            | `{width:25% !important}` |
    | `w-50`            | `{width:50% !important}` |
    | `w-75`            | `{width:75% !important}` |
    | `w-100`          | `{width:100% !important}` |
    | `w-auto`         | `{width:auto !important}` |

- `h-*`样式类：以`h-`为前缀的这组样式类主要用于设置元素的高度尺寸，其可设定的值同样也包括`25`、`50`、`75`、`100`和`auto`这五种，其对应的CSS样式值如下表所示：

    | Bootstrap样式类 | CSS样式值 |
    | :--------------- | :--------- |
    | `h-25`           | `{height:25% !important}` |
    | `h-50`           | `{height:50% !important}` |
    | `h-75`           | `{height:75% !important}` |
    | `h-100`          | `{height:100% !important}` |
    | `h-auto`         | `{height:auto !important}` |

- `m-*`样式类：以`m-`为前缀的这组样式类主要用于设置元素的外边距，其可设置的值主要有`0`、`1`、`2`、`3`、`4`、`5`和`auto`这七种，其对应的CSS样式值如下表所示：

    | Bootstrap样式类 | CSS样式值 |
    | :--------------- | :--------- |
    | `m-0`             | `{margin:0 !important}` |
    | `m-1`             | `{margin:0.25rem !important}` |
    | `m-2`             | `{margin:0.5rem !important}` |
    | `m-3`             | `{margin:1rem !important}` |
    | `m-4`             | `{margin:1.5rem !important}` |
    | `m-5`             | `{margin:3rem !important}` |
    | `m-auto`          | `{margin:auto !important}` |

    当然了，我们也可以在`m`之后加上`l`、`r`、`t`、`b`、`x`、`y`和`a`这七个字母中的任意一个，来分别单独设置元素的外左边距、外右边距、外上边距、外下边距、外左右边距和外上下边距，它们同样可以设置`0`、`1`、`2`、`3`、`4`、`5`和`auto`这七种值，其对应的CSS样式值如下表所示：

    | Bootstrap样式类 | CSS样式值 |
    | :--------------- | :--------- |
    | `ml-0`          | `{margin-left:0 !important}` |
    | `ml-1`          | `{margin-right:0.25 !important}` |
    | `ml-2`          | `{margin-right:0.5 !important}` |
    | `ml-3`          | `{margin-right:1 !important}` |
    | `ml-4`          | `{margin-right:1.5 !important}` |
    | `ml-5`          | `{margin-right:3 !important}` |
    | `ml-auto`       | `{margin-right:auto !important}` |
    | `mr-0`          | `{margin-right:0 !important}` |
    | `mr-1`          | `{margin-right:0.25 !important}` |
    | `mr-2`          | `{margin-right:0.5 !important}` |
    | `mr-3`          | `{margin-right:1 !important}` |
    | `mr-4`          | `{margin-right:1.5 !important}` |
    | `mr-5`          | `{margin-right:3 !important}` |
    | `mr-auto`       | `{margin-right:auto !important}` |
    | `mt-0`          | `{margin-top:0 !important}` |
    | `mt-1`          | `{margin-top:0.25 !important}` |
    | `mt-2`          | `{margin-top:0.5 !important}` |
    | `mt-3`          | `{margin-top:1 !important}` |
    | `mt-4`          | `{margin-top:1.5 !important}` |
    | `mt-5`          | `{margin-top:3 !important}` |
    | `mt-auto`       | `{margin-top:auto !important}` |
    | `mb-0`          | `{margin-bottom:0 !important}` |
    | `mb-1`          | `{margin-bottom:0.25 !important}` |
    | `mb-2`          | `{margin-bottom:0.5 !important}` |
    | `mb-3`          | `{margin-bottom:1 !important}` |
    | `mb-4`          | `{margin-bottom:1.5 !important}` |
    | `mb-5`          | `{margin-bottom:3 !important}` |
    | `mb-auto`       | `{margin-bottom:auto !important}` |
    | `mx-0`          | `{margin-left:0 !important;margin-right:0 !important}` |
    | `mx-1`          | `{margin-left:0.25 !important;margin-right:0.25 !important}` |
    | `mx-2`          | `{margin-left:0.5 !important;margin-right:0.5 !important}` |
    | `mx-3`          | `{margin-left:1 !important;margin-right:1 !important}` |
    | `mx-4`          | `{margin-left:1.5 !important;margin-right:1.5 !important}` |
    | `mx-5`          | `{margin-left:3 !important;margin-right:3 !important}` |
    | `mx-auto`       | `{margin-left:auto !important;margin-right:auto !important}` |
    | `my-0`          | `{margin-top:0 !important;margin-bottom:0 !important}` |
    | `my-1`          | `{margin-top:0.25 !important;margin-bottom:0.25 !important}` |
    | `my-2`          | `{margin-top:0.5 !important;margin-bottom:0.5 !important}` |
    | `my-3`          | `{margin-top:1 !important;margin-bottom:1 !important}` |
    | `my-4`          | `{margin-top:1.5 !important;margin-bottom:1.5 !important}` |
    | `my-5`          | `{margin-top:3 !important;margin-bottom:3 !important}` |
    | `my-auto`       | `{margin-top:auto !important;margin-bottom:auto !important}` |

- `p-*`样式类：以`p-`为前缀的这组样式类主要用于设置元素的内边距，其可设置的值也主要有`0`、`1`、`2`、`3`、`4`、`5`和`auto`这七种，其对应的CSS样式值如下表所示：

    | Bootstrap样式类 | CSS样式值 |
    | :--------------- | :--------- |
    | `p-0`             | `{padding:0 !important}` |
    | `p-1`             | `{padding:0.25rem !important}` |
    | `p-2`             | `{padding:0.5rem !important}` |
    | `p-3`             | `{padding:1rem !important}` |
    | `p-4`             | `{padding:1.5rem !important}` |
    | `p-5`             | `{padding:3rem !important}` |
    | `p-auto`          | `{padding:auto !important}` |

    同样的，我们也可以在`p`之后加上`l`、`r`、`t`、`b`、`x`、`y`和`a`这七个字母中的任意一个，来分别单独设置元素的内左边距、内右边距、内上边距、内下边距、内左右边距和内上下边距，它们同样可以设置`0`、`1`、`2`、`3`、`4`、`5`和`auto`这七种值，其对应的CSS样式值如下表所示：

    | Bootstrap样式类 | CSS样式值 |
    | :--------------- | :--------- |
    | `pl-0`           | `{padding-left:0 !important}` |
    | `pl-1`           | `{padding-left:0.25rem !important}` |
    | `pl-2`           | `{padding-left:0.5rem !important}` |
    | `pl-3`           | `{padding-left:1rem !important}` |
    | `pl-4`           | `{padding-left:1.5rem !important}` |
    | `pl-5`           | `{padding-left:3rem !important}` |
    | `pl-auto`        | `{padding-left:auto !important}` |
    | `pr-0`           | `{padding-right:0 !important}` |
    | `pr-1`           | `{padding-right:0.25rem !important}` |
    | `pr-2`           | `{padding-right:0.5rem !important}` |
    | `pr-3`           | `{padding-right:1rem !important}` |
    | `pr-4`           | `{padding-right:1.5rem !important}` |
    | `pr-5`           | `{padding-right:3rem !important}` |
    | `pr-auto`        | `{padding-right:auto !important}` |
    | `pt-0`           | `{padding-top:0 !important}` |
    | `pt-1`           | `{padding-top:0.25rem !important}` |
    | `pt-2`           | `{padding-top:0.5rem !important}` |
    | `pt-3`           | `{padding-top:1rem !important}` |
    | `pt-4`           | `{padding-top:1.5rem !important}` |
    | `pt-5`           | `{padding-top:3rem !important}` |
    | `pt-auto`        | `{padding-top:auto !important}` |
    | `pb-0`           | `{padding-bottom:0 !important}` |
    | `pb-1`           | `{padding-bottom:0.25rem !important}` |
    | `pb-2`           | `{padding-bottom:0.5rem !important}` |
    | `pb-3`           | `{padding-bottom:1rem !important}` |
    | `pb-4`           | `{padding-bottom:1.5rem !important}` |
    | `pb-5`           | `{padding-bottom:3rem !important}` |
    | `pb-auto`        | `{padding-bottom:auto !important}` |
    | `px-0`           | `{padding-left:0 !important; padding-right:0 !important}` |
    | `px-1`          | `{padding-left:0.25rem !important; padding-right:0.25rem !important}` |
    | `px-2`           | `{padding-left:0.5rem !important; padding-right:0.5rem !important}` |
    | `px-3`           | `{padding-left:1rem !important; padding-right:1rem !important}` |
    | `px-4`           | `{padding-left:1.5rem !important; padding-right:1.5rem !important}` |
    | `px-5`           | `{padding-left:3rem !important; padding-right:3rem !important}` |
    | `px-auto`        | `{padding-left:auto !important; padding-right:auto !important}` |
    | `py-0`           | `{padding-top:0 !important; padding-bottom:0 !important}` |
    | `py-1`          | `{padding-top:0.25rem !important; padding-bottom:0.25rem !important}` |
    | `py-2`           | `{padding-top:0.5rem !important; padding-bottom:0.5rem !important}` |
    | `py-3`           | `{padding-top:1rem !important; padding-bottom:1rem !important}` |
    | `py-4`           | `{padding-top:1.5rem !important; padding-bottom:1.5rem !important}` |
    | `py-5`           | `{padding-top:3rem !important; padding-bottom:3rem !important}` |
    | `py-auto`        | `{padding-top:auto !important; padding-bottom:auto !important}` |

正如读者在之前的图文排版示例中所看到的，我们利用Bootstrap框架提供的这些样式类对页面中的很多元素都设置了相应的宽度和内外边距，以便它们可以更合适的形态出现在页面中，这些操作都是对网页进行图文信息排版时首先要完成的任务。

### 文本元素设置

对于网页中可显示的文本类元素，我们最常用到的主要包括标题、段落、强调、引用、链接这五种。Bootstrap框架对这些元素都预定义了一系列相应的样式类，并且这些样式类之间还有着一定的相互配合关系。

- **标题类元素**：

- **段落类元素**：

- **强调类元素**：

- **引用类元素**：

- **链接类元素**：

### 图表元素设置

## 用户界面设计
