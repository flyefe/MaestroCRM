from django import forms
from django.contrib.auth.models import User, Group
from django.db.models import Q  # Import Q here
from .models import ContactDetail
from settings.models import TrafickSource, Service, Status

class ContactDetailCreationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label="First Name", required=True, widget=forms.TextInput(attrs={
        'class': 'form-input block w-full rounded border-gray-300',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=30, label="Last Name", required=True, widget=forms.TextInput(attrs={
        'class': 'form-input block w-full rounded border-gray-300',
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(attrs={
        'class': 'form-input block w-full rounded border-gray-300',
        'placeholder': 'Email'
    }))

    class Meta:
        model = ContactDetail
        fields = ['first_name', 'last_name', 'email', 'status', 'tags', 'assigned_staff', 
                  'phone_number', 'trafick_source', 'services']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select block w-full rounded border-gray-300'}),
            'tags': forms.TextInput(attrs={'class': 'form-input block w-full rounded border-gray-300'}),
            'assigned_staff': forms.Select(attrs={'class': 'form-select block w-full rounded border-gray-300'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input block w-full rounded border-gray-300'}),
            'open_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input block w-full rounded border-gray-300'}),
            'close_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input block w-full rounded border-gray-300'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Restrict the assigned_staff choices to only staff, admin, or users in a specific group
        specific_group = Group.objects.get(name="Staff")  # Replace "YourGroupName" with your specific group name
        self.fields['assigned_staff'].queryset = User.objects.filter(
            Q(is_staff=True) | Q(groups=specific_group)
        ).distinct()

        # Disable the email field if it's included in the form for some reason
        if 'email' in self.fields:
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['email'].disabled = True




# from django import forms
# from django.contrib.auth.models import User, Group
# from .models import ContactDetail
# from django.db.models import Q  # Import Q here
# from settings.models import TrafickSource, Service, Status

# class ContactDetailCreationForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=30, label="First Name", required=True, widget=forms.TextInput(attrs={
#         'class': 'form-input block w-full rounded border-gray-300',
#         'placeholder': 'First Name'
#     }))
#     last_name = forms.CharField(max_length=30, label="Last Name", required=True, widget=forms.TextInput(attrs={
#         'class': 'form-input block w-full rounded border-gray-300',
#         'placeholder': 'Last Name'
#     }))
#     email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(attrs={
#         'class': 'form-input block w-full rounded border-gray-300',
#         'placeholder': 'Email'
#     }))

#     class Meta:
#         model = ContactDetail
#         fields = ['first_name', 'last_name', 'email', 'status', 'tags', 'assigned_staff', 
#                   'phone_number', 'trafick_source', 'services']
#         widgets = {
#             'status': forms.Select(attrs={'class': 'form-select block w-full rounded border-gray-300'}),
#             'tags': forms.TextInput(attrs={'class': 'form-input block w-full rounded border-gray-300'}),
#             'assigned_staff': forms.Select(attrs={'class': 'form-select block w-full rounded border-gray-300'}),
#             'phone_number': forms.TextInput(attrs={'class': 'form-input block w-full rounded border-gray-300'}),
#             'open_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input block w-full rounded border-gray-300'}),
#             'close_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input block w-full rounded border-gray-300'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         # Restrict the assigned_staff choices to only staff, admin, or users in a specific group
#         specific_group = Group.objects.get(name="Staff")  # Replace "YourGroupName" with your specific group name
#         self.fields['assigned_staff'].queryset = User.objects.filter(
#             models.Q(is_staff=True) | models.Q(groups=specific_group)
#         ).distinct()
