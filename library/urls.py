from django.urls import path
from . import views


# URL CONFIG
urlpatterns = [
    path("", views.Login, name="index"),
    path("view_publishers/", views.listPublishers, name="view_publishers"),
    path("add_publisher/", views.addPublisher, name="add_publishers"),
    path("update_publisher/<int:id>/", views.updatePublisher, name="update_publisher"),
    path("delete_publisher/<int:id>/", views.deletePublisher, name="delete_publisher"),
    path("view_bookgenres/", views.listBookGernes, name="view_bookgenres"),
    path("add_bookgenre/", views.addBookGenre, name="add_bookgenre"),
    path("update_bookgenre/<int:id>/", views.updateBookGenre, name="update_bookgenre"),
    path("delete_bookgenre/<int:id>/", views.deleteBookGerne, name="delete_bookgenre"),
    path("view_books/", views.listBooks, name="view_books"),
    path("add_book/", views.addBook, name="add_book"),
    path("update_book/<int:id>/", views.updateBook, name="update_book"),
    path("delete_book/<int:id>/", views.deleteBook, name="delete_book"),
    path("view_customers/", views.listCustomers, name="view_customers"),
    path("lock_customer/<int:id>/", views.lockCustomer, name="lock_customer"),
    path("unlock_customer/<int:id>/", views.unlockCustomer, name="unlock_customer"),
    path("view_issued_books/", views.listIssuedBooks, name="view_issued_books"),
    path(
        "update_issue_book/<int:id>/",
        views.updateIssueBookStatus,
        name="update_issue_book",
    ),
    path("signup/", views.Signup, name="signup"),
    path("profile/", views.Profile, name="profile"),
    path("edit_profile/", views.editProfile, name="edit_profile"),
    path("change_password/", views.changePassword, name="change_password"),
    path("logout/", views.Logout, name="logout"),
    path("library/", views.Library, name="library"),
    path("issue_book/<int:id>/", views.issueBook, name="issue_book"),
    path("submit_issue_book/", views.submitIssueBook, name="submit_issue_book"),
    path(
        "delete_issuedetail/<int:id>/",
        views.deleteIssueBookDetail,
        name="delete_issuedetail",
    ),
    path(
        "customer_issued_books/",
        views.listCustomerIssuedBooks,
        name="customer_issued_books",
    ),
]
