from django.db import models
from django_cryptography.fields import encrypt

class Seller_detail(models.Model):
    email = models.EmailField(max_length=1000)
    name = models.CharField(max_length=1000)
    age = models.IntegerField(default=None, null=True)
    def __str__(self):
        return self.email

class Li_Model(models.Model):
    seller_email = models.ForeignKey(Seller_detail, on_delete=models.CASCADE, default=None, null=True)
    licence_no = models.CharField(max_length=1000)
    is_used = models.BooleanField(default=False)
    def __str__(self):
        return self.licence_no
