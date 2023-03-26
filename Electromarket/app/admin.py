from django.contrib import admin
from .models import slider, banner_area, Main_Category, Category, Sub_Category, Section, Product, Product_Image, Additional_Information, Color, Brand, Coupon_Code, Order, OrderItem, Wishlist
# Register your models here.
class Product_Images(admin.TabularInline):
    model = Product_Image

class Additional_Informations(admin.TabularInline):
    model = Additional_Information

class Product_Admin(admin.ModelAdmin):
    inlines = (Product_Images, Additional_Informations)
    list_display = ('product_name', 'price', 'Categories', 'color', 'section')
    list_editable = ('Categories', 'section', 'color')

class OrderItemTubleinline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTubleinline]
    list_display = ['user', 'first_name', 'last_name', 'phone', 'email', 'address', 'payment_method', 'amount', 'paid']
    search_fields = ['first_name', 'payment_method']
    list_filter = ['first_name', 'payment_method']


admin.site.register(Section)
admin.site.register(Product, Product_Admin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)
admin.site.register(slider)
admin.site.register(banner_area)
admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Coupon_Code)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Wishlist)