from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav
from .models import UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer


'''用户收藏'''
class UserFavSerializer(serializers.ModelSerializer):
    # 获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        # validata实现唯一联合，一个商品只能收藏一次
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]
        # 收藏的时候需要返回商品的id，因为取消收藏的时候必须知道商品的id是多少
        fields = ("user", "goods", "id")


'''用户收藏详情'''
class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()
    # 通过商品id获取收藏的商品，需要嵌套商品的序列化
    class Meta:
        model = UserFav
        fields = ("goods", "id")


'''用户留言'''
class LeavingMessageSerializer(serializers.ModelSerializer):
    # 获取当前登陆的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # read_only：只返回，post时候可以不用提交；；format：格式化输出
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id" ,"add_time")




















