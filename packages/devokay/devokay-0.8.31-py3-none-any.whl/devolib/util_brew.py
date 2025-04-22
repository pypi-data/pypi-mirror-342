

import subprocess

class Brew:
    def __init__(self):
        self.brew_command = "brew"

    def _run_command(self, *args):
        try:
            result = subprocess.run([self.brew_command] + list(args), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Command failed with error: {e.stderr}"


# MARK: 基础命令
    '''
    @brief 安装指定的包
    '''
    def install(self, package_name):
        print(f"安装 {package_name} 中...")
        return self._run_command("install", package_name)

    '''
    @brief 卸载指定的包
    '''
    def uninstall(self, package_name):
        print(f"卸载 {package_name} 中...")
        return self._run_command("uninstall", package_name)

    '''
    @brief 更新 Homebrew 及其所有包
    '''
    def update(self):
        print("更新 Homebrew 中...")
        return self._run_command("update")

    '''
    @brief 升级 Homebrew 已安装的包
    '''
    def upgrade(self):
        print("升级已安装的软件包中...")
        return self._run_command("upgrade")

    '''
    @brief 列出已安装的包
    '''
    def list_installed(self):
        print("列出已安装的软件包...")
        return self._run_command("list")

    '''
    @brief 搜索指定的包
    '''
    def search(self, package_name):
        print(f"搜索 {package_name} 中...")
        return self._run_command("search", package_name)
    
# MARK: 封装命令