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
from .models import UserManager, User, Cloth_Specific, Outfit_Specific, Friend, KNN
from .serializers import User_Serializer, Cloth_SpecificSerializer, ChangePasswordSerializer, OutfitSerializer, User_Serializer2, Friend_Serializer, KNN_Serializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.hashers import make_password
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
import random
import string
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail
from .knn import knn_results
from . import knn
# Create your views here.


class FriendListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        ownerID = view.kwargs.get('id', None)
        owner = User.objects.get(id=ownerID)
        friend = Friend.objects.filter(
            frienduser=request.user, accepted=True, user=owner)

        # if friend:
        #     return True
        # else:
        #     return False
        return friend


class OwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        ownerID = view.kwargs.get('id', None)
        owner = User.objects.get(id=ownerID)
        if request.user == owner:
            return owner
        # if friend:
        #     return True
        # else:
        #     return False
        else:
            return None


@api_view(['POST'])
def post_userInput(request):
    if request.method == 'POST':
        # knn_input = serializer.save()
        place1 = request.data.get('place1')
        place2 = request.data.get('place2')
        event1 = request.data.get('event1')
        event2 = request.data.get('event2')
        people1 = request.data.get('people1')
        people2 = request.data.get('people2')
        mood = request.data.get('mood')
        style_res = knn_results(
            place1, place2, event1, event2, people1, people2, mood)
        request.data['style'] = style_res
        # knn_mod = KNN.objects.get(KNNID=serializer.data.get('KNNID'))
        # print(knn_mod)
        serializer = KNN_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # knn_data = serializer.data
            # knn_data['style'] = style_res
            # print(style_res)
            # print("---")
            # knn_input.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_knnResult(request, KNNID):
    try:
        result = KNN.objects.get(KNNID=KNNID)

    except KNN.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = KNN_Serializer(result)
        return Response(serializer.data)


# @api_view(['GET'])
# def get_clothes_worn(request, id, datesWorn):
#     try:
#         cloth = Cloth_Specific.objects.filter(id=id, datesWorn=datesWorn)
#     except Cloth_Specific.DoesNotExist:
#         return Response({'response': 'none'})

#     if request.method == 'GET':
#         serializer = Cloth_SpecificSerializer(cloth)
#         return Response(serializer.data)


@ api_view(['POST'])
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
            email_body = ""+str(account.get_nickname()) + "님, 안녕하세요.\n"\
                '저희 버튼에 회원가입을 해주셔서 감사합니다.\n아래 링크로 이메일 인증을 완료해주세요\n '+absurl

            data_ = {'email_body': email_body, 'to_email': str(account.get_email()),
                     'email_subject': '이메일 인증'}
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


@ api_view(['GET'])
def findEmail(request, userEmail):
    if request.method == 'GET':
        if (User.objects.filter(userEmail=userEmail)):
            return Response({'exists': True})
        else:
            return Response({'exists': False})


# @ api_view(['POST'])
# @permission_classes(OwnerPermission)
# def changePassword(request, id, changed):
#     if user_personal.id != user.id:
#         return Response({'response': "You don't have permission for access!"})
#     if request.method == 'POST':
#         try:
#             user = User.objects.get(id=id)
#         except User.DoesNotExist:
#             return Response({'response': "no user found"}, status=status.HTTP_404_NOT_FOUND)
#         if(user):
#             password = changed
#             user.set_password(password)
#             user.save
#             return Response({'response': "password changed successfully"}, status=status.HTTP_201_CREATED)


@ api_view(['GET'])
def retLoggedUser(request, userEmail):
    try:
        user_personal = User.objects.get(userEmail=userEmail)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = User_Serializer2(user_personal)
        return Response(serializer.data)


@ api_view(['GET'])
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


@ api_view(['GET'])
@ permission_classes([FriendListPermission | OwnerPermission])
def user_detail(request, id):
    try:
        user_personal = User.objects.get(id=id)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if request.method == 'GET':
        serializer = User_Serializer(user_personal)
        return Response(serializer.data)


