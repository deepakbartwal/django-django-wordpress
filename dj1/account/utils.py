from django.contrib.auth.models import *
from core.models import *
from api.other_server import *


def RegistrationUtil(data_dict):
    """ Util function for registering user on this and other server """
    username = data_dict['username']
    user_email = data_dict['user_email']
    if not (User.objects.filter(username=username).exists() or User.objects.filter(email=user_email).exists()):
        password = data_dict["password"]
        confirm_password = data_dict["confirm_password"]
        user_nicename = data_dict['user_nicename']
        user_url = data_dict['user_url']
        display_name = data_dict['display_name']
        if RegisterToServer(user_nicename=user_nicename, display_name=display_name, user_email=user_email, username=username, user_url=user_url, password=password, confirm_password=confirm_password):
            registered_user = User.objects.create_user(username = username, email = user_email, password = password)

            p = UserProfile()
            p.user = registered_user
            p.user_nicename = data_dict['user_nicename']
            p.user_url = data_dict['user_url']
            p.display_name = ['display_name']
            p.save()
            return True
    return False

def UpdateInfoUtil(data_dict, user):
    """ Utility to update the user information """
    user_email = data_dict['user_email']
    user_nicename = data_dict['user_nicename']
    display_name = data_dict['display_name']
    user_url = data_dict['user_url']
    username = user.username
    if UpdateToServer(username=username, user_email=user_email, user_nicename=user_nicename, display_name=display_name, user_url=user_url):
        p = UserProfile.objects.get(user = user)
        user.email = user_email
        user.save()
        p.user_nicename = user_nicename
        p.display_name = display_name
        p.user_url = user_url
        p.save()
        return True
    return False

def ChangePasswordUtil(user, old_password, new_password, confirm_new_password):
    username = user.username
    if ChangePasswordToServer(username, old_password, new_password, confirm_new_password):
        user.set_password(new_password)
        user.save()
        return True
    return False

def ChangeUsernameUtil(user, new_username):
    username = user.username
    if ChangeUsernameToServer(user, new_username):
        user.username = new_username
        user.save()
        return True
    return False
