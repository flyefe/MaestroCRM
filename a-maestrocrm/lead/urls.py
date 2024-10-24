from django.urls import path

from . import views

app_name ='leads'

urlpatterns = [
    path('lead_list/', views.LeadListView.as_view(), name='list'),
    # path('add_lead/', views.add_lead, name='add'),
    path('add_lead/', views.LeadCreateView.as_view(), name='add'),
    path('add_comment/<int:pk>', views.AddCommentView.as_view(), name='comment'),
    path('lead/comment/<int:pk>/edit/', views.CommentEditView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),
    path('lead_detail/<int:pk>/', views.LeadDetailView.as_view(), name='detail'),
    path('delete_lead/<int:pk>/delete/', views.LeadDeleteView.as_view(), name='delete'),
    path('edit_lead/<int:pk>/edit/', views.LeadUpdateView.as_view(), name='edit'),
    path('<int:pk>/convert/', views.ConvertToClientView.as_view(), name='convert_to'),


]