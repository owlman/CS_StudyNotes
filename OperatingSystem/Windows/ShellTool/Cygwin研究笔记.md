# Cygwin 研究笔记

## Cygwin 简介

Cygwin 是一个在 Windows 平台上运行的类 UNIX 模拟环境，是Cygnus Solutions公司开发的自由软件（该公司开发的著名工具还有eCos，不过现已被Redhat收购）。它对于学习UNIX/Linux操作环境，或者从UNIX到Windows的应用程序移植，或者进行某些特殊的开发工作，尤其是使用GNU工具集在Windows上进行嵌入式系统开发，非常有用。随着嵌入式系统开发在国内日渐流行，越来越多的开发者对Cygwin产生了兴趣。

Cygwin 提供一个UNIX 模拟 DLL 以及在其上层构建的多种可以在 Linux 系统中找到的软件包，在 Windows XP SP3 以上的版本提供良好的支持。Cygwin主要由Red Hat及其下属社区负责维护。

## Cygwin 的安装与配置

Cygwin 的安装文件很容易通过百度找到。国内的网站上有"网络安装版"和"本地安装版"两种。标准的发行版应该是网络安装版。两者并无大不同，下面介绍一下安装的过程。

step1. 下载后，点击安装文件（setup.exe）进行安装，第一个画面是GNU版权说明，点"下一步(N)—>"，

环境变量

开始运行bash之前，应该设置一些环境变量。Cygwin提供了一个.bat文件，里面已经设置好了最重要的环境变量。通过它来启动bash是最安全的办法。这个.bat文件安装在Cygwin所在的根目录下。可以随意编辑该文件。

CYGWIN变量用来针对Cygwin运行时系统进行多种全局设置。开始时，可以不设置CYGWIN或者在执行bash前用类似下面的格式在dos框下把它设为tty

C:\> set CYGWIN=tty notitle glob

PATH变量被Cygwin应用程序作为搜索可知性文件的路径列表。当一个Cygwin进程启动时，该变量被从windows格式（e.g. C:\WinNT\system32;C:\WinNT）转换成unix格式（e.g., /WinNT/system32:/WinNT）。如果想在不运行bash的时候也能够使用Cygwin工具集，PATH起码应该包含x:\Cygwin\bin，其中x:\Cygwin 是你的系统中的Cygwin目录。

HOME变量用来指定主目录，推荐在执行bash前定义该变量。当Cygwin进程启动时，该变量也被从windows格式转换成unix格式，例如，作者的机器上HOME的值为C:\（dos命令set HOME就可以看到它的值，set HOME=XXX可以进行设置），在bash中用echo $HOME看，其值为/cygdrive/c.

TERM变量指定终端型态。如果没对它进行设置，它将自动设为Cygwin。

LD_LIBRARY_PATH被Cygwin函数dlopen()作为搜索.dll文件的路径列表，该变量也被从windows格式转换成unix格式。多数Cygwin应用程序不使用dlopen,因而不需要该变量。
进入安装模式选择画面。

step2. 安装模式有"Install from Internet"、"Download from Internet"、
"Install from Local Directory" 三种。"Install from Internet"就是直接从internet上装，适用于网速较快的情况。在选择镜像页面，可以使用一些中国的镜像源以便提高网速。

## Windows 重装后，如何删除 Cygwin 目录？

> **参考资料**：
>
> - http://blog.csdn.net/zjjyliuweijie/article/details/6577037
> - http://blog.csdn.net/huangzhtao/article/details/6038504
> - http://blog.csdn.net/hu_shengyang/article/details/7828998

### 为什么 Cygwin 的安装目录（在系统重装后）会如此难以删除？

在正常情况下，Cygwin 的反安装程序自然是删除该目录的最好选择。但 Windows 的重装会反安装程序，这之后再要删除该目录就有点麻烦了。因为 Cygwin 所模拟的是 Linux 的权限管理体系，这跟 Windows 的默认权限管理存在着一些冲突。不信的话，您可以用右键查看一下该目录属性中的安全选项，就会在"组或用户名"一栏中看到一些无法识别的用户（带问号），它们其实是系统重装之前的用户，它会有一串用于唯一识别的数字。所以哪怕我们重装系统之后再使用原来的用户名，这个唯一识别号也是完全不同的。因此，我们当前登录的帐号对文件没有修改和删除的权限。

### 解决方案

在 Windows 系统下，人们对于无法修改或删除的文件夹及文件，一般会采取先获得权限再进行修改的处理方式，这种方式通常包括两个步骤：首先修改目标文件夹及其文件的所有者，使得当前用户获得对其的访问权限。然而在 Windows 中，如果要删除一个文件夹的话，需要对该文件夹下的所有文件和文件夹都拥有权限才能删除，但在图形界面中，修改一个文件夹的用户权限仅对该文件夹下的第一层文件和文件夹有效，无法递归至更深层次的文件及文件夹。而 Cygwin 安装目录的深度很大，且文件众多，手动修改起来会显得非常麻烦，耗时，因此本人强烈建议大家选择第 2 种方法，程序修改。

