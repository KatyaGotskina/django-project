from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from . import views
from .routers import router


urlpatterns = [
    path('', views.homepage, name='home'),
    path('menu/', views.menu, name='menu'),
    path('rest/', include(router.urls)),
    path('register', views.register, name='register'),
    path('profile/', views.profile_page, name='profile'),
    path('auth/', include('django.contrib.auth.urls')),
    path('token/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('buy/', views.buy_product, name='buy_product'),
    path('make_order/', views.making_order, name='make_order'),
    path('canceling', views.cancel_order, name='cancel_order'),
    path('delete/', views.delete_product, name='delete_product'),
    path('filter_category/', views.filter_category, name='filter_category'),
    path('add_comment', views.add_comment, name='add_comment'),
    path('add_num', views.add_num, name='add_num'),
    path('del_num', views.del_num, name='del_num'),
    path('profile/show_order', views.show_order, name='show_order')
]
