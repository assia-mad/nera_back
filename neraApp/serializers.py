from unicodedata import decimal
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer , UserDetailsSerializer
from .models import *
import decimal


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

class CustomLoginSerializer(LoginSerializer): 
    username = None

class CustomUserDetailSerializer(UserDetailsSerializer):
    address = serializers.CharField(max_length=150 )
    tel = serializers.CharField(max_length=10 , validators=[num_only])
    image = serializers.ImageField(allow_null=True)
    role = serializers.ChoiceField(choices= role_choices)
    class Meta : 
        model = User
        fields = ['id','first_name','last_name','email','address','tel','image','role','is_superuser', 'is_active']

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta :
        model = ProductType
        fields = ['id','name']
        lookup_fields = 'id'

class CategorieSerializer(serializers.ModelSerializer):
    class Meta :
        model = Categorie
        fields = ['id','name']

class SubCategorieSerializer(serializers.ModelSerializer):
    class Meta :
        model = SubCategorie
        fields = ['id','name','categorie']

class ColorSerializer(serializers.ModelSerializer):
    class Meta :
        model = Color
        fields = ['id','code']

class SizeSerializer(serializers.ModelSerializer):
    class Meta :
        model = Size
        fields = ['id','code']

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
       fields = ['id','owner','code','name','regular_price','disc_price','disc_per','type','sub_categories','available_colors','available_sizes','images','uploaded_images']

    def create(self, validated_data):
        uploaded_data = validated_data.pop('uploaded_images')
        new_product = super().create(validated_data)
        print(new_product.name)
        regular_price = new_product.regular_price
        percentage = decimal.Decimal(new_product.disc_per / 100)
        new_product.disc_price = regular_price - (regular_price * percentage)
        for uploaded_item in uploaded_data:
            new_product_image = ProductImage.objects.create(product = new_product, images = uploaded_item)
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
        fields = ['id','owner','product','color','size','state']

class PanierSerializer(serializers.ModelSerializer):
    class Meta :
        model = Panier
        fields = ['id','owner','orders','address']