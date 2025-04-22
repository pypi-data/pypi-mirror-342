
# -*- coding: UTF-8 -*-
# python3

from concurrent.futures import ThreadPoolExecutor
import json
import os
import hashlib
import shutil
import stat

from devolib.util_log import LOG_E

# @brief get user home directory:
# Windows: C:\Users\<username>
# macOS: /Users/<username>
# linux: /home/<username>
def path_home():
    return os.path.expanduser("~")

'''
@brief return if path exists
'''
def has_dir(path):
    return os.path.exists(path) and os.path.isdir(path)

@DeprecationWarning
def has_path(path):
    return os.path.exists(path)

def path_exists(path):
    return os.path.exists(path)

def is_file(path):
    return os.path.exists(path) and os.path.isfile(path)

def has_file(path):
    return is_file(path)

'''
@brief remove dir and sub dirs (Not support Permission Promoted)
'''
def remove_dir(dir_path):
    try:
        shutil.rmtree(dir_path)
    except FileNotFoundError:
        LOG_E(f'{dir_path} not found')
    except PermissionError:
        LOG_E(f'{dir_path} no permission')
    except Exception as e:
        LOG_E(f'{e}')

'''
@brief 拷贝文件夹
'''
def copy_dir(src, dst):
    if not has_dir(src):
        return

    if has_dir(dst):
        remove_dir(dst)

    if not os.path.exists(dst):
        os.makedirs(dst)

    shutil.copytree(src, dst, dirs_exist_ok=True)

'''
@brief remove file
'''
def remove_file(file_path):
    try:
        if os.path.exists(file_path):
            # 修改文件权限为可读写
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
            # 删除文件
            os.remove(file_path)
    except OSError as e:
        LOG_E(f'{e}')

def remove_files(file_paths):
    for path in file_paths:
        remove_file(path)

'''
@brief Make path if not exists
'''
def touch_dir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            LOG_E(f'{e}')

'''
@brief 获取文件路径的路径
'''
def dir_of_file(file_path):
    return os.path.dirname(file_path)

'''
@brief 尝试创建文件所在的目录（如果存在则忽略）
'''
def touch_dir_of_file(file_path):
    if os.path.exists(file_path):
        return
    else:
        file_dir = dir_of_file(file_path)

        touch_dir(file_dir)
    
'''
@brief Copy file, with `makepath`
'''
def copy_file(path, dir):
    path = path.replace("\\","/")
    dir = dir.replace("\\","/")

    touch_dir(dir)

    try:
        shutil.copy(path, dir)
    except Exception as e:
        LOG_E(f'{e}')

'''
@brief Copy files by foreach
'''
def copy_files(file_paths, output_dir):
    for path in file_paths:
        copy_file(path, output_dir)

'''
@brief Copy files ext by foreach
'''
def copy_files_ext(file_dir, file_rel_objs, output_dir):
    for obj in file_rel_objs:
        copy_file(f"{file_dir}/{obj['path']}", os.path.dirname(f"{output_dir}/{obj['path']}"))

'''
@brief Copy files by concurrent, but still sync invoking!!!
'''
def copy_files_quick(file_dir, file_rel_objs, output_dir):
    touch_dir(output_dir)

    try:
        with ThreadPoolExecutor() as executor:
            executor.map(lambda obj: copy_file(f"{file_dir}/{obj['path']}", os.path.dirname(f"{output_dir}/{obj['path']}")), file_rel_objs)
    except Exception as e:
        LOG_E(f'{e}')

'''
@brief Make path from drive
'''
def join_root(refer_path, folders):
    current_drive = os.path.splitdrive(refer_path)[0]
    # current_drive = os.path.splitdrive(os.getcwd())[0]
    if len(folders) == 0:
        return current_drive

    return os.path.join(f'{current_drive}\\', *folders)

'''
@brief make path from multi dirs
'''
def path_join_one(path, sub):
    return os.path.join(path, sub)

