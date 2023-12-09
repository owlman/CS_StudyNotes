# Bootstrap 学习笔记

从方法论的角度来说，采用从零开始编写HTML+CSS代码的做法对于网页设计教学是非常有必要的，它能让初学者以“在做中学，学中做”的方式来实现快速入门，但在实际的生产环境中，继续这样做就不见得是最佳实践了，因为它不仅非常耗时费力，而且也极易出错，所以对网页设计师的要求也相对较高。如果我们平常只是一个前端程序员，并没有经历过专业的美术训练，那么大概率会在网页整体布局、图文信息排版、用户界面设计等问题上遇到较大的挑战。因此，在实际生产过程中，设计师们往往更倾向于使用成熟的第三方框架来辅助进行网页设计的工作。这篇笔记中，我们将致力于学习如何基于Bootstrap框架来快速完成网页的设计工作。

## 框架简介

Bootstrap框架是一款由Twitter公司推出、基于HTML+CSS+JavaScript技术实现的前端开发框架。它本质上是一个开源、免费的工具集，其中提供了一系列可重用的页面组件、样式类以及脚本代码，旨在帮助网页设计师快速构建出既充满专业感，又显得精致美观的网页（包括基于网页技术的Web应用程序界面）。目前，Bootstrap框架被广泛用于各种主流的Web应用中，例如Bing、LinkedIn、Instagram、Pinterest、Reddit、StackOverflow等，该框架在网页设计领域的最大竞争优势来自于以下几个方面：

- Bootstrap框架对响应式布局的强大支持。通过在项目中引入该框架，设计师们可以非常轻松地设计出能自动适应不同屏幕尺寸的网页，这将有助于提供更好的用户体验。在移动设备越来越普及的今天，响应式布局已经成为了Web开发的标配，Bootstrap框架的出现为开发者提供了一个快速实现响应式布局的工具。

- Bootstrap框架提供了丰富的用户界面组件和JavaScript插件（如导航栏、表格、表单、模态框等），这些组件和插件都经过了精心的设计和优化，能在不同的显示设备和浏览器上保持一致的显示效果，可以帮助设计师们轻松、快速地构建出各种常见的界面元素，这将大大提高他们的工作效率。除了现成的界面组件和JavaScript插件外，Bootstrap框架还支持自定义主题和样式，开发者可以根据自己的需求进行定制，从而实现更加个性化的界面设计。

- Bootstrap框架的开发者们还为初学者提供了详细的文档、丰富的示例代码以及完善的社区支持，这些资源都极大地平缓了该框架的学习曲线，使得人们快速掌握该框架的使用方法，这也是笔者在这里大力推荐读者基于 Bootstrap框架来学习网页设计的原因之一。

总而言之，Bootstrap框架是一款功能强大、易用性高、可扩展性强的前端开发框架，它为网页设计师们提供了快速构建响应式布局和常见Web界面元素的工具，极大地提高了开发效率和用户体验。如果读者想成为一名前端开发者，Bootstrap框架绝对是你应该要学习的工具之一。下面，就让我们根据网页设计工作中不同的任务主题来具体介绍一下该框架的使用方法。

## 页面整体设计

正如我们在上一节中所说，Bootstrap框架之所以如此受到欢迎，主要因为它提供了大量可重用的界面组件和CSS样式，这些组件和样式可以帮助设计师们快速有效地完成网页的整体设计任务。具体来说，Bootstrap框架在网页整体设计方面可以提供的便利主要如下：

- 它提供了大量的预定义样式，能够帮助网页设计师快速完成网页的整体布局。
- 它提供了大量的预定义模板，能够帮助网页设计师快速选择网页的配色方案。
- 它提供了大量的预定义组件，能够帮助网页设计师快速构建网页中要使用的界面元素。
- 它采用了基于移动设备优先的策略，能够帮助网页设计师快速实现网页的响应式布局。

例如在考虑网页的整体布局时，Bootstrap框架为我们提供了以下几种常见的布局样式：

1. **固定宽度布局**：如果要采用这种布局样式，设计师需要使用`container`类来为网页内容提供了一个中心对齐且具有固定宽度的容器。这种容器会随着屏幕或视口尺寸的改变而调整其宽度。

