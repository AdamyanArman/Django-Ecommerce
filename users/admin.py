from django.contrib import admin
from .models import Customer
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
'''@admin.register(Customer)
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
    )'''


#admin.site.register(Customer)

#admin.site.register(AbstractUser)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(BaseUserAdmin):
  # Ցանկում երևացող սյունակները
  list_display = ("phone", "first_name", "last_name", "is_staff", "is_active")
  list_filter = ("is_staff", "is_superuser", "is_active", "groups")
  search_fields = ("phone", "first_name", "last_name")

  # Խմբագրման էկրանի դաշտերը (Fieldsets)
  fieldsets = (
      (None, {"fields": ("phone", "password",)}),
      ("Անձնական տվյալներ", {"fields": ("first_name", "last_name")}),
      (
          "Իրավունքներ և կարգավիճակ",
          {
              "fields": (
                  "is_active",
                  "is_staff",
                  "is_superuser",
                  "groups",
                  "user_permissions",
              )
          },
      ),
      ("Կարևոր ամսաթվեր", {"fields": ("last_login", "date_joined")}),
  )

  # Նոր օգտատեր ավելացնելիս (Add User) երևացող դաշտերը
  add_fieldsets = BaseUserAdmin.add_fieldsets + (
      (
          "Լրացուցիչ տվյալներ",
          {
              "fields": ("phone",),
          },
      ),
  )