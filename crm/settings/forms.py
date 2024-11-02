from django import forms
from django.contrib.auth.models import User
from .models import Status

# forms.py


class StatusForm(forms.Form):
    statuses = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': '"new", "old", "paid"',  # Placeholder text to guide users
            'required': 'required',  # Make the field required
        }),
        label="Statuses (enclose each value in quotes, separate with commas):"  # Custom label
    )
