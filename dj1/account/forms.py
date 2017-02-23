from django import forms
# from django.forms import ModelForm
# from django.contrib.auth.models import User
# from core.models import *
from pprint import pprint


class BaseForm(forms.Form):
    """Base form for all the forms in EMS"""
    # def is_phone_no_invalid(self, phone_number):
    #     """ Util function for validating phone number """
    #     return ((not str(phone_number).isdigit()) or (len(phone_number)!=10))
    #
    # def is_name_invalid(self,name):
    #     """
    #     This function return true if name contains any digit. However it fails to address the special characters.
    #     """
    #     return self.has_numbers(name)
    #
    # def user_email_already_exists(self, email):
    #     """
    #     This function return true if the user email provided already exists in database.
    #     """
    #     return User.objects.filter(email=email).exists()
    #
    # def company_email_already_exists(self, email):
    #     """
    #     This function return true if the company email provided already exists in database.
    #     """
    #     return CompanyModel.objects.filter(company_email=email).exists()
    #
    # def user_phone_no_already_exists(self, phone_no):
    #     """
    #     This function return true if the Phone Number by user provided already exists in user's database.
    #     """
    #     return UserProfile.objects.filter(phone_no=phone_no).exists()
    #
    # def company_phone_no_already_exists(self, phone_no):
    #     """
    #     This function return true if the Phone Number by user provided already exists in user's database.
    #     """
    #     return CompanyModel.objects.filter(company_phone_no=phone_no).exists()
    #
    # def has_numbers(self,inputString):
    #     """This function to to check if """
    #     return any(char.isdigit() for char in inputString)

class RegistrationForm(BaseForm):
    """Form for user registration/creating account"""
    user_email = forms.EmailField()
    username = forms.CharField(max_length=60)
    user_nicename = forms.CharField(max_length = 50)
    user_url = forms.URLField(max_length=100)
    display_name = forms.CharField(max_length=250)
    password = forms.CharField(max_length = 30)
    confirm_password = forms.CharField(max_length=30)

class UpdateInfoForm(BaseForm):
    """ Form for updating user information """
    user_email = forms.EmailField()
    user_nicename = forms.CharField(max_length = 50)
    user_url = forms.URLField(max_length=100)
    display_name = forms.CharField(max_length=250)

class ChangePasswordForm(BaseForm):
    """ Form for changing password """
    old_password = forms.CharField(30)
    new_password = forms.CharField(30)
    confirm_new_password = forms.CharField(30)


class ChangeUsernameForm(BaseForm):
    """ Form for changin username """
    new_username = forms.CharField(max_length = 50)
