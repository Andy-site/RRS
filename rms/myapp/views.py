from django.shortcuts import render


def index(request):
    return render(request, "myapp/index.html", {})


def index2(request):
    return render(request, "myapp/index2.html", {})


def customer_signup(request):
    return render(request, "myapp/customer_signup.html", {})


def customer_login(request):
    return render(request, "myapp/customer_login.html", {})


def admin_page(request):
    return render(request, "myapp/admin_page.html", {})








