# --coding:utf-8--*--
from sqlalchemy.sql import func
from views.base import BaseHandler
from models.Base import session
from views.product.utils import get_all_product_type
from views.product.utils import get_product_type_by_pid
from views.product.model import Product
import json
from views.comment.utils import get_com_last_3_limit
from views.product.utils import get_product_by_pid_first


class IndexHandler(BaseHandler):
    def get(self):
        pid = self.get_argument('pid', None)
        # product_type = session.query(ProductType).all()
        product_type = get_all_product_type()
        product_type_list = [x.to_json() for x in product_type]
        if pid:
            # banner上的文字
            name = None
            for x in product_type_list:
                if str(x['ProductTypeID']) == pid:
                    name = x['ProductTypeName']

            # 获取品牌分类
            # pid_product_list = session.query(Product).filter(Product.ProductType == pid).all()
            pid_product_list = get_product_type_by_pid(pid)
            product_brand_list = [x.to_json() for x in pid_product_list][:5]

            # 排序方式
            order = self.get_argument('order', "")
            if order:
                def sorted_func(s):
                    if order == '2':
                        col = "ProductMarketPrice"
                    elif order == '3':
                        col = "ProductMarketPrice"
                    elif order == '4':
                        col = "ProductCollectNum"
                    elif order == '5':
                        col = "ProductOnTime"
                    elif order == '6':
                        col = "ProductBuyNum"
                    else:
                        col = "ProductID"
                    return s.to_json()[col]

                pid_product_list = sorted(pid_product_list, key=sorted_func, reverse=True)

            # 获取标签、关键字
            key_words_list = [x.to_json()['ProductKeywords'] for x in pid_product_list][:8]

            # 查询最高价
            max_price = session.query(func.max(Product.ProductMarketPrice)).first()[0]

            # 获取推荐的商品
            hot_product_list = [x.to_json() for x in pid_product_list if x.to_json()['IsHot'] == 1][:4]

            # 商品列表、分页
            data_count = len(pid_product_list)  # 数据总条数
            page_num = int(self.get_argument('page', 0))
            every_page_num = end_page_num = 12
            max_page, remainder = divmod(data_count, every_page_num)
            if remainder != 0:
                max_page += 1
            start_page_num = 0
            if page_num != 0:
                start_page_num = (page_num - 1) * every_page_num
                end_page_num = (page_num) * every_page_num
            # 筛选价格区间
            filter_price = int(self.get_argument('filter_price', 0))
            if filter_price:
                pid_product_list = [x for x in pid_product_list if x.ProductMarketPrice < filter_price][
                                   start_page_num:end_page_num]

            # 筛选商品品牌
            brand = self.get_argument('brand', "")
            brand = json.loads('"' + "".join([(i and "\\" + i) for i in brand.split('%')]) + '"')
            if brand:
                pid_product_list = [x for x in pid_product_list if x.ProductBrand == brand][start_page_num:end_page_num]

            # 筛选标签
            label = self.get_argument('label', "")
            print "=====", [(i and "\\" + i) for i in label.split('%')]
            label = json.loads('"' + "".join([(i and "\\" + i) for i in label.split('%')]) + '"')
            print "label", label
            if label:
                pid_product_list = [x for x in pid_product_list if x.ProductKeywords == label][
                                   start_page_num:end_page_num]
            pid_product_list = [x.to_json() for x in pid_product_list][start_page_num:end_page_num]
            page_data_count = len(pid_product_list)  # 返回前台的数据总条数
            page_info = {"pid": pid, "max_page": max_page, "data_count": data_count, "page_data_count": page_data_count,
                         "page_num": page_num}
            self.render(
                'index_shop_list.html',
                name=name,
                product_brand_list=product_brand_list,
                key_words_list=key_words_list,
                max_price=max_price,
                hot_product_list=hot_product_list,
                product_list=pid_product_list,
                page_info=page_info,
            )
        else:
            # 获取首页大图下的三个图（是新品且是热门）
            info_1 = session.query(Product).filter(Product.IsHot == 1, Product.IsNew == 1)[0:3]
            # 获取首页下的5个热门商品
            info_2 = session.query(Product).filter(Product.IsHot == 1, Product.IsNew == 0)[0:4]
            info_3 = session.query(Product).filter(Product.IsHot == 0, Product.IsNew == 1)[0:4]

            # 获取评论的商品，取最新三条
            # comment_product_limit_3 = session.query(Comment).filter_by(Status=True).all()[-4:-1]
            comment_product_limit_3 = get_com_last_3_limit()
            comment_product_limit_3_list = []
            for com in comment_product_limit_3:
                rmp_com_dict = com.to_json()
                product_id = rmp_com_dict['ProductID']
                product = get_product_by_pid_first(product_id).to_json()
                rmp_com_dict['product'] = product
                comment_product_limit_3_list.append(rmp_com_dict)
            self.render(
                'index_index.html',
                info_1=info_1,
                info_2=info_2,
                info_3=info_3,
                comment_product_limit_3_list=comment_product_limit_3_list
            )


# 模版页
class IndexLayoutHandler(BaseHandler):
    def get(self):
        self.render('index_layout.html')


class BaiduMapHandler(BaseHandler):
    def get(self):
        self.render('baidu_map.html')
