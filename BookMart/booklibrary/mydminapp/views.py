from django.shortcuts import render, redirect
from .models import signapp
# Create your views here.
from myapp.models import Signup, Book, OrderTable,Contactus


def index(request):
    data = Signup.objects.all
    return render(request, "adminmaster/home.html", {"data": data})


def signup(request):
    if request.POST:
        u = request.POST['username']
        e = request.POST['email']
        p = request.POST['password']
        obj = signapp(uname=u, email=e, password=p)
        obj.save()
        return redirect('/#')
    return render(request, 'adminmaster/registration.html')


def login(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        count = signapp.objects.filter(email=email, password=password).count()
        if count > 0:
            request.session['is_login'] = True
            request.session['user_id'] = signapp.objects.values('id').filter(email=email, password=password)[0]['id']
            return redirect('/index')
    return render(request, 'adminmaster/login.html')


def create_blog(request):
    return render(request, "adminmaster/create_blog.html")


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
    return render(request, "adminmaster/create_blog.html")


def viewbook(request):
    data = Book.objects.all
    return render(request, "adminmaster/member.html", {"data": data})


def remove(request, id):
    Book.objects.get(id=id).delete()
    return redirect('/viewbook')


def logout(request):
    del request.session['is_login']
    return redirect('/#')


def vieworder(request):
    data = OrderTable.objects.all
    return render(request, "adminmaster/confirm.html", {"data": data})

def getContact(request):
    data=Contactus.objects.all
    return render(request,"adminmaster/create_portfolio.html",{"data":data})

