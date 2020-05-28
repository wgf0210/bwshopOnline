from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins,generics,viewsets,filters
from goods.serializers import GoodsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer
from goods.models import Goods, GoodsCategory, Banner
from goods.filters import GoodsFilter

'''商品分页'''
class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

# class GoodsListView(APIView):
#     def get(self,request,format=None):
#         goods = Goods.objects.all()
#         goods_serializers = GoodSerializer(goods,many=True)
#
#         return Response(goods_serializers.data)



# class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
#     queryset = Goods.objects.all()
#     serializer_class = GoodSerializer

# 简化写法
# class GoodsListView(generics.ListAPIView):
#     pagination_class = GoodsPagination
#     queryset = Goods.objects.all()
#     serializer_class = GoodSerializer

'''视图集'''
'''商品'''
class GoodsListViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
        商品列表页, 分页， 搜索， 过滤， 排序
    """
    pagination_class = GoodsPagination
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer
#     设置筛选
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = GoodsFilter
#     设置搜索
    search_fields = ('name','goods_brief')
    # 排序
    ordering_fields = ('sold_num','add_time')


'''商品分类'''
class CategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


'''首页轮播'''
class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


'''首页商品分类数据'''
class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    # 获取is_tab=True（导航栏）里面的分类下的商品数据
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer









