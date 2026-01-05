from django.urls import path

from accounts.views import (
    CustomUserListView, DashboardView,
    CustomUserCreateView, CustomUserUpdateView
)

app_name = "accounts"


urlpatterns = [
    path("", DashboardView.as_view(), name="index"),
    path("staff/", CustomUserListView.as_view(), name="staff-list"),
    path("staff/create/", CustomUserCreateView.as_view(), name="staff-create"),
    path("staff/update/", CustomUserUpdateView.as_view(), name="staff-update"),
    ]
