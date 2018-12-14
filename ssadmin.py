import hashlib
import json
import subprocess
import time
from threading import Thread
from flask import Flask
from flask import Response
from flask import render_template, redirect, send_file
from flask import request

import portlib

app = Flask(__name__)

# shadowsocks.json
ss_path = "/etc/ssadmin/shadowsocks.json"
# port.json
port_path = "/etc/ssadmin/port.json"
# user.json
user_path = "/etc/ssadmin/user.json"

user_dict = {}


def checkUserStatus(request):
    global user_dict
    if len(user_dict) == 0:
        with open(user_path, "r", encoding='utf8') as fr:
            user_dict = json.loads(fr.readline())
    user = request.cookies.get("user", None)
    passwd = request.cookies.get("passwd", None)
    # 检查cookie中是否有用户名和密码，以及用户是否处于活跃状态
    if user and passwd and user_dict.get("isactive", False) and \
                    user == user_dict.get("user", "") and passwd == user_dict.get("passwd", ""):
        return True
    else:
        return False


@app.route('/')
def hello_world():
    # 检查cookie中是否有用户名和密码，以及用户是否处于活跃状态
    if checkUserStatus(request):
        return redirect("adminpanel")
    else:
        return redirect("login")


@app.route('/login')
def login():
    # 检查cookie中是否有用户名和密码，以及用户是否处于活跃状态
    if checkUserStatus(request):
        return redirect("adminpanel")
    else:
        return render_template("login.html")


@app.route('/checkAuth', methods=['POST'])
def getCheckAuth():
    global user_dict
    # 获取json中的user passwd
    json_data = dict(request.get_json())
    user_data = json_data.get("user", "")
    passwd_data = json_data.get("passwd", "")
    # 从json中读取的passwd加密
    passwd_data = hashlib.md5(bytes(passwd_data, encoding='utf8')).hexdigest()
    # 获取cookie中user passwd
    user_cookie = request.cookies.get("user", None)
    passwd_cookie = request.cookies.get("passwd", None)
    # cookie存在，已登录 跳转；检查用户是否活跃状态
    if user_cookie and passwd_cookie and user_dict.get("isactive", False) and \
                    user_cookie == user_dict.get("user", "") and passwd_cookie == user_dict.get("passwd", ""):
        response = {"status_code": 302, "location": "/adminpanel"}
        return json.dumps(response)
    # cookie中没有，进行验证，若符合，写入cookie并跳转；用户活跃状态设置为True
    elif user_data and passwd_data and user_data == user_dict.get("user", "") and passwd_data == user_dict.get("passwd", ""):
        user_dict.update({"isactive": True})
        with open(user_path, "w", encoding='utf8') as fw:
            fw.write(json.dumps(user_dict))
        res = Response(
            response=json.dumps({"status_code": 302, "location": "/adminpanel"}),
            status=200,
            mimetype='application/json'
        )
        res.set_cookie('user', user_data)
        res.set_cookie('passwd', passwd_data)
        return res
    # 其他不符合，返回空，前端重试
    else:
        return '', 404


@app.route('/adminpanel', methods=['GET'])
def get_admin_panel():
    # 检查cookie中是否有用户名和密码，以及用户是否处于活跃状态
    if checkUserStatus(request):
        return render_template("controller.html")
    else:
        return redirect("login")


@app.route('/getportinfo')
def get_port_info():
    """
    获取端口信息，发送到客户端
    """
    if checkUserStatus(request):
        port_json = ""
        with open(port_path, "r", encoding='utf8') as fr:
            port_json = json.loads(fr.readline())
        new_data = {}
        for k, v in port_json.items():
            new_data.update({str(k): v})
        return json.dumps(new_data), 200
    else:
        return json.dumps({}), 404


