from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
# from .models import UserDetails


class UserAdminCreationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """

    class Meta:
        model = get_user_model()
        fields = ['phone', 'name', 'address_city', 'address_road']

# class UserDetailForm(forms.ModelForm):
#     class Meta:
#         model = UserDetails
#         fields = '__all__'
#         exclude = ['user']