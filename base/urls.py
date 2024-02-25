from django.contrib import admin
from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.store, name='store'),
    path('categories/new-arrivals', views.new, name='new'),

    path('profile/', views.profile, name= 'profile'),
    path('categories/<slug:catslug>/<slug:prodslug>/', views.product, name= 'product'),
    path('categories/<slug:catslug>/<slug:prodslug>/details/', views.details, name= 'details'),


    path('categories/', views.category, name= 'category'),
    path('categories/<slug:slug>/', views.cat, name= 'cat'),
    path('cart/', views.cart, name='cart'),
    path('cart/<int:id>/<slug:do>', views.update, name='update'),
    path('checkout/', views.checkout, name='checkout'),
    path('<int:id>/add_to_cart/<slug:go>/<slug:catslug>/', views.add_to_cart, name='add'),
    path('<int:tfid>/', views.payment, name = 'payment'),
    path('<int:ship_id>/transfer/', views.order, name='order'),
    path('checkout/create-shipping/', views.create_shipping, name = 'create-ship'),
    path('checkout/update-details/', views.change, name = 'change'),
    path('cart/empty', views.empty, name='empty'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.registration_request, name='register'),
    path('<slug:catslug>/test', views.test, name='test'),
    path('cat-frame/', views.catframe, name='catframe'),
    path('search/', views.search, name='search'),

    
]