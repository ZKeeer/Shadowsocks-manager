import json
import re
import subprocess

# shadowsocks.json
ss_path = "/etc/ssadmin/shadowsocks.json"
# port.json
port_path = "/etc/ssadmin/port.json"
# user.json
user_path = "/etc/ssadmin/user.json"

# add iptables rule
add_iptable_pre = "iptables -I OUTPUT -p tcp --sport "
# del iptables rule
del_iptable_pre = "iptables -D OUTPUT -p tcp --sport "
# query port traffic
query_port_traffic = "iptables -nvL|grep spt*"
# query port traffic
query_port_traffic_detail = "iptables -nvxL|grep spt*"


def checkUsedAndLimit():
    """
    检查流量限制
    :return:
    """
    # 读取端口信息
    port_info_dict = {}
    ss_dict = {}
    with open(port_path, "r", encoding='utf8') as fr:
        port_info_dict = dict(json.loads(fr.readline()))
    # 读取ss信息
    with open(ss_path, "r", encoding="utf8") as fr:
        ss_dict = dict(json.loads(fr.readline()))
    isUpdate = False
    for port, port_info in port_info_dict.items():
        if port_info.get("used", 0) > port_info.get("limit", 0):
            isUpdate = True
            # 更新port.json
            port_info.update({"useable": False})
            port_info_dict.update({port: port_info})
            # 更新ss.json
            ss_port = ss_dict.get("port_password", {})
            ss_port.pop(port)
            ss_dict.update({"port_password": ss_port})
    if isUpdate:
        with open(ss_path, "w", encoding='utf8') as fw:
            fw.write(json.dumps(ss_dict))
        with open(port_path, "w", encoding="utf8") as fw:
            fw.write(json.dumps(port_info_dict))


def checkSpeedLimit():
    """
    检查速度限制
    :return:
    """
    pass


def getPortTraffic():
    # 读取端口信息
    port_info_dict = {}
    with open(port_path, "r", encoding="utf8") as fr:
        port_info_dict = dict(json.loads(fr.readline()))
    # 获取端口流量信息
    res = subprocess.getoutput(query_port_traffic_detail)
    for item in res.split("\n"):
        # 提取查询结果
        item_res = re.sub("\s+", "#", item).split("#")
        if not item_res[0]: item_res.pop(0)
        count_watch = item_res[1]
        port_watch = item_res[9]
        # 将流量统计转换为MB，上取整
        count_watch = int(float(count_watch) / 1000 / 1000) + 1
        # 将port_watch转换为标准格式
        port_watch = port_watch.replace("spt:","")
        # 获取port.json中的信息
        port_info = port_info_dict.get(port_watch, {})
        port_info_used = int(port_info.get("used", 0))
        # 更新port.json的信息
        port_info_used += count_watch
        port_info.update({"used": port_info_used})
        port_info_dict.update({port_watch:port_info})
    # 写入port.json端口信息
    with open(port_path, "w", encoding="utf8") as fw:
        fw.write(json.dumps(port_info_dict))
    # 删除所有port信息，再重新添加，以重新计数
    delAllPortRule()
    addAllPortRule()


def delAllPortRule():
    """
    删除所有iptables规则
    :return:
    """
    port_info_dict = {}
    # 读取端口信息
    with open(port_path, "r", encoding="utf8") as fr:
        port_info_dict = dict(json.loads(fr.readline()))
    for port in port_info_dict.keys():
        command_string = "{}{}".format(del_iptable_pre, port)
        res = subprocess.getoutput(command_string)


def addAllPortRule():
    """
    添加所有端口规则
    :return:
    """
    port_info_dict = {}
    # 读取端口信息
    with open(port_path, "r", encoding="utf8") as fr:
        port_info_dict = dict(json.loads(fr.readline()))
    for port in port_info_dict.keys():
        command_string = "{}{}".format(add_iptable_pre, port)
        res = subprocess.getoutput(command_string)


def delOnePortRule(port):
    commad_string = "{}{}".format(del_iptable_pre, port)
    res = subprocess.getoutput(commad_string)


def addOnePortRule(port):
    command_string = "{}{}".format(add_iptable_pre, port)
    res = subprocess.getoutput(command_string)


if __name__ == '__main__':
    getPortTraffic()
