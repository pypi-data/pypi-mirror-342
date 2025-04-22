



# - 安装最新版本
# sudo apt install -y mysql-server

# - 安装指定版本
# sudo apt install -y mysql-server-8.0

# - 安装完成后，MySQL服务会自动启动，未启动则使用以下命令启动MySQL服务：
# sudo systemctl start mysql

# - 将MySQL设置为开机自启动：
# sudo systemctl enable mysql

# - 检查MySQL状态
# sudo systemctl status mysql

# - 修改密码、权限, 默认安装是没有设置密码的，需要我们自己设置密码。
#   - 登录mysql，在默认安装时如果没有让我们设置密码，则直接回车就能登录成功。
#   mysql -uroot -p
#   - 设置密码 mysql8.0
#   ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '新密码';
#   - 设置密码 mysql5.7
#   set password=password('新密码');
#   - 配置IP 5.7
#   grant all privileges on *.* to root@"%" identified by "密码";
#   - 刷新缓存
#   flush privileges;

# 注意：配置8.0版本参考：我这里通过这种方式没有实现所有IP都能访问；我是通过直接修改配置文件才实现的，MySQL8.0版本把配置文件 my.cnf 拆分成mysql.cnf 和mysqld.cnf，我们需要修改的是mysqld.cnf文件：
# sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf

# 重启MySQL重新加载一下配置：
# sudo systemctl restart mysql


# 步骤1：下载MySQL安装包
# https://blog.csdn.net/weixin_45626288/article/details/133220238