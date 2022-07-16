from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

num_only = RegexValidator(r'^[0-9]*$','only numbers are allowed')

role_choices = [ 
    ('Admin','Admin'),
    ('Client','Client'),
]

class User(AbstractUser):
    address = models.CharField(max_length=150 , blank=True , null= True)
    tel = models.CharField(max_length=10 , validators=[num_only],blank=True)
    image = models.ImageField(upload_to='profile_images/', blank = True , null = True , verbose_name='user_img')
    role = role = models.CharField(max_length=30 , choices=role_choices , default=role_choices[1])

class ProductType( models.Model):
    name = models.CharField(max_length=100 , blank= False , null = False)
    def __str__(self):
        return self.name

class Categorie(models.Model):
    name = models.CharField(max_length=100 , blank= False , null = False)
    def __str__(self):
        return self.name

class SubCategorie(models.Model):
    name = models.CharField(max_length=100 , blank= False , null = False)
    categorie = models.ForeignKey(Categorie , related_name='categorie',on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Color(models.Model):
    code = models.CharField(max_length= 7 , blank= False , null = False)
    def __str__(self):
        return self.code

class Size(models.Model):
    code = models.CharField(max_length=10)
    def __str__(self):
        return self.code

class Product(models.Model):
    code = models.CharField(max_length=30 , blank= False , null = False )
    name = models.CharField(max_length=100 , blank= False, null= False)
    regular_price = models.PositiveIntegerField(blank= False , null= False)
    disc_price = models.PositiveIntegerField(blank= True , null= True) #price after a discount
    type = models.ForeignKey(ProductType , related_name='product_type', on_delete=models.CASCADE)
    sub_categories = models.ManyToManyField(SubCategorie , related_name='product_sub_categories')
    available_colors = models.ManyToManyField(Color , related_name='product_colours')
    available_sizes = models.ManyToManyField(Size , related_name='product_sizes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE , related_name= 'product_images')
    image = models.ImageField(upload_to = 'product_images/', blank = False , null= False)
 
    def __str__(self):
        return self.image.url



