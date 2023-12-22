from django.shortcuts import redirect, render, HttpResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from . import models
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required(login_url="/")
def listPublishers(request):
    publishers = Publisher.objects.all()
    return render(request, "listPublishers.html", {"publishers": publishers})


@login_required(login_url="/")
def addPublisher(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        publishers = Publisher.objects.create(name=name, email=email, contact=contact)
        publishers.save()
        alert = True
        return render(request, "addPublisher.html", {"alert": alert})
    return render(request, "addPublisher.html")


@login_required(login_url="/")
def updatePublisher(request, id):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        contact = request.POST["contact"]

        publisher = Publisher.objects.filter(id=id)
        publisher.update(name=name, email=email, contact=contact)
        alert = True
        return render(request, "updatePublisher.html", {"alert": alert})
    publisher = Publisher.objects.filter(id=id)
    return render(request, "updatePublisher.html", {"publisher": publisher})


@login_required(login_url="/")
def deletePublisher(request, id):
    publishers = Publisher.objects.filter(id=id)
    try:
        publishers.delete()
    except:
        error = True
        return render(request, "listPublishers.html", {"error": error})
    return redirect("/view_publishers/")


@login_required(login_url="/")
def listBookGernes(request):
    bookgenres = BookGenre.objects.all()
    return render(request, "listBookGenres.html", {"bookgenres": bookgenres})


@login_required(login_url="/")
def addBookGenre(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]

        bookgenres = BookGenre.objects.create(name=name, description=description)
        bookgenres.save()
        alert = True
        return render(request, "addBookGenre.html", {"alert": alert})
    return render(request, "addBookGenre.html")


@login_required(login_url="/")
def updateBookGenre(request, id):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]

        bookgenre = BookGenre.objects.filter(id=id)
        bookgenre.update(name=name, description=description)
        alert = True
        return render(request, "updateBookGenre.html", {"alert": alert})
    bookgenre = BookGenre.objects.filter(id=id)
    return render(request, "updateBookGenre.html", {"bookgenre": bookgenre})


@login_required(login_url="/")
def deleteBookGerne(request, id):
    bookgenres = BookGenre.objects.filter(id=id)
    bookgenres.delete()
    return redirect("/view_bookgenres/")


# @login_required(login_url="/")
def listBooks(request):
    books = Book.objects.all()

    for b in books:
        genre = [bg.name for bg in BookGenre.objects.filter(book=b)]
        str1 = ""
        if len(genre) != 0:
            for ele in genre[0 : len(genre) - 1]:
                str1 += ele + ", "
            str1 += genre[len(genre) - 1]
        b.bookGenresStr = str1
    return render(request, "listBooks.html", {"books": books})


@login_required(login_url="/")
def addBook(request):
    if request.method == "POST":
        name = request.POST["name"]
        author = request.POST["author"]
        description = request.POST["description"]
        quantity = request.POST["quantity"]
        publisherId = request.POST["publisherId"]
        bookgenreIds = request.POST.getlist("bookgenreIds")
        image = request.FILES["image"]
        available = True
        if quantity == 0:
            available = False
        books = Book.objects.create(
            name=name,
            image=image,
            author=author,
            publisher_id=publisherId,
            description=description,
            quantity=quantity,
            available=available,
        )
        books.save()
        books.bookGenres.add(*bookgenreIds)
        books.save()
        alert = True
        return render(request, "addBook.html", {"alert": alert})
    publishers = Publisher.objects.all()
    bookgenres = BookGenre.objects.all()
    return render(
        request, "addBook.html", {"publishers": publishers, "bookgenres": bookgenres}
    )


@login_required(login_url="/")
def updateBook(request, id):
    if request.method == "POST":
        author = request.POST["author"]
        description = request.POST["description"]
        quantity = request.POST["quantity"]
        publisherId = request.POST["publisherId"]
        bookgenreIds = request.POST.getlist("bookgenreIds")
        available = True
        if quantity == "0":
            available = False
        books = Book.objects.filter(id=id)
        books.update(
            author=author,
            publisher_id=publisherId,
            description=description,
            quantity=quantity,
            available=available,
        )
        books.first().bookGenres.clear()
        books.first().save()
        books.first().bookGenres.add(*bookgenreIds)
        books.first().save()
        alert = True
        return render(request, "updateBook.html", {"alert": alert})

    book = Book.objects.filter(id=id)
    publishers = Publisher.objects.all()
    bookgenres = BookGenre.objects.all()

    for b in book:
        for p in publishers:
            if b.publisher.id == p.id:
                p.selected = "selected"
            else:
                p.selected = ""

        bookgenreOfBook = BookGenre.objects.filter(book=b)
        for bg1 in bookgenreOfBook:
            for bg2 in bookgenres:
                if bg1.id == bg2.id:
                    bg2.selected = "selected"
                else:
                    bg2.selected = ""

    return render(
        request,
        "updateBook.html",
        {"book": book, "publishers": publishers, "bookgenres": bookgenres},
    )