@ api_view(['PATCH'])
@ permission_classes((IsAuthenticated, OwnerPermission))
def user_detail_change(request, id):
    try:
        user_personal = User.objects.get(id=id)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user_personal.id != user.id:
        return Response({'response': "You don't have permission for access!"})

    elif request.method == 'PATCH':
        serializer = User_Serializer(user_personal, data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['DELETE'])
@ permission_classes((IsAuthenticated, OwnerPermission))
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


@ api_view(['GET', 'POST'])
@ parser_classes([MultiPartParser])
@ permission_classes([FriendListPermission | OwnerPermission])
def cloth_list(request, id):
    def get_id():
        return id
    user = request.user
    # if id != user.id:
<<<<<<< HEAD
    # return Response({'response': "You don't have permission for access!"})
=======
    #     return Response({'response': "You don't have permission for access!"})
>>>>>>> 391b1f7... change auth for clothlist
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


@ api_view(['POST'])
@ permission_classes([OwnerPermission])
def change_password(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("password")):
                print(serializer.data.get("password"))
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # passs = make_password(request.data.get('newPassword'))
                print(request.data.get('newPassword'))
                user.set_password(request.data.get('newPassword'))
                user.save()
                # user.make_password(
                #     serializer.data.get("new_password"))
                # user.save()
                return Response({"password": "Successfully updated password"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['POST'])
def find_password(request, userEmail):
    try:
        user = User.objects.get(userEmail=userEmail)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        current_site = get_current_site(request).domain
        newPass = letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(10))
        print(result_str)
        email_body = ""+str(user.get_nickname()) + \
            ' 님 안녕하세요.\n임시 비밀번호: '+result_str+'\n로그인을 한 후 반드시 비밀번호를 변경해 주시기 바랍니다.'

        data_ = {'email_body': email_body, 'to_email': str(user.get_email()),
                 'email_subject': '비밀번호 찾기'}
        Util.send_email(data_)
        user.set_password(result_str)
        user.save()
        return Response({'response': 'email successfully sent'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'response': 'error'}, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['POST'])
@ permission_classes([FriendListPermission | OwnerPermission])
def outfit_cloth_add(request, id, outfitID, clothID):
    try:
        outfit_ = Outfit_Specific.objects.get(outfitID=outfitID)
        cloth = Cloth_Specific.objects.get(clothID=clothID)
    except Outfit_Specific.DoesNotExist:
        # print('outfit not found')
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Cloth_Specific.DoesNotExist:
       # print('cloth not found')
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        cloth.outfit.add(outfitID)
        cloth.save()
    return Response(status=status.HTTP_201_CREATED)


@ api_view(['DELETE'])
@ permission_classes([FriendListPermission | OwnerPermission])
def outfit_cloth_del(request, id, outfitID, clothID):
    try:
        outfit_ = Outfit_Specific.objects.get(outfitID=outfitID)
        cloth = Cloth_Specific.objects.get(clothID=clothID)
    except Outfit_Specific.DoesNotExist:
        print('outfit not found')
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Cloth_Specific.DoesNotExist:
        print('cloth not found')
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        del_ = cloth.outfit.get(outfitID=outfitID)
        cloth.outfit.remove(outfitID)
        cloth.save()
        return Response(status=status.HTTP_201_CREATED)


@ api_view(['PATCH'])
@ permission_classes([FriendListPermission | OwnerPermission])
def outfit_cloth_change(request, id, outfitID, clothID1, clothID2):
    try:
        outfit_ = Outfit_Specific.objects.get(outfitID=outfitID)
        cloth1 = Cloth_Specific.objects.get(clothID=clothID1)
        cloth2 = Cloth_Specific.objects.get(clothID=clothID2)
    except Outfit_Specific.DoesNotExist:
        print('outfit not found')
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Cloth_Specific.DoesNotExist:
        print('cloth not found')
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        cloth1.outfit.remove(outfitID)
        cloth2.outfit.add(outfitID)
        cloth1.save()
        cloth2.save()
        return Response(status=status.HTTP_201_CREATED)


@ api_view(['GET'])
@ permission_classes([OwnerPermission | FriendListPermission])
def cloth_category_list(request, id, category):
    user = request.user
