import re
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import ContactDetailCreationForm
from .models import ContactDetail
from django.contrib.auth.decorators import login_required
# from .forms import StatusForm, Status



# Create your views here.


@login_required
def update_contact_detail(request, contact_id):
    # Retrieve the ContactProfile by ID and associated User
    contact = get_object_or_404(ContactDetail, id=contact_id)
    user = contact.user  # Access the linked User instance
    
    if request.method == 'POST':
        form = ContactDetailCreationForm(request.POST, instance=contact)
        if form.is_valid():
            # Update user details
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            # user.username = ''  # Ensure username stays blank
            user.save()  # Save the User instance

            # Save the ContactProfile instance
            form.save()
            messages.success(request, 'Contact details updated successfully.')
            return redirect('contact_list')  # Redirect to the profile list or any relevant page
    else:
        # Pre-populate the form with existing ContactProfile and User data
        form = ContactDetailCreationForm(instance=contact, initial={
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })
    
    return render(request, 'contact/update_contact_detail.html', {'form': form})

@login_required
def contact_list(request):
    contacts = ContactDetail.objects.select_related('user').all()  # Retrieves Profile and related User data in a single query
    context = {'contacts': contacts}
    return render(request, 'contact/contact_list.html', context)


def add_contact_detail(request):
    if request.method == 'POST':
        form = ContactDetailCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New contact Detail created successfully.')
            return redirect('contact_list')  # Redirect to a list view or another relevant page
    else:
        form = ContactDetailCreationForm()

    return render(request, 'contact/add_contact_Detail.html', {'form': form})

# from django.contrib.auth.models import User
# from django.db import IntegrityError

# @login_required
# def add_contact_detail(request):
#     if request.method == 'POST':
#         form = ContactDetailCreationForm(request.POST)
#         if form.is_valid():
#             try:
#                 # Create the User instance with username set to email
#                 email = form.cleaned_data['email']
#                 user = User.objects.create(
#                     email=email,
#                     first_name=form.cleaned_data['first_name'],
#                     last_name=form.cleaned_data['last_name'],
#                     username=email  # Set username to email during creation
#                 )
#                 user.save()

#                 # Create the ContactProfile linked to the user
#                 contact = form.save(commit=False)
#                 contact.user = user
#                 contact.save()

#                 messages.success(request, 'New contact created successfully.')
#                 return redirect('contact_list')
#             except IntegrityError:
#                 messages.error(request, 'A contact with this email already exists.')
#     else:
#         form = ContactDetailCreationForm()

#     return render(request, 'contact/add_contact_detail.html', {'form': form})
