# 频道二维码
![1](https://user-images.githubusercontent.com/43106882/169767729-2f582e6e-2fc5-4c0e-b8d8-33759023e7bc.jpg width="500px")


# 使用说明

## 环境搭建

### 环境说明

本项目的测试系统为Ubuntu18.04，编写语言为Python，使用VS code IDE远程编写代码。

### 安装 Python3

在命令行输入 `python --version` 查看是否已经安装过 `Python3`。如果像下面一样，显示的版本为 `Python 3.x.x`，则请跳过安装环节。

```
python3
Python 3.8.13
```

下面开始安装 `Python3` ：

首先安装一些必要的依赖包

```
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel libpcap-devel xz-devel libffi-devel gcc
```

接着，下载 `Python3` 安装包，并解压缩安装包

```
wget https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tgz
tar -zxvf Python-3.7.1.tgz
```

然后，指定 `Python3` 安装路径

```
cd Python-3.7.1
./configure --prefix=/root/python37
```

接着，执行安装 `Python3`

```
make
make install
```

然后，为 `Python3` 和 `pip3` 添加软链接。软链接类似于 windows 的快捷方式，当你在终端输入 `python3` 时会使用你指定的 `python` 地址

```
ln -s /root/python37/bin/python3.7 /usr/bin/python3
ln -s /root/python37/bin/pip3 /usr/bin/pip3
```

**注意：** 这里的 `/root/python37/` 是我的 `Python3` 安装路径，和之前下载的安装包放在同一个位置。运行前请确认一下你的安装路径是否和我一样。

最后，在命令行输入 `python3 --version` 指令检验是否安装完成，如果安装成功，会打印出 `python` 的版本号

```
python3 --version
```

### 安装机器人 SDK

还未安装过机器人 SDK 的需要运行：

```
pip install qq-bot
```

已经安装过机器人 SDK 的需要运行：（本 demo 要求 SDK 版本大于 v0.7.4）

```
pip install qq-bot --upgrade
```

同时，由于需要读取 `yaml` 文件的内容，我们也需要安装 `pyyaml`

```
pip install pyyaml
```



## 测试运行

首先在程序目录下打开终端，执行

```python
python idiomBot.py
```

程序就能够运行起来了，终端提示显示：

![image](https://user-images.githubusercontent.com/43106882/169703297-9582d532-c63a-4a7f-b741-b2f046447075.png)

接着在频道内输入开始游戏的指令：“/接龙”，可以看到下面的输出：

![image](https://user-images.githubusercontent.com/43106882/169703329-2a6acd68-b9cc-444e-b596-66ba7eff3ef2.png)

如果输入正确的成语，能够跟机器人的成语接得上，可看到以下输出：

![image](https://user-images.githubusercontent.com/43106882/169703344-74f871c0-5818-444a-ab9d-7543d3af8718.png)

如果输入的不是一个成语，得到如下输出：

![image](https://user-images.githubusercontent.com/43106882/169703354-a732c24c-b02f-4f3e-80df-fb6fe0f41ec8.png)

如果输入的是成语，但是为错误答案，则得到如下输出：

![image](https://user-images.githubusercontent.com/43106882/169703364-892483dd-e03c-4835-a941-5b99e00e3544.png)

如果输入为非法字符，可以得到：

![image](https://user-images.githubusercontent.com/43106882/169703383-418cf9ac-c4b3-4d62-bf35-18a35091bb84.png)
