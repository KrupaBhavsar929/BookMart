from django.db import models


# Create your models here.
class Signup(models.Model):
    uname = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=10)


class Book(models.Model):
    name = models.CharField(max_length=50)
    detail = models.CharField(max_length=500)
    price = models.CharField(max_length=10)
    image = models.ImageField(upload_to='image/')
    author = models.CharField(max_length=30)
    version = models.CharField(max_length=10)
    audio = models.FileField()
    pdf = models.FileField()


class CartTable(models.Model):
    pid = models.ForeignKey(Book, models.CASCADE)
    uid = models.ForeignKey(Signup, models.CASCADE)


class OrderTable(models.Model):
    uid = models.ForeignKey(Signup, models.CASCADE)
    bookid=models.ForeignKey(Book,models.CASCADE)
    cart_detail=models.CharField(max_length=300)
    amount=models.CharField(max_length=30)

class Contactus(models.Model):
    name=models.CharField(max_length=40)
    email=models.EmailField()
    message=models.CharField(max_length=200)

class Status(models.Model):
    pid = models.ForeignKey(Book, models.CASCADE)
    uid = models.ForeignKey(Signup, models.CASCADE)
    update=models.BooleanField()

