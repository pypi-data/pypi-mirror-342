# -*- coding: UTF-8 -*-
# python3

import subprocess

from devolib.util_fs import path_join_one, path_exists
from devolib.util_log import LOG_D
from devolib.util_fs import path_home, remove_dir

EXPORT_ROOT_DIR='EXPORT'
BUILD_ROOT_DIR='BUILD'
ARCHIVE_ROOT_DIR='ARCHIVE'

CMAKE_CONFIG_FILE='CMakeLists.txt'

class CMakeProject:
    _src_dir = None
    _proj_name = None

    _cpm_dir = None

    def __init__(self, source_dir, proj_name):
        ''' source_dir CMakeLists.txt所在目录 '''
        self._src_dir = source_dir
        self._proj_name = proj_name

        self._cpm_dir = f"{path_home()}/.cache/CPM"

        LOG_D(f"source dir: {self._src_dir}")
        LOG_D(f"project name: {self._proj_name}")
        LOG_D(f"cpm dir: {self._cpm_dir}")

    def run_cmake(self, cmake_args=None):
        """ 运行CMake的生成步骤 """
        if cmake_args is None:
            cmake_args = []
        cmd = ['cmake', self.source_dir] + cmake_args
        LOG_D(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, cwd=self._src_dir, check=True)

    def build(self, target=None):
        """ 编译目标 """
        cmd = ['cmake', '--build', self._src_dir]
        if target:
            cmd += ['--target', target]
        LOG_D(f"Running build: {' '.join(cmd)}")
        subprocess.run(cmd, cwd=self._src_dir, check=True)

    def clean(self):
        """ 清理构建目录 """
        cmd = ['cmake', '--build', self._src_dir, '--target', 'clean']
        LOG_D(f"Running clean: {' '.join(cmd)}")
        subprocess.run(cmd, cwd=self._src_dir, check=True)


    """ 工程导出 """
    def export(self):
        export_dir = f'{EXPORT_ROOT_DIR}/{self._proj_name}'
        remove_dir(export_dir)

        cmd = ['cmake', '-LA', '-G', 'Xcode', '-H.', '-B', export_dir]
        LOG_D(f"cmake export: {' '.join(cmd)}")
        subprocess.run(cmd, cwd=self._src_dir, check=True)


# cmake -G "Visual Studio 17 2022" -A x64 -B build
# -G "Visual Studio 17 2022" 指定了 Visual Studio 2022
# -A x64 指定了目标平台架构（可以选择 Win32 或 x64）
# -B build 指定了构建目录，这里会将生成的 Visual Studio 工程文件放在 build 目录中。

# cmake -G "Visual Studio 16 2019" -A x64 .



# 设置构建输出目录
# set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
# set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
# set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 设置不同构建配置下的输出目录
# set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/lib/Debug)
# set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/bin/Debug)
# set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/bin/Debug)
# set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/lib/Release)
# set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/bin/Release)
# set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/bin/Release)
    


# cmake -G "Visual Studio 17 2022" -A x64 -B build -D CMAKE_ARCHIVE_OUTPUT_DIRECTORY=path/to/output/lib -D CMAKE_LIBRARY_OUTPUT_DIRECTORY=path/to/output/bin -D CMAKE_RUNTIME_OUTPUT_DIRECTORY=path/to/output/bin
    