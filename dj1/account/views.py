from django.shortcuts import render, HttpResponse, Http404, redirect
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from pprint import pprint
from .forms import *
from .utils import *
from django.contrib.auth.hashers import check_password
# Create your views here.

def RegistrationView(request):
    if request.user.is_authenticated:
        return redirect('/')
    current_form = None
    # context = {}
    if request.method == 'GET':
        current_form = RegistrationForm()
    if request.method == "POST":
        current_form = RegistrationForm(request.POST)
        if current_form.is_valid():
            if RegistrationUtil(current_form.cleaned_data):
                return redirect('/login/?status=registered')
    return render(request, "registration.html", context={"form":current_form})

def Login(request):
    """view to handle incoming login request"""
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        next = request.GET.get('next', '/')
    if request.method == "POST":
        next = request.GET.get('next', '/')
        user_email = request.POST['user_email']
        password = request.POST['password']
        user = authenticate(username=user_email, password=password)
        if user is not None:
            login(request, user)
            if next == '':
                return redirect('?status=login')
            return HttpResponseRedirect(next)
        else:
            error = 'Incorrect Email or Password'
            return render(request, 'login.html',
                          context={'error': error, 'next':next})
    else:
        return render(request, "login.html", {'next': next})

def Logout(request):
    """view to handle the incoming logout requst"""
    logout(request)
    return redirect('/landing/?status=logout')
    LogoutMessage="Logout Successful"
    return render(request, 'landing.html',
                  context={'message':LogoutMessage})

@login_required
def UpdateInfoView(request):
    context = None
    current_form = None

    user = User.objects.get(username = request.user.username)
    profile = UserProfile.objects.get(user=user)

    # user_email = forms.EmailField()
    # user_nicename = forms.CharField(max_length = 50)
    # user_url = forms.URLField(max_length=100)
    # display_name = forms.CharField(max_length=250)

    if request.method == 'GET':
        current_form = UpdateInfoForm(initial={'user_email':user.email, 'user_nicename':profile.user_nicename, 'display_name':profile.display_name, 'user_url':profile.user_url, 'display_name':profile.display_name})
    if request.method == 'POST':
        current_form = UpdateInfoForm(request.POST)
        if current_form.is_valid():
            if UpdateInfoUtil(current_form.cleaned_data, user):
                return redirect('/?status=user_info_updated')
    return render(request, "update_info.html", context={"form":current_form})

@login_required
def ChangePasswordView(request):
    context = None
    current_form = None
    if request.method == 'GET':
        current_form = ChangePasswordForm()
    if request.method == 'POST':
        current_form = ChangePasswordForm(request.POST)
        if current_form.is_valid():
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            confirm_new_password = request.POST['confirm_new_password']
            if new_password == old_password:
                return ('new password and old password can not be same')#error
            else:
                user = User.objects.get(username=request.user.username)
                DatabasePassword = request.user.password
                chk = check_password(password=old_password, encoded = DatabasePassword)
                if chk == True:
                    if ChangePasswordUtil(user=user, old_password=old_password, new_password=new_password, confirm_new_password=confirm_new_password) == True:
                        return redirect('/?status=password_changed')
                else:
                    return ('incorrect old password')
    return render(request, "change_password.html", context={"form":current_form})

@login_required
def ChangeUsernameView(request):
    context = None
    current_form = None
    user = User.objects.get(username = request.user.username)
    if request.method == 'GET':
        current_form = ChangeUsernameForm(initial={'user_email':user.email})
    if request.method == 'POST':
        current_form = ChangeUsernameForm(request.POST)
        if current_form.is_valid():
            new_username = request.POST['new_username']
            if new_username == user.username:
                return HttpResponse('New username can not be same as old username')
            elif ChangeUsernameUtil(user=user, new_username=new_username):
                return redirect('/?status=username_changed_updated')
            else:
                return HttpResponse('Server Error')
    return render(request, "change_username.html", context={"form":current_form})