@login_required(login_url="/")
def deleteBook(request, id):
    books = Book.objects.filter(id=id)
    try:
        books.delete()
    except:
        error = True
        return render(request, "listBooks.html", {"error": error})
    return redirect("/view_books/")


@login_required(login_url="/")
def Library(request):
    # if there is keyword, show books that matches with keyword
    if request.method == "POST":
        keyword = request.POST["keyword"]
        books = Book.objects.filter(
            Q(name__icontains=keyword) | Q(author__icontains=keyword)
        )
        for b in books:
            genre = [bg.name for bg in BookGenre.objects.filter(book=b)]
            str1 = ""
            if len(genre) != 0:
                for ele in genre[0 : len(genre) - 1]:
                    str1 += ele + ", "
                str1 += genre[len(genre) - 1]
            b.bookGenresStr = str1
        return render(request, "library.html", {"books": books})

    # if have no keyword show all books
    books = Book.objects.all()
    for b in books:
        genre = [bg.name for bg in BookGenre.objects.filter(book=b)]
        str1 = ""
        if len(genre) != 0:
            for ele in genre[0 : len(genre) - 1]:
                str1 += ele + ", "
            str1 += genre[len(genre) - 1]
        b.bookGenresStr = str1
    return render(request, "library.html", {"books": books})


@login_required(login_url="/")
def issueBook(request, id):

    # if user has any pending issue, they cannot create any issue book
    current_user = request.user
    customer = Customer.objects.filter(user=current_user)
    pendingIssueCount = IssueBook.objects.filter(
        customer=customer.first(), status="Pending"
    ).count()
    unreturnedIssueCount = IssueBook.objects.filter(
        customer=customer.first(), status="Unreturned"
    ).count()
    expiredIssueCount = IssueBook.objects.filter(
        customer=customer.first(), status="Unreturned"
    ).count()

    if pendingIssueCount >= 1 or unreturnedIssueCount >= 1 or expiredIssueCount >= 1:
        books = Book.objects.all()
        for b in books:
            genre = [bg.name for bg in BookGenre.objects.filter(book=b)]
            str1 = ""
            if len(genre) != 0:
                for ele in genre[0 : len(genre) - 1]:
                    str1 += ele + ", "
                str1 += genre[len(genre) - 1]
            b.bookGenresStr = str1
        return render(request, "library.html", {"books": books, "alreadyPending": True})

    # user can only add up to 3 books in on issuebook
    book = Book.objects.filter(id=id)
    issuebook = IssueBook.objects.filter(customer=customer.first(), status="Issueing")
    if not issuebook:
        issue = IssueBook.objects.create(
            customer=customer.first(),
            status="Issueing",
        )
        issue.save()
        issueDetail = IssueBookDetail.objects.create(issueBook=issue, book=book.first())
        issueDetail.save()
    else:
        issueDetailCount = IssueBookDetail.objects.filter(
            issueBook=issuebook.first()
        ).count()
        if issueDetailCount >= 3:
            books = Book.objects.all()
            for b in books:
                genre = [bg.name for bg in BookGenre.objects.filter(book=b)]
                str1 = ""
                if len(genre) != 0:
                    for ele in genre[0 : len(genre) - 1]:
                        str1 += ele + ", "
                    str1 += genre[len(genre) - 1]
                b.bookGenresStr = str1
            return render(
                request, "library.html", {"books": books, "maxIssuedDetail": True}
            )
        issueDetail = IssueBookDetail.objects.create(
            issueBook=issuebook.first(), book=book.first()
        )
        issueDetail.save()
    return render(request, "library.html", {"alert": True})


@login_required(login_url="/")
def submitIssueBook(request):
    current_user = request.user
    customer = Customer.objects.filter(user=current_user)
    issuebook = IssueBook.objects.filter(customer=customer.first(), status="Issueing")
    issuebookDetails = IssueBookDetail.objects.filter(issueBook=issuebook.first())
    if request.method == "POST":
        issuebook.update(status="Pending")
        alert = True
        return render(request, "submitIssueBook.html", {"alert": alert})
    return render(
        request, "submitIssueBook.html", {"issuebookDetails": issuebookDetails}
    )


@login_required(login_url="/")
def deleteIssueBookDetail(request, id):
    issueBookDetails = IssueBookDetail.objects.filter(id=id)
    issueBookDetails.delete()
    return redirect("/submit_issue_book/")