@app.route('/postportinfo', methods=['POST'])
def post_port_info():
    """
    上传端口信息到服务器
    port.json = {port:{},port:{}}
    ss.json = {"server":"","local_address":"127.0.0.1","local_port":1081,"port_password":{"8389":"xxxx",},"timeout":300,"method":"rc4-md5","fast_open":true}

    """
    # 如果用户状态不符合，返回404
    if not checkUserStatus(request):
        return '', 404
    # else:
    data = dict(request.get_json())
    ss_json = {}
    port_json = {}
    # 读取配置
    with open(ss_path, "r", encoding='utf8') as fr:
        ss_json = dict(json.loads(fr.readline()))
    with open(port_path, "r", encoding='utf8') as fr:
        port_json = dict(json.loads(fr.readline()))
    # 替换字段
    if data.get("useable", "") and data.get("useable", "") == "是":
        data.update({"useable": True})
    elif data.get("useable", "") and data.get("useable", "") == "否":
        data.update({"useable": False})
    # 添加端口
    if data.get("type", "") and data.get("type", "") == "add":
        data.pop("type")
        port_json.update({data.get("port", 0): data})  # 添加到port.json
        if data.get("useable", "") and data.get("useable", "") == True:  # 如果可用，写入ss.json
            data.update({})
            port_passwd = ss_json.get("port_password", {})
            port_passwd.update({data.get("port", 0): data.get("passwd", "")})
            # 添加端口流量监控
            portlib.delOnePortRule(data.get("port", 0))
            portlib.addOnePortRule(data.get("port", 0))
    # 修改端口
    elif data.get("type", "") and data.get("type", "") == "modify":
        data.pop("type")
        port_json.update({data.get("port", 0): data})  # 添加到port.json
        if data.get("useable", "") and data.get("useable", "") == True:  # 如果可用，写入ss.json
            port_passwd = ss_json.get("port_password", {})
            port_passwd.update({data.get("port", 0): data.get("passwd", "")})
        elif data.get("useable", "1") == False:  # 如果不可用，从ss.json删除
            port_passwd = ss_json.get("port_password", {})
            port_passwd.pop(data.get("port", 0))
            ss_json.update({"port_password": port_passwd})
    # 写入文件
    with open(ss_path, "w") as fw:
        fw.write(json.dumps(ss_json))
    with open(port_path, "w") as fw:
        fw.write(json.dumps(port_json))
    return '', 200


@app.route('/deloneport', methods=['POST'])
def del_one_port():
    """
    删除某个端口
    :return:
    """
    # 如果用户状态不符合，返回404
    if not checkUserStatus(request):
        return '', 404
    # else:
    info = dict(request.get_json())
    port = info.get("port", 0)

    ss_json = {}
    port_json = {}
    # 读取配置
    with open(ss_path, "r", encoding='utf8') as fr:
        ss_json = dict(json.loads(fr.readline()))
    with open(port_path, "r", encoding='utf8') as fr:
        port_json = dict(json.loads(fr.readline()))

    port_json.pop(port)
    port_password = ss_json.get("port_password", {})
    port_password.pop(port)
    ss_json.update({"port_password": port_password})
    # 写入文件
    with open(ss_path, "w") as fw:
        fw.write(json.dumps(ss_json))
    with open(port_path, "w") as fw:
        fw.write(json.dumps(port_json))
    # 删除port流量监控
    portlib.delOnePortRule(port)
    return '', 200


@app.route('/getssinfo')
def get_ss_info():
    """
    获取ss配置，发送至客户端
    """
    # 如果用户状态不符合，返回404
    if not checkUserStatus(request):
        return json.dumps({}), 404
    # else
    send_data = {}
    with open(ss_path, "r", encoding='utf8') as fr:
        send_data = json.loads(fr.readline())
    return json.dumps(send_data), 200


