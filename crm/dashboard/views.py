from django.shortcuts import render

# Create your views here.
from django.db.models import Count
from contacts.models import ContactDetail

def dashboard(request):
    contacts = ContactDetail.objects.all()
    active_contacts_count = contacts.filter(status__name='Customer').count()
    unassigned_contacts_count = contacts.filter(assigned_staff__isnull=True).count()
    recent_contacts = contacts.order_by('-created_at')[:5]
    
    # Traffic source data for chart
    traffic_sources = contacts.values('traffic_source__name').annotate(count=Count('traffic_source')).order_by('-count')
    traffic_sources_data = {
        'labels': [ts['traffic_source__name'] for ts in traffic_sources],
        'values': [ts['count'] for ts in traffic_sources],
    }

    # Services breakdown
    services_breakdown = contacts.values('services__name').annotate(count=Count('services')).order_by('-count')

    context = {
        'contacts': contacts,
        'active_contacts_count': active_contacts_count,
        'unassigned_contacts_count': unassigned_contacts_count,
        'recent_contacts': recent_contacts,
        'traffic_sources': traffic_sources_data,
        'services_breakdown': {service['services__name']: service['count'] for service in services_breakdown},
    }
    return render(request, 'dashboard/dashboard.html', context)
