"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
     #admin
        path('admin-panel/',views.admin_index, name='admin_index'),

        #add product
        path('add-product/',views.add_product,name="add-product"),
        path('product-data/',views.product_data,name="product-data"),

        #all product
        path('all-product/',views.all_product, name='all-product'),

        #view product 
        path('view-product/<int:pk>/',views.view_product,name="view-product"),

        #edit product
        path('edit-product/<int:pk>/',views.edit_product,name="edit-product"),

        #update-product
        path('update-product/',views.update_product,name="update-product"),

        #delete product 
        
        path('delete-product/<int:pk>/',views.delete_product,name="delete-product"),

        #all order
        path('all-order/',views.all_order,name="all-order"),

        #view order
        path('view_order/<int:pk/',views.view_order1,name="view_order"),

#-----customer-panel--------------------------------------------------------------------------------------------------------------------
        #customer
        path('',views.customer_index,name="customer_index"),

        #view product 
        path('view-product-cust/<int:pk>/',views.view_product_cust,name="view-product-cust"),

        #buynow
        path("buynow/<int:pk>/",views.buynow,name="buynow"),

        #Add to Cart
        path("Add-To-Cart/",views.addToCart,name="addToCart"),

        #order
        path("order",views.order_product,name="order"),

        #view-order
        path('view-order/',views.view_order,name = "view-order"),

        #status
        path('status/',views.status,name="status"),

#-------authtication------------------------------------------------- 
        path('logout/',views.logout,name="logout"),       
        path('login/',views.login,name="login"),
        path('login-data/',views.login_data,name="login-data"),
        path("register",views.register,name="register"),
        path("register-data",views.register_data,name="register-data"),


        #pdf 
        path('generateinvoice/<int:pk>/', views.GenerateInvoice.as_view(), name = 'generateinvoice'),

         

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
