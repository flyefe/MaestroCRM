# import csv
# from django import forms
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import ContactDetail
# from .forms import ContactImportForm

# def import_contacts(request):
#     if request.method == 'POST':
#         if 'file' in request.FILES:
#             # Step 1: Handle CSV Upload
#             csv_file = request.FILES['file']
#             try:
#                 # Read CSV file
#                 file_data = csv_file.read().decode("utf-8-sig").splitlines()
#                 reader = csv.DictReader(file_data)
#                 # Extract headers from CSV
#                 headers = reader.fieldnames

#                 # Save headers temporarily in the session for later mapping
#                 request.session['csv_headers'] = headers
#                 request.session['csv_data'] = [row for row in reader]
#                 return redirect('map_fields')

#             except Exception as e:
#                 messages.error(request, f"Error processing the file: {e}")
#                 return redirect('import_contacts')
#         else:
#             form = ContactImportForm()
#             return render(request, 'import_contacts.html', {'form': form})

#     else:
#         form = ContactImportForm()
#     return render(request, 'import/import_contacts.html', {'form': form})

# def map_fields(request):
#     # Step 2: Display CSV headers for mapping
#     if 'csv_headers' not in request.session:
#         return redirect('import_contacts')

#     csv_headers = request.session['csv_headers']
#     contact_fields = [field.name for field in ContactDetail._meta.get_fields()]  # Get all model fields

#     # Step 3: Create the mapping form dynamically
#     mapping_fields = []
#     for header in csv_headers:
#         mapping_fields.append((header, forms.ChoiceField(choices=[(field, field) for field in contact_fields], required=False)))
    
#     # Dynamically create a form class
#     class FieldMappingForm(forms.Form):
#         for header, field in mapping_fields:
#             locals()[header] = field
    
#     form = FieldMappingForm()

#     return render(request, 'import/map_fields.html', {'form': form, 'csv_headers': csv_headers})

# def save_mapped_data(request):
#     if 'csv_data' not in request.session or 'csv_headers' not in request.session:
#         return redirect('import_contacts')

#     csv_data = request.session['csv_data']
#     header_mapping = {header: request.POST.get(header) for header in request.session['csv_headers']}
    
#     # Save contacts based on the mapping
#     for row in csv_data:
#         contact_data = {}
#         for csv_column, model_field in header_mapping.items():
#             if model_field:
#                 contact_data[model_field] = row.get(csv_column)
        
#         ContactDetail.objects.create(**contact_data)

#     messages.success(request, 'ContactDetails imported successfully.')
#     return redirect('contact_list')


import csv
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactDetail
from .forms import ContactImportForm


# View 1: Import CSV File
def import_contacts(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            # Step 1: Handle CSV Upload
            csv_file = request.FILES['file']
            try:
                # Read CSV file
                file_data = csv_file.read().decode("utf-8-sig").splitlines()
                reader = csv.DictReader(file_data)
                headers = reader.fieldnames

                # Save headers and data in session
                request.session['csv_headers'] = headers
                request.session['csv_data'] = list(reader)

                return redirect('map_fields')

            except Exception as e:
                messages.error(request, f"Error processing the file: {e}")
                return redirect('import_contacts')
        else:
            messages.error(request, "No file uploaded.")
            return redirect('import_contacts')

    else:
        form = ContactImportForm()

    return render(request, 'import/import_contacts.html', {'form': form})


# View 2: Map CSV Headers to ContactDetail Fields
def map_fields(request):
    if 'csv_headers' not in request.session:
        messages.error(request, "No CSV headers found. Please upload the file again.")
        return redirect('import_contacts')

    csv_headers = request.session['csv_headers']

    # Fetch all contact fields dynamically
    contact_fields = [field.name for field in ContactDetail._meta.get_fields()]

    # Step 3: Create the dynamic form for field mapping
    class FieldMappingForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for header in csv_headers:
                self.fields[header] = forms.ChoiceField(
                    choices=[('', '----')] + [(field, field) for field in contact_fields],
                    required=False,
                    label=header
                )

    if request.method == "POST":
        form = FieldMappingForm(request.POST)
        if form.is_valid():
            # Save mapping to session
            request.session['header_mapping'] = form.cleaned_data
            return redirect('save_mapped_data')

    else:
        form = FieldMappingForm()

    return render(request, 'import/map_fields.html', {'form': form, 'csv_headers': csv_headers})


# View 3: Save Mapped Data
def save_mapped_data(request):
    if 'csv_data' not in request.session or 'header_mapping' not in request.session:
        messages.error(request, "No mapping data found. Please re-upload the file.")
        return redirect('import_contacts')

    csv_data = request.session['csv_data']
    header_mapping = request.session['header_mapping']

    # Save contacts based on header mapping
    try:
        for row in csv_data:
            contact_data = {}
            for csv_column, model_field in header_mapping.items():
                if model_field:  # Skip unmapped fields
                    contact_data[model_field] = row.get(csv_column)

            ContactDetail.objects.create(**contact_data)

        # Clear session data
        del request.session['csv_data']
        del request.session['csv_headers']
        del request.session['header_mapping']

        messages.success(request, "ContactDetails imported successfully.")
        return redirect('contact_list')

    except Exception as e:
        messages.error(request, f"Error saving data: {e}")
        return redirect('import_contacts')
