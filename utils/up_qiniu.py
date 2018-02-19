# --*--coding:utf-8--*--
import os
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import settings

class QINIU(object):
    def __init__(self):
        pass

    def upload(self, local_file_path, file_name):
        return_save_file_path = None
        try:
            # 需要填写你的 Access Key 和 Secret Key
            access_key = settings.QINIU_ACCESS_KEY
            secret_key = settings.QINIU_SECRET_KEY
            # 构建鉴权对象
            q = Auth(access_key, secret_key)
            # 要上传的空间
            bucket_name = settings.QINIU_BUCKET_NAME
            # 上传到七牛后保存的文件名
            key = file_name
            # 生成上传 Token，可以指定过期时间等
            token = q.upload_token(bucket_name, key, 3600)
            # 要上传文件的本地路径
            localfile = local_file_path
            ret, info = put_file(token, key, localfile)
            print(info)
            assert ret['key'] == key
            assert ret['hash'] == etag(localfile)
            return_save_file_path = file_name
            return return_save_file_path
        except Exception, e:
            print e
            return return_save_file_path


if __name__ == '__main__':
    obj = QINIU()
    obj.upload()
