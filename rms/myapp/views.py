import random
import urllib
import urllib.parse
import urllib.request
import xmltodict
import calendar
import json
import re
import uuid
from datetime import date
from datetime import timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import MyUser123, Rev, Order, Food, Staff, DineInOrder, DineInOrderItem, Order123
from .models import Table

from django.shortcuts import render, redirect
# from .forms import MenuItemForm
from .models import MenuItem


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
        username = request.POST.get('username')
        email = request.POST.get('email')
        # Construct the sorry email message
        subject = 'Apologies for Inconvenience'
        body = f'Dear {username},\n\nWe apologize, but we are unable to confirm your order at the moment.\n\nPlease accept our apologies. You may check for availability at another time or contact us for further assistance.\n\nBest regards,\nOne Bites Foods'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]

        # Send the email
        send_mail(subject, body, from_email, to_email, fail_silently=False)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


def order_details_view(request):
    # Count the number of completed orders
    completed_orders_count = Order.objects.filter(completed=False).count()
    completed_orders_count1 = DineInOrder.objects.filter(status='Preparing').count()

    # Pass the count to the template context
    context = {
        'completed_orders_count': completed_orders_count,
        'completed_orders_count1': completed_orders_count1,
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
    return render(request, "myapp/take_away.html", {})


def reservation(request):
    return render(request, "myapp/reservation.html", {})


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
                # Perform login and store the admin username and role in the session
                request.session['admin_username'] = admin_user.username
                request.session['admin_role'] = admin_user.role
                return JsonResponse({'success': True, 'username': admin_user.username, 'role': admin_user.role})

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
            return JsonResponse({'success': False, 'error_message': "Please don't leave any of the fields blank!"})

        if len(username) > 10:
            return JsonResponse({'success': False, 'error_message': "Username must be under 10 characters"})

        if not username.isalnum():
            return JsonResponse({'success': False, 'error_message': "Username must be alphanumeric!"})

        # Email validation
        pattern = r'\b[A-Za-z0-9._%+-]+@(?:gmail\.com|heraldcollege\.edu\.np)\b'
        if not re.match(pattern, email):
            return JsonResponse({'success': False, 'error_message': "Email must be in the format abcd@gmail.com"})

        if not phone.isdigit():
            return JsonResponse({'success': False, 'error_message': "Phone number must be numeric!"})

        myuser = MyUser123.objects.create_user(username=username, email=email, phone=phone, password=password)
        myuser.save()

        # Authenticate the user and log them in
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse(
                {'success': True, 'message': "Your account has been successfully created!", 'stay_logged_in': True,
                 'username': user.username})
        else:
            return JsonResponse({'success': False, 'error_message': "Unable to log in the user"})
    else:
        return HttpResponse('404 - Not Found')


def handle2(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = MyUser123.objects.get(username=username)
        except MyUser123.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Invalid Credentials, Please Try Again!!'})

        if user.check_password(password):
            login(request, user)
            return JsonResponse({'success': True, 'username': user.username})

        else:
            return JsonResponse({'success': False, 'error_message': 'Invalid Credentials, Please Try Again!!'})

    return HttpResponse('index')


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
    return JsonResponse({'success': True})


def lout1(request):
    return redirect('admin_login')


def admin_menu(request):
    return render(request, "myapp/admin_menu.html", {})


def name(request):
    return render(request, "myapp/admin_reservation_control.html", {})


def add_tables_for_30_days(request):
    # Get today's date
    today = date.today()

    # Calculate the last day of the month
    last_day_of_month = today.replace(day=calendar.monthrange(today.year, today.month)[1])

    # Check if tables for the entire month already exist
    existing_tables = Table.objects.filter(date__gte=today, date__lte=last_day_of_month)
    if existing_tables.exists():
        return JsonResponse({'status': 'error', 'message': 'Tables already added for this month!'})

    # Loop over the days in the month
    for i in range(last_day_of_month.day):
        # Calculate the date for the current iteration
        current_date = today + timedelta(days=i)

        # Create tables for the current date
        table_sizes = [1, 2, 4, 6, 8]  # Table sizes
        table_numbers = [666, 777, 999, 6969, 1012, 1234]  # Table numbers

        for size in table_sizes:
            for number in table_numbers:
                table = Table.objects.create(date=current_date, size=size, number=number)

    return JsonResponse({'status': 'success', 'message': 'Tables added for the entire month.'})


def dine(request):
    foods = Food.objects.all()  # Assuming Food is your model
    return render(request, 'myapp/dine_in.html', {'foods': foods})


@csrf_exempt
def confirm_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        table_number = data['table_number']
        order_items = data['order_items']
        total_price = data['total_price']

        # Create the DineInOrder
        order = DineInOrder.objects.create(
            table_number=table_number,
            total_price=total_price
        )

        # Create the DineInOrderItems
        for item in order_items:
            DineInOrderItem.objects.create(
                order=order,
                food=item['food'],
                quantity=item['quantity'],
                price=item['price']
            )

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def admin_dashboard(request):
    completed_orders_count = DineInOrder.objects.filter(completed=True).count()
    return render(request, 'myapp/admin_page.html', {'completed_orders_count': completed_orders_count})


def dine_in_details(request):
    orders = DineInOrder.objects.all()
    order_data = []
    for order in orders:
        order_items = DineInOrderItem.objects.filter(order=order)
        order_data.append({
            'id': order.id,
            'table_number': order.table_number,
            'total_price': str(order.total_price),
            'status': order.status,
            'canceled': order.canceled,
            'items': list(order_items.values('food', 'quantity'))
        })
    return JsonResponse(order_data, safe=False)


@csrf_exempt
def cancel_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data['order_id']
        order = DineInOrder.objects.get(id=order_id)
        order.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def complete_orders(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = DineInOrder.objects.get(pk=order_id)
            if order.status == 'Preparing':
                order.status = 'Completed'
                order.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Order is not in the Preparing state'})
        except DineInOrder.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Order not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def place_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        items = data['items']
        pickup_time = data['pickupTime']
        pickup_location = data['pickupLocation']
        total = data['total']
        username = data.get('username', None)  # Get the username from the request data

        # Generate a unique order number
        order_number = generate_order_number()

        # Create a new order and save it to the database
        order = Order123.objects.create(
            items=items,
            pickup_time=pickup_time,
            pickup_location=pickup_location,
            order_number=order_number,
            total=total,
            user_name=username  # Set the user_name field with the received username
        )
        order.save()

        return JsonResponse({'orderNumber': order_number})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def generate_order_number():
    # Generate a random 4-digit order number
    return str(random.randint(1000, 9999))


@login_required
def get_order_history(request):
    if request.method == 'GET':
        today = date.today()
        orders = Order123.objects.filter(
            user_name=request.user.username,
            created_at__date=today
        ).order_by('-created_at').values(
            'order_number', 'items', 'pickup_location', 'pickup_time'
        )
        order_history = []
        for order in orders:
            pickup_time = int(order['pickup_time'].timestamp() * 1000)  # Convert to Unix timestamp in milliseconds
            order_data = {
                'order_number': order['order_number'],
                'items': order['items'],
                'pickup_location': order['pickup_location'],
                'pickup_time': pickup_time,
            }
            order_history.append(order_data)
        return JsonResponse({'order_history': order_history})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def cancel_order_takeaway(request, order_number):
    if request.method == 'DELETE':
        try:
            order = Order123.objects.get(order_number=order_number)
            now = timezone.now()
            time_diff = now - order.created_at
            if time_diff.total_seconds() <= 1800:  # 30 minutes in seconds
                order.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'You can only cancel an order within 30 minutes of placing it.'},
                                    status=400)
        except Order123.DoesNotExist:
            return JsonResponse({'error': 'Order not found.'}, status=404)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def admin_orders(request):
    # Fetch orders from the database
    orders = Order123.objects.all()
    return render(request, 'myapp/ap_2.html', {'orders': orders})


def cancel_order_ta(request):
    if request.method == 'POST':
        order_number = request.POST.get('order_number')
        order = get_object_or_404(Order123, order_number=order_number)
        order.delete()
        return JsonResponse({'message': 'Order canceled successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@require_POST
def complete_order_ta(request):
    order_number = request.POST.get('order_number')
    try:
        order = Order123.objects.get(order_number=order_number)
        order.status = 'Completed'
        order.save()
        return JsonResponse({'success': True, 'message': 'Order marked as completed.'})
    except Order123.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Order not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def esewa(request):
    return render(request, "myapp/esewa.html", {})


def orders69(request, id):
    # Retrieve the order details based on the order_number
    order = get_object_or_404(Order123, order_number=id)

    context = {
        'order': order,
        'order_number': id,
    }
    return render(request, 'myapp/order_checkout.html', context)


def esewa_callback_view(request):
    oid = request.GET.get("oid")
    amt = request.GET.get("amt")
    refId = request.GET.get("refId")
    url = "https://uat.esewa.com.np/epay/transrec"
    data = urllib.parse.urlencode({
        'amt': amt,
        'scd': 'EPAYTEST',
        'rid': refId,
        'pid': oid,
    }).encode()

    response = urllib.request.urlopen(url, data=data).read()
    json_response = xmltodict.parse(response)
    status = json_response["response"]["response_code"]

    if status == "Success":
        order = get_object_or_404(Order123, order_number=oid)
        order.is_paid = True
        order.paid_amount = int(float(amt))
        order.save()
        return render(request, 'myapp/esewa_callback.html')
    else:
        return redirect("payment_failed")


def payment_failed(request):
    return render(request, 'myapp/payment_failed.html')


def esewa_callback(request):
    return render(request, 'myapp/esewa_callback.html')


def order_now(request):
    return render(request, 'myapp/order_page.html', {})


def menu(request):
    menu_items = MenuItem.objects.all()
    form = MenuItemForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('menu')

    context = {
        'menu_items': menu_items,
        'form': form,
    }
    return render(request, 'myapp/admin_menu.html', context)