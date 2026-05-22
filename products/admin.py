from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import SelectMultiple

from .models import Product, ProductTranslations
from category.models import Category
from django import forms

# Register your models here.

class ProductAdminForm(forms.ModelForm):
    categories=forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        #widget=admin.widgets.FilteredSelectMultiple('Categories', is_stacked=False),
        #widget=FilteredSelectMultiple(verbose_name='Categories', is_stacked=False),
        widget=SelectMultiple(),
        label='Categories',
    )

    class Media:
        css = {
            'all': ('admin/css/widgets.css',),
        }
        # Սա ակտիվացնում է "Խմբավորել/Ավելացնել" JavaScript ֆունկցիաները
        js = ('/admin/jsi18n/',)

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Եթե պրոդուկտը արդեն գոյություն ունի (խմբագրում ենք), բերում ենք իր ընթացիկ կատեգորիաները
        if self.instance and self.instance.pk:
            self.fields['categories'].initial = self.instance.categories.all()

    def save(self, commit=True):
        product = super().save(commit=commit)
        # Եթե միանգամից սեյվ է լինում, կատարում ենք կապերի թարմացումը
        if commit:
            self.save_categories()
        return product

    def save_categories(self):
        # Սինքրոնացնում ենք ընտրված Category-ները բազայում
        selected_categories = self.cleaned_data.get('categories', [])
        self.instance.categories.clear()  # Հեռացնում ենք հին կապերը
        for category in selected_categories:
            category.products.add(self.instance)  # Ավելացնում ենք նորերը

class ProductTranslationInline(admin.TabularInline):
    model = ProductTranslations
    #fields = ['language', ('name', 'description')]
    extra=3
    max_num = 3
    can_delete = False



#@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form=ProductAdminForm
    inlines = [ProductTranslationInline]
    #filter_horizontal = ['Category.categories']
    list_display = ['id', 'article', 'image', 'show_categories']
    readonly_fields = ['updated_at', 'created_at']


    '''def show_categories(self, obj):
        return ', '.join([cat.name_hy for cat in obj.categories.all()])

    show_categories.short_description='Categories'''

    def show_categories(self, obj):
        return ", ".join([c.name_hy for c in obj.categories.all()])

    show_categories.short_description = "Categories"



admin.site.register(Product, ProductAdmin)