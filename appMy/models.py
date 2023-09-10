from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Category Model
class Category(models.Model):
    title = models.CharField(("Kategori"), max_length=50)
    
    def __str__(self) -> str:
        return self.title

# Product Model
class Product(models.Model):
    title = models.CharField(("Ürün"), max_length=50)
    desc = models.TextField(("Ürün Açıklaması"))
    features = models.TextField(("Ürün Özellikleri"))
    productImg = models.ImageField(("Ürün Fotoğrafı"), upload_to=None, height_field=None, width_field=None, max_length=None)
    productImg2 = models.ImageField(("Ürün Fotoğrafı 2"), upload_to=None, height_field=None, width_field=None, max_length=None)
    productCategory = models.ForeignKey(Category, verbose_name=("Ürün Kategorisi"), on_delete=models.CASCADE, null=True, blank=True)
    productPrice = models.FloatField(("Ürün Fiyatı"))
    
    def __str__(self) -> str:
        return self.title
    
# Profile Model
class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name=(""), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE, null=True, blank=True)
    profile_img = models.ImageField(("Profil Fotoğrafı"), upload_to=None, height_field=None, width_field=None, max_length=None)
    

# Comment Model
class Comment(models.Model):
    product = models.ForeignKey(Product, verbose_name=("Ürün"), on_delete=models.CASCADE, null=True, blank=True) 
    user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE, null=True, blank=True)
    productComment = models.TextField(("Ürün Yorumu"))
    commentTime = models.DateTimeField(("Yorum Zamanı"), auto_now=False, auto_now_add=True)
