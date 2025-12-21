from django.urls import path

from accounts.views import index, WorkerListView

app_name = "accounts"


urlpatterns = [
    path("", index, name="index"),
    path("staff/", WorkerListView.as_view(), name="staff-list"),
    ]