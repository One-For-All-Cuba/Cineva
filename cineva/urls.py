"""cineva URL Configuration"""
from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import path


def home(request):
    return render(request, 'home.html')


def health(request):
    return JsonResponse({'ok': True, 'service': 'cineva'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('health/', health),
]
