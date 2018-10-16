from django.shortcuts import render, redirect
from user.models import UserModel, CollectGoodsModel
from django.http import JsonResponse, HttpResponseRedirect
from user.forms import UserRegisterForm
from django.contrib.auth.hashers import make_password, check_password
from user.utils import login_required
from goods.models import GoodsModel
from order.models import OrderModel
from django.core.paginator import Paginator, EmptyPage


# Create your views here.
def register(request):
    if request.method == "POST":
        user = UserRegisterForm(request.POST)
        if not user.is_valid():
            return JsonResponse(user.errors.get_json_data(), safe=False)

        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        email = request.POST.get("email", '')

        user = UserModel()
        user.username = username
        user.password = make_password(password)
        user.phone = phone
        user.address = address
        user.email = email
        user.save()
        return redirect('/account/login/')
    return render(request, 'user/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 当remember有值时，就是这事复选框勾选 的值1 没有则为0
        remember = request.POST.get('remember', 0)
        user = UserModel.objects.filter(username=username)
        if user:
            user = user[0]
            if check_password(password, user.password):
                next_url = request.COOKIES.get('next_url', '/goods/index/')
                # 先生成一个response对象
                response = HttpResponseRedirect(next_url)
                # 设置cookies，记住用户名
                if remember != 0:
                    response.set_cookie('username', username)
                else:
                    # max_age为过期时间，当为-1时候为立即过期
                    response.set_cookie('username', '', max_age=-1)
                # 把用户id 和 username放入session
                request.session['user_id'] = user.id
                request.session['username'] = username
                return response
            else:
                return render(request, 'user/login.html', {'error_password': True, 'username': username})
        else:
            return render(request, 'user/login.html', {'error_user': True, 'username': username})

    return render(request, 'user/login.html')


def logout(request):
    del request.session['user_id']
    del request.session['username']
    return redirect("/account/login/")


@login_required
def info(request):
    """用户个人信息"""
    user_id = request.session['user_id']
    user = UserModel.objects.get(id=user_id)
    user_info = {
        'username': user.username,
        'phone': user.phone,
        'address': user.address,
    }
    goods_id_list = request.session.get(str(user_id), [])

    goods_list = []
    for goods_id in goods_id_list:
        goods_list.append(GoodsModel.objects.get(id=goods_id))
    context = {'user_info': user_info, 'goods_list': goods_list, 'title': '个人信息'}
    return render(request, 'user/user_center_info.html', context)


@login_required
def all_orders(request, page_num):
    """全部订单"""
    # 查询当前登录用户的所有订单信息
    user_id = request.session.get('user_id')
    all_order = OrderModel.objects.filter(user_id=user_id)
    # print(all_order)
    # for index in all_order:
    #     print(index.ordergoodsmodel_set.all())
    # 每一页展示2个
    paginator = Paginator(all_order, 2)
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context = {
        "page": page,
        "page_num": page_num,
        "title": "全部订单"
    }
    return render(request, 'user/user_center_order.html', context)


@login_required
def detail_address(request):
    user_id = request.session.get("user_id")
    if request.method == "GET":
        user = CollectGoodsModel.objects.filter(user_id=user_id).filter(is_used=1)
        if user:
            user = user[0]
        context = {
            "title": "收货地址",
            "user": user
        }
        return render(request, 'user/user_center_site.html', context)
    elif request.method == "POST":
        user = CollectGoodsModel()
        user.user_id = user_id
        user.person_name = request.POST.get('user')
        user.detail_address = request.POST.get("detail_address")
        user.postcode = request.POST.get("postcode")
        user.tel = request.POST.get("tel")
        user.is_used = 0
        user.save()

        return redirect("/account/address")


def upload(request):
    """上传接口"""
    myfile = request.FILES.get('myfile')
    if request.method == "GET":
        return render(request, 'upload.html')
    if request.method == "POST":
        with open("a.txt", 'wb') as fp:
            for chunk in myfile.chunks():
                fp.write(chunk)
        return JsonResponse({"result": "success"})