2. **流体宽度布局**：如果要采用这种布局样式，设计师需要使用`container-fluid`类来为网页元素提供一个宽度为100%的容器，意味着它会占据其父元素或视口的整个宽度。

3. **响应式栅格布局**：如果要采用这种布局样式，设计师需要使用`container`和`row`这两个类来组织内容，然后在每个`row`类定义的页面元素中使用`col`类来安排更具体的网页内容。Bootstrap框架的栅格系统是一个强大的布局工具，它是响应式的，可以让网页自行适应不同视口尺寸。

4. **Flexbox布局**：Flexbox是一个独立的CSS布局模型，但Bootstrap框架已经整合了这种布局样式，提供了一系列与Flexbox相关的实用类（包括`d-flex`、 `justify-content-*`、 `align-items-*`等）。这种布局样式可以让设计师在一个容器内以更灵活的方式排列、对齐和分配子元素。与传统的浮动或定位方法相比，Flexbox提供了更多的控制和更简单的解决方案，特别是对于复杂的布局和对齐问题。

5. **组件布局**： Bootstrap框架还提供了许多组件，如导航栏、卡片、警报框等，读者可以使用这些组件来构建特定类型的布局。例如，你可以使用导航栏组件来创建一个具有导航功能的网站头部。

当然了，除了选择上面其中一种布局样式之外，读者还可以根据自己的具体需求灵活地混合使用这些样式，以便创建出更具复杂性的网页。Bootstrap框架的灵活性及其提供的丰富文档资源可以帮助我们轻松实现各种复杂的网页布局设计。接下来，让我们通过一个简单项目来为读者演示一下在项目中引入Bootstrap框架的具体步骤，以及如何基于该框架来完成网页的整体布局任务，项目的创建过程如下。

1. 在本地计算机中创建一个名为`HelloBootstrap`的文件夹，并在其中创建一个名为`index.htm`的网页文件和两个分别名为`styles`和`scripts`的子目录。

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

5. 在保存上述代码之后，读者就可以使用网页浏览器打开`index.htm`文件查看当前网页设计的结果，其外观样式在Google Chrome浏览器中的效果如图2-6所示。

    ![基于Bootstrap框架的网页布局示例](./img/2.png)

在上述示例中，我们首先在项目中引入了Bootstrap框架的CSS样式文件和JavaScript文件（以便能该框架提供的外观样式及其相关的功能），然后使用了该框架提供的样式类来完成网页的整体布局，并安排不同布局元素中的内容。关于页面内容的安排，我们会在后面的章节中做专门介绍，现在先来重点关注网页的整体布局和配色选择。在布局方面，我们在这里主要采用了组件布局和Flexbox布局两大类布局样式。其中，组件布局类的样式主要运用于导航栏区域，而在作为网页主要区域的章节区域中采用的则是Flexbox布局，具体说明如下：

- 在导航栏区域，我们使用`navbar`和`navbar-expand-lg`这两个类创建了一个响应式的`<nav>`元素。在该元素内部，`navbar-brand`类用于定义当前网页的Logo元素（包括图片与文字）。`navbar-nav`类和`nav-item`类用于创建导航栏中的链接列表元素。另外在响应式布局方面，我们还利用`navbar-toggler`类创建了一个按钮元素，当网页在小屏幕设备上被访问时它就会被显示出来，而导航链接列表将会被收起，只有当用户点击该按钮时它才会重新被展开或收起。为此，我们需要将导航栏中的链接列表放在一个由`collapse`和`navbar-collapse`这两个类创建的`<div>`元素中。除此之外，我们还为导航链接列表本身添加了一个`ms-auto`类，这也是Bootstrap的响应式工具类之一，它会在小屏幕设备上自动将导航链接移到另一侧，以适应屏幕宽度。

