from django.db import models

# Create your models here.
class Product(models.Model):
    pro_id = models.AutoField
    pro_name = models.CharField(max_length=100)
    pro_category = models.CharField(max_length=100, default="")
    pro_subcategory = models.CharField(max_length=100, default="")
    desc = models.CharField(max_length=100)
    pub_date = models.DateField()
    pro_price = models.IntegerField(default=0)
    pro_image = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return self.pro_name

class Contact(models.Model):
    msz_id = models.AutoField
    cus_name = models.CharField(max_length=100, default="")
    cus_email = models.CharField(max_length=100, default="")
    cus_mobile = models.CharField(max_length=10, default="")
    desc = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.cus_name

class Order(models.Model):
    o_id = models.AutoField(primary_key=True)
    o_json = models.CharField(max_length=5000, default="")
    o_amount = models.IntegerField(default=0)
    o_name = models.CharField(max_length=100, default="")
    o_email = models.CharField(max_length=100, default="")
    o_mobile = models.CharField(max_length=10, default="")
    o_add1 = models.CharField(max_length=1000, default="")
    o_add2 = models.CharField(max_length=1000, default="")
    o_city = models.CharField(max_length=100, default="")
    o_state = models.CharField(max_length=100, default="")
    o_zip = models.CharField(max_length=6, default="")

    def __str__(self):
        return self.o_name

class Userl(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=100, default="")
    u_email = models.CharField(max_length=100, default="")
    u_psswrd = models.CharField(max_length=100, default="")
    u_rpsswrd = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.u_name

class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."