<<<<<<< HEAD
<<<<<<< HEAD
    # if id != user.id:
=======
   # if id != user.id:
>>>>>>> 35aa25d... last last
    # return Response({'response': "You don't have permission for access!"})
=======
    # if id != user.id:
    #     return Response({'response': "You don't have permission for access!"})
>>>>>>> 391b1f7... change auth for clothlist
    if request.method == 'GET':
        closet = Cloth_Specific.objects.filter(id=id, category=category)
        serializer = Cloth_SpecificSerializer(closet, many=True)
        return Response(serializer.data)


@ api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@ permission_classes([FriendListPermission | OwnerPermission])
def cloth_detail(request, id, clothID):
    try:
        cloth = Cloth_Specific.objects.get(id=id, clothID=clothID)

    except Cloth_Specific.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
<<<<<<< HEAD
=======

<<<<<<< HEAD
>>>>>>> 35aa25d... last last
    # if id != user:
    # return Response({'response': "You don't have permission for access!"})
=======
    # if id != user:
    #     return Response({'response': "You don't have permission for access!"})
>>>>>>> 391b1f7... change auth for clothlist

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
        outfitIDS = cloth.get_outfit()
        outfits = Outfit_Specific.objects.filter(id=outfitIDS)
        for out in outfits:
            out.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@ api_view(['POST'])
@ permission_classes([FriendListPermission | OwnerPermission])
def saveOutfit(request, id):
    user = request.user
    # if id != user.id:
    # return Response({'response': "You don't have permission for access!"})

    # POST부분 authentication 추가!!!
    if request.method == 'POST':
        serializer = OutfitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


<<<<<<< HEAD
@api_view(['GET'])
=======
# @api_view['POST']
# def save_friendship(request):
#      if request.method == 'POST':
#             serializer = Friend_Serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @ api_view(['GET'])
# def friend_list(request, id):
#     if request.method == 'GET':
#         outfit_closet = Outfit_Specific.objects.filter(id=id)
#         serializer = OutfitSerializer(outfit_closet, many=True)
#         return Response(serializer.data)

@ api_view(['GET'])
<<<<<<< HEAD
@ permission_classes([IsAuthenticated | FriendListPermission])
>>>>>>> bcc7d00... add friend and friend permission
def outfit_list(request, id):
    user = request.user
    # if id != user.id:
    # return Response({'response': "You don't have permission for access!"})
=======
@ permission_classes([FriendListPermission | OwnerPermission])
def outfit_list(request, id):
    user = request.user
    # if id != user.id:
    #     return Response({'response': "You don't have permission for access!"})
>>>>>>> 376f70f... correct permissions
    if request.method == 'GET':
        outfit_closet = Outfit_Specific.objects.filter(id=id)
        serializer = OutfitSerializer(outfit_closet, many=True)
        return Response(serializer.data)


