from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from datetime import date
from django.core.mail import send_mail
from .models import MyUser123, Rev, Order, Food, Staff
import re
from .models import Table
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
import json
from django.db.models import Count, Q
from django.conf import settings


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


def submit_review(request):
    if request.method == 'POST':
        if request.user.is_authenticated:  # Check if user is authenticated
            # Retrieve username
            username = request.user.username
        else:
            # If user is not authenticated, display an error message
            messages.error(request, "You must be logged in to submit a review.")
            return redirect("index")  # Redirect the user to the login page

        # Retrieve review text from the form
        text = request.POST.get('text', '')  # Assuming 'text' is the name of the field in your form

        if not text:  # Check if review text is empty
            # If review text is empty, display an error message
            messages.error(request, "Review text cannot be empty.")
            return redirect("index")  # Redirect the user to the home page

        # Create Rev object and save it
        my_review = Rev.objects.create(username=username, text=text)

        # Display success message
        messages.success(request, "Your thoughts have been successfully preserved!")

        # Redirect to home page
        return redirect("index")
    else:
        # If request method is not POST, return 404
        return HttpResponse('404 - Not Found')


def display_reviews(request):
    # Fetch all reviews from the database
    reviews = Rev.objects.all()

    # Render the reviews in a template
    return render(request, 'myapp/admin_rev.html', {'reviews': reviews})


def book(request):
    if request.method == 'POST':
        # Check if the request method is POST (meaning the form was submitted)
        username = request.user.username
        # Get the username of the logged-in user

        # Retrieve the order details from the form
        date = request.POST.get('order-date', '')
        time = request.POST.get('order-time', '')
        nop = request.POST.get('number-of-people', '')
        msg = request.POST.get('order-message', '')

        # Check if any of the fields are empty
        if not (date and time and nop and msg):
            # If any field is empty, display an error message
            messages.error(request, "Kindly fill up all the fields in the form to confirm the order.")
            return redirect("index")  # Redirect to the home page or wherever appropriate

        # Create a Rev object with the retrieved data
        my_review = Order.objects.create(username=username, date=date, time=time, number_of_people=nop, message=msg)

        # Display a success message
        messages.success(request, "Kindly Check your Gmail for confirmation! We will reach you ASAP!!")

        # Redirect to the home page after successfully saving the order
        return redirect("index")
    else:
        # If the request method is not POST, return a 404 response
        return HttpResponse('404 - Not Found')


def display_orders(request):
    # Fetch all orders from the database
    orders = Order.objects.all()

    # Fetch username, phone number, and email from UserDetails for each order
    for order in orders:
        try:
            user_details = MyUser123.objects.get(username=order.username)
            order.phone_number = user_details.phone
            order.email = user_details.email
        except MyUser123.DoesNotExist:
            # Handle the case where UserDetails for the username does not exist
            pass

    # Render the orders in a template
    return render(request, 'myapp/admin_reservation_control.html', {'orders': orders})


def send_confirmation_email(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        number_of_people = request.POST.get('number_of_people')
        message = request.POST.get('message')

        # Construct the email message
        subject = 'Order Confirmation'
        body = f'Dear {username},\n\nThank you for your order.\n\nOrder Details:\nOrder ID: {order_id}\nDate: {date}\nTime: {time}\nNumber of People: {number_of_people}\nMessage: {message}\n\nWe look forward to serving you. If you have any further questions, please don\'t hesitate to contact us.\n\nBest regards,\nOne Bites Foods'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]

        # Send the email
        send_mail(subject, body, from_email, to_email, fail_silently=False)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


def send_sorry_email(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        number_of_people = request.POST.get('number_of_people')
        message = request.POST.get('message')

        # Construct the sorry email message
        subject = 'Apologies for Inconvenience'
        body = f'Dear {username},\n\nWe apologize, but we are unable to confirm your order at the moment.\n\nOrder Details:\nOrder ID: {order_id}\nDate: {date}\nTime: {time}\nNumber of People: {number_of_people}\nMessage: {message}\n\nPlease accept our apologies. You may check for availability at another time or contact us for further assistance.\n\nBest regards,\nOne Bites Foods'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]

        # Send the email
        send_mail(subject, body, from_email, to_email, fail_silently=False)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})
def order_details_view(request):
    # Count the number of completed orders
    completed_orders_count = Order.objects.filter(completed=False).count()

    # Pass the count to the template context
    context = {
        'completed_orders_count': completed_orders_count,
    }

    return render(request, 'myapp/admin_dash.html', context)


