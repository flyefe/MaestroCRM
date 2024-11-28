import json, random, string
from django.db.models import Q
from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.paginator import Paginator


from .models import Segment
from .forms import SegmentForm

from contacts.models import ContactDetail
from contacts.forms import ContactDetailCreationForm, ContactFilterForm, ContactSearchForm

from core.decorators import role_required



@role_required(['Admin'])
@login_required
def create_segment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        conditions = json.loads(request.POST.get('conditions', '[]'))

        # Initialize the main Q object
        q = Q()

        # Variable to keep track of the current condition
        current_q = None

        for i, condition in enumerate(conditions):
            # Create a new Q object for each condition
            new_q = Q()
            
            if condition['type'] == 'status':
                if condition['operation'] == '=':
                    new_q &= Q(status=condition['value'])
                elif condition['operation'] == '!=':
                    new_q &= ~Q(status=condition['value'])
            elif condition['type'] == 'tag':
                if condition['operation'] == '=':
                    new_q &= Q(tags__name=condition['value'])
                elif condition['operation'] == '!=':
                    new_q &= ~Q(tags__name=condition['value'])
            
            # Logic for combining conditions
            if i == 0:
                # For the first condition, just set it as the current condition
                current_q = new_q
            else:
                # Combine with the previous condition based on the logic
                if condition['logic'] == 'and':
                    current_q &= new_q
                elif condition['logic'] == 'or':
                    current_q |= new_q

        # After the loop, current_q holds the combined query
        if current_q:
            q = current_q

        # Filter contacts based on the Q object
        filtered_contacts = ContactDetail.objects.filter(q)

        # Save the segment
        segment = Segment.objects.create(
            name=name,
            description=description,
            created_by=request.user,  # Assuming you have a `created_by` field in the Segment model
            created_at=now(),
            modified_at=now(),
            conditions=conditions,
            # additional_rules=conditions,
        )

        # Optional: Save filtered contacts to the segment if needed
        for contact in filtered_contacts:
            segment.contacts.add(contact)  # Assuming you have a ManyToMany relationship with contacts

        return redirect('segments:segment_list')  # Redirect to a segment list page or detail view after saving
    else:
        form = SegmentForm()

        context = {
            'form': form
        }

    return render(request, 'segments/create_segment.html', context)

# @login_required
# def create_segment(request):
#     if request.method == 'POST':
#         form = SegmentForm(request.POST)
#         conditions = request.POST.get('conditions')  # JSON data from the frontend

#         if form.is_valid():
#             segment = form.save(commit=False)
#             segment.conditions = conditions  # Save JSON conditions
#             segment.created_by = request.user
#             segment.save()
#             messages.success(request, "Segment created successfully.")
#             return redirect('segments:segment_list')
#     else:
#         form = SegmentForm()
#     return render(request, 'segments/create_segment.html', {'form': form})

@login_required
def segment_list(request):
    segments = Segment.objects.filter(created_by=request.user)
    return render(request, 'segments/segment_list.html', {'segments': segments})

@login_required
def segment_detail(request, pk):
    segment = get_object_or_404(Segment, pk=pk)
    # contacts = segment.get_contacts()
    contacts = segment.contacts.all()

    # Add pagination (Optional)
    paginator = Paginator(contacts, 5)  # Show 10 contacts per page
    page_number = request.GET.get('page')
    page_contacts = paginator.get_page(page_number)

    form = ContactDetailCreationForm
    filter_form = ContactFilterForm
    search_form = ContactSearchForm

    context = {
        'segment': segment,
        'contacts': page_contacts,
        'form': form,
        'filter_form': filter_form,
        'search_form' : search_form
    }
    return render(request,'segments/segment_detail.html', context)
