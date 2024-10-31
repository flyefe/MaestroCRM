# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import ContactDetail

class ContactDetailCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    
    class Meta:
        model = ContactDetail
        fields = ['status', 'tags', 'assigned_staff']  # Add any fields from ContactDetail

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        if commit:
            user.set_unusable_password()  # Ensures user will need to reset password
            user.save()
            contact_profile = super().save(commit=False)
            contact_profile.user = user
            contact_profile.save()
        return contact_profile
