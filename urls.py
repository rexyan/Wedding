# --*-- coding:utf-8--*--
from views.admin import view as admin_view

url = [
        # 登录页
        (r"/admin", admin_view.AdminIndexHandler),
        (r"/admin/index", admin_view.AdminIndexHandler),
        
        # layout测试路由
        (r"/admin/layout", admin_view.AdminLayoutHandler),
        
        # 每个模块的路由都是这样，一个index + add + 增删改查。对应三个Handler
        # 商品
        (r"/admin/goods/index/", admin_view.AdminGoodsIndexHandler), 
        (r"/admin/goods/add/", admin_view.AdminGoodsAddHandler),
        (r"/admin/goods/select/(\w+)/", admin_view.AdminGoodsHandler),
        (r"/admin/goods/create/", admin_view.AdminGoodsHandler),
        (r"/admin/goods/update/(\w+)/", admin_view.AdminGoodsHandler),
        (r"/admin/goods/modify/(\w+)/", admin_view.AdminGoodsHandler),
        (r"/admin/goods/delete/(\w+)/", admin_view.AdminGoodsHandler),
        
        # 用户
        (r"/admin/user/index/", admin_view.AdminUserIndexHandler),
        (r"/admin/user/add/", admin_view.AdminUserAddHandler),
        (r"/admin/user/select/(\w+)/", admin_view.AdminUserHandler),
        (r"/admin/user/create/", admin_view.AdminUserHandler),
        (r"/admin/user/update/(\w+)/", admin_view.AdminUserHandler),
        (r"/admin/user/modify/(\w+)/", admin_view.AdminUserHandler),
        (r"/admin/user/delete/(\w+)/", admin_view.AdminUserHandler),

        # 工具接口
        (r"/admin/check_email_is_exists/", admin_view.UtilsHandler),

        # 网站前台路由
      ]