- 在章节区域，我们首先使用`d-flex`类创建了一个以`<div>`标记来定义的弹性容器，然后用该容器来完成相关页面元素的排列和定位。这里的`d-flex`类也是Bootstrap框架提供的一个响应式工具类，下面是关于该类的使用说明：
  - **Flex容器**：`d-flex`类被应用于一个HTML元素（通常是`<div>`），将其定义为Flex容器。这意味着该元素的子元素将遵循Flexbox规则进行排列和布局。
  - **子元素排列**：一旦一个元素被定义为Flex容器，它的直接子元素成为Flex项，这些项会在容器内自动排列。你可以使用Bootstrap框架提供的其他类来控制子元素的排列方式，例如`justify-content-*`和`align-items-*`类，用于水平和垂直对齐。
  - **弹性布局**：Flexbox布局提供了一种强大的方式来管理和调整元素之间的空间分配。使用`d-flex`类，你可以轻松实现弹性的网页布局，以适应不同屏幕尺寸和内容需求。
  - **适应性和响应性**：Flexbox是响应式布局的理想选择，因为它可以在不同屏幕尺寸下自动调整元素的排列和大小，无需使用媒体查询。这使得你可以更容易地创建适应各种设备的网页布局。

除了布局方面之外，网页的整体设计还包含了配色方案的选择。正如你在上述示例中所见，我们通常会使用`bg-*`、`text-*`和`border-*`这三组Bootstrap框架提供的样式类来制定网页的配色方案，这些样式类为设计师们提供了预定义的色彩方案，可以快速有效地设计出具有统一配色风格的网页。下面，我们就来详细介绍一下这三组样式类：

- `bg-*`样式类用于设置网页整体或者特定页面元素的背景颜色，它通常会为整个网页奠定基本的色彩基调。通过使用不同的背景颜色，设计师们可以清晰地划分出网页的不同区域，并给用户带来视觉上的层次感。这组样式类可能采用的颜色具体如下：
  - `bg-primary`类：通常为蓝色或绿色的背景；
  - `bg-secondary`类：通常为灰色或浅色的背景；
  - `bg-success`类：通常为绿色的背景；
  - `bg-danger`类：通常为红色的背景；
  - `bg-warning`类：通常为橙色的背景；
  - `bg-info`类：通常为浅蓝色或浅绿色的背景；
  - `bg-light`类：通常为白色或浅色的背景；
  - `bg-dark`类：通常为黑色或深色的背景；
  - `bg-transparent`类，用于设置透明的背景。
- `text-*`样式类用于设置网页中的文本类元素颜色，它可以使得文本内容在网页中更加突出和易于阅读。设计师们通常根据文本的重要性来选择不同的文本颜色，例如主要文本、次要文本、成功信息、警告信息等。这组样式类可能采用的颜色具体如下：
  - `text-primary`类：采用与`bg-primary`相同的文本颜色；
  - `text-secondary`类：采用与`bg-secondary`相同的文本颜色；
  - `text-success`类：采用与`bg-success`相同的文本颜色；
  - `text-danger`类：采用与`bg-danger`相同的文本颜色；
  - `text-warning`类：采用与`bg-warning`相同的文本颜色；
  - `text-info`类：采用与`bg-info`相同的文本颜色；
  - `text-light`类：采用与`bg-light`相同的文本颜色；
  - `text-dark`类：采用与`bg-dark`相同的文本颜色；
- `border-*`类用于设置网页中各页面元素的边框颜色，它可以让页面各元素之间更易于区分。设计师们可以利用边框颜色与背景颜色（或文本颜色）之间的相互配合来增强网页的视觉层次感。这组样式类可能采用的颜色具体如下：
  - `border-primary`类：采用与`bg-primary`相同的边框颜色；
  - `border-secondary`类：采用与`bg-secondary`相同的边框颜色；
  - `border-success`类：采用与`bg-success`相同的边框颜色；
  - `border-danger`类：采用与`bg-danger`相同的边框颜色；
  - `border-warning`类：采用与`bg-warning`相同的边框颜色；
  - `border-info`类：采用与`bg-info`相同的边框颜色；
  - `border-light`类：采用与`bg-light`相同的边框颜色；
  - `border-dark`类：采用与`bg-dark`相同的边框颜色；

当然了，上述示例中所做的只是使用Bootstrap框架进行网页整体设计的初体验，目的是让读者对该框架能有一个大致的了解。接下来，我们还将结合网页设计工作中的其他任务做更多更为复杂的布局演示，

## 图文信息排版

## 用户界面设计
