import xadmin
from xadmin import views
from xadmin.models import Log,Permission
from .models import *
# from apps.course.models import *
# from apps.operation.models import *
# from apps.organization.models import *


class BaseSettings(object):
    # xadmin基础配置
    enable_themes = True   #开启主题功能
    use_bootswatch = True


class GlobalSettings(object):
    # 设置网站标题和页脚、收起菜单栏
    site_title = '美少女 - 海马生鲜后台管理'
    site_footer = 'TZMM - 北京网络职业学院'
    menu_style = 'accordion'


xadmin.site.register(views.BaseAdminView,BaseSettings)
xadmin.site.register(views.CommAdminView,GlobalSettings)