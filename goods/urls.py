from django.urls import path
from goods.views import index, good_list, detail, comment, MySearchView


app_name = 'goods'
urlpatterns = [
    path('index/', index, name='index'),
    path('list/<int:category_id>/<str:sort>/<int:page_num>/', good_list, name='list'),
    path('detail/<int:goods_id>/', detail, name='detail'),
    path('comment/', comment, name='comment'),
    path('', MySearchView())


]
