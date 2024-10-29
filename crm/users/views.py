from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group

from .forms import UserEditForm, RegisterForm, RoleCreationForm,RoleEditForm



#Edit group
@login_required
def edit_group(request, group_id):
    # Check if the user has the appropriate permissions
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to edit groups.")
        return redirect('create_group')  # Redirect to the list of groups or another preferred page

    # Fetch the group to be edited
    group = get_object_or_404(Group, id=group_id)
    
    if request.method == 'POST':
        form = RoleEditForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, f"Group '{group.name}' has been updated successfully.")
            return redirect('create_group')  # Redirect to a group list or desired page
    else:
        form = RoleEditForm(instance=group)

    return render(request, 'edit_role.html', {'form': form, 'group': group})


#Delete Group
@login_required
def delete_group(request, group_id):
    # Check if the user has the appropriate permissions
    if not request.user.is_superuser:  # or another permission check
        messages.error(request, "You do not have permission to delete groups.")
        return redirect('create_group')  # Redirect to a page that lists groups or any preferred page

    # Get the group to be deleted
    group = get_object_or_404(Group, id=group_id)

    # Delete the group and display a success message
    group.delete()
    messages.success(request, f"Group '{group.name}' has been deleted successfully.")
    return redirect('create_group')  # Redirect to the list of groups or another page


# group.users
@login_required
def users_in_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    users = group.user_set.all()  # Retrieve all users in the specified group

    context = {
        'group': group,
        'users': users
    }
    return render(request, 'users_in_group.html', context)

#Create Role
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



# Delete Users
@login_required
def delete_user(request, user_id):
    # Check if the user has the appropriate permissions
    if not request.user.is_superuser:  # or another permission check
        messages.error(request, "You do not have permission to delete users.")
        return redirect('user_list')  # Redirect to an appropriate page

    # Get the user to be deleted
    user = get_object_or_404(User, id=user_id)

    # Prevent the logged-in user from deleting themselves
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('user_list')

    # Delete the user and display a success message
    user.delete()
    messages.success(request, f"User {user.username} has been deleted successfully.")
    return redirect('user_list')  # Redirect to the list of users or another page



#Edit Users
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

#Users Table
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


#Logout
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')  # Redirect to login page after logout

# Login
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



#Register User
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



