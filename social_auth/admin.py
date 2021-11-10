from django.contrib import admin

# Register your models here.
from django.conf import settings
from app.models import User


admin.site.register(User)