@app.route('/portssinfo', methods=['POST'])
def port_ss_info():
    """
    接收来自客户端的配置信息
    :return:
    """
    # 如果用户状态不符合，返回404
    if not checkUserStatus(request):
        return '', 404
    # else
    client_data = dict(request.get_json())
    server_data = {}
    with open(ss_path, "r", encoding="utf8") as fr:
        server_data = json.loads(fr.readline())
    server_data.update(client_data)
    with open(ss_path, "w", encoding="utf8") as fw:
        fw.write(json.dumps(server_data))
    return "", 200


@app.route('/getsysinfo')
def get_sys_info():
    """
    发送系统信息到客户端
    :return:
    """
    pass


@app.route('/logout')
def logout():
    # 退出，用户活跃状态设置为false
    global user_dict
    if len(user_dict) == 0:
        with open(user_path, "r", encoding='utf8') as fr:
            user_dict = json.loads(fr.readline())
    user_dict.update({"isactive": False})
    with open(user_path, "w", encoding="utf8") as fw:
        fw.write(json.dumps(user_dict))
    return '', 200


@app.route('/startss')
def startss():
    """
    2018-12-05 16:09:25 INFO     loading libcrypto from libcrypto.so.1.0.0
    started
    """
    # 如果用户状态不符合，返回500
    if not checkUserStatus(request):
        return 'error', 500
    # else
    exec_string = "ssserver -c {} -d start".format(ss_path)
    res = subprocess.getoutput(exec_string)
    return 'succeed', 200


@app.route('/stopss')
def stopss():
    """
    INFO: loading config from shadowsocks.json
    stopped
    """
    # 如果用户状态不符合，返回500
    if not checkUserStatus(request):
        return 'error', 500
    # else
    exec_string = "ssserver -c {} -d stop".format(ss_path)
    res = subprocess.getoutput(exec_string)
    return 'succeed', 200


@app.route('/restartss')
def restartss():
    """
    2018-12-05 16:10:40 INFO     loading libcrypto from libcrypto.so.1.0.0
    stopped
    started
    """
    # 如果用户状态不符合，返回500
    if not checkUserStatus(request):
        return 'error', 500
    # else:
    try:
        res = subprocess.getoutput("ssserver -c {} -d stop".format(ss_path))
    except BaseException as e:
        pass
    res = subprocess.getoutput("ssserver -c {} -d start".format(ss_path))
    return 'succeed', 200

@app.route('/resetPasswd', methods=['POST'])
def resetPasswd():
    if not checkUserStatus(request):
        return '',404
    cookie_data = dict(request.get_json())
    if user_dict.get("passwd","")!=cookie_data.get("passwd"," "):
        return '',404
    new_passwd = hashlib.md5(bytes(cookie_data.get("new_passwd",""), encoding='utf8')).hexdigest()
    user_dict.update({"passwd":new_passwd})
    with open(user_path,"w",encoding="utf8") as fw:
        fw.write(json.dumps(user_dict))
    res = Response(status=200)
    res.set_cookie('user', user_dict.get("user",""))
    res.set_cookie('passwd', user_dict.get("passwd",""))
    return res

@app.route('/templates/<file>')
def gethtml(file):
    return send_file("./templates/" + file)


@app.route('/favicon.ico')
def getFavicon():
    return send_file("./static/img/favicon.ico")

@app.route('/robots')
@app.route('/robots.txt')
def getRobotsTxt():
    return send_file("./static/robots.txt")

def checkTime():
    portlib.delAllPortRule()
    portlib.addAllPortRule()
    while True:
        try:
            # 获取流量监控信息
            portlib.getPortTraffic()
            # 获取系统信息
            # getSysInfo()
            # 检查流量限制
            portlib.checkUsedAndLimit()
            # 检查速度限制
        except BaseException as e:
            with open("log", "a") as fa:
                fa.write("{}#location_checkTime: {}\n".format(time.ctime(), e))
        time.sleep(300)


if __name__ == '__main__':
    Thread(target=checkTime).start()

    app.run(host="0.0.0.0",port=8000)
