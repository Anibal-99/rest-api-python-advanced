from django.urls import path
from user.views import CreateUserView, ListUserView

app_name = "user"
urlpatterns = [
    path("", CreateUserView.as_view(), name="create_user"),
    path("list/", ListUserView.as_view(), name="list_user"),
]
