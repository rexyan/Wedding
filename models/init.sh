#
# 使用方法:sh init.sh + 数据库【SQLite、MySQL】,默认值为MySQL，可不加
# 初始化脚本，要修改使用的数据库在Base.py中修改。
# 运行此脚本后会创建所有的表（以前的数据会清空）
# 后台会创建默认用户superadmin、默认密码123456
# 前台会创建默认用户default@test.com、默认密码123456、用户名default
#

echo "数据库类型：$1";
python Collection.py
python Comment.py
python Collection.py
python DeliveryAddress.py
python LoginMap.py
python Manager.py
python Order.py
python Product.py
python ProductType.py
python Settings.py
python ShopCart.py
python User.py

python create_default_user.py

if [ $1 == 'SQLite' ];then
    mv data.db  ../data.db
fi

echo "init end"