from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminUserCreationForm
from accounts.models import CustomUser


class CustomUserCreationForm(AdminUserCreationForm):
    """
    Custom admin panel for operating accounts
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "role", "mechanic_position")

    def clean(self):
        """
        Custom validation during creating User
        :return:
        """
        cleaned = super().clean()
        role = cleaned.get("role")
        pos = cleaned.get("mechanic_position")

        if role == CustomUser.Role.MANAGER:
            cleaned["mechanic_position"] = ""
            return cleaned

        if role == CustomUser.Role.MECHANIC and not pos:
            self.add_error("mechanic_position", "You must specify mechanic position")

        return cleaned


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"
