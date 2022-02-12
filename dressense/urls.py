from django.urls import path,include
from . views import *


urlpatterns = [
    path('', Index.as_view(),name='home'),
    path('cart/', Cart.as_view(),name='cart'),
    path('stores', stores,name='stores'),
    path('wishlist/', wishlist,name='wishlist'),
    path('profile', profile,name='profile'),
    path('logout', logout,name='logout'),
    path('accounts/', Accounts.as_view(),name='accounts'),
    path("<int:myid>", productview, name="productview"),
    path('signup/',Signup.as_view(),name="signup")
]
