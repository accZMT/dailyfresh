# from cart.models import CartModel


def cart_count_goods(request, CartModel):
    if request.session.has_key('user_id'):
        user_id = request.session.get('user_id')
        cart_list = CartModel.objects.filter(user_id=user_id)
        cart_count = 0
        # 统计出购物车中所有商品的数量
        for cart in cart_list:
            cart_count += cart.count
    else:
        cart_count = 0

    return cart_count
