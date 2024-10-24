from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import UpdateView, CreateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.urls import reverse_lazy, reverse

from .models import Lead, LeadComment
from .forms import AddLeadForm, AddCommentForm

from django.contrib import messages
from django.utils import timezone
from client.models import Client, ClientComment
from team.models import Team


from django.core.exceptions import PermissionDenied




class CommentEditView(UpdateView):
    model = LeadComment
    form_class = AddCommentForm
    template_name = 'lead/edit_comment.html'

    def form_valid(self, form):
        messages.success(self.request, "Comment updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the comment. Please try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('leads:detail', kwargs={'pk': self.object.lead.pk})
    
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = LeadComment
    template_name = 'lead/comment_confirm_delete.html'
    
    def get_success_url(self):
            return reverse_lazy('leads:detail', kwargs={'pk': self.object.lead.pk})

    def get_object(self, queryset=None):
        # Retrieve the comment object using the primary key from the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(LeadComment, pk=pk)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.created_by != request.user:
            return self.handle_no_permission()
        return super().delete(request, *args, **kwargs)
    

class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        # Initialize the form with POST data
        form = AddCommentForm(request.POST)
        
        if form.is_valid():
            # Retrieve the team and create a new comment
            team = Team.objects.filter(members=request.user).first()
            if not team:
                messages.error(request, "You don't have a team assigned.")
                return redirect('leads:detail', pk=pk)
            
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()
            
            messages.success(request, "Comment added successfully.")
        else:
            # If form is not valid, send error messages
            messages.error(request, "There was an error with your comment submission. Please try again.")

        return redirect('leads:detail', pk=pk)



class ConvertToClientView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        team = Team.objects.filter(members=request.user).first()
        if not team:
                messages.error(request, "You don't have a team assigned.")
                return redirect('leads:detail', pk=pk)
        else:
            # Get the lead object
            lead = get_object_or_404(Lead, pk=pk)

            # Create a new Client object based on the Lead data
            client = Client.objects.create(
                first_name=lead.first_name,
                status='open',  # default to 'open'
                open_date=timezone.now(),
                assigned_to=request.user,
                traffic_source=lead.traffic_source if hasattr(lead, 'traffic_source') else '',
                converted_by=request.user,
                converted_at=timezone.now(),
                email=lead.email,
                created_by=request.user,
                team=team
            )

              # Transfer comments from Lead to Client
            lead_comments = LeadComment.objects.filter(lead=lead)
            for lead_comment in lead_comments:
                ClientComment.objects.create(
                    team=team,
                    client=client,
                    content=lead_comment.content,
                    created_by=lead_comment.created_by,
                    created_at=lead_comment.created_at
                )

            # Delete the lead after conversion
            lead.delete()

        # Show a success message and redirect
        messages.success(request, f"{client.first_name} has been converted to a Client! Update their details.")
        return redirect('clients:edit', pk=client.pk)

# class LeadUpdateView(LoginRequiredMixin, UpdateView):
#     model = Lead
#     form_class = AddLeadForm
#     template_name = 'lead/edit_lead.html'
#     success_url = reverse_lazy('leads:list')

#     def get_queryset(self):
#         return Lead.objects.filter(created_by=self.request.user)

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         messages.success(self.request, f"{self.object.first_name} has been edited successfully.")
#         return response
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['team'] = Team.objects.filter(created_by=self.request.user).first()
#         return context
    
class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    form_class = AddLeadForm
    template_name = 'lead/edit_lead.html'
    success_url = reverse_lazy('leads:list')

    def get_queryset(self):
        # Ensure that only leads created by the user are considered
        return Lead.objects.filter()

    def get_object(self, queryset=None):
        lead = super().get_object(queryset)
        
        # Get the user's team
        user_team = Team.objects.filter(members=self.request.user).first()

        # Check if the lead's team matches the user's team
        if lead.team != user_team:
            raise PermissionDenied("You do not have permission to edit this lead.")
        
        return lead

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"{self.object.first_name} has been edited successfully.")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = Team.objects.filter(members=self.request.user).first()
        return context
    

# class LeadDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
#     model = Lead
#     success_url = reverse_lazy('leads:list')
#     success_message = "%(first_name)s has been deleted."

