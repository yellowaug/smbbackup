# SMB共享文件夹备份

## Python环境
我的开发环境python 版本是3.10 

我的运行环境是Windows 10

该项目未在Linux环境上进行测试

## 项目目录

backupsmb.py  程序备份的逻辑

main.py  写程序的时候为了方便调试，将程序的逻辑以及一些想法写在这里，然后通过main.py来调试程序

startup.py 程序启动入口

requirements.txt 程序依赖的第三方库

.env 程序登录SMB共享服务器的关键信息（自行在项目目录创建）

### 程序的核心功能

该程序能够根据用户设定的文件最后修改时间备份SMB共享服务器中特定的文件夹中所有的文件以及文件夹。

场景举例：

假设用户需要备份SMB共享服务器中特定文件夹中的2024年3月7日以后的文件以及文件夹，这些文件备份到本地硬盘，那么这个场景该程序是满足需求的。

### 安装依赖

```
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 配置文件
在项目根目录创建`.env`文件，该文件的作用给是程序登录SMB共享服务器的关键信息是内容如下：
```
SMB_USER=test_smb_user_name
SMB_PASSWORD=test_smb_user_password
SMB_SERVER=test_smb_server_ip
BAK_TIMESTAMP=2024-02-01 00:00:00
LOCAL_BAK_DIR=local_windows_floder_path or local_linux_floder_path
```
字段解释

1.`SMB_USER`登录SMB服务器的用户名

2.`SMB_PASSWORD`登录SMB服务器的密码

3.`SMB_SERVER`SMB服务器的IP地址

4.`BAK_TIMESTAMP`文件备份的时间戳，格式为`YYYY-MM-DD HH:MM:SS`

5.`LOCAL_BAK_DIR`文件备份到本地的路径

### 运行程序
#### 例子1
```
python startup.py -fn 文件夹1 
```
#### 例子2
```
python startup.py -fn 文件夹1 文件夹2 文件夹3
```

程序参数解释

1.`-fn`参数后面跟需要备份的文件夹名称，可以跟单个文件夹或者多个文件夹，用空格分隔

### 程序实践

#### 假设

1.SMB服务器IP地址：192.168.1.100

2.SMB服务器用户名 test 

3.SMB服务器密码 test

4.SMB服务器上有两个文件夹：sample1 testmysql2

5.你需要备份这两个文件夹下所有截至在2024年3月7日后修改过的文件夹

#### 操作流程

1.在项目根目录创建`.env`文件，内容如下：
``` 
SMB_USER=test
SMB_PASSWORD=test
SMB_SERVER=192.168.1.100
BAK_TIMESTAMP=2024-03-07 00:00:00
LOCAL_BAK_DIR=D:\\testbak
```

2.运行程序
```
python startup.py -fn sample1 testmysql2
```

3.观察程序输出

#### 最后
个人在工作过程中需要的工具项目，如果对你有帮助，欢迎star，谢谢！有问题可以提issue，我会及时回复。
