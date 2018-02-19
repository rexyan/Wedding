# --*-- coding:utf-8--*--
from views.admin import view as admin_view

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

        # 上传图片接口
        (r"/admin/image/add/", admin_view.AdminProductImgesIndexHandler),
        (r"/admin/image/upload/", admin_view.AdminProductImgesIndexHandler),
        # (r"/admin/goods/image/add/", admin_view.AdminGoodsImgesAddHandler),

        # 网站前台路由
      ]