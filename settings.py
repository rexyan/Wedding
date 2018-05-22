# --coding:utf-8--
import os

MEMCACHE_HOSTS = ('127.0.0.1:11211',)
SITE_PORT = 80
SECRET_KEY = 'd96f097c-4867-4b1b-3859-375838cd69c4'
MONGODB_ADDRESS = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'mobi'
MEMCACHE_SERVER = '127.0.0.1'
MEMCACHE_PORT = 11211
MEMCACHE_EXPIRE_TIME = 120
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 1
DOMAIN_NAME = 'http://127.0.0.1:3344'
DEBUG=True

project_setting = dict(
    debug=True,
    template_path='template',
    static_path='static',
    static_url_prefix='/static/',
    cookie_secret='2379874hsdhf0234990sdhsaiuofyasop977djdj'
)

# SESSION插件配置
# project_setting['pycket'] = {
#     'engine': 'redis',
#     'storage': {
#         'host': REDIS_HOST,
#         'port': REDIS_PORT,
#         'db_sessions': 10,
#         'db_notifications': 11
#     }
# }
project_setting['pycket'] = {
    'engine': 'redis',
    'storage': {
        'host': 'localhost',
        'port': 6379,
        'db_sessions': 10,
        'db_notifications': 11,
        'max_connections': 2 ** 31,
    },
    'cookies': {
        # 设置过期时间
        'expires_days': 2,
        #'expires':None, #秒
    },
}

# 七牛配置
QINIU_ACCESS_KEY = 'Pn_iwLLyDJWqohfT0fF1YlIjfD9u-L1SP76LyCpT'
QINIU_SECRET_KEY = 'yN8Z8zR56DaQDmIxg77kCJ0BwHAqUauVzPeePg0d'
QINIU_BUCKET_NAME = 'rexyan'
QINIU_USER_DOMAIN = 'http://ovsf3r7sm.bkt.clouddn.com'
LOCAL_TMP_PATH = ''

# 又拍配置

# SMTP 账号设置
SMTP_ADD = 'smtp.exmail.qq.com'
SMTP_PORT = 465
SMTP_USER = 'push@kindle15.com'
SMTP_PASS = '18525350524Yrs'
REDIS_QUEUE_NAME = "REDIS_QUEUE_SEND_EMAIL"

# 发送邮件设置
EMAIL_PUSH_SUBJECT = u'Kindle15电子书推送'
EMAIL_PUSH_SENDER = [u"kinlde15推送", u'push@kindle15.com']

# luosimao设置
LUOSIMAO_CHECK_ADDRESS = 'https://captcha.luosimao.com/api/site_verify'
LUOSIMAO_API_KEY = '0ff0f6b9f68ba28f8eaa7bd4914f78b0'


# 网站名称
WEB_NAME = u'春色撩人'
WEB_DOMAIN_NAME = 'test.com'

# 第三方登录设置
# QQ
QQ_APP_ID = '101463730'
QQ_APPKey = '1807ed84146dc54df99bc24b6c169dcc'
QQ_CollBackUrl = 'http://'+WEB_DOMAIN_NAME+'/check_qq'

# 支付宝支付设置
ALIPAY_APPID = 2016080300160299
ALIPAY_GETWAY = 'https://openapi.alipaydev.com/gateway.do'
ALIPAY_APP_PRIVATE_KEY_PATH = os.path.join('pay', 'alipay', 'app_private_key.pem')
ALIPAY_APP_PUBLIC_KEY_PATH = os.path.join('pay', 'alipay', 'app_public_key.pem')
ALIPAY_SIGN_TYPE = "RSA2"
ALIPAY_RETURN_URL = "http://"+WEB_DOMAIN_NAME+"/alipay_success/"
