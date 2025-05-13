from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('create/', views.create, name='create'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('purchase/<int:product_id>/', views.purchase, name='purchase'),
    path('rate/<int:product_id>/', views.rate_product, name='rate_product'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]