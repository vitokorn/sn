from django.contrib import admin
from .models import SNUser


# Register your models here.
class SNUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name','email','is_staff','is_active','date_joined', 'last_activity')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)


admin.site.register(SNUser, SNUserAdmin)