from django.contrib import admin
from .models import OtpModel,UserModel
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name',
                    'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(UserModel, CustomUserAdmin)

@admin.register(OtpModel)
class OtpModelAdmin(admin.ModelAdmin):
    list_display = ("created_at", "is_active", "otp", "user","id")[::-1]
