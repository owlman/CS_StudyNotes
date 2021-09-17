# 常用的shell命令

作为一名有10年以上使用年龄的Linux/MacOSX用户来说，键盘的作用往往要远大于鼠标。而且，作为一个黑客文化的追随者，我也希望越来越多的用户能认识到命令行的潜在价值，不要把它视为只是计算机专家们的玩具，这些工具所带来的方便和效率，是图形界面无法比拟的。计算机管理员可以通过它们在更少的时间内、更有效地完成复杂的任务。以下是我自己除ls、rm、mv、cp、mkdir、rmdir这些基本命令以外的一些常用命令。

## 通用命令

* 建立连接：

    ```bash
     ln -s <dirname or filename> <linkname>
    ```

* wget命令：
  * 下载文件： `wget <URL>`
  * 下载并另存为：`wget -o <filename> <URL>`
  * 断点续传下载：`wget -c <URL>`

* tar命令：
  * 查看压缩包：`tar -tf test.tar.gz`
  * 压缩文件：

      ```bash
      tar –cvf packagename.tar *.jpg
      tar –czf packagename.tar.gz *.jpg
      tar –cjf packagename.tar.bz2 *.jpg
      tar –cZf packagename.tar.Z *.jpg
      ```

  * 解压文件：

      ```bash
      tar –xvf packagename.tar
      tar -xzvf packagename.tar.gz
      tar -xjvf packagename.tar.bz2
      tar.bz2tar –xZvf packagename.tar.Z
      ```

## Babun & Cygwin：

* 剪贴板操作：
  * 将文件内容复制到剪贴板：`cat [file] | pbcopy`
  * 从剪贴板复制到文件：`pbpaste > [file]`

* apt-cyg包管理器：
  * 安装软件包：`apt-cyg install <packagename>`
  * 移除软件包：`apt-cyg remove <packagename>`
  * 更新软件包：`apt-cyg update`
  * 显示已安装包：`apt-cyg show`
  * 查找指定软件包：apt-cyg find <pattern(s)>
  * 查看指定软件包的信息：apt-cyg describe <pattern(s)>
  * 查看本地安装的软件包信息：`apt-cyg packageof <commands or files>`

## Mac OS X：

* 剪贴板操作：
  * 将文件内容复制到剪贴板：`cat [file] | pbcopy`
  * 从剪贴板复制到文件：`pbpaste > [file]`

* homebrew包管理器：
  * 安装brew：`ruby -e "$(curl -fsSkL raw.github.com/mxcl/homebrew/go)"`
  * 安装软件包：`brew install <packagename>`
  * 列出已安装的软件包：`brew list`
  * 删除软件包：`brew remove <packagename>`
  * 查看软件包信息：`brew info <packagename>`
  * 列出软件包的依赖关系：`brew deps <packagename>`
  * 更新：`brew：brew update`
  * 列出过时的软件包（已安装但不是最新版本）：`brew outdated`
  * 更新过时的软件包（全部或指定）：`brew upgrade 或 brew upgrade <packagename>`

## Linux

* 剪贴板操作：
  * 将文件内容复制到剪贴板：`cat [file] | xsel -i`
  * 从剪贴板复制到文件：`xsel > [file]`

* apt包管理器：
  * 搜索指定包：`apt-cache search <packagename>`
  * 获取指定包的信息：`apt-cache show <packagename>`
  * 安装指定包：`apt-get install <packagename>`
  * 重新安装指定包：`apt-get install <packagename> --reinstall`
  * 删除指定包：`apt-get remove <packagename>`
  * 删除指定包及其配置文件：`apt-get remove packagename --purge`
  * 更新源：`apt-get update`
  * 更新已安装的包：`apt-get upgrade`
  * 升级系统：`apt-get dist-upgrade`
  * 了解使用依赖：`apt-cache depends <packagename>`
  * 查看该包被哪些包依赖：`apt-cache rdepends <packagename>`
  * 下载指定的源代码：`apt-get source <packagename>`
  * 清理无用的包：`apt-get clean`

