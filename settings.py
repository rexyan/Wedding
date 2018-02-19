# --coding:utf-8--

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

project_setting = dict(
    debug=True,
    template_path='template',
    static_path='static',
    static_url_prefix='/static/',
    cookie_secret='2379874hsdhf0234990sdhsaiuofyasop977djdj'
)

# SESSION插件配置
project_setting['pycket'] = {
    'engine': 'redis',
    'storage': {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'db_sessions': 10,
        'db_notifications': 11
    }
}

# 七牛配置
QINIU_ACCESS_KEY = 'Pn_iwLLyDJWqohfT0fF1YlIjfD9u-L1SP76LyCpT'
QINIU_SECRET_KEY = 'yN8Z8zR56DaQDmIxg77kCJ0BwHAqUauVzPeePg0d'
QINIU_BUCKET_NAME = 'rexyan'
QINIU_USER_DOMAIN = 'http://ovsf3r7sm.bkt.clouddn.com'
LOCAL_TMP_PATH = ''

# 又拍配置

# 允许上传类型
UP_FILE_TYPE = [u'mobi', u'pdf', u'txt', u'equb']


# SMTP 账号设置
SMTP_ADD = 'smtp.exmail.qq.com'
SMTP_PORT = 25
SMTP_USER = 'push@kindle15.com'
SMTP_PASS = '18525350524Yrs'


# 发送邮件设置
EMAIL_PUSH_SUBJECT = u'Kindle15电子书推送'
EMAIL_PUSH_SENDER = [u"kinlde15推送", u'push@kindle15.com']

# luosimao设置
LUOSIMAO_CHECK_ADDRESS = 'https://captcha.luosimao.com/api/site_verify'
LUOSIMAO_API_KEY = '0ff0f6b9f68ba28f8eaa7bd4914f78b0'