# encoding=utf8
import sys
import commands
import os
import re
import getpass
import time
import requests

current_user = getpass.getuser()


def get_pid(sys_port):
    output = commands.getoutput('ps aux|grep "[p]ython main.py"')
    lines = output.split('\n')
    ps_dict = {}
    re_obj = re.compile(r'%s +(\d+).*main\.py (\d+)$' % current_user)
    for line in lines:
        result = re_obj.findall(line)
        if not result:
            continue
        pid, port1 = result[0]
        ps_dict[port1] = pid

    return ps_dict.get(str(sys_port))


def usage():
    print 'Usage: restart_port.py <port|all> <port_from> <process_number>'
    sys.exit(1)


def kill_port(sys_port):
    pid = get_pid(sys_port)
    if pid:
        cmd = 'kill -9 %s' % pid
        print 'killing process ...'
        commands.getstatusoutput(cmd)
        print 'process %s for port %s is killed' % (pid, sys_port)


def restart_port(sys_port):
    pid = get_pid(sys_port)
    if pid:
        cmd = 'kill -9 %s' % pid
        commands.getstatusoutput(cmd)
        time.sleep(1)
    cmd = 'nohup python main.py %s >> logs/p_%s.log &' % (
        sys_port, sys_port)
    os.system(cmd)


def check_port_is_health(sys_port):
    need_check = True
    while need_check:
        time.sleep(1)
        try:
            response = requests.get('http://127.0.0.1:%s' % sys_port)
            if response.status_code == 200:
                need_check = False
            else:
                need_check = True
                print 'response.status_code=', response.status_code
        except Exception, e:
            print 'port=', sys_port, str(e)
            need_check = True
        if need_check:
            print 'port=', sys_port
            restart_port(sys_port)


if __name__ == '__main__':
    port_from = None
    process_number = None
    sys_port = None
    try:
        sys_port = sys.argv[1]
    except Exception as e:
        print(e)
        usage()
    if sys_port == 'all':
        try:
            port_from = int(sys.argv[2])
        except Exception as e:
            print(e)
            usage()
        try:
            process_number = int(sys.argv[3])
        except Exception as e:
            print(e)
            usage()
        for port in range(port_from, port_from + process_number):
            restart_port(port)
    elif sys_port == 'kill':
        try:
            port_from = int(sys.argv[2])
        except Exception as e:
            print(e)
            usage()
        try:
            process_number = int(sys.argv[3])
        except Exception as e:
            print(e)
            usage()
        for port in range(port_from, port_from + process_number):
            kill_port(port)
    else:
        restart_port(sys_port)
        check_port_is_health(sys_port)
