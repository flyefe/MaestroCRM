
from django import forms
from django.contrib.auth.models import User
from .models import ContactDetail

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

        contact_detail = super().save(commit=False)

        # Create or update the associated user
        if not contact_detail.user_id:
            # Create a new user
            user = User(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.set_unusable_password()  # User needs to set a password later
            if commit:
                user.save()
                contact_detail.user = user  # Link the new user to contact detail
        else:
            # Update the existing user
            user = contact_detail.user
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            if commit:
                user.save()

        if commit:
            contact_detail.save()  # Save the ContactDetail instance

        return contact_detail