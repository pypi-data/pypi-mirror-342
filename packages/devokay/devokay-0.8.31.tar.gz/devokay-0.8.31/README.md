# Devokay

**影响python环境的亮点**
* 必须使用虚拟环境
* 环境变量不能有特殊版本python路径的干扰

## Install
```
# 安装 conda 命令行
brew install anaconda

# 使用 conda 安装 py312
conda create -n py312 python=3.12

# 启用 py312 环境
conda activate py312

# 安装 最新版本
pip install devokay==0.8.30
```


```
# ##############################################
# python 环境准备

# 安装 conda 命令行
#brew install anaconda

# 使用 conda 安装 py312
#conda create -n py312 python=3.12

# 启用 py312 环境
#conda activate py312

# 安装 最新版本
#pip install devokay==0.3.1
```

## Doc

### conda 的其他指令

```
# 显示可安装的python版本
conda search -f python

# 安装虚拟环境,名称为py2
conda create -n py27 python=2.7

# conda info –envs 或者conda env list 查询的虚拟环境

```

### ubuntu 安装 py312

```
# deadsnakes 团队维护了一个专门的 Launchpad PPA，可以帮助 Ubuntu 用户轻松安装最新版本的 Python 及附加模块。
sudo add-apt-repository ppa:deadsnakes/ppa

# 安装
sudo apt install python3.12

# 版本
python3.12 --version

# 安装 pip
sudo apt install python3-pip

# 配置环境
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 3
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 4
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.10 5
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 6
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.12 7

# 切换环境
sudo update-alternatives --config python
```

### ubuntu 安装包时指定源

```
pip install devokay==0.4.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**国内常用源**
```
豆瓣 ··············· https://pypi.douban.com/
华中理工大学 ········ https://pypi.hustunique.com/
山东理工大学 ········ https://pypi.sdutlinux.org/
中国科学技术大学 ···· https://pypi.mirrors.ustc.edu.cn/
阿里云 ············· https://mirrors.aliyun.com/pypi/simple/
清华大学 ··········· https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 本地py版本的问题

当 `python -V` 和 `python3 -V` 版本不一致的时候，按你的预期用指定方式安装包，否则运行时可能遇到包NotFound

```shell
python -m pip install ply # This is my case.
python3 -m pip install ply
```

### slimit 的限制

slimit 是一个针对 ECMAScript 5.1（即 ES5）规范的 JavaScript 解析器，因此它并不支持一些较新的语法特性，比如：
- let 和 const（在 ES6 中引入）
- 箭头函数 () => {}（也在 ES6 中引入）
- 类（class）和模块化（import/export）

## 减负方案

* 按需加载依赖：对于非核心功能的依赖，可以使用惰性加载。例如，只在需要时动态导入：
```
def some_feature():
    import heavy_library
    heavy_library.do_something()
```

* 功能模块化：将 CLI 的功能分成核心和扩展模块，用户可以选择只安装核心模块：
    - 在 pyproject.toml 中使用 optional-dependencies
    ```
    [project.optional-dependencies]
    extra_feature = ["heavy_library"]
    ```
    - 用户可以选择安装特定功能
    ```
    pip install mycli[extra_feature]
    ```


## 其他

**chmod 命令来修改目录中的文件权限，使其支持读和写（rw）权限。**
```
chmod -R u+rw,go+rw /path/to/directory
```