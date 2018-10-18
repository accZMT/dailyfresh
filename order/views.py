from django.shortcuts import render, redirect
from order.models import OrderModel, OrderGoodsModel
from user.models import UserModel, CollectGoodsModel
from user.utils import login_required
from cart.models import CartModel
from datetime import datetime
from django.http import JsonResponse


@login_required
def order(request):
    """订单页面"""
    user_id = request.session.get("user_id")
    user = UserModel.objects.get(id=user_id)
    collect_goods = CollectGoodsModel.objects.filter(user_id=user_id)
    cart_id_list = request.GET.getlist("cart_id_list")
    # 根据购物车的ID，查询出对应的商品
    cart_info_list = []
    for cart_id in cart_id_list:
        cart = CartModel.objects.get(id=cart_id)
        cart_info_list.append(cart)

    context = {
        "title": "订单页面",
        "user": user,
        "collect_goods": collect_goods,
        "cart_info_list": cart_info_list,
    }
    return render(request, 'order/place_order.html', context)


def add_order(request):
    """添加订单"""
    cart_list = request.POST.getlist("cart_list")
    total_price = request.POST.get("total_price", 0)

    user_id = request.session.get('user_id')

    order = OrderModel()
    order.user_id = user_id
    order.create_time = datetime.now()
    order.total_price = total_price
    order.is_pay = 0
    order.save()

    for cart_id in cart_list:
        cart = CartModel.objects.get(id=cart_id)
        order_goods = OrderGoodsModel()
        order_goods.goods_id = cart.goods.id
        order_goods.order_id = order.id
        order_goods.number = cart.count
        order_goods.save()

        # 删除购物车中的数据
        cart.delete()
    return JsonResponse({"result": 'success'})

