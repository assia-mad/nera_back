from django.shortcuts import get_object_or_404
from itertools import product
from unicodedata import decimal
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer , UserDetailsSerializer , PasswordChangeSerializer
from .models import *
import decimal
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import random

class ManageusersSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ['id','first_name','last_name','email','address','tel','image','role','gender','age','language','is_staff', 'is_active']


class UpdateUsersByAdminSerializer(serializers.Serializer):
    role  = serializers.ChoiceField(choices=role_choices , default=role_choices[0])
    is_active = serializers.BooleanField( default=True)
        
    def update(self, instance, validated_data):
        if instance.role != validated_data.get('role') :
            subject = 'Role changed'
            message = f'Salut {instance.first_name} {instance.last_name} your role has been changed please logout then login again to get your suitable interface'
            from_email = settings.EMAIL_HOST_USER 
            recipient_list = [instance.email]
            send_mail(subject, message,from_email,recipient_list , fail_silently=False)
        if validated_data.get('role') == 'Admin' :
            instance.is_staff = True
        if validated_data.get('role') != 'Admin':
            instance.is_staff= False
        instance.role = validated_data.get('role', instance.role)
            
        if instance.is_active != validated_data.get('is_active'):
            if validated_data.get('is_active') == True:
                account = 'has been activated'
            else :
                account = 'has been desactivated'
            subject = 'Nera Shop account'
            message = f'Hi {instance.first_name} {instance.last_name} your account {account}'
            from_email = settings.EMAIL_HOST_USER 
            recipient_list = [instance.email]
            send_mail(subject, message,from_email,recipient_list , fail_silently=False)      
        instance.is_active = validated_data.get('is_active', instance.is_active)
        try:
            instance.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass    
        instance.save()
        return instance 
    

class FavoritListSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        queryset= Product.objects.all(),
        many=True,
        required=False
    )
    class Meta:
        model = FavoriteList
        fields = ['id','owner','products']

class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required = True , write_only = True)
    last_name = serializers.CharField(required = True , write_only = True)
    email = serializers.EmailField(required = True)
    address = serializers.CharField(max_length=150 ,required = True)
    tel = serializers.CharField(max_length=10 , validators=[num_only], required = True)
    gender = serializers.ChoiceField(choices= gender_choices)
    age = serializers.IntegerField(min_value = 10)
    password1 = serializers.CharField( write_only=True, required=True, style={'input_type': 'password', })
    password2 = serializers.CharField( write_only=True, required=True, style={'input_type': 'password', })
    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['first_name'] = self.validated_data.get('first_name', '')
        data_dict['last_name'] = self.validated_data.get('last_name', '')
        data_dict['address'] = self.validated_data.get('address', '')
        data_dict['tel'] = self.validated_data.get('tel', '')
        data_dict['gender'] = self.validated_data.get('gender', '')
        data_dict['age'] = self.validated_data.get('age', '')
        return data_dict
    def save(self, request):
        user = super().save(request)
        Favorite = FavoriteList.objects.create(owner = user)
        wishlist = Wishlist.objects.create(owner = user)
        return user

class CustomLoginSerializer(LoginSerializer): 
    username = None

class CustomUserDetailSerializer(UserDetailsSerializer):
    address = serializers.CharField(max_length=150 )
    tel = serializers.CharField(max_length=10 , validators=[num_only])
    image = serializers.ImageField(allow_null=True)
    role = serializers.ChoiceField(choices= role_choices)
    gender = serializers.ChoiceField(choices= gender_choices)
    age = serializers.IntegerField(min_value = 10)
    language = serializers.ChoiceField(choices=language_choices)
    qte_purchased = serializers.IntegerField(default = 0)
    class Meta : 
        model = User
        fields = ['id','first_name','last_name','email','address','tel','image','role','gender','age','language','qte_purchased','is_staff', 'is_active']

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta :
        model = ProductType
        fields = ['id','name','image','created_at']
        lookup_fields = 'id'