#### 手动删除

1. 右键点要删除 Cygwin 文件夹，依次选择属性->安全->高级->所有者->编辑，将所有者改为你的登录帐户，勾选下方"替换子容器和对象的所有者"。
2. 继续在文件夹的属性对话框中依次点击安全->高级对话框中选"审核选项卡"->"继续"->"添加"，并在其中输入 Everyone，以便添加 Everyone 帐户，在弹出的对话框中将"完全控制"后面的允许勾上，勾选"使用可从此对象继承的权限替换所有子对象权限"，点击"确定"。

现在，我们可以顺利删除 Cygwin 文件夹了。显而易见，手动删除是件非常痛苦的工作。

#### 自动删除

1. 使用 takeown.exe 修改 Cygwin 文件夹及其子文件的权限。takeown.exe 可从网上下载，下载完成之后，将 takeown.exe 放在 Cygwin 的安装目录下，然后在cmd中输入：`takeown.exe /F * /R`。该命令会负责把 takedown 所处目录下的所有文件和文件夹的所有者修改成当前用户，并且可对这些目录进行递归操作，令其对所有子目录和子文件生效。
2. 用 win7 系统提供的命令修改用户对目标文件夹下所有子目录的访问权限。该命令为`Icacls`，其用法亦可在网上搜到：`Icacls \cygwin /T /grant <user>:F`。该命令会赋予`<user>`用户在 Cygwin 文件夹及其所有子目录的完全控制（F）权限。

以上两个步骤都需要 2、3 分钟左右的处理时间，请务必要耐心等其执行完毕。

## 以下为待整理资料

Cygwin 始于 1995 年，最初作为 Cygnus 工程师 Steve Chamberlain 的一个项目。当时 Windows NT 和 Windows 95 将 COFF 作为目标代码，而 GNU 已经支持 x86 和 COFF，以及 C 语言库 newlib。这样至少在理论上，可以将 GCC 重定向，作为 cross compiler，从而产生能在 Windows 上运行的可执行程序。在后来的实践中，这很快实现了。

接下来的问题是如何在 Windows 系统中引导编译器，这需要对 Unix 的足够模拟，以使 GNU configure 的 shell script 可以运行，这样就用到像 bash 这样的 shell，进而需要 Fork 和 standard I/O。Windows含有类似的功能，所以Cygwin库只需要进行翻译调用、管理私有数据，比如文件描述符。

1996 年后，由于看到 Cygwin 可以提供 Windows 系统上的 Cygnus 嵌入式工具（以往的方案是使用 DJGPP），其他工程师也加入了进来。特别吸引人的是，Cygwin 可以实现 three-way cross-compile，例如可以在Sun工作站上 build，如此就形成 Windows-x-MIPS cross-compiler，这样比单纯在 PC 上编译要快不少。1998年起，Cygnus 开始将 Cygwin 包作为产品来提供。

Cygwin 包括了一套库，该库在 Win32 系统下实现了 POSIX 系统调用的API；还有一套 GNU 开发工具集（比如GCC、GDB），这样可以进行简单的软件开发；还有一些 UNIX 系统下的常见程序。2001 年，新增了 X Window System。
另外还有一个名为 MinGW 的库，可以跟Windows本地的MSVCRT库（Windows API）一起工作。MinGW占用内存、硬盘空间都比较少，能够链接到任意软件，但它对POSIX规范的实现没有Cygwin库完备。

但糟糕的是，Cygwin 不支持 Unicode。实际上，除了当前 Windows 系统以及 OEM codepages（例如，一个俄语用户，他的代码页是 CP1251 和 CP866，而不能是 KOI8-R、ISO/IEC 8859-5、UTF-8 等），Cygwin 对其他字符集都不支持。Cygwin 的较新版本可以通过自带终端模拟器的设置来满足显示 UTF-8 和更多代码页的功能。

Red Hat 规定，Cygwin 库遵守 GNU General Public License，但也可以跟符合开源定义的自由软件链接。Red Hat 另有价格不菲的许可协议，这样使用 Cygwin 库的专属软件，就可以进行再发布。

