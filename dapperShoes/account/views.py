from django.shortcuts import render, redirect, get_object_or_404
from product_management.models import *
from .models import *
from django.urls import reverse
from django.http import HttpResponse

# Create your views here.
def account(request):
    return render(request,'user_side/page-account.html')