import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactDetail
from .forms import ContactImportForm

def import_contacts(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            # Step 1: Handle CSV Upload
            csv_file = request.FILES['file']
            try:
                # Read CSV file
                file_data = csv_file.read().decode("utf-8-sig").splitlines()
                reader = csv.DictReader(file_data)
                # Extract headers from CSV
                headers = reader.fieldnames

                # Save headers temporarily in the session for later mapping
                request.session['csv_headers'] = headers
                request.session['csv_data'] = [row for row in reader]
                return redirect('map_fields')

            except Exception as e:
                messages.error(request, f"Error processing the file: {e}")
                return redirect('import_contacts')
        else:
            form = ContactDetailImportForm()
            return render(request, 'import_contacts.html', {'form': form})

    else:
        form = ContactDetailImportForm()
    return render(request, 'import_contacts.html', {'form': form})

def map_fields(request):
    # Step 2: Display CSV headers for mapping
    if 'csv_headers' not in request.session:
        return redirect('import_contacts')

    csv_headers = request.session['csv_headers']
    contact_fields = [field.name for field in ContactDetail._meta.get_fields()]  # Get all model fields

    # Step 3: Create the mapping form dynamically
    mapping_fields = []
    for header in csv_headers:
        mapping_fields.append((header, forms.ChoiceField(choices=[(field, field) for field in contact_fields], required=False)))
    
    # Dynamically create a form class
    class FieldMappingForm(forms.Form):
        for header, field in mapping_fields:
            locals()[header] = field
    
    form = FieldMappingForm()

    return render(request, 'map_fields.html', {'form': form, 'csv_headers': csv_headers})

def save_mapped_data(request):
    if 'csv_data' not in request.session or 'csv_headers' not in request.session:
        return redirect('import_contacts')

    csv_data = request.session['csv_data']
    header_mapping = {header: request.POST.get(header) for header in request.session['csv_headers']}
    
    # Save contacts based on the mapping
    for row in csv_data:
        contact_data = {}
        for csv_column, model_field in header_mapping.items():
            if model_field:
                contact_data[model_field] = row.get(csv_column)
        
        ContactDetail.objects.create(**contact_data)

    messages.success(request, 'ContactDetails imported successfully.')
    return redirect('contact_list')
