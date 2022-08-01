from distutils.command.upload import upload
from email.mime import image
from enum import Flag
from pickle import FROZENSET
from typing import Type
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


num_only = RegexValidator(r'^[0-9]*$','only numbers are allowed')

role_choices = [ 
    ('Admin','Admin'),
    ('Client','Client'),
]
order_states = [
    ('non_traitée','non_traitée'),
    ('Traitée','Traitée'),
    ('annulée','annulée'),
]
codePromo_choices = [ 
    ('normal','normal'),
    ('influencer','influencer'),
]
gender_choices = [
    ('féminin','féminin'),
    ('masculin','masculin'),
]

class User(AbstractUser):
    address = models.CharField(max_length=150 , blank=True , null= True)
    tel = models.CharField(max_length=10 , validators=[num_only],blank=True)
    image = models.ImageField(upload_to='profile_images/', blank = True , null = True , verbose_name='user_img')
    role =  models.CharField(max_length=30 , choices=role_choices , default=role_choices[1])
    gender =  models.CharField(max_length=30 , choices=gender_choices, blank= True , null= True )
    age = models.PositiveIntegerField(blank=True , null= True)

class ProductType( models.Model):
    name = models.CharField(max_length=100 , blank= False , null = False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Categorie(models.Model):
    name = models.CharField(max_length=100 , blank= False , null = False)
    types = models.ManyToManyField(ProductType , related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class SubCategorie(models.Model):
    name = models.CharField(max_length=100 , blank= False , null = False)
    categories = models.ManyToManyField(Categorie , related_name='sub_categorie')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Color(models.Model):
    code = models.CharField(max_length= 7 , blank= False , null = False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.code

class Size(models.Model):
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.code

class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
#produit
class Product(models.Model):
    owner = models.ForeignKey(User , related_name='product_owner', on_delete=models.CASCADE)
    code = models.CharField(max_length=30 , blank= False , null = False )
    name = models.CharField(max_length=100 , blank= False, null= False)
    regular_price = models.DecimalField(decimal_places =2,max_digits =10 )
    disc_price = models.DecimalField(decimal_places =2,max_digits = 10 , blank=True , null= True ) #  price after a discount
    disc_per= models.DecimalField(decimal_places =2,max_digits = 3,  default= 0.00)
    type = models.ForeignKey(ProductType , related_name='product_type', on_delete=models.CASCADE)
    sub_categorie = models.ForeignKey(SubCategorie , related_name='product_sub_categorie', on_delete=models.CASCADE)
    available_colors = models.ManyToManyField(Color , related_name='product_colours')
    available_sizes = models.ManyToManyField(Size , related_name='product_sizes')
    tags = models.ManyToManyField(Tag , related_name='Product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name= 'product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'product_images/', blank = False , null= False)
    def __str__(self):
        return self.image.url

class Panier(models.Model):
    owner = models.ForeignKey(User , related_name='panier',on_delete= models.CASCADE)
    address = models.CharField(max_length=150 , blank= False , null= False)
    wilaya = models.CharField(max_length=100 , blank= False , null= False)
    postal_code = models.PositiveIntegerField()
    payment_delivry = models.CharField(max_length=150 , blank= False , null= False)
    tel = models.CharField(max_length=10 , validators=[num_only], blank= True , null= True)
    created_at = models.DateTimeField(auto_now_add=True)

class PaymentConfirm(models.Model):
    transaction_code = models.CharField(max_length=150 , blank=True , null= True)
    image = models.ImageField(upload_to='payment_confirm/', blank = True , null = True , verbose_name='payment_confirm')
    panier = models.OneToOneField(Panier , related_name='payment_confirm', on_delete= models.CASCADE)

class CodePromo(models.Model):
    code = models.CharField(max_length=50 , blank= False , null= False)
    percentage = models.DecimalField(decimal_places =2,max_digits = 4)
    type =  models.CharField(max_length=30 , choices= codePromo_choices , default= codePromo_choices[0])
    products = models.ManyToManyField(Product , related_name='code_promo_products')
    users = models.ManyToManyField(User,related_name='code_promo_users')
    subCategories = models.ManyToManyField(SubCategorie , related_name='code_promo_sub_categories')
    date_limit =  models.DateField(blank=False , null=False)
    def __str__(self):
        return self.code

class Wishlist(models.Model):
    owner = models.OneToOneField(User , related_name='wishlist', on_delete= models.CASCADE)

#commande
class Order(models.Model):
    panier = models.ForeignKey(Panier , related_name='order',on_delete= models.CASCADE , null= True)
    product = models.ForeignKey(Product , related_name='product_ordered',on_delete=models.CASCADE)
    state = models.CharField(max_length=50 , choices= order_states , default=order_states[0])
    price_to_pay = models.DecimalField(decimal_places =2,max_digits =10 )
    color = models.CharField(max_length=7 , blank=False , null = False)
    size = models.CharField(max_length=10 , blank= False , null = False)
    wishlist = models.ForeignKey(Wishlist, related_name='orders',on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class FavoriteList(models.Model):
    owner = models.OneToOneField(User , related_name='Favoritelist', on_delete= models.CASCADE)
    products = models.ManyToManyField(Product , related_name='favorite_products')









