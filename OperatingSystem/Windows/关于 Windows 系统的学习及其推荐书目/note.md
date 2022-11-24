# 关于 Windows 系统的学习及其推荐书目

众所周知，在我们日常工作和生活中所接触到的个人计算机中，除了少数人使用的以 macOS 为操作系统的 Mac 系列设备之外，大部分人使用的都是以 Windows 为主要操作系统的 IBM PC。因此，如果你是一个面向中国市场的程序员，学习和研究基于 Windows 系统来开发设备驱动和应用程序将是一个绕不过去的课题。而想要在这一领域获得可长可久的生产力，我们自然需要深入地 Windows 系统本身的各种运行机制和设计思想。在本文接下来的内容中，我们将会以推荐书目的形式来为读者规划一个研究 Windows 系统内核及其应用层开发的学习路线图，以供参考。

## Windows 内部机制研究

Windows 9x系列
主条目：Windows 9x、Windows 95、Windows 98和Windows Me

Windows 9x是Windows 95、Windows 98、Windows Me等以Windows 95内核作为参考的微软操作系统通称，与Windows NT分离于两个开发路线。它是一种多任务图形方式的操作系统。

Windows 9x仍然需要依赖16位的DOS基层程序才能运行，不算是真正意义上的32位操作系统，由于使用DOS代码，架构也与16位DOS一样，核心属于单核心，但也引入了部分32位操作系统的特性，具有一定的32位的处理能力。Windows 9x可视为微软将MS-DOS操作系统与早期Windows图形用户界面集成出售。

Windows 95在1995年8月24日正式发布，作为继Windows 3.x后的下一代消费级Windows。尽管仍然以MS-DOS为基础，Windows 95引入了对32位程序、即插即用硬件、抢占式多任务处理、长文件名等功能的支持，并提供更高的稳定性。与此同时，Windows 95引入了全新的、对象化的用户界面设计，用“开始”菜单、任务栏、Windows资源管理器等全新组件取代了之前的程序管理器。Windows 95是微软历史上的一次巨大商业成功。CNET的Ina Fried评价道：“当Windows 95终于在2001年走下市场时，它已然牢牢地钉在了全世界的电脑上。”[24]此外，微软的网页浏览器Internet Explorer首度与Windows捆绑发行。[25]

Windows 98随后于1998年6月25日发布，引入了Windows Driver Model、USB通用设备、ACPI、休眠、多显示器等功能和硬件的支持。Internet Explorer 4还通过活动桌面和Windows桌面更新集成到了Windows 98。1999年5月，Windows 98的更新版本Windows 98 SE（Second Edition，第二版）发布。Windows 98 SE包括Internet Explorer 5.0和Windows Media Player 6.2以及其他升级。

Windows Me（Millennium Edition）发布于2000年9月14日，它是最后一代基于DOS的Windows。Windows Me借鉴了Windows 2000的外观，启动速度较前几代都更快（代价是失去了访问实模式DOS环境的能力，及一些旧程序的兼容性）[26]，增强了多媒体功能（包括 Windows Media Player 7、Windows Movie Maker和用于从扫描仪和数字相机检索图像的Windows Image Acquisition框架）并新增了诸如系统文件保护、系统恢复以及家庭网络工具等功能[27]。不过，Windows Me的运行速度和不稳定性，硬件兼容性问题以及取消对实模式DOS的支持而广受诟病，《个人电脑世界》杂志认为Windows Me是微软历史上最糟糕的一代系统，也是有史以来第四差的科技产品。[28]Windows Me 也经常被戏称为 Windows Mistake Edition。
Windows NT系列
主条目：Windows NT

不同于依然需要DOS基层程序的混合16/32位的Windows 9x，Windows NT系列采用的是重新设计的Windows NT核心，属于混合式核心。最早仅支持纯32位，后期加入了对64位的支持。

32位Windows NT系统包括：[注 7]

    Windows NT 3.1
    Windows NT 3.5
    Windows NT 3.51
    Windows NT 4.0
    Windows 2000
    32位 Windows XP
    32位 Windows Vista
    32位 Windows 7
    32位 Windows 8
    32位 Windows 8.1
    32位 Windows 10
    32位 Windows Server 2003/2003R2/2008

