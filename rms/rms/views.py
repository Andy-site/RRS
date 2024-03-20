from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def index(request):
    return render(request, "myapp/index.html", {})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the entered username and password match with the values stored in the users table
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Redirect to admin page upon successful login
                return redirect('admin_page')
            else:
                # Display an error message if the password is incorrect
                return render(request, 'myapp/index2.html', {'error_message': 'Invalid username or password'})
        except User.DoesNotExist:
            # Display an error message if the username does not exist
            return render(request, 'myapp/index2.html', {'error_message': 'Invalid username or password'})

    else:
        return render(request, 'myapp/index2.html')


def admin_page(request):
    return render(request, 'admin_page.html')