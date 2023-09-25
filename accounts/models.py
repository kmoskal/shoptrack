from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(unique=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


class Rks(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Shop(models.Model):
    shop_id = models.CharField(max_length=5, unique=True)
    district = models.CharField(max_length=50)
    region = models.CharField(max_length=20)
    rks = models.ForeignKey(Rks, null=True, on_delete=models.SET_NULL)
    kss = models.ForeignKey('Kss', null=True, on_delete=models.SET_NULL)
    employees = models.ManyToManyField('Ph', blank=True, related_name='shop_employees')


class Ph(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, null=True, on_delete=models.SET_NULL)
    employee_id = models.CharField(max_length=11, blank=True, unique=True)
    employee_ifs = models.IntegerField(blank=True, unique=True)


class Kss(models.Model):
    ph = models.OneToOneField(Ph, on_delete=models.CASCADE)
