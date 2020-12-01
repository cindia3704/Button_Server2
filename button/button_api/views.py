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
from .models import UserManager, User, Cloth_Specific, Outfit_Specific, Friend, KNN, Calendar_Specific
from .serializers import User_Serializer, Cloth_SpecificSerializer, ChangePasswordSerializer, OutfitSerializer, User_Serializer2, Friend_Serializer, KNN_Serializer, CalendarSerializer
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
import requests
import random
# from random import *
import string
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail
from .knn import knn_results
from . import knn
import datetime
# from . import polyvore
# from .polyvore import run_inference
# from .polyvore.run_inference import extract_features
import json
<<<<<<< HEAD
=======
import os
import jsonpickle
from json import JSONEncoder
>>>>>>> 39a63b3... change json send to ml
# from .. import model
# from .. import polyvore
# from .. import data
# from ..polyvore import run_inference, set_generation
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
        id = request.data.get('id')
        place1 = request.data.get('place1')
        place2 = request.data.get('place2')
        event1 = request.data.get('event1')
        event2 = request.data.get('event2')
        people1 = request.data.get('people1')
        people2 = request.data.get('people2')
        mood = request.data.get('mood')
        season = request.data.get('season')
        style_res = knn_results(
            place1, place2, event1, event2, people1, people2, mood)
        request.data['style'] = style_res
        # knn_mod = KNN.objects.get(KNNID=serializer.data.get('KNNID'))
        # print(knn_mod)
        serializer = KNN_Serializer(data=request.data)
        print(request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            print("valid")
            knn_input = serializer.save()
            knn_data = serializer.data
            knn_data['style'] = style_res
            print(style_res)
            print("---")
            knn_input.save()
            if season == "WINTER" and style_res == "VACANCE":
                style_res = "CASUAL"

            if id == 1:
                ret_result = []
                output = ['1605338853884.jpeg',
                          '1605316954355.jpeg', '72.jpg']
                for clo in output:
                    print(clo)
                    ret_result.append(
                        Cloth_Specific.objects.get(id=id, photo=clo))
                    print(ret_result)
                ret_serializer = Cloth_SpecificSerializer(
                    ret_result, many=True)
                return Response(ret_serializer.data, status=status.HTTP_201_CREATED)
            else:
                ret_result = run_rec_algo(id, style_res, season)
                print(ret_result)
                if ret_result == "does not exist":
                    return Response({"response": "not enough clothes"})
                elif ret_result == "more clothes":
                    return Response({"response": "not enough clothes"})

            # ret_result = False
            # while ret_result != True:
            #     print("get rand")
            #     print("season: "+str(season)+"    style: "+str(style_res))
            #     rand_cloth = get_randomCloth(id, style_res, season)
            #     print(rand_cloth)
            #     if rand_cloth == "does not exist":
            #         return Response({"response": "not enough clothes"})
            #     print(rand_cloth)
            #     bi_lstm_input = rand_cloth.get_photo()
            #     print(bi_lstm_input)
            #     # bi_lstm_output = set_generation(bi_lstm_input, id,style)
            #     bi_lstm_output = ["81.jpg", "86.jpg", "99.jpg", "5.jpg"]
            #     bi_lstm_result = []
            #     for cloth_result in bi_lstm_output:
            #         print(cloth_result)
            #         bi_lstm_result.append(
            #             Cloth_Specific.objects.get(id=id, photo=cloth_result))
            #     print("++++")
            #     if rand_cloth.get_category() == "TOP":
            #         print("TOP")
            #         result = is_valid_outfit_top(
            #             bi_lstm_result[::-1], id, rand_cloth, season)
            #         print(ret_result)
            #         if result == "redo":
            #             ret_result = False
            #         else:
            #             ret_result = True
            #     else:
            #         result = is_valid_outfit_dress(
            #             bi_lstm_result[::-1], id, rand_cloth, season)
            #         print(ret_result)
            #         ret_result = True
                ret_serializer = Cloth_SpecificSerializer(
                    ret_result, many=True)
            return Response(ret_serializer.data, status=status.HTTP_201_CREATED)
    return Response(ret_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# knn 에서 나온 스타일에 맞는 상의 또는 원피스 가져오기


@api_view(['POST'])
def rec_set(request):
    print("inside rec_set")
    decodedSet = jsonpickle.decode(request.data)
    print(decodedSet)
    rand_cloth = decodedSet['rand_cloth']
    id = decodedSet['id']
    season = decodedSet['season']
    bi_lstm_output = decodedSet['clothlist']
    bi_lstm_result = []
    print("output of bi_lstm")
    print(bi_lstm_output)
    for cloth_result in bi_lstm_output:
        print(cloth_result)
        bi_lstm_result.append(
            Cloth_Specific.objects.get(id=id, photo=cloth_result))
    if rand_cloth.get_category() == "TOP":
        print("TOP")
        result = is_valid_outfit_top(
            bi_lstm_result[::-1], id, rand_cloth, season)
        # print(ret_result)
        if result == "redo":
            ret_result = False
        else:
            ret_result = True
    else:
        print("DRESS")
        result = is_valid_outfit_dress(
            bi_lstm_result[::-1], id, rand_cloth, season)
        print(ret_result)
        ret_result = True
    print(result)
    return result


def run_rec_algo(id, style, season):
    ret_result = False
    count = 0
    while ret_result != True:
        print("count:"+str(count))
        count = count+1
        if count == 15 and ret_result == False:
            print("moreeee CLOTHES!!!")
            return "more clothes"
            # return Response({"response": "not enough clothes"})
        print("season: "+str(season)+"    style: "+str(style))
        rand_cloth = get_randomCloth(id, style, season)
        print(rand_cloth)
        if rand_cloth == "does not exist":
            return rand_cloth
            # return Response({"response": "not enough clothes"})
        print(rand_cloth)
        bi_lstm_input = rand_cloth.get_photo()
        bi_data = {}
        clo_serializer = Cloth_SpecificSerializer(
            Cloth_Specific.objects.get(photo=bi_lstm_input))
        saved_object = clo_serializer.instance
        img_path = saved_object.photo.path
        # bi_data["bi_lstm_input"] = Cloth_SpecificSerializer(
        #     Cloth_Specific.objects.get(photo=bi_lstm_input)).data

        bi_data["id"] = id
        bi_data["style"] = style
        bi_data["season"] = season
        bi_data["bi_lstm_input"] = img_path
        print("bi_data:")
        print(bi_data)
        #  send_data = {
        #         "id": id,
        #         "bi_lstem_input":

        #         "style": style,
        #         # "data": {"id": 3, "season": ["HWAN", "SUMMER"], "category": "TOP", "style": ["CASUAL"]}
        #         "season": season
        #     }
        print("sending")
        print(bi_data)
        encoded = jsonpickle.encode(bi_data)
        r = requests.get(
            'http://141.223.121.163:9999/getSet/', json=encoded)
        print(r)
        print(r.text)
        # print(r.json)
        # print(r.json['clothlist'])
        # print(r.json.get(""))
        #decoded = jsonpickle.decode(r)
        # print("decoded:")
        # print(decoded)
        resu = r.text
        print(type(resu))
        real_dic = json.loads(resu)
        print(real_dic)
        print(real_dic['clothlist'])
        resssss = []
        if(real_dic['clothlist'] == None):
            pass

        else:
            print("____")
            print(type(real_dic))

            for rs in real_dic['clothlist']:
                resssss.append(rs.replace(
                    "/home/buttonteam/Button_Server2/button/media/", ""))

        print(resssss)
        # print("-----------------------")
        # print(decoded['clothlist'])
        # print(r.headers)
        # print(r.content)
        # print(r.content['clothlist'])
        # print(r.headers.get('clothlist'))
        # print(r.json)
        # print(r.json['clothlist'])
        # decoded = jsonpickle.decode(r)
        # res_=r.data.get('clothlist')
        # print(res_)
        #res = r.GET['clothlist']
        # print("res:")
        # print(res)
        # print(r)
        #bi_lstm_output = set_generation(bi_data)
        #bi_lstm_output = ["121.jpg", "56.jpg", "442.jpg", "395.jpg"]
        bi_lstm_output = resssss.copy()
        #bi_lstm_output = res
        bi_lstm_result = []
        print("output of bi_lstm")
        print(bi_lstm_output)
        for cloth_result in bi_lstm_output:
            print(cloth_result)
            bi_lstm_result.append(
                Cloth_Specific.objects.get(photo=cloth_result))
        if rand_cloth.get_category() == "TOP":
            print("TOP")
            result = is_valid_outfit_top(
                bi_lstm_result[::-1], id, rand_cloth, season)
            print(ret_result)
            if result == "redo":
                ret_result = False
            else:
                ret_result = True
        else:
            print("DRESS")
            result = is_valid_outfit_dress(
                bi_lstm_result[::-1], id, rand_cloth, season)
            print(ret_result)
            ret_result = True
    print("hi")
    return result


@ api_view(['GET'])
def week_recommendation(request, id, season):
    try:
        user = User.objects.get(id=id)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        style = ""
        knns_casual = KNN.objects.filter(id=id, style="CASUAL")
        knns_semi = KNN.objects.filter(id=id, style="SEMI-FORMAL")
        knns_formal = KNN.objects.filter(id=id, style="FORMAL")
        knns_outdoor = KNN.objects.filter(id=id, style="OUTDOOR")
        knns_vacance = KNN.objects.filter(id=id, style="VACANCE")

        sizeknn = max(len(knns_casual), len(knns_semi), len(
            knns_formal), len(knns_outdoor), len(knns_vacance))
        if sizeknn == 0:
            style = "CASUAL"
            # return Response({"response": "no knn data"})
        else:
            for i in [knns_casual, knns_semi, knns_formal, knns_outdoor, knns_vacance]:
                if len(i) == sizeknn:
                    print(i)
                    style = i[0].get_style()
                    break

        print(style)
        if season == "WINTER" and style == "VACANCE":
            style = "CASUAL"
        week_ = []
        for i in range(0, 7):
            res_ = run_rec_algo(id, style, season)
            if res_ == "does not exist":
                return Response({"response": "not enough clothes"})
            elif res_ == "more clothes":
                return Response({"response": "not enough clothes"})
            else:
                serializer = Cloth_SpecificSerializer(res_, many=True)
                week_.append(serializer.data)
        print(week_)
        return Response(week_, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def get_randomCloth(id, style, season):
    print("inside rand")
    print(season)
    try:
        closet_style = []
        user_closet = Cloth_Specific.objects.filter(
            id=id).exclude(category="OUTER").exclude(category="BOTTOM")
        print(user_closet)
        for clothes in user_closet:
            print(clothes)
            style_ = clothes.get_style()
            seasons = clothes.get_season()
            if style in style_:
                print("*****")
                for se in seasons:
                    if se in season:
                        closet_style.append(clothes)
                        break
    except Cloth_Specific.DoesNotExist:
        return "does not exist"
    print("list")
    print(closet_style)
    # print("-----")
    # print(len(closet_style))
    if len(closet_style) == 0:
        return "does not exist"
    else:
        index = random.randrange(0, len(closet_style))
        print(index)
        print(len(closet_style))
        rand_cloth = closet_style[index]
        # rand_cloth = random.choice(closet_style)
    # print(rand_cloth)
        return rand_cloth

# def random_cordi_week(id,season_input):


def is_valid_outfit_top(bi_lstm_result, id, rand_cloth, season_input):
    valid = False
    index = 0
    leng = len(bi_lstm_result)
    # print(leng)
    outfit = [rand_cloth]
    outfit2 = []
    cat = ["BOTTOM", "OUTER"]
    season = season_input
    # print("&&&&&")
    # print(season)
    season_valid = []
    for i in range(0, leng):
        season_valid.append(False)
    # print(season_valid)
    # print(bi_lstm_result)
    bi_lstm_results = bi_lstm_result.copy()
    # print(bi_lstm_results)
    # 계절 맞지 않는 옷 빼기
    for j in range(0, leng):
        # print(j)
        ses = bi_lstm_result[j].get_season()
        # print("$$$")
        # print(ses)
        while season_valid[j] != True:
            for s in ses:
                # print("@@@@")
                # print(s)
                if s in season:
                    season_valid[j] = True
                    # print(j)
                    break
                # print(j)
            if season_valid[j] == False:
                season_valid[j] = True
                bi_lstm_results.remove(bi_lstm_result[j])

    # print(bi_lstm_results)
    # print(season_valid)
    # print("******")
    while index < len(bi_lstm_results):
        if bi_lstm_results[index].get_category() == "BOTTOM":
            if "BOTTOM" in cat:
                outfit.append(bi_lstm_results[index])
                cat.remove("BOTTOM")
                valid = True
            index = index+1
        elif bi_lstm_results[index].get_category() == "OUTER":
            if "OUTER" in cat:
                outfit.append(bi_lstm_results[index])
                outfit2.append(bi_lstm_result[index])
                cat.remove("OUTER")
            index = index+1
        elif bi_lstm_results[index].get_category() == "DRESS":
            outfit2.append(bi_lstm_results[index])
            index = index+1
        else:
            index = index+1

    print(outfit)
    if valid == True:
        return outfit
    elif valid == False and len(outfit2) > 0:
        return outfit2
    else:
        return "redo"


def is_valid_outfit_dress(bi_lstm_result, id, rand_cloth, season_input):
    # print("DRESS")
    valid = True
    index = 0
    leng = len(bi_lstm_result)
    # print(leng)
    outfit = [rand_cloth]
    cat = ["OUTER"]
    season = season_input
    # print("&&&&&")
    # print(season)

    while index < len(bi_lstm_result):
        if bi_lstm_result[index].get_category() == "OUTER":
            if "OUTER" in cat:
                season_ = bi_lstm_result[index].get_season()
                for se in season_:
                    if se in season:
                        outfit.append(bi_lstm_result[index])
                        cat.remove("OUTER")
                        break
            index = index+1
        else:
            index = index+1

    print(outfit)
    if valid == True:
        return outfit
    else:
        return "redo"


@ api_view(['GET'])
def get_knnResult(request, KNNID):
    try:
        result = KNN.objects.get(KNNID=KNNID)

    except KNN.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = KNN_Serializer(result)
        return Response(serializer.data)


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

            absurl = 'https://'+current_site+relativeLink + \
                "?email="+str(account.get_email())
            email_body = ""+str(account.get_nickname()) + "님, 안녕하세요.\n옷장 관리 및 코디 어플 \'button\'입니다.\n\n"\
                '저희 버튼에 회원가입을 해주셔서 감사합니다.\n아래 링크로 이메일 인증을 완료해주세요\n '+absurl

            data_ = {'email_body': email_body, 'to_email': str(account.get_email()),
                     'email_subject': '이메일 인증'}
            Util.send_email(data_)

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET'])
def findEmail(request, userEmail):
    if request.method == 'GET':
        if (User.objects.filter(userEmail=userEmail)):
            return Response({'exists': True})
        else:
            return Response({'exists': False})


@ api_view(['GET'])
def retLoggedUser(request, userEmail):
    try:
        user_personal = User.objects.get(userEmail=userEmail)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = User_Serializer2(user_personal)
        return Response(serializer.data)


@ permission_classes([IsAuthenticated])
@ api_view(['GET'])
def user_list(request):
    # 모든 사용자 보기 & 추가
    if request.method == 'GET':
        users = User.objects.all()
        serializer = User_Serializer(users, many=True)
        # permission_classes = [IsAuthenticated]
        return Response(serializer.data)


@ api_view(['GET', 'PATCH'])
@ permission_classes([FriendListPermission | OwnerPermission | IsAuthenticated])
def user_detail(request, id):
    try:
        user_personal = User.objects.get(id=id)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if request.method == 'GET':
        serializer = User_Serializer(user_personal)
        return Response(serializer.data)
    if request.method == 'PATCH':
        serializer = User_Serializer(
            user_personal, data=request.data, partial=True)
        print("request.data")
        print(request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            # user_personal.save()
            print("success in patch")
            # return Response(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


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

    if request.method == 'PATCH':
        serializer = User_Serializer(
            user_personal, data=request.data, partial=True)
        print(user_personal)
        print("request.data")
        print(request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            # user_personal.save()
            print("success in patch")
            # return Response(serializer.data)
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
        print(closet)
        print(serializer.data)
        return Response(serializer.data)

    # POST부분 authentication 추가!!!
    elif request.method == 'POST':
        # 밑 세줄 지우고 data=request.data로!
        # photo = request.FILES["photo"]
        # data = json.loads(request.data['data'])
        # data["photo"] = photo
        # serializer = Cloth_SpecificSerializer(data=data)
        serializer = Cloth_SpecificSerializer(data=request.data)
        if serializer.is_valid():
            print(request.data)
            # da = request.data.get('data')
            # print(da)
            # da_season = da[0]
            # print(da_season)
            serializer.save()
            saved_object = serializer.instance
            img_path = saved_object.photo.path
            # print(request.data['season'])
            print(serializer.data.get('season'))
            # s = serializer.data['season']
            # sa = s.copy()
            # print(sa)
            se_ = serializer.data.get('season')
            style = serializer.data.get('style')
            print(style)

            # if "HWAN" in da_season:
            #     se_.append("HWAN")
            # if "WINTER" in da_season:
            #     se_.append("WINTER")
            # if "SUMMER" in da_season:
            #     se_.append("SUMMER")
            # cloth_post = Cloth_Specific.objects.get(
            #     id=id, clothID=request.data["clothID"])
            # print(request.data.get("season"))
            # for s in request.data.get("season"):
            #     se_.append(s)
            print(se_)
            # jsonpickle.encode(se_)
            send_data = {
                "id": id,
                "photo": img_path,
                # "data": {"id": 3, "season": ["HWAN", "SUMMER"], "category": "TOP", "style": ["CASUAL"]}
                "season": se_
            }
            print("sending")
            print(send_data)
            encoded = jsonpickle.encode(send_data)
            print(send_data)
            r = requests.post(
                'http://141.223.121.163:9999/postCloth/', json=encoded)
            print(r)
            # serializer.save()
            # closet_ = Cloth_Specific.objects.filter(id=id)
            # number_ = len(closet_)-1
            # print(number_)
            # extract_features(id, serializer.data)
            print("end extract")
            # seasons = request.data.get('season')
            # tf = []
            # for i in range(0, 4):
            #     tf.append(False)
            # if "SPRING" in seasons:
            #     tf[0] = True
            # if "SUMMER" in seasons:
            #     tf[1] = True
            # if "FALL" in seasons:
            #     tf[2] = True
            # if "WINTER" in seasons:
            #     tf[3] = True

            # if tf[3] == True:
            #     extract(id, serializer.data, number, "winter")
            # if tf[1] == True:
            #     extract(id, serializer.data, number, "summer")
            # if tf[0] == True or tf[2] == True:
            #     extract(id, serializer.data, number, "hwan")

            # extract feature!!
            # closet_=Cloth_Specific.objects.filter(id=id)
            # serializer_ = Cloth_SpecificSerializer(closet_, many=True)
            # extract(id,serializer.data,number)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET'])
@ parser_classes([MultiPartParser])
@ permission_classes([FriendListPermission | OwnerPermission])
def cloth_list_season(request, id, season):
    print("season="+str(season))
    if request.method == 'GET':
        closet = Cloth_Specific.objects.filter(id=id)
        clo = []
        for clothes in closet:
            ses = clothes.get_season()
            if season in ses:
                clo.append(clothes)

        print(closet)
        print(clo)

        serializer = Cloth_SpecificSerializer(clo, many=True)
        print(serializer)
        return Response(serializer.data)


# @ api_view(['GET'])
# @ parser_classes([MultiPartParser])
# @ permission_classes([FriendListPermission | OwnerPermission])
# def cloth_list_season(request, id, days_not_worn):
#     if request.method == 'GET':
#         closet = Cloth_Specific.objects.filter(id=id)


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
            ' 님 안녕하세요.\n옷장 관리 및 코디 어플 \'button\'입니다.\n\n임시 비밀번호: ' + \
            result_str+'\n로그인을 한 후 반드시 비밀번호를 변경해 주시기 바랍니다.'
        # email_body.attach(logo_data())
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    user = request.user
<<<<<<< HEAD
<<<<<<< HEAD
    # if id != user.id:
=======
   # if id != user.id:
>>>>>>> 35aa25d... last last
    # return Response({'response': "You don't have permission for access!"})
=======
=======
    user=request.user
>>>>>>> 6951918... change season field
=======
    user = request.user
>>>>>>> 5758d9e... change season field3
=======
    user=request.user
>>>>>>> 53e5b62... change season field10
=======
    user = request.user
>>>>>>> 891885e... change season field11
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

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    user = request.user
<<<<<<< HEAD
=======
=======
    user=request.user
>>>>>>> 6951918... change season field
=======
    user = request.user
>>>>>>> 5758d9e... change season field3
=======
    user=request.user
>>>>>>> 53e5b62... change season field10
=======
    user = request.user
>>>>>>> 891885e... change season field11

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
        print("PUT request.data")
        print(request.data)
        serializer = Cloth_SpecificSerializer(cloth, data=request.data)
        if serializer.is_valid():
            serializer.save()
            saved_object = serializer.instance
            img_path = saved_object.photo.path
            se_ = serializer.data.get('season')
            send_data = {
                "id": id,
                "photo": img_path,
                "season": se_
                # "data": {"id": 3, "season": ["HWAN", "SUMMER"], "category": "TOP", "style": ["CASUAL"]}
                # "data": serializer.data
            }
            print(send_data)
            encoded = jsonpickle.encode(send_data)
            r = requests.post(
                'http://141.223.121.163:9999/changeCloth/', json=encoded)
            print(r)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = Cloth_SpecificSerializer(cloth, data=request.data)
        if serializer.is_valid():
            serializer.save()
            saved_object = serializer.instance
            img_path = saved_object.photo.path
            se_ = serializer.data.get('season')
            send_data = {
                "id": id,
                "photo": img_path,
                "season": se_
                # "data": {"id": 3, "season": ["HWAN", "SUMMER"], "category": "TOP", "style": ["CASUAL"]}
                # "data": serializer.data
            }
            print(send_data)
            encoded = jsonpickle.encode(send_data)
            r = requests.post(
                'http://141.223.121.163:9999/changeCloth/', json=encoded)
            print(r)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        outfits = Outfit_Specific.objects.filter(clothes=clothID)
        print("hihihihi")
        print(outfits)
        for out in outfits:
            out.delete()
        print("request.data")
        print(request.data)
        serializer = Cloth_SpecificSerializer(cloth)
        # print(serializer.is_valid())
        # if serializer.is_valid():
        print("valid")
        saved_object = serializer.instance
        img_path = saved_object.photo.path
        se_ = serializer.data.get('season')
        send_data = {
            "id": id,
            "photo": img_path,
            "season": se_
            # "data": {"id": 3, "season": ["HWAN", "SUMMER"], "category": "TOP", "style": ["CASUAL"]}
            # "data": serializer.data
        }
        print(send_data)
        encoded = jsonpickle.encode(send_data)
        r = requests.post(
            'http://141.223.121.163:9999/deleteCloth/', json=encoded)
        print(r)
        print("cloth:")
        print(cloth)
        cloth.delete()
        # outfitIDS = cloth.get_outfit()
        # print(outfitIDS)
        # #outfits =[]
        # for i in outfitIDS:
        #     outfit = Outfit_Specific.objects.get(id=i)
        #     print(outfit)
        #     outfit.delete()

        # for out in outfits:
        #     out.delete()
        # return Response(status=status.HTTP_201_CREATED)
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

=======
>>>>>>> c7b0972... add outfit check
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
        outfit_closet = Outfit_Specific.objects.filter(
            id=id, outfitBy=id)
        serializer = OutfitSerializer(outfit_closet, many=True)
        return Response(serializer.data)


@ api_view(['GET'])
@ permission_classes([FriendListPermission | OwnerPermission])
def outfit_list_all(request, id):
    user = request.user
    # if id != user.id:
    #     return Response({'response': "You don't have permission for access!"})
    if request.method == 'GET':
        outfit_closet = Outfit_Specific.objects.filter(
            id=id)
        serializer = OutfitSerializer(outfit_closet, many=True)
        return Response(serializer.data)


@ api_view(['GET'])
@ permission_classes([FriendListPermission | OwnerPermission])
def outfit_list_friend(request, id):
    user = request.user
    # if id != user.id:
    #     return Response({'response': "You don't have permission for access!"})
    if request.method == 'GET':
        outfit_closet = Outfit_Specific.objects.filter(
            id=id).exclude(outfitBy=id)
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
        outfit = Outfit_Specific.objects.get(outfitID=outfitID)
        userrr = User.objects.get(id=id)
        # print(request.id)

    except Outfit_Specific.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if request.method == 'PATCH':
        serializer = OutfitSerializer(outfit, data=request.data)
        if serializer.is_valid():
            print("outfitby: "+str(id)+"   owner:"+str(outfit.get_owner()))
            if outfit.get_outfitby() != userrr and outfit.get_owner() != userrr:
                return Response({"response": "cannot modify cloth"})
            else:
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        print("outfitby: "+str(outfit.get_outfitby()) +
              "   owner:"+str(outfit.get_owner())+"   id:"+str(id))
        if outfit.get_outfitby() != userrr and outfit.get_owner() != userrr:
            print("not outfitby and not owner")
            return Response({"response": "cannot delete cloth"})
        # elif outfit.get_outfitby() == id:
        #     print("is outfitby")
        #     outfit.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            outfit.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'GET':
        serializer = OutfitSerializer(outfit)
        return Response(serializer.data)


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
    if request.method == 'DELETE':
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
        print("posttttt")
        if not Friend.objects.filter(user=User.objects.get(id=id), frienduser=reciever).exists():
            new_friend = Friend()
            new_friend.user = User.objects.get(id=id)
            new_friend.frienduser = User.objects.get(
                userEmail=userEmail)
            new_friend.save()

        # user = User.objects.get(id=id)
            senderEmail = user.get_email()
        # reciever = User.objects.get(userEmail=userEmail)
            recieverEmail = userEmail

            current_site = get_current_site(request).domain
            relativeLink = reverse('verify-friend')

            absurl = 'https://'+current_site+relativeLink + \
                "?email="+str(recieverEmail)+"&sender="+str(senderEmail)
            email_body = ""+str(reciever.get_nickname()) + "님, 안녕하세요.\n옷장 관리 및 코디 어플 \'button\'입니다.\n\n" \
                + str(user.get_nickname()) + \
                "님이 친구 요청을 보냈습니다.\n아래 링크를 클릭해 친구요청을 수락해주세요.\n"+absurl

            data_ = {'email_body': email_body, 'to_email': str(recieverEmail),
                     'email_subject': '친구 요청'}
            Util.send_email(data_)

            return Response({'email': 'Successfully sent'}, status=status.HTTP_201_CREATED)
        elif Friend.objects.filter(user=User.objects.get(id=id), frienduser=reciever, accepted=False).exists():
            return Response({'email': 'already sent request'}, status=status.HTTP_400_BAD_REQUEST)
        elif Friend.objects.filter(user=User.objects.get(id=id), frienduser=reciever, accepted=True).exists():
            return Response({'email': 'already friend'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'email': 'ERROR'}, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET'])
@ permission_classes((IsAuthenticated, OwnerPermission))
def get_friendRequest(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'response': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        req = Friend.objects.filter(frienduser=user, accepted=False)
        serializer = Friend_Serializer(req, many=True)
        print(req)
        print(serializer.data)
        return Response(serializer.data)


@ api_view(['POST', 'DELETE'])
@ permission_classes((IsAuthenticated, OwnerPermission))
def accept_friendRequest(request, id, friendID):
    try:
        req = Friend.objects.get(
            frienduser=User.objects.get(id=id), accepted=False, user=User.objects.get(id=friendID))
    except Friend.DoesNotExist:
        return Response({'response': 'friendRequest not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        if not req.accepted:
            req.accepted = True
            req.save()
            new_friend = Friend()
            new_friend.user = User.objects.get(id=friendID)
            new_friend.frienduser = User.objects.get(id=id)
            new_friend.accepted = True
            new_friend.save()
        return Response({'friend': 'Successfully added'}, status=status.HTTP_201_CREATED)
    return Response({'friend': 'ERROR'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        req.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


@ api_view(['POST', 'PATCH'])
@ permission_classes([IsAuthenticated | OwnerPermission])
def saveToCalendar(request, id, outfitID, year, month, day):
    try:
        user = User.objects.get(id=id)
        outfit = Outfit_Specific.objects.get(outfitID=outfitID)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Outfit_Specific.DoesNotExist:
        print("outfit not found")
        return Response({'outfit': 'not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        month_ = str(month)
        if month < 10:
            month_ = "0"+str(month)
        day_ = str(day)
        if day < 10:
            day_ = "0"+str(day)
        date_ = str(year)+"-"+month_+"-"+day_
        request.data['date'] = date_
        # request.data['outfit_worn'] = outfit.outfitID
        print(request.data)
        print("-------")
        serializer = CalendarSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            cal = Calendar_Specific.objects.get(id=id, date=date_)
            cal.outfit_worn = outfit
            cal.save()
            print(cal)
            # outfit.date_worn.add(
            # Calendar_Specific.objects.get(id=id, date=date_))
            # outfit.save()
            count = outfit.get_count()+1
            outfit.count = count
            outfit.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET', 'DELETE', 'PATCH'])
@ permission_classes([IsAuthenticated | OwnerPermission])
def getCalendar_specific_date(request, id, year, month, day):
    month_ = str(month)
    if month < 10:
        month_ = "0"+str(month)
    day_ = str(day)
    if day < 10:
        day_ = "0"+str(day)
    date_ = str(year)+"-"+month_+"-"+day_
    try:
        user = User.objects.get(id=id)
        calendar = Calendar_Specific.objects.get(date=date_, id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    except Calendar_Specific.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        calendar.outfit_worn.count = calendar.outfit_worn.get_count()-1
        calendar.outfit_worn.save()
        calendar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        serializer = CalendarSerializer(calendar, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['POST'])
@ permission_classes([IsAuthenticated | OwnerPermission])
def change_Outfit_Calendar(request, id, calendarID, outfitID):
    try:
        cal = Calendar_Specific.objects.get(calendarID=calendarID, id=id)
        outfit = Outfit_Specific.objects.get(outfitID=outfitID)
    except Calendar_Specific.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Outfit_Specific.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        cal.outfit_worn.count = cal.outfit_worn.get_count()-1
        cal.save()
        cal.outfit_worn.save()
        cal.outfit_worn = outfit
        outfit.count = outfit.get_count()+1
        outfit.save()
        cal.save()
        return Response(status=status.HTTP_201_CREATED)


@ api_view(['GET'])
@ permission_classes([IsAuthenticated | OwnerPermission])
def getCalendar_all(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        calendar = Calendar_Specific.objects.filter(id=id)
        # if calendar.:
        #     return Response({'calendar': 'no data'}, status=status.HTTP_201_CREATED)
        serializer = CalendarSerializer(calendar, many=True)
        return Response(serializer.data)


@ api_view(['GET'])
@ permission_classes([IsAuthenticated | OwnerPermission])
def getCalendar_month(request, id, year, month):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        month_ = str(month)
        if str(month) == "1" or str(month) == "2" or str(month) == "3" or str(month) == "4" or str(month) == "5" or str(month) == "6" or str(month) == "7" or str(month) == "8" or str(month) == "9":
            month_ = "0"+str(month)
        date__ = str(year)+"-"+str(month_)+"-"
        print("__date__")
        print(date__)
        calendar = Calendar_Specific.objects.filter(id=id)
        print("calendar")
        print(calendar)
        calendar__ = []
        for cal in calendar:
            datee = str(cal.get_date())
            print("datee")
            print(datee)
            if date__ in datee:
                calendar__.append(cal)
                print("add")

        print(calendar__)
        # if calendar.:
        #     return Response({'calendar': 'no data'}, status=status.HTTP_201_CREATED)
        serializer = CalendarSerializer(calendar__, many=True)
        return Response(serializer.data)


@ api_view(['GET'])
@ permission_classes([IsAuthenticated | OwnerPermission])
def outfit_stats_best5(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        outfit_list = Outfit_Specific.objects.filter(id=id).order_by('count')
        # best_worn = sorted(outfit_list, key=(lambda x: x['count']))
        outfit_list_ = outfit_list[::-1]
        serializer = OutfitSerializer(outfit_list_[:4], many=True)
        return Response(serializer.data)


@ api_view(['GET'])
@ permission_classes([IsAuthenticated | OwnerPermission])
def outfit_stats_worst5(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        outfit_list = Outfit_Specific.objects.filter(id=id).order_by('count')
        # best_worn = sorted(outfit_list, key=(lambda x: x['count']))
        serializer = OutfitSerializer(outfit_list[:4], many=True)
        return Response(serializer.data)
# @ api_view(['GET','POST'])
# @ permission_classes([IsAuthenticated | OwnerPermission])
# def bi_lstm(request, id):
#     try:
#         user = User.objects.get(id=id)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         calendar = Calendar_Specific.objects.filter(id=id)
#         # if calendar.:
#         #     return Response({'calendar': 'no data'}, status=status.HTTP_201_CREATED)
#         serializer = CalendarSerializer(calendar, many=True)
#         return Response(serializer.data)