@login_required(login_url="/")
def listCustomerIssuedBooks(request):
    autoUpdatedIssueBookStatus()
    current_user = request.user
    customer = Customer.objects.filter(user=current_user)
    issueBooks = IssueBook.objects.filter(customer=customer.first()).exclude(
        status="Issueing"
    )
    issueBookDetails = []
    for issue in issueBooks:
        details = IssueBookDetail.objects.filter(issueBook=issue)
        issueBookDetails.append({"issue": issue, "details": details})

    return render(
        request,
        "listCustomerIssuedBooks.html",
        {"issueBookDetails": issueBookDetails},
    )


@login_required(login_url="/")
def listIssuedBooks(request):
    autoUpdatedIssueBookStatus()
    issueBooks = IssueBook.objects.exclude(status="Issueing")
    issueBookDetails = []
    for issue in issueBooks:
        isPending = False
        isUnreturned = False
        isExpired = False
        if issue.status == "Pending":
            isPending = True
        if issue.status == "Unreturned":
            isUnreturned = True
        if issue.status == "Expired":
            isExpired = True

        details = IssueBookDetail.objects.filter(issueBook=issue)
        issueBookDetails.append(
            {
                "issue": issue,
                "details": details,
                "isPending": isPending,
                "isUnreturned": isUnreturned,
                "isExpired": isExpired,
            }
        )
    return render(
        request,
        "listIssuedBooks.html",
        {"issueBookDetails": issueBookDetails},
    )


def autoUpdatedIssueBookStatus():
    issuebooks = IssueBook.objects.filter(
        status="Unreturned", returnDate__lt=datetime.date(datetime.today())
    )
    issuebooks.update(status="Expired")


@login_required(login_url="/")
def updateIssueBookStatus(request, id):
    issuebook = IssueBook.objects.filter(id=id)
    if issuebook.first().status == "Pending":
        details = IssueBookDetail.objects.filter(issueBook=issuebook.first())
        for detail in details:
            book = Book.objects.filter(id=detail.book.id)
            book.update(quantity=book.first().quantity - 1)
        issuebook.update(status="Unreturned")
    elif issuebook.first().status == "Unreturned":
        issuebook.update(status="Returned")
    elif issuebook.first().status == "Expired":
        issuebook.update(status="ExpireReturned")
    return redirect("/view_issued_books/")


@login_required(login_url="/")
def listCustomers(request):
    customers = Customer.objects.all()
    return render(request, "listCustomers.html", {"customers": customers})


@login_required(login_url="/")
def lockCustomer(request, id):
    users = User.objects.filter(id=id)
    users.update(is_active=0)
    return redirect("/view_customers/")


@login_required(login_url="/")
def unlockCustomer(request, id):
    users = User.objects.filter(id=id)
    users.update(is_active=1)
    return redirect("/view_customers/")


def Login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/view_books")
            else:
                return redirect("/library")
        else:
            text = "Tên hoặc mật khẩu không hợp lệ."
            alert = True
            return render(request, "index.html", {"alert": alert, "text": text})
    return render(request, "index.html")


def Signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        fullName = request.POST["fullName"]
        sex = request.POST["sex"]
        pic = request.FILES["pic"]
        address = request.POST["address"]
        email = request.POST["email"]
        contact = request.POST["contact"]

        if password != confirm_password:
            passnotmatch = True
            return render(
                request, "customerRegistration.html", {"passnotmatch": passnotmatch}
            )

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
            )
            customer = Customer.objects.create(
                user=user,
                fullName=fullName,
                sex=sex,
                address=address,
                email=email,
                contact=contact,
                pic=pic,
            )
            user.save()
            customer.save()
        except:
            return render(request, "customerRegistration.html", {"alreadyExist": True})
        alert = True
        return render(request, "customerRegistration.html", {"alert": alert})
    return render(request, "customerRegistration.html")


@login_required(login_url="/")
def Profile(request):
    return render(request, "profile.html")


@login_required(login_url="/")
def editProfile(request):
    if request.method == "POST":
        fullName = request.POST["fullName"]
        sex = request.POST["sex"]
        address = request.POST["address"]
        email = request.POST["email"]
        contact = request.POST["contact"]

        current_user = request.user
        customer = Customer.objects.filter(user=current_user)
        customer.update(
            fullName=fullName,
            sex=sex,
            address=address,
            email=email,
            contact=contact,
        )
        alert = True
        return render(request, "editProfile.html", {"alert": alert})
    return render(request, "editProfile.html")


@login_required(login_url="/")
def changePassword(request):
    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "changePassword.html", {"alert": alert})
            else:
                currpasswrong = True
                return render(
                    request, "changePassword.html", {"currpasswrong": currpasswrong}
                )
        except:
            pass
    return render(request, "changePassword.html")


def Logout(request):
    logout(request)
    return redirect("/")
