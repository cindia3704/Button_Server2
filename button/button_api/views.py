# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, views
from rest_framework.views import APIView
from .models import UserManager, User, Cloth_Specific
from .serializers import User_Serializer, Cloth_SpecificSerializer, ChangePasswordSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail
# Create your views here.


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        user = request.data
        serializer = User_Serializer(data=user)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "successfully registerd a new user"
            data['userEmail'] = account.userEmail
            data['userGender'] = account.userGender
            data['userNickName'] = account.userNickName
            user_data = serializer.data
            user__ = User.objects.get(userEmail=user_data['userEmail'])
            token = Token.objects.get(user=account).key
            # token = RefreshToken.for_user(user__).access_token
            data['token'] = token

            # token2 = RefreshToken.for_user(account).access_token
            # data['token'] = token2
            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')

            absurl = 'http://'+current_site+relativeLink + \
                "?email="+str(account.get_email())
            email_body = "Hi "+str(account.get_nickname()) + \
                ' Thank you for registering to out application "button"!!\nUse link below to verify your email\n '+absurl

            data_ = {'email_body': email_body, 'to_email': str(account.get_email()),
                     'email_subject': 'Verify your email'}
            Util.send_email(data_)

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def setPassword(request):
#     if request.method == 'POST':
#         user = request.data
#         serializer = User_Serializer(data=user)
#         data = {}
#         if serializer.is_valid():
#             account = serializer.save()
#             data['response'] = "successfully registerd a new user"
#             data['userEmail'] = account.userEmail
#             data['userGender'] = account.userGender
#             data['userNickName'] = account.userNickName
#             user_data = serializer.data
#             user__ = User.objects.get(userEmail=user_data['userEmail'])
#             user__.set_password()
#             token = Token.objects.get(user=account).key
#             #token = RefreshToken.for_user(user__).access_token
#             data['token'] = token

#             # token2 = RefreshToken.for_user(account).access_token
#             # data['token'] = token2
#             current_site = get_current_site(request).domain
#             relativeLink = reverse('email-verify')

#             absurl = 'http://'+current_site+relativeLink + \
#                 "?email="+str(account.get_email())
#             email_body = "Hi "+str(account.get_nickname()) + \
#                 ' Thank you for registering to out application "button"!!\nUse link below to verify your email\n '+absurl

#             data_ = {'email_body': email_body, 'to_email': str(account.get_email()),
#                      'email_subject': 'Verify your email'}
#             Util.send_email(data_)

#             return Response(data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def findPassword(request, userEmail):
#     try:
#         user = User.objects.filter(userEmail=userEmail)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#         data = {}
#     if request.method == 'GET':
#         if (user):
#             serializer = ChangePasswordSerializer(user)
#             data_ = serializer.data
#             password = str(data_['password'])
#             nickName = str(data_['userNickName'])
#             current_site = get_current_site(request).domain
#             relativeLink = reverse('email-find')
#             # absurl = 'http://'+current_site+relativeLink + \
#             #     "?email="+str(account.get_email())
#             email_body = "Hi "+str(nickName) + \
#                 ' \nYour password is: '+str(password)

#             data_ = {'email_body': email_body, 'to_email': str(userEmail),
#                      'email_subject': 'Find your email'}
#             Util.send_email(data_)
#             return Response(data)
#         else:
#             return Response(data)


@api_view(['GET'])
def findEmail(request, userEmail):
    if request.method == 'GET':
        if (User.objects.filter(userEmail=userEmail)):
            return Response({'exists': True})
        else:
            return Response({'exists': False})


@api_view(['GET'])
def user_list(request):
    # 모든 사용자 보기 & 추가
    if request.method == 'GET':
        users = User.objects.all()
        serializer = User_Serializer(users, many=True)
        # permission_classes = [IsAuthenticated]
        return Response(serializer.data)
    # elif request.method == 'POST':
    #     serializer = User_Serializer(data=request.data)
    #     permission_classes = [IsAuthenticated]
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_detail(request, id):
    try:
        user_personal = User.objects.get(id=id)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user_personal.id != user.id:
        return Response({'response': "You don't have permission for access!"})
    if request.method == 'GET':
        serializer = User_Serializer(user_personal)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def user_detail_change(request, id):
    try:
        user_personal = User.objects.get(id=id)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user_personal.id != user.id:
        return Response({'response': "You don't have permission for access!"})

    elif request.method == 'PUT':
        serializer = User_Serializer(user_personal, data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def user_delete(request, id):
    try:
        user_personal = User.objects.get(id=id)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user_personal.id != user.id:
        return Response({'response': "You don't have permission for access!"})

    elif request.method == 'DELETE':
        user_personal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def cloth_list(request, id):
    user = request.user
    # if id != user.id:
    # return Response({'response': "You don't have permission for access!"})
    if request.method == 'GET':
        closet = Cloth_Specific.objects.filter(id=id)
        serializer = Cloth_SpecificSerializer(closet, many=True)
        return Response(serializer.data)

    # POST부분 authentication 추가!!!
    elif request.method == 'POST':
        serializer = Cloth_SpecificSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def cloth_category_list(request, id, category):
    user = request.user
<<<<<<< HEAD
    # if id != user.id:
=======
   # if id != user.id:
>>>>>>> 35aa25d... last last
    # return Response({'response': "You don't have permission for access!"})
    if request.method == 'GET':
        closet = Cloth_Specific.objects.filter(id=id, category=category)
        serializer = Cloth_SpecificSerializer(closet, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@permission_classes((IsAuthenticated,))
def cloth_detail(request, id, clothID):
    try:
        cloth = Cloth_Specific.objects.get(id=id, clothID=clothID)

    except Cloth_Specific.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
<<<<<<< HEAD
=======

>>>>>>> 35aa25d... last last
    # if id != user:
    # return Response({'response': "You don't have permission for access!"})

    if request.method == 'GET':
        serializer = Cloth_SpecificSerializer(cloth)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = Cloth_SpecificSerializer(cloth, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = Cloth_SpecificSerializer(cloth, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        cloth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ChangePasswordView(generics.UpdateAPIView):
#     """
#     An endpoint for changing password.
#     """
#     serializer_class = ChangePasswordSerializer
#     model = User
#     permission_classes = (IsAuthenticated,)

#     def get_object(self, queryset=None):
#         obj = self.request.user
#         return obj

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully',
#                 'data': []
#             }

#             return Response(response)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(views.APIView):
    def get(self, request):
        email = request.GET.get('email')
        try:
            user = User.objects.get(userEmail=email)

            if not user.confirmedEmail:
                user.confirmedEmail = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
