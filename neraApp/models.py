from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
import datetime

num_only = RegexValidator(r'^[0-9]*$','only numbers are allowed')

role_choices = [ 
    ('Admin','Admin'),
    ('Client','Client'),
    ('influencer','influencer'),
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
payment_choices = [
    ('CCP','CCP'),
    ('BaridiMob','BaridiMob'),
]
product_gender_choices = [
    ('féminin','féminin'),
    ('masculin','masculin'),
    ('mixte','mixte'),
]
panier_state = [
    ('payé','payé'),
    ('non payé','non payé'),
    ('confirmé','confirmé'),
    ('non confirmé','non confirmé'),
    ('livré','livré'),
]
language_choices = [
    ('arabe','arabe'),
    ('français','français'),
    ('anglais','anglais'),
]


class User(AbstractUser):
    address = models.CharField(max_length=50 , blank=True , null= True)
    tel = models.CharField(max_length=10 , validators=[num_only],blank=True)
    image = models.ImageField(upload_to='profile_images/', blank = True , null = True , verbose_name='user_img')
    role =  models.CharField(max_length=10 , choices=role_choices , default='Client')
    gender =  models.CharField(max_length=8 , choices=gender_choices, blank= True , null= True )
    age = models.PositiveIntegerField(blank=True , null= True)
    language = models.CharField(max_length=8,choices=language_choices,default='anglais')
    dark_mode = models.BooleanField(default=False)
    qte_purchased = models.PositiveIntegerField(default=0)

class ProductType( models.Model):
    name = models.CharField(max_length=25 , blank= False , null = False)
    image = models.ImageField(upload_to='type_images/', blank = True , null = True , verbose_name='type_img')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Categorie(models.Model ):
    name = models.CharField(max_length=25 , blank= False , null = False)
    types = models.ManyToManyField(ProductType , related_name='categories')
    image = models.ImageField(upload_to='categorie_images/', blank = True , null = True , verbose_name='categorie_img')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class SubCategorie(models.Model):
    name = models.CharField(max_length=25 , blank= False , null = False)
    image = models.ImageField(upload_to='sub_categorie_images/', blank = True , null = True , verbose_name='sub_categorie_img')
    categories = models.ManyToManyField(Categorie , related_name='sub_categorie')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Color(models.Model):
    code = models.CharField(max_length= 7 ,unique=True, blank= False , null = False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.code

class Size(models.Model):
    code = models.CharField(max_length=10 , unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.code

class Tag(models.Model):
    name = models.CharField(max_length=25)
    def __str__(self):
        return self.name
#produit
class Product(models.Model):
    owner = models.ForeignKey(User , related_name='product_owner', on_delete=models.CASCADE)
    code = models.CharField(max_length=30, null = True ,blank=True)
    name = models.CharField(max_length=25 , blank= False, null= False)
    description = models.TextField(null=True,blank=True)
    regular_price = models.DecimalField(decimal_places=2,max_digits =10)
    disc_price = models.DecimalField(decimal_places =2,max_digits = 10 , blank=True , null= True ) #  price after a discount
    disc_per= models.DecimalField(decimal_places =2,max_digits = 4,  default= 0.00)
    type = models.ForeignKey(ProductType , related_name='product_type', on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie,related_name='products',on_delete=models.CASCADE)
    sub_categorie = models.ForeignKey(SubCategorie , related_name='product_sub_categorie', on_delete=models.CASCADE)
    available_colors = models.ManyToManyField(Color , related_name='product_colours')
    available_sizes = models.ManyToManyField(Size , related_name='product_sizes')
    tags = models.ManyToManyField(Tag , related_name='Product')
    gender = models.CharField(max_length=8, choices=product_gender_choices, default=product_gender_choices[2])
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name= 'product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'product_images/', blank = False , null= False)
    def __str__(self):
        return self.image.url
        
class Company(models.Model):
    name = models.CharField(max_length=25 , blank= False , null= False)
    image = models.ImageField(upload_to = 'company_images/',blank = True , null = True , verbose_name='company_images')
    def __str__(self):
        return self.name

class Wilaya(models.Model):
    name = models.CharField(max_length= 25 , blank= False , null= False)
    def __str__(self):
        return self.name 

class Commune(models.Model):
    name = models.CharField(max_length= 25 , blank= False , null= False)
    wilaya = models.ForeignKey(Wilaya , related_name = 'Commune',on_delete = models.CASCADE)
    def __str__(self):
        return self.name

class StopDesk(models.Model):
    name = models.CharField(max_length= 25 , blank= False , null= False)
    delivery_price = models.PositiveIntegerField(blank= False , null= False)
    company = models.ForeignKey(Company , related_name = 'stop_desks', on_delete = models.CASCADE)
    wilaya = models.ForeignKey(Wilaya , related_name = 'stop_desks',on_delete = models.CASCADE)
    def __str__(self) :
        return self.name

class CommuneCompany(models.Model):
    commune = models.ForeignKey(Commune, related_name = 'company_commune', on_delete = models.CASCADE)
    company = models.ForeignKey(Company , related_name = 'commune_company', on_delete = models.CASCADE)
    delivery_price = models.PositiveIntegerField(blank= False , null= False)
    def __str__(self):
        return self.company.name +' '+ self.commune.name
    
class Panier(models.Model):
    owner = models.ForeignKey(User, related_name='panier',on_delete= models.CASCADE)
    detailed_place = models.CharField(max_length=35 , blank= False , null= False)
    wilaya = models.ForeignKey(Wilaya, related_name ='panier', on_delete = models.CASCADE)
    commune = models.ForeignKey(Commune, related_name = 'panier', on_delete = models.CASCADE)
    postal_code = models.PositiveIntegerField()
    advanced_payment = models.CharField(max_length=9 , choices= payment_choices, null = True , blank = True)
    desk_delivery = models.ForeignKey(StopDesk, related_name = 'panier' , on_delete = models.CASCADE , null = True)
    commune_delivery = models.ForeignKey(CommuneCompany, related_name = 'panier' , on_delete = models.CASCADE , null = True)
    state = models.CharField(max_length=12 , choices= panier_state , default= 'non payé')
    tel = models.CharField(max_length=10 , validators=[num_only], blank= True , null= True)
    total_price = models.DecimalField(decimal_places=2,max_digits=10, default=00.0 )
    created_at = models.DateTimeField(auto_now_add=True)

class PaymentConfirm(models.Model):
    transaction_code = models.CharField(max_length=20 , blank=True , null= True)
    image = models.ImageField(upload_to='payment_confirm/', blank = True , null = True , verbose_name='payment_confirm')
    panier = models.OneToOneField(Panier , related_name='payment_confirm', on_delete= models.CASCADE)
    accept_payment = models.BooleanField(default=False)

class Discount(models.Model):
    percentage = models.DecimalField(decimal_places =2,max_digits = 4)
    products = models.ManyToManyField(Product , related_name='discounts')
    categories = models.ManyToManyField(Categorie , related_name='discounts')
    subCategories = models.ManyToManyField(SubCategorie , related_name='code_promo_sub_categories')
    date_debut = models.DateField(blank=True , null=True)#change it later tooo not null
    date_limit =  models.DateField(blank=False , null=False)

class CodePromo(Discount):
    code = models.CharField(max_length=15 ,unique= True, blank= False , null= False)
    influencer = models.ForeignKey(User , related_name='code_promo_influencer',on_delete= models.CASCADE, null= True)
    used_one_time = models.BooleanField(default=True) #if code promo can be used once 
    type =  models.CharField(max_length=10 , choices= codePromo_choices , default= 'normal')
    users = models.ManyToManyField(User,related_name='code_promo_users')
    def __str__(self):
        return self.code

class Wishlist(models.Model):
    owner = models.OneToOneField(User , related_name='wishlist', on_delete= models.CASCADE)
    users = models.ManyToManyField(User , related_name='whishlists')

class Order(models.Model):
    owner = models.ForeignKey(User , related_name='orders', on_delete= models.CASCADE , null=True)
    panier = models.ForeignKey(Panier , related_name='orders',on_delete= models.CASCADE , null= True)
    product = models.ForeignKey(Product , related_name='product_ordered',on_delete=models.CASCADE)
    state = models.CharField(max_length=11 , choices= order_states , default='non_traitée')
    price_to_pay = models.DecimalField(decimal_places =2,max_digits =10)
    color = models.CharField(max_length=7 , blank=False , null = False)
    size = models.CharField(max_length=10 , blank= False , null = False)
    wishlist = models.ForeignKey(Wishlist, related_name='orders',on_delete=models.CASCADE, null=True)
    qte = models.PositiveIntegerField(default = 1)
    code_promo = models.ForeignKey(CodePromo, related_name = 'orders',on_delete = models.CASCADE ,null = True)
    created_at = models.DateTimeField(auto_now_add=True)

class FavoriteList(models.Model):
    owner = models.OneToOneField(User , related_name='Favoritelist', on_delete= models.CASCADE)
    products = models.ManyToManyField(Product , related_name='favorite_products')

class Request(models.Model):
    sender = models.ForeignKey(User , related_name='request_sent', on_delete= models.CASCADE)
    wishlist = models.ForeignKey(Wishlist , related_name='request',on_delete= models.CASCADE)
    is_accepted = models.BooleanField(default= False)

class Gift(models.Model):
    product = models.ForeignKey(Product , related_name='gift',on_delete=models.CASCADE)
    rarity = models.FloatField(validators=[MinValueValidator(0.0),MaxValueValidator(100)]) #the proba of gift to be win

class EasterEgg(models.Model):
    winner = models.ForeignKey(User , related_name='easter_egg',on_delete=models.CASCADE)
    gift = models.ForeignKey(Gift , related_name='easter_egg_gift',on_delete= models.CASCADE)

#easter_eggs_settings
class Settings(models.Model): 
    activate_gifts = models.BooleanField(default= True) #activate or not gifts system
    qte_to_win = models.PositiveIntegerField(default= 5) # the quantity that allow win a gift
    poste_delivery_price = models.PositiveIntegerField(default = 0) #the price of delivery by poste
    ccp_code = models.CharField(null = True , blank = True,max_length = 10)
    ccp_cle = models.CharField(null = True , blank = True,max_length = 2) 

class News(models.Model):
    image = models.ImageField(upload_to='news_images/', blank = True , null = True , verbose_name='news_image')

class Visitor(models.Model):
    ip_add = models. GenericIPAddressField()
    last_visit = models.DateField(default=datetime.date.today)

class Signal(models.Model):
    user = models.ForeignKey(User , related_name='signal',on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to = 'signals_images/', blank = True, null= True)
    