from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import SelectMultiple
from django import forms
from django.utils.safestring import mark_safe
from django.urls import path, reverse_lazy
from django.http import JsonResponse

from .models import Product, ProductTranslations, Attribute, AttributeValue, ProductAttributeValue
from category.models import Category


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name_hy", "name_en", "name_ru")
    search_fields = ("name_hy", "name_en", "name_ru")


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("attribute", "value_hy", "value_en", "value_ru")
    list_filter = ("attribute",)
    search_fields = ("value_hy", "value_en", "value_ru")


class ProductAdminForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=SelectMultiple(),
        label='Categories',
    )

    # Step 1: pick an Attribute to filter the values list below
    attribute_filter = forms.ModelChoiceField(
        queryset=Attribute.objects.all(),
        required=False,
        label='Filter by attribute',
        help_text='Pick an attribute, select values below, then click "Add selected ▸".',
        widget=forms.Select(attrs={
            'id': 'id_attribute_filter',
            'data-ajax-url': reverse_lazy('admin:product_values_by_attribute'),
        }),
    )

    # Step 2: values filtered by the chosen attribute via AJAX (staging field, not saved directly)
    values = forms.ModelMultipleChoiceField(
        queryset=AttributeValue.objects.none(),
        required=False,
        widget=SelectMultiple(attrs={'id': 'id_values_picker', 'size': 8}),
        label='Values for selected attribute',
    )

    # The real M2M field — accumulates selections across attributes, gets saved on submit
    attribute_values = forms.ModelMultipleChoiceField(
        queryset=AttributeValue.objects.all(),
        required=False,
        widget=SelectMultiple(attrs={'id': 'id_attributes_final', 'size': 8}),
        label='Selected attribute values (final)',
    )

    class Media:
        css = {
            'all': ('admin/css/widgets.css',),
        }
        js = ('admin/js/product_attribute_picker.js',)

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['categories'].initial = self.instance.categories.all()
            self.fields['attribute_values'].initial = self.instance.attribute_values.all()

        # Keep the 'values' queryset consistent on validation-error round-trips
        data = self.data if self.is_bound else None
        attr_id = data.get(self.add_prefix('attribute_filter')) if data else None
        if attr_id:
            self.fields['values'].queryset = AttributeValue.objects.filter(attribute_id=attr_id)

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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'ajax/values-by-attribute/',
                self.admin_site.admin_view(self.values_by_attribute),
                name='product_values_by_attribute',
            ),
        ]
        return custom_urls + urls

    def values_by_attribute(self, request):
        attribute_id = request.GET.get('attribute_id')
        if not attribute_id:
            return JsonResponse({'results': []})

        values = AttributeValue.objects.filter(
            attribute_id=attribute_id
        ).order_by('value_hy')

        results = [{'id': v.pk, 'text': str(v)} for v in values]
        return JsonResponse({'results': results})