#     def get_queryset(self):
#         return Lead.objects.filter(created_by=self.request.user)
    
#     def get_success_message(self, cleaned_data):
#         return f"{self.object.first_name} has been deleted."

#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         messages.success(self.request, self.get_success_message(None))
#         return super().delete(request, *args, **kwargs)

class LeadDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list')
    success_message = "%(first_name)s has been deleted."

    def get_queryset(self):
        # Ensure that only leads created by the user are considered
        return Lead.objects.filter()

    def delete(self, request, *args, **kwargs):
        lead = self.get_object()
        
        # Get the user's team
        user_team = Team.objects.filter(members=self.request.user).first()

        # Check if the lead's team matches the user's team
        if lead.team != user_team:
            raise PermissionDenied("You do not have permission to delete this lead.")

        # Proceed with deletion if the user is allowed
        messages.success(self.request, self.get_success_message(None))
        return super().delete(request, *args, **kwargs)
    
    def get_success_message(self, cleaned_data):
        return f"{self.object.first_name} has been deleted."
    

# class LeadDetailView(LoginRequiredMixin, DetailView):
#     model = Lead
#     success_url = reverse_lazy('leads:detail')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = AddCommentForm
#         return context


#     def get_object(self):
#         pk = self.kwargs.get("pk")
#         user_team = Team.objects.filter(members=self.request.user).first()
#         return get_object_or_404(Lead, pk=pk)
    
class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    success_url = reverse_lazy('leads:detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        return context

    def get_object(self):
        pk = self.kwargs.get("pk")
        user_team = Team.objects.filter(members=self.request.user).first()
        
        # Check if the lead exists and belongs to a team that includes the user
        lead = get_object_or_404(Lead, pk=pk)

        # Restrict access if the lead's team is not the user's team
        if lead.team != user_team:
            raise PermissionDenied("You do not have permission to view this lead.")

        return lead

    



class LeadListView(LoginRequiredMixin, ListView):
    model = Lead

    def get_queryset(self):
        user_team = Team.objects.filter(members=self.request.user).first()
        return Lead.objects.filter(team=user_team, convert_to_client=False)

class LeadAssignView(LoginRequiredMixin, ListView):
    model = Lead

    def get_queryset(self):
        user_team = Team.objects.filter(members=self.request.user, assign_to=self.request.user).first()
        return Lead.objects.filter(team=user_team, convert_to_client=False)





# class LeadCreateView(LoginRequiredMixin, CreateView):
#     model = Lead
#     form_class = AddLeadForm
#     template_name = 'lead/add_lead.html'
#     success_url = reverse_lazy('leads:list')
    
#     def form_valid(self, form):
#         # Get the team associated with the current user
#         team = Team.objects.filter(members=self.request.user).first()
        
#         # Assign the team and created_by fields to the lead instance
#         lead = form.save(commit=False)
#         lead.created_by = self.request.user
#         lead.team = team
#         lead.save()
        
#         # Add a success message
#         messages.success(self.request, f"{lead.first_name} has been added successfully.")
        
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get the context
#         context = super().get_context_data(**kwargs)
        
#         # Get the team associated with the current user
#         team = Team.objects.filter(created_by=self.request.user).first()
        
#         # Add the team object to the context
#         context['team'] = team
        
#         return context
    
class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    form_class = AddLeadForm
    template_name = 'lead/add_lead.html'
    success_url = reverse_lazy('leads:list')
    
    def form_valid(self, form):
        # Get the team associated with the current user as a member
        team = Team.objects.filter(members=self.request.user).first()
        
        # If the user is not a member of any team, return a forbidden response
        if not team:
            messages.error(self.request, "You are not a member of any team.")
            return self.form_invalid(form)
        
        # Assign the team and created_by fields to the lead instance
        lead = form.save(commit=False)
        lead.created_by = self.request.user
        lead.team = team
        lead.save()
        
        # Add a success message
        messages.success(self.request, f"{lead.first_name} has been added successfully.")
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        
        # Get the team associated with the current user as a member
        team = Team.objects.filter(members=self.request.user).first()
        
        # Add the team object to the context
        context['team'] = team
        
        return context