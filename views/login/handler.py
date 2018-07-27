# --*--coding:utf-8--*--
from views.base import BaseHandler
from models.Base import session
import settings
import requests
import json
from views.user.model import Users
import datetime
from views.login.model import LoginMap


# QQ登录页
class IndexQQLoginPageHandler(BaseHandler):
    def get(self):
        self.render('qq.html')


class IndexQQLoginHandler(BaseHandler):
    def get(self):
        try:
            # 获取code
            code = self.get_argument('code')
            # 根据code获取access_token
            url1 = 'https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&client_id=' + settings.QQ_APP_ID + '&client_secret=' \
                   + settings.QQ_APPKey + '&code=' + code + '&redirect_uri=' + settings.QQ_CollBackUrl
            req1 = requests.get(url1)
            access_token = req1.content.split('&')[0].split('=')[1]
            # 根据access_token获取openid
            url2 = 'https://graph.qq.com/oauth2.0/me?access_token=' + access_token
            req2 = requests.get(url2)
            openid = json.loads(req2.content.split('(')[1].split(')')[0]).get('openid')

            # 根据openid获取用户信息
            url3 = 'https://graph.qq.com/user/get_user_info?access_token=' + access_token + '&oauth_consumer_key=' + settings.QQ_APP_ID + '&openid=' + openid
            req3 = requests.get(url3)
            qq_user_info = json.loads(req3.content)
            nickname = qq_user_info.get('nickname')

            # 查询有没有绑定帐号
            self.session['openid'] = openid
            self.session['nickname'] = nickname
            ret = session.query(LoginMap).filter_by(OpenID=openid).first()
            if not ret:
                self.redirect('/register/?status=1')  # 未绑定帐号
            else:
                # 登录
                userid = ret.UserID
                ret = session.query(Users).filter_by(UserID=userid).first()
                self.session['index_user'] = ret
                session.query(Users).filter(Users.UserID == ret.UserID).update({
                    "UserLastVisitTime": datetime.datetime.now(),
                    "UserLastVisitIP": self.request.remote_ip})
                session.commit()
                self.redirect('/index')
        except Exception, e:
            print(e)
            self.redirect('/register/?status=2')  # 第三方登录出现错误


class WeiboLoginHandler(BaseHandler):
    def get(self):
        code = self.get_argument('code')
        url = 'https://api.weibo.com/oauth2/access_token'
        url1 = 'https://api.weibo.com/2/users/show.json'
        canshu = {
            "client_id": "1816247821",
            "client_secret": "eda276ef28ae911ba030fea6bfbbc360",
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://test.com/check_weibo/"
        }
        re = requests.post(url, data=canshu)
        re_json = json.loads(re.content)
        re1 = requests.get(url1 + "?access_token=" + re_json.get('access_token') + "&uid=" + re_json.get('uid'))
        weibo_user_info = json.loads(re1.content)

        ret = session.query(LoginMap).filter_by(OpenID=weibo_user_info.get('id')).first()
        if not ret:
            self.session['openid'] = weibo_user_info.get('id')
            self.session['nickname'] = weibo_user_info.get('screen_name')
            self.redirect('/register/?status=1')  # 未绑定帐号
        else:
            # 登录
            userid = ret.UserID
            ret = session.query(Users).filter_by(UserID=userid).first()
            session.query(Users).filter(Users.UserID == ret.UserID).update(
                {"UserLastVisitTime": datetime.datetime.now(),
                 "UserLastVisitIP": self.request.remote_ip})
            self.session['index_user'] = ret
            session.commit()
            self.redirect('/index')


class ActiveEmailHandler(BaseHandler):
    def get(self):
        try:
            email_address = self.get_argument('address')
            hash_code = self.get_argument('hash_code')
            ret = session.query(Users).filter_by(UserEmail=email_address).first()
            if ret and hash_code == ret.UserHashCode:
                # 激活账户
                session.query(Users).filter(Users.UserEmail == email_address).update({"UserHashCode": ""})
                session.commit()
                self.redirect('/login/?active_status=1')
        except Exception, e:
            print(e)
            self.redirect('/login/?active_status=0')


class CheckLoginHandler(BaseHandler):
    def get(self):
        user_info = None
        code = None
        try:
            user_info = self.session['index_user'].to_json()
            code = 1
        except Exception, e:
            print(e)
            user_info = None
            code = 0
        finally:
            self.write_json(user_info, code=code)


# 登录页
class IndexLoginHandler(BaseHandler):
    def get(self):
        self.render('index_login.html')

    def post(self):
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

        # 验证帐号密码，帐号状态
        ret = session.query(Users).filter(Users.UserEmail == data.get('Email'),
                                          Users.UserPwd == sec_pass(data.get('Pass'))).first()
        if not ret:
            code = 2
            msg = u"帐号密码错误"
            self.write_json(msg, code=code)
            return
        if ret.UserHashCode:
            # 账户未激活
            code = 0
            msg = u"帐号未激活"
            self.write_json(msg, code=code)
            return
        else:
            code = 1
            msg = u"登录成功"
            session.query(Users).filter(Users.UserID == ret.UserID).update(
                {"UserLastVisitTime": datetime.datetime.now(), "UserLastVisitIP": self.request.remote_ip})
            self.session['index_user'] = ret
            session.commit()
            self.write_json(msg, code=code)

    def patch(self):
        self.session['index_user'] = ""
        self.write_json(u"注销成功", code=1)