64位Windows NT系统，分为支持于IA-64架构和x64架构的两种不同版本。在历史上微软曾对两种不同的64位架构提供支持，其一是英特尔公司和惠普公司联合开发具有革新化的Itanium家族架构，或称之为IA-64；和AMD公司开发的演进化的x86-64架构。由于两种架构的核心设计思想不同，因此两种架构的操作系统和应用软件不具有互通性，但都对传统的IA-32架构的软件一定程度上提供支持。微软在发布Windows Server 2012 R2前放弃了对Itanium架构的支持。因此现在微软的64位产品指的单单是x86-64架构，而在微软的词汇中称为x64。

支持Itanium家族架构的微软Windows产品有：

    Windows 2000 Advanced/Datacenter Server Limited Edition
    Windows XP 64-bit Edition
    Windows XP 64-bit Edition Version 2003
    Windows Server 2003/2003 R2 Enterprise/Datacenter
    Windows Server 2008/2008 R2 for Itanium Based System

支持x64架构的Windows产品有：

    Windows XP Professional x64 Edition
    Windows Server 2003/2003R2全线产品（Web版除外）
    Windows Vista/7
    Windows Server 2008/2008R2/2012/2012R2全线产品
    Windows 8/8.1
    Windows 10
    Windows 11

下面以以发布时间为线索介绍。
早期版本（Windows NT 3.1/3.5/3.51/4.0/2000）
主条目：Windows NT 3.1、Windows NT 3.5、Windows NT 3.51、Windows NT 4.0和Windows 2000

1988年11月，一支新组建的微软团队（包括前DEC开发人员戴夫·卡特勒和马克·洛考夫斯基）开始开发IBM和微软的OS/2操作系统的改进版本“NT OS/2”。NT OS/2旨在设计为一个安全的、多用户的，支持POSIX、模块化的、可移植内核支持多种处理器架构的操作系统。然而，在Windows 3.0的成功后，团队决定重新着手开发称为Win32的Windows API的扩展32位接口，而不是OS/2的接口。Win32保持了与Windows API相似的结构（允许现有的Windows应用程序轻松移植到其他平台），又支持NT内核的功能。在征得微软同意后，这样的开发继续了下去，直到Windows NT诞生。但是，IBM反对这些更改，并最终独自继续开发OS/2。[29][30]

Windows NT首度基于混合核心运行。

初代的NT系统被命名为Windows NT 3.1（以和Windows 3.1相联系），于1993年7月发布，有用于工作站和服务器的版本。

Windows NT 3.5在1994年9月发布，专注于性能改进和对Novell的NetWare的支持。Windows NT 3.51在1995年5月发布，包括对PowerPC体系结构的额外改进和支持。Windows NT 4.0在1996年6月发布，向NT系列带来了Windows 95的用户界面设计。2000年2月17日，Windows 2000发布，自此之后NT系列不再保留“NT”的名称。[31]
Windows XP
主条目：Windows XP
参见：Windows XP版本列表

Windows NT的下一个大版本Windows XP于2001年10月25日正式发布。Windows XP的诞生旨在将Windows 9x的用户引入到Windows NT中，微软为此保证其将提供比DOS系列更好的性能和体验。Windows XP引入了经典的用户界面设计（其中包括了新版的“开始”菜单和面向任务的Windows浏览器）、流式传输的多媒体服务和Internet Explorer 6。[32]

在零售中，Windows XP分为两个主要的版本：家庭版（Home Edition）和专业版（Professional）。家庭版主要面向普通客户，而专业版面向商业客户和专业用户。之后也发行了媒体中心版（Media Center Edition，设计于家庭影院的电脑，拥有更强的影音功能）和平板电脑版（Tablet PC Edition，设计于可携带的平板电脑，支持手写笔输入等功能）。[33][34][35]
Windows Vista 和 Windows 7
主条目：Windows Vista和Windows 7

经历了漫长的开发进程，Windows Vista在2006年11月30日发布（此时发布的是批量许可版本，零售版稍后于2007年1月30日发布）。它引入了全新的Windows Aero设计，加入了大量新技术[36]，但因为性能下滑、启动变慢等诸多原因饱受批评。

在2009年7月22日，Windows 7和Windows Server 2008 R2发行给制造商（RTM），零售版则于3个月后发布。与上一代Windows Vista大量引入新功能不同，Windows 7的升级更集中、更平缓，意图与Windows Vista的应用和硬件完全兼容[37]。Windows 7继续改良了Windows Aero设计，并引入了多点触控、家庭组等新功能。
Windows 8 / 8.1
主条目：Windows 8和Windows 8.1

