import re
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .forms import ContactDetailCreationForm
from .models import ContactDetail
from django.contrib.auth.decorators import login_required
# from .forms import StatusForm, Status



# Create your views here.



@login_required
def update_contact_detail(request, contact_id):
    contact = get_object_or_404(ContactDetail, id=contact_id)
    user = contact.user
    
    if request.method == 'POST':
        form = ContactDetailCreationForm(request.POST, instance=contact)
        if form.is_valid():
            email = form.cleaned_data['email']

             # Check if the email has been changed and if it exists for another user
            if email != user.email and User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already used for another contact.')
                return render(request, 'contact/update_contact_detail.html', {'form': form})
            
            # Save the user and contact details
            form.save()
            messages.success(request, 'Contact details updated successfully.')
            return redirect('contact_list')
    else:
        form = ContactDetailCreationForm(instance=contact, initial={
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })

    return render(request, 'contact/update_contact_detail.html', {'form': form})


def contact_detail(request, contact_id):
    contact = get_object_or_404(ContactDetail, id=contact_id)
    context = {
        'contact': contact,
    }
    return render(request, 'contact/contact_detail.html', context)

@login_required
def delete_contact(request, contact_id):
     # Check if the user has permission to delete a group
    if not request.user.has_perm('auth.delete_user'):  # Explicitly check for the 'delete group' permission
        messages.error(request, "You do not have permission to delete contact.")
        return redirect('contact_detail')  # Redirect to an appropriate page


    #get contact
    contact = get_object_or_404(ContactDetail, id=contact_id)
    
    #Delete Contact
    contact.delete()
    messages.success(request, f"'{contact.user.first_name}' has been successfully deleted")
    return redirect('contact_list')

@login_required
def add_contact_detail(request):
    if request.method == 'POST':
        form = ContactDetailCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            #check if the user with the same email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'A user with this email already exists.')
                return render(request, 'contact/add_contact_detail.html', {'form': form})
            
            #if no existing user, save the form
            form.save()
            messages.success(request, 'New contact detail created successfully.')
            return redirect('contact_list')
    else:
        form = ContactDetailCreationForm()

    return render(request, 'contact/add_contact_detail.html', {'form': form})

@login_required
def contact_list(request):
    contacts = ContactDetail.objects.select_related('user').all()  # Retrieves Profile and related User data in a single query
    context = {'contacts': contacts}
    return render(request, 'contact/contact_list.html', context)