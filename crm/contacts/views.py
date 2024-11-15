import re
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .forms import ContactDetailCreationForm, LogForm
from .models import ContactDetail, Log
from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.contrib.auth.hashers import make_password
import random
import string
from django.urls import reverse




# from .forms import StatusForm, Status


@login_required
def delete_log(request, log_id):

    log = get_object_or_404(Log, id=log_id)

    log.delete()

    contact_id = log.contact_id
    
    messages.success(request, f" Log has been successfully deleted.")
    return redirect ('contact_detail', contact_id)




@login_required
def update_log(request, log_id):
    log = get_object_or_404(Log, id=log_id)
    contact_id = log.contact_id

    if request.method == 'POST':
        form = LogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            messages.success(request, "Log updated successfully.")
            return redirect('contact_detail', contact_id=contact_id)
    else:
        # Populate form with current log details
        form = LogForm(instance=log)

    context = {
        'contact_id': contact_id,
        'form': form,
        'log_id': log_id
    }

    return render(request, 'contact/update_log.html', context)

@login_required
def update_contact(request, contact_id):
    contact = get_object_or_404(ContactDetail, id=contact_id)
    user = contact.user
    
    if request.method == 'POST':
        form = ContactDetailCreationForm(request.POST, instance=contact)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            # Check if the email has been changed
            if email != user.email:
                # Check if the new email already exists for another user
                if User.objects.filter(email=email).exclude(id=user.id).exists():
                    messages.error(request, 'This email is already in use by another contact.')
                    return render(request, 'contact/update_contact_detail.html', {'form': form})
            
            # Update user details first
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()  # Save user changes

            # Update contact details
            contact = form.save(commit=False)
            contact.updated_by = request.user
            contact.save()
            form.save_m2m()
            messages.success(request, 'Contact and user details updated successfully.')
            
            # Redirect to contact detail page
            return redirect(reverse('contact_detail', args=[contact.id]))
    else:
        # Populate the form with current contact details
        form = ContactDetailCreationForm(instance=contact, initial={
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })

    # If GET, display the form for editing
    return render(request, 'contact/update_contact_detail.html', {'form': form})



# def contact_detail(request, contact_id):
#     contact = get_object_or_404(ContactDetail, id=contact_id)
    
#     # Fetch recent activities (assuming Log model has a ForeignKey to ContactDetail)
#     recent_activities = contact.log.all().order_by('-created_at') [:3] # Last 5 logs as an example
#     logs = Log.objects.filter(contact=contact).order_by('-created_at') 

#     # Handle form submission --- Log Details
#     if request.method == 'POST':
#         form = LogForm(request.POST)
#         if form.is_valid():
#             # Save the log, associating it with the contact
#             log = form.save(commit=False)
#             log.contact = contact
#             log.created_by = request.user
#             log.save()
#             # Redirect to avoid resubmission on refresh
#             return redirect('contact_detail', contact_id=contact_id)
#     else:
#         form = LogForm()

#     context = {
#         'contact': contact,
#         'recent_activities': recent_activities,
#         'logs': logs,
#         'form': form,
#     }
#     return render(request, 'contact/contact_detail.html', context)



@login_required
def contact_detail(request, contact_id, log_id=None):
    contact = get_object_or_404(ContactDetail, id=contact_id)

    # Fetch recent activities (assuming Log model has a ForeignKey to ContactDetail)
    recent_activities = contact.log.all().order_by('-created_at')[:3]
    logs = Log.objects.filter(contact=contact).order_by('-created_at')

    # If log_id is provided, get the specific log and populate the form for editing
    form = LogForm()
    if log_id:
        log = get_object_or_404(Log, id=log_id)
        form = LogForm(instance=log)  # Populate the form with the current log details

    # Handle form submission for new logs
    if request.method == 'POST' and not log_id:
        form = LogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.contact = contact
            log.created_by = request.user
            log.save()
            messages.success(request, "Log added successfully.")
            return redirect('contact_detail', contact_id=contact_id)
    elif request.method == 'POST' and log_id:
        # Update the existing log
        form = LogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            messages.success(request, "Log updated successfully.")
            return redirect('contact_detail', contact_id=contact_id)

    context = {
        'contact': contact,
        'recent_activities': recent_activities,
        'logs': logs,
        'form': form,
        'log_id': log_id,  # Pass the log_id to identify the form in the template
    }
    return render(request, 'contact/contact_detail.html', context)



@login_required
def delete_contact(request, contact_id):
    # Check if the user has permission to delete a user (since deleting a contact also deletes the user)
    if not request.user.has_perm('auth.delete_user'):
        messages.error(request, "You do not have permission to delete contacts or associated user accounts.")
        return redirect('contact_list')  # Assuming you have a contact list view

    contact = get_object_or_404(ContactDetail, id=contact_id)
    
    # Check if the user is trying to delete their own contact
    if contact.user == request.user:
        messages.error(request, "You cannot delete your own contact.")
        return redirect('contact_detail', contact_id=contact.id)

    # Delete the contact first
    contact.delete()

    # Then delete the associated user
    user = contact.user
    user.delete()

    messages.success(request, f"Contact '{contact.user.first_name}' and associated user account have been successfully deleted.")
    return redirect('contact_list')  # Redirect to contact list or another appropriate page



@login_required
@transaction.atomic
def create_contact(request):
    if request.method == 'POST':
        form = ContactDetailCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

            try:
                # Attempt to get or create the user, which inherently checks for existence
                user, created = User.objects.get_or_create(
                    username=email,
                    defaults={
                        'email': email,
                        'first_name': form.cleaned_data['first_name'],
                        'last_name': form.cleaned_data['last_name'],
                    }
                )
                
                if not created:
                    messages.error(request, "A user with this email already exists.")
                    return render(request, 'contact/create_contact.html', {'form': form})
                
                # If we reach here, the user was created
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                user.set_password(make_password(password))
                user.save()    
                print(f"Password for {email} is: {password}")  # Log or send password

                # Add the user to the 'Contact' group
                contact_group = Group.objects.get(name='Contact')
                user.groups.add(contact_group)

                # Create the ContactDetail instance
                contact = form.save(commit=False)
                contact.user = user
                contact.created_by = request.user
                contact.updated_by = request.user
                contact.save()
                messages.success(request, "Contact created successfully.")
                return redirect('contact_list')

            except Exception as e:
                # Generic exception handling, you might want to be more specific
                messages.error(request, f"An error occurred: {str(e)}")
                return render(request, 'contact/create_contact.html', {'form': form})

    else:
        form = ContactDetailCreationForm()
    return render(request, 'contact/create_contact.html', {'form': form})
    
@login_required
def contact_list(request):
    contacts = ContactDetail.objects.select_related('user').all()  # Retrieves Profile and related User data in a single query
    context = {'contacts': contacts}
    return render(request, 'contact/contact_list.html', context)



