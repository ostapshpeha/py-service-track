from django.urls import path

from accounts.views import index, CustomUserListView

app_name = "accounts"


urlpatterns = [
    path("", index, name="index"),
    path("staff/", CustomUserListView.as_view(), name="staff-list"),
    ]