from django.db import models
from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.storage import get_storage_class
import uuid

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,  email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
    username = None
    email = models.EmailField(
        max_length=255, primary_key=True, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, blank=True)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email+' , '+self.first_name+' '+self.middle_name+' '+self.last_name

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Pharmacy(models.Model):
    name = models.CharField(max_length=255, null=True, default=None)
    location = models.CharField(max_length=255, null=True, default=None)
    contact = models.CharField(max_length=255, null=True, default=None)
    class Meta:
        verbose_name_plural = "Pharmacies"
    def __str__(self):
        if self.name is not None:    
            return self.name
        else:
            return '_'

class Rider(models.Model):
    name = models.CharField(max_length=255, null=True, default=None)
    email = models.EmailField(max_length=255, null=True, default=None, blank=True)
    address = models.CharField(max_length=255, null=True,default=None, blank=True)
    contact = models.CharField(max_length=255, null=True, default=None,blank=True)
    def __str__(self):
        if self.name is not None:    
            return self.name
        else:
            return '_'
    
class Lab(models.Model):
    name = models.CharField(max_length=255,default=None, null=True)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=4, null=True, default=None)
    discount_percent = models.IntegerField(null=True, default=0)
    pharmacies = models.ManyToManyField('Pharmacy',related_name='%(class)s_pharmacies', blank=True)
    riders = models.ManyToManyField('Rider',related_name='%(class)s_riders', blank=True)
    
    

    def __str__(self):
        if self.name is not None:    
            return self.name
        else:
            return '_'

class Test(models.Model):
    name = models.CharField(max_length=255, null=True, default=None)
    description = models.CharField(max_length=255, null=True, default=None)
    labs = models.ManyToManyField('Lab',related_name='%(class)s_labs', blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.name is not None:    
            return self.name
        else:
            return '_'

class Patient(models.Model):
    user = models.ForeignKey('User', null=True,default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, default=None)
    city = models.CharField(max_length=255, null=True, default=None, blank=True)
    address = models.CharField(max_length=1000, null=True,default=None, blank=True)
    phone = models.CharField(max_length=255, null=True, default=None, blank=True)
    def __str__(self):
        if self.name is not None:    
            return self.name
        else:
            return '_'
    
class Cart(models.Model):
    test = models.ForeignKey('Test', related_name='%(class)s_tests', on_delete=models.CASCADE , default=None,null=True)
    patient = models.ForeignKey('Patient', related_name='%(class)s_patient', on_delete=models.CASCADE,null=True,default=None)
    rider = models.ForeignKey('Rider', related_name='%(class)s_rider', on_delete=models.CASCADE,null=True,default=None,blank=True)
    pharmacy = models.ForeignKey('Pharmacy', related_name='%(class)s_pharmacy', on_delete=models.CASCADE,null=True,default=None, blank=True)
    datetime=models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        if self.patient.name is not None:    
            return self.patient.name
        else:
            return '_'
class Order(models.Model):
    patient = models.ForeignKey('Patient', related_name='%(class)s_patient', on_delete=models.CASCADE,null=True,default=None)
    items = models.CharField(max_length=1000, null=True, default='', blank=True)
    datetime=models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        if self.patient.name is not None:    
            return self.patient.name
        else:
            return '_'