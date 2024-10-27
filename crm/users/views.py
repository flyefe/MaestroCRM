from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group

from .forms import UserEditForm, RegisterForm, RoleCreationForm

from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# views.py

@login_required
def users_in_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    users = group.user_set.all()  # Retrieve all users in the specified group

    context = {
        'group': group,
        'users': users
    }
    return render(request, 'users_in_group.html', context)

@login_required
def create_group(request):
    
    groups = Group.objects.all()

    if request.method == 'POST':
        form = RoleCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New role created successfully.')
            return redirect('create_group')  # Redirect to a page that lists groups or any desired page
    else:
        form = RoleCreationForm()

    context = {
        'form':form,
        'groups':groups
    }

    return render(request, 'create_role.html', context)



class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')  # Redirect to the user list page after deletion

    # Ensure that only the user or an admin can delete the account
    def test_func(self):
        user = self.get_object()
        return self.request.user == user or self.request.user.is_staff


def register_user(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            staff_group = Group.objects.get(name='Contact')
            user.groups.add(staff_group)
            messages.success(request, 'User registered successfully.')
            return redirect('user_list')  # Redirect to user list or any desired page
        else:
            messages.error(request, 'please correct the errors below.')
    else:
        form = RegisterForm()


    
    return render(request, 'register.html', {'form': form})


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User has been editted successfully.')
            return redirect('user_list')  # Redirect to a page that lists all users or any preferred page
    else:
        form = UserEditForm(instance=user)
    return render(request, 'edit_user.html', {'form': form, 'user': user})

@login_required
def users_table(request):
    users = User.objects.all()  # Fetch all users
    user_list = []  # This will hold user data with roles

    for user in users:
        groups = user.groups.all()  # Fetch all roles (groups) for each user
        user_list.append({
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'roles': [group.name for group in groups]  # Add roles (group names)
        })

    context = {
        'user_list': user_list
    }
    return render(request, 'user_list.html', context)


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
                    messages.success(request, 'Logged in successfully.')
                    return redirect(next_url)  # Redirect to the page the user was trying to access
                else:
                    messages.success(request, 'Logged in successfully.')
                    return redirect('/')  # Or use a default page like 'index'
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html', {'form': form})


