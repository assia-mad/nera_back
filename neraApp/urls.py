from django.urls import path , include , re_path
from dj_rest_auth.registration.views import RegisterView , ConfirmEmailView , VerifyEmailView
from dj_rest_auth.views import UserDetailsView, LoginView, LogoutView , PasswordResetView , PasswordResetConfirmView , PasswordChangeView
from rest_framework import routers
from .views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from fcm_django.api.rest_framework import FCMDeviceViewSet

schema_view = get_schema_view(

   openapi.Info(

      title="nera shop API",
      default_version='v1',
      description="nera is an e-commerce application ",
      contact=openapi.Contact(email="neradzshop@gmail.com"),
      license=openapi.License(name="BSD License"),

   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
router = routers.DefaultRouter()
router.register('devices', FCMDeviceViewSet)
router.register('products', ProductView , basename='products')
router.register('types', ProductTypeView , basename='product_type')
router.register('categories', CategorieView , basename='categories')
router.register('sub_categories', SubCategorieView , basename='product_sub_categorie')
router.register('colors', ColorView , basename='product_colors')
router.register('sizes', SizeView, basename='product_sizes')
router.register('images', ProductImageView, basename='product_images')
router.register('orders', OrderView , basename='orders')
router.register('futur_orders',FuturPersonnelOrders, basename='futur_orders')
router.register('panier', PanierView, basename='panier')
router.register('favorites', FavoriteListView, basename='favorites')
router.register('manage_users',ManageUsersView , basename= 'manage_users')
router.register('code_promo',CodePromoView , basename='code_promo')
router.register('followed_wish',FollowedWishlistView , basename='followed_wishlists')
router.register('follower_wish', FollowerWishlistView , basename='follower_wishlists')
router.register('other_wish', OtherWishlistView , basename='other_wishlists')
router.register('wilayas',WilayaView , basename='wilayas')
router.register('communes',CommuneView , basename='communes')
router.register('delivery',DeliveryView , basename='delivery')
router.register('payment_confirm', PaymentConfirmView , basename='payment_confirm')
router.register('companies',CompanyView , basename='companies')
router.register('requests',RequestView , basename= 'requests')
router.register('easter_eggs', EasterEggView , basename = 'easter_eggs')
router.register('settings', SettingsView , basename = 'easter_eggs_settings')
router.register('news',NewsView , basename='news')
router.register('gifts',GiftView , basename='gifts')

urlpatterns = [
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',VerifyEmailView.as_view(), name='account_confirm_email'),
    path('password-reset/', PasswordResetView.as_view()),
    path('password-change/',PasswordChangeView.as_view()),
    path('user/', UserDetailsView.as_view()),
    path('google_auth/', GoolgeAuth.as_view(), 	 name='google_login'),
    path('facebook_auth/', FacebookLogin.as_view(), name='fb_login'),
    path('stats_futur_orders/',FutureOrdersStat.as_view() , name='futur_orders'),
    path('stats_purchasted_sizes/', SizeOrdersStat.as_view() , name='orders_sizes'),
    path('stats_purchasted_colors/', ColorOrdersStat.as_view() , name='orders_colors'),
    path('stats_gender/', GenderStatisticsView.as_view() , name='gender_stats'),
    path('stats_wilayas/', WilayasOrderStat.as_view() , name='wilayas_stats'),
    path('stats_companies/',CompaniesStatisticsView.as_view(), name = 'companies_stats'),
    path('stats_age/', AgeStat.as_view() , name='age_stats'),
    path('stats_purchasted_products/', ProductPurchastedView.as_view() , name='products_stats'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]
urlpatterns += router.urls