class CategorieSerializer(serializers.ModelSerializer):
    types = serializers.PrimaryKeyRelatedField(
        queryset= ProductType.objects.all(),
        many=True,
        required=True
    )
    class Meta :
        model = Categorie
        fields = ['id','name','types','image','created_at']

class SubCategorieSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset= Categorie.objects.all(),
        many=True,
        required=True
    )
    class Meta :
        model = SubCategorie
        fields = ['id','name','categories','image','created_at']

class ColorSerializer(serializers.ModelSerializer):
    class Meta :
        model = Color
        fields = ['id','code','created_at']

class SizeSerializer(serializers.ModelSerializer):
    class Meta :
        model = Size
        fields = ['id','code','created_at']

class ImageSerializer(serializers.ModelSerializer):
    class Meta :
        model = ProductImage
        fields = ['image','product']

class ProductSerializer(serializers.ModelSerializer):
    available_colors = serializers.PrimaryKeyRelatedField(
        queryset= Color.objects.all(),
        many=True,
        required=True
    )
    available_sizes = serializers.PrimaryKeyRelatedField(
        queryset= Size.objects.all(),
        many=True,
        required= True
    )
    images= ImageSerializer(many=True, read_only = True,required = False)
    uploaded_images = serializers.ListField ( child = serializers.FileField(max_length = 1000000, allow_empty_file =True, use_url = False) , write_only = True )
    tags = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    update_tags = serializers.ListField(
        child=serializers.CharField(max_length=100), write_only=True , required = False)
     
    class Meta:
       model = Product
       fields = ['id','owner','code','name','regular_price','disc_price','disc_per','sub_categorie','type','available_colors','available_sizes','gender','created_at','images','uploaded_images','tags','update_tags']

    def create(self, validated_data):
        uploaded_data = validated_data.pop('uploaded_images')
        tag_names = validated_data.pop('update_tags')
        tags = []
        new_product = super().create(validated_data)
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        new_product.tags.set(tags)
        print(new_product.name)
        regular_price = new_product.regular_price
        percentage = decimal.Decimal(new_product.disc_per / 100)
        new_product.disc_price = regular_price - (regular_price * percentage)
        print(new_product.disc_price)
        new_product.save()
        for uploaded_item in uploaded_data:
            new_product_image = ProductImage.objects.create(product = new_product, image = uploaded_item)
        new_product.save()
        return new_product       
    
    def update(self, instance, validated_data):
        percentage = validated_data.get('disc_per') / 100
        regular_price = validated_data.get('regular_price')
        instance.disc_price = regular_price - (regular_price * percentage)
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.regular_price = validated_data.get('regular_price', instance.regular_price)
        instance.disc_per = validated_data.get('disc_per', instance.disc_per)
        instance.type = validated_data.get('type', instance.type)
        instance.name = validated_data.get('name', instance.name)
        instance.sub_categorie = validated_data.get('sub_categorie',instance.sub_categorie)
        instance.gender = validated_data.get('gender',instance.gender) 
        available_colors= validated_data.pop('available_colors')
        for color in available_colors :
            instance.available_colors.add(color)
        available_sizes = validated_data.pop('available_sizes')
        for size in available_sizes :
            instance.available_sizes.add(size)
        tag_names = validated_data.pop('update_tags')
        tags = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        uploaded_data = validated_data.pop('uploaded_images')
        for uploaded_item in uploaded_data:
            new_product_image = ProductImage.objects.create(product = instance, image = uploaded_item)
        instance.tags.set(tags)
        instance.save() 
        return instance

class OrderSerializer(serializers.ModelSerializer):
    class Meta :
        model = Order
        fields = ['id','owner','panier','product','color','size','state','wishlist','price_to_pay','qte','created_at']
    def create(self, validated_data):
        owner = validated_data.get('owner')
        qte = validated_data.get('qte')
        owner.qte_purchased += qte
        admin_settings = Settings.objects.first()
        if admin_settings.activate_gifts and owner.qte_purchased >= admin_settings.qte_to_win :
            random_gift = random.choices(Gift.objects.values_list('id',flat=True).order_by('id'),Gift.objects.values_list('rarity',flat=True).order_by('id'),k=1)
            print(random_gift[0])
            easter_egg = EasterEgg.objects.create(winner = owner , gift = Gift.objects.get(pk = random_gift[0]))
            owner.qte_purchased = 0
        owner.save()
        return super().create(validated_data)

