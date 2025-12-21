from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminUserCreationForm
from accounts.models import Worker


class WorkerCreationForm(AdminUserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = ("username", "first_name", "last_name", "email", "role", "mechanic_position")

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")
        pos = cleaned.get("mechanic_position")

        if role == Worker.Role.MANAGER:
            cleaned["mechanic_position"] = ""
            return cleaned

        if role == Worker.Role.MECHANIC and not pos:
            self.add_error("mechanic_position", "You must specify mechanic position")

        return cleaned


class WorkerChangeForm(UserChangeForm):
    class Meta:
        model = Worker
        fields = "__all__"
