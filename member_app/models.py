from django.db import models
from django.contrib.auth.models import User
from lecture_app.models import Lecture

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    klue_name = models.CharField(max_length=50, unique=True, verbose_name='클루 연동 닉네임')
    # 즐겨찾기 등록한 lecture들은 어떻게 하지? => 다대다 관계
    wish_lectures = models.ManyToManyField(Lecture, blank=True, related_name='wish_users')

    # admin 페이지에서 출력명
    def __str__(self):
        return self.klue_name
    
    class Meta:
        db_table = 'profiles'


