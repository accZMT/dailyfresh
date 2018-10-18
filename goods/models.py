from django.db import models
from django.contrib import admin
from user.models import UserModel
from datetime import datetime


class CategoryModel(models.Model):

    category_name = models.CharField(max_length=20, null=False, verbose_name='商品分类名称')
    number = models.IntegerField(default=0, verbose_name='排序字段')
    image = models.CharField(max_length=200, verbose_name='分类展示的图片', null=False, default='images/goods/goods003.jpg')

    class Meta:
        db_table = 'category'
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category_name


@admin.register(CategoryModel)
class CategoryAdminModel(admin.ModelAdmin):
    list_display = ('category_name', )


class GoodsModel(models.Model):
    # 添加一个分类外键
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, verbose_name='商品的分类', default=1)
    goods_name = models.CharField(max_length=50, null=False, verbose_name='商品名称')
    abstract = models.CharField(max_length=200, null=True, verbose_name='商品简介')
    # max_digits 总共限制几位  decimal_places 小数点后几位
    price = models.DecimalField(default=0, max_digits=11, decimal_places=2, verbose_name='价格')

    unit = models.CharField(max_length=20, null=False, verbose_name='商品售卖单位')
    stock = models.IntegerField(default=0, verbose_name='商品库存')
    desc = models.TextField(null=True, verbose_name='详细介绍')
    pic = models.CharField(null=False, verbose_name='商品图片', max_length=200, default='/static/images/goods/goods003.jpg')
    popular = models.IntegerField(default=0, verbose_name='人气指数')

    def __str__(self):
        return self.goods_name

    class Meta:
        db_table = 'goods'
        verbose_name = '商品表'
        verbose_name_plural = verbose_name


@admin.register(GoodsModel)
class GoodsAdminModel(admin.ModelAdmin):
    list_display = ('goods_name', 'stock', 'price')


class CommentModel(models.Model):

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='评论的用户')
    # 商品跟评论一对多的关系
    goods = models.ForeignKey(GoodsModel, on_delete=models.CASCADE, verbose_name='商品名称')
    content = models.CharField(max_length=255, null=False, verbose_name='评论的内容')
    vote_number = models.IntegerField(default=0, verbose_name='点赞数')
    create_time = models.DateTimeField(default=datetime.now(), verbose_name='创建时间')

    class Meta:
        db_table = 'comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


@admin.register(CommentModel)
class CommentAdminModel(admin.ModelAdmin):
    list_display = ('goods_id', 'user_id', 'content', 'vote_number', 'create_time')


class ImagesModel(models.Model):
    """存储图片与商品的关系"""
    goods = models.ForeignKey(GoodsModel, models.CASCADE, verbose_name='商品')
    image_url = models.CharField(max_length=200, verbose_name='图片地址', null=False)

    class Meta:
        db_table = 'images'
        verbose_name = '图片'
        verbose_name_plural = verbose_name


@admin.register(ImagesModel)
class ImagesAdminModel(admin.ModelAdmin):
    list_display = ('goods', 'image_url')


class CategoryGoodsModel(models.Model):
    """商品分类和商品之间的关系"""
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, verbose_name='商品分类')
    goods = models.ForeignKey(GoodsModel, on_delete=models.CASCADE, verbose_name='商品')

    class Meta:
        db_table = 'category_goods'
        verbose_name = '商品分类和商品关系'
        verbose_name_plural = verbose_name


@admin.register(CategoryGoodsModel)
class CategoryGoodsAdminModel(admin.ModelAdmin):
    list_display = ('category', 'goods')
