from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from newapp.forms import UserForm, ProfileForm, TodoForm
from newapp.models import DashboardImage, Profile,Todo


def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, 'User registered successfully!')
        return redirect('login')
    return render(request, 'newapp/register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('create_todo')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')
    return render(request, 'newapp/login.html')

def show_context(request):
    if request.user.is_superuser:
        users = User.objects.all()
    else:
        users = User.objects.filter(id=request.user.id)
    registered_users = {
        user.id: {
            'username': user.username,
            'email': user.email if user.email else 'N/A' ,
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M')
        }
        for user in users
    }
    context = {'registered_users': registered_users,'is_admin': request.user.is_superuser}
    return render(request, 'newapp/context.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    users = User.objects.all()

    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            DashboardImage.objects.create(image=image)
            messages.success(request, 'Image uploaded successfully!')
            return redirect('dashboard')
    images = DashboardImage.objects.all().order_by('-uploaded_at')

    return render(request, 'newapp/dashboard.html', {
        'users': users,
        'images': images
    })
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not request.user.is_superuser and  user != request.user:
        messages.error(request, 'You dont have permission to delete user')
        return redirect('show_context')
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('show_context')

@login_required
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not request.user.is_superuser and  user != request.user:
        messages.error(request, 'You dont have permission to update user')
        return redirect('show_context')
    if request.method == 'POST':
        new_password = request.POST['password']
        user.set_password(new_password)
        user.save()
        messages.success(request, 'Password updated successfully!')
        if request.user == user:
            update_session_auth_hash(request, user)
        return redirect('show_context')
    return render(request, 'newapp/update.html', {'user': user})

# @login_required
# def user_profile(request):
#     user = request.user
#     profile, created = Profile.objects.get_or_create(user=user)
#
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=user)
#         profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user_obj = user_form.save(commit=False)
#             password = user_form.cleaned_data.get('password')
#             if password:
#                 user_obj.set_password(password)
#             user_obj.save()
#             profile_form.save()
#             update_session_auth_hash(request, user_obj)
#             messages.success(request, 'Profile updated successfully!')
#             return redirect('user_profile')
#     else:
#         user_form = UserForm(instance=user)
#         profile_form = ProfileForm(instance=profile)
#
#     return render(request, 'newapp/profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'profile': profile
#     })

@login_required
def todo_list(request):
    if request.user.is_superuser:
        todos = Todo.objects.all()
    else:
        todos = Todo.objects.filter(user=request.user)
    return render(request, 'newapp/todo_list.html', {'todos': todos})

@login_required
def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Todo created successfully!')
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'newapp/create_todo.html', {'form': form})


@login_required
def update_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    if not request.user.is_superuser and todo.user != request.user:
        messages.error(request, "You don't have permission to edit this todo.")
        return redirect('todo_list')
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)         #initialize the form with existing data
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo updated successfully!')
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'newapp/create_todo.html', {'form': form, 'todo': todo})

@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    if not request.user.is_superuser and todo.user != request.user:
        messages.error(request, "You don't have permission to delete this todo.")
        return redirect('todo_list')

    todo.delete()
    messages.success(request, 'Todo deleted successfully!')
    return redirect('todo_list')