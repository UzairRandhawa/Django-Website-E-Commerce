from django.db import models
from django.forms import ModelForm, fields
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Customer, Order

class CustomForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']