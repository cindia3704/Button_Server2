from django.urls import path, include
from .views import user_list, user_detail, cloth_list, cloth_detail, register, findEmail, user_detail_change, user_delete, cloth_category_list, VerifyEmail
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
    # 사용자 info 수정
    path('user/<int:id>/delete/', views.user_delete),
    # 로그인
    path('login/', obtain_auth_token, name="login"),
    # 회원가입
    path('register/', views.register),
    # 이메일 인증
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    # # 비번 바꾸기
    #path('user/<int:id>/changePassword/', ChangePasswordView.as_view()),
    # # 비번 찾기
    # path('email-find/<userEmail>/', views.findPassword, name="email-find"),
    #path('email-find', views.send_email_findPassword, name="email-find")
    # 이메일 찾기
    path('user/findEmail/<userEmail>/', views.findEmail),
    # 한 사용자의 모든 옷 보여주기
    path('closet/<int:id>/', views.cloth_list),
    # 옷의 세부 정보
    path('closet/<int:id>/<int:clothID>/', views.cloth_detail),

    # 옷의 카테고리별로 보기 (GET)
    path('closet/<int:id>/<category>/', views.cloth_category_list),

    # 추천알고리즘 통한 의상 추천 보기 (GET)
    # path('<int:id>/recommend/ml')

    # 직접 코디한거 저장하기(POST)
    # path('<int:id>/saveTryMyself/')

    # 직접 코디한거 보기 (GET)
    # path('<int:id>/recommend/mySelf/')

    # 한동안 안입은 옷 보기 (GET)
    # path('<int:id>/recommend/outdated/')

    # 매일 뭐입는지 저장 (POST)
    # path('<int:id>/myfashiontoday/')

    # 그동안 뭐입었는지 보기 (GET)
    # path('<int:id>/myfashion/')

    # 친구리스트

    # 친구 한명꺼 들어가기(옷정보)

    # 친구 코디 저장



]
