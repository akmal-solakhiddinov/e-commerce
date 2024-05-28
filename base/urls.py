from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
                  path('login/', views.loginPage, name='login'),
                  path('logout/', views.logoutUser, name='logout'),
                  path('register/', views.registerPage, name='register'),

                  path('', views.home_page, name='home'),
                  path('profile-page', views.profile, name='profile-page'),
                  path('products-page/', views.productsPage, name='products-page'),
                  path('cart-page/', views.cartPage, name='cart-page'),
                  path('search/', views.searchPage, name='search-page'),
                  path('chekout-page/', views.checkoutPage, name='checkout-page'),

                  path('add-to-cart/<str:pk>', views.addToCart, name='add-to-cart'),
                  path('delete-from-cart/', views.deleteFromCart, name='delete-from-cart'),
                  path('update-quantity/<str:pk>', views.updateQuantity, name='update-quantity'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
