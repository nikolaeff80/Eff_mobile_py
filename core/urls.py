from django.urls import path
from .views import auth, mock_resources, admin

urlpatterns = [
    # Auth
    path("register/", auth.RegisterView.as_view(), name="register"),
    path("login/", auth.LoginView.as_view(), name="login"),
    path("profile/", auth.ProfileView.as_view(), name="profile"),
    path("delete/", auth.DeleteAccountView.as_view(), name="delete-account"),

    # Mock resources
    path("books/", mock_resources.BooksListView.as_view(), name="books"),
    path("orders/", mock_resources.OrdersListView.as_view(), name="orders"),
]
