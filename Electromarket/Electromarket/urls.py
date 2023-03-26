from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
admin.site.site_header = "Electromarket"
from .import views
urlpatterns = [
    path('404', views.Error404, name='404'),
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),

    path('', views.HOME, name='home'),
    path('about', views.ABOUT, name='about'),
    path('contact', views.CONTACT, name='contact'),
    path('product', views.PRODUCT, name='product'),
    path('search/', views.SEARCH, name='search'),
    path('product/filter-data', views.filter_data, name="filter-data"),
    path('product/<slug:slug>', views.PRODUCT_DETAILS, name='product_detail'),
    #account urls
    path('account/my-account', views.MY_ACCOUNT, name='my_account'),
    path('account/register', views.REGISTER, name='handleregister'),
    path('account/login', views.LOGIN, name='handlelogin'),
    path('account/profile', views.PROFILE, name='profile'),
    path('account/profile/update', views.PROFILE_UPDATE, name='profile_update'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
    path('cart/checkout/placeorder', views.PLACE_ORDER, name='place_order'),
    path('myorder/', views.myOrder, name='myOrder'),
    path('checkout/', views.CHECKOUT, name='checkout'),
    path('success/', views.SUCCESS, name='success'),
    path('api/verify_payment', views.verify_payment, name='verify_payment'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('order/<int:order_id>/save_pdf/', views.save_pdf, name='save_pdf'),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
