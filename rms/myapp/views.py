from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import MyUser123, Rev
import re
from .models import Table
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
import json


def get_tables(request):
    if request.method == 'GET':
        # Get date and size parameters from the request
        date_str = request.GET.get('date')
        size = int(request.GET.get('size', 0))

        # Validate the date format
        try:
            date = parse_date(date_str)
        except ValidationError:
            return JsonResponse({'error': 'Invalid date format. Date must be in YYYY-MM-DD format.'}, status=400)

        # Query the database for tables
        # tables = Table.objects.filter(date=date, size=size).values('number', 'reserved')
        tables = Table.objects.filter(date=date, size=size).values('id', 'number', 'reserved')  # Include 'id'
        # Serialize the queryset into JSON format
        table_data = list(tables)

        # Return JSON response
        return JsonResponse(table_data, safe=False)
    else:
        # Handle invalid request method
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def update_table_status(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)  # Parse JSON data from request body
        print("Data is: ", data)
        for table_data in data:
            table_id = table_data.get('id')  # Get table_id from POST data
            if table_id is None:
                return JsonResponse({'success': False, 'message': 'Missing table ID in request'}, status=400)

            table_id = int(table_id)  # Attempt to convert to integer
            reserved = table_data.get('reserved')

            table = Table.objects.get(pk=table_id)  # Use primary key (pk) for clarity
            table.reserved = reserved
            table.save()

        return JsonResponse({'success': True})

    except ValueError:  # Handle invalid table_id format
        return JsonResponse({'success': False, 'message': 'Invalid table ID format'}, status=400)
    except Table.DoesNotExist:  # Handle table not found
        return JsonResponse({'success': False, 'message': 'Table does not exist'}, status=404)


def admin_rev123(request):
    # Fetch all reviews from the database
    reviews = Rev.objects.all()

    # Pass the reviews to the template context
    return render(request, 'myapp/admin_rev.html', {'reviews': reviews})


def submit_review(request):
    if request.method == 'POST':
        if request.user.is_authenticated:  # Check if user is authenticated
            # Retrieve username
            username = request.user.username
        else:
            # If user is not authenticated, display an error message
            messages.error(request, "You must be logged in to submit a review.")
            return redirect("home")  # Redirect the user to the login page

        # Retrieve review text from the form
        text = request.POST.get('text', '')  # Assuming 'text' is the name of the field in your form

        if not text:  # Check if review text is empty
            # If review text is empty, display an error message
            messages.error(request, "Review text cannot be empty.")
            return redirect("home")  # Redirect the user to the home page

        # Create Rev object and save it
        my_review = Rev.objects.create(username=username, text=text)

        # Display success message
        messages.success(request, "Your thoughts have been successfully preserved!")

        # Redirect to home page
        return redirect("home")
    else:
        # If request method is not POST, return 404
        return HttpResponse('404 - Not Found')


def index(request):
    return render(request, "myapp/index.html", {})


def rev123(request):
    return render(request, "myapp/cust_rev.html", {})


def admin_rev(request):
    return render(request, "myapp/admin_rev.html", {})


def test(request):
    return render(request, "myapp/test.html", {})


def index2_boot(request):
    return render(request, "myapp/index2_boot.html", {})


def ap(request):
    return render(request, "myapp/admin_page.html", {})


def common(request):
    return render(request, "myapp/common.html", {})


def home(request):
    return render(request, "myapp/home.html", {})


def about(request):
    return render(request, "myapp/aboutus.html", {})


def menu(request):
    return render(request, "myapp/menu.html", {})


def take_away(request):
    if request.user.is_authenticated:
        return render(request, "myapp/take_away.html", {})
    else:
        messages.error(request, "Please login through the connect section for Take-Away")
        return render(request, "myapp/home.html", {})


def reservation(request):
    if request.user.is_authenticated:
        return render(request, "myapp/reservation.html", {})
    else:
        messages.error(request, "Please login through the connect section to book a Table!")
        return render(request, "myapp/home.html", {})


def manage_table(request):
    return render(request, "myapp/ap_1.html", {})


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
            return redirect("home")
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect("home")

        # Email validation
        pattern = r'\b[A-Za-z0-9._%+-]+@gmail.com\b'
        if not re.match(pattern, email):
            messages.error(request, "Email must be in the format abcd@gmail.com")
            return redirect("home")

        if not phone.isdigit():
            messages.error(request, "Phone number must be numeric!")
            return redirect("home")

        myuser = MyUser123.objects.create_user(username=username, email=email, phone=phone, password=password)
        myuser.save()
        messages.success(request, "Your account has been successfully created!")
        return redirect("home")
    else:
        return HttpResponse('404 - Not Found')


def handle2(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the input is an email
        if '@gmail.com' in username_or_email:
            # If it's an email, try to authenticate with email
            user = authenticate(email=username_or_email, password=password)
        else:
            # Otherwise, try to authenticate with username
            user = authenticate(username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username} to One Bite Foods!")
            return redirect("home")
        else:
            messages.error(request, "Invalid Credentials, Please Try Again!!")
            return redirect("home")
    return HttpResponse('handle2')


def handler(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = authenticate(username=username)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Please Sign In from Connect Section!!")
            return redirect("home")
    return HttpResponse('handler')


def lout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')


def lout1(request):
    logout(request)
    return redirect('index2_boot')
