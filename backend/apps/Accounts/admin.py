from django.contrib import admin
from .models import Users
from django.contrib.auth.admin import UserAdmin


class AccountsAdmin(UserAdmin):
    
    list_display        = ('username','email','id')
    search_fields       = ('email', 'username',)
    readonly_fields     = ('id',)
    
    filter_horizontal   = ()
    list_filter         = ('created_on','updated_on',)
    fieldsets           = ()
admin.site.register(Users,AccountsAdmin)
