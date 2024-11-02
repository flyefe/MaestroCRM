from django import forms
from django.contrib.auth.models import User
from .models import ContactDetail

# forms.py
from django import forms
from .models import Status

# class StatusForm(forms.ModelForm):
#     class Meta:
#         model = Status
#         fields = ['name']

# class ContactDetailCreationForm(forms.ModelForm):
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(max_length=30)
#     last_name = forms.CharField(max_length=150)
    
#     class Meta:
#         model = ContactDetail
#         fields = ['status', 'tags', 'assigned_staff']  # Fields from ContactDetail

#     def save(self, commit=True):
#         # Create user associated with the contact
#         email = self.cleaned_data['email']
#         user = User(
#             username=email,  # username set to blank
#             email=email,
#             first_name=self.cleaned_data['first_name'],
#             last_name=self.cleaned_data['last_name']
#         )
        
#         if commit:
#             user.set_unusable_password()  # Ensures user will need to reset password
#             user.save()

#             # Create the ContactDetail profile and link to user
#             contact_profile = super().save(commit=False)
#             contact_profile.user = user
#             contact_profile.save()
#         return contact_profile
    

class ContactDetailCreationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    
    class Meta:
        model = ContactDetail
        fields = ['status', 'tags', 'assigned_staff']  # Fields from ContactDetail

    def save(self, commit=True):
        email = self.cleaned_data['email']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']

        # Check if an associated user already exists
        contact_detail = super().save(commit=False)
        user = contact_detail.user  # Get the associated User, if any

        if user is None:
            # If no associated user, create a new one
            user = User(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.set_unusable_password()  # Ensures user will need to reset password
        else:
            # Update the existing user's details
            user.email = email
            user.first_name = first_name
            user.last_name = last_name

        if commit:
            user.save()  # Save the User instance
            contact_detail.user = user
            contact_detail.save()  # Save the ContactDetail instance

        return contact_detail

