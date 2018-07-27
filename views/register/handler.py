# --*--coding:utf-8--*--
from views.base import BaseHandler
from models.Base import session
import json
import time
import requests
import settings
from utils.auth import sec_pass
from views.user.model import Users
from views.email import utils as redis_queue_send_email


# 注册页
class IndexRegisterHandler(BaseHandler):
    def get(self):
        self.render('index_register.html')

    def post(self):
        # 注册
        try:
            # 获取前端传来的参数
            data = json.loads(self.get_argument('data'))
            luosimao_rep = data.get('luosimao_rep')
            check_json = {
                'api_key': settings.LUOSIMAO_API_KEY,
                'response': luosimao_rep
            }
            check_response = requests.post(settings.LUOSIMAO_CHECK_ADDRESS, data=check_json)
            if json.loads(check_response.content).get('res') != 'success':
                code = 3
                msg = u"人机验证失败"
                self.write_json(msg, code=code)
                return
            data.pop('luosimao_rep')
            data['UserAge'] = int(data['UserAge'])
            data['UserPwd'] = sec_pass(data['UserPwd'])
            data['UserLastVisitIP'] = self.request.remote_ip
            active_hash_code = sec_pass(str(int(time.time())))
            data['UserHashCode'] = active_hash_code
            session.add(Users(**data))
            session.commit()
            active_url = '<a href=' + 'http://' + settings.WEB_DOMAIN_NAME + \
                         '/active_email/?address=' + data['UserEmail'] + \
                         '&hash_code=' + active_hash_code + '>http://' + settings.WEB_DOMAIN_NAME + \
                         '/active_email/?address=' + data['UserEmail'] + \
                         '&hash_code=' + active_hash_code + '</a>'
            content = u'''
<html>
<body>
<p>亲爱的用户：</p>
<pre>
  您收到这封邮件，是由于在 春色撩人网站 进行了新用户注册，或用户修改 Email 使用 了这个邮箱地址。
 如果您并没有访问过 春色撩人网站，或没有进行上述操作，请忽 略这封邮件。您不需要退订或进行其他进一步的操作。
</pre>
<pre>
 ===============激活链接===================

''' + active_url + u'''

(如果上面不是链接形式，请将该地址手工粘贴到浏览器地址栏再访问)

</pre>
</body>
</html>
'''
            obj = redis_queue_send_email.REDIS_QUEUE()
            obj.send_email_via_queue(settings.SMTP_USER, data['UserEmail'], settings.WEB_NAME + u"注册", content)

            self.write_json("success", code=1)
        except Exception, e:
            print(e)
            session.rollback()
            self.write_json("failed", code=0)
        finally:
            session.close()
