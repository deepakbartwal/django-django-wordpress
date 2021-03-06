from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication,SessionAuthentication, BasicAuthentication
import json
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from django.contrib.auth.models import User
from wordpress.models import WpUsers
# from .serializers import *
from pprint import pprint


class RegisterFromServerView(APIView):
    """
    view to register user in current as well as other server
    """
    # authentication_classes = (TokenAuthentication,)
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        data = request.data
        username = data['username']
        user_email = data['user_email']
        if not (WpUsers.objects.filter(user_login=username).exists() and WpUsers.objects.filter(user_email = user_email)):
            if not (User.objects.filter(username=username).exists() and User.objects.filter(email = user_email)):
                password = data['password']
                confirm_password = data['confirm_password']
                if password == confirm_password:

                    user_nicename = data.get('user_nicename', None)
                    user_url = data.get('user_url', None)
                    display_name = data.get('display_name', None)

                    user = User.objects.create_user(username = username, email = user_email, password = password)

                    wp_user = WpUsers()
                    wp_user.user_login = username
                    wp_user.user_pass = user.password[7:]
                    wp_user.user_nicename = user_nicename
                    wp_user.user_email = user_email
                    wp_user.user_url = user_url
                    wp_user.display_name = display_name
                    wp_user.save()
                    return Response(data={'status': True}, status=status.HTTP_200_OK)
        return Response(data={'status': False}, status=status.HTTP_200_OK)


class UpdateFromServerView(APIView):
    """
    View update the user profile from other server
    """
    authentication_classes = (TokenAuthentication,)
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        #work here later ... its okey for now
        # serializer =  UserProfileSerializer(request.data)
        # if serializer.is_valid():
        #     up_instance = serializer.update(user, serializer.validated_data)
        #     return Response(data={'status': True}, status=status.HTTP_200_OK)
        #

        user = request.user
        wp_user = WpUsers.objects.get(user_login=user.username)
        data = request.data
        user_email = data.get("user_email", wp_user.user_email)
        user.email = user_email
        wp_user.user_email = user_email
        wp_user.user_nicename = data.get('user_nicename', wp_user.user_nicename)
        wp_user.display_name = data.get('display_name', wp_user.display_name)
        wp_user.user_url = data.get('user_url', wp_user.user_url)
        user.save()
        wp_user.save()
        return Response(data={'status': True}, status=status.HTTP_200_OK)


class ChangePasswordFromServerView(APIView):
    """
    View to change the user password from other server
    """
    authentication_classes = (TokenAuthentication,)
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = User.objects.get(username=request.user.username)
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        confirm_new_password = request.data['confirm_new_password']
        if new_password == old_password:
            return Response(data={'status': False}, status=status.HTTP_200_OK)#error
        else:
            DatabasePassword = request.user.password
            from django.contrib.auth.hashers import check_password
            chk = check_password(password=old_password, encoded = DatabasePassword)
            if chk == True:
                user.set_password(new_password)
                user.save()
                wp_user = WpUsers.objects.get(user_login=user.username)
                wp_user.user_pass = user.password[7:]
                wp_user.save()
                return Response(data={'status': True}, status=status.HTTP_200_OK)
        return Response(data={'status': False}, status=status.HTTP_200_OK)

class ChangeUsernameFromServerView(APIView):
    """
    View to change the username from other server
    """
    authentication_classes = (TokenAuthentication,)
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = User.objects.get(username=request.user.username)
        old_username = user.username
        new_username = request.data['new_username']
        if new_username == old_username:
            return Response(data={'status': False}, status=status.HTTP_200_OK)#error
        else:
            user.username = new_username
            wp_user = WpUsers.objects.get(user_login=old_username)
            wp_user.user_login = new_username
            user.save()
            wp_user.save()
            return Response(data={'status': True}, status=status.HTTP_200_OK)
        return Response(data={'status': False}, status=status.HTTP_200_OK)




