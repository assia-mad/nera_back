from calendar import week
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework import viewsets , generics
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
from django.db.models import Count , Sum, Avg
from datetime import timedelta
from django.utils import timezone
from hitcount.views import HitCountMixin
from itertools import chain
from django.core.cache import cache

# manage users by Admin
class ManageUsersView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ManageusersSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    parser_classes = [FormParser, JSONParser, MultiPartParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['first_name','last_name','email','address','tel','role','is_superuser', 'is_active','language']
    filterset_fields = ['first_name','last_name','email','address','tel','role','is_superuser', 'is_active','language']
    search_fields = ['first_name','last_name','email','address','tel','role','is_superuser', 'is_active','language']
    ordering_fields = ['first_name','last_name','email','address','tel','role','is_superuser', 'is_active','language']

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

class CategorieView(viewsets.ModelViewSet, HitCountMixin):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name','types__id','created_at']
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
    pagination_class = CustomPagination
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
    filter_fields = ['owner','code','name','regular_price','disc_price','disc_per','gender','type','categorie','sub_categorie','available_colors','available_sizes','tags']
    filterset_fields = ['owner','code','name','regular_price','disc_price','disc_per','gender','type','categorie','sub_categorie','available_colors','available_sizes','tags']
    search_fields = ['owner__id','code','name','regular_price','disc_price','disc_per','gender','type__id','categorie__id','sub_categorie__id','available_colors__id','available_sizes__id','tags__id']
    ordering_fields = ['owner','code','name','regular_price','disc_price','disc_per','gender','type','categorie','sub_categorie','available_colors','available_sizes','tags']
    
class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = None
    # permission_classes = [IsAuthenticated , AdminOrownerPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','panier','product','color','size','state','wishlist','qte','code_promo','created_at']
    filterset_fields = ['owner','panier','product','color','size','state','wishlist','qte','code_promo','created_at']
    search_fields = ['owner__id','panier__id','product__id','color','size','state','wishlist__id','qte','code_promo','created_at']
    ordering_fields = ['owner','panier','product','color','size','state','wishlist','qte','code_promo','created_at']
    def get_queryset(self):
        if self.request.query_params.get('filter_null', "false") == "true":
            return Order.objects.filter( panier__isnull = True , wishlist__isnull = True)
        return Order.objects.all()

class FuturPersonnelOrders(viewsets.ModelViewSet):#for every user
    serializer_class = OrderSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','panier','product','color','size','state','wishlist','qte','created_at']
    filterset_fields = ['owner','panier','product','color','size','state','wishlist','qte','created_at']
    search_fields = ['owner__id','panier__id','product__id','color','size','state','wishlist__id','qte','created_at']
    ordering_fields = ['owner','panier','product','color','size','state','wishlist','qte','created_at']
    def get_queryset(self):
            return Order.objects.filter( panier__isnull = True , wishlist__isnull = True)

class PanierView(viewsets.ModelViewSet):
    queryset = Panier.objects.all()
    serializer_class = PanierSerializer
    pagination_class = CustomPagination
    # permission_classes = [IsAuthenticated , AdminOrownerPermission]
    filter_fields = ['owner','wilaya','commune','tel','detailed_place','postal_code','desk_delivery','commune_delivery','state','created_at','advanced_payment']
    filterset_fields = ['owner','wilaya','commune','tel','detailed_place','postal_code','desk_delivery','commune_delivery','state','created_at','advanced_payment']
    search_fields = ['owner','wilaya__id','commune__id','tel','detailed_place','postal_code','desk_delivery__id','commune_delivery__id','state','created_at','advanced_payment']
    ordering_fields = ['owner','wilaya','commune','tel','detailed_place','postal_code','desk_delivery','commune_delivery','state','created_at','advanced_payment']

class FavoriteListView(viewsets.ModelViewSet):
    queryset = FavoriteList.objects.all()
    serializer_class = FavoritListSerializer
    pagination_class = CustomPagination
    # permission_classes = [IsAuthenticatedAndOwner]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','products']
    filterset_fields = ['owner','products']
    search_fields = ['owner__id','products']
    ordering_fields = ['owner','products']

class DiscountView(viewsets.ModelViewSet):
    current = datetime.now()
    queryset = Discount.objects.filter(date_limit__gte = current, date_debut__lte = current)
    serializer_class = DiscountSerializer
    pagination_class = CustomPagination
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['percentage','products','subCategories','categories','date_debut','date_limit']
    filterset_fields = ['percentage','products','subCategories','categories','date_debut','date_limit']
    search_fields = ['percentage','products__id','subCategories__id','categories__id','date_debut','date_limit']
    ordering_fields = ['percentage','products','subCategories','categories','date_debut','date_limit']

class CodePromoView(viewsets.ModelViewSet):
    current = datetime.now()
    queryset = CodePromo.objects.filter(date_limit__gte = current, date_debut__lte = current)
    serializer_class = CodePromoSerializer
    pagination_class = CustomPagination
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['code','percentage','type','products','subCategories','categories','users','date_limit']
    filterset_fields = ['code','percentage','type','products','subCategories','categories','users','date_limit']
    search_fields = ['code','percentage','type','products__id','subCategories__id','categories__id','users__id','date_limit']
    ordering_fields = ['code','percentage','type','products','subCategories','categories','users','date_limit']

class WishlistView(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner']
    filterset_fields = ['owner']
    search_fields = ['owner__id']
    ordering_fields = ['owner']

class FollowedWishlistView(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner']
    filterset_fields = ['owner']
    search_fields = ['owner__id']
    ordering_fields = ['owner']
    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(users__exact = user)

class FollowerWishlistView(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner']
    filterset_fields = ['owner']
    search_fields = ['owner__id']
    ordering_fields = ['owner']
    def get_queryset(self):
        user = self.request.user
        mywishlist = Wishlist.objects.get(owner=user)
        return Wishlist.objects.filter(owner__in = mywishlist.users.all())

class OtherWishlistView(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner']
    filterset_fields = ['owner']
    search_fields = ['owner__id']
    ordering_fields = ['owner']
    def get_queryset(self):
        user = self.request.user
        mywishlist = Wishlist.objects.get(owner=user)
        return Wishlist.objects.exclude(users__exact = user)

class PaymentConfirmView(viewsets.ModelViewSet):
    queryset = PaymentConfirm.objects.all()
    serializer_class = PaymentConfirmSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['transaction_code','panier','accept_payment']
    filterset_fields = ['transaction_code','panier','accept_payment']
    search_fields = ['transaction_code','panier__id','accept_payment']
    ordering_fields = ['transaction_code','panier','accept_payment']

class WilayaView(viewsets.ModelViewSet):
    queryset = Wilaya.objects.all()
    serializer_class = WilayaSerializer
    pagination_class = None
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name']
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']

class CommuneView(viewsets.ModelViewSet):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    pagination_class = None
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name','wilaya']
    filterset_fields = ['name','wilaya']
    search_fields = ['name','wilaya__id']
    ordering_fields = ['name','wilaya']

class CommuneCompanyView(viewsets.ModelViewSet):
    queryset = CommuneCompany.objects.all()
    serializer_class = CommuneCompanySerializer
    pagination_class = CustomPagination
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['commune','company','delivery_price','commune__wilaya']
    filterset_fields = ['commune','company','delivery_price','commune__wilaya']
    search_fields = ['commune__id','company__id','delivery_price','commune__wilaya__id']
    ordering_fields = ['commune','company','delivery_price','commune__wilaya']

class StopDeskView(viewsets.ModelViewSet):
    queryset = StopDesk.objects.all()
    serializer_class = StopDeskSerializer
    pagination_class = CustomPagination
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name','company','wilaya','delivery_price']
    filterset_fields = ['name','company','wilaya','delivery_price']
    search_fields = ['name','company__id','wilaya__id','delivery_price']
    ordering_fields = ['name','company','wilaya','delivery_price']

class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = None
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
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['sender','wishlist','is_accepted']
    filterset_fields = ['sender','wishlist','is_accepted']
    search_fields = ['sender__id','wishlist__id','is_accepted']
    ordering_fields = ['sender','wishlist','is_accepted']

class EasterEggView(viewsets.ModelViewSet):
    queryset = EasterEgg.objects.all()
    serializer_class = EasterEggSerializer
     # permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
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
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['product','rarity']
    filterset_fields = ['product','rarity']
    search_fields = ['product__id','rarity']
    ordering_fields = ['product','rarity']

class FutureOrdersStat(APIView): 
    def get(self , request , format = None):
        products = dict()
        some_day_last_month = timezone.now().date() - timedelta(days=30)
        products = Order.objects.filter(panier__isnull = True , wishlist__isnull = True, created_at__gt = some_day_last_month ).values('product').annotate(total = Sum('qte')).order_by('-total')
        data = {
            'products': products
        }

        return Response(data)

class SizeOrdersStat(APIView): 
    def get(self , request , format = None):
        sizes_last_week = dict()
        sizes_last_month = dict()
        sizes_last_6_month = dict()
        sizes_last_year = dict()
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        some_day_last_month = timezone.now().date() - timedelta(days=30)
        some_day_last_6_month = timezone.now().date() - timedelta(days=180)
        some_day_last_year = timezone.now().date() - timedelta(days=365)
        sizes_last_week = Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt =some_day_last_week).values('size').annotate(total = Sum('qte')).order_by('-total')
        sizes_last_month = Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt =some_day_last_month).values('size').annotate(total = Sum('qte')).order_by('-total')
        sizes_last_6_month = Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt =some_day_last_6_month).values('size').annotate(total = Sum('qte')).order_by('-total')
        sizes_last_year= Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt =some_day_last_year).values('size').annotate(total = Sum('qte')).order_by('-total')
        data = {
            'sizes_last_week': sizes_last_week,
            'sizes_last_month':sizes_last_month,
            'sizes_last_6_month':sizes_last_6_month,
            'sizes_last_year':sizes_last_year,
        }
        
        return Response(data)

class ColorOrdersStat(APIView): 
    def get(self , request , format = None):
        colors_last_week = dict()
        colors_last_month = dict()
        colors_last_6_month = dict()
        colors_last_year = dict()
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        some_day_last_month = timezone.now().date() - timedelta(days=30)
        some_day_last_6_month = timezone.now().date() - timedelta(days=180)
        some_day_last_year = timezone.now().date() - timedelta(days=365)
        colors_last_week = Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt = some_day_last_week).values('color').annotate(total = Sum('qte')).order_by('-total')
        colors_last_month = Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt =some_day_last_month).values('color').annotate(total = Sum('qte')).order_by('-total')
        colors_last_6_month = Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt =some_day_last_6_month).values('color').annotate(total = Sum('qte')).order_by('-total')
        colors_last_year= Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt =some_day_last_year).values('color').annotate(total = Sum('qte')).order_by('-total')
        data = {
            'colors_last_week': colors_last_week,
            'colors_last_month':colors_last_month,
            'colors_last_6_month':colors_last_6_month,
            'colors_last_year':colors_last_year,
        }
        
        return Response(data)

