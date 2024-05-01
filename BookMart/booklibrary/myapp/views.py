import json

from django.shortcuts import render, redirect
from .models import Book, Signup, CartTable, OrderTable, Contactus, Status
from django.http import JsonResponse
from django.db.models import Sum
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# Create your views here.

def index(request):
    data = Book.objects.all
    session_status = False;
    try:
        if request.session.get('is_login'):
            session_status = True
            if request.method == 'POST':
                if not request.session.get("is_login"):
                    # Redirect to login page if user is not logged in
                    return redirect('/login')

                uid = request.session.get("user_id")
                if uid is not None:
                    # Check if uid is not None (user is logged in)
                    CartTable.objects.create(uid_id=uid, pid_id=id)
                    session_status = True
                    return redirect('/cart')
                else:
                    # Redirect to login page if user is not logged in
                    return redirect('/login')
        else:
            session_status = False
    except:
        pass
    return render(request, "user/index.html", {"data": data, "status": session_status})


# def bookd(request, id):
#     session_status = False  # Initialize session_status
#     if request.method == 'POST':
#         if not request.session.get("is_login"):
#             # Redirect to login page if user is not logged in
#             return redirect('/login')
#
#         uid = request.session.get("user_id")
#         if uid is not None:
#             # Check if uid is not None (user is logged in)
#             CartTable.objects.create(uid_id=uid, pid_id=id)
#             book_id = id
#             session_status = True
#             return redirect('/cart')
#         else:
#             # Redirect to login page if user is not logged in
#             return redirect('/login')
#     data = Book.objects.get(id=id)
#     uid = request.session.get("user_id")
#     state = Status.objects.filter(uid_id=uid, pid_id=id, update=True).exists()
#     print(session_status)
#     return render(request, "user/bookdetail.html", {"data": data, "session_status": session_status,"buy":state})
#
from django.shortcuts import render, redirect
from .models import Book, Status


def bookd(request, id):
    session_status = False  # Initialize session_status
    if request.method == 'POST':
        if not request.session.get("is_login"):
            # Redirect to login page if user is not logged in
            return redirect('/login')

        uid = request.session.get("user_id")
        if uid is not None:
            # Check if uid is not None (user is logged in)
            # Assuming CartTable is your model for storing cart items
            CartTable.objects.create(uid_id=uid, pid_id=id)
            book_id = id
            session_status = True
            return redirect('/cart')
        else:
            # Redirect to login page if user is not logged in
            return redirect('/login')

    # Retrieve book details
    data = Book.objects.get(id=id)

    # Check if the user has bought the book
    if request.session.get("is_login"):
        uid = request.session.get("user_id")
        state = Status.objects.filter(uid_id=uid, pid_id=id, update=True).exists()
        print("MySTATE",state)
    else:
        state = False
        print("MySTATE",state)

    return render(request, "user/bookdetail.html", {"data": data, "session_status": session_status, "buy": state})


def cart(request):
    if not request.session.get("is_login"):
        return redirect('/login')

    user_id = request.session.get("user_id")

    cart_items = CartTable.objects.filter(uid=user_id)
    total_price = cart_items.aggregate(total_price=Sum('pid__price'))['total_price'] or 0

    cart_details = []
    book_id = None  # Assign a default value to book_id before the loop
    for item in cart_items:
        book_id = item.pid.id  # Update book_id inside the loop
        book_name = item.pid.name
        book_price = item.pid.price
        cart_details.append({'name': book_name, 'price': book_price, "id": book_id})
        request.session['totalprice'] = total_price
        status = Status.objects.create(
            pid_id=book_id,  # Assuming pid is the ForeignKey to Book in Status model
            uid_id=user_id,  # Assuming uid is the ForeignKey to Signup in Status model
            update=True  # Assuming you want to indicate that the order is not yet updated
        )
    # Move the creation of the OrderTable object outside the loop
    cart_details_json = json.dumps(cart_details)
    if book_id:  # Ensure book_id is not None before creating the OrderTable object
        order = OrderTable.objects.create(uid_id=user_id, cart_detail=cart_details_json, amount=total_price,
                                          bookid_id=book_id)

    context = {
        "cart_details": cart_details,
        "total_price": total_price,
        "cart_details_json": json.dumps([]),  # Default value if cart_details is empty
    }

    if cart_details:
        context["cart_details_json"] = cart_details_json

    return render(request, 'user/cart.html', context)


