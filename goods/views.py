from django.shortcuts import render, redirect
from goods.models import CategoryModel, CommentModel, GoodsModel
from cart.models import CartModel
from common.common import cart_count_goods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from haystack.views import SearchView
from user.utils import login_required
from order.models import OrderModel, OrderGoodsModel
from datetime import datetime


def index(request):
    """主页"""
    # 拿出所有的分类
    category_list = CategoryModel.objects.all()
    # 分别取出分类下的最新的商品
    new_goods_dict = {}
    for category in category_list:
        # goods_list = CategoryGoodsModel.objects.filter(category_id=category.id).order_by("-goods_id")[:4]
        goods_list = GoodsModel.objects.filter(category_id=category.id).order_by("-id")[:4]
        new_goods_dict[category] = goods_list
    context = {
        "new_goods_dict": new_goods_dict,
        "cart_count": cart_count_goods(request, CartModel)
    }
    return render(request, 'goods/index.html', context)


def good_list(request, category_id, sort, page_num):
    """商品列表视图
        category_id :　分类ｉｄ
        sort　：排序字段（默认：default，　价格：price，人气：popular）
    """
    category = CategoryModel.objects.get(id=category_id)
    # 取该类型最新的两个商品
    news = GoodsModel.objects.filter(category_id=category_id).order_by('-id')[:2]
    # 外键的用法
    # news = category.goodsmodel_set.order_by("-id")[:2]
    # if sort == 'default':
    #     goods = GoodsModel.objects.filter(category_id=category_id).order_by('-id')
    # elif sort == 'price':
    #     goods = GoodsModel.objects.filter(category_id=category_id).order_by('-price')
    # else:
    #     goods = GoodsModel.objects.filter(category_id=category_id).order_by('-popular')
    if sort in ['price', 'popular']:
        list_goods = GoodsModel.objects.filter(category_id=category_id).order_by('-'+sort)
    else:
        sort = 'default'
        list_goods = GoodsModel.objects.filter(category_id=category_id).order_by('-' + 'id')
    paginator = Paginator(list_goods, 1)
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page = paginator.page(1)

    context = {
        "category": category,
        "news": news,
        "list_goods": list_goods,
        "sort": sort,
        'cart_count': cart_count_goods(request, CartModel),
        "page_num": page_num,
        "page": page,
    }
    return render(request, 'goods/list.html', context)


def detail(request, goods_id):
    """某个商品的详细信息 goods_id"""
    goods = GoodsModel.objects.get(id=goods_id)
    goods.popular += 1
    goods.save()
    news = goods.category.goodsmodel_set.order_by("-id")[:2]
    # 查看商品的评论
    comments = CommentModel.objects.filter(goods_id=goods_id).order_by('-id')

    context = {
        "goods": goods,
        "news": news,
        'cart_count': cart_count_goods(request, CartModel),
        'comments': comments
    }
    # 记录最近的浏览记录， 在用户中心使用
    # 判断是否已经登录
    if request.session.has_key('user_id'):
        user_id = request.session.get('user_id')

        # 判断登录用户是否购买过该商品

        buy_goods = OrderGoodsModel.objects.filter(goods_id=goods_id)
        if buy_goods:
            for goods in buy_goods:
                order_id = goods.order_id
                order = OrderModel.objects.get(id=order_id)
                if order.user_id == user_id:
                    is_buy = True
                    break
                else:
                    is_buy = False
        else:
            is_buy = False
        context.update({"is_buy": is_buy})
        goods_id_list = (request.session.get(str(user_id), []))
        if len(goods_id_list) >= 5:
            goods_id_list.pop()
        if goods_id in goods_id_list:
            goods_id_list.remove(goods_id)
        goods_id_list.insert(0, goods_id)
        request.session[str(user_id)] = goods_id_list
    return render(request, "goods/detail.html", context)


@login_required
def comment(request):
    user_id = request.session.get("user_id")
    content = request.POST.get("content")
    goods_id = request.POST.get("goods_id")
    comments = CommentModel()
    comments.goods_id = goods_id
    comments.user_id = user_id
    comments.content = content
    comments.create_time = datetime.now()
    comments.vote_number = 0
    comments.save()
    return redirect('/goods/detail/{0}/'.format(goods_id))


class MySearchView(SearchView):

    def extra_context(self):
        news = GoodsModel.objects.all().order_by('-id')[:2]
        goods_name = self.request.GET.get('q')
        page_num = self.request.GET.get('page')
        # search_goods = GoodsModel.objects.filter(goods_name__iregex=".*?".join(list(goods_name)))
        sort = self.request.GET.get('sort', "default")
        if sort in ['price', 'popular']:
            list_goods = self.results.order_by('-' + sort)
        else:
            sort = 'default'
            list_goods = self.results.order_by('-' + 'id')
        paginator = Paginator(list_goods, 2)
        try:
            page = paginator.page(page_num)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            page = paginator.page(1)
        context = {
            'cart_count': cart_count_goods(self.request, CartModel),
            'goods_name': goods_name,
            'my_page': page,
            'my_paginator': paginator,
            'sort': sort,
            'page_num': page_num,
            'news': news
        }
        return context


