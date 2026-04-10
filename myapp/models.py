from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class UserDetails(models.Model):
    username=models.CharField(max_length=255)
    email = models.EmailField()
    userpassword=models.CharField(max_length=255)
    address=models.TextField()
    mobilenumber=models.CharField(max_length=12, unique=True)
    alternatemobile=models.CharField(max_length=12)

class Product(models.Model):
    name=models.CharField(max_length=100)


    price=models.IntegerField(default=0)
    description=models.TextField()
    image=models.ImageField(upload_to='products/',null=True, blank=True)

def __str__(self):
    return self.name



class Cart(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

class Order(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    ordered_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.name} ({self.user.username})"









    











