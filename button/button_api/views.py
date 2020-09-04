# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import UserManager, User, Cloth_Specific
from .serializers import User_Serializer, Cloth_SpecificSerializer, User_findEmail_Serializer
# Create your views here.


@api_view(['GET'])
def user_list(request):
    # 모든 사용자 보기 & 추가
    if request.method == 'GET':
        users = User.objects.all()
        serializer = User_Serializer(users, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, id):
    try:
        user = User.objects.get(id=id)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = User_Serializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = User_Serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def cloth_list(request, id):
    if request.method == 'GET':
        closet = Cloth_Specific.objects.filter(id=id)
        serializer = Cloth_SpecificSerializer(closet, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = Cloth_SpecificSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def cloth_detail(request, id, clothID):
    try:
        cloth = Cloth_Specific.objects.get(id=id, clothID=clothID)

    except Cloth_Specific.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

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


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = User_Serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def findEmail(request, userEmail):
    if request.method == 'GET':
        if (User.objects.filter(userEmail=userEmail)):
            return Response({'exists': True})
        else:
            return Response({'exists': False})


@api_view(['GET'])
def login(request, userEmail, password):
    if request.method == 'GET':
        user = User.objects.filter(userEmail=userEmail)
        if(user):
            if(user.get('password') == password):
                return Response({'result': True})
            else:
                return Response({'result': False})
        else:
            return Response({'result': False})


# @csrf_exempt
# def login(request):
#     if request.method == 'POST':

#         userid = request.POST.get("userid", "")
#         userpw = request.POST.get("userpw", "")
#         login_result = authenticate(username=userid, password=userpw)
#         print("userid = " + userid + " result = " + str(login_result))
#         if login_result:
#             return Response(status=status.HTTP_200)
#         else:
#             return render(request, "addresses/login.html", status=401)
#         return render(request, "addresses/login.html")
