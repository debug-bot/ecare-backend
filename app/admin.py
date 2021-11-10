from django.contrib import admin
from .models import Pharmacy, Lab, Test, Rider, Cart, Patient
# Register your models here.
admin.site.register(Pharmacy)
admin.site.register(Lab)
admin.site.register(Test)
admin.site.register(Rider)
admin.site.register(Cart)
admin.site.register(Patient)