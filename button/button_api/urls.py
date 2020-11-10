from django.urls import path, include
from .views import user_list, user_detail, cloth_list, cloth_detail, register, findEmail, user_detail_change, user_delete, cloth_category_list, VerifyEmail, saveOutfit, outfit_list, outfit_change, retLoggedUser, VerifyFriendRequest, send_friendRequest, get_friendlist, get_acceped_friendlist, post_userInput, get_knnResult, outfit_cloth_add, outfit_cloth_del, outfit_cloth_change, change_password, find_password, getCalendar_specific_date, getCalendar_all, saveToCalendar, change_Outfit_Calendar, cloth_list_season, outfit_stats_best5, outfit_stats_worst5, getCalendar_month
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    # 모든 사용자 리스트 보기
    path('user/', views.user_list),
    # 사용자 한명 info 보기 -- change info 가능
    path('user/<int:id>/', views.user_detail),
    # 사용자 info 수정
    path('user/<int:id>/changeInfo/', views.user_detail_change),
    # 사용자 info 삭제
    path('user/<int:id>/delete/', views.user_delete),
    # 로그인
    path('login/', obtain_auth_token, name="login"),

    # 로그인된 사용자 정보
    path('login/<userEmail>/', views.retLoggedUser),
    # 회원가입
    path('register/', views.register),
    # 이메일 인증
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    # # 비번 바꾸기
    # path('user/<int:id>/changePassword/<changed>/', views.changePassword),
    # 비번 찾기
    path('passwordfind/<userEmail>/', views.find_password, name="find-password"),
    # path('email-find', views.send_email_findPassword, name="email-find")
    # 이메일 찾기
    path('user/findEmail/<userEmail>/', views.findEmail),
    # 한 사용자의 모든 옷 보여주기
    path('closet/<int:id>/', views.cloth_list),

    # 사용자 봄옷
    path('closet/<int:id>/getseason/<season>/', views.cloth_list_season),
    #     # 사용자 여름옷
    #     path('closet/<int:id>/spring/', views.cloth_list_spring),
    #     # 사용자 가을옷
    #     path('closet/<int:id>/spring/', views.cloth_list_spring),
    #     # 사용자 겨울옷
    #     path('closet/<int:id>/spring/', views.cloth_list_spring),
    # 옷의 세부 정보
    path('closet/<int:id>/<int:clothID>/', views.cloth_detail),

    # 옷의 카테고리별로 보기 (GET)
    path('closet/<int:id>/<category>/', views.cloth_category_list),

    # 직접 코디한거 저장하기(POST)
    path('<int:id>/outfit/', views.saveOutfit),

    # 직접 코디한거 보기 (GET)
    path('<int:id>/outfit/list/', views.outfit_list),

    # 직접 코디한 outfit 수정(GET/PATCH/DELETE)
    path('<int:id>/outfit/list/<int:outfitID>/', views.outfit_change),

    # 한동안 안입은 옷 보기 (GET)
    # path('<int:id>/recommend/outdated/')

    # 추천알고리즘 사용자 input 올리기 (POST)
    path('knn/', views.post_userInput),

    # knn result 보기 (GET)
    path('knn/<int:KNNID>/', views.get_knnResult),
    # 추천알고리즘 통한 의상 추천 보기 (GET)
    # path('<int:id>/recommend/ml')
    # outfitID 에 clothID 옷 추가
    path('<int:id>/<int:outfitID>/addcloth/<int:clothID>/', views.outfit_cloth_add),
    # outfitID 에 clothID 옷 삭제
    path('<int:id>/<int:outfitID>/delcloth/<int:clothID>/', views.outfit_cloth_del),
    # outfitID에 있는 clothID1 을 clothID2로 바꾼다.
    path('<int:id>/<int:outfitID>/changecloth/<int:clothID1>/to/<int:clothID2>/',
         views.outfit_cloth_change),
    path('<int:id>/changepassword/', views.change_password),
    # 매일 뭐입는지 저장 (POST)
    # path('<int:id>/myfashiontoday/')
    # path('<int:id>/myfashiontoday/<date')
    # 그동안 뭐입었는지 보기 (GET)
    # path('calendar/<int:id>/<datesWorn>/', views.get_clothes_worn),

    # 친구리스트 모두 보기-- accept 안된 것도!
    path('friendlist/<int:id>/', views.get_friendlist),

    # 친구리스트 accept된것만 보기
    path('friendlist/accepted/<int:id>/', views.get_acceped_friendlist),

    # 친구 상세정보 & 삭제하기
    path('friendlist/<int:id>/<int:friendId>/', views.specific_friend),
    # 친구 추가
    path('<int:id>/addfriend/<userEmail>/', views.send_friendRequest),
    # 친구 이메일 인증
    path('verify-friend/', views.VerifyFriendRequest.as_view(), name="verify-friend"),

    # 캘린더에 추가하기
    path('addToCalendar/<int:id>/<int:outfitID>/<int:year>/<int:month>/<int:day>/',
         views.saveToCalendar),
    # 캘린더에서 어떤 날짜꺼 갖고오기(GET,DELETE,PATCH)
    path('getCalendar/<int:id>/<int:year>/<int:month>/<int:day>/',
         views.getCalendar_specific_date),
    # 캘린더에서 모두 갖고오기(GET)
    path('getCalendar/<int:id>/',
         views.getCalendar_all),
     # 캘린더에서 해당 달 갖고오기 
    path('getCalendar/<int:id>/<int:year>/<int:month>/',
         views.getCalendar_month),
    # 캘린더 아웃핏 바꾸기
    path('changeCalendar/<int:id>/<int:calendarID>/<int:outfitID>/',
         views.change_Outfit_Calendar),
    # 아웃핏 statistic
    path('outfitStatsBest/<int:id>/', views.outfit_stats_best5),
    path('outfitStatsWorst/<int:id>/', views.outfit_stats_worst5)

    # 일주일치 옷 추천 ('POST'),GET
    # path('weekRecommend/<int:id>/')

]
