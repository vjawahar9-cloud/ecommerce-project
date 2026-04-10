from django.urls import path
from.import views

urlpatterns = [
    path("",views.homepage,name="home",),
    path("signup/",views.signuppage,name="signup",),
    path("signupprocess/",views.signupprocess,name="signupprocess",),
    path("login/",views.loginpage,name="login",),
    path("login/adminprocess/",views.adminprocess,name="adminprocess",),
    path('products/', views.productpage,name='productpage',),
    path('product/<int:id>/', views.productdetail,name='productdetail',),
    path('add-to-cart/<int:id>/',views.add_to_cart,name='add_to_cart',),
    path('cart/',views.cart_page,name='cart',),
    path('addproduct/',views.add_product,name='addproduct',),
    path('place-order/', views.place_order, name='place_order',),
    path('payment/', views.payment_page, name='payment',),



    path('toggle-cart/<int:id>/', views.toggle_cart, name='toggle_cart'),


    
]