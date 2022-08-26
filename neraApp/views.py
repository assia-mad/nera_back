from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework import viewsets 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.parsers import JSONParser , FormParser , MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters import CharFilter
from .models import *
from .serializers import *
from .permissions import *
from .pagination import *
from datetime import datetime
from django.db.models import Count , Sum

# manage users by Admin
class ManageUsersView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ManageusersSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
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
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name','created_at']
    ordering_fields = ['name','created_at']

class CategorieView(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name','types','created_at']
    ordering_fields = ['name','types','created_at']

class SubCategorieView(viewsets.ModelViewSet):
    queryset = SubCategorie.objects.all()
    serializer_class = SubCategorieSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name','categories','created_at']
    ordering_fields = ['name','categories','created_at']

class ColorView(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['code','created_at']
    ordering_fields = ['code','created_at']

class SizeView(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class =SizeSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['code','created_at']
    ordering_fields = ['code','created_at']
    
class ProductImageView(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ImageSerializer
    # permission_classes = [IsAuthenticated , AdminOrownerPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = None
    filter_fields = ['product']
    filterset_fields = ['product']
    search_fields = ['product__id']
    ordering_fields = ['product']
    
class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','code','name','regular_price','disc_price','disc_per','gender','type','sub_categorie','available_colors','available_sizes','tags']
    filterset_fields = ['owner','code','name','regular_price','disc_price','disc_per','gender','type','sub_categorie','available_colors','available_sizes','tags']
    search_fields = ['owner__id','code','name','regular_price','disc_price','disc_per','gender','type__id','sub_categorie__id','available_colors__id','available_sizes__id','tags__id']
    ordering_fields = ['owner','code','name','regular_price','disc_price','disc_per','gender','type','sub_categorie','available_colors','available_sizes','tags']
    
class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    # permission_classes = [IsAuthenticated , AdminOrownerPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','panier','product','color','size','state','wishlist','qte','created_at']
    filterset_fields = ['owner','panier','product','color','size','state','wishlist','qte','created_at']
    search_fields = ['owner__id','panier__id','product__id','color','size','state','wishlist__id','qte','created_at']
    ordering_fields = ['owner','panier','product','color','size','state','wishlist','qte','created_at']

class FuturPersonnelOrders(viewsets.ModelViewSet):#for every user
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','panier','product','color','size','state','wishlist','qte','created_at']
    filterset_fields = ['owner','panier','product','color','size','state','wishlist','qte','created_at']
    search_fields = ['owner__id','panier__id','product__id','color','size','state','wishlist__id','qte','created_at']
    ordering_fields = ['owner','panier','product','color','size','state','wishlist','qte','created_at']
    def get_queryset(self):
            return Order.objects.filter(owner = self.request.user , panier__isnull = True , wishlist__isnull = True)


class PanierView(viewsets.ModelViewSet):
    queryset = Panier.objects.all()
    serializer_class = PanierSerializer
    # permission_classes = [IsAuthenticated , AdminOrownerPermission]
    filter_fields = ['owner','detailed_place','wilaya','commune','postal_code','payment_delivry','tel']
    filterset_fields = ['owner','detailed_place','wilaya','commune','postal_code','payment_delivry','tel']
    search_fields = ['owner__id','detailed_place','wilaya','commune','postal_code','payment_delivry__id','tel']
    ordering_fields = ['owner','detailed_place','wilaya','commune','postal_code','payment_delivry','tel']

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
    pagination_class = CustomPagination
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['code','percentage','type','products','subCategories','users','date_limit']
    filterset_fields = ['code','percentage','type','products','subCategories','users','date_limit']
    search_fields = ['code','percentage','type','products__id','subCategories__id','users__id','date_limit']
    ordering_fields = ['code','percentage','type','products','subCategories','users','date_limit']

class WishlistView(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner']
    filterset_fields = ['owner']
    search_fields = ['owner__id']
    ordering_fields = ['owner']

class PaymentConfirmView(viewsets.ModelViewSet):
    queryset = PaymentConfirm.objects.all()
    serializer_class = PaymentConfirmSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['transaction_code','panier']
    filterset_fields = ['transaction_code','panier']
    search_fields = ['transaction_code','panier__id']
    ordering_fields = ['transaction_code','panier']

class WilayaView(viewsets.ModelViewSet):
    queryset = Wilaya.objects.all()
    serializer_class = WilayaSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name','delivery_price']
    filterset_fields = ['name','delivery_price']
    search_fields = ['name','delivery_price']
    ordering_fields = ['name','delivery_price']

class CommuneView(viewsets.ModelViewSet):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name','wilaya','delivery_price']
    filterset_fields = ['name','wilaya','delivery_price']
    search_fields = ['name','wilaya__id','delivery_price']
    ordering_fields = ['name','wilaya','delivery_price']

class DeliveryView(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['company','payment_method']
    filterset_fields = ['company','payment_method']
    search_fields = ['company__id','payment_method']
    ordering_fields = ['company','payment_method']

class PaymentConfirmView(viewsets.ModelViewSet):
    queryset = PaymentConfirm.objects.all()
    serializer_class = PaymentConfirmSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['transaction_code','panier']
    filterset_fields = ['transaction_code','panier']
    search_fields = ['transaction_code','panier__id']
    ordering_fields = ['transaction_code','panier']

class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name']
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']

class RequestView(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
     # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['sender','wishlist','is_accepted']
    filterset_fields = ['sender','wishlist','is_accepted']
    search_fields = ['sender__id','wishlist__id','is_accepted']
    ordering_fields = ['sender','wishlist','is_accepted']

class EasterEggView(viewsets.ModelViewSet):
    queryset = EasterEgg.objects.all()
    serializer_class = EasterEggSerializer
     # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['winner','gift']
    filterset_fields = ['winner','gift']
    search_fields = ['winner__id','gift__id']
    ordering_fields = ['winner','gift']

class SettingsView(viewsets.ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = Settingserializer
     # permission_classes = [IsAuthenticated]

class NewsView(viewsets.ModelViewSet):
    queryset = News.objects.all()
    pagination_class = None
    serializer_class = NewsSerializer
     # permission_classes = [IsAuthenticated]

class GiftView(viewsets.ModelViewSet):
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer
     # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['product','rarity']
    filterset_fields = ['product','rarity']
    search_fields = ['product__id','rarity']
    ordering_fields = ['product','rarity']

class FutureOrdersStat(APIView):
     
    def get(self , request , format = None):
        products = dict()
        products = Order.objects.filter(panier__isnull = True , wishlist__isnull = True).values('product').annotate(total = Sum('qte')).order_by('-total')
        data = {
            'products': products
        }
        return Response(data)
    
    

