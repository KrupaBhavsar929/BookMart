from django.shortcuts import render, redirect
from .models import suppliersignup
# Create your views here.
from myapp.models import Signup, Book, OrderTable,Contactus


def index(request):
    data = suppliersignup.objects.all
    return render(request, "supplier/home.html", {"data": data})


def signup(request):
    if request.POST:
        u = request.POST['username']
        e = request.POST['email']
        p = request.POST['password']
        obj = suppliersignup(uname=u, email=e, password=p)
        obj.save()
        return redirect('/#')
    return render(request, 'supplier/registration.html')


def login(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        count = suppliersignup.objects.filter(email=email, password=password).count()
        if count > 0:
            request.session['is_login'] = True
            request.session['user_id'] = suppliersignup.objects.values('id').filter(email=email, password=password)[0]['id']
            return redirect('/index')
    return render(request, 'supplier/login.html')


def create_blog(request):
    return render(request, "supplier/create_blog.html")


def blog(request):
    if request.POST:
        name = request.POST['name']
        description = request.POST['description']
        img = request.FILES['img']
        price = request.POST['price']
        author = request.POST['author']
        version = request.POST['version']
        audio = request.FILES['audio']
        pdf = request.FILES['pdf']
        obj = Book(name=name, image=img, detail=description, price=price, author=author, version=version, audio=audio,
                   pdf=pdf)
        obj.save()
        return redirect("/index")
    return render(request, "supplier/create_blog.html")


def viewbook(request):
    data = Book.objects.all
    return render(request, "supplier/member.html", {"data": data})


def remove(request, id):
    Book.objects.get(id=id).delete()
    return redirect('/viewbook')


def logout(request):
    del request.session['is_login']
    return redirect('/#')


def vieworder(request):
    data = OrderTable.objects.all
    return render(request, "supplier/confirm.html", {"data": data})

def getContact(request):
    data=Contactus.objects.all
    return render(request,"supplier/create_portfolio.html",{"data":data})

