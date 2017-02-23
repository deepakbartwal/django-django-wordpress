import requests
from pprint import pprint
import json
from django.contrib.auth.models import User
from core.models import *

REGISTER_URL = "http://localhost:8000/register-from-server/"
UPDATE_URL = "http://localhost:8000/update-from-server/"
CHANGE_PASSWORD_URL = "http://localhost:8000/change-password-from-server/"
CHANGE_USERNAME_URL = "http://localhost:8000/change-username-from-server/"

AUTH_TOKEN_URL = ""
#this is copied ... it will be different for different user. code may be written to get this.
#Here code si being written for test purpose.... so in actual implementation, authorization token has to be generated for every user with get request.
# AUTH_TOKEN = "383e0336efc1e4023240a4225b547ee2cef59dd7"
AUTH_TOKEN = "0ff2eb42e048d998567a744b90b86aad18daea97"

def RegisterToServer(user_nicename, display_name, user_email, username, user_url, password, confirm_password):
    r = requests.post(REGISTER_URL, data = {'user_nicename':user_nicename, 'display_name':display_name, 'user_email':user_email, 'username':username, 'user_url':user_url, 'password':password, 'confirm_password':confirm_password})
    if r.json()['status'] == True:
        return True
    return False

def UpdateToServer(username, user_email, user_nicename='', display_name='', user_url=''):
    # authentication token is required
    # r = requests.post(UPDATE_URL, data = {'username':user_nicename, 'password':password})
    # let us assume we have the authentication token
    auth_token = AUTH_TOKEN
    if User.objects.get(username=username):
        user = User.objects.get(username=username)
        if UserProfile.objects.get(user = user):
            p = UserProfile.objects.get(user = user)
            # profile = {}
            payload = {'user_email':user_email, 'user_nicename':user_nicename, 'display_name':display_name, 'user_url':user_url}
            headers = {"Authorization":"Token 0ff2eb42e048d998567a744b90b86aad18daea97", 'Content-type': 'application/json'}
            r = requests.post(UPDATE_URL, data=json.dumps(payload), headers=headers)
            if r.json()['status'] == True:
                return True
                user.email = user_email
                user.save()

                p.user_nicename = user_nicename
                p.display_name = display_name
                p.user_url = user_url
                p.save()
# write code for errors here

def ChangePasswordToServer(username, old_password, new_password, confirm_new_password):
    auth_token = AUTH_TOKEN
    if User.objects.get(username=username):
        user = User.objects.get(username=username)
        if UserProfile.objects.get(user = user):
            p = UserProfile.objects.get(user = user)
            payload = {'old_password':old_password, 'new_password':new_password, 'confirm_new_password':confirm_new_password}
            headers = {"Authorization":"Token 0ff2eb42e048d998567a744b90b86aad18daea97", 'Content-type': 'application/json'}
            r = requests.post(CHANGE_PASSWORD_URL, data=json.dumps(payload), headers=headers)
            pprint(r.json())
            if r.json()['status'] == True:
                pprint('_________--trest______________--')
                pprint(r.json())
                return True
    return False

def ChangeUsernameToServer(user, new_username):
    auth_token = AUTH_TOKEN
    payload = {'new_username':new_username}
    headers = {"Authorization":"Token 0ff2eb42e048d998567a744b90b86aad18daea97", 'Content-type': 'application/json'}
    r = requests.post(CHANGE_USERNAME_URL, data=json.dumps(payload), headers=headers)
    if r.json()['status'] == True:
        return True
    return False
