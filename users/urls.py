from django.urls import path, include

from accounts import views
# import django.contrib.auth.urls as auth_views


from .views import index, search, product_details, addtocart, cart, confirmOrder

urlpatterns = [
# path('login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
# path('logout/', auth_views.logout, name='logout'),
path('accounts/', include('django.contrib.auth.urls')),

path('', index, name='home'),
path('search', search, name = 'search'),
path('cart', cart, name="cart"),
path('product-details/<pk>/', product_details, name='product-details' ),

path('addtocart/<pk>', addtocart, name='addtocart'),
path('register/', views.register, name='register'),
# path('details/', views.details, name='userdetails')
path('confirmorder/', confirmOrder, name='confirmorder'),
]