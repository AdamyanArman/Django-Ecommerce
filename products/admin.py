from django.contrib import admin
from .models import Product, ProductTranslations

# Register your models here.

class ProductTranslationInline(admin.TabularInline):
    model = ProductTranslations
    #fields = ['language', ('name', 'description')]
    extra=3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductTranslationInline]


admin.site.register(Product, ProductAdmin)