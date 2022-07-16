from cgitb import lookup
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer , UserDetailsSerializer
from .models import *
from allauth.account.adapter import DefaultAccountAdapter




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
    images = serializers.SerializerMethodField()

    def get_images(self, product):
       return ImageSerializer(product.product_images.all(), many=True).data 
    class Meta:
       model = Product
       fields = ['id','code','name','regular_price','disc_price','type','sub_categories','available_colors','available_sizes','images']