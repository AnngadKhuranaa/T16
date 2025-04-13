from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('order/', views.order, name='order'),
    path('order_now/<int:item_id>/', views.order_now, name='order_now'),
]
