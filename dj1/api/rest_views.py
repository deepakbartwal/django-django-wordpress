# from rest_framework import viewsets
from rest_framework import status
# from rest_framework import viewsets
from rest_framework import status
# from rest_framework.authtoken.models import Token
# from api.models import *
# from api.serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from pprint import pprint
import json
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from django.contrib.auth.models import User
from .other_server import RegisterToServer

@api_view(['POST', 'GET'])
@permission_classes((permissions.AllowAny,))
def RegisterUser(request):
    """
    view to register user in current as well as other server
    """
    if request.method == 'POST':
        username = request.data['username']
        email = request.data['email']
        if not(User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
            first_name = request.data['first_name']
            last_name = request.data["last_name"]
            password = request.data['password']
            if RegisterToServer(username, email, password, first_name, last_name):
                current_user = User.objects.create_user(username = username, email = email, password = password, first_name = first_name, last_name = last_name)
                return Response(data={'status': True}, status=status.HTTP_200_OK)
        return Response(data={'status': False}, status=status.HTTP_200_OK)
