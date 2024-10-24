from django import forms
from .models import Team


from django.contrib.auth.models import User

class UserSearchForm(forms.Form):
    query = forms.CharField(label='Search Users', max_length=100)


class AddTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'name',
        ]
        # Remove readonly_fields if it's not needed