def path_join_many(path, subs):
    return os.path.join(path, *subs)

'''
@brief get md5 of file
'''
def md5_of_file(path):
    try:
        hash_md5 = hashlib.md5()
        with open(path, "rb") as f:
            # 使用read（）一次读取文件的内容，并在每次迭代中更新哈希对象
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except FileNotFoundError:
        if len(path) > 255:
            LOG_E(f"Get file md5 failed(File path size exceed): {path}")
        else:
            LOG_E(f"Get file md5 failed(File not found): {path}")
    except Exception:
        LOG_E("Get file md5 failed(Others error): {path}")
    return ""

'''
@brief size of file, in bytes,
'''
def size_of_file(path):
    try:
        return os.stat(path).st_size
    except Exception:
        LOG_E("Get file size failed: Others error")
    return 0

'''
@brief write string to file
'''
def write_file(file_path, content_str=''):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content_str)

def write_bytes_to_file(file_path, content_bytes):
    with open(file_path, 'wb') as f:
        f.write(content_bytes)

def read_bytes_of_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except IOError as e:
        print(f"Error: Could not read file '{file_path}'. Details: {e}")
        return None
    
def read_of_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except IOError as e:
        print(f"Error: Could not read file '{file_path}'. Details: {e}")
        return None

'''
@brief read file to json object
'''
def json_from_file(file_path):
    json_obj = {}
    try:
        with open(file_path, 'r') as file:
            json_obj = json.load(file)
    except FileNotFoundError:
        LOG_E(f'{file_path} not exists')
    except json.JSONDecodeError as e:
        LOG_E(f'Error decoding JSON: {e}')

    return json_obj

def json_to_file(file_path, json_data):
    write_file(file_path, json.dumps(json_data))

'''
@brief fullname == filename with suffix
'''
def fullname_of_path(path):
    return os.path.basename(path)

'''
@brief filename == filename without suffix
'''
def filename_of_path(path):
    return os.path.splitext(os.path.basename(path))[0]

'''
@brief 传入文件夹名，内部通过获取当前路径，找到对应文件夹名称，并返回对应的path
'''
def target_path_of_dirname(folder_name):
    current_path = os.getcwd()  # 获取当前路径
    while True:
        folder_path = os.path.join(current_path, folder_name)  # 拼接文件夹路径
        if os.path.isdir(folder_path):  # 判断路径是否为文件夹
            return folder_path
        # 如果已经到达根目录，则退出循环
        if current_path == os.path.dirname(current_path):
            break
        # 否则继续向上查找
        current_path = os.path.dirname(current_path)
    return None  # 如果未找到文件夹，则返回 None

'''
@brief 

# 测试函数
folder = "/path/to/your/folder"
extension = ".txt"
files = get_files_by_extension(folder, extension)
for file in files:
    print(file)
'''
def list_files(in_folder, by_extension):
    # 列出文件夹中的所有文件
    all_files = os.listdir(in_folder)
    
    # 过滤出满足后缀名条件的文件
    filtered_files = [file for file in all_files if file.endswith(by_extension)]
    
    # 获取文件的完整路径并获取创建时间
    files_with_creation_time = []
    for file in filtered_files:
        file_path = os.path.join(in_folder, file)
        creation_time = os.path.getctime(file_path)
        files_with_creation_time.append((file_path, creation_time))
    
    # 按创建时间升序排列
    sorted_files = sorted(files_with_creation_time, key=lambda x: x[1])
    
    # 返回排序后的文件列表
    return [file[0] for file in sorted_files]

"""
@brief 设置文件为可读可写
"""
def normalize_file(file_path):
    if is_file(file_path):
        os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)  # 用户可读可写
    else:
        print(f"normalize file skipped: {file_path}")

if __name__ == '__main__':
    path = target_path_of_dirname('src')

    print(f'path: {path}')

    path = target_path_of_dirname('devokay-py')

    print(f'path: {path}')