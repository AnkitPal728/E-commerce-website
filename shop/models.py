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