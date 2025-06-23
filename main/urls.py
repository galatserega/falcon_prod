from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from views import faq_view

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('support/', views.support, name='support'),
    path('delivery_payment/', views.delivery_payment, name='delivery_payment'),
    path('contact/', views.contact, name='contact'),
    path('faq/', faq_view, name='faq')

]