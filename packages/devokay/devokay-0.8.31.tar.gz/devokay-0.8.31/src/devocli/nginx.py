# -*- coding: UTF-8 -*-
# python3

import os
import shutil
import subprocess
from devolib.util_log import LOG_CONSOLE
from devolib.util_str import replace_newline_with_comma

# 检查是否已安装 Nginx
def check_installed():
    try:
        subprocess.run(['nginx', '-v'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

# 检查 Nginx 是否正在运行
def check_running():
    try:
        subprocess.run(['sudo', 'systemctl', 'status', 'nginx'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def check_conf_files():
    try:
        current_folder = os.getcwd()
        conf_files = [f for f in os.listdir(current_folder) if f.endswith('.conf')]

        if conf_files:
            print("当前文件夹下存在以下 .conf 文件:")
            return True
        else:
            print("当前文件夹下不存在 .conf 文件")

    except Exception as e:
        print(f"检查 .conf 文件失败：{e}")

    return False

def add_current_folder_to_nginx():
    try:
        # 获取当前文件夹路径
        current_folder = os.getcwd()

        # 确定 Nginx 主配置文件路径（Ubuntu 默认路径）
        nginx_conf_path = '/etc/nginx/nginx.conf'

        # 备份原始配置文件
        nginx_conf_backup = nginx_conf_path + '.bak'
        shutil.copy2(nginx_conf_path, nginx_conf_backup)

        # 编辑 Nginx 主配置文件，添加 include 指令
        with open(nginx_conf_path, 'a') as f:
            f.write(f'\n\n# Include current folder\n')
            f.write(f'include {current_folder}/*.conf;\n')

        print(f"已将 {current_folder} 添加到 Nginx 主配置文件中")

    except Exception as e:
        print(f"添加到 Nginx 主配置文件失败：{e}")

def get_nginx_pid():
    try:
        # 使用 pgrep 命令获取 nginx 进程 ID
        pid_result = subprocess.run(['pgrep', 'nginx'], check=True, stdout=subprocess.PIPE, text=True)
        nginx_pid = pid_result.stdout.strip()
        
        if nginx_pid:
            return replace_newline_with_comma(nginx_pid)
        else:
            # print("Nginx 未找到运行中的进程")
            pass

    except subprocess.CalledProcessError as e:
        print(f"获取 Nginx 进程 ID 失败：{e}")

    return None

###################################

def handle_install():
    if check_installed():
        LOG_CONSOLE(f'Nginx is already installed, abort.')
        return
    
    try: # 使用 apt-get 安装 nginx
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', 'nginx', '-y'], check=True)
        LOG_CONSOLE("Install successfully.")
    except subprocess.CalledProcessError as e:
        LOG_CONSOLE(f"Install failed: {e}")


def handle_start():
    if check_running():
        LOG_CONSOLE(f'Already running, abort.')
        return
    
    try:
        subprocess.run(['sudo', 'systemctl', 'start', 'nginx'], check=True)
        print("Nginx 启动成功！")
    except subprocess.CalledProcessError as e:
        print(f"Nginx 启动失败：{e}")

def handle_status():
    LOG_CONSOLE(f'程序  : /usr/sbin/nginx')
    LOG_CONSOLE(f'配置  : /etc/nginx')
    LOG_CONSOLE(f'静态  : /usr/share/nginx')
    LOG_CONSOLE(f'日志  : /var/log/nginx')

    if check_running():
        LOG_CONSOLE(f'运行  : on')

        LOG_CONSOLE(f'进程  : {get_nginx_pid()}')
    else:
        LOG_CONSOLE(f'运行  : off')

def handle_reload():
    if not check_running():
        LOG_CONSOLE(f'Not running, abort.')
        return
    
    try:
        subprocess.run(['sudo', 'systemctl', 'reload', 'nginx'], check=True)
        LOG_CONSOLE("Done")
    except subprocess.CalledProcessError as e:
        LOG_CONSOLE(f"Reload error: {e}")

def handle_stop():
    if not check_running():
        LOG_CONSOLE(f'Not running, abort.')
        return
    
    try:
        subprocess.run(['sudo', 'systemctl', 'stop', 'nginx'], check=True)
        print("Nginx 停止成功！")
    except subprocess.CalledProcessError as e:
        print(f"Nginx 停止失败：{e}")

def handle_restart():
    handle_stop()
    handle_start()

#######################################

def cmd_handle(args):
    if args.run is not None:

        if args.run == 'install':
            handle_install()
        elif args.run == 'status':
            handle_status()
        elif args.run == 'start':
            handle_start()
        elif args.run == 'stop':
            handle_stop()
        elif args.run == 'reload':
            handle_reload()
        elif args.run == 'restart':
            handle_restart()
        elif args.run == 'add-conf-dir': # 添加配置文件夹路径
            if check_conf_files():
                add_current_folder_to_nginx()

def cmd_regist(subparsers):
    parser = subparsers.add_parser('nginx', help='nginx助手')
    parser.add_argument('-r', '--run', type=str, default='.', help='执行命令')
    parser.set_defaults(handle=cmd_handle)
    
if __name__ == '__main__':
    # scan_files(folder_path, suffixes)
    pass