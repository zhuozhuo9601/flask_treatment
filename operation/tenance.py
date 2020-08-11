import platform
import socket
from datetime import datetime
from random import randrange

from flask import Blueprint
from flask import jsonify
from flask import render_template
import psutil

opera = Blueprint('opera', __name__)


@opera.route('/index', methods=['GET'])
def opera_index():
    """
    进入页面
    :return:
    """
    boot_time = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time)
    now_time = datetime.now()
    delta_time = now_time - boot_time
    delta_time = str(delta_time).split('.')[0]
    return render_template('opera.html',
                           master=socket.gethostname(),
                           system=platform.system(),
                           machine=platform.machine(),
                           version=platform.version(),
                           architecture=platform.architecture(),
                           now_time=now_time,
                           boot_time=boot_time,
                           delta_time=delta_time)


@opera.route('/opera_meter', methods=['POST'])
def opera_meter():
    """
    返回CPU仪表盘数据
    :return:
    """
    cpu_count = psutil.cpu_count(logical=False)  # 1代表单核CPU，2代表双核CPU
    xc_count = psutil.cpu_count()  # 线程数，如双核四线程
    cpu_slv = round((psutil.cpu_percent(1)), 2)  # cpu使用率
    cpu_list = [cpu_count, xc_count, cpu_slv]
    return jsonify(cpu_list)


@opera.route('/opera_ram', methods=['POST'])
def opera_ram():
    """
    返回内存饼图数据
    :return:
    """
    memory = psutil.virtual_memory()
    total_nc = round((float(memory.total) / 1024 / 1024 / 1024), 2)  # 总内存
    used_nc = round((float(memory.used) / 1024 / 1024 / 1024), 2)  # 已用内存
    free_nc = round((float(memory.free) / 1024 / 1024 / 1024), 2)  # 空闲内存
    syl_nc = round((float(memory.used) / float(memory.total) * 100), 2)  # 内存使用率

    ret_list = [{'key': '总内存', 'name': total_nc}, {'key': '已用内存', 'name': used_nc}, {'key': '空闲内存', 'name': free_nc},
                {'key': '内存使用率', 'name': syl_nc}]

    return jsonify(ret_list)


@opera.route('/opera_hard', methods=['POST'])
def opera_hard():
    """
    返回内存饼图数据
    :return:
    """
    list = psutil.disk_partitions()  # 磁盘列表
    ilen = len(list)  # 磁盘分区个数
    i = 0
    retlist1 = []
    retlist2 = []
    while i < ilen:
        diskinfo = psutil.disk_usage(list[i].device)
        total_disk = round((float(diskinfo.total) / 1024 / 1024 / 1024), 2)  # 总大小
        used_disk = round((float(diskinfo.used) / 1024 / 1024 / 1024), 2)  # 已用大小
        free_disk = round((float(diskinfo.free) / 1024 / 1024 / 1024), 2)  # 剩余大小
        syl_disk = diskinfo.percent

        retlist1 = [i, list[i].device, total_disk, used_disk, free_disk, syl_disk]  # 序号，磁盘名称，
        retlist2.append(retlist1)
        i = i + 1

    return jsonify(retlist2)


@opera.route('/opera_net', methods=['POST'])
def opera_net():
    """
    获取网络信息
    :return:
    """
    # 获取网卡流量信息
    # recv = {}
    # sent = {}
    # data = psutil.net_io_counters(pernic=True)
    # interfaces = data.keys()
    # for interface in interfaces:
    #     recv.setdefault(interface, data.get(interface).bytes_recv)
    #     sent.setdefault(interface, data.get(interface).bytes_sent)
    # n_list = [interfaces, recv, sent]
    # 获取磁盘情况
    # name = psutil.disk_partitions()
    # name1 = psutil.disk_usage('/')
    # name2 = psutil.disk_io_counters()
    # 获取温度
    temperatures = psutil.sensors_temperatures()
    print(temperatures)

    fans = psutil.sensors_fans()
    print(fans)

    battery = psutil.sensors_battery()
    print(battery)
    n_list = [temperatures, fans, battery]

    # 获取系统的开机时间
    psutil.boot_time()
    # 获取连接系统的用户列表

    psutil.users()

    # 获取系统全部的进程信息

    psutil.pids()

    # 获取单个进程的信息

    p = psutil.Process(2399)

    return jsonify(n_list)


@opera.route('/opera_message', methods=['GET'])
def opera_message():
    boot_time = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time)
    now_time = datetime.now()
    delta_time = now_time - boot_time
    delta_time = str(delta_time).split('.')[0]
    return render_template('sysinfo.html',
                           master=socket.gethostname(),
                           system=platform.system(),
                           machine=platform.machine(),
                           version=platform.version(),
                           architecture=platform.architecture(),
                           now_time=now_time,
                           boot_time=boot_time,
                           delta_time=delta_time
                           )
