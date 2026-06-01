# 自动化打包工具：Webpack

这篇学习笔记将用于记录本人在学习 Webpack 打包工具过程中所编写的心得体会与代码示例。为此，我会在`https://github.com/owlman/study_note`项目的`Programming/Client-Server/Frameworks`目录下创建一个名为的`webpackjs`目录，并在该目录下设置以下两个子目录：

- `notes`目录用于存放 Markdown 格式的笔记。
- `examples`目录则用于存放笔记中所记录的代码示例。

## 学习规划

- 学习基础：
  - 掌握 HTML、CSS、JavaScript 相关的基础知识。
  - 掌握 Node.js 运行平台的基础知识。
  - 掌握 npm 包管理器的基本用法。
  - 了解 B/S 应用程序架构的基本原理。
- 学习资料：
  - 视频资料：
    - [webpack 前端配置](https://www.bilibili.com/video/BV1Ks411j714)
  - 线上文档：
    - [webpack 官方文档](https://www.webpackjs.com/concepts/)

## 为何需要打包

程序员们在构建应用程序的前端部分时往往会出于可重用性方面的考虑将用户界面划分成不同的组件来编写，我们将这种编程思路称为模块化编程。在模块化编程中，每个模块通常都会涉及到一段用于描述界面元素的 HTML 代码，这些 HTML 代码又会去分别加载一系列 JavaScript 代码、CSS 样式以及其他静态资源（包括图片、字体、视频等）。并且在许多情况下，这些代码、样式和资源还都分别被存储在不同类型的文件中，这些文件之间是存在着一定依赖关系的。这就带来了一个潜在的问题：即当 Web 浏览器或其他客户端在加载某个模块时，如果该模块中文件的加载顺序和速度因各种不同的客观条件而产生一些不可预测的状况，那么这些状况中的大部分都会给应用程序带来一些负面影响。如果想避免这些状况，程序员们就应该考虑先将这些模块压缩并打包成更便于加载的文件单元。

除了模块加载带来的隐患之外，Web 浏览器或其他客户端对 JavaScript 语言标准的支持程度也是一个不容忽视的问题。毕竟，如今依然还存在着大量的用户仍在使用比 IE9 更老旧的浏览器，这些浏览器是完全不支持 ES6 标准规范的。如果希望应用程序被更多的用户使用，我们也需要将使用 ES6 标准编写的 JavaScript 代码转译成符合更早期标准的、具有同等效果的代码。

在如今的 Vue.js 项目实践中，上面所讨论的模块打包和代码转译工作大多数时候是通过 Webpack 这个工具来完成的。Webpack 是一个基于 JavaScript 语言的现代化**前端打包工具**，它会尝试着在前端项目中各类型文件之间构建起一个依赖关系图，这个关系图很大程度上就体现了应用程序中各模块之间、以及模块内部文件之间存在的依赖关系。然后，Webpack 会负责将这些模块按页面加载的具体需求压缩并打包成一个或多个经过压缩过的文件，整个过程如下图所示[^1]。

![前端打包原理](https://img2023.cnblogs.com/blog/691082/202305/691082-20230530100626806-1544887002.png)

## 基本打包选项

接下来，就让我们以下面这个简单的`webpack.config.js`文件为例来说明一下使用 Webpack 打包一个 Vue.js 前端项目需要进行的基本配置吧。这个配置文件的内容如下：

```JavaScript
const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const config = {
    entry: {
        main: path.join(__dirname,'src/main.js')
    },
    output: {
        path: path.join(__dirname,'./public/'),
        filename:'js/[name]-bundle.js'
    },
    plugins:[
        new VueLoaderPlugin(),
        new HtmlWebpackPlugin({
            template: path.join(__dirname, 'src/index.htm')
        })
    ],
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.js$/,
                loader: 'babel-loader'
            },
            {
                test: /\.css/,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            }
        ]
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        }
    },
    mode: 'development'
};

module.exports = config;
```

正如读者所见，Webpack 的配置文件实际上是一个遵守 CommonJS 规范 JavaScript 文件，其中所有的配置工作都是通过定义一个名为`config`的 JSON 格式的数据对象来完成的。下面来详细介绍一下这个对象中定义的成员。

### `entry`成员：配置入口模块

在`config`对象中，`entry`成员通常是我们第一个要定义的配置选项，该选项主要用于指定对当前项目进行打包时的入口模块。换句话说，`entry`成员所配置的就是 Webpack 的输入选项，后者就是以该选项指定的模块为起点开始构建依赖关系图的。在该关系图的构建过程中，Webpack 会搜寻到项目中存在的所有模块，并确认这些模块内外存在的、直接或间接的依赖关系。另外，由于在许多情况下，项目的入口模块未必只有一个，所以`entry`成员可以有四种定义形式。首先是字符串形式，当我们确定项目自始至终只会存在单一入口模块时，`entry`成员就可以被直接被定义成一个字符串类型的值，其具体示例代码如下：

```JavaScript
const path = require('path');

const config = {
    entry: path.join(__dirname,'src/main.js')
    // 其他配置
};

module.export = config;
```

当然，以上这种配置方式只能应付一些极为简单的项目打包工作，我们在项目实践中并没有多少机会能用到它。下面再来看数组形式，当项目中存在多个入口模块，或者我们不确定项目今后会不会增加入口模块时，更好的选择是将`entry`成员定义成一个字符串数组，因为这样做不仅可以一次指定多个入口模块，也可以为今后增加入口模块预留接口，其具体示例代码如下：

```JavaScript
const path = require('path');

const config = {
    entry:  [
        path.join(__dirname,'src/main.js'),
        path.join(__dirname,'liba/index.js')
        // 其他入口模块
    ],
    // 其他配置
};

module.export = config;
```

`entry`成员的第三种定义形式是将它定义成一个 JSON 格式的数据对象。由于 Webpack 打包时是以 chunk 为单位来进行源码分割的，该单位在默认情况下是按照它读取到的 JavaScript 文件来进行划分的，这在我们从外部引入第三方源码时会带来一些没有必要的重复打包。如果想按照指定的业务逻辑对项目进行分 chunk 打包，也可以使用对象定义的语法来定义`entry`成员，其具体定义方式如下：

```JavaScript
const path = require('path');

const config = {
    entry:  {
        main: path.join(__dirname,'src/main.js'),
        liba: path.join(__dirname,'liba/index.js'),
        vendor: 'vue' 
        // 其他入口模块
    },
    // 其他配置
};

module.export = config;
```

在上述配置中，我们为`src/main.js`和`liba/index.js`这两个入口模块，以及 Vue.js 这个第三方框架源文件指定了分别相应的 chunk 名称。这样一来，我们就可以在后面搭配`optimization`选项的配置将自己开发的业务代码和从外部引入的第三方源码分离开来。毕竟第三方框架在被安装之后，源码基本就不再会发生变化了，因此如果能将它们独立打包成一个 chunk，这一部分的源码就不用再重复打包了，这有助于提高项目的整体打包速度。

最后，如果我们在配置入口模块时需要设计一些在运行时才能获得路径的动态逻辑，也可以将`entry`成员定义成函数形式。其具体示例代码如下：

```JavaScript
const path = require('path');

const config = {
    entry: function() {
        return new Promise(function(resolve) {
            // 在此处模拟一个异步调用
            setTimeout(function() {
                resolve(path.join(__dirname,'src/main.js'));
            }, 1000);
        });
    }
    // 其他配置
};

module.export = config;
```

需要特别说明的是，Webpack 在 4.0 之后的版本中新增了默认配置的机制，所以在使用最新版本的 Webpack 进行项目打包时，如果读者忘记了定义`config`对象的`entry`成员，Webpack 的输入选项会被配置为`./src`这个默认值。

### `output`成员：配置输出选项

在配置完 Webpack 的输入选项之后，接下来要配置的自然是输出选项了。在`config`对象中，Webpack 的输出选项是通过定义其`output`成员来配置的，主要用于指定 Webpack 在完成打包工作之后以何种方式产生输出文件。在 Webpack 4.0 发布之后，该选项的默认值为`./dist`。在通常情况下，`output`成员通常会被定义成一个 JSON 格式的数据对象，该对象主要包含了以下两个最基本的属性：

- **`filename`成员**：用于指定输出文件的名称；
- **`path`成员**：用于指定输出文件的存放路径。

下面来看一下`output`成员的基本定义形式，其具体示例代码如下：

```JavaScript
const path = require('path');

const config = {
    entry:  [ // 配置入口模块
        path.join(__dirname,'src/main.js'),
        path.join(__dirname,'liba/index.js')
    ],
    output: { // 配置输出文件
        filename: 'bundle.js',
        path: path.join(__dirname,'./public/')
    },
    // 其他配置
};

module.export = config;
```

需要注意的是，在配置输出选项时，`path`属性的值必须是一个绝对路径。另外，无论我们在`entry`成员中定义了几个入口模块，Webpack 根据上述配置产生的输出结果都是一个名为`bundle.js`的文件。如果想让 Webpack 根据指定的 chunk 名来产生不同文件名的输出结果，那就需要先在定义`entry`成员时为其指定 chunk 名称，然后再在定义`output`成员时将`filename`属性的值定义为`[name].js`。其具体示例代码如下：

```JavaScript
const path = require('path');

const config = {
    entry:  {
        main: path.join(__dirname,'src/main.js'),
        liba: path.join(__dirname,'liba/index.js')
    },
    output: {
        filename: '[name].js',
        path: path.join(__dirname,'./public/')
    },
    // 其他配置
};

module.export = config;
```

在上述配置中，`[name]`是一种作用类似于模板变量一样的占位符，它在打包过程中会被自动替换成我们在配置入口模块选项时指定的 chunk 名称。这样一来，Webpack 就会在`./public/`目录下分别产生出`main.js`和`liba.js`这两个输出文件。除了`[name]`之外，我们还可以使用`[id]`、`[chunkhash]`等其他占位符来更详细地定义输出文件的名称。

### `module`成员：配置预处理器

正如我们在 6.1.1 节中所说，Webpack 的工作除了对项目中的源码文件进行压缩打包之外，另一个作用就是将这些源码文件中的部分代码进行转译。这部分工作要针对的模板既包含了之前提到的、使用 ES6 标准来编写的 JavaScript 文件，也包含了 CSS、XML、HTML、PNG 等其他各种类型的文件。 在 Webpack 中，代码的转译工作是通过一个名叫**预处理器（loader）**的机制来完成的。在这里，预处理器可以被视为 Webpack 从外部引入的转译器组件，我们可以利用这种转译器组件处理一些非 JavaScript 类型的文件，以便可以在 JavaScript 代码中使用`import`语句导入一些非 JavaScript 模块。简而言之就是，在使用预处理器之前，项目中只有 JavaScript 文件才会被视为是模块，而在使用了预处理器之后，项目中的所有文件都可被视为模块。当然，为了让 Webpack 识别不同类型的模块，我们需要从外部引入相应类型的预处理器组件。在一个 Vue.js 项目中，我们通常需要引入以下最基本的预处理器组件：

- `css-loader`：用于将 CSS 文件中的代码转译成符合 CommonJS 规范的 JavaScript 代码。
- `style-loader`：用于将`css-loader`产生的转译结果进一步转译成 HTML 中的`<style>`标签。
- `babel-loader`：用于将使用 ES6 标准编写的代码转译成符合早期标准的 JavaScript 代码。
- `vue-loader`：用于将 Vue 专用文件中的代码转译成普通的 JavaScript 代码。

除此之外，如果项目中还包含了对图片文件的处理，就还需要用到`file-loader`、`url-loader`等预处理器。当然了，这些组件都需要通过在项目的根目录下执行`npm install <组件名> --save-dev`命令来将它们安装到项目中。待一切安装完成之后，我们就可以来配置这些预处理器了。在`config`对象中，配置预处理器是通过定义`module`成员的`rules`属性来完成的。该`rules`属性是个数组类型的对象，其中的每个元素对象都代表着一个指定类型的文件所要使用的预处理器，通常需要配置以下两个基本属性：

- `test`属性：该属性是一个正则表达式，主要用于以文件扩展名的方式来指定待处理目标的文件类型。
- `use`属性：该属性用于由`test`属性所指定的类型文件应该使用的预处理器。

下面是一个最基本的 Vue.js 项目的预处理器配置：

```JavaScript
const path = require('path');

const config = {
    entry:  {
        main: path.join(__dirname,'src/main.js'),
        liba: path.join(__dirname,'liba/index.js')
    },
    output: {
        filename: '[name].js',
        path: path.join(__dirname,'./public/')
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.js$/,
                loader: 'babel-loader'
            },
            {
                test: /\.css/,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            }
        ]
    }
    // 其他配置
};

module.export = config;
```

在某些情况下，对于一些特殊类型的文件，我们还可以使用多个预处理器来对它进行转译。例如在处理 CSS 样式文件时，`css-loader`只能将它转译成符合 CommonJS 规范的 JavaScript 代码，使我们可以在 JavaScript 代码中使用`import Styles from './style.css'`这样的语句将名为`style.css`的 CSS 文件作为一个模块导入。但如果我们想让这个模块中定义的样式真正产生效果，还需要用`style-loader`将其转译成内嵌到 HTML 文件中的`<style>`标签才行。为相同类型的文件配置多个预处理器的方式也非常简单，只需要将`use`属性设置为一个可列举预处理器名称的数组即可。Webpack 会按照数组中设定的先后顺序来递归地进行转译工作。

### `plugins`成员：配置插件选项

预处理器只能负责将一些 ES6 模块或非 JavaScript 类型的文件转换成符合早期标准的 JavaScript 模块。但如果想让 Webpack 在打包过程中执行一些更复杂的任务，就需要用到它更为灵活的插件机制了。例如在基于 Vue.js 框架的项目实践中，程序员们通常会选择将应用程序的源码保存在`src`这样的源码目录中，然后再由 Webpack 根据源码目录中的 HTML 模板、Vue 组件以及一般性的 JavaScript 脚本来产生真正要部署在服务器上的应用程序，后者通常会被保存在`dist`或`public`这样的产品目录中。在这种情况下。Webpack 的输出结果中就不只有 JavaScript 文件了。其中至少还会包含已经引入了打包结果之后的 HTML 页面。而 HTML 页面的输出并不是 Webpack 本身具备的功能，在之前的示例配置中。这部分的功能是依靠`HtmlWebpackPlugin`插件来实现的。下面我们就以该插件为例来介绍一下如何配置 Webpack 的插件，其基本步骤如下：

1. 和预处理器一样。在使用`HtmlWebpackPlugin`插件之前，我们也需要在项目的根目录下执行`npm install html-webpack-plugin --save-dev`命令，以便将该插件安装到项目中。

2. 在安装完插件之后，我们需要使用 CommonJS 规范将`HtmlWebpackPlugin`插件作为一个对象类型引入到`webpack.config.js`配置文件中，具体做法就是在文件的开头加入如下语句：

   ```JavaScript
    const HtmlWebpackPlugin = require('html-webpack-plugin');   
   ```

3. 在`config`对象中，我们是通过定义其`plugins`成员来进行插件配置的。该成员的值是个数组类型的对象，其中的每个元素对象都代表着一个插件，我们可以通过`new`操作符来创建`HtmlWebpackPlugin`插件对象，其具体代码如下：

   ```JavaScript
    const path = require('path');
    const HtmlWebpackPlugin = require('html-webpack-plugin');

    const config = {
        entry: {
            main: path.join(__dirname,'src/main.js')
        },
        output: {
            path: path.join(__dirname,'./public/'),
            filename:'js/[name]-bundle.js'
        },
        plugins:[
            new HtmlWebpackPlugin({
                template: path.join(__dirname, 'src/index.htm')
            })
        ]
        // 其他配置
    };

    module.exports = config;   
   ```

在上述配置中，我们在创建`HtmlWebpackPlugin`插件实例时还通过`template`参数为其指定了模板文件。这样一来，Webpack 就会根据`src`目录下的`index.htm`文件来产生输出到`public`目录中的 HTML 页面了。另外，如果项目中有多个 HTML 页面要输出，解决方案也非常简单，就是在`plugins`成员中创建相应数量的`HtmlWebpackPlugin`插件实例，其示例代码如下：

```JavaScript
plugins: [
    new HtmlWebpackPlugin({
        filename: 'index.html',
        template: path.join(__dirname, 'src/index.htm')
    }),
    new HtmlWebpackPlugin({
        filename: 'list.html',
        template: path.join(__dirname, 'src/list.htm')
    }), 
    new HtmlWebpackPlugin({
        filename: 'message.html',
        template: path.join(__dirname, 'src/message.htm')
    })
]
```

在上述插件配置中，我们创建了三个`HtmlWebpackPlugin`插件实例，它们会在`public`目录中分别输出`index.html`、`list.html`和`message.html`这三个 HTML 页面。正如读者所看到的，我们这一次在创建`HtmlWebpackPlugin`插件实例时，除了使用`template`参数指定输出页面的模板文件之外，还用`filename`参数指定了输出页面的文件名。当然，如果还想对输出页面进行更多的设置。我们还可能会需要用到下面这些常用参数。

- `title`: 该参数用于生成输出页面的标题。其作用就相当于在输出页面在插入这样一个带模板语法的`<title>`标签：

  ```HTML
   <title>(( o.htmlWebpackPlugin.options.title }}</title>
  ```

- `templateContent`: 该参数用于以字符串或函数的形式指定输出页面的 HTML 模板，当该参数被配置为函数形式时，它既可以直接返回模板字符串，也可以用异步调用的方式返回模板字符串。需要注意的是，该参数不能与`template`同时出现在`HtmlWebpackPlugin`对象的构造函数调用中，我们必须在两者之间二选一。

- `inject`：该参数用于指定向由`template`或`templateContent`指定的 HTML 模板中插入资源引用标签的方式，它主要有以下三种配置：
  - `true`或`body`：将资源引用标签插入到`<body>`标签的底部。
  - `head`: 将资源引用标签插入到`<head>`标签中。
  - `false`： 不在 HTML 模板中插入资源引用标签。

需要说明的是，以上列出的只是`HtmlWebpackPlugin`插件中一部分常用的配置参数，如果读者想更全面地了解创建该插件时可以使用的所有参数，可以自行查阅`HtmlWebpackPlugin`插件的官方文档[^2]。由于我们在这里只是借用该插件来介绍配置 Webpack 插件的基本步骤，出于篇幅方面的考虑，就不进一步展开讨论了。当然，除了用于输出 HTML 页面的`HtmlWebpackPlugin`插件之外，在 Vue.js 项目中可能还会用到其他功能的插件。下面，我们就来介绍几个常用的 Webpack 插件：

- **`VueLoaderPlugin`插件**：该插件的主要作用是将我们挚爱其他地方定义的规则复制并应用到`vue`专用文件里相应语言的标签中。例如在下面的示例中，我们用于匹配`/\.js$/`的规则也将会被应用到`vue`文件里的`<script>`标签中。这意味着，该标签中使用 ES6 标准编写的代码也会被 babel-loader 预处理器转译：

  ```JavaScript
    const path = require('path');
    const VueLoaderPlugin = require('vue-loader/lib/plugin');
    const HtmlWebpackPlugin = require('html-webpack-plugin');

    const config = {
        entry: {
            main: path.join(__dirname,'src/main.js')
        },
        output: {
            path: path.join(__dirname,'./public/'),
            filename:'js/[name]-bundle.js'
        },
        plugins:[
            new VueLoaderPlugin(),
            new HtmlWebpackPlugin({
                template: path.join(__dirname, 'src/index.htm')
            })
        ],
        module: {
            rules: [
                {
                    test: /\.vue$/,
                    loader: 'vue-loader'
                },
                {
                    test: /\.js$/,
                    loader: 'babel-loader'
                }
                // 其他预处理器配置
            ]
        }
        // 其他配置
    };

    module.exports = config;
  ```

- **`CleanWebpackPlugin`插件**：该插件主要用于在打包工作开始之前清理上一次打包产生的输出文件，它会根据我们在`output`成员照中配置的`path`属性值自动清理文件夹，其具体示例代码如下：

   ```JavaScript
    const path = require('path');
    const HtmlWebpackPlugin = require('html-webpack-plugin');
    const { CleanWebpackPlugin } = require('clean-webpack-plugin');

    const config = {
        entry: {
            main: path.join(__dirname,'src/main.js')
        },
        output: {
            path: path.join(__dirname,'./public/'),
            filename:'js/[name]-bundle.js'
        },
        plugins:[
            new HtmlWebpackPlugin({
                template: path.join(__dirname, 'src/index.htm')
            }),
            new CleanWebpackPlugin()
        ]
        // 其他配置
    };

    module.exports = config;   
   ```

- **`ExtractTextPlugin`插件**：该插件主要用于在打包时产生出独立的 CSS 样式文件，从而避免因将样式代码打包在 JavaScript 代码中而可能引起的样式加载错乱现象，其具体示例代码如下：

   ```JavaScript
    const path = require('path');
    const HtmlWebpackPlugin = require('html-webpack-plugin');
    const ExtractTextPlugin = require('extract-text-webpack-plugin');

    const config = {
        entry: {
            main: path.join(__dirname,'src/main.js')
        },
        output: {
            path: path.join(__dirname,'./public/'),
            filename:'js/[name]-bundle.js'
        },
        plugins:[
            new HtmlWebpackPlugin({
                template: path.join(__dirname, 'src/index.htm')
            }),
            new ExtractTextPlugin(
                path.join(__dirname, 'src/styles/main.css')
            )
        ]
        // 其他配置
    };

    module.exports = config;   
   ```

- **`PurifyCssWebpack`插件**：该插件主要用于清除指定文件中重复或多余的样式代码，以减少打包之后的文件体系，其具体示例代码如下：

   ```JavaScript
    const path = require('path');
    const glob = require('glob');
    const HtmlWebpackPlugin = require('html-webpack-plugin');
    const PurifyCssWebpack = require('purifycss-webpack');

    const config = {
        entry: {
            main: path.join(__dirname,'src/main.js')
        },
        output: {
            path: path.join(__dirname,'./public/'),
            filename:'js/[name]-bundle.js'
        },
        plugins:[
            new HtmlWebpackPlugin({
                template: path.join(__dirname, 'src/index.htm')
            }),
            new PurifyCssWebpack({
                paths: glob.sync(path.join(__dirname, 'src/*.htm')),
            })
        ]
        // 其他配置
    };

    module.exports = config;   
   ```

- **`CopyWebpackPlugin`插件**：在默认情况下，webpack 在打包时是不会将我们在`src`源码目录中使用的图片等静态资源复制到输出目录的，该插件能够很好地完成这方面的工作，其具体示例代码如下：

   ```JavaScript
    const path = require('path');
    const HtmlWebpackPlugin = require('html-webpack-plugin');
    const CopyWebpackPlugin = require('copy-webpack-plugin')

    const config = {
        entry: {
            main: path.join(__dirname,'src/main.js')
        },
        output: {
            path: path.join(__dirname,'./public/'),
            filename:'js/[name]-bundle.js'
        },
        plugins:[
            new HtmlWebpackPlugin({
                template: path.join(__dirname, 'src/index.htm')
            }),
            new CopyWebpackPlugin({
                patterns: [{
                    from: path.join(__dirname, 'src/img/*.png'),
                    to: path.join(__dirname, 'public/img', 'png'),
                    flatten: true
                }]
        ]
        // 其他配置
    };

    module.exports = config;   
   ```

### `resolve`成员：配置路径解析

另外，如果我们觉得每次使用`import`语句引入 Vue.js 框架时都需要手动输入`vue.esm.browser.js`这么长的文件名（况且还包含路径）是一件非常麻烦的事情，那么就可以通过定义`config`对象的`resolve`成员来简化一下框架文件的引用方式。例如，我们可以通过`resolve`成员的`alive`属性为该框架文件设置一个别名，具体代码如下：

```JavaScript
const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const config = {
    entry: {
        main: path.join(__dirname,'src/main.js')
    },
    output: {
        path: path.join(__dirname,'./public/'),
        filename:'js/[name]-bundle.js'
    },
    plugins:[
        new VueLoaderPlugin(),
        new HtmlWebpackPlugin({
            template: path.join(__dirname, 'src/index.htm')
        })
    ],
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.js$/,
                loader: 'babel-loader'
            },
            {
                test: /\.css/,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            }
        ]
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        }
    }
};

module.exports = config;
```

需要留意的是，由于 Webpack 的打包工作是在程序员所在的开发环境中进行的，所以这里引用的应该是`vue.esm.js`文件，而不是直接在浏览器中使用的`vue.esm.browser.js`文件。在完成上述配置之后，我们在 JavaScript 代码中就可以直接使用`import Vue from 'vue'`语句来引入 Vue.js 框架了，这既大大增加了代码的整洁度，也降低了程序员输入出错的概率。

### `mode`成员：配置打包模式

最后，我们还需要通过定义`config`对象的`mode`成员来配置一下 Webpack 所要采用的打包模式。Webpack 主要有生产环境模式（`mode`的值为`production`）和开发环境模式（`mode`的值为`development`）两种打包模式。这两种模式之间的主要区别是，在生产环境模式下，Webpack 会自动对项目中的代码文件采取一系列优化措施，这可以免除程序员们许多手动调整配置的麻烦。例如在下面的配置中，我们将项目的打包模式设置成了生产环境模式：

```JavaScript
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

const config = {
    entry: {
        main: path.join(__dirname,'src/main.js')
    },
    output: {
        path: path.join(__dirname,'./public/'),
        filename:'js/[name]-bundle.js'
    },
    plugins:[
        new HtmlWebpackPlugin({
            template: path.join(__dirname, 'src/index.htm')
        }),
        new CleanWebpackPlugin()
    ],
    // 其他配置
    mode: 'production'
};

module.exports = config;   
```

## 实现自动化打包

在掌握了上述基本打包选项之后，我们就可以利用 Webpack 完成一般性的前端项目打包工作了。接下来要做的就是对我们的开发环境做一些基本的配置，以实现打包工作的自动化，从而让前端项目的开发、测试和部署工作更为便捷、高效。该配置工作的基本步骤如下：

### 项目环境配置

1. 创建一个用于演示 Webpack 打包配置的前端项目，项目的位置和名称可以任意，我们在这里将其命名为`webpackDemo`。该项目的初始结构设置如下：

   ```bash
    ├───src
    |   ├───index.htm
    |   ├───main.js
    |   └───sayHello.vue
    └───public
   ```

2. 使用`npm init -y`初始化项目，并在项目根目录下执行`npm install vue-loader --save-dev`等命令，将要用到的预处理器和插件安装到项目中。

3. 在项目该目录下执行`npm install webpack webpack-cli --save-dev`命令，将 Webpack 工具安装到项目中：

4. 在项目根目录下创建`webpack.config.js`文件，并根据之前所学知识配置 Webpack 打包选项，例如：

   ```JavaScript
    const path = require('path');
    const VueLoaderPlugin = require('vue-loader/lib/plugin');
    const HtmlWebpackPlugin = require('html-webpack-plugin');
    const { CleanWebpackPlugin } = require('clean-webpack-plugin');

    const config = {
        mode: 'development',
        entry: {
            main: path.join(__dirname,'src/main.js')
        },
        output: {
            path: path.join(__dirname,'./public/'),
            filename:'js/[name]@[chunkhash].js'
        },
        plugins:[
            new VueLoaderPlugin(),
            new HtmlWebpackPlugin({
                template: path.join(__dirname, 'src/index.htm')
            }),
            new CleanWebpackPlugin()
        ],
        module: {
            rules: [
                {
                    test: /\.vue$/,
                    loader: 'vue-loader'
                },
                {
                    test: /\.js$/,
                    loader: 'babel-loader'
                },
                {
                    test: /\.css/,
                    use: [
                        'style-loader',
                        'css-loader'
                    ]
                }
            ]
        },
        resolve: {
            alias: {
                'vue$': 'vue/dist/vue.esm.js'
            }
        }
    };

    module.exports = config;
   ```

5. 在项目根目录下将`package.json`文件中的`scripts`选项修改如下：

   ```JSON
    "scripts": {
        "build": "webpack"
    }
   ```

到这一步，我们就已经可以在项目的根目录下执行`npm run build`命令来使用 webpack-cli 了，该命令在终端中的执行效果如下：

![webpack-cli执行效果](https://img2023.cnblogs.com/blog/691082/202305/691082-20230530100856094-60372982.png)

### 开发环境配置

如果读者觉得在开发环境中，每次修改代码之后都要重新手动执行`npm run build`命令是一件效率过低的事，我们还可以在`webpack.config.js`配置文件中为`config`对象添加一个名为`devtool`成员，并将成员的值配置为`source-map`或`inline-source-map`，打开 source maps 选项，然后就可以用两种方式来进一步实现打包的自动化：

**方法 1，启用 webpack-cli 工具的`watch`模式**：

开启该模式的具体做法就是在项目根目录下修改`package.json`文件中的`scripts`选项，为 webpack 命令加上`--watch`参数，像这样：

```JSON
"scripts": {
    "build": "webpack --watch"
}
```

这样一来，当我们再使用 webpack-cli 进行打包时，该工具就开启了`watch`模式，在该模式下，一旦项目依赖关系图中的任意模块发生了变化，webpack-cli 工具就会自动对项目进行重新打包。

**方法 2，搭建 webpack-dev-server 服务器**：

该服务器不仅会在打包之后自动调用 Web 浏览器打开我们正在开发的应用程序，而且一旦检测到项目依赖关系图中的文件发生了变化，就会项目进行重新打包，并命令浏览器重新载入应用程序，基本实现了所见即所得的开发体验。下面，就让我们来具体介绍一下搭建 webpack-dev-server 服务器的基本步骤：

- 在项目根目录下执行`npm install webpack-dev-server --save-dev`命令将服务器组件安装到项目中。

- 在`webpack.config.js`配置文件中为`config`对象添加一个名为`devServer`成员，并将成员的`contentBase`值配置如下：

    ```JavaScript
    const path = require('path');
    // 引入其他模块

    const config = {
        // 其他配置选项
        devServer: {
           contentBase: path.join(__dirname,'./public/')
        }
    };

    module.exports = config;
   ```

- 在项目根目录下将`package.json`文件中的`scripts`选项修改如下：

   ```JSON
    "scripts": {
        "build": "webpack --watch",
        "start": "webpack-dev-server --open"
    }
   ```

在完成上述配置之后，读者只需要在项目根目录下执行`npm run start`命令就可以启动 webpack-dev-server 服务器了。如果服务器的启动过程“一切正常”，我们就会看到 Web 浏览器自动打开了应用程序，然后可以继续试探性地修改一些代码，并查看浏览器中的内容是否如自己期待的那样进行了实时更新。当然，“一切正常”的前提是这里所使用的 webpack-dev-server 服务器与我们安装的 webpack-cli 在版本上是相匹配的，毕竟截止到作者撰写本章内容的这一刻，该服务器还不能支持最新版本的 webpack-cli。一旦遇到了这种情况，我们就需要在安装 webpack 和 webpack-cli 时为其指定与 webpack-dev-server 服务器相匹配的版本，指定的方式非常简单，只需要在安装命令中输入版本信息即可，例如像这样：

```bash
npm install webpack@4.39.2 --save-dev
npm install webpack-cli@3.3.12 --save-dev
```

当然了，上述演示操作所构建的是一个最基本的 webpack-dev-server 服务器，我们还可以在`config`对象的`devServer`成员中为该服务器定义更详细的配置信息，例如指定服务器使用的端口、是否开启热更新模式等等，如果读者想详细了解这些配置的作用和具体定义方法，可以自行查阅 webpack-dev-server 服务器的官方文档[^3]。

<!-- 以下为注释区 -->

[^1]: 该图出自Webpack中文网：`https://www.webpackjs.com/`。
[^2]: `HtmlWebpackPlugin`插件官方文档：`https://github.com/jantimon/html-webpack-plugin#configuration`。
[^3]: webpack-dev-server服务器组件的中文文档：`https://www.webpackjs.com/configuration/dev-server/`。

----
#已完成