class GenderStatisticsView(APIView):
    def get(self, request, format=None):
        ''' gender Statistics '''
        gender_last_week = dict()
        gender_last_month = dict()
        gender_last_6_month = dict()
        gender_last_year = dict()
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        some_day_last_month = timezone.now().date() - timedelta(days=30)
        some_day_last_6_month = timezone.now().date() - timedelta(days=180)
        some_day_last_year = timezone.now().date() - timedelta(days=365)
        gender_last_week = User.objects.filter(date_joined__gt = some_day_last_week).values('gender').annotate(percentage =( Count('id')* 100)/(User.objects.filter(date_joined__gt = some_day_last_week).count())).order_by('-percentage')
        gender_last_month = User.objects.filter(date_joined__gt = some_day_last_month).values('gender').annotate(percentage =( Count('id')* 100)/(User.objects.filter(date_joined__gt = some_day_last_month)).count()).order_by('-percentage')
        gender_last_6_month = User.objects.filter(date_joined__gt = some_day_last_6_month).values('gender').annotate(percentage =( Count('id')* 100)/(User.objects.filter(date_joined__gt = some_day_last_6_month)).count()).order_by('-percentage')
        gender_last_year = User.objects.filter(date_joined__gt = some_day_last_year).values('gender').annotate(percentage =( Count('id')* 100)/(User.objects.filter(date_joined__gt = some_day_last_year)).count()).order_by('-percentage')
        data = {
            'gender_last_week':gender_last_week,
            'gender_last_month':gender_last_month,
            'gender_last_6_month':gender_last_6_month,
            'gender_last_year':gender_last_year,
        }
        return Response(data)

