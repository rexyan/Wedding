# --*-- coding:utf-8--*--
from views.admin import login as admin_login


url = [
        # 网站后台路由
        (r"/admin", admin_login.AdminIndexHandler),
        (r"/admin/index", admin_login.AdminIndexHandler),
        (r"/admin/goods", admin_login.AdminGoodsHandler),
        (r"/admin/user", admin_login.AdminGoodsHandler)
        
        # 网站前台路由
      ]