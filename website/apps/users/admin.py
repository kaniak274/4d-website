from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('login', 'email', 'coins')
    list_filter = ('admin',)
    fieldsets = (
        ('Informacje konta', {'fields': (
            'login',
            'email',
            'social_id',
            'coins',
        ),}),
        ('Zezwolenia', {'fields': ('admin',)}),
        ('Bany', {'fields': ('banlength',),}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'login', 'social_id')}
        ),
    )

    search_fields = ('login', 'email',)
    ordering = ('login', 'email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
