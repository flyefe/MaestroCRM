from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from.forms import SignupForm 
from .models import Userprofile

from team.models import Team

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)     
        if form.is_valid():
            user = form.save()
            Userprofile.objects.create(user=user)
            
            # team = Team.objects.create(name='The team name', created_by=user)
            # team.members.add(user)
            # team.save()

            return redirect('/log-in/')
    else:
        form = SignupForm()

    return render(request, 'userprofile/signup.html', {
        'form': form
    })


@login_required
def myaccount(request):
    team = Team.objects.filter(created_by=request.user).first()
    user = request.user
    teams = user.teams.all()
    team_members = team.members.all() if team else []


    return render(request, 'userprofile/myaccount.html', {
        'team' : team,
        'teams' : teams,
        'team_members' : team_members
    })



@login_required
def error(request):

    return render(request, 'userprofile/error.html')