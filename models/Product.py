# --*--coding:utf8--*--
from Base import *
import datetime

LOCAL = 1
QINIU = 2
UPYUN = 3
UPLOAD_TYPE = {
    (LOCAL, u"本地"),
    (QINIU, u"七牛云"),
    (UPYUN, u"又拍云"),
}

# 创建单表
class Product(Base):
    __tablename__ = 'product'  # 表名
    ProductID = Column(Integer, primary_key=True, autoincrement=True) # 商品 ID
    ProductType = Column(Integer)  # 商品类型
    ProductName = Column(String(100))  # 商品名称
    ProductBrand = Column(String(100), nullable=True) # 商品品牌
    ProductKeywords = Column(String(100), nullable=True)  # 商品关键词
    ProductIntroduce = Column(String(2000), nullable=True)  # 商品简介
    ProductDescribe = Column(String(5000), nullable=True)  # 商品完整描述
    ProductMarketPrice = Column(Integer)  # 商品市场价格
    ProductFavorablePrice = Column(Integer)  # 商品优惠价格
    ProductVipPrice = Column(Integer)  # 商品VIP价格
    ProductPoint = Column(Integer)  # 商品积分
    ProductCount = Column(Integer)  # 商品库存
    IsHot = Column(Boolean, default=False)  # 是否是热门商品
    IsNew = Column(Boolean, default=False)  # 是否是新品
    SmallPictureUpType = Column(Integer)  #1为本地，2为七牛云，3为又拍云
    BigPictureUpType = Column(Integer)  #1为本地，2为七牛云，3为又拍云
    ProductSmallPicture = Column(String(100), nullable=True)
    ProductBigPictureProductBigPicture = Column(String(100), nullable=True)
    ProductOnTime = Column(String,  nullable=True)
    ProductCreatTime = Column(DateTime,  nullable=True, default=datetime.datetime.now())
    ProductBuyNum = Column(Integer, nullable=True, default=0)
    ProductCollectNum = Column(Integer, nullable=True, default=0)

    def __repr__(self):
        return "%s-%s" % (self.ProductName, self.ProductID)

    def to_json(self):
        return {
            'ProductID': self.ProductID,
            'ProductType': self.ProductType,
            'ProductName': self.ProductName,
            'ProductBrand': self.ProductBrand,
            'ProductKeywords': self.ProductKeywords,
            'ProductIntroduce': self.ProductIntroduce,
            'ProductDescribe': self.ProductDescribe,
            'ProductMarketPrice': self.ProductMarketPrice,
            'ProductFavorablePrice': self.ProductFavorablePrice,
            'ProductVipPrice': self.ProductVipPrice,
            'ProductPoint': self.ProductPoint,
            'ProductCount': self.ProductCount,
            'IsHot': self.IsHot,
            'IsNew': self.IsNew,
            'SmallPictureUpType': self.SmallPictureUpType,
            'BigPictureUpType': self.BigPictureUpType,
            'ProductSmallPicture': self.ProductSmallPicture,
            'ProductBigPictureProductBigPicture': self.ProductBigPictureProductBigPicture,
            'ProductOnTime': self.ProductOnTime,
            'ProductCreatTime': self.ProductCreatTime,
            'ProductBuyNum': self.ProductBuyNum,
            'ProductCollectNum': self.ProductCollectNum
        }


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


def main(arg):
    if arg == 1:
        init_db()
    elif arg == 0:
        drop_db()


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    main(1)

