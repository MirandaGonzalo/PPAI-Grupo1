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


def landing_page(request):
    return render(request, 'index.html')
