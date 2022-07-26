from django.shortcuts import render
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework import views ,viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.parsers import JSONParser , FormParser , MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .permissions import *
from .pagination import *
from datetime import datetime

# manage users by Admin
class ManageUsersView(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = ManageusersSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ManageUsersPagination
    parser_classes = [FormParser, JSONParser, MultiPartParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['first_name','last_name','email','address','tel','role','is_superuser', 'is_active']
    filterset_fields = ['first_name','last_name','email','address','tel','role','is_superuser', 'is_active']
    search_fields = ['first_name','last_name','email','address','tel','role','is_superuser', 'is_active']
    ordering_fields = ['first_name','last_name','email','address','tel','role','is_superuser', 'is_active']

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = UpdateUsersByAdminSerializer
        return serializer_class

class GoolgeAuth(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class ProductTypeView(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name','created_at']
    ordering_fields = ['name','created_at']

class CategorieView(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name','created_at']
    ordering_fields = ['name','created_at']

class SubCategorieView(viewsets.ModelViewSet):
    queryset = SubCategorie.objects.all()
    serializer_class = SubCategorieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name','categorie','created_at']
    ordering_fields = ['name','categorie','created_at']

class ColorView(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['code','created_at']
    ordering_fields = ['code','created_at']

class SizeView(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class =SizeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['code','created_at']
    ordering_fields = ['code','created_at']
    
class ProductImageView(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ImageSerializer
    
class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','code','name','regular_price','disc_price','disc_per','type','sub_categories','available_colors','available_sizes']
    filterset_fields = ['owner','code','name','regular_price','disc_price','disc_per','type','sub_categories','available_colors','available_sizes']
    search_fields = ['owner__id','code','name','regular_price','disc_price','disc_per','type','sub_categories','available_colors','available_sizes']
    ordering_fields = ['owner','code','name','regular_price','disc_price','disc_per','type','sub_categories','available_colors','available_sizes']
    
class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated , AdminOrownerPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['panier','product','color','size','state']
    filterset_fields = ['panier','product','color','size','state']
    search_fields = ['panier__id','product__id','color','size','state']
    ordering_fields = ['panier','product','color','size','state']

class PanierView(viewsets.ModelViewSet):
    queryset = Panier.objects.all()
    serializer_class = PanierSerializer
    # permission_classes = [IsAuthenticated , AdminOrownerPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','address','tel']
    filterset_fields = ['owner','address','tel']
    search_fields = ['owner__id','address','tel']
    ordering_fields = ['owner','address','tel']

class FavoriteListView(viewsets.ModelViewSet):
    queryset = FavoriteList.objects.all()
    serializer_class = FavoritListSerializer
    # permission_classes = [IsAuthenticatedAndOwner]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','products']
    filterset_fields = ['owner','products']
    search_fields = ['owner__id','products']
    ordering_fields = ['owner','products']

class CodePromoView(viewsets.ModelViewSet):
    current = datetime.now()
    queryset = CodePromo.objects.filter(date_limit__gte = current)
    serializer_class = CodePromoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['code','percentage','type','products','subCategories','users','date_limit']
    filterset_fields = ['code','percentage','type','products','subCategories','users','date_limit']
    search_fields = ['code','percentage','type','products__id','subCategories__id','users__id','date_limit']
    ordering_fields = ['code','percentage','type','products','subCategories','users','date_limit']
