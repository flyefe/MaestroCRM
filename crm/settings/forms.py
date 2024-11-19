from django import forms
from .models import Status, Service, TrafickSource

class UpdateSettingsForm(forms.Form):
    statuses = forms.CharField(
        label="Statuses (comma-separated):",
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., "new", "old", "paid"',
            'class': 'form-input block w-full rounded border border-black p-2 mb-2',
            'style': 'background-color: #f5f5f5;'
        }),
        required=False,
    )
    services = forms.CharField(
        label="Services (comma-separated):",
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., "Consulting", "Development"',
            'class': 'form-input block w-full rounded border border-black p-2 mb-2',
            'style': 'background-color: #f5f5f5;'
        }),
        required=False,
    )
    traffic_sources = forms.CharField(
        label="Traffic Sources (comma-separated):",
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., "Google", "Referral"',
            'class': 'form-input block w-full rounded border border-black p-2 mb-2',
            'style': 'background-color: #f5f5f5;'
        }),
        required=False,
    )
