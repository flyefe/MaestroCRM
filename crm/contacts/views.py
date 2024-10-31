from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ContactDetailCreationForm

# Create your views here.


def add_contact_Detail(request):
    if request.method == 'POST':
        form = ContactDetailCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New contact Detail created successfully.')
            return redirect('contact_list')  # Redirect to a list view or another relevant page
    else:
        form = ContactDetailCreationForm()

    return render(request, 'add_contact_detail.html', {'form': form})
