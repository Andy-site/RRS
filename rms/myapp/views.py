from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def index(request):
    return render(request, "myapp/index.html", {})


def index2(request):
    return render(request, "myapp/index2.html", {})


def basic(request):
    return render(request, "myapp/basic.html", {})


def customer_signup(request):
    return render(request, "myapp/customer_signup.html", {})


def customer_login(request):
    return render(request, "myapp/customer_login.html", {})


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
