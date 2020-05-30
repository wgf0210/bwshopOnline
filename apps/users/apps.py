from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = '用户管理'

    # 配置可以使用信号量的机制
    def ready(self):
        import users.signals
