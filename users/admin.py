from django.contrib import admin
from django.db.models import fields
from .models import (Product, ProductDetails, ProductImage, Category, SliderImage, Cart,
                    order, ordered_item, temp_order)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 6

class ProductDetailsInline(admin.TabularInline):
    model = ProductDetails
    extra = 0
    max_num = 4

class ProductAdmin(admin.ModelAdmin):
    # exclude = ['thumbnail']
    inlines = [ ProductImageInline, ProductDetailsInline ]

class SliderImageAdmin(admin.ModelAdmin):
    readonly_fields = ['name']
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False


class TempOrderAdmin(admin.ModelAdmin):
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(delivered = False)
    # order_date = models.DateField(auto_now_add=True)
    # order_address = models.CharField(max_length=50)
    # delivery_name = models.CharField(max_length=50)
    # delivery_phone = models.IntegerField()

    
    def user(self, obj):
        return obj.order.user
    
    def address(self, obj):
        return obj.order.order_address
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(SliderImage, SliderImageAdmin)

admin.site.register(Cart)

admin.site.register(order)
admin.site.register(temp_order, TempOrderAdmin)
admin.site.register(ordered_item)

