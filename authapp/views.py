from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SignUpForm, EditProfileForm

# Create your views here.

def index(request):
    return render(request, 'authapp/index.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ('You have been successfully logged in'))
            return redirect('home')
        else:
            messages.success(request, ('Error logging in - please try again'))
            return redirect('login')

    else:
        return render(request, 'authapp/login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out'))
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ('You have been successfully registered'))
            return redirect('home')

    else:
        form = SignUpForm()

    return render(request, 'authapp/register.html', {'form': form})

def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()            
            messages.success(request, ('You have successfully edited your profile'))
            return redirect('home')

    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'authapp/edit_profile.html', {'form': form})

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()  
            update_session_auth_hash(request, form.user)          
            messages.success(request, ('You have successfully changed your password'))
            return redirect('home')

    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'authapp/change_password.html', {'form': form})
