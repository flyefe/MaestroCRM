from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

from django.contrib import messages

from .models import Team
from .forms import AddTeamForm

from .forms import UserSearchForm



@login_required
def remove_team_member(request, user_id):
    team = Team.objects.filter(created_by=request.user).first()
    user = get_object_or_404(User, pk=user_id)

    # if team and user in team.members.all():
    #     team.members.remove(user)
    #     messages.success(request, f'{user.username} has been removed from the team.')
    # else:
    #     messages.error(request, 'User is not a member of the team or no team found.')
    if team:
        # Check if the user to be removed is the owner of the team
        if user == team.created_by:
            messages.error(request, "You cannot remove the team owner from the team.")
        elif user in team.members.all():
            team.members.remove(user)
            messages.success(request, f'{user.username} has been removed from the team.')
        else:
            messages.error(request, 'User is not a member of the team.')
    else:
        messages.error(request, 'No team found.')

    return redirect('userprofiles:myaccount')


@login_required
def add_team_member(request):
    form = UserSearchForm()
    team = Team.objects.filter(created_by=request.user).first()

    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            users = User.objects.filter(username__icontains=query) | User.objects.filter(email__icontains=query)
            return render(request, 'team/add_member.html', {
                    'form': form, 
                    'users': users, 
                    'team': team
                })
   
    # Fetch team members
    # team_members = team.members.all() if team else []

    return render(request, 'team/add_member.html', {
        'form': form, 
        'team': team
    })



@login_required
def add_member_to_team(request, user_id):
    user = User.objects.get(pk=user_id)
    new_team = Team.objects.filter(created_by=request.user).first()

    if new_team is None:
        messages.error(request, 'No team found to add members to.')
        return redirect('team:add_member')

    # Add the user to the new team
    if not new_team.members.filter(pk=user.id).exists():
        new_team.members.add(user)
        messages.success(request, f'{user.username} has been added to your team.')
    else:
        messages.info(request, f'{user.username} is already a member of this team.')

    return redirect('userprofiles:myaccount')





@login_required
def edit_team(request, pk):
    team = get_object_or_404(Team, created_by=request.user, pk=pk)
    if request.method == 'POST':
        form = AddTeamForm(request.POST, instance=team)

        if form.is_valid():
            form.save()

            messages.success(request,
                             f"{team.name} has been edited successfully.")
            return redirect('userprofiles:myaccount')
        else:
            messages.success(request, f" form is not valid")
            return render(request, 'team/edit_team.html', {
                'team': team,
                'form': form,
            })

    else:
        form = AddTeamForm(instance=team)
        return render(request, 'team/edit_team.html', {
            'team': team,
            'form': form
        })
