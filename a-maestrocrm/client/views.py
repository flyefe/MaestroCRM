from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import UpdateView, CreateView
from django.views import View
from django.http import HttpResponseForbidden


from django.contrib import messages
from django.urls import reverse_lazy, reverse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .models import Client, ClientComment
from .forms import AddClientForm, AddCommentForm
from team.models import Team
# from lead.models import Lead




class CommentEditView(UpdateView):
    model = ClientComment
    form_class = AddCommentForm
    template_name = 'client/edit_comment.html'

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        team = comment.team

        # Check if the logged-in user is a member of the team
        if not team.members.filter(id=request.user.id).exists():
            return HttpResponseForbidden("You are not allowed to edit this comment.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Comment updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the comment. Please try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('clients:detail', kwargs={'pk': self.object.client.pk})



class CommentDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ClientComment
    success_message = "%(content)s has been deleted."

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        team = comment.team

        # Check if the logged-in user is a member of the team
        if not team.members.filter(id=request.user.id).exists():
            return HttpResponseForbidden("You are not allowed to delete this comment.")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return ClientComment.objects.filter()
    
    def get_success_url(self):
        client_pk = self.object.client.pk
        return reverse_lazy('clients:detail', kwargs={'pk': client_pk})
    
    def get_success_message(self, cleaned_data):
        return f"Comment by {self.object.created_by} has been deleted."
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, self.get_success_message(None))
        return super().delete(request, *args, **kwargs)


class ClientDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clients:list')
    success_message = "%(first_name)s has been deleted."

    def dispatch(self, request, *args, **kwargs):
        client = self.get_object()
        team = client.team

        # Check if the logged-in user is a member of the team
        if not team.members.filter(id=request.user.id).exists():
            return HttpResponseForbidden("You are not allowed to delete this client.")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Client.objects.filter()
    
    def get_success_message(self, cleaned_data):
        return f"{self.object.first_name} has been deleted."

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, self.get_success_message(None))
        return super().delete(request, *args, **kwargs)


@login_required
def edit_client(request, pk):
      # Get the client object
    client = get_object_or_404(Client, pk=pk)

    # Get the team associated with the client
    team = client.team

    # Check if the logged-in user is a member of the team
    if not team.members.filter(id=request.user.id).exists():
        return HttpResponseForbidden("You are cannont access this page because you are not a team member.")
    # client = get_object_or_404(Client, created_by=request.user, pk=pk)

    else:
        if request.method == 'POST':
            form = AddClientForm(request.POST, instance=client)

            if form.is_valid():
                form.save()

                messages.success(request, f"{client.first_name} has been edited successfully.")
                return redirect('clients:list')
        else:
            
            form = AddClientForm(instance=client)

            return render(request, 'client/edit_client.html', {
                'form': form
            })







@login_required
def client_detail(request, pk):
    # Get the client object
    client = get_object_or_404(Client, pk=pk)

    # Get the team associated with the client
    team = client.team

    # Check if the logged-in user is a member of the team
    if not team.members.filter(id=request.user.id).exists():
        return HttpResponseForbidden("You are cannont access this page because you are not a team member.")

    # Handle form submission
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.client = client  # Assign the comment to the client
            comment.save()
            return redirect('clients:detail', pk=pk)  # Redirect to the client detail page
    else:
        form = AddCommentForm()

    return render(request, 'client/client_detail.html', {
        'client': client,
        'form': form,
    })



@login_required
def client_list(request):
    user_team = Team.objects.filter(members=request.user).first()
    
    clients = Client.objects.filter(team=user_team)  # Fetch all clients without filtering by team

    return render(request, 'client/client_list.html', {
        'clients': clients,
    })

@login_required
def client_assigned(request):
    user_team = Team.objects.filter(members=request.user).first()
    
    clients = Client.objects.filter(team=user_team, assigned_to=request.user)  # Fetch all clients without filtering by team

    return render(request, 'client/client_assigned.html', {
        'clients': clients,
    })


@login_required
def add_client(request):
    
    # team=Team.objects.filter(created_by=request.user).first()members=request.user
    team=Team.objects.filter(members=request.user).first()

    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            team=Team.objects.filter(members=request.user).first()

            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()

            messages.success(
                request, f"{client.first_name} has been added successfully.")

            return redirect(
                'clients:list'
            )  # Redirect to a success page or another relevant page
    else:
        form = AddClientForm()

    return render(request, 'client/add_client.html', {
        'form': form,
        'team' : team
        })
