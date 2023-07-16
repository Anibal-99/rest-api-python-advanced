from django.urls import path
from user import views

app_name = "user"
urlpatterns = [
    path("", views.CreateUserView.as_view(), name="create_user"),
    path("login/", views.CreateTokenView.as_view(), name="login"),
    path("me/", views.ManageUserView.as_view(), name="me"),
]
