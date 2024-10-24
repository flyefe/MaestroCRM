from django import forms
from .models import Lead, LeadComment

class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('first_name', 'email', 'description', 'priority', 'status',)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = LeadComment
        fields = ('content',)

#         widgets = {
#             'comment': forms.Textarea(attrs={'class': 'form-control'}),
#         }
