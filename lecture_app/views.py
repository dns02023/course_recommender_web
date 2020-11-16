from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Lecture
from urllib.parse import quote
import logging

logger = logging.getLogger(__name__)

def index(request):
    page = request.GET.get('page', '1')
    lecture_list = Lecture.objects.order_by('id')

    paginator = Paginator(lecture_list, 50)
    page_obj = paginator.get_page(page)

    context = {'lecture_list' : page_obj}

    return render(request, 'lecture_app/lecture_list.html', context)

def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)

    # click 로그 수집
    if request.user.is_authenticated:
        logger.info('{} {} {}'.format(request.user.id, 'CLICK', lecture.id))

    lectid = lecture.lectid
    lectname = quote(lecture.lectname)
    professor = quote(lecture.professor)

    # 클루로 리다이렉트
    return redirect('https://klue.kr/lecture/search/' + lectid + ',' + lectname + ',' + professor)

