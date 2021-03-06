from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('user/', views.user_page, name='user'),
    path('account/', views.account_page, name='account'),
    path('products/', views.products, name='products'),
    path('customer/<int:pk>', views.customer, name='customer'),
    path('create_order/<int:pk>', views.create_order, name='create_order'),
    path('update_order/<int:pk>', views.update_order, name='update_order'),
    path('delete_order/<int:pk>', views.delete_order, name='delete_order'),
]
