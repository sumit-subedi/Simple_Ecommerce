from django.contrib import admin
from .models import (Product, ProductDescription, ProductImage, Category, SliderImage)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 6

class ProductDescriptionInline(admin.TabularInline):
    model = ProductDescription
    extra = 0
    max_num = 4

class ProductAdmin(admin.ModelAdmin):
    # exclude = ['thumbnail']
    inlines = [ ProductImageInline, ProductDescriptionInline ]

class SliderImageAdmin(admin.ModelAdmin):
    readonly_fields = ['name']
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(SliderImage, SliderImageAdmin)
