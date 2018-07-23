# --coding:utf-8--
import os

MEMCACHE_HOSTS = ('127.0.0.1:11211',)
SITE_PORT = 80
SECRET_KEY = ''
MONGODB_ADDRESS = '127.0.0.1'
MONGODB_PORT = 27017
MEMCACHE_SERVER = '127.0.0.1'
MEMCACHE_PORT = 11211
MEMCACHE_EXPIRE_TIME = 120
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 1
DOMAIN_NAME = 'http://127.0.0.1:3344'
DEBUG = True

project_setting = dict(
    debug=True,
    template_path='template',
    static_path='static',
    static_url_prefix='/static/',
    cookie_secret=''
)

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
        # 'expires':None, #秒
    },
}

# 七牛配置
QINIU_ACCESS_KEY = ''
QINIU_SECRET_KEY = ''
QINIU_BUCKET_NAME = ''
QINIU_USER_DOMAIN = ''
LOCAL_TMP_PATH = ''

# 又拍配置

# SMTP 账号设置
SMTP_ADD = ''
SMTP_PORT = ''
SMTP_USER = ''
SMTP_PASS = ''
REDIS_QUEUE_NAME = ""

# 发送邮件设置
EMAIL_PUSH_SUBJECT = u''
EMAIL_PUSH_SENDER = [u"", u'']

# luosimao设置
LUOSIMAO_CHECK_ADDRESS = ''
LUOSIMAO_API_KEY = ''

# 网站名称
WEB_NAME = u''
WEB_DOMAIN_NAME = ''

# 第三方登录设置
# QQ
QQ_APP_ID = ''
QQ_APPKey = ''
QQ_CollBackUrl = ''

# 支付宝支付设置
ALIPAY_APPID = ''
ALIPAY_GETWAY = ''
ALIPAY_APP_PRIVATE_KEY_PATH = os.path.join('pay', 'alipay', 'app_private_key.pem')
ALIPAY_APP_PUBLIC_KEY_PATH = os.path.join('pay', 'alipay', 'app_public_key.pem')
ALIPAY_SIGN_TYPE = "RSA2"
ALIPAY_RETURN_URL = ""

try:
    import local_setting
except Exception as e:
    print("local setting load fail", str(e))
