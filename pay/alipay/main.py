#--*--coding:utf-8--*--
import requests
from alipay import AliPay
import settings


app_private_key_string = open(settings.ALIPAY_APP_PRIVATE_KEY_PATH).read()
alipay_public_key_string = open(settings.ALIPAY_APP_PUBLIC_KEY_PATH).read()

alipay = AliPay(
      appid=settings.ALIPAY_APPID,
      app_notify_url="http://test.com/alipay/",  # 默认回调url
      app_private_key_string=app_private_key_string,
      alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
      sign_type=settings.ALIPAY_SIGN_TYPE,  # RSA 或者 RSA2
      debug=False  # 默认False
)

def return_order_string(subject, trade_no, total_amount, return_url):
    subject = subject.encode("utf8")
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=trade_no,
        total_amount=total_amount,
        subject=subject,
        return_url=return_url,
        notify_url="http://test.com/alipay/"  # 可选, 不填则使用默认notify url
    )
    return order_string

if __name__=='__main__':
    print return_order_string(u"测试", '10126210', 5, "http://test.com/alipay/")