# --*-- coding:utf-8--*--
from views.admin import view as admin_view
from views.index import view as index_view

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
        (r"/admin/user/index/", admin_view.AdminUserIndexHandler), #
        (r"/admin/user/add/", admin_view.AdminUserAddHandler),     #
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
        (r"/layout/", index_view.IndexLayoutHandler),  # 模版页
        (r"/", index_view.IndexHandler),  # 首页
        (r"/login/", index_view.IndexLoginHandler),  # 登录
        (r"/register/", index_view.IndexRegisterHandler),  # 注册
        (r"/check_login/", index_view.CheckLoginHandler),  # 注册
        (r"/active_email/", index_view.ActiveEmailHandler),  # 用户激活
        (r"/get_product_list/", index_view.GetProductListHandler),  # 获取所有导航类型（商品类型）
        (r"/index", index_view.IndexHandler),
        (r"/qq_login_page/", index_view.IndexQQLoginPageHandler),  # QQ登录页面
        (r"/check_qq", index_view.IndexQQLoginHandler),  # QQ登录页面
        (r"/check_weibo/", index_view.WeiboLoginHandler),  # QQ登录页面
        (r"/baidu_map_page/", index_view.BaiduMapHandler),  # 百度地图页面
        (r"/collection_product/(\w+)/", index_view.CollectionProductHandler),  # 百度地图页面
        (r"/shopcart/", index_view.ShopCartHandler),  # 购物车页面
        (r"/add_shop_cart/(\w+)/", index_view.AddShopCartHandler),  # 添加商品到购物车
        (r"/get_delivery_address/", index_view.DeliveryAddressHandler),  # 获得收货地址
        (r"/alipay/", index_view.AlipayHandler),  # 支付宝支付
        (r"/alipay_success/", index_view.AlipaySusscessHandler),  # 支付支付成功
        (r"/index_logout/", index_view.IndexLoginHandler),  # 注销
        (r"/shop_product_detail", index_view.ShopProductDetailHandler),  # 商品详情
        (r"/add_product_comment/", index_view.ProductCommentHandler),  # 添加商品评论
        (r"/user_center/", index_view.UserCenterHandler),  # 用户中心
        (r"/modify_user_info/", index_view.UserCenterHandler),  # 修改用户信息
        (r"/product_history/", index_view.ProductHistoryHandler),  # 修改用户信息
        (r"/wish_list/", index_view.WishListHandler),  # 修改用户信息
        (r"/my_address/", index_view.MyAddressHandler),  # 修改用户信息

        (r".*", index_view.ErrorHandler),  # 在所有的路由后面捕获错误
      ]