class AgeStat(APIView): 
    def get(self , request , format = None):
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        some_day_last_month = timezone.now().date() - timedelta(days=30)
        some_day_last_6_month = timezone.now().date() - timedelta(days=180)
        some_day_last_year = timezone.now().date() - timedelta(days=365)
        ages_last_week_15_17 = User.objects.filter(date_joined__gt = some_day_last_week , age__gte = 15 , age__lte = 17).count()
        ages_last_week_18_23 = User.objects.filter(date_joined__gt = some_day_last_week , age__gt = 17 , age__lte = 23).count()
        ages_last_week_23_28 = User.objects.filter(date_joined__gt = some_day_last_week , age__gt = 23 , age__lte = 28).count()
        ages_last_week_28_35 = User.objects.filter(date_joined__gt = some_day_last_week , age__gt = 28, age__lte = 35).count()
        ages_last_week_35_40 = User.objects.filter(date_joined__gt = some_day_last_week , age__gt = 35 , age__lte = 40).count()
        ages_last_week_40 = User.objects.filter(date_joined__gt = some_day_last_week , age__gt = 40).count()
        ages_last_month_15_17 = User.objects.filter(date_joined__gt = some_day_last_month , age__gte = 15 , age__lte = 17).count()
        ages_last_month_18_23  = User.objects.filter(date_joined__gt = some_day_last_month , age__gt = 17 , age__lte = 23).count()
        ages_last_month_23_28 = User.objects.filter(date_joined__gt = some_day_last_month , age__gt = 23 , age__lte = 28).count()
        ages_last_month_28_35 = User.objects.filter(date_joined__gt = some_day_last_month , age__gt = 28, age__lte = 35).count()
        ages_last_month_35_40 = User.objects.filter(date_joined__gt = some_day_last_month , age__gt = 35 , age__lte = 40).count()
        ages_last_month_40= User.objects.filter(date_joined__gt = some_day_last_month , age__gt = 40).count()
        # ages_last_6_month = User.objects.filter(date_joined__gt = some_day_last_6_month,age__isnull = False).values('age').annotate(percentage =( Count('id')* 100)/(User.objects.filter(date_joined__gt = some_day_last_6_month)).count()).order_by('-percentage')
        ages_last_6_month_15_17 = User.objects.filter(date_joined__gt = some_day_last_6_month, age__gte = 15 , age__lte = 17).count()
        ages_last_6_month_18_23  = User.objects.filter(date_joined__gt = some_day_last_6_month, age__gt = 17 , age__lte = 23).count()
        ages_last_6_month_23_28 = User.objects.filter(date_joined__gt = some_day_last_6_month, age__gt = 23 , age__lte = 28).count()
        ages_last_6_month_28_35 = User.objects.filter(date_joined__gt = some_day_last_6_month, age__gt = 28, age__lte = 35).count()
        ages_last_6_month_35_40 = User.objects.filter(date_joined__gt = some_day_last_6_month, age__gt = 35 , age__lte = 40).count()
        ages_last_6_month_40= User.objects.filter(date_joined__gt = some_day_last_6_month, age__gt = 40).count()
        ages_last_year_15_17 = User.objects.filter(date_joined__gt = some_day_last_year, age__gte = 15 , age__lte = 17).count()
        ages_last_year_18_23  = User.objects.filter(date_joined__gt = some_day_last_year, age__gt = 17 , age__lte = 23).count()
        ages_last_year_23_28 = User.objects.filter(date_joined__gt = some_day_last_year, age__gt = 23 , age__lte = 28).count()
        ages_last_year_28_35 = User.objects.filter(date_joined__gt = some_day_last_year, age__gt = 28, age__lte = 35).count()
        ages_last_year_35_40 = User.objects.filter(date_joined__gt = some_day_last_year, age__gt = 35 , age__lte = 40).count()
        ages_last_year_40= User.objects.filter(date_joined__gt = some_day_last_year, age__gt = 40).count()
        data = {
            'ages_last_week':{
                "15_17":ages_last_week_15_17,
                "18_23":ages_last_week_18_23,
                "23_28":ages_last_week_23_28,
                "28_35":ages_last_week_28_35,
                "35_40":ages_last_week_35_40,
                "plus_40":ages_last_week_40,
                },
             'ages_last_month':{
                "15_17":ages_last_month_15_17,
                "18_23":ages_last_month_18_23,
                "23_28":ages_last_month_23_28,
                "28_35":ages_last_month_28_35,
                "35_40":ages_last_month_35_40,
                "plus_40":ages_last_month_40,
                },
            'ages_last_6_month':{
                "15_17":ages_last_6_month_15_17,
                "18_23":ages_last_6_month_18_23,
                "23_28":ages_last_6_month_23_28,
                "28_35":ages_last_6_month_28_35,
                "35_40":ages_last_6_month_35_40,
                "plus_40":ages_last_6_month_40,
                },
            'ages_last_year':{
                "15_17":ages_last_year_15_17,
                "18_23":ages_last_year_18_23,
                "23_28":ages_last_year_23_28,
                "28_35":ages_last_year_28_35,
                "35_40":ages_last_year_35_40,
                "plus_40":ages_last_year_40,
                },
        }
        
        return Response(data)

