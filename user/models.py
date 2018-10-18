from django.db import models
from django.contrib import admin
# Create your models here.


class UserModel(models.Model):
    username = models.CharField(max_length=50,null=False,verbose_name='用户名')
    password = models.CharField(max_length=256,null=False,verbose_name='密码')
    phone = models.CharField(max_length=11,null=False,verbose_name='联系方式')
    address = models.CharField(max_length=200,null=False,verbose_name='联系地址')
    email = models.EmailField(verbose_name='电子邮件')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


@admin.register(UserModel)
class UserAdminModel(admin.ModelAdmin):
    list_display = ['username','phone']


class CollectGoodsModel(models.Model):
    """收货地址和信息管理"""
    # 属于谁的收货信息   用户对收货信息是一对多的关系
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    person_name = models.CharField(max_length=30,null=False,verbose_name='收件人')
    detail_address = models.CharField(max_length=200,null=False,verbose_name='详细地址')
    postcode = models.IntegerField(default=000000,verbose_name='邮政编码')
    tel = models.CharField(max_length=20,null=False,verbose_name='联系方式')

    is_used = models.BooleanField(verbose_name='是否正在使用')

    def __str__(self):
        return self.person_name

    class Meta:
        verbose_name = '收货信息管理'
        verbose_name_plural = verbose_name


@admin.register(CollectGoodsModel)
class CollectGoodsAdminModel(admin.ModelAdmin):
    list_display = ('person_name','tel','detail_address','is_used')
