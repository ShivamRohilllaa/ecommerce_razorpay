from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name='home'),
    path('Category/<slug:category_slug>', views.product_by_category, name='product_by_category'),
    path('Category/<slug:category_slug>/<slug:product_slug>', views.product_page, name='product_detail'),
    path('cart/add/<int:product_id>', views.add_cart, name='add_cart'),
    path('cart', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('cart/delete/<int:product_id>', views.cart_delete, name='cart_delete'),
    path('thank/<int:order_id>', views.thank_page, name='thanks'),
    path("payment/charge/", views.app_charge,name="charge"),


] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)