class WilayasOrderStat(APIView): 
    def get(self , request , format = None):
        wilayas_last_week = dict()
        wilayas_last_month = dict()
        wilayas_last_6_month = dict()
        wilayas_last_year = dict()
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        some_day_last_month = timezone.now().date() - timedelta(days=30)
        some_day_last_6_month = timezone.now().date() - timedelta(days=180)
        some_day_last_year = timezone.now().date() - timedelta(days=365)
        wilayas_last_week = Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt = some_day_last_week).values('panier__wilaya').annotate(total = Sum('qte')).order_by('-total')
        wilayas_last_month = Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt = some_day_last_month).values('panier__wilaya').annotate(total = Sum('qte')).order_by('-total')
        wilayas_last_6_month = Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt = some_day_last_6_month).values('panier__wilaya').annotate(total = Sum('qte')).order_by('-total')
        wilayas_last_year= Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt = some_day_last_year).values('panier__wilaya').annotate(total = Sum('qte')).order_by('-total')
        data = {
            'wilayas_last_week': wilayas_last_week,
            'wilayas_last_month':wilayas_last_month,
            'wilayas_last_6_month':wilayas_last_6_month,
            'wilayas_last_year':wilayas_last_year,
        }
        return Response(data)

class CompaniesDeskStatisticsView(APIView):
    def get(self, request, format=None):
        ''' companies stats'''
        last_week = dict()
        last_month = dict()
        last_6_month = dict()
        last_year = dict()
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        some_day_last_month = timezone.now().date() - timedelta(days=30)
        some_day_last_6_month = timezone.now().date() - timedelta(days=180)
        some_day_last_year = timezone.now().date() - timedelta(days=365)
        last_week = Panier.objects.filter(created_at__gt = some_day_last_week,desk_delivery__isnull = False).values('desk_delivery__company__name').annotate(percentage =(Count('id')*100)/Panier.objects.filter(created_at__gt = some_day_last_week,desk_delivery__isnull = False).count()).annotate(total = Count('id')).order_by('-percentage')
        last_month = Panier.objects.filter(created_at__gt = some_day_last_month,desk_delivery__isnull = False).values('desk_delivery__company__name').annotate(percentage =(Count('id')*100)/Panier.objects.filter(created_at__gt = some_day_last_month,desk_delivery__isnull = False).count()).annotate(total = Count('id')).order_by('-percentage')
        last_6_month = Panier.objects.filter(created_at__gt = some_day_last_6_month,desk_delivery__isnull = False).values('desk_delivery__company__name').annotate(percentage =(Count('id')*100)/Panier.objects.filter(created_at__gt = some_day_last_6_month,desk_delivery__isnull = False).count()).annotate(total = Count('id')).order_by('-percentage')
        last_year = Panier.objects.filter(created_at__gt = some_day_last_year,desk_delivery__isnull = False).values('desk_delivery__company__name').annotate(percentage =(Count('id')*100)/Panier.objects.filter(created_at__gt = some_day_last_year,desk_delivery__isnull = False).count()).annotate(total = Count('id')).order_by('-percentage')
        data = {
            'last_week_stats':last_week ,
            'last_month_stats':last_month,
            'last_6_month_stats':last_6_month,
            'last_year_stats':last_year,
        }
        return Response(data)

