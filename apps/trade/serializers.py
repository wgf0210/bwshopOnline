import time
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import Goods
from goods.serializers import GoodsSerializer
from rest_framework import serializers


'''购物车：增删改'''
class ShopCartSerializer(serializers.Serializer):
    # 获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, label="数量", min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能小于一",
                                        "required": "请选择购买数量"
                                    })
    # 这里是继承serializer，必须指定queryset对象，如果继承ModelSerializer则不需要指定
    # goods是一个外键，可以通过这方法获取goods里object中所有的值
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())
    # 继承的serializer没有save功能，必须写一个create方法
    def create(self, validated_data):
        # validated_data是已经处理过得数据
        # 获取当前用户，view中：self.request.user:serializer中：self.context['request'].user
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        # 如果购物车有记录就+1，没有记录就创建
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            # 添加到购物车
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


'''购物车：展示（商品详情）'''
class ShopCartDetailSerializer(serializers.ModelSerializer):
    # 一个购物车对一个商品
    goods = GoodsSerializer(many=False, read_only=True)
    class Meta:
        model = ShoppingCart
        fields = ("goods", "nums")


'''订单中的商品'''
class OrderGoodsSerialzier(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = "__all__"


'''订单商品信息'''
class OrderDetailSerializer(serializers.ModelSerializer):
    # goods需要嵌套一个OrderGoodsSerialzier
    goods = OrderGoodsSerialzier(many=True)
    # alipay_url = serializers.SerializerMethodField(read_only=True)

    # def get_alipay_url(self, obj):
    #     alipay = AliPay(
    #         appid="",
    #         app_notify_url="http://127.0.0.1:8000/alipay/return/",
    #         app_private_key_path=private_key_path,
    #         alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    #         debug=True,  # 默认False,
    #         return_url="http://127.0.0.1:8000/alipay/return/"
    #     )
    #
    #     url = alipay.direct_pay(
    #         subject=obj.order_sn,
    #         out_trade_no=obj.order_sn,
    #         total_amount=obj.order_mount,
    #     )
    #     re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    #
    #     return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 生成订单的时候这些不用post
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    # alipay_url = serializers.SerializerMethodField(read_only=True)

    # def get_alipay_url(self, obj):
    #     alipay = AliPay(
    #         appid="",
    #         app_notify_url="http://127.0.0.1:8000/alipay/return/",
    #         app_private_key_path=private_key_path,
    #         alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    #         debug=True,  # 默认False,
    #         return_url="http://127.0.0.1:8000/alipay/return/"
    #     )
    #
    #     url = alipay.direct_pay(
    #         subject=obj.order_sn,
    #         out_trade_no=obj.order_sn,
    #         total_amount=obj.order_mount,
    #     )
    #     re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    #
    #     return re_url


    def generate_order_sn(self):
        # 生成订单号：
        # 当前时间+userid+随机数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id, ranstr=random_ins.randint(10, 99))

        return order_sn

    def validate(self, attrs):
        # validate中添加order_sn，然后再view中就可以save
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"














