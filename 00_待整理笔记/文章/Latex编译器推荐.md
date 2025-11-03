### 前言：

**大家平时用的最多的排版工具想必就是Microsort的Word或者WPS了，所见即所得，Latex是另外一种排版工具，需要编译才可以生成pdf。相信大家在投稿的时候，会发现很多杂志都提供的tex template。**

**至于Latex好还是word好，这个已经有很多讨论了，不在此多讨论。简单说下，Natue Science不会因为你是word还是latex排版拒绝你。Latex的主要优势是：如果Latex命令掌握非常熟练，在排版公式非常多的论文或者书籍时，比word要快速、稳定、美观的多。**

**在Latex命令还没那么熟的时候，你还是需要一个编译器的，就像你学习Python的时候，一般会选择Pycharm或者VS code来辅助你一样。Latex也有很多不同的编译器。这个在知乎上（[https://www.zhihu.com/question/19954023](https://www.zhihu.com/question/19954023 "https://www.zhihu.com/question/19954023")）和Wiki上（[https://en.wikipedia.org/wiki/Comparison\_of\_TeX\_editors](https://en.wikipedia.org/wiki/Comparison_of_TeX_editors "https://en.wikipedia.org/wiki/Comparison_of_TeX_editors")）已经有好多讨论了。截一个wiki的图。**

![Tex editor.jpg](https://i-blog.csdnimg.cn/img_convert/2963e8deed0bd5194f38bb5e549b6d3d.jpeg)

加上知乎里面推荐的VScode、vim、Notepad++ Emacs等等，可谓琳琅满目。每一个都不能说不好，各有特点。对于初学者或者不太愿意折腾各种配置的朋友来说。

#### 一、Tex环境或者发行版一般就两个比较常用： 

    1.Texlive，2.Miktex。

Texlive包比较全，Miktex占用空间比较小，遇到需要的包需要在线下载。所以，硬盘空间比较充足的，网络不太方便的电脑，可以选择Texlive，反之硬盘空间小，一直保持网络链接的可以选择Miktex。我一直用MiKtex，相对比较灵活小巧。

![v2-12a0e2fc02c7714a3796d0f67cb73fb1_1200x500 (1).jpg](https://i-blog.csdnimg.cn/img_convert/735fe1ebc915f75ebc060c995cd08aca.jpeg)

![basic-miktex-finish.png](https://i-blog.csdnimg.cn/img_convert/e8628d9342fcf8c0981f8c8e922b282d.png)

#### 二、Tex editor （Tex编译器）的选择。

1、首选Winedt（非免费，试用30天），界面比较友好，提示做的也比较好，毕竟是要花钱的软件。

![](https://i-blog.csdnimg.cn/img_convert/43a2c206d9c5cb549b50a6b7bee9ed2f.jpeg)

![WinEdt-TeX.png](https://i-blog.csdnimg.cn/img_convert/1f3fb246dbebeb2ac99240d23072b603.png)

其次也可以选择Texmaker（[Texmaker (free cross-platform latex editor)](https://www.xm1math.net/texmaker/ "Texmaker (free cross-platform latex editor) ")）或者Kile（[Kile - an Integrated LaTeX Editing Environment](https://kile.sourceforge.io/ "Kile - an Integrated LaTeX Editing Environment")），都是免费，这两个的操作界面竟然安装好以后直接就是中文，这点比Winedt还友好，只不过用户用的比较少。大家可以试试。  

![](https://i-blog.csdnimg.cn/img_convert/c829073639df97244292ca12cef456ce.jpeg)

                                      Texmaker 截图

![](https://i-blog.csdnimg.cn/img_convert/3f1f2820f90f85f01a4de6cb76455c9a.jpeg)

                             Kile 截图

#### 三、[Texstudio](https://so.csdn.net/so/search?q=Texstudio&spm=1001.2101.3001.7020)

特别提醒的是，Texstudio这个编译器，还是很强大的，也很友好，国际范围内，使用的人也很多，推荐在Linux下工作的朋友使用，Windows下就算了，非常丑陋不说，如果遇到高分辨率的显示器，也会出现工具栏过小或者模糊的问题。

总结一下：对于初学者来讲可以选择Winedt+Miktex（Texlive）的组合，也可以尝试Texmaker+Miktex（Texlive），或者Kile + Miktex（Texlive）。Win10特别是显示器是高分辨率的朋友，其他的可以暂时不用试了，都有这样那样的问题，这几个比较有好些。等把这几个玩熟了再去折腾知乎上推荐的那些吧。