class CompanieshomeStatisticsView(APIView):
    def get(self, request, format=None):
        ''' companies stats'''
        last_week = dict()
        last_month = dict()
        last_6_month = dict()
        last_year = dict()
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        some_day_last_month = timezone.now().date() - timedelta(days=30)
        some_day_last_6_month = timezone.now().date() - timedelta(days=180)
        some_day_last_year = timezone.now().date() - timedelta(days=365)
        last_week = Panier.objects.filter(created_at__gt = some_day_last_week,commune_delivery__isnull = False).values('commune_delivery__company__name').annotate(percentage =(Count('id')*100)/Panier.objects.filter(created_at__gt = some_day_last_week,commune_delivery__isnull = False).count()).annotate(total = Count('id')).order_by('-percentage')
        last_month = Panier.objects.filter(created_at__gt = some_day_last_month,commune_delivery__isnull = False).values('commune_delivery__company__name').annotate(percentage =(Count('id')*100)/Panier.objects.filter(created_at__gt = some_day_last_month,commune_delivery__isnull = False).count()).annotate(total = Count('id')).order_by('-percentage')
        last_6_month = Panier.objects.filter(created_at__gt = some_day_last_6_month,commune_delivery__isnull = False).values('commune_delivery__company__name').annotate(percentage =(Count('id')*100)/Panier.objects.filter(created_at__gt = some_day_last_6_month,commune_delivery__isnull = False).count()).annotate(total = Count('id')).order_by('-percentage')
        last_year = Panier.objects.filter(created_at__gt = some_day_last_year,commune_delivery__isnull = False).values('commune_delivery__company__name').annotate(percentage =(Count('id')*100)/Panier.objects.filter(created_at__gt = some_day_last_year,commune_delivery__isnull = False).count()).annotate(total = Count('id')).order_by('-percentage')
        data = {
            'last_week_stats':last_week ,
            'last_month_stats':last_month,
            'last_6_month_stats':last_6_month,
            'last_year_stats':last_year,
        }
        return Response(data)

