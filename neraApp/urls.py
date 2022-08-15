from django.urls import path , include , re_path
from dj_rest_auth.registration.views import RegisterView , ConfirmEmailView , VerifyEmailView
from dj_rest_auth.views import UserDetailsView, LoginView, LogoutView , PasswordResetView , PasswordResetConfirmView , PasswordChangeView
from rest_framework import routers
from .views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

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
router.register('products', ProductView , basename='products')
router.register('types', ProductTypeView , basename='product_type')
router.register('categories', CategorieView , basename='categories')
router.register('sub_categories', SubCategorieView , basename='product_sub_categorie')
router.register('colors', ColorView , basename='product_colors')
router.register('sizes', SizeView, basename='product_sizes')
router.register('images', ProductImageView, basename='product_images')
router.register('orders', OrderView , basename='orders')
router.register('panier', PanierView, basename='panier')
router.register('favorites', FavoriteListView, basename='favorites')
router.register('manage_users',ManageUsersView , basename= 'manage_users')
router.register('code_promo',CodePromoView , basename='code_promo')
router.register('wishlists',WishlistView , basename='wishlists')
router.register('wilayas',WilayaView , basename='wilayas')
router.register('communes',CommuneView , basename='communes')
router.register('delivery',DeliveryView , basename='delivery')
router.register('payment_confirm', PaymentConfirmView , basename='payment_confirm')
router.register('companies',CompanyView , basename='companies')
router.register('requests',RequestView , basename= 'requests')
router.register('easter_eggs', EasterEggView , basename = 'easter_eggs')
router.register('settings', SettingsView , basename = 'easter_eggs_settings')
router.register('news',NewsView , basename='news')

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
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]
urlpatterns += router.urls
