from pydoc import describe
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)


class BookGenre(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)


class Book(models.Model):
    publisher = models.ForeignKey("Publisher", on_delete=models.PROTECT)
    bookGenres = models.ManyToManyField("BookGenre")
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    quantity = models.PositiveIntegerField()
    available = models.BooleanField()
    image = models.ImageField(upload_to="bookPics/", null=True)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    fullName = models.CharField(max_length=100)
    sex = models.CharField(max_length=20)
    address = models.CharField(max_length=1000)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    pic = models.ImageField(upload_to="customerPics/", null=True)


def expiry():
    return datetime.today() + timedelta(days=7)


class IssueBook(models.Model):
    STATUS = (
        ("Issueing", "Issueing"),
        ("Pending", "Pending"),
        ("Unreturned", "Unreturned"),
        ("Returned", "Returned"),
        ("Expired", "Expired"),
        ("ExpireReturned", "ExpireReturned"),
    )
    customer = models.ForeignKey("Customer", on_delete=models.PROTECT)
    issueDate = models.DateField(auto_now_add=True)
    returnDate = models.DateField(default=expiry)
    status = models.CharField(max_length=20, choices=STATUS)


class IssueBookDetail(models.Model):
    issueBook = models.ForeignKey("IssueBook", on_delete=models.PROTECT)
    book = models.ForeignKey("Book", on_delete=models.PROTECT)