def save_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        is_checked = request.POST.get('is_checked') == 'true'  # Convert string to boolean

        order = Order.objects.get(pk=order_id)

        # Update the confirmed status based on the checkbox state
        if is_checked:
            order.confirmed = True
        else:
            order.confirmed = False

        order.save()

        # Return JSON response with the confirmed status
        return JsonResponse({'status': 'success', 'confirmed': order.confirmed})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def complete_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(pk=order_id)
        order.completed = not order.completed  # Toggle the completed status
        order.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def index(request):
    return render(request, "myapp/index.html", {})


def rev123(request):
    return render(request, "myapp/cust_rev.html", {})


def test(request):
    return render(request, "myapp/test.html", {})


def ad(request):
    return render(request, "myapp/admin_dash.html", {})


def dine_in(request):
    return render(request, "myapp/dine_in.html", {})


def ap(request):
    return render(request, "myapp/admin_page.html", {})


def common(request):
    return render(request, "myapp/common.html", {})


def about(request):
    return render(request, "myapp/aboutus.html", {})


def menu(request):
    return render(request, "myapp/menu.html", {})


def take_away(request):
    if request.user.is_authenticated:
        return render(request, "myapp/take_away.html", {})
    else:
        messages.error(request, "Please login through the connect section for Take-Away")
        return render(request, "myapp/index.html", {})


def reservation(request):
    if request.user.is_authenticated:
        return render(request, "myapp/reservation.html", {})
    else:
        messages.error(request, "Please login through the connect section to book a Table!")
        return render(request, "myapp/index.html", {})


def manage_table(request):
    return render(request, "myapp/ap_1.html", {})


def admin_login(request):
    return render(request, "myapp/admin_cred.html", {})


def admin_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            admin_user = Staff.objects.get(username=username)
            if admin_user.password == password:
                # Perform login and store the admin username in the session
                request.session['admin_username'] = admin_user.username
                return JsonResponse({'success': True, 'username': admin_user.username})
            else:
                return JsonResponse({'success': False, 'error_message': 'Invalid Credentials, Please Try Again!!'})
        except Staff.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Invalid Credentials, Please Try Again!!'})

    return HttpResponse('admin_page')


def handle1(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        # Check if any of the fields are empty
        if not username or not email or not phone or not password:
            messages.error(request, "Please don't leave any of the fields blank!")
            return redirect("index")

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect("index")
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect("index")

        # Email validation
        pattern = r'\b[A-Za-z0-9._%+-]+@gmail.com\b'
        if not re.match(pattern, email):
            messages.error(request, "Email must be in the format abcd@gmail.com")
            return redirect("index")

        if not phone.isdigit():
            messages.error(request, "Phone number must be numeric!")
            return redirect("index")

        myuser = MyUser123.objects.create_user(username=username, email=email, phone=phone, password=password)
        myuser.save()
        messages.success(request, "Your account has been successfully created!")
        return redirect("index")
    else:
        return HttpResponse('404 - Not Found')


def handle2(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome to One Bite Foods, {user.username}!")
            return redirect("index")
        else:
            messages.error(request, "Invalid Credentials, Please Try Again!!")
            return redirect("index")
    return HttpResponse('handle2')


def handler(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = authenticate(username=username)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Please Sign In from Connect Section!!")
            return redirect("index")
    return HttpResponse('handler')


def lout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('index')


def lout1(request):
    return redirect('admin_login')


def admin_menu(request):
    return render(request, "myapp/admin_menu.html", {})


def name(request):
    return render(request, "myapp/admin_reservation_control.html", {})


def add_tables_for_day(request):
    # Get today's date
    today = date.today()

    # Check if tables for today already exist
    existing_tables = Table.objects.filter(date=today)

    if not existing_tables:
        # If tables for today don't exist, create them
        table_sizes = [1, 2, 4, 6, 8]  # Table sizes
        table_numbers = [666, 777, 999, 6969, 1012, 1234]  # Table numbers

        for size in table_sizes:
            for number in table_numbers:
                table = Table.objects.create(date=today, size=size, number=number)

        return JsonResponse({'status': 'success', 'message': 'Tables added for the day.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Tables for the day already exist.'})


def dine(request):
    foods = Food.objects.all()  # Assuming Food is your model
    return render(request, 'myapp/dine_in.html', {'foods': foods})