Windows 8在2012年10月26日发布，它呈现出了巨大的变化，包括现代UI（Modern UI）的引入、迎合触摸设备的磁贴化设计等。这些变化中包含了对开始菜单的重新设计，在其中微软使用了巨大的磁贴以方便平板电脑等设备的触摸，并且磁贴本身也可以用于快速呈现用户需要的信息。此外还诞生了Metro应用程序，它们与常规的应用在外观和设计上大相径庭。值得一提的是，Windows 8激进地将最低分辨率上调至了1024×768像素[38]，这使得很多上网本无法运行Windows 8。

Windows 8.1作为Windows 8的升级版，于2013年10月17日发布，包含了功能上的一些增强。
Windows 10
主条目：Windows 10

2014年9月30日，微软宣布将以Windows 10作为Windows的下一代操作系统，并发行技术预览版。Windows 10在2015年7月29日正式发布，并且解决了Windows 8中用户界面设计的缺陷。Windows 10的改变包括传统开始菜单的回归、全新的虚拟桌面系统，以及可以窗口化运行的Windows Store应用。Windows 10声称会免费提供给符合条件的Windows 7、Windows 8和Windows 8.1电脑[39]。Windows 10是微软有史以来安全性最高的Windows，其中支持Windows Hello、指纹以及面部ID登录。Windows 10包括数码笔、平板电脑等服务，同时也是兼容性最强的Windows。而Windows 10也是支持Xbox游戏机的操作系统。

2021年6月，在Windows 11公布之后，微软更新了Windows 10的产品生命周期政策，表示Windows 10将在2025年10月14日后停止支持[40][41]。
Windows 11
主条目：Windows 11

在2021年6月24日的直播中，微软宣布了将以Windows 11作为Windows的下一代操作系统。据微软称，Windows 11将会被设计的更加友好和易用。Windows 11于2021年10月5日正式发布[42]，并且会免费提供给符合Windows 11最低硬件需求的Windows 10用户升级。[43]
Windows 365

2021年7月，微软宣布将在8月2日推出虚拟化Windows订阅服务“Windows 365”。它不是Microsoft Windows的独立版本，而是一种Web服务。他被视为创建在Windows虚拟桌面之上的Windows 10和Windows 11。Windows 365可以跨平台使用，因此Apple和Android以及任何带有网络浏览器的操作系统用户都可以使用Windows 365[44][45][46][47][48][49]。
移动设备操作系统

主条目：Windows Mobile和Windows Phone


不过，幸而还有一些书，在讲述其然的同时还在讲述其所以然。有趣的是，其中特别重要的几本正是由微软出版社组织和出版的。可见微软自己也知道，光作黑盒子描述，光让人家知其然而不知其所以然，是不够的，那样很难成长起高质量的Windows软件开发人员，反过来对微软也不利。这跟奴隶主有时候也意识到该让奴隶们吃的壮实一些，是同一个道理。而对于我们，这些书的重要性就不言而喻了。

Windows参考书的首选当推Mark Russinovich和 David Solomon的“Microsoft Windows Internals”第4版，微软出版社2005年版。我们只要简单回顾一下这本书 的历史，读者就可体会到它的重要性。这本书的第一版由Helen Custer编写，书名“Inside Windows NT”。第二版(1998年) 改由David Solomon编写，由WinNT开发团队的主任Lou Perazzoli作序。第三版(2000年)的书名改成 “Inside Windows 2000”，由David Solomon和Mark Russinovich共同编写。到了第四版，书名又改成 “Microsoft Windows Internals”，由Mark Russinovich和David Solomon共同编写。尤其引人注目的是，第四版上有David Cutler写的前言，题为“Historical Perspective”，文中回顾了WinNT的由来。这位 David Cutler可不是等闲之辈，他是WinNT之父。就是他，当年把VMS的技术和(部分)人马从DEC带到了微软。有个笑话很形象地说出了 WinNT和VMS之间的渊源关系：把“VMS”这三个字母的ASCII代码每个都加1，就成了“WNT”。而David Solomon是 David Cutler在DEC就相识的老伙伴。正是David Cutler特许David Solomon可以自由翻看WinNT的源代码。这种 “看”，跟把人请去住在旅馆里十天半个月、每天去微软资料室看上几个钟头的那种“双规”下的“看”，当然有着天壤之别。所以，这本书应该说是一本权威著作，书中所讲应该认为是有源代码根据的。再说，这本书也确实让人知其然并且知其所以然。当然，要是有源代码就更好了，但是要知道那是微软，能有如此这般就很不错了。在兼容内核的开发过程中，这本书无疑将在总体上起很大的指导作用。

