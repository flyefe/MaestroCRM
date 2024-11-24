def filter_contacts(queryset, filters):
    if 'status' in filters and filters['status']:
        queryset = queryset.filter(status=filters['status'])
    if 'tag' in filters and filters['tag']:
        queryset = queryset.filter(tags=filters['tag'])
    if 'assigned_staff' in filters and filters['assigned_staff']:
        queryset = queryset.filter(assigned_staff=filters['assigned_staff'])
    return queryset
