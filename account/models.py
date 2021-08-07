from io import SEEK_CUR
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    profileImg = models.ImageField(default="profile1.png",null=True)

 
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
	
    CATEGORY = (
			('Indoor', 'Indoor'),
			('Out Door', 'Out Door'),
			)     
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(max_length=200, null=True,choices=CATEGORY)
    discription = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.name



class Order(models.Model):
    STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)
    
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    
    def __str__(self):
        return str(self.id)

