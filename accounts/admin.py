from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "full_name","phone_number","date_of_birth", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("email", "full_name", "phone_number")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name", "phone_number","date_of_birth")}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser",'groups','user_permissions')}), 
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "phone_number","date_of_birth", "role", "password1", "password2", "is_active", "is_staff"),
        }),
    )
     
    def has_change_permission(self, request, obj=None):
        return True

admin.site.register(CustomUser, CustomUserAdmin)
