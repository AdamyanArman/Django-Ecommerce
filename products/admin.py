from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import SelectMultiple
from django import forms
from django.utils.safestring import mark_safe
from django.urls import path, reverse_lazy
from django.http import JsonResponse

from .models import Product, ProductTranslations, Brand, Type
from category.models import Category

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Brand._meta.fields]


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('value_hy', 'value_en', 'value_ru')

class ProductAdminForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=SelectMultiple(),
        label='Categories',
    )


    class Media:
        css = {
            'all': ('admin/css/widgets.css',),
        }
        #js = ('admin/js/product_attribute_picker.js',)

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['categories'].initial = self.instance.categories.all()


    def save(self, commit=True):
        instance = super().save(commit=False)

        # super().save(commit=False) just set self.save_m2m = self._save_m2m,
        # which would silently shadow any class-level save_m2m override.
        # Grab that reference and wrap it so our category logic actually runs.
        original_save_m2m = self.save_m2m

        def save_m2m():
            original_save_m2m()  # saves attribute_values (real model M2M)
            self.save_categories()  # saves categories (virtual field, custom logic)

        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()

        return instance

    def save_categories(self):
        selected_categories = self.cleaned_data.get('categories', [])
        self.instance.categories.clear()
        for category in selected_categories:
            category.products.add(self.instance)


class ProductTranslationInline(admin.TabularInline):
    model = ProductTranslations
    extra = 3
    max_num = 3
    can_delete = False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [ProductTranslationInline]
    list_display = ['id', 'article', 'image', 'show_categories']
    readonly_fields = ['updated_at', 'created_at']

    def show_categories(self, obj):
        return ", ".join([c.name_hy for c in obj.categories.all()])
    show_categories.short_description = "Categories"
