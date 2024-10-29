from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import UserCreationForm


class UserEditForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Roles (Groups)"
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'groups']


class RoleEditForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
        labels = {
            'name': 'Role Name',
            'permissions': 'Assign Permissions'
        }

class RoleCreationForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
        labels = {
            'name': 'Role Name',
            'permissions': 'Assign Permissions'
        }


class RegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
