from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profile_pic/customerprofile_pic/',null=True,blank=True)
    address=models.CharField(max_length=20,null=False)
    mobile=models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name
    @property
    def thumbnail_preview(self):
        if self.profile_pic:
            return mark_safe('<img src="/static{}" width="100" height="100"/>'.format(self.profile_pic.url))
        return""

class Product(models.Model):
    name=models.CharField(max_length=40)
    product_img=models.ImageField(upload_to='product_img/',null=True,blank=True)
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    @property
    def thumbnail_preview(self):
        if self.product_img:
            return mark_safe('<img src="/static{}" width="100" height="100"/>'.format(self.product_img.url))
        return""

class Order(models.Model):
    STATUS=(
            ('Pending','Pending'),
            ('order Confirmed','Order Confirmed'),
            ('Out for Delivery','Out for Delivery'),
            ('Delivered','Delivered'),
            )
    customer=models.ForeignKey('Customer',on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
    email=models.CharField(max_length=50,null=True)
    address=models.CharField(max_length=50,null=True)
    mobile=models.CharField(max_length=50,null=True)
    order_date=models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)

class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date=models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name
