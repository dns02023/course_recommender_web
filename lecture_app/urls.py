from django.urls import path
from . import views

app_name = 'lecture_app'
# 템플릿에 url 링크걸 때 app_name:url_name 으로 클린 코딩 가능
# + 다른 앱에 같은 url 이름이 있어도 app_name으로 구분 가능

urlpatterns = [
    path('', views.index, name='index'),
    # url_name = 'index'
    path('<int:lecture_id>/', views.lecture_detail, name='detail'),
]