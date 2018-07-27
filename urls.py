# --*-- coding:utf-8--*--
from views.admin import view as admin_view
from views.address import handler as address_handler
from views.search import handler as search_handler
from views.comment import handler as comment_handler
from views.user import handler as user_handler
from views.wishlist import handler as wishlist_handler
from views.product import handler as product_handler
from views.index import handler as index_handler
from views.login import handler as login_handler
from views.register import handler as register_handler
from views.shopcard import handler as shopcard_handler
from views.alipay import handler as alipay_handler
from views.collection import handler as collection_handler
from views.error import handler as error_handler

url = [
    # 登录页
    (r"/admin/", admin_view.AdminIndexHandler),
    (r"/admin/index/", admin_view.AdminIndexHandler),

    # layout测试路由
    (r"/admin/layout", admin_view.AdminLayoutHandler),

    # 每个模块的路由都是这样，一个index + add + 增删改查。对应三个Handler
    # 商品
    (r"/admin/product/index/", admin_view.AdminProductIndexHandler),
    (r"/admin/product/add/", admin_view.AdminProductAddHandler),
    (r"/admin/product/select/(\w+)/", admin_view.AdminProductHandler),
    (r"/admin/product/create/", admin_view.AdminProductHandler),
    (r"/admin/product/update/(\w+)/", admin_view.AdminProductHandler),
    (r"/admin/product/delete/(\w+)/", admin_view.AdminProductHandler),

    # 用户
    (r"/admin/user/index/", admin_view.AdminUserIndexHandler),  #
    (r"/admin/user/add/", admin_view.AdminUserAddHandler),  #
    (r"/admin/user/select/(\w+)/", admin_view.AdminUserHandler),
    (r"/admin/user/create/", admin_view.AdminUserHandler),
    (r"/admin/user/update/(\w+)/", admin_view.AdminUserHandler),
    (r"/admin/user/delete/(\w+)/", admin_view.AdminUserHandler),

    # 商品类型
    (r"/admin/product_type/index/", admin_view.AdminProductTypeIndexHandler),
    (r"/admin/product_type/add/", admin_view.AdminProductTypeAddHandler),
    (r"/admin/product_type/select/(\w+)/", admin_view.AdminProductTypeHandler),
    (r"/admin/product_type/create/", admin_view.AdminProductTypeHandler),
    (r"/admin/product_type/update/(\w+)/", admin_view.AdminProductTypeHandler),
    (r"/admin/product_type/delete/(\w+)/", admin_view.AdminProductTypeHandler),

    # 订单
    (r"/admin/order/index/false/", admin_view.AdminOrderFalseHandler),
    (r"/admin/order/index/true/", admin_view.AdminOrderTrueHandler),
    (r"/admin/order/select/(\w+)/", admin_view.AdminOrderHandler),
    (r"/admin/order/update/(\w+)/", admin_view.AdminOrderHandler),

    # 评论
    (r"/admin/comment/index/", admin_view.AdminCommentIndexHandler),
    (r"/admin/comment/select/(\w+)/", admin_view.AdminCommenHandler),
    (r"/admin/comment/update/(\w+)/", admin_view.AdminCommenHandler),
    (r"/admin/comment/delete/(\w+)/", admin_view.AdminCommenHandler),

    # 后台登录
    (r"/admin/user/login/", admin_view.AdminUserLoginHandler),
    (r"/admin/user/current/", admin_view.AdminUserLoginHandler),

    # 工具接口
    (r"/admin/check_email_is_exists/", admin_view.UtilsHandler),
    (r"/tools/send_email/(\w+)/", admin_view.SendEmailHandler),  # 邮件接口
    (r"/tools/check_code/(\w+)/", admin_view.CheckCodeHandler),  # 邮件接口

    # 上传图片接口
    (r"/admin/image/add/", admin_view.AdminProductImgesIndexHandler),
    (r"/admin/image/upload/", admin_view.AdminProductImgesIndexHandler),
    # (r"/admin/goods/image/add/", admin_view.AdminGoodsImgesAddHandler),

    # 网站前台路由
    (r"/layout/", index_handler.IndexLayoutHandler),  # 模版页
    (r"/", index_handler.IndexHandler),  # 首页
    (r"/login/", login_handler.IndexLoginHandler),  # 登录
    (r"/register/", register_handler.IndexRegisterHandler),  # 注册
    (r"/check_login/", login_handler.CheckLoginHandler),  # 注册
    (r"/active_email/", login_handler.ActiveEmailHandler),  # 用户激活
    (r"/get_product_list/", product_handler.GetProductListHandler),  # 获取所有导航类型（商品类型）
    (r"/index", index_handler.IndexHandler),
    (r"/qq_login_page/", login_handler.IndexQQLoginPageHandler),  # QQ登录页面
    (r"/check_qq", login_handler.IndexQQLoginHandler),  # QQ登录页面
    (r"/check_weibo/", login_handler.WeiboLoginHandler),  # QQ登录页面
    (r"/baidu_map_page/", index_handler.BaiduMapHandler),  # 百度地图页面
    (r"/collection_product/(\w+)/", collection_handler.CollectionProductHandler),  # 百度地图页面
    (r"/shopcart/", shopcard_handler.ShopCartHandler),  # 购物车页面
    (r"/add_shop_cart/(\w+)/", shopcard_handler.AddShopCartHandler),  # 添加商品到购物车
    (r"/get_delivery_address/", address_handler.DeliveryAddressHandler),  # 获得收货地址
    (r"/alipay/", alipay_handler.AlipayHandler),  # 支付宝支付
    (r"/alipay_success/", alipay_handler.AlipaySusscessHandler),  # 支付支付成功
    (r"/index_logout/", login_handler.IndexLoginHandler),  # 注销
    (r"/shop_product_detail", shopcard_handler.ShopProductDetailHandler),  # 商品详情
    (r"/add_product_comment/", comment_handler.ProductCommentHandler),  # 添加商品评论
    (r"/user_center/", user_handler.UserCenterHandler),  # 用户中心
    (r"/modify_user_info/", user_handler.UserCenterHandler),  # 修改用户信息
    (r"/product_history/", product_handler.ProductHistoryHandler),  # 修改用户信息
    (r"/wish_list/", wishlist_handler.WishListHandler),  # 修改用户信息
    (r"/my_address_delete/(\w+)/", address_handler.DeliveryAddress),  # 修改用户信息
    (r"/my_address/", address_handler.MyAddressHandler),  # 修改用户信息
    (r"/search", search_handler.SearchHandler),  # 查询商品
    (r"/address_page", address_handler.AddressPageHandler),  # 查询商品

    (r".*", error_handler.ErrorHandler),  # 在所有的路由后面捕获错误
]
