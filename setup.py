import json
import os
import re
import subprocess
import sys
import portlib


def install():
    stop()
    # 安装python依赖
    print("更新环境.......")
    res = subprocess.getoutput("sudo apt-get update -y")
    res = subprocess.getoutput("sudo apt-get upgrade -y")
    print("安装依赖.......")
    res = subprocess.getoutput("sudo apt-get install dpkg -y")
    res = subprocess.getoutput("sudo apt-get install python-m2crypto -y")
    res = subprocess.getoutput("sudo apt-get install build-essential -y")
    res = subprocess.getoutput("sudo apt-get install python3-pip -y")
    res = subprocess.getoutput("sudo apt-get install python3-setuptools -y")
    #       安装flask相关
    print("安装flask......")
    res = subprocess.getoutput("sudo pip3 install flask")
    #       安装shadowsocks相关
    print("安装shadowsocks")
    res = subprocess.getoutput("sudo pip3 install shadowsocks")
    # 复制相关配置
    print("更新配置.......")
    ssstring = {"local_address": "127.0.0.1", "timeout": 300, "method": "rc4-md5", "server": "66.42.58.196",
                "port_password": {"8389": "ssadmin"}, "local_port": 1081, "fast_open": True}
    with open("./defaultConfig/shadowsocks.json", "w", encoding="utf8") as fw:
        fw.write(json.dumps(ssstring))

    portstring = {"8389": {"used": "0", "port": "8389", "speed": "10240", "passwd": "ssadmin", "limit": "500000",
                           "useable": True}}
    with open("./defaultConfig/port.json", "w", encoding="utf8") as fw:
        fw.write(json.dumps(portstring))

    userstring = {"user": "admin", "passwd": "8784b1eb76a1aa5fae25ad19fbaf0afb", "isactive": False}
    with open("./defaultConfig/user.json", "w", encoding="utf8") as fw:
        fw.write(json.dumps(userstring))
    # 获取本机IP
    res = subprocess.getoutput("sudo ifconfig")
    ip = ""
    for item in re.findall("inet addr:(\d+\.\d+\.\d+\.\d+)", res):
        if item != '127.0.0.1':
            ip = item
            break
    # 写入shadowsocks.json本机ip
    ss_config = {}
    with open("./defaultConfig/shadowsocks.json", "r", encoding="utf8") as fr:
        ss_config = dict(json.loads(fr.readline()))
        ss_config.update({"server": ip})
    with open("./defaultConfig/shadowsocks.json", "w", encoding="utf8") as fw:
        fw.write(json.dumps(ss_config))
    if not os.path.exists("/etc/ssadmin/"):
        res = subprocess.getoutput("sudo mkdir /etc/ssadmin")
    res = subprocess.getoutput("sudo cp defaultConfig/* /etc/ssadmin/")
    # 设置权限
    print("授权.......")
    res = subprocess.getoutput("sudo chmod 775 -R *")
    res = subprocess.getoutput("sudo chmod 775 -R /etc/ssadmin/")
    # 启动shadowsocks
    print("启动........")
    portlib.delAllPortRule()
    portlib.addAllPortRule()
    res = subprocess.getoutput("sudo ssserver -c /etc/ssadmin/shadowsocks.json -d start")
    os.system("sudo nohup python3 ssadmin.py &")
    tipsString = """
    访问方式：
        1.若有域名解析到此ip，请访问http://domain:8000/
        2.访问http://{}:8000/
        3.默认用户名：admin 密码：ssadmin  登陆后请修改密码。""".format(ip)
    print(tipsString)


def start():
    # 清理老的进程
    command_string = "sudo ps aux|grep ssadmin.py"
    res = str(subprocess.getoutput(command_string))
    for item in res.split("\n"):
        pid = re.sub("\s+","#",item).split("#")[1]
        subprocess.getoutput("sudo kill -9 {}".format(pid))
    os.system("nohup python3 ssadmin.py &")
    #res = subprocess.getoutput("python3 ssadmin.py")
    res = subprocess.getoutput("cd .")
    res = subprocess.getoutput("cd .")
    print("ssadmin started.")


def stop():
    # 清理老的进程
    command_string = "sudo ps aux|grep ssadmin.py"
    res = str(subprocess.getoutput(command_string))
    for item in res.split("\n"):
        pid = re.sub("\s+","#",item).split("#")[1]
        subprocess.getoutput("sudo kill -9 {}".format(pid))
    print("ssadmin stoped.")

def restart():
    # 先执行stop 再执行start
    stop()
    start()

def gethelp():
    help_string = """
    Usage: python3 setup.py [command]
    use this command to manage ssadmin
    
    [commands]:
    install - install shadowsocks and flask,then start them.
    start - start ssadmin(not shadowsocks).
    stop - stop ssadmin(not shadowsocks).
    restart - restart ssadmin(not shadowsocks).
    
    if you want to start/stop/restart shadowsocks, login ssadmin.
    """
    print(help_string)


if __name__ == '__main__':
    action = sys.argv[1]
    if action=="install":
        install()
    elif action=="start":
        start()
    elif action=="stop":
        stop()
    elif action=="restart":
        restart()
    else:
        gethelp()