def signup(request):
    if request.POST:
        n = request.POST['name']
        e = request.POST['email']
        p = request.POST['password']
        obj = Signup(uname=n, email=e, password=p)
        obj.save()
        return redirect('/login')
    return render(request, "user/signup.html")


def login(request):
    if request.POST:
        e = request.POST['email']
        p = request.POST['password']
        count = Signup.objects.filter(email=e, password=p).count()
        request.session['is_login'] = True
        request.session['user_id'] = Signup.objects.values('id').filter(email=e, password=p)[0]['id']
        if count > 0:
            return redirect('/#')
    return render(request, "user/login.html")


def payment_process(request):
    # Razorpay KeyId and key Secret
    key_id = 'rzp_test_PvM4GxK9MYlCUc'
    key_secret = 'WzsOTRAU4l3oAA1CS7jlVS5E'

    amount = int(request.session['totalprice']) * 100  # Your Amount
    request.session['amount'] = amount
    client = razorpay.Client(auth=(key_id, key_secret))

    data = {
        'amount': amount,
        'currency': 'INR',
        "receipt": "Kindle",
        "notes": {
            'name': 'Krupa Bhavsar',
            'payment_for': 'Kindle Test'
        }
    }
    id = request.session.get("user_id")
    result = Signup.objects.get(pk=id)
    payment = client.order.create(data=data)
    request.session['amount'] = amount
    context = {'payment': payment, 'result': result, 'amount': amount}
    return render(request, 'user/payment_process.html', context, )


@csrf_exempt
def success(request):
    context = {}
    user_id = request.session.get('user_id')
    print("MYUSERID", user_id)
    payment_id = request.POST.get('razorpay_payment_id')
    cart_detail = request.session.get("cart_details", [])
    data1 = None

    if user_id:
        data1 = Signup.objects.filter(id=user_id).first()
        if data1:
            context['paymentID'] = payment_id
            context['user_id'] = data1.uname
            print("MYUSERID", user_id)

    # Pass cart details to the template
    context['cart_detail'] = cart_detail

    return render(request, 'user/success.html', context)


def myorder(request):
    # requestdata=CartTable.objects.all()

    if not request.session.get("is_login"):
        return redirect('/login')

    user_id = request.session.get("user_id")

    # Filter CartTable objects for the current user ID
    cart_items = CartTable.objects.filter(uid=user_id)
    total_price = cart_items.aggregate(total_price=Sum('pid__price'))['total_price'] or 0

    # Extract book details for the user's cart
    cart_details = []
    for item in cart_items:
        book_name = item.pid.name
        book_price = item.pid.price
        book_image = item.pid.image
        pdf = item.pid.pdf
        audio = item.pid.audio

        # Add any other book details you need here
        cart_details.append({'name': book_name, 'price': book_price, 'image': book_image, "pdf": pdf, "audio": audio})
        print(book_name)
        print(book_price)
        request.session['totalprice'] = total_price
    return render(request, 'user/showdetail.html', {"data": cart_details, "total_price": total_price})


def logout(request):
    del request.session['is_login']
    return redirect('/')


def add_to_cart(request, id):
    if not request.session.get("is_login"):
        return JsonResponse({'error': 'User not logged in'}, status=401)

    uid = request.session.get("user_id")
    if uid is not None:
        CartTable.objects.create(uid_id=uid, pid_id=id)

    total_items = CartTable.objects.filter(uid_id=uid).count()

    # Update the session with the new total items count
    request.session['total'] = total_items

    total_items = request.session.get('total', 0)

    # Return JSON response with updated total items count
    return JsonResponse({'total_items': total_items})


def contactus(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['msg']
        obj = Contactus(name=name, email=email, message=message)
        obj.save()
        return redirect('/#')
