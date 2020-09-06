# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import UserManager, User, Cloth_Specific
from .serializers import User_Serializer, Cloth_SpecificSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail
# Create your views here.


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = User_Serializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "successfully registerd a new user"
            data['userEmail'] = account.userEmail
            data['userGender'] = account.userGender
            data['userNickName'] = account.userNickName
            token = Token.objects.get(user=account).key
            data['token'] = token
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def findEmail(request, userEmail):
    if request.method == 'GET':
        if (User.objects.filter(userEmail=userEmail)):
            return Response({'exists': True})
        else:
            return Response({'exists': False})


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
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
@permission_classes((IsAuthenticated,))
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
    if id != user.id:
        return Response({'response': "You don't have permission for access!"})
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
    if id != user.id:
        return Response({'response': "You don't have permission for access!"})
    if request.method == 'GET':
        closet = Cloth_Specific.objects.filter(id=id, category=category)
        serializer = Cloth_SpecificSerializer(closet, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def cloth_detail(request, id, clothID):
    try:
        cloth = Cloth_Specific.objects.get(id=id, clothID=clothID)

    except Cloth_Specific.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if id != user:
        return Response({'response': "You don't have permission for access!"})

    if request.method == 'GET':
        serializer = Cloth_SpecificSerializer(cloth)
        return Response(serializer.data)

    elif request.method == 'PUT':
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


# @api_view()
# def null_view(request):
#     return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view()
# def complete_view(request):
#     return Response("Email account is activated")
