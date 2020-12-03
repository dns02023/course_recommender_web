from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from lecture_app.models import Lecture
from django.contrib import messages
import logging
import elasticsearch

es = elasticsearch.Elasticsearch("localhost:9200")

logger = logging.getLogger(__name__)

def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile = profile_form.save(commit=False)

            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')

            # credential 매개변수들이 유효하다면, 해당되는 User 객체를 반환해준다.
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            profile.user = user
            # 로그인 전까지는 anonymous user 객체이므로 user 객체를 매핑 할 수 없어서
            # authenticate, login 과정을 거친 후 user 객체가 로그인되면 프로필에 매핑
            profile.save()
            return redirect('index')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, 'member_app/signup.html',
                  {
                      'user_form': user_form,
                      'profile_form': profile_form
                  })

@login_required(login_url='member_app:signin')
def mypage(request):
    user = request.user
    body1 = {
        "query": {
        "query_string": {
        "default_field": "user_id",
        "query": user.id
            }
          }
        }
    res1 = es.search(index='recommenders_db', body=body1)
    count = res1['hits']['total']['value']

    body2 = {
        "from": count - 1,
        "size": 1,

        "query": {
            "query_string": {
                "default_field": "user_id",
                "query": 1
            }
        }
    }
    res2 = es.search(index='recommenders_db', body=body2)
    rec_ids = res2['hits']['hits'][-1]['_source']['best']
    recommends = list()
    for rec_id in rec_ids:
        rec = get_object_or_404(Lecture, pk=rec_id)
        recommends.append(rec)

    context = {'user': user, 'recommends': recommends}
    return render(request, 'member_app/mypage.html', context)

@login_required(login_url='member_app:signin')
def wish(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    if lecture in request.user.profile.wish_lectures.all():
        messages.error(request, '이미 담은 강의입니다.')
    else:
        request.user.profile.wish_lectures.add(lecture)
        lecture.wish_users.add(request.user.profile)
        # 담아두기 로그 수집
        logger.info('{} {} {}'.format(request.user.id, 'WISH', lecture.id))

    return redirect('index')

@login_required(login_url='member_app:signin')
def wish_cancel(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    if lecture not in request.user.profile.wish_lectures.all():
        messages.error(request, '담아두지 않은 강의입니다.')
    else:
        request.user.profile.wish_lectures.remove(lecture)
        lecture.wish_users.remove(request.user.profile)

    return redirect('member_app:mypage')