class CompanySerializer(serializers.ModelSerializer):
    class Meta :
        model = Company
        fields = ['id','name','image']

class WilayaSerializer(serializers.ModelSerializer):
    class Meta :
        model = Wilaya
        fields = ['id','company','name','delivery_price']

class CommuneSerializer(serializers.ModelSerializer):
    class Meta :
        model = Commune
        fields = ['id','name','wilaya','delivery_price']

class DeliverySerializer(serializers.ModelSerializer):
    class Meta :
        model = Delivery
        fields = ['id','company','payment_method','description']

class PanierSerializer(serializers.ModelSerializer):
    orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.filter(panier__isnull = True))
    class Meta :
        model = Panier
        fields = ['id','owner','wilaya','commune','detailed_place','postal_code','payment_delivry','tel','state','created_at','orders','home_delivery']
    def create(self, validated_data):
        orders = validated_data.pop('orders')
        panier = super().create(validated_data)
        for order in orders:
            order.panier = panier
            order.save()
        return panier

class PaymentConfirmSerializer(serializers.ModelSerializer):
    class Meta :
        model = PaymentConfirm
        fields = ['id','transaction_code','image','panier']
 
class CodePromoSerializer(serializers.ModelSerializer):
    products= serializers.PrimaryKeyRelatedField(
        queryset= Product.objects.all(),
        many=True,
        required= False
    )
    subCategories = serializers.PrimaryKeyRelatedField(
        queryset= SubCategorie.objects.all(),
        many=True,
        required= False
    )
    users = serializers.PrimaryKeyRelatedField(
        queryset= User.objects.all(),
        many=True,
        required= False
    )
    class Meta :
        model = CodePromo
        fields = ['id','code','influencer','percentage','type','products','subCategories','users','date_limit','used_one_time']

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code')
        instance.percentage = validated_data.get('percentage')
        instance.type = validated_data.get('type')
        instance.date_limit = validated_data.get('date_limit')
        subCategories = validated_data.pop('subCategories')
        for sub_cat in subCategories :
            instance.subCategories.add(sub_cat)
        products = validated_data.pop('products')
        for product in products :
            instance.products.add(product)
        users = validated_data.pop('users')
        for user in users :
            if instance.used_one_time == True :
                if  user in instance.users.all():
                    error = {'message':  'code can be used only once'}
                    raise serializers.ValidationError(error) 
            instance.users.add(user)
        return instance

class WishlistSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        queryset= User.objects.all(),
        many=True,
        required= False
    )
    class Meta:
        model = Wishlist
        fields = ['id','owner','users']
 

class TagSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Tag
        fields = ['id','name']    

class PaymentConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentConfirm
        fields = ['id','transaction_code','image','panier']

class RequestSerializer(serializers.ModelSerializer):
    class Meta :
        model = Request
        fields = ['id','sender','wishlist','is_accepted']    
    def update(self, instance, validated_data):
        is_accepted = validated_data.get('is_accepted')
        wishlist = validated_data.get('wishlist')
        sender = validated_data.get('sender')
        if is_accepted == True :
            wishlist.users.add(sender)
        return super().update(instance, validated_data)

class EasterEggSerializer(serializers.ModelSerializer):
    class Meta :
        model = EasterEgg
        fields = ['id','winner','gift']

class Settingserializer(serializers.ModelSerializer):
    class Meta :
        model = Settings
        fields = ['id','activate_gifts','qte_to_win']

class NewsSerializer(serializers.ModelSerializer):
    class Meta :
        model = News
        fields = ['id','image']

class GiftSerializer(serializers.ModelSerializer):
    class Meta :
        model = Gift
        fields = ['id','product','rarity']

class DarkModeSerializer(serializers.ModelSerializer):
    class Meta :
        model = DarkMode
        fields = ['id','user','dark_mode']