from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StaffProfile,NameVerification,TwoFactorAuth


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "full_name","phone_number","time_zone","date_of_birth", "role", "is_active", "is_staff","profile_image")
    list_filter = ("role", "is_active", "is_staff","time_zone")
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
            "fields": ("email", "full_name", "phone_number","date_of_birth", "role", "password1", "password2", "time_zone","language", "is_active", "is_staff"),
        }),
    )

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or (request.user.role in ['staff', 'admin']):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

admin.site.register(CustomUser, CustomUserAdmin)
class StaffProfileAdmin(admin.ModelAdmin): # updated
    def get_queryset(self, request):
        qs=super().get_queryset(request)
        return qs.filter(user__role='staff')

admin.site.register(StaffProfile,StaffProfileAdmin)

admin.site.register(NameVerification)
admin.site.register(TwoFactorAuth)