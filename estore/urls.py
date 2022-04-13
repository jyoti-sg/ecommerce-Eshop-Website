"""estore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from eshops import views
from django.contrib.auth.views import LoginView,LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homeview),
    path('search/',views.search_view,name='search'),
    path('product_detail/<int:pid>',views.view_product,name='detail'),
    path('customersignup/',views.customer_signup),
    path('customerlogin/',LoginView.as_view(template_name='ecom/customerlogin.html'),name='customerlogin'),
    path('afterlogin/',views.afterlogin_view,name='afterlogin'),
    path('customer-home/',views.customerhome_view,name='customer-home'),
    path('add-to-cart/<int:pk>/',views.add_to_cart_view,name='add-to-cart'),
    path('cart/',views.cart_view,name='cart'),
    path('remove-from-cart/<int:pk>',views.remove_from_cart_view,name='remove-from-cart'),
    path('customer-address/',views.customer_address_view,name='customer-address'),
    path('payment-success/', views.payment_success_view,name='payment-success'),
    path('logout/',LogoutView.as_view(template_name='ecom/logout.html'),name='logout'),
    path('my-order/', views.my_order_view,name='my-order'),
    path('my-profile/', views.my_profile_view,name='my-profile'),
    path('send-feedback', views.send_feedback_view,name='send-feedback'),
    path('contactus', views.contactus_view,name='contactus'),
    path('customer-home2/',views.customerhome_view,name='customer-home'),

]
