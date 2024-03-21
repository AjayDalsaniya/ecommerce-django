
from django.db import models
import datetime

# Create your models here.
class user(models.Model):
     email = models.EmailField(unique=True,max_length=30)
     password = models.CharField(max_length=30)
     role = models.CharField(max_length=30)
     def __str__(self):
        return self.email

class customer(models.Model):
     cust_id  = models.ForeignKey(user,on_delete=models.CASCADE)
     name = models.CharField(max_length=30)
     country = models.CharField(max_length=30)
     state = models.CharField(max_length=30)
     city = models.CharField(max_length=30)
     pic = models.FileField(upload_to="media/cutomer/",null=True)
     def __str__(self):
        return self.name


class product(models.Model):
     mobile_name = models.CharField(max_length=30)
     ram = models.CharField(max_length=30)
     rom = models.CharField(max_length=30)
     info = models.TextField()
     price = models.CharField(max_length=30)
     pic = models.FileField(upload_to="media/mobile/")
     def __str__(self):
        return self.mobile_name

class order(models.Model):
     product_id = models.ForeignKey(product,on_delete=models.CASCADE)
     user_id = models.ForeignKey(user,on_delete=models.CASCADE)
     cust_id = models.ForeignKey(customer,on_delete=models.CASCADE)
     name = models.CharField(max_length=30)
     mobile_no = models.CharField(max_length=30,null=True)
     country = models.CharField(max_length=30)
     state  = models.CharField(max_length=30)
     city = models.CharField(max_length=30)
     productname = models.CharField(max_length=30)
     ram = models.CharField(max_length=30)
     rom  = models.CharField(max_length=30)
     qty = models.CharField(max_length=30)
     price = models.CharField(max_length=30)
     total_price = models.CharField(max_length=30)
     date = models.DateField(default=datetime.datetime.today)
     status = models.BooleanField(default= False)

     def __str__(self):
        return self.name

class AddCart(models.Model):
      product_id = models.ForeignKey(product,on_delete=models.CASCADE)
      user_id = models.ForeignKey(user,on_delete=models.CASCADE)
      cust_id = models.ForeignKey(customer,on_delete=models.CASCADE)
      productname = models.CharField(max_length=30)
      ram = models.CharField(max_length=30)
      rom  = models.CharField(max_length=30)
      qty = models.CharField(max_length=30)
      price = models.CharField(max_length=30)
      total_price = models.CharField(max_length=30)
      pic = models.FileField(upload_to="media/mobile/")
    
      def __str__(self):
        return self.productname
     

     

    