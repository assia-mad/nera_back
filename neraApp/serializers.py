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

class ManageusersSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ['id','first_name','last_name','email','address','tel','image','role','is_staff', 'is_active']


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
    password1 = serializers.CharField( write_only=True, required=True, style={'input_type': 'password', })
    password2 = serializers.CharField( write_only=True, required=True, style={'input_type': 'password', })
    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['first_name'] = self.validated_data.get('first_name', '')
        data_dict['last_name'] = self.validated_data.get('last_name', '')
        data_dict['address'] = self.validated_data.get('address', '')
        data_dict['tel'] = self.validated_data.get('tel', '')
        return data_dict
    def save(self, request):
        user =super().save(request)
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
    class Meta : 
        model = User
        fields = ['id','first_name','last_name','email','address','tel','image','role','is_staff', 'is_active']

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta :
        model = ProductType
        fields = ['id','name','created_at']
        lookup_fields = 'id'

class CategorieSerializer(serializers.ModelSerializer):
    class Meta :
        model = Categorie
        fields = ['id','name','created_at']

class SubCategorieSerializer(serializers.ModelSerializer):
    class Meta :
        model = SubCategorie
        fields = ['id','name','categorie','created_at']

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
        fields = ['image']

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
    sub_categories= serializers.PrimaryKeyRelatedField(
        queryset= SubCategorie.objects.all(),
        many=True,
        required= False
    )
    images= ImageSerializer(many=True, read_only = True,required = False)
    uploaded_images = serializers.ListField ( child = serializers.FileField(max_length = 1000000, allow_empty_file =True, use_url = False) , write_only = True )
     
    class Meta:
       model = Product
       fields = ['id','owner','code','name','regular_price','disc_price','disc_per','type','sub_categories','available_colors','available_sizes','created_at','images','uploaded_images']

    def create(self, validated_data):
        uploaded_data = validated_data.pop('uploaded_images')
        new_product = super().create(validated_data)
        print(new_product.name)
        regular_price = new_product.regular_price
        percentage = decimal.Decimal(new_product.disc_per / 100)
        new_product.disc_price = regular_price - (regular_price * percentage)
        for uploaded_item in uploaded_data:
            new_product_image = ProductImage.objects.create(product = new_product, image = uploaded_item)
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
        sub_categories = validated_data.pop('sub_categories')
        for sub_cat in sub_categories :
            instance.sub_categories.add(sub_cat)
        available_colors= validated_data.pop('available_colors')
        for color in available_colors :
            instance.available_colors.add(color)
        available_sizes = validated_data.pop('available_sizes')
        for size in available_sizes :
            instance.available_sizes.add(size)
        instance.save() 
        return instance

class OrderSerializer(serializers.ModelSerializer):
    class Meta :
        model = Order
        fields = ['id','panier','product','color','size','state','price_to_pay']

class PanierSerializer(serializers.ModelSerializer):
    class Meta :
        model = Panier
        fields = ['id','owner','address','tel','created_at']

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
        fields = ['id','code','percentage','type','products','subCategories','users','date_limit']

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
            if  user in instance.users.all():
                error = {'message':  'code can be user only once'}
                raise serializers.ValidationError(error) 
            instance.users.add(user)
        return instance

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id','owner']    

    