class ProductPurchastedView(APIView):
    def get(self, request, format=None):
        ''' products stats'''
        products_last_week = dict()
        products_last_month = dict()
        products_last_6_month = dict()
        products_last_year = dict()
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        some_day_last_month = timezone.now().date() - timedelta(days=30)
        some_day_last_6_month = timezone.now().date() - timedelta(days=180)
        some_day_last_year = timezone.now().date() - timedelta(days=365)
        products_last_week = Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt = some_day_last_week).values('product').annotate(total = Sum('qte')).order_by('-total')
        products_last_month = Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt = some_day_last_month).values('product').annotate(total = Sum('qte')).order_by('-total')
        products_last_6_month = Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt = some_day_last_6_month).values('product').annotate(total = Sum('qte')).order_by('-total')
        products_last_year = Order.objects.filter(panier__isnull = False , wishlist__isnull = True, created_at__gt = some_day_last_year).values('product').annotate(total = Sum('qte')).order_by('-total')        
        data = {
            'last_week_stats':products_last_week ,
            'last_month_stats':products_last_month,
            'last_6_month_stats':products_last_6_month,
            'last_year_stats':products_last_year,
        }
        return Response(data)

class VisitorView(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorsSerializer

class VisitorStatsView(APIView):
    def get(self, request, format=None):
        ''' visitors stats'''
        this_year = datetime.now().year
        visitor_1 = Visitor.objects.filter(last_visit__month = 1 , last_visit__year = this_year).count()
        visitor_2 = Visitor.objects.filter(last_visit__month = 2 , last_visit__year = this_year).count()
        visitor_3 = Visitor.objects.filter(last_visit__month = 3 , last_visit__year = this_year).count()
        visitor_4 = Visitor.objects.filter(last_visit__month = 4 , last_visit__year = this_year).count()
        visitor_5 = Visitor.objects.filter(last_visit__month = 5 , last_visit__year = this_year).count()
        visitor_6 = Visitor.objects.filter(last_visit__month = 6 , last_visit__year = this_year).count()
        visitor_7 = Visitor.objects.filter(last_visit__month = 7 , last_visit__year = this_year).count()
        visitor_8 = Visitor.objects.filter(last_visit__month = 8 , last_visit__year = this_year).count()
        visitor_9 = Visitor.objects.filter(last_visit__month = 9 , last_visit__year = this_year).count()
        visitor_10 = Visitor.objects.filter(last_visit__month = 10 , last_visit__year = this_year).count()
        visitor_11 = Visitor.objects.filter(last_visit__month = 11 , last_visit__year = this_year).count()
        visitor_12 = Visitor.objects.filter(last_visit__month = 12 , last_visit__year = this_year).count()       
        data = {
            'janvier':visitor_1 ,
            'février':visitor_2 ,
            'mars':visitor_3 ,
            'avril':visitor_4 ,
            'mai':visitor_5 ,
            'juin': visitor_6 ,
            'juillet':visitor_7 ,
            'aout':visitor_8 ,
            'septembre':visitor_9 ,
            'octobre':visitor_10 ,
            'novembre':visitor_11 ,
            'décembre':visitor_12,
        }
        return Response(data)

class CodePromoStats(APIView):
    def get(self, request, format=None):
        ''' codepromo stats per month '''
        codes_last_week = dict()
        codes_third_week = dict()
        codes_second_week = dict()
        codes_first_week = dict()
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        some_day_third_week = timezone.now().date() - timedelta(days=14)
        some_day_second_week = timezone.now().date() - timedelta(days=21)
        some_day_first_week = timezone.now().date() - timedelta(days=28)
        codes_last_week = Order.objects.filter(panier__isnull = False , wishlist__isnull = True,code_promo__isnull = False,code_promo__influencer__isnull =True, created_at__gte = some_day_last_week).values('code_promo').annotate(total = Sum('qte')).order_by('-total')
        codes_third_week = Order.objects.filter(panier__isnull = False , wishlist__isnull = True,code_promo__isnull = False,code_promo__influencer__isnull =True, created_at__lt = some_day_last_week,created_at__gte = some_day_third_week).values('code_promo').annotate(total = Sum('qte')).order_by('-total')
        codes_second_week = Order.objects.filter(panier__isnull = False , wishlist__isnull = True,code_promo__isnull = False,code_promo__influencer__isnull =True,created_at__lt = some_day_third_week ,created_at__gte = some_day_second_week).values('code_promo').annotate(total = Sum('qte')).order_by('-total')
        codes_first_week = Order.objects.filter(panier__isnull = False , wishlist__isnull = True,code_promo__isnull = False,code_promo__influencer__isnull =True, created_at__lt = some_day_second_week, created_at__gte = some_day_first_week).values('code_promo').annotate(total = Sum('qte')).order_by('-total')        
        data = {
            'last_week_stats':codes_last_week ,
            'third_week_stats':codes_third_week,
            'second_week_stats':codes_second_week,
            'first_week_stats':codes_first_week,
        }
        return Response(data)

class CodeInfluencerStats(APIView):
    def get(self, request, format=None):
        ''' codeinfluencer stats per month '''
        codes_last_week = dict()
        codes_third_week = dict()
        codes_second_week = dict()
        codes_first_week = dict()
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        some_day_third_week = timezone.now().date() - timedelta(days=14)
        some_day_second_week = timezone.now().date() - timedelta(days=21)
        some_day_first_week = timezone.now().date() - timedelta(days=28)
        codes_last_week = Order.objects.filter(panier__isnull = False , wishlist__isnull = True,code_promo__isnull = False,code_promo__influencer__isnull =False, created_at__gte = some_day_last_week).values('code_promo').annotate(total = Sum('qte')).order_by('-total')
        codes_third_week = Order.objects.filter(panier__isnull = False , wishlist__isnull = True,code_promo__isnull = False,code_promo__influencer__isnull =False, created_at__lt = some_day_last_week,created_at__gte = some_day_third_week).values('code_promo').annotate(total = Sum('qte')).order_by('-total')
        codes_second_week = Order.objects.filter(panier__isnull = False , wishlist__isnull = True,code_promo__isnull = False,code_promo__influencer__isnull =False,created_at__lt = some_day_third_week ,created_at__gte = some_day_second_week).values('code_promo').annotate(total = Sum('qte')).order_by('-total')
        codes_first_week = Order.objects.filter(panier__isnull = False , wishlist__isnull = True,code_promo__isnull = False,code_promo__influencer__isnull =False, created_at__lt = some_day_second_week, created_at__gte = some_day_first_week).values('code_promo').annotate(total = Sum('qte')).order_by('-total')        
        data = {
            'last_week_stats':codes_last_week ,
            'third_week_stats':codes_third_week,
            'second_week_stats':codes_second_week,
            'first_week_stats':codes_first_week,
        }
        return Response(data)

class SuggestedProductsView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    def get_queryset(self):
        user = self.request.user
        print("the user is ", user.pk)
        print('in the cache', cache.get(user.pk))
        orders_list = Order.objects.order_by('created_at').filter(owner = user).all()[:20]
        favorites = FavoriteList.objects.get(owner = user).products.all()
        visited_sub_categories = cache.get(user.pk)
        print("the visited",visited_sub_categories)
        print("the keys",cache.has_key(user.pk))
        print("the fav",favorites)
        print("orders",orders_list)
        if all(v is None for v in [orders_list, favorites, visited_sub_categories]):
            return Product.objects.all().order_by('?')
        else :
            suggestes_sub_categories = [] #suggest based on them
            purchasted_products = [] #to eleminate them from suggestions
            suggested_tags = [] # suggest products by tags too
            if visited_sub_categories is not None :
                    suggestes_sub_categories.extend(visited_sub_categories)
            if orders_list is not None :
                for order in orders_list:
                    purchasted_products.append(order.product.pk)
                    sub_categorie = order.product.sub_categorie
                    tags = order.product.tags.all()
                    if not ( sub_categorie in suggestes_sub_categories) :
                        suggestes_sub_categories.append(order.product.sub_categorie)
                    for tag in tags :
                        if not ( tag  in suggested_tags) and len(suggested_tags)<20 :
                            suggested_tags.append(tag)
            if favorites is not None :
                for product in favorites.all() :
                    purchasted_products.append(product.pk)
                    if not (product.sub_categorie in suggestes_sub_categories):
                        suggestes_sub_categories.append(product.sub_categorie)
                    for tag in product.tags.all():
                        if not ( tag  in suggested_tags) and len(suggested_tags)<20 :
                            suggested_tags.append(tag)
            print("the suggested sub categories",suggestes_sub_categories)
            print("the suggested tags",suggested_tags)
            suggested_products1 = Product.objects.filter(sub_categorie__in = suggestes_sub_categories,tags__in = suggested_tags).exclude(pk__in = purchasted_products).order_by('?')[:20]
            random_products = Product.objects.exclude(pk__in = suggested_products1).order_by('?')[:10]
        return (suggested_products1 | random_products).distinct()
    def get_object(self):
        product = super().get_object()
        user = self.request.user
        cached_data = cache.get(user.pk)
        if cached_data is None:
            cached_data = [product.sub_categorie]
        else :
            if not (product.sub_categorie in cached_data):
                cached_data.append(product.sub_categorie)
        cache.set(user.pk , cached_data , 3600*60)
        print("we caached",cache.get(user.pk))
        print("the keys",cache.has_key(user.pk))
        return product

class SimillarProducts(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        pk = self.kwargs['pk']
        product = Product.objects.get(pk=pk)
        simillar_products1 = Product.objects.filter(sub_categorie = product.sub_categorie).exclude(pk = product.pk).order_by('?')
        simillar_products2 = Product.objects.filter(tags__in = product.tags.all()).exclude(pk = product.pk).order_by('?')
        return list(chain(simillar_products1 , simillar_products2))[:9]

class SignalView(viewsets.ModelViewSet):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['id','user','description','image']
    filterset_fields = ['id','user','description','image']
    search_fields = ['id','user__id','description','image']
    ordering_fields =['id','user','description','image']
    