第二本书是Walter Oney的 “Programming the Microsoft Windows Driver Model”第2版，微软出版社2003年版。这本书对微软的 WDM设备驱动模型(即框架)作了深入的介绍。微软要求从Win2k开始的设备驱动模块都符合WDM的要求。与传统的WinNT设备驱动相比，WDM要求设备驱动模块都支持PnP(即插即用)、电源管理(不用时可转入省电模式)、以及WMI (Windows Management Instrumentation，意为Windows管理手段，是微软版的WBEM实现)。所以，这本书所介绍的是新的Window设备驱动框架的设计与实现，附带着也介绍了设备驱动界面上的一些重要的函数。显然，这本书对于兼容内核中设备驱动框架和设备驱动界面的实现有着重要的指导意义。读了这本书，再回过去看Windows DDK中一些样本实例的源代码，就更容易理解，理解也可以更深了。

不过，现在实际上在使用的.sys模块还有不少只是传统的WinNT设备驱动。WinNT的设备驱动框架可以说是WDM的一个子集，比WDM要简单一些。对于WinNT设备驱动，Art Baker的“The Windows NT Device Driver Book”是一本很好的参考书。这本书是由 Prentice Hall在1996年出版的。虽然年代已经久远，书的内容却并不显得太陈旧，可以作为WDM那本书的补充，参照阅读。
第四本书是Jeffrey Richter的“Advanced Windows”第3版，微软出版社1997年版。这本书就不仅仅是讲内核了。它让读者对Windows操作系统有个整体上的理解。例如，在另一篇文章中笔者曾提到，Windows在创建子进程时对于已打开文件的遗传与Unix/Linux 在方式上有很大的不同，这本书对此就有很详细的叙述。而这一点正可以说明，不同内核间的有些差别是很难在内核外面得到补偿的。

第五本书是 Gary Nebbett的“Windows NT/2000 Native API Reference”，MTP出版社。这里所说的 “Native API”，实际上就是系统调用。显然，这是一本关于WinNT系统调用的参考手册。既然微软把系统调用界面藏在黑盒子里面，或者说藏在 Win32 API后面，从来都不公开，那么这本参考手册的价值也就不言而喻了。看一下这本书，就可以知道实现Windows系统调用界面的工作量该有多 大。

作为对这本书的补充，Parasad Dabak等人的“Undocumented Windows NT”，M& T Books，1999年出版，对于WinNT系统调用的实现也是一本有用的参考书。与前面几本由微软出版的参考书不同的是，这两本书的材料主要是通过逆向工程得来的。有源代码作为根基的著作固然比较权威，根据实验取得的资料也值得重视。

还有一本Sven Schreiber的 “Undocumented Windows 2000 Secrets”，Addison-Wesley，2001年出版，也是一本好书，甚至更好。这本书一边是基于逆向工程介绍Windows内核各方面的内容，也包括设备驱动；另一边还教给读者一些逆向工程的方法，所以对程序的调试很有好处。特别值得一提的是，这本书的附录中实际上还列出了Win2k系统调用的函数跳转表、即函数名与系统调用号的对照，书中还讲述了这个对照表是如何得来的。这可是个宝贵的信息。因为Native API一书中虽然详细介绍了各个具体系统调用的使用方法，却并未提供它们的系统调用号。而若缺了这个信息，我们在实现 Windows系统调用界面的函数跳转表时就得多费许多周折。

Rajeev Nagar的“Windows NT File System Internals”，O’Reilly，1997，虽然主题是“文件系统内幕”，但是实际上对内核的各个方面都有一些介绍，也有一定的参考价值。

## Windows 应用程序开发

《Windows 程序设计》
《Windows 核心编程》

最后，关于 Windows 的技术资料，微软本身的各种 SDK、DDK、以及 MSDN 网站上的资料当然是重要的，但是信息量太大。在笔者看来，微软的资料数量之大正是由于不公开源代码。一件东西，放在透明的玻璃瓶里，自然就不需要作太多的描述；而若封装在一个黑盒子中，描述起来可就费劲了。微软既不肯公开其源码，却又想要别人在此基础上开发各种第三方软件，自然就得对其各种产品作黑盒子描述，“信息爆炸”就不可避免了。许多人见了微软的资料就烦，是因为这些资料只告诉你“其然”而不告诉你“其所以然”。也有许多人很喜欢微软的资料，是因为这些资料就像使用手册，所以“一抓就灵”。也难怪市面上有那么多关于 Windows的各种“宝典”。读微软的资料可以使你成为“很好的”工程师，却不会使你成为科学家。

## 结束语
