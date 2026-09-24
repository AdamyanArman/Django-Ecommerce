from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("phone", "full_name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("phone", "first_name", "last_name")
    #ordering = ("-date_joined",)
    #readonly_fields = ("date_joined", "last_login")

    fieldsets = (
        (None, {
            "fields": ("phone", )
        }),
        ("Անձնական տվյալներ", {
            "fields": ("first_name", "last_name")
        }),
        ("Կարգավիճակ", {
            "fields": ("is_active",)
        }),
    )
