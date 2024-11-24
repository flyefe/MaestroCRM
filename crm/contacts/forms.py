from django import forms
from django.contrib.auth.models import User, Group
from django.db.models import Q  # Import Q here
from .models import ContactDetail, Log
from settings.models import TrafickSource, Service, Status,Tag


class ContactFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        empty_label="All Statuses",
        widget=forms.Select(attrs={"class": "text-sm border-gray-300 rounded py-2 px-3"})
    )
    tags = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        empty_label="All Tags",
        widget=forms.Select(attrs={"class": "text-sm border-gray-300 rounded py-2 px-3"})
    )
    services = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        required=False,
        empty_label="All Services",
        widget=forms.Select(attrs={"class": "text-sm border-gray-300 rounded py-2 px-3"})
    )
    trafick_source = forms.ModelChoiceField(
        queryset=TrafickSource.objects.all(),
        required=False,
        empty_label="All Traffic Sources",
        widget=forms.Select(attrs={"class": "text-sm border-gray-300 rounded py-2 px-3"})
    )

class ContactDetailCreationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label="First Name", required=True, widget=forms.TextInput(attrs={
        'class': 'form-input block w-full rounded border border-black p-2 mb-2',
        'style': 'background-color: #f5f5f5;',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=30, label="Last Name", required=True, widget=forms.TextInput(attrs={
        'class': 'form-input block w-full rounded border border-black p-2 mb-2',
        'style': 'background-color: #f5f5f5;',
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(attrs={
        'class': 'form-input block w-full rounded border border-black p-2 mb-2',
        'style': 'background-color: #f5f5f5;',
        'placeholder': 'Email'
    }))

    tag = forms.CharField(label="Tags", widget=forms.TextInput(attrs={
        'placeholder': 'Enter tags separated by commas',
        'class': 'form-input block w-full rounded border border-black p-2 mb-2',
        'style': 'background-color: #f5f5f5;',
    }),
        required=False,
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'p-2 border border-gray-300 rounded-lg bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-300'
        }),
        required=False,
        label="Assign Tags"
    )

    assigned_staff = forms.ModelChoiceField(
        queryset=User.objects.filter(Q(is_staff=True) | Q(groups__name="Staff")).distinct(),
        label="Assigned Staff",
        empty_label="Select Staff",
        to_field_name="id",  # This is important to keep the correct ID
        widget=forms.Select(attrs={
            'class': 'form-select block w-full rounded border border-black p-2 mb-2',
            'style': 'background-color: #f5f5f5;'
        }),
        required=False
    )

    class Meta:
        model = ContactDetail
        fields = ['first_name', 'last_name', 'email', 'status', 'tags', 'assigned_staff', 
                  'phone_number', 'trafick_source', 'services']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select block w-full rounded border border-black p-2 mb-2',
                'style': 'background-color: #f5f5f5;'
            }),
            # 'assigned_staff': forms.Select(attrs={
            #     'class': 'form-select block w-full rounded border border-black p-2 mb-2',
            #     'style': 'background-color: #f5f5f5;'
            # }),
            
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input block w-full rounded border border-black p-2 mb-2',
                'style': 'background-color: #f5f5f5;'
            }),

            'trafick_source': forms.Select(attrs={
                'class': 'form-select block w-full rounded border border-black p-2 mb-2',
                'style': 'background-color: #f5f5f5;'
            }),
            'services': forms.Select(attrs={
                'class': 'form-select block w-full rounded border border-black p-2 mb-2',
                'style': 'background-color: #f5f5f5;'
            }),
            'open_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'class': 'form-input block w-full rounded border border-black p-2 mb-2', 
                'style': 'background-color:#f5f5f5'
            }),
            'close_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'class': 'form-input block w-full rounded border border-black p-2 mb-2', 
                'style': 'background-color:#f5f5f5'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Restrict the assigned_staff choices to only staff, admin, or users in a specific group
        specific_group = Group.objects.get(name="Staff")  # Replace "YourGroupName" with your specific group name
        self.fields['assigned_staff'].queryset = User.objects.filter(
            Q(is_staff=True) | Q(groups=specific_group)
        ).distinct()
        self.fields['assigned_staff'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"


# class LogForm (forms.ModelForm):

#     class Meta:
#         model = Log
#         fields = ['log_title', 'log_type', 'log_description']
#         widget = {
#             'log_title': forms.TextInput(attrs={'class': 'form-input block w-full rounded border-gray-300'}),
#             'log_type': forms.Select(attrs={'class': 'form-select block w-full rounded border-gray-300'}),
#             'lod_description': forms.TextInput(attrs={'class': 'form-input block w-full rounded border-gray-300'}),
#         }

from django import forms
from .models import Log, User, ContactDetail

class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = [ 'log_type', 'log_title', 'log_description']
        labels = {
            'log_type': 'Log Type',
            'log_title': 'Log Title',
            'log_description': 'Description',
        }
        widgets = {
            'log_type': forms.Select(attrs={
                'class': 'form-select block w-full rounded border border-black p-2 mb-2',
                'style': 'background-color: #f5f5f5;'
            }),
            'log_title': forms.TextInput(attrs={
                'class': 'form-input block w-full rounded border border-black p-2 mb-2',
                'style': 'background-color: #f5f5f5;'
            }),
            'log_description': forms.Textarea(attrs={
                'class': 'form-textarea block w-full rounded border border-black p-2 mb-2',
                'style': 'background-color: #f5f5f5;',
                'rows': '4'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(LogForm, self).__init__(*args, **kwargs)
        # self.fields['contact'].queryset = ContactDetail.objects.all()
        # self.fields['created_by'].queryset = User.objects.all()