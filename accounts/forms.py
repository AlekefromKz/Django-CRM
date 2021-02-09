from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        # fields = ('customer', 'product', 'status')


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
