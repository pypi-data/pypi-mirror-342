# -*- coding: UTF-8 -*-
# python3

import os
import sys
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from itertools import islice

from devolib.util_fs import fullname_of_path, target_path_of_dirname
from devolib.util_log import LOG_D

'''
@brief oss管理工具
@need 确保已设置环境变量 OSS_ACCESS_KEY_ID OSS_ACCESS_KEY_SECRET

@TODO: 下载文件夹
https://help.aliyun.com/zh/oss/user-guide/how-to-upload-directories-to-and-download-directories-from-oss?spm=5176.8466032.bucket.dquestion-file-upload.50ed1450UKZMb9
@TODO: 分片上传
https://help.aliyun.com/zh/oss/user-guide/multipart-upload?spm=5176.8466032.bucket.dquestion-file-multipart.50ed1450UKZMb9
'''
class Oss:
    _auth = None
    _bucket = None

    _path_prefix = None

    _end_point = None
    _bucket_name = None
    _path_prefix = None

    def __init__(self, end_point, bucket_name, path_prefix=''):
        self._end_point = end_point
        self._bucket_name = bucket_name
        self._path_prefix = path_prefix

        if end_point is not None and bucket_name is not None:

            self._auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
            self._bucket = oss2.Bucket(self._auth, end_point, bucket_name)

        else:

            # print(f'end_point or bucket_name none')

            pass

    def _with_path_prefix(self, object_name):
        recal_object_name = None
        if len(self._path_prefix) > 0:
            recal_object_name = f'{self._path_prefix}/{object_name}'
        else:
            recal_object_name = object_name

        recal_object_name = recal_object_name.replace("\\","/")
        recal_object_name = recal_object_name.replace("//","/")
        recal_object_name = recal_object_name.replace("\\/","/")
        recal_object_name = recal_object_name.replace("/\\","/")

        return recal_object_name

    '''
    @brief 上传
    '''
    def put(self, file_path, object_name=''):
        if not object_name or len(object_name) == 0:
            object_name = fullname_of_path(file_path)
        object_name = self._with_path_prefix(object_name)

        ret = self._bucket.put_object_from_file(object_name, file_path)

        LOG_D(f'put_ret: {ret}')

        # https://fakeme.oss-cn-shanghai.aliyuncs.com/pcsdk/pcsdk-0.1.0.1-windows.zip
        if len(self._path_prefix) > 0:
            url = f'https://{self._bucket_name}.{self._end_point}/{self._path_prefix}/{object_name}'
        else:
            url = f'https://{self._bucket_name}.{self._end_point}/{object_name}'
        LOG_D(f'put_url: {url}')

    '''
    @brief 下载
    '''
    def get(self, file_path, object_name=''):
        if not object_name or len(object_name) == 0:
            object_name = fullname_of_path(file_path)
        object_name = self._with_path_prefix(object_name)
        
        ret = self._bucket.get_object_to_file(object_name, file_path)

        LOG_D(f'{ret}')

    '''
    @brief 列表
    '''
    def li(self):
        # oss2.ObjectIterator用于遍历文件。
        for b in islice(oss2.ObjectIterator(self._bucket), 10):
            print(b.key)

    '''
    @brief 删除
    '''
    def rm(self, object_name):
        # yourObjectName表示删除OSS文件时需要指定包含文件后缀，不包含Bucket名称在内的完整路径，例如abc/efg/123.jpg。
        self._bucket.delete_object(self._with_path_prefix(object_name))

# python src/devolib/utils/oss_util.py
'''
@brief xxxxx
@environment variables
export OSS_END_POINT=<your end point>
export OSS_BUCKET_NAME=<your bucket name>
export OSS_ACCESS_KEY_ID=<your access key id>
export OSS_ACCESS_KEY_SECRET=<your access key secret>
'''
if __name__ == '__main__':
    end_point = os.getenv('OSS_END_POINT')
    bucket_name = os.getenv('OSS_BUCKET_NAME')

    oss = Oss(end_point=end_point, bucket_name=bucket_name, path_prefix='pcsdk')

    res_path = target_path_of_dirname('res')
    file_path = f'{res_path}/oss_test.jpeg'
    oss.put(file_path=file_path)

    tmp_path = target_path_of_dirname('tmp')
    file_path = f'{tmp_path}/oss_test.jpeg'
    oss.get(file_path=file_path)



