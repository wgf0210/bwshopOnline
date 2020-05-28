__author__ = 'bobby'

from django.views.generic.base import View
from goods.models import Goods


class GoodsListView(View):
    def get(self,request):
        # 通过django的view实现商品列表页

        json_list = []
        # 获取所有商品
        goods = Goods.objects.all()
        # for good in goods:
        #     json_dict = {}
        #     json_dict["name"] = good.name
        #     json_dict["category"] = good.category.name
        #     json_dict["market_price"] = good.market_price
        #     json_dict["add_time"] = good.add_time
        #     json_list.append(json_dict)

        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)

        '''
        ---------serializers----------
        
        import json
        from django.core import serializers
        json_data = serializers.serialize('json', goods)
        json_data = json.loads(json_data)
        from django.http import HttpResponse, JsonResponse
        return JsonResponse(json_data, safe=False)
        
        '''

        # 只能转换dict和list类型
        import json
        from django.http import HttpResponse
        # 返回json，一定要指定类型content_type='application/json'
        return HttpResponse(json.dumps(json_list),content_type='application/json')