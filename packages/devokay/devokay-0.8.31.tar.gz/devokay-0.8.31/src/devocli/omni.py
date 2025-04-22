# -*- coding: UTF-8 -*-
# python3

import os

from devolib.util_fs import path_join_one, path_exists
from devolib.util_httpc import GET, POST
from devolib.util_json import json_from_str
from devolib.util_log import LOG_D, LOG_E
from devolib.util_cache import cache_has, cache_get, cache_set

# devo
# export OMNI_ENDPOINT=--
# export OMNI_ENV_ID=--
# export OMNI_TOKEN=--

class Environment:
    pass

class Config:
    _host = None
    _path = '/v1/get_config/'
    _env_id = None

    _env_info = {}
    def __init__(self, host):
        self._host = host
        
    def env(self):
        # TODO: 未来支持env 切换
        self._env_id = os.getenv('OMNI_ENV_ID')
        if self._env_id is None:
            raise Exception("`OMNI_ENV_ID` not set")

        # 检查缓存
        if cache_has(self._env_id):
            env_info_str = cache_get(self._env_id)
        else:
            # 远端拉取
            env_info_str = GET(self._host, f'{self._path}{self._env_id}')

        if env_info_str is not None:
            self._env_info = json_from_str(env_info_str)

            LOG_D(f'env_info: {self._env_info}')

            cache_set(self._env_id, env_info_str)
        else:
            raise Exception(f'env info get failed: {self._env_id}')

    def data(self):
        return self._env_info['data']
    def host(self):
        data = self.data()
        sdk_hosts = data['sdk_hosts']
        return sdk_hosts[0]
    def env_id(self):
        data = self.data()
        return data['env_id']
    def app_id(self):
        data = self.data()
        return data['app_id']
    def game_id(self):
        data = self.data()
        game_config = data['game_config']
        return game_config['game_id']

    def package_name(self):
        data = self.data()
        pc_config = data['pc_config']
        return pc_config['package_name']
    
    def channel(self):
        data = self.data()
        pc_config = data['pc_config']
        return pc_config['channel']

    def common_data(self):
        return {
            'env_id': self._env_id,
            'package_name': self.package_name(),
            'app_version': '0.1.1.1',
            'channel_id': self.channel(),
            'device_id': '4634d336-196d-47b2-9632-0c7e28688d31',
            'lang': 'en',
            'game_id': f'{self.game_id()}',
            'os': 'win',
            "sdk_version": "test"
        }

class Api:
    _path = None
    _config = None
    _host = None

    def __init__(self, config, path, host=None):
        self._config = config
        self._path = path
        self._host = host

    '''
    @brief 执行api
    '''
    def go(self, params):
        req_params = {
            'app_id': self._config.app_id(),
            'common_event_data': self._config.common_data()
        }
        req_params.update(params)

        headers = {}
        if 'login' not in self._path:
            headers.update({ 'Authorization': os.getenv('OMNI_TOKEN') })

            if 'token' in params:
                headers.update({ 'Authorization': params.get('token') })

        if self._host is None:
            self._host = self._config.host()
            
        return POST(self._host, self._path, req_params, headers)

host = os.getenv('OMNI_ENDPOINT')
config = Config(host=host)

api_omni_login = Api(config, '/v1/passport/mobile/login')
api_login = Api(config, '/v1/account/mobile/login')

api_unbind_all = Api(config, '/v1/account/mobile/unbind')

api_account_delete = Api(config, '/v1/app_user/delete', host)

'''
@brief 处理env
'''
def handle_env():
    global config
    config.env()

'''
@brief 账号解绑
'''
def account_unbind_all(args):
    if args.account_unbind_all is not None:
       api_unbind_all.go({'acc_id': args.account_unbind_all, 'token': args.token}) 

'''
@brief 邮箱注册
'''
def account_register(args):
    if args.account_register is not None:
        # omni登陆
        res = api_omni_login.go({'account': args.account_register, 'pass': '888888', 'login_type': '3'}) 
        if res.code == 200: # {"code":200,"data":{"omni_id":"1200005","omni_token":"BN5p70R1MaetQtk49PShzpgFLB6OlnPiP7fGKLfLwIVyqLsq7VhSwFDlyMHBrQlK","expire_time":600,"is_reg":true}}
            # acc登陆
            data = res.get('data')
            omni_id = data.get('omni_id')
            omni_token = data.get('omni_token')
            expire_time = data.get('expire_time')
            is_reg = data.get('is_reg')

            api_login.go({'user_id': omni_id, 'user_token': omni_token, 'login_type': ''})

'''
@brief 账号删除
'''
def account_delete(args):
    if args.account_delete is not None:
        api_account_delete.go({'acc_id': args.account_delete, 'env': 'dev', 'desc': 'test by sevenli', 'token': 'TRSbYcRYZWFWbdWHKNb6VQSuM8tJ45GkLXnkD6aM'}) 

'''
@cate cmds
@brief omni助手
'''
class OmniCmd:
    def __init__(self):
        pass

    def regist(self, subparsers):
        parser = subparsers.add_parser('omni', help='omni助手')

        # 命令参数
        parser.add_argument('-aua', '--account_unbind_all', type=str, default=None, help='账号解绑: origin acc_id')
        parser.add_argument('-ar', '--account_register', type=str, default=None, help='注册账号: email or phone')
        parser.add_argument('-ad', '--account_delete', type=str, default=None, help='删除账号: acc_id')

        # 纯参数
        parser.add_argument('-t', '--token', type=str, default=None, help='--')


        # parser.add_argument('-e', '--email', type=str, default='', help='注册账号')

        parser.set_defaults(handle=OmniCmd.handle)

    @classmethod
    def handle(cls, args):
        # 配置拉取
        handle_env()
        # 解绑
        account_unbind_all(args)
        # 注册
        account_register(args)
        # 删账号
        account_delete(args)

    