# @api_view(['POST', 'GET'])
# @permission_classes((permissions.AllowAny,))
# def RegisterFromServer(request):
#     """
#     view to register user in current as well as other server
#     """
#     if request.method == 'POST':
#         username = request.data['username']
#         user_email = request.data['user_email']
#         if not (WpUsers.objects.filter(user_login=username).exists() and WpUser.objects.filter(user_email = user_email)):
#             password = request.data['password']
#             confirm_password = request.data['confirm_password']
#             if password == confirm_password:
#                 user = WpUsers()
#                 p.user_nicename = request.data['user_nicename']
#                 p.user_url = request.data['user_url']
#                 p.display_name = request.data['display_name']
#                 p.save()
#                 return Response(data={'status': True}, status=status.HTTP_200_OK)
#         return Response(data={'status': False}, status=status.HTTP_200_OK)


        # if not(User.objects.filter(username=username).exists() or User.objects.filter(email=user_email).exists()):
        #     password = request.data['password']
        #     confirm_password = request.data['confirm_password']
        #     if password == confirm_password:
        #         current_user = User.objects.create_user(username = username, email = user_email, password = password)
        #         p = UserProfile()
        #         p.user = current_user
        #         p.user_nicename = request.data['user_nicename']
        #         p.user_url = request.data['user_url']
        #         p.display_name = request.data['display_name']
        #         p.save()
        #         return Response(data={'status': True}, status=status.HTTP_200_OK)
        # return Response(data={'status': False}, status=status.HTTP_200_OK)

# class UpdateFromServerView(APIView):
#     """
#     View update the user profile from other server
#     """
#     authentication_classes = (TokenAuthentication,)
#     renderer_classes = (JSONRenderer,)
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def post(self, request):
#         #work here later ... its okey for now
#         user = request.user
#         # serializer =  UserProfileSerializer(request.data)
#         # if serializer.is_valid():
#         #     up_instance = serializer.update(user, serializer.validated_data)
#         #     return Response(data={'status': True}, status=status.HTTP_200_OK)
#         #
#         p = UserProfile.objects.get(user = user)
#         data = request.data
#         user_email = request.data['user_email']
#         user.email = user_email
#         pprint(user.save())
#
#         p.user_nicename = request.data['user_nicename']
#         p.display_name = request.data['user_nicename']
#         p.user_url = request.data['user_url']
#         p.save()
#         return Response(data={'status': True}, status=status.HTTP_200_OK)
#
# class ChangePasswordFromServerView(APIView):
#     """
#     View to change the user password from other server
#     """
#     authentication_classes = (TokenAuthentication,)
#     renderer_classes = (JSONRenderer,)
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def post(self, request):
#         user = User.objects.get(username=request.user.username)
#         old_password = request.data['old_password']
#         new_password = request.data['new_password']
#         confirm_new_password = request.data['confirm_new_password']
#         if new_password == old_password:
#             return Response(data={'status': False}, status=status.HTTP_200_OK)#error
#         else:
#             DatabasePassword = request.user.password
#             from django.contrib.auth.hashers import check_password
#             chk = check_password(password=old_password, encoded = DatabasePassword)
#             if chk == True:
#                     user.set_password(new_password)
#                     user.save()
#                     return Response(data={'status': True}, status=status.HTTP_200_OK)
#         return Response(data={'status': False}, status=status.HTTP_200_OK)
#
# class ChangeUsernameFromServerView(APIView):
#     """
#     View to change the username from other server
#     """
#     authentication_classes = (TokenAuthentication,)
#     renderer_classes = (JSONRenderer,)
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def post(self, request):
#         user = User.objects.get(username=request.user.username)
#         new_username = request.data['new_username']
#         if new_username == user.username:
#             return Response(data={'status': False}, status=status.HTTP_200_OK)#error
#         else:
#             user.username = new_username
#             user.save()
#             return Response(data={'status': True}, status=status.HTTP_200_OK)
#         return Response(data={'status': False}, status=status.HTTP_200_OK)
