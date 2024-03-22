from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import  User


def index(request):
    return render(request, "myapp/index.html", {})


def index2(request):
    return render(request, "myapp/index2.html", {})


def basic(request):
    return render(request, "myapp/basic.html", {})


def cp(request):
    return render(request, "myapp/cust_page.html", {})


def admin_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'myapp/admin_page.html')
        else:
            return redirect("/basic")
    else:
        # If it's not a POST request, just render the admin login page
        return render(request, 'myapp/index2.html')


def handle1(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect("cp")
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect("cp")
        if pass1 != pass2:
            messages.error(request, "Password do not match")
            return redirect("cp")

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been successfully created!")
        return redirect("cp")
    else:
        return HttpResponse('404 - Not Found')