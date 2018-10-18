from django.urls import path
from user.views import register, user_login, info, logout, all_orders, detail_address, upload


app_name = 'user'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('info/', info, name='info'),
    path('logout/', logout, name='logout'),
    path('all_order/<int:page_num>/', all_orders, name='all_order'),
    path('address/', detail_address, name='address'),
    path('upload/', upload, name='upload')
]
