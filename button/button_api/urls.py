from django.urls import path, include
from .views import user_list, user_detail, cloth_list, cloth_detail, register, findEmail, login
from . import views

urlpatterns = [
    # 모든 사용자 리스트 보기
    path('user/', views.user_list),
    # 사용자 한명 info 보기 -- change info 가능
    path('user/<int:id>/', views.user_detail),
    # 로그인
    path('login/<userEmail>/<password>/', views.login),
    # 회원가입
    path('register/', views.register),
    # # 비번 바꾸기
    # path('user/<int:id>/changePassword/'),
    # # 비번 찾기
    # path('user/findPassword/'),
    # 이메일 찾기
    path('user/findEmail/<userEmail>/', views.findEmail),
    # 한 사용자의 모든 옷 보여주기
    path('closet/<int:id>/', views.cloth_list),
    # 옷의 세부 정보
    path('closet/<int:id>/<int:clothID>/', views.cloth_detail),



]
