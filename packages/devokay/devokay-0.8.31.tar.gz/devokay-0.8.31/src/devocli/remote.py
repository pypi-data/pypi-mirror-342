# -*- coding: UTF-8 -*-
# python3

import os
import paramiko
from datetime import datetime
import hashlib
import stat
from devolib.util_fs import path_join_one, path_exists, touch_dir
from devolib.util_log import LOG_E, LOG_D

# # devo - remote
# export REMOTE_HOST=47.116.--
# export REMOTE_USER=ro
# export REMOTE_PASS=lx--

# 示例用法
remote_host = os.getenv('REMOTE_HOST')
remote_user = os.getenv('REMOTE_USER')
remote_password = os.getenv('REMOTE_PASS')
remote_dir = '/root/backend/logs/lx-iot'

# 获取用户主目录
user_home = os.path.expanduser('~')

# 拼接 .devo/remote_logs 目录
local_dir = os.path.join(user_home, '.devo', 'remote_logs')

def __sync_remote_dir_to_local(remote_host, remote_user, remote_password, remote_dir, local_dir, since_date):

    LOG_D(f'remote_dir: {remote_dir}')
    LOG_D(f'local_dir: {local_dir}')

    touch_dir(local_dir)

    # 建立SSH连接
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=remote_host, username=remote_user, password=remote_password)

    # 创建SFTP客户端
    sftp_client = ssh_client.open_sftp()

    # 计算远程文件的MD5值
    def get_remote_file_md5(remote_path):
        md5 = hashlib.md5()
        with sftp_client.open(remote_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                md5.update(chunk)
        return md5.hexdigest()

    # 计算本地文件的MD5值
    def get_local_file_md5(local_path):
        md5 = hashlib.md5()
        with open(local_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                md5.update(chunk)
        return md5.hexdigest()

    # 【递归】递归同步远程目录到本地
    def sync_recursively(remote_dir, local_dir):
        for item in sftp_client.listdir_attr(remote_dir):
            remote_path = remote_dir + '/' + item.filename
            local_path = os.path.join(local_dir, item.filename)
            if stat.S_ISDIR(item.st_mode):
                # 如果是目录，递归同步子目录
                os.makedirs(local_path, exist_ok=True)
                sync_recursively(remote_path, local_path)
            else:
                # 如果是文件，检查最后修改时间是否晚于指定日期，然后下载到本地
                mtime = datetime.fromtimestamp(item.st_mtime)
                if mtime >= since_date:
                    # 计算远程文件的MD5值
                    remote_md5 = get_remote_file_md5(remote_path)
                    # 计算本地文件的MD5值
                    local_md5 = get_local_file_md5(local_path)
                    # 如果MD5值相同，则跳过同步
                    if remote_md5 == local_md5:
                        print(f"文件 '{item.filename}' MD5相同，跳过同步")
                        continue
                    sftp_client.get(remote_path, local_path)

    # sync_recursively(remote_dir, local_dir)

    # 【单层】下载远程目录到本地
    remote_files = sftp_client.listdir(remote_dir)
    # LOG_D(f'remote_files: {remote_files}')
    for item in sftp_client.listdir_attr(remote_dir):
        remote_path = os.path.join(remote_dir, item.filename)
        local_path = os.path.join(local_dir, item.filename)
        
        # 检查最后修改时间是否等于指定日期，然后下载到本地
        mtime = datetime.fromtimestamp(item.st_mtime)
        if mtime.date() == since_date.date():
            # 计算远程文件的MD5值
            remote_md5 = get_remote_file_md5(remote_path)
            if path_exists(local_path):
                # 计算本地文件的MD5值
                local_md5 = get_local_file_md5(local_path)
                # 如果MD5值相同，则跳过同步
                if remote_md5 == local_md5:
                    LOG_D(f"'{item.filename}' exists")
                    continue
            sftp_client.get(remote_path, local_path)

    # 关闭连接
    sftp_client.close()
    ssh_client.close()

'''
@cate bizs
@brief 清除所有改动
'''
def _dir_copy(args):
    global local_dir

    if args.dir_copy is None:
        return
    scope = args.dir_copy
    date_str = args.date

    local_dir = os.path.join(local_dir, scope, date_str)
    since_date = datetime.strptime(date_str, '%Y-%m-%d') # datetime.datetime(2024, 4, 9)  # 指定日期
    
    __sync_remote_dir_to_local(
        remote_host,
        remote_user,
        remote_password,
        remote_dir,
        local_dir,
        since_date)

'''
@cate cmds
@brief 远程日志助手
'''
class RemoteCmd:
    def __init__(self):
        pass

    def regist(self, subparsers):
        parser = subparsers.add_parser('remote', help='远程日志助手')
        parser.add_argument('-dc', '--dir_copy', type=str, default='logs', help='文件夹拷贝')
        parser.add_argument('-d', '--date', type=str, default='2024-01-01', help='指定日期')
        parser.add_argument('-fc', '--file_copy', type=int, default=1, help='文件拷贝')
        parser.set_defaults(handle=RemoteCmd.handle)

    @classmethod
    def handle(cls, args):
        _dir_copy(args)

    
if __name__ == '__main__':
    _dir_copy({})