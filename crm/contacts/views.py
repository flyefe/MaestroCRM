import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactDetailCreationForm
from .models import ContactDetail
from django.contrib.auth.decorators import login_required
# from .forms import StatusForm, Status



# Create your views here.




# def add_status(request):
#     if request.method == 'POST':
#         form = StatusForm(request.POST)
#         if form.is_valid():
#             statuses_input = form.cleaned_data['statuses']
#             statuses_list = re.findall(r'"(.*?)"', statuses_input)  # Extract quoted values

#             # Clear the previous statuses
#             Status.objects.all().delete()

#             # Save new statuses
#             for status in statuses_list:
#                 if status:
#                     Status.objects.create(name=status.strip())  # Create new status

#             messages.success(request, 'Statuses added successfully.')
#             return redirect('add_contact')  # Redirect to the list of statuses or any desired page
#     else:
#         form = StatusForm()  # Instantiate the form if not a POST request

#     return render(request, 'contact/add_status.html', {'form': form})  # Pass the form to the template

# def add_status(request):
#     if request.method == 'POST':
#         form = StatusForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Status added successfully.')
#             return redirect('add_contact')  # Redirect to a status list page or any relevant page
#     else:
#         form = StatusForm()
#     return render(request, 'contact/add_status.html', {'form': form})


# def add_status(request):
#     if request.method == 'POST':
#         statuses_input = request.POST.get('statuses')
#         if statuses_input:
#             # Use regex to find all quoted substrings
#             statuses_list = re.findall(r'"(.*?)"', statuses_input)
            
#             # Clear the previous statuses
#             Status.objects.all().delete()
            
#             # Save new statuses
#             for status in statuses_list:
#                 # Only create if the status name is not empty
#                 if status:
#                     Status.objects.create(name=status.strip())
                    
#             messages.success(request, 'Statuses added successfully.')
#             return redirect('add_contact')  # Redirect to a status list page or any relevant page
#     return render(request, 'contact/add_status.html')



@login_required
def contact_list(request):
    contacts = ContactDetail.objects.select_related('user').all()  # Retrieves Profile and related User data in a single query
    context = {'contacts': contacts}
    return render(request, 'contact/contact_list.html', context)


def add_contact_Detail(request):
    if request.method == 'POST':
        form = ContactDetailCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New contact Detail created successfully.')
            return redirect('contact_list')  # Redirect to a list view or another relevant page
    else:
        form = ContactDetailCreationForm()

    return render(request, 'contact/add_contact_Detail.html', {'form': form})
