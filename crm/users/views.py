from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group


# views.py

@login_required
def users_table(request):
    users = User.objects.all()  # Fetch all users
    user_roles = []  # This will hold user data with roles

    for user in users:
        groups = user.groups.all()  # Fetch all roles (groups) for each user
        user_roles.append({
            'username': user.username,
            'email': user.email,
            'roles': [group.name for group in groups]  # Add roles (group names)
        })

    context = {
        'user_roles': user_roles
    }
    return render(request, 'users.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')  # Redirect to login page after logout

# Create your views here.
def login_view(request):

    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # return redirect('index')
                # Get the 'next' parameter from the query string
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)  # Redirect to the page the user was trying to access
                else:
                    return redirect('/')  # Or use a default page like 'index'
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html', {'form': form})


