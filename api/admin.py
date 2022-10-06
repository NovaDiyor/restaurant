from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['id','username', 'first_name','last_name', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Extra'), {'fields': ('type',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

# Register your models here.

admin.site.register(Category)
admin.site.register(Food)
admin.site.register(Table)
admin.site.register(OrderItem)
admin.site.register(Order)
