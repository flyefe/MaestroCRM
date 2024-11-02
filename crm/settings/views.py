import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StatusForm
from .models import Status
from django.contrib.auth.decorators import login_required
# Create your views here.



def update_statuses(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            # Clear all existing statuses
            Status.objects.all().delete()

            # Split input by commas, strip whitespace, and remove duplicates
            status_list = form.cleaned_data['statuses'].split(',')
            unique_statuses = set(status.strip() for status in status_list if status.strip())

            # Add each status to the database
            for status_name in unique_statuses:
                Status.objects.create(name=status_name)

            messages.success(request, "Statuses updated successfully.")
            return redirect('add_contact')  # Replace with your redirect target
    else:
        form = StatusForm()

    return render(request, 'setting/update_statuses.html', {'form': form})