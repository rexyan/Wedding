# --coding:utf-8--

from hashlib import md5
import settings
import io
import re
import os
from tornado.web import HTTPError
import functools
from bson import ObjectId


def get_user(user_id):
    try:
        return User.objects.get(id=ObjectId(user_id))
    except User.DoesNotExist:
        return None


def authenticated(method):
    '''
    :param method:
    :return:
    '''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        ''''''
        if not self.session.get('user_id'):
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper


def sec_pass(new_passworld):
    '''
    :param new_passworld:
    :return:
    '''
    return md5(new_passworld + settings.SECRET_KEY).hexdigest()


def check_pass_re(password):
    '''
    :param password:
    :return:
    '''
    pattern = re.compile(
        # ur'^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])|(?=.*[A-Z])(?=.*[a-z])(?=.*[^A-Za-z0-9])|(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])|(?=.*[a-z])(?=.*[0-9])(?=.*[^A-Za-z0-9])).{8,}')
        ur'^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(.{8,})'
        # ur'^(.{8,})')
    )
    return pattern.search(password)


def check_email_re(email):
    '''
    :param email:
    :return:
    '''
    if len(email) >= 5:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False


def check_mail_exist(email):
    '''
    :param email:
    :return:
    '''
    obj = User.objects.filter(mail=email)
    if obj:
        return False
    else:
        return True


def randomstring(n):
    '''
    :param n:
    :return:
    '''
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(n))))[0:40]


def upload_file(file, path):
    if file is not None:
        filename = u"{0}_{1}".format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"), file["filename"])
        if not os.path.exists(path):
            os.makedirs(path)
        filepath = os.path.join(path, filename)
        with open(filepath, "wb") as f:
            f.write(file["body"])
            f.close()
        return filepath


if __name__ == '__main__':
    print randomstring(40)