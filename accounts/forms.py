from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AdminUserCreationForm
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div
from accounts.models import CustomUser



class CustomUserCreationForm(AdminUserCreationForm):
    """
    Custom admin panel for operating accounts
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "username", "first_name", "last_name",
            "email", "role", "mechanic_position"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='w-full md:w-1/2 px-2 mb-4'),
                Column('email', css_class='w-full md:w-1/2 px-2 mb-4'),
                css_class='flex flex-wrap -mx-2'
            ),
            Row(
                Column('first_name', css_class='w-full md:w-1/2 px-2 mb-4'),
                Column('last_name', css_class='w-full md:w-1/2 px-2 mb-4'),
                css_class='flex flex-wrap -mx-2'
            ),
            Row(
                Column('role', css_class='w-full md:w-1/2 px-2 mb-4'),
                Column('mechanic_position', css_class='w-full md:w-1/2 px-2 mb-4'),
                css_class='flex flex-wrap -mx-2'
            ),
            # Add password fields if present in form (UserCreationForm adds them)
            # We check if fields exist to avoid errors if form changes
            Row(
                Column('password_1', css_class='w-full md:w-1/2 px-2 mb-4'),
                Column('password_2', css_class='w-full md:w-1/2 px-2 mb-4'),
                css_class='flex flex-wrap -mx-2'
            ) if 'password_1' in self.fields else None,
            
            Submit('submit', 'Create User', css_class='w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4 transition duration-150')
        )
        # Remove None values from layout if conditional logic used
        # But Layout accepts None? No, it might crash.
        # Better to add them conditionally.
        
        # Simpler approach:
        common_layout = [
            Row(
                Column('username', css_class='w-full md:w-1/2 px-2 mb-4'),
                Column('email', css_class='w-full md:w-1/2 px-2 mb-4'),
                css_class='flex flex-wrap -mx-2'
            ),
            Row(
                Column('first_name', css_class='w-full md:w-1/2 px-2 mb-4'),
                Column('last_name', css_class='w-full md:w-1/2 px-2 mb-4'),
                css_class='flex flex-wrap -mx-2'
            ),
            Row(
                Column('role', css_class='w-full md:w-1/2 px-2 mb-4'),
                Column('mechanic_position', css_class='w-full md:w-1/2 px-2 mb-4'),
                css_class='flex flex-wrap -mx-2'
            ),
        ]
        
        if 'password_1' in self.fields:
             common_layout.append(
                Row(
                    Column('password_1', css_class='w-full md:w-1/2 px-2 mb-4'),
                    Column('password_2', css_class='w-full md:w-1/2 px-2 mb-4'),
                    css_class='flex flex-wrap -mx-2'
                )
             )
        
        common_layout.append(
            Submit('submit', 'Create User', css_class='w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4 transition duration-150')
        )
        
        self.helper.layout = Layout(*common_layout)


    def clean(self):
        """
        Custom validation during creating User
        """
        cleaned = super().clean()
        role = cleaned.get("role")
        pos = cleaned.get("mechanic_position")

        if role == CustomUser.Role.MANAGER:
            cleaned["mechanic_position"] = ""
            return cleaned

        if role == CustomUser.Role.MECHANIC and not pos:
            self.add_error(
                "mechanic_position",
                "You must specify mechanic position"
            )

        return cleaned


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'mechanic_position',
            'is_active',
            'is_staff',
            'is_superuser',
            Submit('submit', 'Update User', css_class='w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4 transition duration-150')
        )
