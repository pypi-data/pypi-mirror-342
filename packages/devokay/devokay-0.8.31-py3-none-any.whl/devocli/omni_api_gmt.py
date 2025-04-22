#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import parse

from devolib.util_httpc import GET, POST
from devolib.util_log import LOG_D, LOG_E
from devolib.util_json import json_from_str

HEADERS = {
	'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF',
	'Authorization': '9uIjoiYXAtc291dGhlYXN0LTEiLCJhY2',
	'Content-Type': 'application/json'
}

SDK_SVR = 'https://app-api-dev.aomengni.com'
API_GM_APP_USER_DELETE = '/v1/gm/app_user/delete'

class OmniApiGmt:

	# gm接口：删号
	@classmethod
	def gm_user_delete( cls , app_id, acc_id ):
		req_params = { 'app_id': app_id, 'acc_id': acc_id }
		res = POST(SDK_SVR, API_GM_APP_USER_DELETE, req_params, HEADERS)
		res_json = json_from_str(res)

		code = res_json['code']
		data = res_json['data']
		result = data['result']
		LOG_D(f'res: {res}, code: {code}, result: {result}')


if __name__ == '__main__':
	OmniApiGmt.gm_user_delete('10001', '29')