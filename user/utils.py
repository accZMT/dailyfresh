from django.http import HttpResponseRedirect


# 判断是否登录，如果没有登录跳到登录页
def login_required(func):

    def login_fun(request, *args, **kwargs):
        # 判断session中是否有user_id，如果没有则认为该用户没有登录
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)
        else:
            response = HttpResponseRedirect('/account/login/')
            # 把访问的路径存到cookies中，key: next_url
            response.set_cookie('next_url', request.get_full_path())
            return response
    return login_fun


"""
http://localhost:8000/account/info/?age=1
request.path: 表示当前路径，返回的是/account/info/
request.get_full_path() ,返回的是当前路径/account/info/?age=1
"""