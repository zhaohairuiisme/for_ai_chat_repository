# 你好

你可以克隆 index.py 文件，不过，你需要先安装 Python [python.org]

--- 

# Python 仓库依赖说明

以下是在本项目中使用的 Python 库及其安装方法。请确保在开始项目前按照说明安装所有必要的依赖项。

## 所需库

- **requests**: 用于发送 HTTP 请求。
- **json**: 用于处理 JSON 数据。
- **subprocess**: 用于执行系统命令。
- **platform**: 用于获取系统相关信息。
- **markdown**: 用于解析和渲染 Markdown 文本。
- **pygments**: 用于代码高亮显示。
- **easygui**: 用于创建简单的图形界面。

## 安装命令

可以通过以下`bash`命令一次性安装所有依赖库：

```bash
pip install requests json subprocess platform markdown pygments easygui
```
如果安装太慢，请输入：
```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
安装失败请更换源（已知可用源：
- 清华大学源：https://pypi.tuna.tsinghua.edu.cn/simple ；
- 阿里云源：https://mirrors.aliyun.com/pypi/simple ；
- 豆瓣源：https://pypi.douban.com/simple ；
- 中国科学技术大学源：https://pypi.mirrors.ustc.edu.cn/simple ；
- 腾讯云源：https://mirrors.cloud.tencent.com/pypi/simple ；
）
> <h3>注：大家根据自身需要选择合适的镜像源，个人推荐中科大的镜像源</h3>
当然，您可以临时换源：
``` bash
pip install package_name -i https://pypi.tuna.tsinghua.edu.cn/simple
```
> i后面表示你要的源

<h3>重置镜像源</h3>
安装完后您可以重置镜像源：

查看当前镜像源：

```bash

pip config list
```

删除全局设置的镜像源:

```bash
pip config unset global.index-url
```

删除用户级别设置的镜像源:

```bash
pip config unset global.index-url --user
```
> --user表示你的用户名，下面不一一叙述

如果还设置了其他镜像源（如 extra-index-url），也需要一并删除：

```bash
pip config unset global.extra-index-url --user
```

<h3>其他关于 pip 的操作和设置</h3>


查看当前环境中已安装的所有包及其版本信息：

```bash
pip list
```

<h1>安装包与卸载包：</h1>

<h3>安装</h3>

```bash
pip install package_name
```

<h3>卸载</h3>

```bash
pip uninstall package_name
```

> package_name 为包的名字

删除当前环境的所有 pip 缓存：

```bash
pip cache purge
```

删除特定包的缓存：

```bash
pip cache remove package_name
```

> package_name 为要删除的包的名字


<h1>问题</h1>

换源之后下载的包无法匹配其他依赖包:

> ERROR: Could not find a version that satisfies the requirement …

网络无法连接：

> WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by ‘NewConnectionError(’<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7f4248ebf7c0>: Failed to establish a new connection: [Errno 101] 网络不可达’)':…
