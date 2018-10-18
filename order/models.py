
from datetime import datetime
from django.db import models
from user.models import UserModel
from django.contrib import admin
from goods.models import GoodsModel


class OrderModel(models.Model):
    """订单管理"""
    create_time = models.DateTimeField(default=datetime.now(), verbose_name='创建时间')
    is_pay = models.BooleanField(verbose_name='是否支付')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='总价格')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='用户')

    class Meta:
        db_table = 'order'
        verbose_name = '订单管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


@admin.register(OrderModel)
class OrderAdminModel(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'is_pay')


class OrderGoodsModel(models.Model):
    """商品和订单的关系"""
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, verbose_name='订单')
    goods = models.ForeignKey(GoodsModel, on_delete=models.CASCADE, verbose_name='商品')
    number = models.IntegerField(default=0, verbose_name='购买数量')

    class Meta:
        db_table = 'order_goods'
        verbose_name = '订单商品关系'
        verbose_name_plural = verbose_name


@admin.register(OrderGoodsModel)
class OrderGoodsAdminModel(admin.ModelAdmin):
    list_display = ('order', 'goods', 'number')
