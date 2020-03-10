# DNSPOD_DDNS
群晖专用自动DDNS检测更新脚本_Python
10分钟检测一次IP是否变化，变化则更改，没变则继续等待

1. 系统要求：Linux
2. 软件要求：Python2/3(3理论可行，还没试) curl wget

使用教程:

打开脚本修改
loginToken = ID,Token # dnspod密钥管理添加修改
domain_1 = baidu.com # 你要使用的一级域名 如：baidu.com
domain_2 = www # 域名主机头 如www

注意：
如果要使用新的域名或者主机头记录，则删掉当前目录下的info.json文件，重新运行脚本即可。

运行:
python dnspood_Python.py