cygnus 当初首先把 gcc，gdb，gas 等开发工具进行了改进，使他们能够生成并解释win32的目标文件。然后，他们要把这些工具移植到 windows 平台上去。一种方案是基于win32 api对这些工具的源代码进行大幅修改，这样做显然需要大量工作。因此，他们采取了一种不同的方法——他们写了一个共享库（就是Cygwin dll），把win32 api中没有的unix风格的调用（如fork，spawn，signals，select，sockets等）封装在里面，也就是说，他们基于 win32 api写了一个unix系统库的模拟层。这样，只要把这些工具的源代码和这个共享库连接到一起，就可以使用unix主机上的交叉编译器来生成可以在windows平台上运行的工具集。以这些移植到windows平台上的开发工具为基础，cygnus又逐步把其他的工具（几乎不需要对源代码进行修改，只需要修改他们的配置脚本）软件移植到windows上来。这样，在windows平台上运行bash和开发工具、用户工具，感觉好像在unix上工作。
下载安装

网站
	
网络协议
中国科学技术大学开源软件镜像
	
HTTP/FTP
大连东软信息学院网络中心开源镜像站
	
HTTP/FTP
网易开源镜像站
	
HTTP
搜狐开源镜像站
	
HTTP
如果你的网速不是很快，或者说装过之后想把下载的安装文件保存起来，下次不再下载了直接安装，就应该选择"Download from Internet"，下载安装的文件（大约40M左右）。
事实上，所谓的"本地安装版"，也是别人从网上下载全部文件后打的包，适用于网络不佳的情况。
step3. 接下来是选择安装目的路径和安装源文件所在的路径，之后就进入了选择安装包所在的路径。
这里是安装的重点部分。在这里选择要安装的组件，不安装自然就不可能工作。可以使用搜索框找到要安装的软件。例如，不安装gcc就不可能编译软件，等等。
+ All Default
+ Admin Default
....
+ Devel Default
+ Editors Default
....
你在这个TreeView的某个节点上双击，就可以改变它的状态，如Default、Install、Uninstall、Reinstall四种状态。默认的都是Default状态，很多工具的默认状态都是不安装。
在这里我选择了在All这一行上后面的Default上点Install，全部安装，以免后患。（注意：这里的树形控件和win下面的不同，你试试点在All上点 和 在All这一行后面的Default上点，会有不同的响应）
step4. 点下一步，安装成功。它会自动在你的桌面上建立一个快捷方式。
好了，下面就开始我的linux旅程了。双击Cygwin的快捷方式进入系统。
首先介绍几个简单的linux命令。
pwd 显示当前的路径
cd 改变当前路径，无参数时进入对应用户的home目录
ls 列出当前目录下的文件。此命令有N多参数，比如ls -al
ps 列出当前系统进程
kill 杀死某个进程
mkdir 建立目录
rmdir 删除目录
rm 删除文件
mv 文件改名或目录改名
man 联机帮助
tail 显示文件的最末几行
由于linux下面的命令大多都有很多参数，可以组合使用。所以，每当你不会或者记不清楚改用那个参数，那个开关的时候，可以用man来查找，比如，我想查找ls怎么使用，可以键入
$ man ls
系统回显信息如下：
LS(1) FSF LS(1)
NAME
ls - list directory contents
SYNOPSIS
ls [OPTION]... [FILE]...
DESCRIPTION
List information about the FILEs (the current directory by
default). Sort entries alphabetically if none of -cftuSUX
nor --sort.
-a, --all
do not hide entries starting with .
-A, --almost-all
do not list implied . and ..
-b, --escape
print octal escapes for nongraphic characters
--block-size=SIZE
use SIZE-byte blocks
使用指南
编辑
播报
Cygwin同时支持win32和posix风格的路径，路径分隔符可以是正斜杠也可以是反斜杠。还支持UNC路径名。（在网络中，UNC是一种确定文件位置的方法，使用这种方法用户可以不关心存储设备的物理位置，方便了用户使用。在Windows操作系统，Novell Netware和其它操作系统中，都已经使用了这种规范以取代本地命名系统。在UNC中，我们不用关心文件在什么盘（或卷）上，不用关心这个盘（或卷）所在服务器在什么地方。我们只要以下面格式就可以访问文件：
\\服务器名\共享名\路径\文件名
共享名有时也被称为文件所在卷或存储设备的逻辑标识，但使用它的目的是让用户不必关心这些卷或存储设备所在的物理位置。）
符合posix标准的操作系统（如linux）没有盘符的概念。所有的绝对路径都以一个斜杠开始，而不是盘符（如c:）。所有的文件系统都是其中的子目录。例如，两个硬盘，其中之一为根，另一个可能是在/disk2路径下。
因为许多unix系统上的程序假定存在单一的posix文件系统结构，所以Cygwin专门维护了一个针对win32文件系统的内部posix视图，使这些程序可以在Windows下正确运行。在某些必要的情况下，Cygwin会使用这种映射来进行win32和posix路径之间的转换。
Cygwin中的mount程序用来把win32盘符和网络共享路径映射到Cygwin的内部posix目录树。这是与典型unix mount程序相似的概念。对于那些对unix不熟悉而具有Windows背景的的人来说，mount程序和早期的dos命令join非常相似，就是把一个盘符作为其他路径的子目录。
路径映射信息存放在当前用户的Cygwin mount表中，这个mount table 又在windows的注册表中。这样，当该用户下一次登录进来时，这些信息又从注册表中取出。mount 表分为两种，除了每个用户特定的表，还有系统范围的mount表，每个Cygwin用户的安装表都继承自系统表。系统表只能由拥有合适权限的用户（Windows nt的管理员）修改。
当前用户的mount表可以在注册表"HKEY_CURRENT_USER/Software/Red Hat, Inc./Cygwin/mounts v" 下看到。
系统表
存在HKEY_LOCAL_MACHINE下。
posix根路径/缺省指向系统分区，但是可以使用mount命令重新指向到Windows文件系统中的任何路径。Cygwin从win32路径生成posix路径时，总是使用mount表中最长的前缀。例如如果c:被同时安装在/c和/，Cygwin将把C:/foo/bar转换成/c/foo/bar.
如果不加任何参数地调用mount命令，会把Cygwin当前安装点集合全部列出。在下面的例子中，c盘是POSIX根，而d盘被映射到/d。本例中，根是一个系统范围的安装点，它对所有用户都是可见的，而/d仅对当前用户可见。
c:\> mount
f:\Cygwin\bin on /usr/bin type system (binmode)
f:\Cygwin\lib on /usr/lib type system (binmode)
f:\Cygwin on / type system (binmode)
e:\src on /usr/src type system (binmode)
c: on /cygdrive/c type user (binmode,noumount)
e: on /cygdrive/e type user (binmode,noumount)
还可以使用mount命令增加新的安装点，用umount删除安装点。
当Cygwin不能根据已有的安装点把某个win32路径转化为posix路径时，Cygwin会自动把它转化到一个处于缺省posix路径/cygdrive下的的一个安装点. 例如，如果Cygwin 访问Z:\foo，而Z盘当前不在安装表内，那么Z:\将被自动转化成/cygdrive/Z.
可以给每个安装点赋予特殊的属性。自动安装的分区显示为“auto”安装。安装点还可以选择是"textmode"还是 "binmode"，这个属性决定了文本文件和二进制文件是否按同样的方式处理。
路径信息
cygpath工具提供了在shell脚本中进行win32-posix路径格式转换的能力。
HOME, PATH,和LD_LIBRARY_PATH环境变量会在Cygwin进程启动时自动被从Win32格式转换成了POSIX格式(例如，如果存在从该win32路径到posix路径的安装，会把c:\Cygwin\bin转为/bin)。
存储容量
Cygwin程序缺省可以分配的内存不超过384 MB（program+data）。多数情况下不需要修改这个限制。然而，如果需要更多实际或虚拟内存，应该修改注册表的HKEY_LOCAL_MACHINE或HKEY_CURRENT_USER区段。添加一个DWORD键heap_chunk_in_mb并把它的值设为需要的内存限制，单位是十进制MB。也可以用Cygwin中的regtool完成该设置。例子如下：
regtool -i set /HKLM/Software/Cygnus\ Solutions/Cygwin/heap_chunk_in_mb 1024
regtool -v list /HKLM/Software/Cygnus\ Solutions/Cygwin
1.7版本和Eclipse的问题
Eclipse是一款比较出名的IDE，功能强大，可以用来做C\C++开发。Eclipse开发C\C++，需要用到CDT插件，就可以利用Cygwin开发一些linux移植windows的开发，或者交叉编译（微软的VC编译器不提供此功能）。如今比较火爆的Android NDK开发，如果在windows平台下就必须使用Cygwin。而且CDT插件使用注册表发现Cygwin软件的安装位置，如果使用Eclipse软件开发的话，Cygwin在安装的时候就不用配置任何的环境变量，非常方便。
但是随着Cygwin更新到1.7，CDT插件工作开始不正常，最明显的两个症状是：1.console无输出，2.按住ctrl点击，很多标准对象找不到对应的头文件。
解决方法：打开eclipse，windows->preferences->C\C++->Debug->Source Lookup Path，点击Add，添加一个Path Mapping，名字可以随意取，比如Cygwin Path Mapping；假设Cygwin安装在C盘，将/cygdriver/c映射到C:\，确定保存以后，重启Eclipse，以前的ctrl点击，控制台输出就正常了。
此方法出处来自于CDT插件的FAQ，具体网址是参见扩展阅读。原理非常简单，因为Eclipse是一个跨平台的编译器，所以CDT插件在磁盘上找文件的时候也是采用的unix风格的路径，所以在windows上无法正常工作，做一个路径映射，将Cygwin所在磁盘的路径映射为windows风格的路径，CDT就可以正常的发现头文件了。
