# -*- coding: utf-8 -*-

# Python2/3 通用 dnspood
# ip1 = http://whatismyip.akamai.com/
import os,time,json,io

loginToken = 'ID,Token' # 你的ID,Token dnspood > 密钥管理 注意：不要删除,号
domain_id = '' # 域名id
record_id = '' # 记录id
domain_1 = 'baidu.com' # 你的主域名 如 baidu.com
domain_2 = 'www' # 你的记录主机头 如 www
url1 = 'http://myip.dnsomatic.com/'
ip = 0

def getInfo():
    # 读取已有的信息数据
    if os.path.exists('info.json') == True:
        with open('info.json') as info:
            infoData = json.load(info)
            global domain_id, record_id
            domain_id = infoData['domain_id']
            record_id = infoData['record_id']

    else:
        # 自动获取域名id，记录id信息等
        os.system("curl -X POST https://dnsapi.cn/Domain.List -d 'login_token={}&format=json' > 1.json".format(loginToken))
        with open('1.json') as f:
            json1 = json.load(f)
            for i in range(json1['info']['domain_total']): # 获取域名数量
                if domain_1 == json1['domains'][i]['punycode']:
                    # 找到域名，开始获取域名id
                    domain_id = json1['domains'][i]['id']
        os.system("curl -X POST https://dnsapi.cn/Record.List -d 'login_token={}&format=json&domain_id={}&sub_domain={}&record_type=A&offset=0&length=3' > 2.json".format(loginToken, domain_id, domain_2))
        with open('2.json') as f:
            json2 = json.load(f)
            record_id = json2['records'][0]['id'] # 取到记录id
        # 写入数据到info.json
        datalist = {'domain_id':domain_id, 'record_id':record_id}
        dataJson = json.dumps(datalist)
        with open('info.json', 'w') as f:
            f.write(dataJson)
        # 删除临时数据
        os.system('rm -rf 1.json && rm -rf 2.json')

def getIp():
    result = os.popen("wget -qO- " + url1)
    return result.readline()

def main():
    print('\n' + '正常运行中......')
    while True:
        time.sleep(60 * 10) # 10min
        nowIp = getIp()
        global ip
        if nowIp == ip:
            # 没有变换，继续循环
            pass
        else:
            # 出现变换，更改域名解析值
            os.system("curl -X POST https://dnsapi.cn/Record.Modify -d 'login_token={}&format=json&domain_id={}&record_id={}&sub_domain={}&value={}&record_type=A&record_line_id=0'".format(loginToken, domain_id, record_id, domain_2, nowIp))
            ip = nowIp # 最新IP赋值
            
if __name__ == "__main__":
    getInfo()
    ip = getIp() # 初始IP，循环对上次结果比对
    # 首次修改域名记录，防止一开始域名解析就不对
    os.system("curl -X POST https://dnsapi.cn/Record.Modify -d 'login_token={}&format=json&domain_id={}&record_id={}&sub_domain={}&value={}&record_type=A&record_line_id=0'".format(loginToken, domain_id, record_id, domain_2, ip))
    print('\n' + '第一次IP更新成功: {}'.format(ip))
    main()