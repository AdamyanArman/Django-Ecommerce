from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Թույլ չի տալիս դատարկ տողեր ավելացնել (ըստ ցանկության կարող եք փոխել)
    readonly_fields = ('subtotal',)  # Կարող եք դարձնել միայն կարդալու (read-only), որ ադմինիստրատորը պատահաբար չփոխի հին պատվերի գները
    raw_id_fields = ('product',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'phone', 'location', 'payment_method', 'is_paid', 'total_price', 'status', 'updated_at', 'created_at')
    list_editable = ('payment_method', 'is_paid', 'status')
    search_fields = ('id', 'name', 'surname', 'phone', 'location')
    inlines = [OrderItemInline]
    list_filter = ('id', 'name', 'surname', 'phone', 'location', 'payment_method', 'is_paid', 'status', 'updated_at', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'total_price')
