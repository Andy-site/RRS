from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def index(request):
    return render(request, "myapp/index.html", {})


def index2(request):
    return render(request, "myapp/index2.html", {})