<<<<<<< HEAD
@api_view(['PATCH', 'DELETE', 'GET'])
=======
@ api_view(['PATCH', 'DELETE', 'GET'])
<<<<<<< HEAD
@ permission_classes([IsAuthenticated | FriendListPermission])
>>>>>>> bcc7d00... add friend and friend permission
=======
@ permission_classes([FriendListPermission | OwnerPermission])
>>>>>>> 376f70f... correct permissions
def outfit_change(request, id, outfitID):
    def get_id():
        return id
    try:
        outfit = Outfit_Specific.objects.get(id=id, outfitID=outfitID)

    except Outfit_Specific.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if request.method == 'PATCH':
        serializer = OutfitSerializer(outfit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        outfit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'GET':
        serializer = OutfitSerializer(outfit)
        return Response(serializer.data)

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


# class AcceptFriendEmail(views.APIView):
#     def get(self, request):
#         email = request.GET.get('email')
#         try:
#             user = User.objects.get(userEmail=email)

#             if not user.confirmedEmail:
#                 user.confirmedEmail = True
#                 user.save()
#             return Response({'email': 'Successfully activated'}, status=status.HTTP_201_CREATED)
#         except jwt.ExpiredSignatureError as identifier:
#             return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
#         except jwt.exceptions.DecodeError as identifier:
#             return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@ api_view(['GET'])
@ permission_classes((IsAuthenticated, OwnerPermission))
def get_friendlist(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        friendList = Friend.objects.filter(user=user)
        serializer = Friend_Serializer(friendList, many=True)
        return Response(serializer.data)


@ api_view(['GET', 'DELETE'])
@ permission_classes((IsAuthenticated, OwnerPermission))
def specific_friend(request, id, friendId):
    try:
        user = User.objects.get(id=id)
        friend = User.objects.get(id=friendId)
        friendspecific = Friend.objects.get(
            user=user, accepted=True, frienduser=friend)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = Friend_Serializer(friendspecific)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        friendspecific.delete()
        friend2 = Friend.objects.get(
            user=friend, frienduser=user, accepted=True)
        friend2.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@ api_view(['GET'])
@ permission_classes((IsAuthenticated, OwnerPermission))
def get_acceped_friendlist(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        friendList = Friend.objects.filter(user=user, accepted=True)
        serializer = Friend_Serializer(friendList, many=True)
        return Response(serializer.data)


@ api_view(['POST'])
@ permission_classes((IsAuthenticated, OwnerPermission))
def send_friendRequest(request, id, userEmail):
    try:
        user = User.objects.get(id=id)
        reciever = User.objects.get(userEmail=userEmail)
    except User.DoesNotExist:
        return Response({'email': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        if not Friend.objects.filter(frienduser=reciever).exists():
            new_friend = Friend()
            new_friend.user = User.objects.get(id=id)
            new_friend.frienduser = User.objects.get(
                userEmail=userEmail)
            new_friend.save()
        # user = User.objects.filter(id=id)
        # reciever = User.objects.get(userEmail=userEmail)
        # data = {}
        # data['user'] =
        # data['frienduser'] = reciever
        # serializer = Friend_Serializer(data=data)
        # if(serializer.is_valid()):
        #     serializer.save()

        # user = User.objects.get(id=id)
            senderEmail = user.get_email()
        # reciever = User.objects.get(userEmail=userEmail)
            recieverEmail = userEmail

            current_site = get_current_site(request).domain
            relativeLink = reverse('verify-friend')

            absurl = 'http://'+current_site+relativeLink + \
                "?email="+str(recieverEmail)+"&sender="+str(senderEmail)
            email_body = ""+str(reciever.get_nickname()) + "님, 안녕하세요.\n" \
                + str(user.get_nickname()) + \
                "님이 친구 요청을 보냈습니다.\n아래 링크를 클릭해 친구요청을 수락해주세요.\n"+absurl

            data_ = {'email_body': email_body, 'to_email': str(recieverEmail),
                     'email_subject': '친구 요청'}
            Util.send_email(data_)

            return Response({'email': 'Successfully sent'}, status=status.HTTP_201_CREATED)
        elif Friend.objects.filter(user=user, frienduser=reciever, accepted=False).exists():
            return Response({'email': 'already sent request'}, status=status.HTTP_400_BAD_REQUEST)
        elif Friend.objects.filter(user=user, frienduser=reciever, accepted=True).exists():
            return Response({'email': 'already friend'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'email': 'ERROR'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyFriendRequest(views.APIView):
    def get(self, request):
        email = request.GET.get('email')
        senderEmail = request.GET.get('sender')
        print('email:'+str(email))
        print('senderEmail:'+str(senderEmail))
        try:
            friendUser = User.objects.get(userEmail=email)
            user = User.objects.get(userEmail=senderEmail)
            friend = Friend.objects.get(
                user=User.objects.get(userEmail=senderEmail), frienduser=User.objects.get(userEmail=email))
            if not friend.accepted:
                friend.accepted = True
                friend.save()
                new_friend = Friend()
                new_friend.user = User.objects.get(userEmail=email)
                new_friend.frienduser = User.objects.get(
                    userEmail=senderEmail)
                new_friend.accepted = True
                new_friend.save()

            return Response({'friendship': 'Successfully connected'}, status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
