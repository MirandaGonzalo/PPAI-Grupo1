import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.core import serializers
from django.db import transaction
from django.urls import reverse
from django.utils.dateparse import parse_date
from .models import *
from datetime import date, datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login as auth_login
from django import forms
from django.contrib import messages

def landing_page(request):
    return render(request, 'index.html')

def loginForm(request):
    return render(request, 'login/loginForm.html')

def perfil(request):
    sedes = Sede.getSedes()
    return render(request, 'perfil.html', {'sedes':sedes})

def logOutUser(request):
    logout(request)
    return redirect(landing_page)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('perfil')
        else:
            messages.error(request,'Los datos ingresados no son correctos.')
            return redirect('loginForm')
    else:
        form = LoginForm()
    return render(request, 'login/loginForm.html', {'form': form})
    
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
