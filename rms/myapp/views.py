from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def index(request):
    return render(request, "myapp/index.html", {})


def index2_boot(request):
    return render(request, "myapp/index2_boot.html", {})


def cp(request):
    return render(request, "myapp/cust_copy.html", {})


def ap(request):
    return render(request, "myapp/admin_page.html", {})


def common(request):
    return render(request, "myapp/common.html", {})


def admin_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("ap")
        else:
            messages.error(request, "Invalid Credentials, Please Try Again!!")
            return redirect("index2_boot")
    return HttpResponse('admin_page')


def handle1(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect("common")
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect("common")

        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        messages.success(request, "Your account has been successfully created!")
        return redirect("common")
    else:
        return HttpResponse('404 - Not Found')


def handle2(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged in!")
            return redirect("common")
        else:
            messages.error(request, "Invalid Credentials, Please Try Again!!")
            return redirect("common")
    return HttpResponse('handle2')
