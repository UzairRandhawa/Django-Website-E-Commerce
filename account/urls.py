
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboardpage, name='index' ),
    path('product/', views.prodcutpage, name='product' ),
    path('customer/<str:pk>/', views.customerpage, name='customer' ),
    path('create_order/<str:pk>/', views.ordercreate, name='create' ),
    path('update_order/<str:pk>/', views.orderUpdate, name='update' ),
    path('delete_order/<str:pk>/', views.orderDelete, name='delete' ),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logoutpage,name='logout'),
    path('register/',views.registerpage,name='register'),
    path('user/',views.userPage,name='user-page'),
    path('setting/',views.profilePage,name='profile'),
    
    
    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name = "account/password_reset.html"),
    name='reset_password'),
    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name = "account/password_reset_sent.html"),
    name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = "account/password_reset_form.html"),
    name='password_reset_confirm'),
    path('reset_password_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name = "account/password_reset_done.html"),name='password_reset_complete'),

]
