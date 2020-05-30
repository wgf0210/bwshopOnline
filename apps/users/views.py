from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers,viewsets,status,mixins,permissions,authentication
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler,jwt_encode_handler
from users.serializers import SmsSerializer,UserRegSerializer,UserDetailSerializer
from users.models import VerifyCode
from bwshopOnline.settings import APIKEY
from utils.yunpian import YunPian
from random import choice


User = get_user_model()

'''自定义验证：用户名和手机号都允许登录'''
class CustomBackend(ModelBackend):
    def authenticate(self,request, username=None, password=None, **kwargs):
        try:
            # 用户名、手机号都能登录
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
        #     # 异常信息UserProfile matching query does not exist
        #     raise serializers.ValidationError({'username_error_field': '账户输入错误'})
        #     return None
        # else:
        #     raise serializers.ValidationError({'password_error_field': '密码输入错误'})
            return None


'''手机的验证码'''
class SmsCodeViewset(CreateModelMixin,viewsets.GenericViewSet):
    serializer_class = SmsSerializer
    def generate_code(self):
        """
        生成四位数字的验证码
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 验证合法
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)
        # 生成验证码
        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)



'''用户：注册，更新'''
class UserViewset(CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    # 判断登录，只有登录了才能更新
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        # 生成token
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 这里需要动态选择用哪个序列化方式：1.UserRegSerializer(用户注册)只返回username和mobile，会员中心页面需要显示更多字段，所以要创建一个UserDetailSerializer；2.问题又来了，如果注册的试用UserDetailSerializer，又会导致验证失败，所以需要动态的试用serializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer


    # 这里需要动态权限配置：1.用户注册的时候不应该有权限限制；2.党项获取用户详情信息的时候，必须登录才行
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    def get_object(self):
        return self.request.user


    def perform_create(self, serializer):
        return serializer.save()













