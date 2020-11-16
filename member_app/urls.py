from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'member_app'

urlpatterns = [
    path('signin/', auth_views.LoginView.as_view(template_name='member_app/signin.html'), name='signin'),
    #loginview는 디폴트로 registration/login.html 이라는 경로의 템플릿 참조하므로 수정해줌
    path('signout/', auth_views.LogoutView.as_view(), name='signout'),
    path('signup/', views.signup, name='signup'),
    path('mypage/', views.mypage, name='mypage'),
    path('wish/add/<int:lecture_id>/', views.wish, name='wish'),
    path('wish/remove/<int:lecture_id>/', views.wish_cancel, name='wish_cancel'),



]