from django.contrib import admin

# Register your models here.
from app.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'auth_provider', 'created_on', 'updated_on']


admin.site.register(User, UserAdmin)