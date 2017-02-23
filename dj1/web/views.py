from django.shortcuts import render, HttpResponse, Http404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from pprint import pprint

# Create your views here.

# @login_required
# def Home(request):
#     """Home Page"""
#     context={}
#     if request.GET.get('status') == 'login':
#         context['message'] = "Login Sucessful"
#     return render(request, 'home.html', context=context)

def Index(request):
    """ Main page """
    context={}

    if request.user.is_authenticated:
        if request.GET.get('status') == 'login':
            context['message'] = "Login Sucessful"
        return render(request, 'home.html', context=context)

    else:
        if request.GET.get('status') == "logout":
            context['message'] = ("Logout Successful")
        return render(request, 'landing.html', context=context)
